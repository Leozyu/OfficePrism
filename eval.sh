#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# 用法:
#   ./eval.sh            全量评测（所有 agent × 420 条 task）
#   ./eval.sh --dry-run  试跑模式（所有 agent × 第一条 task）
# ============================================================================
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo ">>> DRY-RUN 模式：所有 agent × 1 条 task"
fi

# ============================================================================
# 评测配置
# ============================================================================
# cross 入口：加载全部任务，每条任务路由到其所属域的单域环境执行（默认单域）
DOMAIN="cross"
TASK_PATH="data/tasks_eval/task_v1.json"
MAX_STEPS=50
LOG_LEVEL="DEBUG"
TOOL_MODE="${TOOL_MODE:-full}"
MODEL_LABEL="${MODEL_LABEL:-qwen4-max}"
USE_CAFFEINATE="${USE_CAFFEINATE:-false}"

# ============================================================================
# Agent 列表
# ============================================================================
AGENTS=(
    # 内置 agent（开箱即用）
    "react_agent"
    # "plan_execute_agent"
    # 外部 agent（需先自行部署对应服务）
    # "ext_code_action"
    # "ext_llmcompiler"
    # "ext_reflexion"
    # "ext_supervisor"
    # "ext_swarm"
    # AutoGen group-chat variants are noisy on HR NL tasks; skip for overnight runs.
    # "ext_debate"
    # "ext_round_robin"
    # "ext_moa"
    # "ext_openclaw"
    # "ext_claude_code"
    # "ext_hermes"
    # "ext_deerflow"
    # "ext_agentzero"
    # "ext_hierarchical"
)

# ============================================================================
# 执行评测
# ============================================================================
if $DRY_RUN; then
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
        SAVE_TO="${RESULT_DIR}/task_v1_${AGENT}_${MODEL_LABEL}.json"
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
        --tool-mode "${TOOL_MODE}" \
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
        SAVE_TO="${RESULT_DIR}/task_v1_${AGENT}_${MODEL_LABEL}.json"
        if [[ -f "${SAVE_TO}" ]]; then
            echo "  python -m bench.eval_stats --result-path ${SAVE_TO}"
        fi
    done
fi
