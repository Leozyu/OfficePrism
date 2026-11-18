"""XAgent 外部适配器。

通过本地 Tool Server + XAgent REST/WebSocket API 完成 OfficePrism 评测：
1. 启动 HTTP tool server，将 OfficePrism 工具暴露为 REST 端点
2. 调用 XAgent API 登录并创建任务
3. 通过 WebSocket 触发执行并监听流式事件
4. 所有工具调用经 call_tool 回调记录 trace 并修改 DB
"""

from __future__ import annotations

import json
import textwrap
import time
from typing import Any, Callable
from urllib.parse import quote

import requests
from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class XAgentAdapter:
    """让 XAgent 以自身 agent loop 完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

        self.api_url = llm_config.get("xagent_api_url", "http://localhost:8000").rstrip("/")
        self.username = llm_config.get("xagent_username", "admin")
        self.password = llm_config.get("xagent_password", "")
        self.agent_id = llm_config.get("xagent_agent_id")
        self.timeout = float(llm_config.get("timeout", 600))

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
        docker_url = server_url.replace("127.0.0.1", "host.docker.internal")

        return textwrap.dedent(
            f"""\
你是 OfficePrism 任务执行代理。你的唯一目标是使用下面列出的业务工具完成用户任务。

## 极其重要的规则（必须严格遵守）
1. 你必须且只能通过 Python Executor/terminal 执行 curl 命令调用业务工具。
2. 严禁直接编造工具结果，严禁通过文件搜索或猜测替代工具调用。
3. 每次工具调用都必须执行如下格式命令：

curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

4. 如果运行在 Docker/隔离环境里，且 `127.0.0.1` 无法连接，请改用：

curl -s -X POST {docker_url}/call_tool \\
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
        try:
            from websocket import create_connection
            from websocket import WebSocketException, WebSocketTimeoutException
        except ImportError as e:
            raise ImportError(
                "XAgent 依赖未安装。请执行: pip install websocket-client"
            ) from e

        tool_server = ToolServer(call_tool=call_tool, tools_schema=tools)
        tool_server.start()
        try:
            prompt = self._build_message(task, tools, tool_server.base_url)
            with requests.Session() as session:
                token = self._login(session)
                if not token:
                    return ""

                task_id = self._create_task(session, token, task)
                if task_id is None:
                    return ""

                return self._execute_and_wait(
                    session=session,
                    token=token,
                    task_id=task_id,
                    prompt=prompt,
                    create_connection=create_connection,
                    ws_exception_cls=WebSocketException,
                    ws_timeout_cls=WebSocketTimeoutException,
                )
        except Exception as e:
            logger.error(f"XAgent execution failed: {e}")
            return ""
        finally:
            tool_server.stop()

    def _login(self, session: requests.Session) -> str:
        if not self.password:
            logger.error("XAgent login password is empty. Please set xagent_password.")
            return ""

        payload = {"username": self.username, "password": self.password}
        try:
            resp = session.post(
                f"{self.api_url}/api/auth/login",
                json=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            logger.error(f"XAgent login request failed: {e}")
            return ""

        if resp.status_code >= 400:
            logger.error(f"XAgent login failed [{resp.status_code}]: {resp.text[:500]}")
            return ""

        try:
            data = resp.json()
        except ValueError:
            logger.error(f"XAgent login returned non-JSON: {resp.text[:500]}")
            return ""

        token = self._extract_token(data) or self._extract_token(dict(resp.cookies))
        if not token:
            logger.error(f"XAgent login succeeded but token missing. Keys: {list(data.keys())}")
            return ""
        return token

    def _create_task(self, session: requests.Session, token: str, task: str) -> int | None:
        payload: dict[str, Any] = {
            "title": self._build_task_title(task),
            "description": "OfficePrism external evaluation task",
        }

        if self.agent_id is not None:
            try:
                payload["agent_id"] = int(self.agent_id)
            except (TypeError, ValueError):
                logger.warning(f"Invalid xagent_agent_id: {self.agent_id!r}. Ignore this field.")

        try:
            resp = session.post(
                f"{self.api_url}/api/chat/task/create",
                json=payload,
                headers=self._auth_headers(token),
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            logger.error(f"XAgent create_task request failed: {e}")
            return None

        if resp.status_code >= 400:
            logger.error(f"XAgent create_task failed [{resp.status_code}]: {resp.text[:500]}")
            return None

        try:
            data = resp.json()
        except ValueError:
            logger.error(f"XAgent create_task returned non-JSON: {resp.text[:500]}")
            return None

        task_id = data.get("task_id")
        if task_id is None and isinstance(data.get("data"), dict):
            task_id = data["data"].get("task_id")
        if not isinstance(task_id, int):
            logger.error(f"XAgent create_task payload missing task_id: {data}")
            return None
        return task_id

    def _execute_and_wait(
        self,
        session: requests.Session,
        token: str,
        task_id: int,
        prompt: str,
        create_connection: Callable[..., Any],
        ws_exception_cls: type[Exception],
        ws_timeout_cls: type[Exception],
    ) -> str:
        ws = None
        last_answer = ""
        last_error = ""
        deadline = time.monotonic() + self.timeout

        try:
            ws = create_connection(self._build_ws_url(task_id, token), timeout=min(self.timeout, 30))
            ws.settimeout(10)
            ws.send(json.dumps({"type": "execute_task", "query": prompt}, ensure_ascii=False))

            while time.monotonic() < deadline:
                try:
                    raw = ws.recv()
                except ws_timeout_cls:
                    continue
                except ws_exception_cls as e:
                    logger.error(f"XAgent websocket error: {e}")
                    break

                if not isinstance(raw, str):
                    continue

                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                candidate = self._extract_chat_text(msg)
                if candidate:
                    last_answer = candidate

                if msg.get("type") == "error":
                    last_error = str(msg.get("message", "unknown websocket error"))
                    logger.error(f"XAgent task websocket returned error: {last_error}")
                    break

                event_type = msg.get("event_type")
                if event_type == "task_error":
                    data = msg.get("data")
                    if isinstance(data, dict):
                        last_error = str(data.get("error", "task_error"))
                    else:
                        last_error = "task_error"

                if self._is_task_finished(msg):
                    break
        finally:
            if ws is not None:
                try:
                    ws.close()
                except Exception:
                    pass

        if last_answer.strip():
            return last_answer.strip()

        fallback = self._fetch_task_result(session, token, task_id)
        if fallback:
            return fallback

        if time.monotonic() >= deadline:
            logger.error(f"XAgent websocket timeout after {self.timeout}s (task_id={task_id})")
        elif last_error:
            logger.error(f"XAgent task failed: {last_error}")
        else:
            logger.warning("XAgent task completed without assistant answer.")
        return ""

    def _fetch_task_result(self, session: requests.Session, token: str, task_id: int) -> str:
        try:
            resp = session.get(
                f"{self.api_url}/api/chat/task/{task_id}",
                headers=self._auth_headers(token),
                timeout=self.timeout,
            )
        except requests.RequestException:
            return ""

        if resp.status_code >= 400:
            return ""

        try:
            data = resp.json()
        except ValueError:
            return ""
        return self._extract_text_from_payload(data)

    def _extract_text_from_payload(self, data: Any) -> str:
        if isinstance(data, str):
            return data.strip()

        if isinstance(data, list):
            for item in reversed(data):
                text = self._extract_text_from_payload(item)
                if text:
                    return text
            return ""

        if not isinstance(data, dict):
            return ""

        messages = data.get("messages")
        if isinstance(messages, list):
            for message in reversed(messages):
                if not isinstance(message, dict):
                    continue
                role = message.get("role")
                if role not in {"assistant", "ai"}:
                    continue
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()

        for key in ("final_answer", "answer", "result", "output", "message", "content"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        nested_data = data.get("data")
        if nested_data is not None:
            nested_text = self._extract_text_from_payload(nested_data)
            if nested_text:
                return nested_text
        return ""

    def _extract_chat_text(self, msg: dict[str, Any]) -> str:
        msg_type = msg.get("type")
        if msg_type == "chat":
            message = msg.get("message")
            if isinstance(message, str):
                return message.strip()

        data = msg.get("data")
        if isinstance(data, dict):
            for key in ("response", "message", "output", "result", "final_answer"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
        return ""

    def _is_task_finished(self, msg: dict[str, Any]) -> bool:
        event_type = msg.get("event_type")
        if event_type in {"task_end_dag", "task_end_react", "task_end_general"}:
            return True
        if event_type == "task_error":
            return True

        if msg.get("type") == "status":
            status = str(msg.get("status", "")).lower()
            if status in {"completed", "failed", "cancelled"}:
                return True
        return False

    def _build_task_title(self, task: str) -> str:
        first_line = task.strip().splitlines()[0] if task.strip() else "OfficePrism Task"
        return first_line[:120]

    def _build_ws_url(self, task_id: int, token: str) -> str:
        if self.api_url.startswith("https://"):
            ws_base = "wss://" + self.api_url[len("https://") :]
        elif self.api_url.startswith("http://"):
            ws_base = "ws://" + self.api_url[len("http://") :]
        else:
            ws_base = "ws://" + self.api_url
        return f"{ws_base}/ws/chat/{task_id}?token={quote(token, safe='')}"

    def _auth_headers(self, token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    def _extract_token(self, payload: Any) -> str:
        if isinstance(payload, str):
            return payload.strip()
        if not isinstance(payload, dict):
            return ""

        token_keys = (
            "access_token",
            "token",
            "jwt",
            "auth_token",
            "id_token",
        )
        for key in token_keys:
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        nested = payload.get("data")
        if nested is not None:
            nested_token = self._extract_token(nested)
            if nested_token:
                return nested_token
        return ""
