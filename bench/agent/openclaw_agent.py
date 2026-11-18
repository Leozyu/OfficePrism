"""
OpenClaw baseline（评测注册名：`openclaw_agent`）

说明：PyPI 上的 `openclaw` 包是 CMDOP 的 OpenClaw 客户端（`OpenClaw.remote(...).agent.run`），
走的是远端 gRPC 闭式执行，无法接入本仓库的逐步 Orchestrator + 本地 Environment 工具调用协议。

因此评测里的「openclaw baseline」采用与 `fc_agent` 相同的策略：OpenAI 兼容 API + 原生
Function Calling（`bench.utils.llm_utils.generate` + 域内 `Tool`）。若需在论文/表格中单独一列
对比，使用 `--agent openclaw_agent` 即可；行为与 `fc_agent` 一致，仅 implementation 标签不同。

若未来 CMDOP 支持逐步 tool 协议或与本地 env 对齐，可再实现独立适配器。
"""

from __future__ import annotations

from bench.agent.function_calling_agent import FunctionCallingAgent


class OpenClawAgent(FunctionCallingAgent):
    """FC 基线；名称用于实验对比列，当前逻辑与 FunctionCallingAgent 相同。"""

    pass


__all__ = ["OpenClawAgent"]
