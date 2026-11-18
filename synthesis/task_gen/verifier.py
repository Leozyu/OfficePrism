"""任务验证器：解析 LLM 生成的 tool_chain，在真实 DB 上执行验证。"""
import ast
import json
import re
from typing import Any, Dict, List, Tuple
from bench.environment.toolkit import ToolKitBase
from copy import deepcopy


def _parse_tool_chain(answer_str: str, toolkit: ToolKitBase = None) -> List[Dict[str, Any]]:
    """使用 Python AST 安全解析 LLM 输出的 answer 字符串为结构化 tool call 列表。"""
    if isinstance(answer_str, list):
        # 兼容已经是解析好的列表（比如 LLM 输出的已经是标准 JSON 数组）
        if all(isinstance(i, dict) for i in answer_str):
            return answer_str
        answer_str = str(answer_str)

    answer_str = answer_str.strip()
    
    # 尝试作为纯 JSON 解析（防止大模型有时很乖地输出 JSON 格式）
    try:
        parsed = json.loads(answer_str)
        if isinstance(parsed, list) and all(isinstance(i, dict) for i in parsed):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    # 处理可能的包裹符号
    if not answer_str.startswith("["):
        answer_str = f"[{answer_str}]"
        
    calls = []
    try:
        # 使用 AST 将字符串作为 Python 表达式安全解析
        tree = ast.parse(answer_str, mode='eval')
        if isinstance(tree.body, ast.List):
            for item in tree.body.elts:
                if isinstance(item, ast.Call):
                    name = item.func.id if isinstance(item.func, ast.Name) else str(item.func)
                    kwargs = {}
                    # 解析关键字参数
                    for kw in item.keywords:
                        if kw.arg:
                            try:
                                kwargs[kw.arg] = ast.literal_eval(kw.value)
                            except ValueError:
                                # 兼容无法 literal_eval 的极端情况
                                kwargs[kw.arg] = None 
                    
                    # 兼容仅有位置参数的情况
                    if not kwargs and item.args and toolkit:
                        try:
                            sigs = toolkit.get_tools()
                            tool = sigs.get(name)
                            if tool and tool.params:
                                first_param = list(tool.params.keys())[0]
                                kwargs[first_param] = ast.literal_eval(item.args[0])
                        except Exception:
                            kwargs["arg0"] = ast.literal_eval(item.args[0])

                    calls.append({"name": name, "kwargs": kwargs})
        return calls
    except SyntaxError as e:
        raise ValueError(f"AST 解析失败，格式非法: {answer_str} -> {e}")


def verify_task(
    task: Dict[str, Any],
    toolkit: ToolKitBase,
) -> Tuple[bool, List[str]]:
    """验证任务的可执行性。

    Returns:
        (passed, errors): passed=True 表示通过，errors 为错误列表
    """
    errors = []

    # 1. 基本字段检查
    for field in ("question", "answer"):
        if not task.get(field):
            errors.append(f"缺少必要字段: {field}")
    if errors:
        return False, errors

    # 2. 解析 tool chain
    try:
        tool_calls = _parse_tool_chain(task["answer"], toolkit)
    except Exception as e:
        errors.append(f"tool_chain 解析失败: {e}")
        return False, errors

    if not tool_calls:
        errors.append("tool_chain 为空")
        return False, errors

    # 3. 检查所有工具是否存在
    for tc in tool_calls:
        if not toolkit.has_tool(tc["name"]):
            errors.append(f"工具 '{tc['name']}' 不存在")

    if errors:
        return False, errors

    # 4. 在 DB 副本上执行验证
    toolkit_copy = deepcopy(toolkit)
    for i, tc in enumerate(tool_calls):
        try:
            toolkit_copy.use_tool(tc["name"], **tc["kwargs"])
        except Exception as e:
            errors.append(f"步骤 {i+1} 执行失败: {tc['name']}({tc['kwargs']}) → {e}")
            break

    passed = len(errors) == 0
    return passed, errors
