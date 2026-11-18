"""Hermes Agent 外部适配器。

通过 Hermes Python 库 + 本地 Tool Server 完成 OfficePrism 评测：
1. 启动 HTTP tool server，将 OfficePrism 工具暴露为 REST 端点
2. 通过 Hermes 的 terminal 工具执行 curl 调用这些端点
3. 所有工具调用经 call_tool 回调记录 trace 并修改 DB
"""

from __future__ import annotations

import re
import textwrap
from typing import Any, Callable

from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class HermesAdapter:
    """让 Hermes Agent 以自身 agent loop 完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

        self.model = llm_config.get("hermes_model", "anthropic/claude-sonnet-4")
        self.max_iterations = int(llm_config.get("hermes_max_iterations", 30))
        self.api_key = llm_config.get("hermes_api_key")
        self.base_url = llm_config.get("hermes_base_url")
        self.provider = llm_config.get(
            "hermes_provider",
            "custom" if self.base_url else None,
        )
        self.max_tokens = llm_config.get("hermes_max_tokens") or llm_config.get("max_tokens")
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _record_usage(self, agent: Any) -> None:
        """从 hermes-agent AIAgent 实例读取会话级 token/成本累计。

        hermes_agent 包在 agent/conversation_loop.py 里每次真实 LLM 调用后
        累加 session_prompt_tokens/session_completion_tokens/session_total_tokens/
        session_estimated_cost_usd 到 AIAgent 实例上；用 getattr 兜底，避免
        依赖版本升级后属性改名导致这里报错。
        """
        prompt = getattr(agent, "session_prompt_tokens", None)
        completion = getattr(agent, "session_completion_tokens", None)
        total = getattr(agent, "session_total_tokens", None)
        if prompt is None and completion is None and total is None:
            return
        prompt = prompt or 0
        completion = completion or 0
        self.last_usage = {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": total if total is not None else prompt + completion,
        }
        cost = getattr(agent, "session_estimated_cost_usd", None)
        if isinstance(cost, (int, float)):
            self.last_cost = float(cost)

    def _request_overrides(self) -> dict[str, Any] | None:
        overrides = self.llm_config.get("hermes_request_overrides")
        if overrides is not None:
            overrides = dict(overrides)
        # enable_thinking 仅 dashscope 兼容端点支持；其它网关（国外模型）不认，
        # 会直接 400。按端点而非模型名判断，避免误伤国产模型。
        base_url = (self.base_url or "").lower()
        if (not base_url or "dashscope" in base_url or "aliyuncs" in base_url) and (
            "enable_thinking" in self.llm_config
        ):
            overrides = dict(overrides or {})
            extra_body = dict(overrides.get("extra_body") or {})
            extra_body["enable_thinking"] = self.llm_config["enable_thinking"]
            overrides["extra_body"] = extra_body
        return overrides

    def _build_tool_docs(self, tools_schema: list[dict]) -> str:
        docs = []
        for schema in tools_schema:
            func = schema.get("function", schema)
            name = func["name"]
            desc = func.get("description", "")
            params = func.get("parameters", {})
            properties = params.get("properties", {})
            required = set(params.get("required", []))

            param_lines = []
            for pname, pinfo in properties.items():
                ptype = pinfo.get("type", "string")
                pdesc = pinfo.get("description", "")
                req_mark = "（必填）" if pname in required else "（可选）"
                param_lines.append(f"    - {pname} ({ptype}) {req_mark}: {pdesc}")

            params_block = "\n".join(param_lines) if param_lines else "    （无参数）"
            docs.append(f"### {name}\n{desc}\n参数:\n{params_block}")

        return "\n\n".join(docs)

    def _build_system_prompt(self, task: str, tools_schema: list[dict], server_url: str) -> str:
        tool_docs = self._build_tool_docs(tools_schema)

        return textwrap.dedent(
            f"""\
<policy>
{self.domain_policy}
</policy>

<ticket>
{task}
</ticket>

你是办公运营任务执行代理。提问人身份已经在 <ticket> 中给出，不要再询问身份。
必须严格按照 <policy> 执行任务。

## 策略：直接执行
根据 ticket 和 policy 直接调用工具，不需要显式输出推理。

## Hermes 工具协议
1. 你必须使用 `terminal` 工具执行 `curl` 命令，调用本地 OfficePrism 工具服务。
2. 严禁编造工具结果，严禁浏览文件，严禁用猜测替代工具调用。
3. 只能调用“可用工具列表”中的工具。完成任务后，必须调用 `done` 工具，并把最终结论放在 `result` 参数中。
4. 如果工具支持筛选参数，必须把用户问题中的条件填入参数；不要无参数全量查询后自行筛选。例如查询开放招聘需求时，应使用 `status` 等筛选参数。
5. list/search/find 类工具只用于定位候选记录或引用 ID；如果已经定位到目标记录且存在对应的 get_* 明细工具，必须调用该 get_* 工具确认最终字段后再作答。例如定位到 `job_requisition_ref` 后，要调用 `get_job_requisition`，不要用 `get_position_details` 替代招聘需求明细。
6. 必须使用下面的请求格式：

curl -sS --connect-timeout 5 --max-time 20 -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

7. 如果工具服务返回错误或超步数提示，停止继续调用，并基于已有证据给出最终结论。
8. 完成任务后，不要直接输出自然语言；必须通过 `/call_tool` 调用 `done`，格式为 `{{"tool_name":"done","arguments":{{"result":"最终结论"}}}}`。

## 输出规则
1. 最终结论只围绕用户问题作答。
2. 涉及薪酬、福利、排班、人事记录等问题时，必须包含工具返回中与问题直接相关的字段，尤其是金额、比例、状态、日期、城市和编号。
3. 不要添加“现在我可以回答了”这类过程性文字。

## 可用工具列表
{tool_docs}

## 用户任务
{task}
"""
        )

    def solve(self, task: str, tools: list[dict], call_tool: Callable[[str, dict], str]) -> str:
        self.last_usage = None
        self.last_cost = None
        try:
            from run_agent import AIAgent
        except ImportError as e:
            raise ImportError(
                "Hermes 依赖未安装。请执行: "
                "pip install git+https://github.com/NousResearch/hermes-agent.git"
            ) from e

        tool_server = ToolServer(call_tool=call_tool, tools_schema=tools)
        tool_server.start()
        agent = None
        try:
            system_prompt = self._build_system_prompt(task, tools, tool_server.base_url)
            agent_kwargs: dict[str, Any] = {
                "model": self.model,
                "quiet_mode": True,
                "skip_memory": True,
                "skip_context_files": True,
                "enabled_toolsets": ["terminal"],
                "ephemeral_system_prompt": system_prompt,
                "max_iterations": self.max_iterations,
            }
            request_overrides = self._request_overrides()
            if request_overrides:
                agent_kwargs["request_overrides"] = request_overrides
            if self.max_tokens:
                agent_kwargs["max_tokens"] = int(self.max_tokens)
            if self.provider:
                agent_kwargs["provider"] = self.provider
            if self.api_key:
                agent_kwargs["api_key"] = self.api_key
            if self.base_url:
                agent_kwargs["base_url"] = self.base_url

            agent = AIAgent(**agent_kwargs)
            result = agent.chat(task)
            if isinstance(result, str):
                answer = result.strip()
            else:
                answer = str(result)
            return self._clean_final_answer(answer)
        except Exception as e:
            logger.error(f"Hermes execution failed: {e}")
            return ""
        finally:
            if agent is not None:
                try:
                    self._record_usage(agent)
                except Exception as usage_exc:
                    logger.debug(f"Hermes usage extraction failed: {usage_exc}")
            tool_server.stop()

    @staticmethod
    def _extract_completion_argument(arguments: dict) -> str:
        for key in ("result", "answer", "final_answer", "text", "content"):
            value = arguments.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    @classmethod
    def _clean_final_answer(cls, answer: str, captured_final: str = "") -> str:
        text = (answer or "").strip()
        if "###STOP###" in text:
            text = text.split("###STOP###", 1)[-1].strip()

        completion = cls._extract_completion_call(text)
        if completion:
            text = completion
        elif captured_final and cls._is_meta_answer(text):
            text = captured_final.strip()

        meta_prefixes = (
            "我需要按照正确的格式输出结论。",
            "根据查询到的数据，我可以直接提供结论：",
            "现在我可以提供最终结论。",
            "我可以提供最终结论：",
        )
        changed = True
        while changed:
            changed = False
            for prefix in meta_prefixes:
                if text.startswith(prefix):
                    text = text[len(prefix):].strip()
                    changed = True

        return text.strip()

    @staticmethod
    def _extract_completion_call(text: str) -> str:
        match = re.search(r"(?:done|final_answer)\((.*)\)\s*$", text, flags=re.DOTALL)
        if not match:
            return ""
        value = match.group(1).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1].strip()
        return value

    @staticmethod
    def _is_meta_answer(text: str) -> bool:
        return text.startswith(("我需要", "现在我可以", "根据查询到的数据"))
