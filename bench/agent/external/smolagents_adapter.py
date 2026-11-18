"""smolagents 适配器：Code-as-Action + Hierarchical 方法。

Code-as-Action (2024): LLM 写 Python 代码调工具，支持循环/条件/组合。
Hierarchical (2023): Manager agent 规划分解 + Worker agents 分别执行子任务。
"""

from typing import Any, Callable

from loguru import logger


class _SmolAgentsBase:
    """smolagents 适配器公共基类。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _agent_token_counts(self, agent: Any) -> tuple[int, int] | None:
        """尝试从 smolagents agent 实例读取累计 token 数。

        不同版本的 smolagents 字段名不一致（Monitor.total_input_token_count
        vs 逐 step 的 memory.steps[*].token_usage），链式尝试，都取不到就
        返回 None，交由调用方保持 last_usage=None。
        """
        monitor = getattr(agent, "monitor", None)
        if monitor is not None:
            input_count = getattr(monitor, "total_input_token_count", None)
            output_count = getattr(monitor, "total_output_token_count", None)
            if input_count is not None or output_count is not None:
                return input_count or 0, output_count or 0

        memory = getattr(agent, "memory", None)
        steps = getattr(memory, "steps", None) if memory is not None else None
        if steps:
            input_total = 0
            output_total = 0
            found = False
            for step in steps:
                usage = getattr(step, "token_usage", None)
                if usage is None:
                    continue
                found = True
                input_total += getattr(usage, "input_tokens", 0) or 0
                output_total += getattr(usage, "output_tokens", 0) or 0
            if found:
                return input_total, output_total

        return None

    def _record_usage_from_agents(self, agents: list[Any]) -> None:
        totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        found_any = False
        for agent in agents:
            try:
                counts = self._agent_token_counts(agent)
            except Exception as e:
                logger.debug(f"smolagents usage extraction failed for {agent!r}: {e}")
                continue
            if counts is None:
                continue
            found_any = True
            input_tokens, output_tokens = counts
            totals["prompt_tokens"] += input_tokens
            totals["completion_tokens"] += output_tokens
            totals["total_tokens"] += input_tokens + output_tokens

        if found_any:
            self.last_usage = totals
        else:
            logger.debug("smolagents usage 字段未确认，请在实际环境校验")

    def _make_model(self):
        """根据 llm_config 创建 smolagents 模型。"""
        from smolagents import OpenAIServerModel

        model = self.llm_config.get("model", "gpt-4o")
        api_key = self.llm_config.get("api_key", "dummy")
        base_url = self.llm_config.get("base_url")
        extra_body = self.llm_config.get("extra_body")
        if "enable_thinking" in self.llm_config:
            extra_body = dict(extra_body or {})
            extra_body["enable_thinking"] = self.llm_config["enable_thinking"]

        return OpenAIServerModel(
            model_id=model,
            api_key=api_key,
            api_base=base_url,
            extra_body=extra_body,
        )

    def _build_task_prompt(self, task: str) -> str:
        if self.domain_policy:
            return (
                f"<policy>\n{self.domain_policy}\n</policy>\n\n"
                f"<ticket>\n{task}\n</ticket>\n\n"
                "严格按照 policy 执行 ticket。只能通过工具完成任务，最后输出明确结论。"
            )
        return task


class CodeActionAdapter(_SmolAgentsBase):
    """Code-as-Action 方法：LLM 生成 Python 代码来调用工具。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from smolagents import CodeAgent
        from bench.agent.external.tool_bridge import to_smolagents_tools

        self.last_usage = None
        self.last_cost = None

        native_tools = to_smolagents_tools(tools, call_tool)
        model = self._make_model()

        agent = CodeAgent(
            model=model,
            tools=native_tools,
            max_steps=30,
            verbosity_level=1,
        )

        prompt = self._build_task_prompt(task)
        try:
            result = agent.run(prompt)
        finally:
            self._record_usage_from_agents([agent])
        return str(result) if result else ""


class HierarchicalAdapter(_SmolAgentsBase):
    """Hierarchical 方法：Manager agent 规划 + Worker agents 执行。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from smolagents import CodeAgent, ToolCallingAgent
        from bench.agent.external.tool_bridge import to_smolagents_tools, split_tools_by_function

        self.last_usage = None
        self.last_cost = None

        native_tools = to_smolagents_tools(tools, call_tool)
        model = self._make_model()

        tool_groups = split_tools_by_function(tools)
        native_by_name = {t.name: t for t in native_tools}

        # 为每组创建 worker agent
        workers = []
        for group_name, group_schemas in tool_groups.items():
            group_tool_names = {s.get("function", s)["name"] for s in group_schemas}
            group_native = [native_by_name[n] for n in group_tool_names if n in native_by_name]
            if not group_native:
                continue

            worker = ToolCallingAgent(
                model=model,
                tools=group_native,
                name=f"{group_name}_worker",
                description=f"{group_name} 类操作的专门执行代理（{', '.join(group_tool_names)}）",
                max_steps=15,
                verbosity_level=0,
            )
            workers.append(worker)

        if not workers:
            workers = [ToolCallingAgent(model=model, tools=native_tools, name="worker", description="通用执行代理", max_steps=20, verbosity_level=0)]

        manager = CodeAgent(
            model=model,
            tools=[],
            managed_agents=workers,
            max_steps=20,
            verbosity_level=1,
        )

        prompt = self._build_task_prompt(task)
        try:
            result = manager.run(prompt)
        finally:
            self._record_usage_from_agents([manager, *workers])
        return str(result) if result else ""
