#!/usr/bin/env bash
# 批量生成所有域的 tasks
# 用法：./gen_tasks.sh [--domains "hr it finance"] [--concurrent 5] [--output-dir tasks]

set -euo pipefail

DOMAINS="purchase work"
MAX_CONCURRENT=5
OUTPUT_DIR="data/tasks"
DO_GLOBAL_DEDUP=1

while [[ $# -gt 0 ]]; do
  case $1 in
    --domains)   DOMAINS="$2";       shift 2 ;;
    --concurrent) MAX_CONCURRENT="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2";    shift 2 ;;
    --skip-global-dedup) DO_GLOBAL_DEDUP=0; shift 1 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

for domain in $DOMAINS; do
  echo "========================================"
  echo "▶ 生成域: $domain"
  echo "========================================"
  python -m synthesis.task_gen.pipeline \
    --domain "$domain" \
    --output "$OUTPUT_DIR/tasks_${domain}.json" \
    --max-concurrent "$MAX_CONCURRENT"
  echo "✓ $domain 完成 → $OUTPUT_DIR/tasks_${domain}.json"
done

if [[ "$DO_GLOBAL_DEDUP" -eq 1 ]]; then
  echo "========================================"
  echo "▶ 全域去重: $OUTPUT_DIR/tasks_*.json"
  echo "========================================"
  python -m synthesis.task_gen.dedup "$OUTPUT_DIR" --pattern "tasks_*.json" --inplace --report "$OUTPUT_DIR/dedup_report.json"
  echo "✓ 去重完成 → $OUTPUT_DIR/dedup_report.json"
fi

echo ""
echo "全部完成，输出目录: $OUTPUT_DIR"
