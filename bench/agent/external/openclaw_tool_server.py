"""OpenClaw 评测用 Tool Server。

在评测期间启动一个本地 HTTP 服务，将 OfficePrism Environment 的工具暴露为 REST 端点。
OpenClaw 通过自定义 skill 调用这些端点，从而在 OpenClaw 自有 agent loop 中使用 OfficePrism 工具。
所有调用经过 call_tool 回调，保证 trace 记录与 DB 变更完整可评测。
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable

from loguru import logger


class _ToolHandler(BaseHTTPRequestHandler):
    """处理 /call_tool 请求，转发给 call_tool 回调。"""

    call_tool: Callable[[str, dict], str]
    tools_schema: list[dict]
    stats: dict[str, object]

    def do_POST(self):
        if self.path == "/call_tool":
            self._handle_call_tool()
        else:
            self._respond(404, {"error": "not found"})

    def do_GET(self):
        if self.path == "/tools":
            self._respond(200, {"tools": self.tools_schema})
        elif self.path == "/health":
            self._respond(200, {"ok": True})
        else:
            self._respond(404, {"error": "not found"})

    def _handle_call_tool(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except Exception as e:
            self._respond(400, {"error": f"bad request: {e}"})
            return

        tool_name = body.get("tool_name", "")
        arguments = body.get("arguments", {})
        if not tool_name:
            self._respond(400, {"error": "missing tool_name"})
            return

        logger.info(
            f"[ToolServer] 收到工具调用请求 | "
            f"来源: {self.client_address[0]}:{self.client_address[1]} | "
            f"工具: {tool_name} | 参数: {json.dumps(arguments, ensure_ascii=False)}"
        )
        self.stats["call_count"] += 1

        try:
            result = self.call_tool(name=tool_name, arguments=arguments)
            logger.info(
                f"[ToolServer] 工具调用成功 | 工具: {tool_name} | "
                f"返回: {result[:200] if isinstance(result, str) else result}"
            )
            if tool_name == "done":
                self.stats["done_called"] = True
            self._respond(200, {"result": result})
        except StopIteration:
            logger.warning(f"[ToolServer] 超出最大步数限制 | 工具: {tool_name}")
            self._respond(429, {"error": "max_steps_exceeded"})
        except Exception as e:
            logger.error(f"[ToolServer] 工具调用失败 | 工具: {tool_name} | 错误: {e}")
            self._respond(500, {"error": str(e)})

    def _respond(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class ToolServer:
    """管理 tool HTTP server 生命周期。"""

    def __init__(
        self,
        call_tool: Callable[[str, dict], str],
        tools_schema: list[dict],
        port: int = 0,
        bind_host: str = "127.0.0.1",
        advertised_host: str | None = None,
    ):
        self.bind_host = bind_host
        self.advertised_host = advertised_host or bind_host
        self.stats: dict[str, object] = {"call_count": 0, "done_called": False}
        handler_cls = type(
            "_BoundHandler",
            (_ToolHandler,),
            {
                "call_tool": staticmethod(call_tool),
                "tools_schema": tools_schema,
                "stats": self.stats,
            },
        )
        self.server = HTTPServer((bind_host, port), handler_cls)
        self.port = self.server.server_address[1]
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        return self.url_for_host(self.advertised_host)

    @property
    def loopback_url(self) -> str:
        return self.url_for_host("127.0.0.1")

    @property
    def call_count(self) -> int:
        return self.stats["call_count"]

    @property
    def done_called(self) -> bool:
        return bool(self.stats["done_called"])

    def url_for_host(self, host: str) -> str:
        return f"http://{host}:{self.port}"

    def start(self):
        self._thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self._thread.start()
        logger.info(
            "External tool server started | "
            f"bind={self.bind_host}:{self.port} | advertised={self.base_url} | "
            f"loopback={self.loopback_url}"
        )

    def stop(self):
        self.server.shutdown()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info(
            "External tool server stopped | bind={} | calls={}",
            f"{self.bind_host}:{self.port}",
            self.call_count,
        )
