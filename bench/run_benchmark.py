"""批量评测入口：多 Agent x 多模型笛卡尔积运行。

用法::

    python -m bench.run_benchmark --domain hr \\
        --agents react_agent fc_agent plan_execute_agent \\
        --models qwen4-max gpt-4o \\
        --task-path tasks_clean/tasks_hr.json \\
        --max-steps 100 --num-trials 1
"""

import argparse
import itertools
import sys
from pathlib import Path

from loguru import logger

from bench.config import DEFAULT_MAX_STEPS
from bench.run_domain_eval import run_domain_evaluation


def run_benchmark(
    domain: str,
    agents: list[str],
    models: list[str],
    task_path: str | None = None,
    task_ids: list[str] | None = None,
    num_trials: int = 1,
    max_steps: int = DEFAULT_MAX_STEPS,
    output_dir: str = "data/results",
    log_level: str = "INFO",
):
    combinations = list(itertools.product(agents, models))
    logger.info(f"Benchmark: {len(combinations)} combinations ({len(agents)} agents x {len(models)} models)")

    for agent_name, model_name in combinations:
        safe_model = model_name.replace("/", "_").replace(":", "_")
        save_to = Path(output_dir) / domain / f"{agent_name}_{safe_model}.json"

        logger.info(f"{'='*60}")
        logger.info(f"Running: agent={agent_name}, model={model_name}")
        logger.info(f"Output: {save_to}")
        logger.info(f"{'='*60}")

        try:
            from configs.config_loader import load_config
            config = load_config()
            config["evaluation"]["llm"]["agent"]["model"] = model_name
            config["evaluation"]["llm"]["agent"]["implementation"] = agent_name
        except Exception:
            pass

        try:
            run_domain_evaluation(
                domain=domain,
                agent=agent_name,
                task_ids=task_ids,
                num_trials=num_trials,
                max_steps=max_steps,
                task_path=task_path,
                save_to=str(save_to),
                log_level=log_level,
            )
        except Exception as e:
            logger.error(f"Failed: agent={agent_name}, model={model_name}: {e}")
            import traceback
            logger.error(traceback.format_exc())

    logger.info(f"\nBenchmark complete. Results in: {output_dir}/{domain}/")
    logger.info(f"Compare with: python -m bench.eval_stats --pattern '{output_dir}/{domain}/*.json'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multi-agent multi-model benchmark")
    parser.add_argument("--domain", default="hr")
    parser.add_argument("--agents", nargs="+", default=["react_agent"], help="Agent names (e.g. react_agent fc_agent plan_execute_agent)")
    parser.add_argument("--models", nargs="+", default=None, help="Model names (default: use config)")
    parser.add_argument("--task-path", default=None)
    parser.add_argument("--task-ids", nargs="+", default=None)
    parser.add_argument("--num-trials", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)
    parser.add_argument("--output-dir", default="data/results")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    args = parser.parse_args()

    logger.remove()
    log_format = "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    logger.add(sys.stderr, level=args.log_level, colorize=True, format=log_format)

    models = args.models
    if models is None:
        from bench.config import get_llm_config
        cfg = get_llm_config("agent")
        models = [cfg.get("model", "qwen4-max")]

    run_benchmark(
        domain=args.domain,
        agents=args.agents,
        models=models,
        task_path=args.task_path,
        task_ids=args.task_ids,
        num_trials=args.num_trials,
        max_steps=args.max_steps,
        output_dir=args.output_dir,
        log_level=args.log_level,
    )
