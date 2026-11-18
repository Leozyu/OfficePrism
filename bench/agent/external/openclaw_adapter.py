"""OpenClaw 外部适配器。

通过 HTTP 调用远端 OpenClaw 网关服务：
1. 启动本地 Tool Server，将 OfficePrism 工具暴露为 REST 端点
2. 向 OpenClaw 网关发送任务 prompt，告知它通过 HTTP 调用工具
3. OpenClaw 网关自主规划、调用工具、完成任务
4. 所有工具调用经 call_tool 回调记录 trace 并修改 DB

OpenClaw 作为独立服务/网关运行在外部，bench 只通过 HTTP 发任务给它。
"""

import json
import os
import textwrap
import uuid
from urllib import error, request
from typing import Callable, Any

from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class OpenClawAdapter:
    """通过 HTTP 调用远端 OpenClaw 网关完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy
        self.timeout = float(llm_config.get("timeout", 600))

        # OpenClaw 网关地址（OPENCLAW_BASE_URL 环境变量优先，便于指向独立网关实例）
        base_url = os.environ.get("OPENCLAW_BASE_URL") or llm_config.get(
            "openclaw_base_url", "http://127.0.0.1:18789/v1"
        )
        if not (base_url.endswith("/v1") or base_url.endswith("/v1/")):
            base_url = f"{base_url.rstrip('/')}/v1"
        self.base_url = base_url.rstrip("/")
        self.api_key = llm_config.get("openclaw_api_key", "openclaw")
        self.agent_id = llm_config.get("openclaw_agent_id", "main")

        # 模型选择：优先用环境变量 OPENCLAW_PROVIDER_MODEL 切换模型
        self.model = llm_config.get("model", "qwen4-max")
        self.provider_model = os.environ.get("OPENCLAW_PROVIDER_MODEL") or llm_config.get(
            "openclaw_provider_model",
            f"custom-dashscope-aliyuncs-com/{self.model}",
        )

        # Tool Server 配置：远端 OpenClaw 需要回调的地址
        self.tool_server_host = llm_config.get("openclaw_tool_server_host", "127.0.0.1")

        self.http_max_tokens = int(llm_config.get("openclaw_http_max_tokens", 4096))
        # token 记账代理（可选的外部 usage 代理服务，按 URL 配置）。网关自身不回传上游
        # usage（session 里恒为 0），设 OPENCLAW_USAGE_PROXY=http://127.0.0.1:18791
        # 后：solve() 在 system prompt 嵌 [[RUN:<id>]] 标记，代理按标记聚合上游
        # usage，跑完查询回填 last_usage。不设则行为不变（token 记 0）。
        self.usage_proxy = (
            os.environ.get("OPENCLAW_USAGE_PROXY")
            or llm_config.get("openclaw_usage_proxy")
            or ""
        ).rstrip("/")
        self._run_marker: str | None = None
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _record_usage_from_dict(self, usage: dict | None) -> None:
        """usage 用 OpenAI 风格键名（HTTP /chat/completions 响应体）。"""
        if not isinstance(usage, dict):
            return
        prompt = usage.get("prompt_tokens")
        completion = usage.get("completion_tokens")
        total = usage.get("total_tokens")
        if prompt is None and completion is None and total is None:
            return
        prompt = prompt or 0
        completion = completion or 0
        self.last_usage = {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": total if total is not None else prompt + completion,
        }

    def _build_tool_docs(self, tools_schema: list[dict]) -> str:
        """从 OpenAI tool schema 生成工具使用文档。"""
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
        return textwrap.dedent(f"""\
你是 OfficePrism 任务执行代理。你的唯一目标是使用下面列出的业务工具完成用户的任务。
{f'(run-id: [[RUN:{self._run_marker}]])' if self._run_marker else ''}

## 极其重要的规则（必须严格遵守）
1. 你 **必须且只能** 通过执行 curl 命令调用工具，**严禁** 用其他任何方式（如直接编造结果、浏览文件、猜测数据）。
2. 每次调用工具，**必须** 用 exec 工具执行以下格式的 curl 命令：

curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name": "<工具名>", "arguments": {{<参数JSON>}}}}'

3. curl 会返回 JSON，格式为 {{"result": "..."}}，这就是工具的真实返回值。
4. **绝对禁止** 编造或猜测工具返回值。每次都必须执行 curl 拿到真实结果。
5. 如果返回 {{"error": "max_steps_exceeded"}}，立即停止并汇报已完成的内容。
6. list/search/find 类工具只用于定位候选记录或引用 ID；如果已经定位到目标记录且存在对应的 get_* 明细工具，必须调用该 get_* 工具确认最终字段后再作答。
7. 完成所有必要的工具调用后，给出简洁的结果摘要。

## 调用示例
要查询员工详情，执行：
curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name": "get_employee_details", "arguments": {{"employee_ref": "EMP001"}}}}'

{f'## 业务政策{chr(10)}{self.domain_policy}{chr(10)}' if self.domain_policy else ''}
## 可用工具列表

{tool_docs}

## 用户任务
{task}
""")

    def solve(self, task: str, tools: list[dict], call_tool: Callable[[str, dict], str]) -> str:
        """启动 Tool Server，通过 HTTP 调用 OpenClaw 网关完成任务。"""
        self.last_usage = None
        self.last_cost = None
        # 每次 run 生成唯一标记，嵌进 system prompt；usage 代理按它聚合上游 usage。
        self._run_marker = uuid.uuid4().hex if self.usage_proxy else None

        # 启动本地 Tool Server，供 OpenClaw 回调
        tool_server = ToolServer(
            call_tool=call_tool,
            tools_schema=tools,
            advertised_host=self.tool_server_host,
        )
        tool_server.start()

        try:
            return self._run_openclaw_http(task, tools, tool_server.base_url)
        finally:
            tool_server.stop()
            self._fetch_proxy_usage()

    def _fetch_proxy_usage(self) -> None:
        """跑完后向 usage 代理查询本次 run 聚合的真实 token 用量。"""
        if not (self.usage_proxy and self._run_marker):
            return
        try:
            req = request.Request(f"{self.usage_proxy}/usage/{self._run_marker}")
            with request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            prompt = int(data.get("prompt_tokens") or 0)
            completion = int(data.get("completion_tokens") or 0)
            if prompt or completion:
                # 网关自身不回传 usage；代理统计优先（真实上游数字）。
                self.last_usage = {
                    "prompt_tokens": prompt,
                    "completion_tokens": completion,
                    "total_tokens": data.get("total_tokens") or (prompt + completion),
                }
                logger.info(
                    "OpenClaw usage via proxy | calls={} in={} out={}",
                    data.get("calls"), prompt, completion,
                )
        except Exception as e:  # 代理不可用不影响评测本身
            logger.debug(f"usage proxy query failed: {e}")

    def _run_openclaw_http(self, task: str, tools_schema: list[dict], server_url: str) -> str:
        """通过 HTTP 调用 OpenClaw 网关。"""
        system_prompt = self._build_system_prompt(task, tools_schema, server_url)

        try:
            data = self._post_chat_completion(system_prompt)
        except Exception as e:
            if "timed out" in str(e).lower():
                logger.warning("OpenClaw HTTP request timed out")
                return "__OPENCLAW_TIMEOUT__"
            logger.error(f"OpenClaw HTTP request failed: {e}")
            return ""

        try:
            self._record_usage_from_dict(data.get("usage"))
        except Exception as usage_exc:
            logger.debug(f"OpenClaw HTTP usage extraction failed: {usage_exc}")

        choices = data.get("choices") or []
        if not choices:
            logger.warning("OpenClaw returned empty choices")
            return ""

        content = ((choices[0].get("message") or {}).get("content")) or ""
        return content.strip()

    def _post_chat_completion(self, prompt: str) -> dict[str, Any]:
        """调用 OpenClaw 网关的 /v1/chat/completions 端点。"""
        payload = {
            "model": "openclaw/default",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": float(self.llm_config.get("temperature", 1.0)),
            "max_tokens": self.http_max_tokens,
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        # 使用固定的 agent ID（gateway 只认注册的 agent）
        agent_id = self.agent_id

        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "x-openclaw-agent-id": agent_id,
                "x-openclaw-model": self.provider_model,
                "x-openclaw-session-key": str(uuid.uuid4()),
            },
            method="POST",
        )

        logger.info(
            "Calling OpenClaw HTTP API | agent={} | model={} | timeout={}s",
            agent_id,
            self.provider_model,
            self.timeout,
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {detail[:2000]}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError("OpenClaw returned non-JSON response") from e
