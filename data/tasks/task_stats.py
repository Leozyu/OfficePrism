#!/usr/bin/env python3
"""统计 tasks_*.json 中各域 L1/L2/L3 的题目指标。"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

LEVELS: Tuple[str, str, str] = ("L1", "L2", "L3")
TOOL_CALL_RE = re.compile(r"[A-Za-z_]\w*\s*\(")


@dataclass
class Stats:
    count: int = 0
    question_len_sum: int = 0
    tool_call_sum: int = 0

    def add(self, question_len: int, tool_calls: int) -> None:
        self.count += 1
        self.question_len_sum += question_len
        self.tool_call_sum += tool_calls

    def avg_question_len(self) -> float:
        return self.question_len_sum / self.count if self.count else 0.0

    def avg_tool_calls(self) -> float:
        return self.tool_call_sum / self.count if self.count else 0.0


def _load_json(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} 不是 JSON 数组")
    return data


def _normalize_level(raw: object) -> str:
    level = str(raw or "").strip().upper()
    return level if level in LEVELS else ""


def _count_tool_calls(answer: object) -> int:
    # answer 主要是字符串形式的工具调用链；若未来变为 list，也兼容统计。
    if isinstance(answer, list):
        return len(answer)
    if not isinstance(answer, str):
        return 0
    return len(TOOL_CALL_RE.findall(answer))


def _question_len(question: object) -> int:
    if not isinstance(question, str):
        return 0
    return len(question.strip())


def collect_stats(tasks_dir: Path, pattern: str) -> Dict[str, Dict[str, Stats]]:
    files = sorted(tasks_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"未找到匹配文件：{tasks_dir / pattern}")

    domain_level_stats: Dict[str, Dict[str, Stats]] = {}
    for file in files:
        # 约定文件名为 tasks_<domain>.json
        domain = file.stem.replace("tasks_", "", 1)
        domain_stats = domain_level_stats.setdefault(domain, {lv: Stats() for lv in LEVELS})
        for task in _load_json(file):
            level = _normalize_level(task.get("level"))
            if level not in LEVELS:
                continue
            domain_stats[level].add(
                question_len=_question_len(task.get("question")),
                tool_calls=_count_tool_calls(task.get("answer")),
            )
    return domain_level_stats


def _weighted_avg(items: Iterable[Tuple[int, int]]) -> float:
    total_count = 0
    total_sum = 0
    for count, value_sum in items:
        total_count += count
        total_sum += value_sum
    return (total_sum / total_count) if total_count else 0.0


def _render_table(domain_level_stats: Dict[str, Dict[str, Stats]], metric: str, title: str) -> str:
    rows: List[List[str]] = []
    domains = sorted(domain_level_stats.keys())

    for domain in domains:
        by_level = domain_level_stats[domain]
        if metric == "count":
            values = [by_level[lv].count for lv in LEVELS]
            total = sum(values)
            row_values = [str(v) for v in values] + [str(total)]
        elif metric == "avg_question_len":
            values = [by_level[lv].avg_question_len() for lv in LEVELS]
            total = _weighted_avg((by_level[lv].count, by_level[lv].question_len_sum) for lv in LEVELS)
            row_values = [f"{v:.2f}" for v in values] + [f"{total:.2f}"]
        elif metric == "avg_tool_calls":
            values = [by_level[lv].avg_tool_calls() for lv in LEVELS]
            total = _weighted_avg((by_level[lv].count, by_level[lv].tool_call_sum) for lv in LEVELS)
            row_values = [f"{v:.2f}" for v in values] + [f"{total:.2f}"]
        else:
            raise ValueError(f"未知 metric: {metric}")
        rows.append([domain] + row_values)

    # 汇总行：跨所有域按级别统计
    level_totals: Dict[str, Stats] = {lv: Stats() for lv in LEVELS}
    for by_level in domain_level_stats.values():
        for lv in LEVELS:
            level_totals[lv].count += by_level[lv].count
            level_totals[lv].question_len_sum += by_level[lv].question_len_sum
            level_totals[lv].tool_call_sum += by_level[lv].tool_call_sum

    if metric == "count":
        total_values = [level_totals[lv].count for lv in LEVELS]
        total_col = sum(total_values)
        total_row_values = [str(v) for v in total_values] + [str(total_col)]
    elif metric == "avg_question_len":
        total_values = [level_totals[lv].avg_question_len() for lv in LEVELS]
        total_col = _weighted_avg((level_totals[lv].count, level_totals[lv].question_len_sum) for lv in LEVELS)
        total_row_values = [f"{v:.2f}" for v in total_values] + [f"{total_col:.2f}"]
    else:  # avg_tool_calls
        total_values = [level_totals[lv].avg_tool_calls() for lv in LEVELS]
        total_col = _weighted_avg((level_totals[lv].count, level_totals[lv].tool_call_sum) for lv in LEVELS)
        total_row_values = [f"{v:.2f}" for v in total_values] + [f"{total_col:.2f}"]
    rows.append(["total"] + total_row_values)

    header = ["domain", "L1", "L2", "L3", "total"]
    sep = ["---"] * len(header)
    lines = [f"## {title}", "| " + " | ".join(header) + " |", "| " + " | ".join(sep) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def build_report(domain_level_stats: Dict[str, Dict[str, Stats]]) -> str:
    parts = [
        _render_table(domain_level_stats, metric="count", title="question 个数"),
        _render_table(domain_level_stats, metric="avg_question_len", title="平均 question 长度（字符）"),
        _render_table(domain_level_stats, metric="avg_tool_calls", title="平均工具链个数"),
    ]
    return "\n\n".join(parts)


def _metric_row(domain: str, by_level: Dict[str, Stats], metric: str) -> List[str]:
    if metric == "count":
        values = [by_level[lv].count for lv in LEVELS]
        total = sum(values)
        return [domain] + [str(v) for v in values] + [str(total)]
    if metric == "avg_question_len":
        values = [by_level[lv].avg_question_len() for lv in LEVELS]
        total = _weighted_avg((by_level[lv].count, by_level[lv].question_len_sum) for lv in LEVELS)
        return [domain] + [f"{v:.2f}" for v in values] + [f"{total:.2f}"]
    if metric == "avg_tool_calls":
        values = [by_level[lv].avg_tool_calls() for lv in LEVELS]
        total = _weighted_avg((by_level[lv].count, by_level[lv].tool_call_sum) for lv in LEVELS)
        return [domain] + [f"{v:.2f}" for v in values] + [f"{total:.2f}"]
    raise ValueError(f"未知 metric: {metric}")


def write_csv_report(domain_level_stats: Dict[str, Dict[str, Stats]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics = ("count", "avg_question_len", "avg_tool_calls")
    metric_labels = {
        "count": "question_count",
        "avg_question_len": "avg_question_len",
        "avg_tool_calls": "avg_tool_calls",
    }

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "domain", "L1", "L2", "L3", "total"])

        for metric in metrics:
            for domain in sorted(domain_level_stats.keys()):
                writer.writerow([metric_labels[metric], *_metric_row(domain, domain_level_stats[domain], metric)])

            # total 行
            total_by_level: Dict[str, Stats] = {lv: Stats() for lv in LEVELS}
            for by_level in domain_level_stats.values():
                for lv in LEVELS:
                    total_by_level[lv].count += by_level[lv].count
                    total_by_level[lv].question_len_sum += by_level[lv].question_len_sum
                    total_by_level[lv].tool_call_sum += by_level[lv].tool_call_sum
            writer.writerow([metric_labels[metric], *_metric_row("total", total_by_level, metric)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统计各域 L1/L2/L3 的 question 指标。")
    parser.add_argument(
        "--tasks-dir",
        type=Path,
        default=Path("tasks"),
        help="任务 JSON 所在目录，默认 tasks",
    )
    parser.add_argument(
        "--pattern",
        default="tasks_*.json",
        help="文件匹配模式，默认 tasks_*.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="可选：将统计结果写入 CSV 文件",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stats = collect_stats(args.tasks_dir, args.pattern)
    if args.output:
        write_csv_report(stats, args.output)
        print(f"CSV 已输出到: {args.output}")
        return

    report = build_report(stats)
    print(report)


if __name__ == "__main__":
    main()
