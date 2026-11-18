"""Mixture of Agents 适配器。

Mixture of Agents (2024): 多个 LLM 并行生成方案 → 聚合器综合最优方案。
参考: Wang et al., "Mixture-of-Agents" 2024.06; togethercomputer/MoA
"""

import json
import concurrent.futures
from typing import Any, Callable

from loguru import logger

import openai


class MoAAdapter:
    """Mixture of Agents: 多 LLM 并行提案 + 聚合。

    在 tool calling 场景下的适配：
    - 多个 "proposer" 独立分析任务并提出工具调用方案（文本形式）
    - 一个 "aggregator" 综合所有提案，执行最终的工具调用
    """

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

    def _make_client(self) -> openai.OpenAI:
        return openai.OpenAI(
            api_key=self.llm_config.get("api_key", "dummy"),
            base_url=self.llm_config.get("base_url"),
            timeout=float(self.llm_config.get("timeout", 120)),
        )

    def _build_system_prompt(self, task: str) -> str:
        parts = []
        if self.domain_policy:
            parts.append(f"<policy>\n{self.domain_policy}\n</policy>")
        parts.append(f"<ticket>\n{task}\n</ticket>")
        return "\n\n".join(parts)

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        client = self._make_client()
        model = self.llm_config.get("model", "gpt-4o")
        system = self._build_system_prompt(task)
        n_proposers = 3

        # Phase 1: 并行生成 N 个提案（纯文本，不调用工具）
        proposer_prompt = (
            "Analyze the ticket and policy carefully. "
            "Propose a step-by-step plan of tool calls to complete the task. "
            "For each step, specify the tool name and arguments. "
            "Be precise with argument values."
        )

        def get_proposal(idx: int) -> str:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": proposer_prompt},
                    ],
                    temperature=0.9,
                    max_tokens=2000,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                logger.warning(f"MoA proposer {idx} failed: {e}")
                return ""

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_proposers) as pool:
            proposals = list(pool.map(get_proposal, range(n_proposers)))

        proposals = [p for p in proposals if p.strip()]
        if not proposals:
            return ""

        # Phase 2: 聚合器综合提案并执行工具调用
        proposals_text = "\n\n---\n\n".join(
            f"Proposal {i+1}:\n{p}" for i, p in enumerate(proposals)
        )

        aggregator_messages = [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": (
                    f"Here are {len(proposals)} independent proposals for completing the task:\n\n"
                    f"{proposals_text}\n\n"
                    "Synthesize the best approach from these proposals. "
                    "Now execute the optimal plan by calling the tools."
                ),
            },
        ]

        # 聚合器执行工具调用循环
        max_rounds = 20
        for _ in range(max_rounds):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=aggregator_messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=4000,
                )
            except Exception as e:
                logger.error(f"MoA aggregator error: {e}")
                break

            msg = response.choices[0].message

            if msg.tool_calls:
                # 追加 assistant 消息
                aggregator_messages.append({
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                            "type": "function",
                        }
                        for tc in msg.tool_calls
                    ],
                })

                for tc in msg.tool_calls:
                    try:
                        args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
                    except json.JSONDecodeError:
                        args = {}
                    result = call_tool(tc.function.name, args)
                    aggregator_messages.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tc.id,
                    })
            else:
                return msg.content or ""

        # 超出轮次，提取最后内容
        for m in reversed(aggregator_messages):
            if isinstance(m, dict) and m.get("role") == "assistant" and m.get("content"):
                return m["content"]
        return ""
