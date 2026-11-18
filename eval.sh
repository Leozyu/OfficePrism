#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 用法:
#   ./eval.sh            全量评测（所有 agent × 70 条 task）
#   ./eval.sh --dry-run  试跑模式（第一个 agent × 第一条 task）
# ============================================================================
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo ">>> DRY-RUN 模式：只跑 react_agent × 1 条 task"
fi

# ============================================================================
# 评测配置
# ============================================================================
DOMAIN="hr"
TASK_PATH="data/tasks_clean/tasks_hr_70.json"
MAX_STEPS=50
LOG_LEVEL="DEBUG"
# macOS 防休眠开关（Linux 上保持 false，caffeinate 仅 macOS 可用）
USE_CAFFEINATE="${USE_CAFFEINATE:-false}"

# ============================================================================
# Agent 列表
# ============================================================================
AGENTS=(
    # 内置 agent（只需 LLM API key，开箱即用）
    "react_agent"
    # "plan_execute_agent"
    # 外部 agent（需先安装 requirements-external.txt 中的可选依赖）
    # "ext_code_action"
    # "ext_llmcompiler"
    # "ext_reflexion"
    # "ext_supervisor"
    # "ext_swarm"
    # "ext_debate"
    # "ext_round_robin"
    # "ext_moa"
    # "ext_hierarchical"
)


# ============================================================================
# 执行评测
# ============================================================================
if $DRY_RUN; then
    # 每次 dry-run 用独立时间戳目录，避免 resume 逻辑跳过已有（可能失败的）结果
    DRY_RUN_ID="${DRY_RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
    RESULT_DIR="data/results/${DOMAIN}-dry-run/${DRY_RUN_ID}"
else
    RESULT_DIR="data/results/${DOMAIN}"
fi
mkdir -p "${RESULT_DIR}"

TASK_ID_ARGS=""
if $DRY_RUN; then
    TASK_ID_ARGS="--task-ids l1_56a218f4"
fi

for AGENT in "${AGENTS[@]}"; do
    if $DRY_RUN; then
        SAVE_TO="${RESULT_DIR}/dry_run_${AGENT}.json"
    else
        SAVE_TO="${RESULT_DIR}/tasks_hr_70_${AGENT}_qwen4-max.json"
    fi

    echo ""
    echo "=================================================================="
    echo "  Agent: ${AGENT}"
    echo "  Save:  ${SAVE_TO}"
    echo "=================================================================="

    RUNNER=(python -m bench.run_domain_eval)
    if [[ "${USE_CAFFEINATE}" == "true" ]]; then
        RUNNER=(caffeinate -i "${RUNNER[@]}")
    fi

    "${RUNNER[@]}" \
        --domain "${DOMAIN}" \
        --task-path "${TASK_PATH}" \
        --agent "${AGENT}" \
        --max-steps "${MAX_STEPS}" \
        --log-level "${LOG_LEVEL}" \
        --save-to "${SAVE_TO}" \
        ${TASK_ID_ARGS} \
    || echo ">>> [WARN] ${AGENT} failed, continuing..."

    echo ">>> Done: ${AGENT}"
done

echo ""
echo "=================================================================="
if $DRY_RUN; then
    echo "  Dry-run 完成！各 Agent 结果："
    for AGENT in "${AGENTS[@]}"; do
        SAVE_TO="${RESULT_DIR}/dry_run_${AGENT}.json"
        if [[ -f "${SAVE_TO}" ]]; then
            python -m bench.eval_stats --result-path "${SAVE_TO}"
        fi
    done
else
    echo "  全部评测完成！汇总命令："
    for AGENT in "${AGENTS[@]}"; do
        SAVE_TO="${RESULT_DIR}/tasks_hr_70_${AGENT}_qwen4-max.json"
        if [[ -f "${SAVE_TO}" ]]; then
            echo "  python -m bench.eval_stats --result-path ${SAVE_TO}"
        fi
    done
fi
