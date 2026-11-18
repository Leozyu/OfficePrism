import ast
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from bench.data_model.tasks import RewardType, Task
from bench.domains.hr.models import HRDB as DatabaseModel
from bench.domains.hr.tools import HRTools as DomainTools
from bench.domains.hr.utils import (
    BASE_DB_PATH,
    HR_DB_PATH,
    HR_POLICY_PATH,
    HR_TASK_SET_PATH,
)
from bench.environment.environment import Environment
from bench.environment.tool_discovery import ToolDiscoveryToolkit
from bench.utils import load_file


def _parse_tool_chain(answer_str: str) -> List[Dict[str, Any]]:
    """使用 Python AST 安全解析 tool chain 字符串为结构化 tool call 列表。"""
    if isinstance(answer_str, list):
        if all(isinstance(i, dict) for i in answer_str):
            return answer_str
        answer_str = str(answer_str)

    answer_str = answer_str.strip()
    if not answer_str:
        return []

    try:
        parsed = json.loads(answer_str)
        if isinstance(parsed, list) and all(isinstance(i, dict) for i in parsed):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    if not answer_str.startswith("["):
        answer_str = f"[{answer_str}]"

    calls = []
    try:
        tree = ast.parse(answer_str, mode='eval')
        if isinstance(tree.body, ast.List):
            for item in tree.body.elts:
                if isinstance(item, ast.Call):
                    name = item.func.id if isinstance(item.func, ast.Name) else str(item.func)
                    kwargs = {}
                    for kw in item.keywords:
                        if kw.arg:
                            try:
                                kwargs[kw.arg] = ast.literal_eval(kw.value)
                            except ValueError:
                                kwargs[kw.arg] = None
                    calls.append({"name": name, "kwargs": kwargs})
        return calls
    except SyntaxError as e:
        logger.warning(f"Tool chain parse failed: {answer_str} -> {e}")
        return []


def _is_read_only_tool_chain(tool_calls: List[Dict[str, Any]]) -> bool:
    """Best-effort check for GAIA reference chains that only inspect state."""
    if not tool_calls:
        return False
    read_prefixes = ("get_", "list_", "find_", "search_")
    return all(
        str(tool_call.get("name") or "").startswith(read_prefixes)
        for tool_call in tool_calls
    )


def _build_ticket(raw_task: dict[str, Any]) -> str:
    """把 GAIA 任务转成 solo agent 可直接执行的 ticket。"""
    question = (raw_task.get("question") or "").strip()
    business_scenario = (raw_task.get("business_scenario") or "").strip()
    caller = raw_task.get("caller") or {}
    caller_parts = []
    for k, v in caller.items():
        if v and k != "employment_status":
            caller_parts.append(f"{k}: {v}")
    caller_str = ", ".join(caller_parts) if caller_parts else "未知"
    from bench.domains.base.tools import SIM_NOW_TICKET_LINE

    lines = [
        f"提问人信息：{caller_str}",
        SIM_NOW_TICKET_LINE,
        f"问题：{question}",
        "要求：仅通过工具调用完成，并在最后输出明确结论。",
    ]
    return "\n".join(lines)


def _convert_gaia_task(raw_task: dict[str, Any]) -> dict[str, Any]:
    """将 GAIA 格式任务转换为 bench Task 格式。"""
    task_id = raw_task.get("task_id") or raw_task.get("id")
    question = raw_task.get("question") or ""
    business_scenario = raw_task.get("business_scenario") or ""
    final_answer = raw_task.get("expected_answer") or raw_task.get("final_answer") or ""
    level = (raw_task.get("level") or "UNKNOWN").upper()
    caller = raw_task.get("caller") or {}
    raw_nl_assertions = raw_task.get("nl_assertions")
    nl_assertions = (
        [str(item) for item in raw_nl_assertions if item]
        if isinstance(raw_nl_assertions, list)
        else ([final_answer] if final_answer else None)
    )
    raw_forbidden_tools = raw_task.get("forbidden_tools")
    forbidden_tools = (
        [str(item) for item in raw_forbidden_tools if item]
        if isinstance(raw_forbidden_tools, list)
        else None
    )
    is_cross_task = str(raw_task.get("domain") or "").lower() == "cross"

    answer_str = raw_task.get("tool_chain") or raw_task.get("answer") or ""
    tool_calls = _parse_tool_chain(answer_str)
    actions = []
    for idx, tool_call in enumerate(tool_calls, 1):
        kwargs = tool_call.get("kwargs") or {}
        actions.append(
            {
                "action_id": f"{task_id}_action_{idx}",
                "requestor": "assistant",
                "name": tool_call.get("name"),
                "arguments": kwargs,
                "compare_args": list(kwargs.keys()),
            }
        )

    read_only_reference = _is_read_only_tool_chain(tool_calls)

    known_info = []
    if business_scenario:
        known_info.append(f"业务背景：{business_scenario}")
    if caller.get("employee_ref"):
        known_info.append(f"发起人工号：{caller['employee_ref']}")

    description_notes = f"level={level};source_task_id={task_id}"
    return {
        "id": task_id,
        "description": {
            "purpose": question or business_scenario or "完成 HR 工单查询或办理",
            "notes": description_notes,
        },
        "user_scenario": {
            "persona": f"{caller.get('display_name', '员工')}（{caller.get('employee_ref', 'unknown')}）",
            "instructions": {
                "domain": str(raw_task.get("domain") or "hr").upper(),
                "reason_for_call": question or "请协助处理 HR 相关事项",
                "known_info": "\n".join(known_info) if known_info else None,
                "unknown_info": None,
                "task_instructions": question or "请根据 policy 完成该 HR 任务",
            },
        },
        "ticket": _build_ticket(raw_task),
        "initial_state": None,
        "evaluation_criteria": {
            "actions": actions,
            "nl_assertions": nl_assertions,
            "forbidden_tools": forbidden_tools,
            "reward_basis": (
                [RewardType.NL_ASSERTION.value]
                if nl_assertions
                and not forbidden_tools
                and (is_cross_task or read_only_reference)
                else [RewardType.ACTION.value, RewardType.NL_ASSERTION.value]
            ),
        },
    }


def get_environment(
    db: Optional[DatabaseModel] = None,
    solo_mode: bool = True,
    tool_mode: str = "full",
) -> Environment:
    """
    功能说明（Description）：
        获取环境，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `db` (Optional[DatabaseModel]): 数据库对象实例；为空时通常会走默认加载逻辑。 默认值为 `None`。
        - `solo_mode` (bool): 布尔开关参数，用于控制分支逻辑。 默认值为 `False`。
    返回（Returns）：
        - `Environment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    if db is None:
        # 分别加载 base 和 HR 数据
        base_data = load_file(BASE_DB_PATH)
        hr_data = load_file(HR_DB_PATH)
        
        # 合并数据
        merged_data = {**base_data, **hr_data}
        
        # 创建 DatabaseModel 实例
        db = DatabaseModel.model_validate(merged_data)
        
    tools = DomainTools(db)
    if tool_mode == "search":
        tools = ToolDiscoveryToolkit(tools)
    
    try:
        with open(HR_POLICY_PATH, "r") as fp:
            policy = fp.read()
    except FileNotFoundError:
        policy = "HR Domain Policy"

    env = Environment(
        domain_name="hr",
        policy=policy,
        tools=tools,
    )
    if solo_mode:
        env.set_solo_mode(True)
    return env


def get_tasks(task_path=None, save_to=None) -> list[Task]:
    """
    功能说明（Description）：
        获取任务列表，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `task_path` (Any): 业务入参，按函数语义传入。 默认值为 `None`。
        - `save_to` (Any): 业务入参，按函数语义传入。 默认值为 `None`。
    返回（Returns）：
        - `list[Task]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    if task_path is None:
        task_path = HR_TASK_SET_PATH
    
    logger.info(f"Load tasks from {task_path}")
    with open(task_path, "r") as fp:
        tasks = json.load(fp)
    
    if save_to is not None:
        tasks_dict = {t.get('task_id', t.get('id', '')): t for t in tasks}
        save_dir = str(save_to)
        if save_dir.endswith('.json'):
            save_dir = save_dir[:-len('.json')]
        
        processed_task_ids = set()
        if os.path.isdir(save_dir):
            for subfile in os.listdir(save_dir):
                if subfile.endswith('.json'):
                    try:
                        with open(os.path.join(save_dir, subfile)) as f:
                            o = json.load(f)
                        processed_task_ids.add(o['task_id'])
                    except:
                        continue
        
        updated_tasks = [v for k, v in tasks_dict.items() if k not in processed_task_ids]
        logger.info(f"Total tasks: {len(tasks)}")
        logger.info(f"Tasks to run: {len(updated_tasks)}")
        tasks = updated_tasks
    
    normalized_tasks = []
    for task in tasks:
        if isinstance(task, dict) and 'id' in task:
            if not isinstance(task.get('initial_state'), dict):
                task['initial_state'] = None
            
            # 补齐缺少的 domain 字段以通过 Pydantic 校验
            user_scenario = task.get('user_scenario', {})
            if isinstance(user_scenario, dict):
                instructions = user_scenario.get('instructions', {})
                if isinstance(instructions, dict) and 'domain' not in instructions:
                    instructions['domain'] = 'HR'
            normalized_tasks.append(task)
        elif isinstance(task, dict) and 'task_id' in task:
            try:
                normalized_tasks.append(_convert_gaia_task(task))
            except Exception as exc:
                logger.warning(f"Skip invalid GAIA task {task.get('task_id')}: {exc}")

    return [Task.model_validate(task) for task in normalized_tasks if isinstance(task, dict) and 'id' in task]
