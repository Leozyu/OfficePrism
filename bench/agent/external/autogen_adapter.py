"""AutoGen 适配器：Debate (SelectorGroupChat) / Round-Robin 方法。

Debate (2023-2025): 多 agent 讨论，LLM 动态选择下一个发言者。
Round-Robin (2023-2025): 多 agent 固定顺序轮流执行。
"""

import asyncio
from typing import Any, Callable

from loguru import logger


class _AutoGenBase:
    """AutoGen 适配器公共基类。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

    def _make_model_client(self):
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        model_name = self.llm_config.get("model", "gpt-4o")
        kwargs: dict[str, Any] = {
            "model": model_name,
            "api_key": self.llm_config.get("api_key", "dummy"),
        }
        base_url = self.llm_config.get("base_url")
        if base_url:
            kwargs["base_url"] = base_url

        # 非标准 OpenAI 模型需要提供 model_info
        _known_prefixes = ("gpt-", "o1-", "o3-", "o4-")
        if not any(model_name.startswith(p) for p in _known_prefixes):
            kwargs["model_info"] = {
                "vision": False,
                "function_calling": True,
                "json_output": True,
                "family": "unknown",
            }

        return OpenAIChatCompletionClient(**kwargs)

    def _build_system_msg(self, role: str, task: str) -> str:
        parts = [f"You are a {role}."]
        if self.domain_policy:
            parts.append(f"\n<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"\n<ticket>\n{task}\n</ticket>")
        parts.append("\nExecute the ticket according to policy using the available tools.")
        return "".join(parts)

    def _run_async(self, coro):
        """在同步上下文中运行异步代码。"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                return pool.submit(asyncio.run, coro).result()
        else:
            return asyncio.run(coro)


class DebateAdapter(_AutoGenBase):
    """Debate 方法 (SelectorGroupChat): 多角色讨论，LLM 选择下一个发言者。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.teams import SelectorGroupChat
        from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
        from bench.agent.external.tool_bridge import to_autogen_tools

        ag_tools = to_autogen_tools(tools, call_tool)
        model_client = self._make_model_client()

        # 三角色：执行者 / 审核者 / 规划者
        executor = AssistantAgent(
            name="executor",
            model_client=model_client,
            tools=ag_tools,
            system_message=self._build_system_msg("task executor who calls tools to complete actions", task),
        )

        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=self._build_system_msg(
                "policy reviewer who checks if the executor's actions comply with policy. "
                "Point out any policy violations or suggest corrections. "
                "Say 'APPROVE' if the action is correct",
                task,
            ),
        )

        planner = AssistantAgent(
            name="planner",
            model_client=model_client,
            system_message=self._build_system_msg(
                "task planner who analyzes the ticket, breaks it into steps, "
                "and decides which agent should act next. "
                "Say 'TERMINATE' when the task is fully complete",
                task,
            ),
        )

        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

        team = SelectorGroupChat(
            participants=[planner, executor, reviewer],
            model_client=model_client,
            termination_condition=termination,
        )

        async def _run():
            result = await team.run(task=task)
            for msg in reversed(result.messages):
                content = getattr(msg, "content", "")
                if content and isinstance(content, str) and content.strip():
                    return content
            return ""

        return self._run_async(_run())


class RoundRobinAdapter(_AutoGenBase):
    """Round-Robin 方法: 多 agent 固定顺序轮流执行。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
        from bench.agent.external.tool_bridge import to_autogen_tools

        ag_tools = to_autogen_tools(tools, call_tool)
        model_client = self._make_model_client()

        # 规划者 → 执行者 → 检查者 轮流
        planner = AssistantAgent(
            name="planner",
            model_client=model_client,
            system_message=self._build_system_msg(
                "task planner who reads the ticket and produces a step-by-step plan "
                "for the executor to follow. Update the plan based on execution results",
                task,
            ),
        )

        executor = AssistantAgent(
            name="executor",
            model_client=model_client,
            tools=ag_tools,
            system_message=self._build_system_msg(
                "task executor who follows the planner's instructions and calls tools",
                task,
            ),
        )

        checker = AssistantAgent(
            name="checker",
            model_client=model_client,
            system_message=self._build_system_msg(
                "result checker who verifies the executor's work. "
                "Say 'TERMINATE' if the task is complete and all steps are done correctly",
                task,
            ),
        )

        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

        team = RoundRobinGroupChat(
            participants=[planner, executor, checker],
            termination_condition=termination,
        )

        async def _run():
            result = await team.run(task=task)
            for msg in reversed(result.messages):
                content = getattr(msg, "content", "")
                if content and isinstance(content, str) and content.strip():
                    return content
            return ""

        return self._run_async(_run())
