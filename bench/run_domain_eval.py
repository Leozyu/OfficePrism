"""在 domain 上运行 solo evaluation pipeline。"""

import argparse
import inspect
import json
import re
import sys
from pathlib import Path

from loguru import logger

from bench.agent.react_agent import ReActAgent
from bench.config import DEFAULT_MAX_STEPS, get_llm_config
from bench.data_model.message import AssistantMessage, ToolMessage
from bench.data_model.simulation import RewardInfo
from bench.data_model.tasks import RewardType, Task
from bench.evaluator.evaluator import EvaluationType, evaluate_simulation
from bench.orchestrator.orchestrator import Orchestrator
from bench.registry import registry
from bench.user.user_simulator import DummyUser
from bench.utils.llm_utils import get_cost, get_token_usage

STOP_TOKEN = ReActAgent.STOP_TOKEN


def _make_environment(get_environment, tool_mode: str, pool_domains: list[str] | None = None, home_domain: str | None = None):
    """Construct an environment while preserving compatibility with old domains.

    pool_domains 非空时（tool-scaling 实验）改用 cross_domain 环境，把可发现工具池
    放大到 home + pool_domains 多个域，但 policy 只保留 home 域（把「工具发现压力」
    与「政策膨胀」解耦）。任务加载与评测仍用 home 域，不受影响。
    """
    if pool_domains:
        from bench.domains.cross_domain.environment import get_environment as _cross_env

        merged: list[str] = []
        for d in [home_domain, *pool_domains]:
            if d and d not in merged:
                merged.append(d)
        return _cross_env(domains=merged, policy_domains=[home_domain], tool_mode=tool_mode)

    signature = inspect.signature(get_environment)
    if "tool_mode" in signature.parameters:
        return get_environment(tool_mode=tool_mode)
    return get_environment()


def _mask_secrets(obj):
    """递归掩码配置中的凭证字段，避免把 key 打进日志。"""
    if isinstance(obj, dict):
        return {
            k: ("***" if any(s in k.lower() for s in ("api_key", "password", "token", "secret")) else _mask_secrets(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_mask_secrets(v) for v in obj]
    return obj


def _agent_capability_info(
    *,
    agent_impl: str,
    is_external: bool,
    tool_mode: str,
    exposed_tool_count: int,
    available_tool_count: int,
) -> dict:
    """Describe how tools/skills were exposed for this run."""
    return {
        "tool_mode": tool_mode,
        "tool_interface": (
            "discovery_meta_tools" if tool_mode == "search" else "native_function_schema"
        ),
        "skill_mode": (
            "external_adapter_tool_schema"
            if is_external
            else "prompt_policy_and_tool_schema"
        ),
        "agent_impl": agent_impl,
        "is_external": is_external,
        "exposed_tool_count": exposed_tool_count,
        "available_tool_count": available_tool_count,
    }


def _is_run_success(reward_info: RewardInfo, task: Task) -> bool:
    """Answer-first success for read-style tasks, strict success for stateful tasks."""
    strict_success = reward_info.reward > 0.5
    if task.evaluation_criteria is None:
        return strict_success

    basis = set(task.evaluation_criteria.reward_basis or [])
    stateful_bases = {RewardType.DB, RewardType.ENV_ASSERTION}
    if RewardType.NL_ASSERTION not in basis or basis & stateful_bases:
        return strict_success

    breakdown = reward_info.reward_breakdown or {}
    nl_reward = breakdown.get(RewardType.NL_ASSERTION)
    if nl_reward is None:
        nl_reward = breakdown.get(RewardType.NL_ASSERTION.value)
    if nl_reward is None:
        return strict_success
    return nl_reward > 0.5


def _infer_task_level(task: Task) -> str:
    if task.description and task.description.notes:
        m = re.search(r"level\s*=\s*(L[1-5])", task.description.notes, flags=re.IGNORECASE)
        if m:
            return m.group(1).upper()
    m = re.match(r"^(l[1-5])_", task.id, flags=re.IGNORECASE)
    if m:
        return m.group(1).upper()
    return "UNKNOWN"


def build_ticket_from_gt(task: Task) -> str:
    """从 GT actions 动态构建 ticket。
    只暴露 compare_args（评测实际检查的参数），非检查参数提示 agent 自行填写。
    """
    lines = []

    if task.description and task.description.purpose:
        lines.append(f"任务目标：{task.description.purpose}")

    if task.user_scenario and task.user_scenario.persona:
        lines.append(f"操作员工：{task.user_scenario.persona}")
    else:
        for action in (task.evaluation_criteria.actions or []):
            emp = action.arguments.get("employee_ref")
            if emp:
                lines.append(f"操作员工：{emp}")
                break

    lines.append("")
    lines.append("执行步骤（按顺序调用）：")

    has_non_checked = False
    for i, action in enumerate(task.evaluation_criteria.actions or [], 1):
        checked = set(action.compare_args or action.arguments.keys())
        key_args = {k: v for k, v in action.arguments.items() if k in checked}
        skip_args = [k for k in action.arguments if k not in checked]

        args_str = ", ".join(f"{k}={v}" for k, v in key_args.items())
        line = f"  {i}. {action.name}({args_str})"
        if skip_args:
            has_non_checked = True
            line += f"  # 还需填写: {', '.join(skip_args)}"
        lines.append(line)

    if has_non_checked:
        lines.append("")
        lines.append("注意：# 注释的参数为非 ID 类字段，请自行填写合理的测试值。")

    lines.append("\n请直接调用工具完成任务，无需与用户对话。")
    return "\n".join(lines)


def _extract_agent_answer(messages: list) -> str | None:
    """从 STOP 消息中提取 agent 最终答案。"""
    for msg in reversed(messages):
        if (
            isinstance(msg, AssistantMessage)
            and msg.content
            and STOP_TOKEN in msg.content
        ):
            return msg.content.split(STOP_TOKEN, 1)[-1].strip()
    return None


def _build_trajectory(messages: list) -> list[dict]:
    """构建可读轨迹，保留 assistant 消息和 tool 返回。"""
    steps = []
    for msg in messages:
        if isinstance(msg, AssistantMessage):
            entry = {"role": "assistant"}
            if msg.content:
                entry["content"] = msg.content
            if msg.tool_calls:
                entry["tool_calls"] = [
                    {"name": tc.name, "arguments": tc.arguments}
                    for tc in msg.tool_calls
                ]
            steps.append(entry)
        elif isinstance(msg, ToolMessage):
            steps.append(
                {"role": "tool", "tool_call_id": msg.id, "content": msg.content, "error": msg.error}
            )
    return steps


def _resolve_output_path(domain: str, task_path: str | None, save_to: str | None, agent: str | None, model: str | None = None) -> Path:
    if save_to:
        return Path(save_to)
    resolved_task_path = (
        Path(task_path) if task_path else Path(f"data/domains/{domain}/tasks.json")
    )
    agent_tag = agent or "react_agent"
    model_tag = (model or "default").replace("/", "_").replace(":", "_")
    return Path(f"data/results/{domain}/{resolved_task_path.stem}_{agent_tag}_{model_tag}.json")


def _load_existing_results(save_to: str | None) -> list[dict]:
    if not save_to:
        return []
    save_path = Path(save_to)
    if not save_path.exists():
        return []
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.warning(f"加载历史结果失败，忽略断点续测：{e}")
        return []
    if not isinstance(data, list):
        logger.warning("历史结果文件格式非法（非列表），忽略断点续测。")
        return []
    return data


def _save_results(save_to: str | None, results: list[dict]) -> None:
    if not save_to:
        return
    save_path = Path(save_to)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)


def run_domain_evaluation(
    domain: str = "hr",
    task_ids: list[str] = None,
    num_trials: int = 1,
    max_steps: int = DEFAULT_MAX_STEPS,
    task_path: str = None,
    save_to: str = None,
    log_level: str = "DEBUG",
    agent: str = None,
    model: str = None,
    base_url: str = None,
    api_key: str = None,
    tool_mode: str = "full",
    pool_domains: list[str] = None,
):
    agent_config = get_llm_config("agent")
    if agent:
        agent_config["implementation"] = agent
    if model:
        agent_config["model"] = model
        # ext_hermes/ext_deerflow 读的是专属 *_model 字段而非通用 model，
        # --model 无法直接生效，这里按 agent 类型映射过去，让 sweep 能切模型。
        agent_impl_preview = agent or agent_config.get("implementation", "react_agent")
        if agent_impl_preview == "ext_hermes":
            agent_config["hermes_model"] = model
        elif agent_impl_preview == "ext_deerflow":
            agent_config["deerflow_model"] = model
    if base_url:
        agent_config["base_url"] = base_url
        if agent_config.get("implementation") == "ext_hermes":
            agent_config["hermes_base_url"] = base_url
            agent_config["hermes_provider"] = "custom"
    if api_key:
        agent_config["api_key"] = api_key
        if agent_config.get("implementation") == "ext_hermes":
            agent_config["hermes_api_key"] = api_key

    logger.info("=" * 60)
    logger.info(f"Domain {domain} Solo Evaluation")
    logger.info("=" * 60)
    safe_config = _mask_secrets(agent_config)
    logger.info(f"Agent config: {safe_config}")

    get_tasks = registry.get_tasks_loader(domain)
    resolved_task_path = (
        Path(task_path) if task_path else Path(f"data/domains/{domain}/tasks.json")
    )
    if save_to is None:
        agent_tag = agent or agent_config.get("implementation", "react_agent")
        model_tag = agent_config.get("model", "default").replace("/", "_").replace(":", "_")
        save_to = Path(f"data/results/{domain}/{resolved_task_path.stem}_{agent_tag}_{model_tag}.json")
    tasks = get_tasks(task_path=resolved_task_path, save_to=Path(save_to))

    if task_ids:
        tasks = [t for t in tasks if t.id in task_ids]

    results = _load_existing_results(str(save_to) if save_to else None)
    completed_runs: set[tuple[str, int]] = set()
    for row in results:
        tid = row.get("task_id")
        trial = row.get("trial")
        if isinstance(tid, str) and isinstance(trial, int):
            completed_runs.add((tid, trial))

    completed_task_ids: set[str] = set()
    for task in tasks:
        done_count = sum(1 for trial in range(num_trials) if (task.id, trial) in completed_runs)
        if done_count >= num_trials:
            completed_task_ids.add(task.id)

    tasks_to_run = [t for t in tasks if t.id not in completed_task_ids]
    logger.info(
        f"Loaded {len(tasks)} tasks from {domain} domain | "
        f"resume skip={len(completed_task_ids)} | run={len(tasks_to_run)}"
    )
    
    agent_impl = agent_config.get("implementation", "react_agent")
    is_external = agent_impl.startswith("ext_")
    if not is_external:
        agent_cls = registry.get_agent_constructor(agent_impl)
    user_cls = DummyUser

    for task in tasks_to_run:
        logger.info(f"{'='*60}")
        logger.info(f"Running task: {task.id}: {task.description}")

        for trial in range(num_trials):
            if (task.id, trial) in completed_runs:
                logger.info(f"  Trial {trial + 1}/{num_trials} already done, skip")
                continue
            logger.info(f"  Trial {trial + 1}/{num_trials}")

            try:
                # cross 入口：默认把每条任务路由到其所属域的单域环境
                # （DB/工具/policy 均为本域）；其余入口保持 CLI 指定域。
                task_domain = getattr(
                    getattr(task.user_scenario, "instructions", None), "domain", None
                )
                eff_domain = (
                    str(task_domain).lower()
                    if domain == "cross" and task_domain
                    else domain
                )
                env = _make_environment(
                    registry.get_env_constructor(eff_domain),
                    tool_mode=tool_mode,
                    pool_domains=pool_domains,
                    home_domain=eff_domain,
                )
                exposed_tool_count = len(env.get_tools())
                available_tool_count = getattr(env.tools, "wrapped", env.tools).get_statistics()["num_tools"]
                capability_info = _agent_capability_info(
                    agent_impl=agent_impl,
                    is_external=is_external,
                    tool_mode=tool_mode,
                    exposed_tool_count=exposed_tool_count,
                    available_tool_count=available_tool_count,
                )
                run_task = task
                if run_task.ticket is None and run_task.evaluation_criteria:
                    run_task = run_task.model_copy(update={"ticket": build_ticket_from_gt(run_task)})

                adapter_error: str | None = None
                if is_external:
                    from bench.agent.external import get_external_agent
                    from bench.agent.external_adapter import ExternalAgentRunner

                    ext_agent = get_external_agent(
                        agent_impl,
                        llm_config=agent_config,
                        domain_policy=env.policy,
                    )
                    runner = ExternalAgentRunner(ext_agent, max_steps=max_steps)
                    sim_run = runner.run_task(run_task, env)
                    n_steps = len([m for m in sim_run.messages if isinstance(m, AssistantMessage)])
                    adapter_error = getattr(ext_agent, "last_error", None)
                else:
                    agent_kwargs = {
                        "tools": env.get_tools(),
                        "domain_policy": env.policy,
                        "task": run_task,
                        "llm": agent_config.get("model"),
                        "llm_args": {"temperature": agent_config.get("temperature", 1.0)},
                        "llm_config": agent_config,
                    }
                    agent_instance = agent_cls(**agent_kwargs)
                    user_instance = user_cls()

                    # orchestrator (solo) 路径要求 env 处于 solo mode；
                    # 部分 domain 的 get_environment 未默认开启，这里统一兜底。
                    if not env.solo_mode:
                        env.set_solo_mode(True)

                    orchestrator = Orchestrator(
                        domain=eff_domain,
                        agent=agent_instance,
                        user=user_instance,
                        environment=env,
                        task=run_task,
                        max_steps=max_steps,
                        max_errors=10,
                        solo_mode=True,
                    )
                    sim_run = orchestrator.run()
                    n_steps = len(orchestrator.trajectory)

                logger.info(f"    Steps: {n_steps}")
                logger.info(f"    Termination: {sim_run.termination_reason}")

                # 基础设施级失败（CC 超时 / CLI 非零退出等）不是任务失败：
                # 写入 error 行让 _part_is_done 判为未完成，从而触发重跑，
                # 同时避免污染成功率统计。
                if adapter_error:
                    logger.warning(f"    Adapter infra failure: {adapter_error}")
                    results.append({
                        "task_id": run_task.id,
                        "level": _infer_task_level(run_task),
                        "trial": trial,
                        "success": False,
                        "error": adapter_error,
                        "tool_mode": tool_mode,
                    })
                    _save_results(str(save_to) if save_to else None, results)
                    continue

                # replay_strict 判据：只要「可发现工具池被放大」就必须用宽松重放。
                #   1) search 模式：tool_search 检索结果随池大小变化，跨池/跨进程重放
                #      时返回文本必然不一致，严格重放会对每个 search 轨迹误判抛错。
                #   2) full 模式 + pool_domains 非空（tool-scaling）：agent 会调用跨域
                #      工具（如 finance 任务里调 list_it_service_tickets），而 DB_STATUS
                #      把轨迹重放进纯本域参考环境，跨域工具不存在 → strict 必崩。
                # 宽松模式只重放工具效果还原最终 DB、忽略返回文本伪漂移与跨域工具缺失，
                # DB_STATUS 仍有效（home 域工具经 ToolDiscoveryToolkit 的 use_tool 容错正确重放）。
                _loose_replay = (tool_mode == "search") or bool(pool_domains)
                reward_info = evaluate_simulation(
                    simulation=sim_run,
                    task=run_task,
                    evaluation_type=EvaluationType.ALL,
                    solo_mode=True,
                    domain=eff_domain,
                    tool_mode=tool_mode,
                    replay_strict=(not _loose_replay),
                )

                breakdown = {
                    (k.value if hasattr(k, 'value') else str(k)): v
                    for k, v in (reward_info.reward_breakdown or {}).items()
                }
                # DB_STATUS：agent 轨迹执行后 DB 是否与标准工具链执行后的 DB 一致（1/0）
                db_status = breakdown.get(RewardType.DB_STATUS.value, 0.0)
                run_success = _is_run_success(reward_info, run_task)
                run_strict_success = reward_info.reward > 0.5
                tokens = get_token_usage(sim_run.messages)
                prompt_tokens = tokens.get("prompt_tokens", 0)
                completion_tokens = tokens.get("completion_tokens", 0)
                agent_cost = (get_cost(sim_run.messages) or (0.0, 0.0))[0]
                agent_answer = _extract_agent_answer(sim_run.messages)

                logger.info(f"    Reward: {reward_info.reward} | Breakdown: {breakdown}")
                logger.info(f"    Tokens: in={prompt_tokens}, out={completion_tokens}, cost_usd={agent_cost}")
                if agent_answer:
                    logger.info(f"    Agent answer: {agent_answer}")

                results.append({
                    "task_id": run_task.id,
                    "level": _infer_task_level(run_task),
                    "trial": trial,
                    "success": run_success,
                    "strict_success": run_strict_success,
                    "db_status": db_status,
                    "success_w_db": bool(run_success and db_status >= 1.0),
                    "strict_success_w_db": bool(run_strict_success and db_status >= 1.0),
                    "nl_w_db": bool(breakdown.get(RewardType.NL_ASSERTION.value, 0.0) > 0.5 and db_status >= 1.0),
                    "reward": reward_info.reward,
                    "reward_breakdown": breakdown,
                    # DB_STATUS 拆分：结构分（哈希重放）× 文案分（LLM 判自由文本）
                    "db_struct": (reward_info.db_check.db_struct
                                  if reward_info.db_check is not None else None),
                    "db_text": (reward_info.db_check.db_text
                                if reward_info.db_check is not None else None),
                    "db_text_detail": (reward_info.db_check.db_text_detail
                                       if reward_info.db_check is not None else None),
                    # NL 断言逐条判定及 judge 推理
                    "nl_judge": [
                        {"assertion": c.nl_assertion, "met": c.met,
                         "justification": c.justification}
                        for c in (reward_info.nl_assertions or [])
                    ],
                    "steps": n_steps,
                    "termination": sim_run.termination_reason.value,
                    "input_tokens": prompt_tokens,
                    "output_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                    "cost_usd": agent_cost,
                    "ticket": run_task.ticket,
                    "agent_answer": agent_answer,
                    "tool_mode": tool_mode,
                    "tool_capabilities": capability_info,
                    "trajectory": _build_trajectory(sim_run.messages),
                })
                _save_results(str(save_to) if save_to else None, results)

            except Exception as e:
                logger.error(f"    Error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                results.append({
                    "task_id": task.id,
                    "level": _infer_task_level(task),
                    "trial": trial,
                    "success": False,
                    "error": str(e),
                    "tool_mode": tool_mode,
                })
                _save_results(str(save_to) if save_to else None, results)

    _save_results(str(save_to) if save_to else None, results)
    if save_to:
        logger.info(f"\nResults saved to: {save_to}")
        logger.info(f"Run summary with: python -m bench.eval_stats --result-path {save_to}")

    logger.info(f"{'='*60}")
    logger.info(f"Evaluation finished | Total tasks: {len(tasks)} | Total runs: {len(results)}")
    logger.info(f"{'='*60}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run domain solo evaluation")
    parser.add_argument("--domain", default="hr", help="Domain name (default: hr)")
    parser.add_argument("--agent", default=None, help="Agent name: react_agent, fc_agent, plan_execute_agent, ext_code_action, ext_supervisor, ... (default: from config)")
    parser.add_argument("--task-ids", nargs="+", help="Task IDs to run (default: all)")
    parser.add_argument("--num-trials", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)
    parser.add_argument("--task-path", help="Path to task JSON file")
    parser.add_argument("--save-to", help="Path to save results")
    parser.add_argument("--log-level", default="DEBUG", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--model", help="Override agent model name (e.g. gpt-4o, claude-sonnet-4-20250514)")
    parser.add_argument("--base-url", help="Override LLM API base URL")
    parser.add_argument("--api-key", help="Override LLM API key")
    parser.add_argument("--tool-mode", default="full", choices=["full", "search"], help="Tool exposure mode")
    parser.add_argument("--pool-domains", nargs="+", default=None,
                        help="Tool-scaling: 放大可发现工具池到 home+这些域（policy 仍为本域）。空则不放大")

    args = parser.parse_args()

    from bench.config import get_llm_config as _get_cfg
    _model = args.model or _get_cfg("agent").get("model")

    resolved_save_to = _resolve_output_path(
        domain=args.domain,
        task_path=args.task_path,
        save_to=args.save_to,
        agent=args.agent,
        model=_model,
    )

    logger.remove()
    log_format = "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    logger.add(sys.stderr, level=args.log_level, colorize=True, format=log_format)
    resolved_save_to.parent.mkdir(parents=True, exist_ok=True)
    # buffering=1（行缓冲）: 默认写文件是块缓冲（几 KB），进程被 kill -9 或
    # TASK_TIMEOUT 超时杀死时，缓冲区里尚未落盘的内容会整块丢失——日志看起来像是
    # 在某一行中间戛然而止，实际是从上一次块缓冲刷新点开始的所有内容都没写进去，
    # 而不是模型输出本身被截断。行缓冲让每条日志换行时就立即落盘，kill 造成的
    # 影响最多只丢最后一条不完整的记录，不会误导成"输出被截断"。
    logger.add(
        str(resolved_save_to.with_suffix(".log")),
        level="DEBUG",
        colorize=False,
        format=log_format,
        encoding="utf-8",
        buffering=1,
    )

    run_domain_evaluation(
        domain=args.domain,
        agent=args.agent,
        task_ids=args.task_ids,
        num_trials=args.num_trials,
        max_steps=args.max_steps,
        task_path=args.task_path,
        save_to=str(resolved_save_to),
        log_level=args.log_level,
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        tool_mode=args.tool_mode,
        pool_domains=args.pool_domains,
    )
