"""在 domain 上运行 solo evaluation pipeline。"""

import argparse
import json
import re
import sys
from pathlib import Path

from loguru import logger

from bench.agent.react_agent import ReActAgent
from bench.config import DEFAULT_MAX_STEPS, get_llm_config
from bench.data_model.message import AssistantMessage, ToolMessage
from bench.data_model.tasks import Task
from bench.evaluator.evaluator import EvaluationType, evaluate_simulation
from bench.orchestrator.orchestrator import Orchestrator
from bench.registry import registry
from bench.user.user_simulator import DummyUser
from bench.utils.llm_utils import get_token_usage

STOP_TOKEN = ReActAgent.STOP_TOKEN


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
):
    agent_config = get_llm_config("agent")
    if agent:
        agent_config["implementation"] = agent
    if model:
        agent_config["model"] = model
    if base_url:
        agent_config["base_url"] = base_url
    if api_key:
        agent_config["api_key"] = api_key

    logger.info("=" * 60)
    logger.info(f"Domain {domain} Solo Evaluation")
    logger.info("=" * 60)
    safe_config = {k: v for k, v in agent_config.items() if k != "api_key"}
    logger.info(f"Agent config: {safe_config}")

    get_environment = registry.get_env_constructor(domain)
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

    def infer_task_level(task: Task) -> str:
        if task.description and task.description.notes:
            m = re.search(r"level\s*=\s*(L[123])", task.description.notes, flags=re.IGNORECASE)
            if m:
                return m.group(1).upper()
        m = re.match(r"^(l[123])_", task.id, flags=re.IGNORECASE)
        if m:
            return m.group(1).upper()
        return "UNKNOWN"

    for task in tasks_to_run:
        logger.info(f"{'='*60}")
        logger.info(f"Running task: {task.id}: {task.description}")

        for trial in range(num_trials):
            if (task.id, trial) in completed_runs:
                logger.info(f"  Trial {trial + 1}/{num_trials} already done, skip")
                continue
            logger.info(f"  Trial {trial + 1}/{num_trials}")

            try:
                env = get_environment()
                run_task = task
                if run_task.ticket is None and run_task.evaluation_criteria:
                    run_task = run_task.model_copy(update={"ticket": build_ticket_from_gt(run_task)})

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

                    orchestrator = Orchestrator(
                        domain=domain,
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

                reward_info = evaluate_simulation(
                    simulation=sim_run,
                    task=run_task,
                    evaluation_type=EvaluationType.ALL,
                    solo_mode=True,
                    domain=domain,
                )

                breakdown = {
                    (k.value if hasattr(k, 'value') else str(k)): v
                    for k, v in (reward_info.reward_breakdown or {}).items()
                }
                tokens = get_token_usage(sim_run.messages)
                agent_answer = _extract_agent_answer(sim_run.messages)

                logger.info(f"    Reward: {reward_info.reward} | Breakdown: {breakdown}")
                logger.info(f"    Tokens: in={tokens.get('prompt_tokens', 0)}, out={tokens.get('completion_tokens', 0)}")
                if agent_answer:
                    logger.info(f"    Agent answer: {agent_answer}")

                results.append({
                    "task_id": run_task.id,
                    "level": infer_task_level(run_task),
                    "trial": trial,
                    "success": reward_info.reward > 0.5,
                    "reward": reward_info.reward,
                    "reward_breakdown": breakdown,
                    "steps": n_steps,
                    "termination": sim_run.termination_reason.value,
                    "input_tokens": tokens.get("prompt_tokens", 0),
                    "output_tokens": tokens.get("completion_tokens", 0),
                    "ticket": run_task.ticket,
                    "agent_answer": agent_answer,
                    "trajectory": _build_trajectory(sim_run.messages),
                })
                _save_results(str(save_to) if save_to else None, results)

            except Exception as e:
                logger.error(f"    Error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                results.append({
                    "task_id": task.id,
                    "level": infer_task_level(task),
                    "trial": trial,
                    "success": False,
                    "error": str(e),
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
    logger.add(str(resolved_save_to.with_suffix(".log")), level="DEBUG", colorize=False, format=log_format, encoding="utf-8")

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
    )
