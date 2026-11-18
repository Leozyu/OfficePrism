"""LangGraph 适配器：LLMCompiler / Reflexion / Supervisor / Swarm 方法。

LLMCompiler (ICML 2024): 规划工具调用 DAG，无依赖的并行执行。
Reflexion (NeurIPS 2023): 执行 → 失败 → 生成反思 → 带记忆重试。
Supervisor (2024): 中央协调 agent 按任务类型分派给专家 agent。
Swarm (2024): 无中央控制，agent 间点对点 handoff。
"""

from typing import Any, Callable

from loguru import logger


class _LangGraphBase:
    """LangGraph 适配器公共基类。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy
        self.recursion_limit = int(llm_config.get("langgraph_recursion_limit", 20))
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

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

        extra_body = self.llm_config.get("extra_body")
        if "enable_thinking" in self.llm_config:
            extra_body = dict(extra_body or {})
            extra_body["enable_thinking"] = self.llm_config["enable_thinking"]

        return ChatOpenAI(
            model=self.llm_config.get("model", "gpt-4o"),
            api_key=self.llm_config.get("api_key", "dummy"),
            base_url=self.llm_config.get("base_url"),
            temperature=self.llm_config.get("temperature", 0.7),
            max_tokens=self.llm_config.get("max_tokens", 4000),
            timeout=float(self.llm_config.get("timeout", 600)),
            extra_body=extra_body,
        )

    def _build_system_prompt(self, task: str) -> str:
        parts = []
        if self.domain_policy:
            parts.append(f"<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"<ticket>\n{task}\n</ticket>")
        parts.append("严格按照 policy 执行 ticket。只能通过工具完成任务，完成后输出明确结论。")
        return "\n\n".join(parts)

    def _extract_answer(self, result: dict) -> str:
        messages = result.get("messages", [])
        for msg in reversed(messages):
            content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
            if content and isinstance(content, str):
                return content
        return ""

    def _invoke_graph(self, graph, task: str) -> dict:
        return graph.invoke(
            {"messages": [("user", task)]},
            {"recursion_limit": self.recursion_limit},
        )


class LLMCompilerAdapter(_LangGraphBase):
    """LLMCompiler: DAG 规划 + 并行工具执行。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from langgraph.prebuilt import create_react_agent
        from bench.agent.external.tool_bridge import to_langchain_tools

        # LLMCompiler 的完整实现需要自定义 Planner/Executor/Joiner graph。
        # 这里用 create_react_agent + parallel_tool_calls 作为简化版本，
        # 它允许模型在单步中生成多个并行 tool call。
        lc_tools = to_langchain_tools(tools, call_tool)
        model = self._make_chat_model()
        prompt = self._build_system_prompt(task)

        agent = create_react_agent(
            model,
            tools=lc_tools,
            prompt=prompt,
        )

        result = self._invoke_graph(agent, task)
        totals = self._new_totals()
        self._accumulate_from_messages(totals, result.get("messages", []))
        self.last_usage = totals
        return self._extract_answer(result)


class ReflexionAdapter(_LangGraphBase):
    """Reflexion: 执行 → critique → 带反思重试，最多 max_retries 轮。"""

    MAX_RETRIES = 3

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from langgraph.prebuilt import create_react_agent
        from bench.agent.external.tool_bridge import to_langchain_tools

        lc_tools = to_langchain_tools(tools, call_tool)
        model = self._make_chat_model()
        system_prompt = self._build_system_prompt(task)

        critique_prompt = (
            "请根据 policy 和 ticket 检查代理的工具调用和结果。"
            "如果存在错误、违反政策或任务未完成，请指出需要修正的具体问题。"
            "如果全部正确且任务已完成，只回复：LGTM"
        )

        agent = create_react_agent(model, tools=lc_tools, prompt=system_prompt)
        messages_input = [("user", task)]
        totals = self._new_totals()

        for attempt in range(self.MAX_RETRIES):
            result = agent.invoke(
                {"messages": messages_input},
                {"recursion_limit": self.recursion_limit},
            )
            self._accumulate_from_messages(totals, result.get("messages", []))
            answer = self._extract_answer(result)

            if attempt == self.MAX_RETRIES - 1:
                self.last_usage = totals
                return answer

            critique_response = model.invoke([
                {"role": "system", "content": critique_prompt},
                {"role": "user", "content": f"Agent output:\n{answer}"},
            ])
            self._accumulate_from_messages(totals, [critique_response])
            feedback = (critique_response.content or "").strip()
            if not feedback or "LGTM" in feedback.upper():
                self.last_usage = totals
                return answer

            logger.info(f"Reflexion attempt {attempt + 1}: critique feedback received, retrying")
            messages_input = [("user", f"{task}\n\n[Reflection from previous attempt]\n{feedback}")]

        self.last_usage = totals
        return answer


class SupervisorAdapter(_LangGraphBase):
    """Supervisor: 中央协调 agent 分派给专家 agent。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from langgraph.prebuilt import create_react_agent
        from bench.agent.external.tool_bridge import to_langchain_tools, split_tools_by_function

        model = self._make_chat_model()
        tool_groups = split_tools_by_function(tools)

        # 为每组创建专家 agent
        workers = []
        for group_name, group_schemas in tool_groups.items():
            group_lc_tools = to_langchain_tools(group_schemas, call_tool)
            tool_names = [s.get("function", s)["name"] for s in group_schemas]
            worker = create_react_agent(
                model,
                tools=group_lc_tools,
                prompt=f"你是 {group_name} 类工具的专门执行代理。可用工具：{', '.join(tool_names)}。请按任务要求调用工具完成工作。",
                name=f"{group_name}_agent",
            )
            workers.append(worker)

        if not workers:
            all_tools = to_langchain_tools(tools, call_tool)
            worker = create_react_agent(model, tools=all_tools, prompt="请调用工具完成任务。", name="worker")
            workers = [worker]

        totals = self._new_totals()
        try:
            from langgraph_supervisor import create_supervisor

            system_prompt = self._build_system_prompt(task)
            workflow = create_supervisor(
                agents=workers,
                model=model,
                prompt=system_prompt,
                include_agent_name="inline",
            )
            compiled = workflow.compile()
            result = self._invoke_graph(compiled, task)
            self._accumulate_from_messages(totals, result.get("messages", []))
            self.last_usage = totals
            return self._extract_answer(result)

        except ImportError:
            logger.warning("langgraph-supervisor not installed, falling back to plain ReAct")
            all_tools = to_langchain_tools(tools, call_tool)
            agent = create_react_agent(model, tools=all_tools, prompt=self._build_system_prompt(task))
            result = self._invoke_graph(agent, task)
            self._accumulate_from_messages(totals, result.get("messages", []))
            self.last_usage = totals
            return self._extract_answer(result)


class SwarmAdapter(_LangGraphBase):
    """Swarm: 无中央控制，agent 间点对点 handoff。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from langgraph.prebuilt import create_react_agent
        from bench.agent.external.tool_bridge import to_langchain_tools, split_tools_by_function

        model = self._make_chat_model()
        tool_groups = split_tools_by_function(tools)
        totals = self._new_totals()

        try:
            from langgraph_swarm import create_swarm, create_handoff_tool

            agent_names = list(tool_groups.keys())
            agents = []

            for i, (group_name, group_schemas) in enumerate(tool_groups.items()):
                group_lc_tools = to_langchain_tools(group_schemas, call_tool)

                # 添加 handoff 工具到其他 agent
                handoff_tools = []
                for other_name in agent_names:
                    if other_name != group_name:
                        handoff_tools.append(
                            create_handoff_tool(
                                agent_name=f"{other_name}_agent",
                                description=f"转交给 {other_name} 类工具的专门执行代理。",
                            )
                        )

                agent = create_react_agent(
                    model,
                    tools=group_lc_tools + handoff_tools,
                    prompt=f"你是 {group_name} 类工具的专门执行代理。\n\n{self._build_system_prompt(task)}",
                    name=f"{group_name}_agent",
                )
                agents.append(agent)

            if not agents:
                all_tools = to_langchain_tools(tools, call_tool)
                agents = [create_react_agent(model, tools=all_tools, prompt=self._build_system_prompt(task), name="worker")]

            workflow = create_swarm(
                agents=agents,
                default_active_agent=f"{agent_names[0]}_agent" if agent_names else "worker",
            )
            compiled = workflow.compile()
            result = self._invoke_graph(compiled, task)
            self._accumulate_from_messages(totals, result.get("messages", []))
            self.last_usage = totals
            return self._extract_answer(result)

        except ImportError:
            logger.warning("langgraph-swarm not installed, falling back to plain ReAct")
            all_tools = to_langchain_tools(tools, call_tool)
            agent = create_react_agent(model, tools=all_tools, prompt=self._build_system_prompt(task))
            result = self._invoke_graph(agent, task)
            self._accumulate_from_messages(totals, result.get("messages", []))
            self.last_usage = totals
            return self._extract_answer(result)
