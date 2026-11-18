"""Deep Agents 外部适配器（进程内直跑）。

deepagents 是 LangChain 的 "deep agent" 库：在 create_react_agent 之上叠加了
规划（write_todos）、虚拟文件系统、子代理（task）、上下文摘要等中间件，本身就是
一个 agent harness。这里让它以自身的 agent loop 完成 OfficePrism 任务：

1. 把 OfficePrism 的 (OpenAI tool schema, call_tool) 通过 tool_bridge 转成
   LangChain StructuredTool；
2. 用 llm_config 构造一个 OpenAI 兼容的 ChatOpenAI（走 dashscope / 网关 等）；
3. create_deep_agent(model, tools=..., system_prompt=policy+ticket) 组装图；
4. graph.invoke({"messages": [("user", ticket)]}) 跑到结束，取最后一条文本消息为答案；
5. 从 AIMessage.usage_metadata 汇总 token 用量挂到 last_usage，供下游记账。

与 langgraph_adapter 的区别只是把 create_react_agent 换成 create_deep_agent，
从而带上 deepagents 的完整 harness。内置工具（write_todos/文件系统/execute/task）
默认走内存 StateBackend，不触碰真实磁盘，也不经过 call_tool，因此不计入 max_steps，
只有真正的 domain 工具调用才计步。
"""

from __future__ import annotations

from typing import Any, Callable

from loguru import logger

# 部分模型的后端已弃用 temperature 参数：显式下发会被 400 拒绝
# （claude 系经 Anthropic 兼容网关报 "`temperature` is deprecated for this model"，
# 网关对 claude 带 temperature 一律拒）。对这些模型省略 temperature；其余模型行为不变。
# 按模型名子串匹配，便于后续扩充；省略无副作用（1.0 即后端默认值）。
_TEMPERATURE_UNSUPPORTED = ("claude-opus-4-8", "claude-opus-4-7", "claude-sonnet-5")

# 部分模型的后端拒绝 enable_thinking（DashScope/Qwen 系参数）：
# claude-opus-4-8 / claude-opus-4-7 经 Anthropic 兼容网关报
# "enable_thinking: Extra inputs are not permitted"。
# 对这些模型不把 enable_thinking 注入 extra_body（gpt-5.5 等能容忍，不受影响）。
_ENABLE_THINKING_UNSUPPORTED = ("claude-opus-4-8", "claude-opus-4-7", "claude-sonnet-5")


class DeepAgentsAdapter:
    """让 deepagents 以自身 agent loop 完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy
        # deepagents 的图每个工具轮要过多个 middleware 节点（super-step），比裸
        # ReAct 多得多；recursion_limit 必须给足，让 ExternalAgentRunner 的 max_steps
        # 成为实际上限。注意不能回退到 app.yaml 的 langgraph_recursion_limit（那是给
        # 裸 ReAct 用的、默认才 20），否则复杂模型几轮就撞 GRAPH_RECURSION_LIMIT。
        self.recursion_limit = int(llm_config.get("deepagents_recursion_limit", 400))
        self.last_usage: dict | None = None
        self.last_cost: float | None = None
        self.last_error: str | None = None

    # ------------------------------------------------------------------ helpers
    def _new_totals(self) -> dict[str, int]:
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def _accumulate_from_messages(self, totals: dict[str, int], messages: list) -> None:
        """从 LangChain AIMessage.usage_metadata 累加 token 用量。"""
        for msg in messages:
            usage = getattr(msg, "usage_metadata", None)
            if not usage:
                continue
            totals["prompt_tokens"] += usage.get("input_tokens", 0) or 0
            totals["completion_tokens"] += usage.get("output_tokens", 0) or 0
            totals["total_tokens"] += usage.get("total_tokens", 0) or 0

    def _make_chat_model(self):
        from langchain_openai import ChatOpenAI

        cfg = self.llm_config
        model_name = cfg.get("model", "gpt-4o")
        extra_body = cfg.get("extra_body")
        # enable_thinking 是 DashScope/Qwen 系参数；部分模型（如 claude-opus-4-8）后端
        # 会拒绝 "enable_thinking: Extra inputs are not permitted"，对这些模型不注入。
        if "enable_thinking" in cfg and not any(
            m in model_name for m in _ENABLE_THINKING_UNSUPPORTED
        ):
            extra_body = dict(extra_body or {})
            extra_body["enable_thinking"] = cfg["enable_thinking"]

        max_out = int(cfg.get("max_tokens", 8192))  # 最大输出 token
        chat_kwargs: dict[str, Any] = dict(
            model=model_name,
            api_key=cfg.get("api_key", "dummy"),
            base_url=cfg.get("base_url"),
            max_tokens=max_out,
            timeout=float(cfg.get("timeout", 600)),
            extra_body=extra_body,
        )
        # 仅在模型支持时下发 temperature：部分模型（如 claude-opus-4-8）后端已弃用该
        # 参数，显式传会 400；配置里显式设为 null 也视为不下发。
        temperature = cfg.get("temperature", 1.0)
        if temperature is not None and not any(
            m in model_name for m in _TEMPERATURE_UNSUPPORTED
        ):
            chat_kwargs["temperature"] = temperature
        model = ChatOpenAI(**chat_kwargs)

        # 上下文窗口：deepagents 的 SummarizationMiddleware 依据 model.profile 的
        # max_input_tokens 决定何时压缩上下文（有 profile 按其 85% 触发；无 profile
        # 回退到固定 170k 阈值）。dashscope 等自定义 base_url 模型默认无 profile，
        # 这里显式注入真实上下文窗口（默认 1,000,000），让摘要按 1M 窗口触发。
        context_window = int(
            cfg.get("deepagents_context_window", cfg.get("max_input_tokens", 1_000_000))
        )
        profile = dict(getattr(model, "profile", None) or {})
        profile["max_input_tokens"] = context_window
        profile.setdefault("max_output_tokens", max_out)
        try:
            model.profile = profile
        except Exception as e:  # pragma: no cover - 个别模型 profile 只读
            logger.warning(f"set model.profile failed（摘要将回退固定阈值）: {e}")

        return model

    def _build_system_prompt(self, task: str) -> str:
        parts = []
        if self.domain_policy:
            parts.append(f"<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"<ticket>\n{task}\n</ticket>")
        parts.append(
            "严格按照 policy 执行 ticket。只能通过工具完成任务，完成后输出明确结论。"
        )
        return "\n\n".join(parts)

    def _extract_answer(self, result: dict) -> str:
        messages = result.get("messages", [])
        for msg in reversed(messages):
            content = getattr(msg, "content", None) or (
                msg.get("content") if isinstance(msg, dict) else None
            )
            if content and isinstance(content, str):
                return content
        return ""

    # -------------------------------------------------------------------- solve
    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        try:
            from deepagents import create_deep_agent

            from bench.agent.external.tool_bridge import to_langchain_tools
        except ImportError as e:
            # 缺依赖属于基础设施失败：记 last_error 让 run_domain_eval 写 error 行触发重跑，
            # 而不是被当成一次真实的 0 分任务。
            self.last_error = (
                f"deepagents import failed: {e}. "
                f"pip install -e libs/deepagents langchain-openai"
            )
            logger.error(self.last_error)
            return ""

        lc_tools = to_langchain_tools(tools, call_tool)
        model = self._make_chat_model()
        system_prompt = self._build_system_prompt(task)

        try:
            # 传入已配置好的 ChatOpenAI 实例（而非模型字符串），避免 deepagents
            # 回退到默认 Anthropic 模型。AnthropicPromptCachingMiddleware 以
            # unsupported_model_behavior="ignore" 挂载，对非 Anthropic 模型 no-op。
            agent = create_deep_agent(
                model=model,
                tools=lc_tools,
                system_prompt=system_prompt,
            )
            result = agent.invoke(
                {"messages": [("user", task)]},
                {"recursion_limit": self.recursion_limit},
            )
        except Exception as e:
            self.last_error = f"deepagents run failed: {e}"
            logger.error(self.last_error)
            import traceback

            logger.error(traceback.format_exc())
            return ""

        totals = self._new_totals()
        self._accumulate_from_messages(totals, result.get("messages", []))
        self.last_usage = totals
        return self._extract_answer(result)
