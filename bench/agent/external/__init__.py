"""外部 Agent 方法工厂。

通过 get_external_agent(name, ...) 获取实现了 ExternalAgentProtocol 的适配器实例。
所有 ext_ 前缀的 agent 名称在 run_domain_eval.py 中被路由到此模块。
"""

from typing import Any

from loguru import logger

from bench.agent.external_adapter import ExternalAgentProtocol

EXTERNAL_AGENTS: dict[str, str] = {
    # 单 agent 方法
    "ext_code_action": "bench.agent.external.smolagents_adapter:CodeActionAdapter",
    "ext_llmcompiler": "bench.agent.external.langgraph_adapter:LLMCompilerAdapter",
    "ext_reflexion": "bench.agent.external.langgraph_adapter:ReflexionAdapter",
    # multi-agent 方法
    "ext_supervisor": "bench.agent.external.langgraph_adapter:SupervisorAdapter",
    "ext_swarm": "bench.agent.external.langgraph_adapter:SwarmAdapter",
    "ext_debate": "bench.agent.external.autogen_adapter:DebateAdapter",
    "ext_round_robin": "bench.agent.external.autogen_adapter:RoundRobinAdapter",
    "ext_moa": "bench.agent.external.moa_adapter:MoAAdapter",
    "ext_openclaw": "bench.agent.external.openclaw_adapter:OpenClawAdapter",
    "ext_claude_code": "bench.agent.external.claude_code_adapter:ClaudeCodeAdapter",
    "ext_hermes": "bench.agent.external.hermes_adapter:HermesAdapter",
    "ext_deerflow": "bench.agent.external.deerflow_adapter:DeerFlowAdapter",
    "ext_deepagents": "bench.agent.external.deepagents_adapter:DeepAgentsAdapter",
    "ext_agentzero": "bench.agent.external.agentzero_adapter:AgentZeroAdapter",
    "ext_xagent": "bench.agent.external.xagent_adapter:XAgentAdapter",
    "ext_hierarchical": "bench.agent.external.smolagents_adapter:HierarchicalAdapter",
}


def get_external_agent(
    name: str,
    llm_config: dict[str, Any] | None = None,
    domain_policy: str = "",
) -> ExternalAgentProtocol:
    """根据名称获取外部 agent 适配器实例。"""
    if name not in EXTERNAL_AGENTS:
        available = ", ".join(sorted(EXTERNAL_AGENTS))
        raise KeyError(f"Unknown external agent '{name}'. Available: {available}")

    module_path, cls_name = EXTERNAL_AGENTS[name].rsplit(":", 1)

    import importlib
    try:
        mod = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError(
            f"Failed to import {module_path} for agent '{name}'. "
            f"Install the required package: {e}"
        ) from e

    cls = getattr(mod, cls_name)
    instance = cls(llm_config=llm_config or {}, domain_policy=domain_policy)

    if not isinstance(instance, ExternalAgentProtocol):
        raise TypeError(f"{cls_name} does not implement ExternalAgentProtocol")

    logger.info(f"Loaded external agent: {name} -> {cls_name}")
    return instance
