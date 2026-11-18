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

    def _make_chat_model(self):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=self.llm_config.get("model", "gpt-4o"),
            api_key=self.llm_config.get("api_key", "dummy"),
            base_url=self.llm_config.get("base_url"),
            temperature=self.llm_config.get("temperature", 0.7),
            max_tokens=self.llm_config.get("max_tokens", 4000),
        )

    def _build_system_prompt(self, task: str) -> str:
        parts = []
        if self.domain_policy:
            parts.append(f"<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"<ticket>\n{task}\n</ticket>")
        parts.append("Execute the ticket according to the policy. Call tools to complete the task. When done, provide a final answer.")
        return "\n\n".join(parts)

    def _extract_answer(self, result: dict) -> str:
        messages = result.get("messages", [])
        for msg in reversed(messages):
            content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
            if content and isinstance(content, str):
                return content
        return ""


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

        result = agent.invoke({"messages": [("user", task)]})
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
            "Review the agent's actions and results against the policy and ticket. "
            "If there are errors, policy violations, or the task is incomplete, "
            "provide specific feedback on what to fix. "
            "If everything is correct and complete, reply ONLY with: LGTM"
        )

        agent = create_react_agent(model, tools=lc_tools, prompt=system_prompt)
        messages_input = [("user", task)]

        for attempt in range(self.MAX_RETRIES):
            result = agent.invoke({"messages": messages_input})
            answer = self._extract_answer(result)

            if attempt == self.MAX_RETRIES - 1:
                return answer

            critique_response = model.invoke([
                {"role": "system", "content": critique_prompt},
                {"role": "user", "content": f"Agent output:\n{answer}"},
            ])
            feedback = (critique_response.content or "").strip()
            if not feedback or "LGTM" in feedback.upper():
                return answer

            logger.info(f"Reflexion attempt {attempt + 1}: critique feedback received, retrying")
            messages_input = [("user", f"{task}\n\n[Reflection from previous attempt]\n{feedback}")]

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
                prompt=f"You are a {group_name} specialist. Available tools: {', '.join(tool_names)}. Execute tool calls as instructed.",
                name=f"{group_name}_agent",
            )
            workers.append(worker)

        if not workers:
            all_tools = to_langchain_tools(tools, call_tool)
            worker = create_react_agent(model, tools=all_tools, prompt="Execute tool calls.", name="worker")
            workers = [worker]

        try:
            from langgraph_supervisor import create_supervisor

            system_prompt = self._build_system_prompt(task)
            workflow = create_supervisor(
                agents=workers,
                model=model,
                prompt=system_prompt,
            )
            compiled = workflow.compile()
            result = compiled.invoke({"messages": [("user", task)]})
            return self._extract_answer(result)

        except ImportError:
            logger.warning("langgraph-supervisor not installed, falling back to plain ReAct")
            all_tools = to_langchain_tools(tools, call_tool)
            agent = create_react_agent(model, tools=all_tools, prompt=self._build_system_prompt(task))
            result = agent.invoke({"messages": [("user", task)]})
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
                                description=f"Hand off to the {other_name} specialist agent.",
                            )
                        )

                agent = create_react_agent(
                    model,
                    tools=group_lc_tools + handoff_tools,
                    prompt=f"You are a {group_name} specialist. {self._build_system_prompt(task)}",
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
            result = compiled.invoke({"messages": [("user", task)]})
            return self._extract_answer(result)

        except ImportError:
            logger.warning("langgraph-swarm not installed, falling back to plain ReAct")
            all_tools = to_langchain_tools(tools, call_tool)
            agent = create_react_agent(model, tools=all_tools, prompt=self._build_system_prompt(task))
            result = agent.invoke({"messages": [("user", task)]})
            return self._extract_answer(result)
