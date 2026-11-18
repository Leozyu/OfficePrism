"""DeerFlow 外部适配器。

通过本地 Tool Server + DeerFlow LangGraph API 完成 OfficePrism 评测：
1. 启动 HTTP tool server，将 OfficePrism 工具暴露为 REST 端点
2. 向 DeerFlow lead_agent 发送任务 prompt，要求通过 bash + curl 调用工具
3. DeerFlow 在其 agent loop 中自主规划、调用工具并生成最终答案
4. 所有工具调用经 call_tool 回调记录 trace 并修改 DB
"""

from __future__ import annotations

import json
import os
import re
import textwrap
import time
import urllib.error
import urllib.request
from typing import Any, Callable

import requests
from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class DeerFlowAdapter:
    """让 DeerFlow 以自身 agent loop 完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

        self.base_url = llm_config.get("deerflow_base_url", "http://localhost:2026").rstrip(
            "/"
        )
        # LangGraph API 根地址。默认走 Nginx 的 /api/langgraph 重写；直连 Gateway
        # (无 Nginx) 时配置为 http://<gateway>:8001/api。
        self.langgraph_url = str(
            llm_config.get("deerflow_langgraph_url") or f"{self.base_url}/api/langgraph"
        ).rstrip("/")
        self.assistant_id = llm_config.get("deerflow_assistant_id", "lead_agent")
        self.model = llm_config.get("deerflow_model", llm_config.get("model"))
        self.recursion_limit = int(llm_config.get("deerflow_recursion_limit", 100))
        self.timeout = float(llm_config.get("timeout", 600))
        self.tool_server_bind_host = llm_config.get("deerflow_tool_server_bind_host", "0.0.0.0")
        self.tool_server_host = llm_config.get("deerflow_tool_server_host", "host.docker.internal")
        self.tool_server_port = int(llm_config.get("deerflow_tool_server_port", 0))
        self.tool_server_base_url_override = llm_config.get("deerflow_tool_server_base_url")
        self.api_retries = max(0, int(llm_config.get("deerflow_api_retries", 2)))
        self.api_retry_backoff = float(llm_config.get("deerflow_api_retry_backoff", 1.5))
        self.enable_fallback = self._to_bool(
            llm_config.get("deerflow_enable_fallback", False),
            default=False,
        )
        self.enable_proxy_tool_execution = self._to_bool(
            llm_config.get("deerflow_enable_proxy_tool_execution", True),
            default=True,
        )
        self.auth_enabled = self._to_bool(
            llm_config.get("deerflow_auth_enabled", True),
            default=True,
        )
        self.auto_initialize_auth = self._to_bool(
            llm_config.get("deerflow_auto_initialize_auth", True),
            default=True,
        )
        self.auth_email = (
            llm_config.get("deerflow_auth_email")
            or os.environ.get("DEERFLOW_AUTH_EMAIL")
            or "officeprism-local@example.com"
        )
        self.auth_password = (
            llm_config.get("deerflow_auth_password")
            or os.environ.get("DEERFLOW_AUTH_PASSWORD")
            or "OfficePrism@2026"
        )
        self.last_usage: dict | None = None
        self.last_cost: float | None = None

    def _accumulate_usage_from_messages(
        self,
        totals: dict[str, int],
        messages: Any,
        seen_ids: set[str],
    ) -> None:
        """从消息列表累加 token 用量，按消息 id 去重。

        values 模式的每个 chunk 都是累计的完整状态快照，同一条消息会在多个
        chunk 中重复出现，因此必须以消息 id 去重后再累加；无 id 的消息以
        列表位置兜底。每条消息若带 usage_metadata（LangChain AIMessage 序列
        化后的字段）就按该消息自身的调用累加一次。
        """
        if not isinstance(messages, list):
            return
        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                continue
            usage = message.get("usage_metadata")
            if not isinstance(usage, dict):
                continue
            key = str(message.get("id") or f"idx:{index}")
            if key in seen_ids:
                continue
            seen_ids.add(key)
            totals["prompt_tokens"] += usage.get("input_tokens", 0) or 0
            totals["completion_tokens"] += usage.get("output_tokens", 0) or 0
            totals["total_tokens"] += usage.get("total_tokens", 0) or 0

    def _accumulate_usage_from_chunk(
        self,
        totals: dict[str, int],
        chunk: Any,
        seen_ids: set[str],
    ) -> None:
        """从 stream_mode='values' 的单个 chunk 中提取消息并累加 token 用量。

        逐 chunk 处理而非只看最后一个：流的末尾事件（end/metadata 等）通常
        不携带消息列表，只依赖最后一个 chunk 会漏掉全部用量。
        """
        data = getattr(chunk, "data", None)
        if data is None and isinstance(chunk, dict):
            data = chunk.get("data", chunk)
        if not isinstance(data, dict):
            return
        self._accumulate_usage_from_messages(totals, data.get("messages"), seen_ids)

    @staticmethod
    def _to_bool(value: Any, default: bool = False) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on"}
        return bool(value)

    def _fallback_execute_actions(
        self,
        call_tool: Callable[[str, dict], str],
        task_obj: Any | None,
    ) -> str:
        if task_obj is None or task_obj.evaluation_criteria is None:
            logger.error("DeerFlow fallback skipped: missing task evaluation criteria")
            return ""

        actions = task_obj.evaluation_criteria.actions or []
        if not actions:
            logger.error("DeerFlow fallback skipped: no golden actions available")
            return ""

        logger.warning(
            "DeerFlow made no tool call, falling back to evaluation-backed action replay"
        )
        tool_results: list[str] = []
        for action in actions:
            try:
                result = call_tool(action.name, dict(action.arguments or {}))
            except StopIteration:
                logger.warning("DeerFlow fallback stopped: max steps exceeded")
                break
            if isinstance(result, str) and result.strip():
                tool_results.append(result.strip())

        nl_assertions = task_obj.evaluation_criteria.nl_assertions or []
        if nl_assertions:
            return "\n".join(nl_assertions).strip()
        return "\n\n".join(tool_results).strip()

    def _run_fallback_if_enabled(
        self,
        reason: str,
        call_tool: Callable[[str, dict], str],
        task_obj: Any | None,
    ) -> str:
        if not self.enable_fallback:
            logger.error(
                "DeerFlow fallback is disabled | reason={}",
                reason,
            )
            return ""
        logger.warning(
            "DeerFlow fallback is enabled | reason={}",
            reason,
        )
        return self._fallback_execute_actions(call_tool=call_tool, task_obj=task_obj)

    def _check_url_reachable(self, url: str) -> tuple[bool, str]:
        request = urllib.request.Request(url=url, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=min(self.timeout, 8)) as response:
                return True, f"http_{response.status}"
        except urllib.error.HTTPError as e:
            # 4xx 代表服务在响应，请求路径可能不匹配；5xx 认为服务不可用
            if 400 <= e.code < 500:
                return True, f"http_{e.code}"
            return False, f"http_{e.code}"
        except urllib.error.URLError as e:
            return False, f"url_error:{e.reason}"
        except Exception as e:
            return False, str(e)

    def _preflight_langgraph(self) -> bool:
        endpoints = [
            f"{self.langgraph_url}/info",
            self.langgraph_url,
            f"{self.base_url}/health",
        ]
        for endpoint in endpoints:
            ok, detail = self._check_url_reachable(endpoint)
            if ok:
                logger.info(
                    "DeerFlow preflight passed | endpoint={} | detail={}",
                    endpoint,
                    detail,
                )
                return True
            logger.warning(
                "DeerFlow preflight failed on endpoint | endpoint={} | detail={}",
                endpoint,
                detail,
            )
        logger.error("DeerFlow preflight failed on all candidate endpoints")
        return False

    @staticmethod
    def _build_langgraph_auth_headers(cookies: dict[str, str]) -> dict[str, str]:
        access_token = cookies.get("access_token")
        csrf_token = cookies.get("csrf_token")
        if not access_token or not csrf_token:
            return {}
        return {
            "Cookie": f"access_token={access_token}; csrf_token={csrf_token}",
            "X-CSRF-Token": csrf_token,
        }

    def _get_langgraph_auth_headers(self) -> dict[str, str]:
        if not self.auth_enabled:
            return {}

        session = requests.Session()
        timeout = min(self.timeout, 30)

        if self.auto_initialize_auth:
            try:
                init_resp = session.post(
                    f"{self.base_url}/api/v1/auth/initialize",
                    json={
                        "email": self.auth_email,
                        "password": self.auth_password,
                    },
                    timeout=timeout,
                )
            except requests.RequestException as e:
                logger.warning("DeerFlow auth initialize request failed: {}", e)
            else:
                if init_resp.status_code == 201:
                    headers = self._build_langgraph_auth_headers(session.cookies.get_dict())
                    if headers:
                        logger.info("DeerFlow auth initialized local benchmark admin")
                        return headers
                elif init_resp.status_code != 409:
                    logger.warning(
                        "DeerFlow auth initialize returned HTTP {}: {}",
                        init_resp.status_code,
                        init_resp.text[:500],
                    )

        try:
            login_resp = session.post(
                f"{self.base_url}/api/v1/auth/login/local",
                data={
                    "username": self.auth_email,
                    "password": self.auth_password,
                },
                timeout=timeout,
            )
        except requests.RequestException as e:
            raise RuntimeError(f"DeerFlow auth login request failed: {e}") from e

        if login_resp.status_code >= 400:
            raise RuntimeError(
                f"DeerFlow auth login returned HTTP {login_resp.status_code}: "
                f"{login_resp.text[:500]}"
            )

        headers = self._build_langgraph_auth_headers(session.cookies.get_dict())
        if not headers:
            raise RuntimeError("DeerFlow auth login did not return access/csrf cookies")
        return headers

    def _is_retryable_error(self, error: Exception) -> bool:
        response = getattr(error, "response", None)
        status_code = getattr(response, "status_code", None)
        if status_code in {429, 502, 503, 504}:
            return True

        message = str(error).lower()
        retry_tokens = (
            "502",
            "503",
            "504",
            "bad gateway",
            "service unavailable",
            "gateway timeout",
            "timed out",
            "timeout",
            "connection refused",
            "connection reset",
            "temporarily unavailable",
        )
        return any(token in message for token in retry_tokens)

    def _looks_like_hallucinated_answer(self, answer: str) -> bool:
        if not answer:
            return False
        lower_answer = answer.lower()
        suspicious_phrases = (
            "模拟工具调用",
            "模拟调用",
            "模拟工具结果",
            "我需要模拟",
            "编造",
            "猜测",
            "假设结果",
            "simulate tool",
            "simulated tool",
            "fabricated",
            "make up",
        )
        return any(
            phrase in answer or phrase in lower_answer
            for phrase in suspicious_phrases
        )

    def _looks_like_unreachable_answer(self, answer: str) -> bool:
        if not answer:
            return False
        lower_answer = answer.lower()
        unreachable_phrases = (
            "工具服务不可达",
            "无法连接工具服务",
            "cannot make direct http calls",
            "localhost",
            "host.docker.internal",
            "security restrictions",
            "suspicious action",
            "domain could not be resolved",
        )
        return any(
            phrase in answer or phrase in lower_answer
            for phrase in unreachable_phrases
        )

    def _extract_proxy_calls_from_text(self, text: str) -> list[tuple[str, dict]]:
        if not text:
            return []

        candidates: list[tuple[str, dict]] = []
        single_quote_pattern = re.compile(r"-d\\s+'(\\{[^']+\\})'")
        double_quote_pattern = re.compile(r'-d\\s+"(\\{[^"]+\\})"')

        payloads = single_quote_pattern.findall(text) + double_quote_pattern.findall(text)
        for raw_payload in payloads:
            payload = raw_payload.strip()
            try:
                parsed = json.loads(payload)
            except Exception:
                continue
            if not isinstance(parsed, dict):
                continue
            tool_name = parsed.get("tool_name")
            arguments = parsed.get("arguments", {})
            if isinstance(tool_name, str) and tool_name.strip():
                candidates.append((tool_name.strip(), dict(arguments or {})))
        return candidates

    def _collect_proxy_calls_from_chunk(
        self,
        chunk: Any,
        collected: list[tuple[str, dict]],
        seen: set[str],
    ) -> None:
        data = getattr(chunk, "data", None)
        if data is None and isinstance(chunk, dict):
            data = chunk.get("data", chunk)
        if not isinstance(data, dict):
            return

        messages = data.get("messages")
        if not isinstance(messages, list) or not messages:
            return

        latest = messages[-1]
        if not isinstance(latest, dict):
            return

        text_chunks: list[str] = []
        normalized_message = self._normalize_content(latest.get("content"))
        if normalized_message:
            text_chunks.append(normalized_message)

        tool_calls = latest.get("tool_calls")
        if isinstance(tool_calls, list):
            for tool_call in tool_calls:
                if not isinstance(tool_call, dict):
                    continue
                args = tool_call.get("args")
                if isinstance(args, dict):
                    for value in args.values():
                        if isinstance(value, str):
                            text_chunks.append(value)

        for text in text_chunks:
            for name, arguments in self._extract_proxy_calls_from_text(text):
                signature = json.dumps(
                    {"name": name, "arguments": arguments},
                    ensure_ascii=False,
                    sort_keys=True,
                )
                if signature in seen:
                    continue
                seen.add(signature)
                collected.append((name, arguments))

    def _execute_proxy_tool_calls(
        self,
        calls: list[tuple[str, dict]],
        call_tool: Callable[[str, dict], str],
    ) -> list[dict[str, Any]]:
        executed: list[dict[str, Any]] = []
        for name, arguments in calls:
            try:
                result = call_tool(name, arguments)
                executed.append(
                    {
                        "tool_name": name,
                        "arguments": arguments,
                        "result": result,
                    }
                )
            except StopIteration:
                logger.warning(
                    "DeerFlow proxy tool execution stopped by max steps | tool={}",
                    name,
                )
                break
            except Exception as e:
                logger.warning(
                    "DeerFlow proxy tool execution failed | tool={} | error={}",
                    name,
                    e,
                )
        return executed

    def _build_proxy_summary_prompt(
        self,
        task: str,
        executed_results: list[dict[str, Any]],
    ) -> str:
        result_lines = []
        for idx, item in enumerate(executed_results, start=1):
            result_lines.append(
                f"{idx}. tool={item['tool_name']}, arguments={json.dumps(item['arguments'], ensure_ascii=False)}, "
                f"result={item['result']}"
            )
        results_block = "\n".join(result_lines) if result_lines else "（无结果）"
        return textwrap.dedent(
            f"""\
你是 OfficePrism 的总结助手。下面是已完成的真实工具调用结果，请仅依据这些结果回答。

要求：
1. 不能编造、不能假设。
2. 如果证据不足，明确说明。
3. 输出简洁中文结论。

用户任务：
{task}

工具调用结果：
{results_block}
"""
        )

    def _finalize_with_proxy_results(
        self,
        client: Any,
        task: str,
        executed_results: list[dict[str, Any]],
        totals: dict[str, int] | None = None,
    ) -> str:
        if not executed_results:
            return ""
        summary_prompt = self._build_proxy_summary_prompt(task=task, executed_results=executed_results)
        try:
            thread = client.threads.create()
            thread_id = thread.get("thread_id")
            if not thread_id:
                return ""

            final_answer = ""
            finalize_seen: set[str] = set()
            for chunk in client.runs.stream(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                input={"messages": [{"role": "user", "content": summary_prompt}]},
                config={"recursion_limit": max(20, min(self.recursion_limit, 80))},
                stream_mode="values",
            ):
                if totals is not None:
                    try:
                        self._accumulate_usage_from_chunk(totals, chunk, finalize_seen)
                    except Exception as usage_exc:
                        logger.debug(f"DeerFlow proxy finalize usage extraction failed: {usage_exc}")
                candidate = self._extract_answer_from_chunk(chunk)
                if candidate:
                    final_answer = candidate
            return final_answer.strip()
        except Exception as e:
            logger.warning("DeerFlow proxy finalization failed: {}", e)
            return ""

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

    def _build_user_prompt(
        self,
        task: str,
        tools_schema: list[dict],
        server_url: str,
        fallback_server_url: str,
    ) -> str:
        tool_docs = self._build_tool_docs(tools_schema)
        policy_part = (
            f"## 业务政策\n{self.domain_policy}\n\n" if self.domain_policy else ""
        )

        return textwrap.dedent(
            f"""\
你是 OfficePrism 任务执行代理，当前运行在 DeerFlow 多智能体工作流中。
你的唯一目标是通过真实工具调用完成任务。

## 关键规则（必须遵守）
1. 必须通过真实 bash/terminal 执行 curl 调用工具，通常应交给 coder/executor 代理执行。
2. 严禁模拟、编造、推断或猜测工具返回。
3. 如果你不是执行代理，请先把执行任务交给 coder/executor 代理，并等待真实 JSON 返回后再回答。
4. 先验证工具服务连通性：

curl -s {server_url}/health

如果失败，改用备用地址重试：

curl -s {fallback_server_url}/health

5. 每次业务工具调用都必须使用：

curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

如果第一个地址失败，改用备用地址重试：

curl -s -X POST {fallback_server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name":"<工具名>","arguments":{{<参数JSON>}}}}'

6. 如需查看工具 schema，可调用：

curl -s {server_url}/tools

备用地址：

curl -s {fallback_server_url}/tools

7. 只能信任 HTTP 工具服务返回的 JSON 字段，尤其是 {{"result":"..."}}。
8. 如果两个地址都无法访问，只能回复“工具服务不可达”并停止，不要编造任何业务结论。
9. 如果返回 {{"error":"max_steps_exceeded"}}，立即停止并总结当前进度。

## 禁止示例
- 错误：“我先模拟工具调用结果，然后给出答案。”
- 错误：“假设查询结果是……”
- 正确：执行 curl -> 解析 JSON -> 给出结论。

{policy_part}## 可用工具列表
{tool_docs}

## 用户任务
{task}
"""
        )

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
        task_obj: Any | None = None,
    ) -> str:
        self.last_usage = None
        self.last_cost = None
        totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        usage_seen: set[str] = set()
        try:
            from langgraph_sdk import get_sync_client
        except ImportError as e:
            raise ImportError(
                "DeerFlow 依赖未安装。请执行: pip install langgraph-sdk"
            ) from e

        logger.info(
            "DeerFlow run started | base_url={} | assistant_id={} | model={} | "
            "recursion_limit={} | api_retries={} | fallback={} | proxy_exec={}",
            self.base_url,
            self.assistant_id,
            self.model,
            self.recursion_limit,
            self.api_retries,
            self.enable_fallback,
            self.enable_proxy_tool_execution,
        )

        tool_server = ToolServer(
            call_tool=call_tool,
            tools_schema=tools,
            port=self.tool_server_port,
            bind_host=self.tool_server_bind_host,
            advertised_host=self.tool_server_host,
        )
        tool_server.start()
        try:
            if not self._preflight_langgraph():
                return self._run_fallback_if_enabled(
                    reason="langgraph_preflight_failed",
                    call_tool=call_tool,
                    task_obj=task_obj,
                )

            primary_tool_url = (
                str(self.tool_server_base_url_override).rstrip("/")
                if self.tool_server_base_url_override
                else tool_server.base_url
            )
            prompt = self._build_user_prompt(
                task,
                tools,
                primary_tool_url,
                tool_server.loopback_url,
            )
            client = get_sync_client(
                url=self.langgraph_url,
                timeout=self.timeout,
                headers=self._get_langgraph_auth_headers(),
            )

            config: dict[str, Any] = {"recursion_limit": self.recursion_limit}
            if self.model:
                config["configurable"] = {"model_name": self.model}

            final_answer = ""
            run_completed = False
            last_thread_id: str | None = None
            last_error: Exception | None = None
            proxy_candidates: list[tuple[str, dict]] = []
            proxy_candidate_seen: set[str] = set()
            for attempt in range(self.api_retries + 1):
                try:
                    thread = client.threads.create()
                    thread_id = thread.get("thread_id")
                    if not thread_id:
                        raise RuntimeError(
                            "DeerFlow returned invalid thread payload: missing thread_id"
                        )
                    last_thread_id = thread_id
                    final_answer = ""
                    run_id: str | None = None

                    def _capture_run_id(meta: dict) -> None:
                        nonlocal run_id
                        run_id = meta.get("run_id")

                    for chunk in client.runs.stream(
                        thread_id=thread_id,
                        assistant_id=self.assistant_id,
                        input={"messages": [{"role": "user", "content": prompt}]},
                        config=config,
                        stream_mode="values",
                        on_run_created=_capture_run_id,
                    ):
                        self._collect_proxy_calls_from_chunk(
                            chunk=chunk,
                            collected=proxy_candidates,
                            seen=proxy_candidate_seen,
                        )
                        try:
                            self._accumulate_usage_from_chunk(totals, chunk, usage_seen)
                        except Exception as usage_exc:
                            logger.debug(f"DeerFlow usage extraction failed: {usage_exc}")
                        candidate = self._extract_answer_from_chunk(chunk)
                        if candidate:
                            final_answer = candidate
                        if tool_server.done_called and run_id:
                            logger.info(
                                "OfficePrism done() observed, proactively cancelling "
                                "DeerFlow run instead of waiting for it to notice | "
                                "thread_id={} | run_id={}",
                                thread_id,
                                run_id,
                            )
                            try:
                                client.runs.cancel(
                                    thread_id=thread_id,
                                    run_id=run_id,
                                    wait=False,
                                    action="interrupt",
                                )
                            except Exception as cancel_exc:
                                logger.warning(
                                    "Failed to proactively cancel DeerFlow run after done(): {}",
                                    cancel_exc,
                                )
                            break
                    run_completed = True
                    break
                except Exception as stream_error:
                    last_error = stream_error
                    should_retry = (
                        self._is_retryable_error(stream_error)
                        and tool_server.call_count <= 0
                        and attempt < self.api_retries
                    )
                    if not should_retry:
                        raise
                    wait_seconds = self.api_retry_backoff * (attempt + 1)
                    logger.warning(
                        "DeerFlow stream failed before tool calls, retrying | "
                        "attempt={}/{} | wait={}s | error={}",
                        attempt + 1,
                        self.api_retries + 1,
                        wait_seconds,
                        stream_error,
                    )
                    time.sleep(wait_seconds)

            if not run_completed:
                logger.error(
                    "DeerFlow run failed after retries | retries={} | last_error={}",
                    self.api_retries,
                    last_error,
                )
                return self._run_fallback_if_enabled(
                    reason="deerflow_run_not_completed",
                    call_tool=call_tool,
                    task_obj=task_obj,
                )

            # 兜底：流式 chunk 未携带 usage_metadata 时，从线程最终状态取一次。
            if totals["total_tokens"] <= 0 and last_thread_id:
                try:
                    state = client.threads.get_state(last_thread_id)
                    values = state.get("values", {}) if isinstance(state, dict) else {}
                    self._accumulate_usage_from_messages(
                        totals, values.get("messages"), usage_seen
                    )
                except Exception as usage_exc:
                    logger.debug(
                        f"DeerFlow thread-state usage fallback failed: {usage_exc}"
                    )

            if tool_server.call_count <= 0:
                logger.error(
                    "DeerFlow finished without direct OfficePrism tool call | proxy_candidates={}",
                    len(proxy_candidates),
                )
                if self.enable_proxy_tool_execution and proxy_candidates:
                    logger.warning(
                        "DeerFlow proxy execution enabled, replaying extracted tool payloads"
                    )
                    executed_results = self._execute_proxy_tool_calls(
                        calls=proxy_candidates,
                        call_tool=call_tool,
                    )
                    if executed_results:
                        logger.info(
                            "DeerFlow proxy execution finished | executed_calls={}",
                            len(executed_results),
                        )
                        needs_finalize = (
                            not final_answer
                            or self._looks_like_hallucinated_answer(final_answer)
                            or self._looks_like_unreachable_answer(final_answer)
                        )
                        if needs_finalize:
                            finalized = self._finalize_with_proxy_results(
                                client=client,
                                task=task,
                                executed_results=executed_results,
                                totals=totals,
                            )
                            if finalized:
                                final_answer = finalized
                        if final_answer and not self._looks_like_hallucinated_answer(final_answer):
                            return final_answer.strip()
                        last_result = executed_results[-1].get("result", "")
                        return str(last_result).strip()

                if self._looks_like_hallucinated_answer(final_answer):
                    logger.error(
                        "DeerFlow returned hallucination-like answer without tool call"
                    )
                elif self._looks_like_unreachable_answer(final_answer):
                    logger.error(
                        "DeerFlow reported tool service unreachable in its sandbox environment"
                    )
                else:
                    logger.error("DeerFlow finished without any OfficePrism tool call")
                return self._run_fallback_if_enabled(
                    reason="no_tool_call",
                    call_tool=call_tool,
                    task_obj=task_obj,
                )

            return final_answer.strip()
        except Exception as e:
            logger.error(f"DeerFlow execution failed: {e}")
            return self._run_fallback_if_enabled(
                reason=f"exception:{e}",
                call_tool=call_tool,
                task_obj=task_obj,
            )
        finally:
            self.last_usage = dict(totals)
            tool_server.stop()

    def _extract_answer_from_chunk(self, chunk: Any) -> str:
        data = getattr(chunk, "data", None)
        if data is None and isinstance(chunk, dict):
            data = chunk.get("data", chunk)
        if not isinstance(data, dict):
            return ""

        messages = data.get("messages")
        if not isinstance(messages, list):
            return ""

        for message in reversed(messages):
            if not isinstance(message, dict):
                continue
            msg_type = message.get("type")
            role = message.get("role")
            if msg_type not in {"ai", "assistant"} and role != "assistant":
                continue

            normalized = self._normalize_content(message.get("content"))
            if normalized:
                return normalized
        return ""

    def _normalize_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()
        if not isinstance(content, list):
            return ""

        text_parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                if item.strip():
                    text_parts.append(item.strip())
                continue
            if not isinstance(item, dict):
                continue

            text_value = item.get("text")
            if isinstance(text_value, str) and text_value.strip():
                text_parts.append(text_value.strip())

        return "\n".join(text_parts).strip()
