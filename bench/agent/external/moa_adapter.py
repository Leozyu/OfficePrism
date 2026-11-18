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
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _accumulate_usage(self, totals: dict[str, int], response: Any) -> None:
        usage = getattr(response, "usage", None)
        if not usage:
            return
        totals["prompt_tokens"] += usage.prompt_tokens or 0
        totals["completion_tokens"] += usage.completion_tokens or 0
        totals["total_tokens"] += usage.total_tokens or 0

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

    def _extra_body(self) -> dict[str, Any] | None:
        extra_body = self.llm_config.get("extra_body")
        if "enable_thinking" in self.llm_config:
            extra_body = dict(extra_body or {})
            extra_body["enable_thinking"] = self.llm_config["enable_thinking"]
        return extra_body

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        self.last_usage = None
        self.last_cost = None
        totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        client = self._make_client()
        model = self.llm_config.get("model", "gpt-4o")
        system = self._build_system_prompt(task)
        n_proposers = 3
        extra_body = self._extra_body()

        # Phase 1: 并行生成 N 个提案（纯文本，不调用工具）
        proposer_prompt = (
            "请仔细分析 ticket 和 policy。"
            "提出一个逐步工具调用计划来完成任务。"
            "每一步都要写清楚工具名和参数。"
            "参数值必须准确。"
        )

        def get_proposal(idx: int) -> tuple[str, Any]:
            try:
                req_kwargs = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": proposer_prompt},
                    ],
                    "temperature": 0.9,
                    "max_tokens": 2000,
                }
                if extra_body:
                    req_kwargs["extra_body"] = extra_body
                response = client.chat.completions.create(**req_kwargs)
                return response.choices[0].message.content or "", response
            except Exception as e:
                logger.warning(f"MoA proposer {idx} failed: {e}")
                return "", None

        with concurrent.futures.ThreadPoolExecutor(max_workers=n_proposers) as pool:
            # 每个 proposer 在独立线程里跑，usage 累加放到线程池 join 之后按序处理，
            # 避免多线程并发写 totals 字典引入竞态。
            proposal_results = list(pool.map(get_proposal, range(n_proposers)))

        for _, response in proposal_results:
            if response is not None:
                self._accumulate_usage(totals, response)

        proposals = [p for p, _ in proposal_results if p.strip()]
        if not proposals:
            self.last_usage = dict(totals)
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
                    f"下面是 {len(proposals)} 个独立完成方案：\n\n"
                    f"{proposals_text}\n\n"
                    "请综合这些方案，选择最稳妥的执行路径。"
                    "现在通过调用工具执行最优计划。"
                ),
            },
        ]

        # 聚合器执行工具调用循环
        max_rounds = 20
        for _ in range(max_rounds):
            try:
                req_kwargs = {
                    "model": model,
                    "messages": aggregator_messages,
                    "tools": tools,
                    "tool_choice": "auto",
                    "temperature": 0.3,
                    "max_tokens": 4000,
                }
                if extra_body:
                    req_kwargs["extra_body"] = extra_body
                response = client.chat.completions.create(**req_kwargs)
            except Exception as e:
                logger.error(f"MoA aggregator error: {e}")
                break

            self._accumulate_usage(totals, response)
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
                self.last_usage = dict(totals)
                return msg.content or ""

        self.last_usage = dict(totals)

        # 超出轮次，提取最后内容
        for m in reversed(aggregator_messages):
            if isinstance(m, dict) and m.get("role") == "assistant" and m.get("content"):
                return m["content"]
        return ""
