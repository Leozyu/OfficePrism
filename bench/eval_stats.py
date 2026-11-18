"""评测结果统计脚本：支持单文件或批量结果聚合 + 多维对比。

用法::

    # 单文件统计
    python -m bench.eval_stats --result-path results/domains/hr/react_agent_qwen4-max.json

    # 多文件对比（按 agent/model 分组）
    python -m bench.eval_stats --pattern "results/domains/hr/*.json"
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path


def _load_results_file(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} 不是 JSON 数组")
    return data


def _resolve_result_paths(result_path: str | None, pattern: str | None) -> list[Path]:
    if result_path:
        path = Path(result_path)
        if not path.exists():
            raise FileNotFoundError(f"结果文件不存在: {path}")
        return [path]
    if not pattern:
        raise ValueError("必须提供 --result-path 或 --pattern")
    paths = [Path(p) for p in sorted(glob.glob(pattern))]
    if not paths:
        raise FileNotFoundError(f"未匹配到结果文件: {pattern}")
    return paths


def _infer_agent_model(path: Path) -> tuple[str, str]:
    """从文件名推断 agent 和 model（文件名格式：{agent}_{model}.json）。"""
    stem = path.stem
    parts = stem.split("_", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return stem, "unknown"


def _compute_stats(results: list[dict]) -> dict:
    total = len(results)
    if total == 0:
        return {"total": 0, "success": 0, "rate": 0.0, "avg_reward": 0.0, "avg_steps": 0.0, "total_cost": 0.0}

    successful = sum(1 for r in results if r.get("success", False))
    total_reward = sum(r.get("reward", 0) for r in results)
    total_steps = sum(r.get("steps", 0) for r in results)
    total_cost = sum((r.get("agent_cost", 0) or 0) + (r.get("user_cost", 0) or 0) for r in results)

    return {
        "total": total,
        "success": successful,
        "rate": successful / total * 100,
        "avg_reward": total_reward / total,
        "avg_steps": total_steps / total,
        "total_cost": total_cost,
    }


def _compute_level_stats(results: list[dict]) -> dict[str, dict]:
    by_level: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_level[r.get("level", "UNKNOWN")].append(r)
    return {level: _compute_stats(rows) for level, rows in sorted(by_level.items())}


def print_summary(results: list[dict], label: str = "Overall", total_tasks: int | None = None) -> None:
    stats = _compute_stats(results)
    level_stats = _compute_level_stats(results)

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Success: {stats['success']}/{stats['total']} ({stats['rate']:.1f}%)")
    if total_tasks is not None:
        print(f"  Total tasks: {total_tasks}")
    for level, ls in level_stats.items():
        print(f"  {level}: {ls['success']}/{ls['total']} ({ls['rate']:.1f}%)")
    print(f"  Avg reward: {stats['avg_reward']:.3f}")
    print(f"  Avg steps: {stats['avg_steps']:.1f}")
    print(f"  Total cost: ${stats['total_cost']:.4f}")
    print(f"{'='*60}")


def print_comparison_table(file_results: dict[str, list[dict]]) -> None:
    """打印多文件交叉对比表格。"""
    if len(file_results) <= 1:
        return

    print(f"\n{'='*80}")
    print("  Comparison Table")
    print(f"{'='*80}")

    header = f"{'Config':<35} {'Success':>10} {'Rate':>8} {'Reward':>8} {'Steps':>8} {'Cost':>10}"
    print(header)
    print("-" * 80)

    for label, results in sorted(file_results.items()):
        stats = _compute_stats(results)
        row = (
            f"{label:<35} "
            f"{stats['success']:>4}/{stats['total']:<5} "
            f"{stats['rate']:>6.1f}% "
            f"{stats['avg_reward']:>7.3f} "
            f"{stats['avg_steps']:>7.1f} "
            f"${stats['total_cost']:>8.4f}"
        )
        print(row)

    print(f"{'='*80}")

    # 按 level 对比
    all_levels = set()
    for results in file_results.values():
        for r in results:
            all_levels.add(r.get("level", "UNKNOWN"))

    for level in sorted(all_levels):
        print(f"\n  Level: {level}")
        print(f"  {'Config':<33} {'Success':>10} {'Rate':>8}")
        print(f"  {'-'*55}")
        for label, results in sorted(file_results.items()):
            level_results = [r for r in results if r.get("level", "UNKNOWN") == level]
            ls = _compute_stats(level_results)
            print(f"  {label:<33} {ls['success']:>4}/{ls['total']:<5} {ls['rate']:>6.1f}%")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统计 run_domain_eval 产出的结果文件。")
    parser.add_argument("--result-path", help="单个结果文件路径")
    parser.add_argument("--pattern", help='批量匹配模式，例如 "results/domains/hr/*.json"')
    parser.add_argument("--show-files", action="store_true", help="打印参与统计的文件列表")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = _resolve_result_paths(args.result_path, args.pattern)

    if args.show_files:
        print("Files:")
        for path in paths:
            print(f"  - {path}")

    file_results: dict[str, list[dict]] = {}
    merged_results: list[dict] = []

    for path in paths:
        results = _load_results_file(path)
        merged_results.extend(results)
        label = path.stem
        file_results[label] = results

    if len(paths) == 1:
        print_summary(merged_results, label=paths[0].stem)
    else:
        print_summary(merged_results, label=f"All ({len(paths)} files)")
        print_comparison_table(file_results)


if __name__ == "__main__":
    main()
