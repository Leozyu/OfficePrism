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

    def _make_model(self):
        """根据 llm_config 创建 smolagents 模型。"""
        from smolagents import OpenAIServerModel

        model = self.llm_config.get("model", "gpt-4o")
        api_key = self.llm_config.get("api_key", "dummy")
        base_url = self.llm_config.get("base_url")

        return OpenAIServerModel(
            model_id=model,
            api_key=api_key,
            api_base=base_url,
        )

    def _build_task_prompt(self, task: str) -> str:
        if self.domain_policy:
            return f"<policy>\n{self.domain_policy}\n</policy>\n\n<ticket>\n{task}\n</ticket>\n\nExecute the ticket according to the policy. Call tools to complete the task."
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

        native_tools = to_smolagents_tools(tools, call_tool)
        model = self._make_model()

        agent = CodeAgent(
            model=model,
            tools=native_tools,
            max_steps=30,
            verbosity_level=1,
        )

        prompt = self._build_task_prompt(task)
        result = agent.run(prompt)
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
                description=f"Specialist agent for {group_name} operations ({', '.join(group_tool_names)})",
                max_steps=15,
                verbosity_level=0,
            )
            workers.append(worker)

        if not workers:
            workers = [ToolCallingAgent(model=model, tools=native_tools, name="worker", description="General worker", max_steps=20, verbosity_level=0)]

        manager = CodeAgent(
            model=model,
            tools=[],
            managed_agents=workers,
            max_steps=20,
            verbosity_level=1,
        )

        prompt = self._build_task_prompt(task)
        result = manager.run(prompt)
        return str(result) if result else ""
