#!/usr/bin/env python3
"""对两份 task 文件做 LLM Judge 对比评测。"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv
from omegaconf import OmegaConf

from .llm_judge import judge_task

LEVELS: Tuple[str, str, str] = ("L1", "L2", "L3")


def _load_llm_conf(config_path: Path) -> Tuple[str, Dict[str, Any]]:
    load_dotenv()
    cfg = OmegaConf.to_container(OmegaConf.load(str(config_path)), resolve=True)
    llm = cfg.get("synthesis", {}).get("llm", {})
    model = llm.get("model_name") or llm.get("model") or "gpt-4o"
    llm_config = {
        "api_key": llm.get("api_key", "dummy"),
        "base_url": llm.get("base_url"),
        "temperature": llm.get("temperature", 0.7),
        "max_tokens": llm.get("max_tokens", 64000),
    }
    return model, llm_config


def _init_level_stats() -> Dict[str, Dict[str, Any]]:
    return {
        lv: {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "logic_sum": 0.0,
            "naturalness_sum": 0.0,
            "difficulty_sum": 0.0,
            "score_sum": 0.0,
            "score_count": 0,
            "error_count": 0,
        }
        for lv in LEVELS
    }


def _run_single_judge(
    task: Dict[str, Any], model: str, llm_config: Dict[str, Any]
) -> Tuple[str, bool, Dict[str, Any]]:
    level = str(task.get("level", "")).upper()
    if level not in LEVELS:
        return level, False, {"comments": "invalid level"}
    try:
        passed, result = judge_task(task, model=model, llm_config=llm_config)
        if not isinstance(result, dict):
            return level, False, {"comments": "judge result is not dict"}
        return level, passed, result
    except Exception as e:  # pragma: no cover
        return level, False, {"comments": f"judge error: {e}"}


def _finalize_level_stats(level_stats: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for lv in LEVELS:
        st = level_stats[lv]
        total = st["total"]
        passed = st["passed"]
        failed = st["failed"]
        score_count = st["score_count"]
        result[lv] = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) if total else 0.0,
            "filter_rate": (failed / total) if total else 0.0,
            "avg_logic": (st["logic_sum"] / score_count) if score_count else None,
            "avg_naturalness": (st["naturalness_sum"] / score_count) if score_count else None,
            "avg_difficulty": (st["difficulty_sum"] / score_count) if score_count else None,
            "avg_score_5": (st["score_sum"] / score_count) if score_count else None,
            "avg_score_100": ((st["score_sum"] / score_count) * 20) if score_count else None,
            "score_count": score_count,
            "error_count": st["error_count"],
        }
    return result


def evaluate_file(
    name: str,
    task_path: Path,
    model: str,
    llm_config: Dict[str, Any],
    max_workers: int,
) -> Dict[str, Any]:
    with task_path.open("r", encoding="utf-8") as f:
        tasks: List[Dict[str, Any]] = json.load(f)

    level_stats = _init_level_stats()
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for task in tasks:
            futures.append(executor.submit(_run_single_judge, task, model, llm_config))

        total_jobs = len(futures)
        done = 0
        for fu in as_completed(futures):
            level, passed, judge_result = fu.result()
            done += 1
            if done % 20 == 0 or done == total_jobs:
                print(f"[{name}] progress: {done}/{total_jobs}", flush=True)

            if level not in LEVELS:
                continue

            st = level_stats[level]
            st["total"] += 1
            st["passed"] += 1 if passed else 0
            st["failed"] += 0 if passed else 1

            logic = judge_result.get("logic_score")
            naturalness = judge_result.get("naturalness_score")
            difficulty = judge_result.get("difficulty_score")
            if not all(isinstance(x, (int, float)) for x in (logic, naturalness, difficulty)):
                st["error_count"] += 1
                continue

            logic = float(logic)
            naturalness = float(naturalness)
            difficulty = float(difficulty)
            st["logic_sum"] += logic
            st["naturalness_sum"] += naturalness
            st["difficulty_sum"] += difficulty
            st["score_sum"] += (logic + naturalness + difficulty) / 3.0
            st["score_count"] += 1

    levels_result = _finalize_level_stats(level_stats)
    total = sum(level_stats[lv]["total"] for lv in LEVELS)
    passed = sum(level_stats[lv]["passed"] for lv in LEVELS)
    failed = sum(level_stats[lv]["failed"] for lv in LEVELS)
    score_count = sum(level_stats[lv]["score_count"] for lv in LEVELS)
    score_sum = sum(level_stats[lv]["score_sum"] for lv in LEVELS)

    return {
        "name": name,
        "path": str(task_path),
        "task_count": len(tasks),
        "levels": levels_result,
        "overall": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) if total else 0.0,
            "filter_rate": (failed / total) if total else 0.0,
            "avg_score_5": (score_sum / score_count) if score_count else None,
            "avg_score_100": ((score_sum / score_count) * 20) if score_count else None,
            "score_count": score_count,
        },
    }


def _pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def print_summary(old_res: Dict[str, Any], new_res: Dict[str, Any]) -> None:
    print("\n=== 过滤比率对比（越低越好） ===")
    for lv in LEVELS:
        old_filter = old_res["levels"][lv]["filter_rate"]
        new_filter = new_res["levels"][lv]["filter_rate"]
        delta = (new_filter - old_filter) * 100
        print(
            f"{lv}: old={_pct(old_filter)} | new={_pct(new_filter)} | Δ={delta:+.2f}pp"
        )

    old_o = old_res["overall"]
    new_o = new_res["overall"]
    old_score = old_o["avg_score_100"]
    new_score = new_o["avg_score_100"]
    old_score_text = f"{old_score:.2f}" if isinstance(old_score, (int, float)) else "N/A"
    new_score_text = f"{new_score:.2f}" if isinstance(new_score, (int, float)) else "N/A"
    delta_filter_pp = (new_o["filter_rate"] - old_o["filter_rate"]) * 100
    delta_score = (
        (new_score - old_score)
        if isinstance(new_score, (int, float)) and isinstance(old_score, (int, float))
        else None
    )
    delta_score_text = f"{delta_score:+.2f}" if isinstance(delta_score, (int, float)) else "N/A"

    print("\n=== 总体对比 ===")
    print(
        f"overall filter: old={_pct(old_o['filter_rate'])} | new={_pct(new_o['filter_rate'])} | Δ={delta_filter_pp:+.2f}pp"
    )
    print(f"overall score(100): old={old_score_text} | new={new_score_text} | Δ={delta_score_text}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="比较旧/新 task 文件的 LLM Judge 过滤率与分数。")
    parser.add_argument(
        "--old",
        type=Path,
        default=Path("backup/tasks-back/tasks_hr.json"),
        help="旧版 task 路径",
    )
    parser.add_argument(
        "--new",
        type=Path,
        default=Path("tasks/tasks_hr.json"),
        help="新版 task 路径",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/app.yaml"),
        help="LLM 配置文件路径",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="并发线程数（过大可能触发限流）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/llm_judge_compare_hr.json"),
        help="输出 JSON 路径",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model, llm_config = _load_llm_conf(args.config)
    workers = max(1, args.workers)

    print(f"judge model: {model}")
    print(f"old: {args.old}")
    print(f"new: {args.new}")
    print(f"workers: {workers}")

    old_res = evaluate_file("old", args.old, model, llm_config, workers)
    new_res = evaluate_file("new", args.new, model, llm_config, workers)

    output = {
        "meta": {
            "model": model,
            "workers": workers,
            "old_path": str(args.old),
            "new_path": str(args.new),
        },
        "old": old_res,
        "new": new_res,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print_summary(old_res, new_res)
    print(f"\n结果已写入: {args.output}")


if __name__ == "__main__":
    main()
