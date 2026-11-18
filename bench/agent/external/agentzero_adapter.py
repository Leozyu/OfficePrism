"""Agent Zero 外部适配器。

通过本地 Tool Server + Agent Zero External API 完成 OfficePrism 评测：
1. 启动 HTTP tool server，将 OfficePrism 工具暴露为 REST 端点
2. 向 Agent Zero 发送任务 message，要求通过 code execution + curl 调用工具
3. Agent Zero 在其 agent loop 中自主规划、调用工具并生成最终答案
4. 所有工具调用经 call_tool 回调记录 trace 并修改 DB
"""

from __future__ import annotations

import textwrap
import time
import uuid
from typing import Any, Callable

import requests
from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class AgentZeroAdapter:
    """让 Agent Zero 以自身 agent loop 完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

        self.base_url = llm_config.get("agentzero_base_url", "http://localhost:50001").rstrip(
            "/"
        )
        self.api_key = llm_config.get("agentzero_api_key", "")
        self.lifetime_hours = int(llm_config.get("agentzero_lifetime_hours", 24))
        self.timeout = float(llm_config.get("timeout", 600))
        self.tool_server_bind_host = llm_config.get("agentzero_tool_server_bind_host", "0.0.0.0")
        self.tool_server_host = llm_config.get("agentzero_tool_server_host", "host.docker.internal")

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

    def _build_message(self, task: str, tools_schema: list[dict], server_url: str) -> str:
        tool_docs = self._build_tool_docs(tools_schema)
        policy_part = (
            f"## 业务政策\n{self.domain_policy}\n\n" if self.domain_policy else ""
        )
        container_url = server_url.replace("127.0.0.1", "host.docker.internal")

        return textwrap.dedent(
            f"""\
你是 OfficePrism 任务执行代理。你的唯一目标是使用下面列出的业务工具完成用户任务。

## 极其重要的规则（必须严格遵守）
1. 你必须且只能通过 code execution/terminal 执行 curl 命令调用业务工具。
2. 严禁直接编造工具结果，严禁通过文件搜索或猜测替代工具调用。
3. 每次工具调用都必须执行如下格式命令：

curl -sS --connect-timeout 5 --max-time 20 -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

4. 如果你运行在 Docker 容器中，请使用下面这个容器可达地址；若命令失败，原样重试一次，不要改成 localhost、127.0.0.1 或 172.17.0.1：

curl -sS --connect-timeout 5 --max-time 20 -X POST {container_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

5. 返回为 JSON，格式为 {{"result":"..."}}，这是唯一可信数据源。
6. 如果返回 {{"error":"max_steps_exceeded"}}，立即停止并总结当前进度。
7. 完成必要调用后输出明确结论。

{policy_part}## 可用工具列表
{tool_docs}

## 用户任务
{task}
"""
        )

    def solve(self, task: str, tools: list[dict], call_tool: Callable[[str, dict], str]) -> str:
        tool_server = ToolServer(
            call_tool=call_tool,
            tools_schema=tools,
            bind_host=self.tool_server_bind_host,
            advertised_host=self.tool_server_host,
        )
        tool_server.start()
        answer = ""
        try:
            prompt = self._build_message(task, tools, tool_server.base_url)
            answer = self._run_agentzero(prompt)
            if tool_server.call_count <= 0:
                logger.error("Agent Zero finished without any OfficePrism tool call")
                return ""
            return answer
        finally:
            tool_server.stop()

    def _run_agentzero(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-KEY"] = self.api_key

        payload: dict[str, Any] = {
            "message": prompt,
            "lifetime_hours": self.lifetime_hours,
        }

        try:
            response = requests.post(
                f"{self.base_url}/api_message",
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            logger.error(f"Agent Zero request failed: {e}")
            return ""

        if response.status_code in (404, 405):
            logger.warning(
                f"Agent Zero /api_message unavailable (HTTP {response.status_code}), "
                "fallback to web API flow"
            )
            return self._run_agentzero_web_api(prompt)

        if response.status_code >= 400:
            body_preview = response.text[:500]
            logger.error(
                f"Agent Zero returned HTTP {response.status_code}: {body_preview}"
            )
            return ""

        try:
            data = response.json()
        except ValueError:
            logger.error(f"Agent Zero returned non-JSON response: {response.text[:500]}")
            return ""

        result = data.get("response")
        if isinstance(result, str):
            return result.strip()

        logger.warning(f"Agent Zero returned unexpected payload keys: {list(data.keys())}")
        return ""

    def _run_agentzero_web_api(self, prompt: str) -> str:
        """兼容新版 Agent Zero：通过 csrf_token + message_async + poll 交互。"""
        session = requests.Session()
        browser_headers = {
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/",
        }

        csrf_token = self._fetch_csrf_token(session, browser_headers)
        if not csrf_token:
            return ""

        request_headers = {
            "Content-Type": "application/json",
            "X-CSRF-Token": csrf_token,
            **browser_headers,
        }
        context_id = self._create_chat_context(session, request_headers)

        message_id = str(uuid.uuid4())
        send_payload = {
            "text": prompt,
            "attachments": [],
            "context": context_id,
            "message_id": message_id,
        }
        try:
            send_resp = session.post(
                f"{self.base_url}/api/message_async",
                headers=request_headers,
                json=send_payload,
                timeout=min(self.timeout, 60),
            )
        except requests.RequestException as e:
            logger.error(f"Agent Zero message_async request failed: {e}")
            return ""

        if send_resp.status_code >= 400:
            logger.error(
                f"Agent Zero message_async returned HTTP {send_resp.status_code}: "
                f"{send_resp.text[:500]}"
            )
            return ""

        try:
            send_data = send_resp.json()
        except ValueError:
            logger.error(
                f"Agent Zero message_async returned non-JSON response: {send_resp.text[:500]}"
            )
            return ""

        context = send_data.get("context")
        if not isinstance(context, str) or not context:
            logger.error(f"Agent Zero message_async response missing context: {send_data}")
            return ""

        return self._poll_web_result(
            session=session,
            headers=request_headers,
            context=context,
        )

    def _create_chat_context(
        self, session: requests.Session, headers: dict[str, str]
    ) -> str | None:
        try:
            resp = session.post(
                f"{self.base_url}/api/chat_create",
                headers=headers,
                json={"current_context": None},
                timeout=min(self.timeout, 30),
            )
        except requests.RequestException as e:
            logger.warning(f"Agent Zero chat_create request failed, fallback to current context: {e}")
            return None

        if resp.status_code >= 400:
            logger.warning(
                f"Agent Zero chat_create returned HTTP {resp.status_code}, "
                "fallback to current context"
            )
            return None

        try:
            data = resp.json()
        except ValueError:
            logger.warning("Agent Zero chat_create returned non-JSON response, fallback context")
            return None

        ctxid = data.get("ctxid")
        if isinstance(ctxid, str) and ctxid:
            return ctxid
        return None

    def _fetch_csrf_token(
        self, session: requests.Session, headers: dict[str, str]
    ) -> str:
        try:
            csrf_resp = session.get(
                f"{self.base_url}/api/csrf_token",
                headers=headers,
                timeout=min(self.timeout, 30),
            )
        except requests.RequestException as e:
            logger.error(f"Agent Zero csrf_token request failed: {e}")
            return ""

        if csrf_resp.status_code >= 400:
            logger.error(
                f"Agent Zero csrf_token returned HTTP {csrf_resp.status_code}: "
                f"{csrf_resp.text[:500]}"
            )
            return ""

        try:
            csrf_data = csrf_resp.json()
        except ValueError:
            logger.error(
                f"Agent Zero csrf_token returned non-JSON response: {csrf_resp.text[:500]}"
            )
            return ""

        token = csrf_data.get("token")
        if csrf_data.get("ok") is not True or not isinstance(token, str) or not token:
            logger.error(f"Agent Zero csrf_token payload invalid: {csrf_data}")
            return ""
        return token

    def _poll_web_result(
        self,
        session: requests.Session,
        headers: dict[str, str],
        context: str,
    ) -> str:
        deadline = time.monotonic() + self.timeout
        start_time = time.monotonic()
        last_snapshot: dict[str, Any] = {}
        stagnant_polls = 0
        last_log_version: int | None = None
        last_progress: str = ""
        max_stagnant_polls = 30
        startup_grace_seconds = 8.0
        saw_active = False

        while time.monotonic() < deadline:
            poll_payload = {
                "log_from": 0,
                "notifications_from": 0,
                "context": context,
                "timezone": "UTC",
            }
            try:
                poll_resp = session.post(
                    f"{self.base_url}/api/poll",
                    headers=headers,
                    json=poll_payload,
                    timeout=min(self.timeout, 30),
                )
            except requests.RequestException as e:
                logger.error(f"Agent Zero poll request failed: {e}")
                return ""

            if poll_resp.status_code >= 400:
                logger.error(
                    f"Agent Zero poll returned HTTP {poll_resp.status_code}: "
                    f"{poll_resp.text[:500]}"
                )
                return ""

            try:
                snapshot = poll_resp.json()
            except ValueError:
                logger.error(
                    f"Agent Zero poll returned non-JSON response: {poll_resp.text[:500]}"
                )
                return ""

            if isinstance(snapshot, dict):
                last_snapshot = snapshot
                log_version = snapshot.get("log_version")
                progress = str(snapshot.get("log_progress", ""))
                is_active = bool(snapshot.get("log_progress_active"))
                if isinstance(log_version, int) and log_version == last_log_version:
                    stagnant_polls += 1
                else:
                    stagnant_polls = 0
                    last_log_version = log_version if isinstance(log_version, int) else None
                last_progress = progress
                if is_active:
                    saw_active = True

                if stagnant_polls >= max_stagnant_polls:
                    logger.error(
                        "Agent Zero web flow appears stalled "
                        f"(log_version={last_log_version}, progress={last_progress!r})"
                    )
                    break

                if not is_active:
                    # 某些版本在 message_async 后存在短暂 idle，再进入运行态。
                    # 避免首轮 poll 即误判结束。
                    if saw_active or (time.monotonic() - start_time) >= startup_grace_seconds:
                        break

            time.sleep(1.0)

        if not last_snapshot:
            logger.error("Agent Zero poll returned empty snapshot")
            return ""

        return self._extract_answer_from_snapshot(last_snapshot)

    @staticmethod
    def _extract_answer_from_snapshot(snapshot: dict[str, Any]) -> str:
        logs = snapshot.get("logs")
        if not isinstance(logs, list):
            return ""

        ignored_types = {"warning", "error", "user", "util", "tool"}
        fallback = ""
        for item in reversed(logs):
            if not isinstance(item, dict):
                continue
            content = AgentZeroAdapter._content_to_text(item.get("content")).strip()
            if not content:
                continue
            if not fallback:
                fallback = content
            item_type = str(item.get("type", "")).lower()
            if item_type not in ignored_types:
                return content
        return fallback

    @staticmethod
    def _content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, dict):
            for key in ("text", "message", "content"):
                value = content.get(key)
                if isinstance(value, str):
                    return value
        return ""
