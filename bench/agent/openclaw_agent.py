"""OpenClaw 评测注册名：`openclaw_agent`

说明：OpenClaw 作为独立网关服务运行在外部，bench 通过 HTTP 发送任务。
评测时使用 `--agent ext_openclaw` 走外部适配器路径（ExternalAgentRunner），
此文件仅为 registry 中的占位注册，实际逻辑在
`bench.agent.external.openclaw_adapter.OpenClawAdapter`。
"""

from __future__ import annotations

from bench.agent.function_calling_agent import FunctionCallingAgent


class OpenClawAgent(FunctionCallingAgent):
    """占位注册；实际评测请用 --agent ext_openclaw。"""

    pass


__all__ = ["OpenClawAgent"]
