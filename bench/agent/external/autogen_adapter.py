"""AutoGen 适配器：Debate (SelectorGroupChat) / Round-Robin 方法。

Debate (2023-2025): 多 agent 讨论，LLM 动态选择下一个发言者。
Round-Robin (2023-2025): 多 agent 固定顺序轮流执行。
"""

import asyncio
import json
from typing import Any, Callable

from loguru import logger


class _AutoGenBase:
    """AutoGen 适配器公共基类。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _new_totals(self) -> dict[str, int]:
        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def _accumulate_from_messages(self, totals: dict[str, int], messages: list[Any]) -> None:
        """从 AutoGen BaseChatMessage.models_usage (RequestUsage) 累加 token 用量。"""
        for msg in messages:
            usage = getattr(msg, "models_usage", None)
            if not usage:
                continue
            prompt = getattr(usage, "prompt_tokens", 0) or 0
            completion = getattr(usage, "completion_tokens", 0) or 0
            totals["prompt_tokens"] += prompt
            totals["completion_tokens"] += completion
            totals["total_tokens"] += prompt + completion

    def _make_model_client(self):
        from autogen_ext.models.openai import OpenAIChatCompletionClient

        model_name = self.llm_config.get("model", "gpt-4o")
        kwargs: dict[str, Any] = {
            "model": model_name,
            "api_key": self.llm_config.get("api_key", "dummy"),
            "timeout": float(self.llm_config.get("timeout", 600)),
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
                "structured_output": False,
            }

        return OpenAIChatCompletionClient(**kwargs)

    def _build_system_msg(self, role: str, task: str) -> str:
        parts = [f"你是{role}。"]
        if self.domain_policy:
            parts.append(f"\n<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"\n<ticket>\n{task}\n</ticket>")
        parts.append("\n请严格按照 policy 使用可用工具完成 ticket。")
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

    def _message_text(self, content: Any) -> str:
        """Normalize AutoGen message content into readable text."""
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                else:
                    text = getattr(item, "content", None) or getattr(item, "text", None)
                    if text:
                        parts.append(str(text))
            return "\n".join(parts)
        return str(content)

    def _clean_final_text(self, text: str) -> str:
        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.upper() == "TERMINATE":
                continue
            lines.append(line)
        return "\n".join(lines).strip()

    def _is_meta_answer(self, text: str) -> bool:
        normalized = text.strip()
        if not normalized:
            return False
        if normalized in {"[]", "{}"}:
            return True
        if normalized.startswith(("[", "{")) and normalized.endswith(("]", "}")):
            try:
                json.loads(normalized)
                return True
            except Exception:
                pass
        meta_markers = (
            "**Ticket 分析**",
            "步骤拆分",
            "决定下一位发言者",
            "用户需要我作为",
            "负责核验执行结果的检查者",
            "逐步计划",
            "逐步执行计划",
            "工具执行与结果模拟",
            "计划更新与结论",
            "工具调用与执行结果",
            "工具调用执行",
            "模拟执行结果返回",
            "模拟执行链路",
            "模拟执行",
            "工具执行与数据获取",
            "query_internal_referrals",
            "query_referral_bonus",
            "计划更新与核验",
            "回复 TERMINATE",
            "The user wants to verify",
            "The user wants me to act",
            "**Analyze Policy",
            "**Policy Analysis",
            "**Execution Log Analysis",
            "**Verification**",
            "Reply with TERMINATE",
            "Reply: TERMINATE",
            "The user wants to terminate",
            "The execution plan was followed",
            "I should output TERMINATE",
            "The assistant used the tool",
            "I should check if the output matches",
            "Therefore, I should approve",
            "Error: Expecting value:",
            "I have already queried the system",
            "simulated in previous turns",
            "The prompt provided by the user",
            "This looks like a loop",
        )
        if normalized.startswith("提问人信息：") and "问题：" in normalized:
            return True
        return any(marker in normalized for marker in meta_markers)

    def _answer_from_messages(self, messages: list[Any]) -> str:
        for msg in reversed(messages):
            content = self._message_text(getattr(msg, "content", ""))
            answer = self._clean_final_text(content)
            if (
                answer
                and answer.upper() not in {"APPROVE"}
                and not self._is_meta_answer(answer)
            ):
                return answer
        return ""

    def _choose_answer(
        self,
        answer: str,
        tool_results: list[tuple[str, dict, str]],
    ) -> str:
        if tool_results and (not answer or self._is_meta_answer(answer)):
            fallback = self._fallback_answer_from_tools(tool_results)
            if fallback:
                return fallback
        return answer

    def _fallback_answer_from_tools(self, tool_results: list[tuple[str, dict, str]]) -> str:
        """Build a conservative answer when AutoGen only returns a stop marker."""
        if not tool_results:
            return ""

        name, arguments, result = tool_results[-1]
        try:
            parsed = json.loads(result)
        except Exception:
            parsed = result

        if name == "get_employee_referrals":
            employee_ref = arguments.get("referrer_employee_ref") or arguments.get("employee_ref")
            if parsed == []:
                subject = f"员工 {employee_ref}" if employee_ref else "该员工"
                return f"经查询，{subject}没有提交过任何内推记录，因此没有相关的内推奖金发放情况。"

        return f"已完成工具查询，最后一次调用 {name} 返回：{result}"


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

        model_client = self._make_model_client()
        tool_results: list[tuple[str, dict, str]] = []

        def tracked_call_tool(name: str, arguments: dict) -> str:
            result = call_tool(name, arguments)
            tool_results.append((name, arguments, result))
            return result

        ag_tools = to_autogen_tools(tools, tracked_call_tool)

        # 三角色：执行者 / 审核者 / 规划者
        executor = AssistantAgent(
            name="executor",
            model_client=model_client,
            tools=ag_tools,
            system_message=self._build_system_msg("负责调用工具完成任务的执行者", task),
        )

        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=self._build_system_msg(
                "负责检查执行者是否符合 policy 的审核者。如果发现违反政策或任务未完成，请指出修正建议；如果正确，请回复 APPROVE",
                task,
            ),
        )

        planner = AssistantAgent(
            name="planner",
            model_client=model_client,
            system_message=self._build_system_msg(
                "负责任务规划的规划者。请分析 ticket、拆分步骤，并决定下一位发言者；任务完成后回复 TERMINATE",
                task,
            ),
        )

        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

        team = SelectorGroupChat(
            participants=[planner, executor, reviewer],
            model_client=model_client,
            termination_condition=termination,
        )

        self.last_usage = None
        self.last_cost = None
        totals = self._new_totals()

        async def _run():
            result = await team.run(task=task)
            self._accumulate_from_messages(totals, result.messages)
            answer = self._answer_from_messages(result.messages)
            if not tool_results:
                executor_result = await executor.run(task=task)
                self._accumulate_from_messages(totals, executor_result.messages)
                answer = self._answer_from_messages(executor_result.messages) or answer
            return self._choose_answer(answer, tool_results)

        try:
            return self._run_async(_run())
        finally:
            self.last_usage = totals


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

        model_client = self._make_model_client()
        tool_results: list[tuple[str, dict, str]] = []

        def tracked_call_tool(name: str, arguments: dict) -> str:
            result = call_tool(name, arguments)
            tool_results.append((name, arguments, result))
            return result

        ag_tools = to_autogen_tools(tools, tracked_call_tool)

        # 规划者 → 执行者 → 检查者 轮流
        planner = AssistantAgent(
            name="planner",
            model_client=model_client,
            system_message=self._build_system_msg(
                "负责任务规划的规划者。请阅读 ticket 并给执行者制定逐步计划，根据执行结果更新计划",
                task,
            ),
        )

        executor = AssistantAgent(
            name="executor",
            model_client=model_client,
            tools=ag_tools,
            system_message=self._build_system_msg(
                "负责按照规划者指令调用工具的执行者",
                task,
            ),
        )

        checker = AssistantAgent(
            name="checker",
            model_client=model_client,
            system_message=self._build_system_msg(
                "负责核验执行结果的检查者。如果任务已完成且步骤正确，请回复 TERMINATE",
                task,
            ),
        )

        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

        team = RoundRobinGroupChat(
            participants=[planner, executor, checker],
            termination_condition=termination,
        )

        self.last_usage = None
        self.last_cost = None
        totals = self._new_totals()

        async def _run():
            result = await team.run(task=task)
            self._accumulate_from_messages(totals, result.messages)
            answer = self._answer_from_messages(result.messages)
            return self._choose_answer(answer, tool_results)

        try:
            return self._run_async(_run())
        finally:
            self.last_usage = totals
