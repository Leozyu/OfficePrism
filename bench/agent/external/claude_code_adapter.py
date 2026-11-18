"""Claude Code 外部适配器。

通过本地 Tool Server + Claude Code headless CLI 实现真正的 Claude Code 评测：
1. 启动 HTTP tool server，将 OfficePrism 工具暴露为 REST 端点
2. 拼系统 prompt，告知 Claude Code 通过执行 curl 调用工具
3. Claude Code 以自身 agent loop 自主规划、调用工具、完成任务
4. 所有工具调用经 call_tool 回调记录 trace 并修改 DB

与 openclaw_adapter 一致的思路：外部 agent 用自己的 shell(Bash) 能力 curl 本地
tool server，评测只关心最终答案文本与 DB 变更。
"""

import json
import os
import subprocess
import textwrap
from typing import Any, Callable

from loguru import logger

from bench.agent.external.openclaw_tool_server import ToolServer


class ClaudeCodeAdapter:
    """让 Claude Code 以自身 agent 能力完成 OfficePrism 任务。"""

    def __init__(self, llm_config: dict[str, Any], domain_policy: str = ""):
        self.llm_config = llm_config
        self.domain_policy = domain_policy

        self.bin = os.environ.get("CLAUDE_CODE_BIN") or llm_config.get(
            "claude_code_bin", "claude"
        )
        self.model = os.environ.get("CLAUDE_CODE_MODEL") or llm_config.get(
            "claude_code_model", "claude-sonnet-4-6"
        )
        self.timeout = float(
            os.environ.get("CLAUDE_CODE_TIMEOUT") or llm_config.get("claude_code_timeout", 600)
        )
        # bypassPermissions 保证 headless 下工具调用不会因权限确认而卡住。
        self.permission_mode = os.environ.get("CLAUDE_CODE_PERMISSION_MODE") or llm_config.get(
            "claude_code_permission_mode", "bypassPermissions"
        )
        self.extra_args = list(llm_config.get("claude_code_extra_args", []) or [])

        # 可选：为 subprocess 注入 API 认证（官方 API 或自定义网关）。
        # 未配置则继承当前进程环境（例如已 login 的凭证或已导出的环境变量）。
        self.api_key = os.environ.get("CLAUDE_CODE_API_KEY") or llm_config.get(
            "claude_code_api_key", ""
        )
        self.base_url = os.environ.get("CLAUDE_CODE_BASE_URL") or llm_config.get(
            "claude_code_base_url", ""
        )

        # 每次 solve 后填充，供 runner 记账用（token / 真实美元成本）。
        self.last_usage: dict | None = None
        self.last_cost: float | None = None
        # infra 级失败（超时 / CLI 非零退出 / 找不到二进制）信号，供上层写入
        # error 字段并触发重试，避免把基础设施失败误记为任务失败。
        self.last_error: str | None = None

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

    def _build_prompt(self, task: str, tools_schema: list[dict], server_url: str) -> str:
        tool_docs = self._build_tool_docs(tools_schema)
        policy_block = (
            f"## 业务政策\n{self.domain_policy}\n" if self.domain_policy else ""
        )
        return textwrap.dedent(f"""\
你是 OfficePrism 任务执行代理。你的唯一目标是使用下面列出的业务工具完成用户的任务。

## 极其重要的规则（必须严格遵守）
1. 你 **必须且只能** 通过 Bash 工具执行 curl 命令调用业务工具，**严禁** 用其他任何方式（如直接编造结果、读写本地文件、猜测数据）。
2. 每次调用工具，**必须** 用 Bash 执行以下格式的 curl 命令：

curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name": "<工具名>", "arguments": {{<参数JSON>}}}}'

3. curl 会返回 JSON，格式为 {{"result": "..."}}，这就是工具的真实返回值。
4. **绝对禁止** 编造或猜测工具返回值。每次都必须执行 curl 拿到真实结果。
5. 如果返回 {{"error": "max_steps_exceeded"}}，立即停止并汇报已完成的内容。
6. list/search/find 类工具只用于定位候选记录或引用 ID；如果已经定位到目标记录且存在对应的 get_* 明细工具，必须调用该 get_* 工具确认最终字段后再作答。
7. 完成所有必要的工具调用后，给出简洁的结果摘要作为最终回复。

## 调用示例
要查询员工详情，执行：
curl -s -X POST {server_url}/call_tool \\
  -H "Content-Type: application/json" \\
  -d '{{"tool_name": "get_employee_details", "arguments": {{"employee_ref": "EMP001"}}}}'

{policy_block}## 可用工具列表

{tool_docs}

## 用户任务
{task}
""")

    def solve(self, task: str, tools: list[dict], call_tool: Callable[[str, dict], str]) -> str:
        self.last_usage = None
        self.last_cost = None
        self.last_error = None
        tool_server = ToolServer(call_tool=call_tool, tools_schema=tools)
        tool_server.start()
        try:
            return self._run_claude_code(task, tools, tool_server.base_url)
        finally:
            tool_server.stop()

    def _run_claude_code(self, task: str, tools_schema: list[dict], server_url: str) -> str:
        prompt = self._build_prompt(task, tools_schema, server_url)

        # 注意：prompt 通过 stdin 传入，不作为命令行参数。
        # full 模式下 prompt 内嵌全部工具 schema（可达 ~900 个工具、数 MB），
        # 作为 argv 会触发 OSError [Errno 7] Argument list too long（超 ARG_MAX）。
        # `claude -p` 在未提供 prompt 位置参数时会从 stdin 读取。
        cmd = [
            self.bin,
            "-p",
            "--output-format",
            "json",
            "--model",
            self.model,
            "--permission-mode",
            self.permission_mode,
            *self.extra_args,
        ]

        # 用户全局 ~/.claude/settings.json 的 env 块会覆盖子进程环境变量，
        # 可能把请求劫持到其它端点。命令行 --settings 优先级最高，用它把
        # 本次路由的 base_url/api_key/模型钉死，附带把 haiku/sonnet/opus
        # 默认模型全部指到目标模型，避免 CLI 后台小模型调用打到不存在的模型。
        if self.base_url or self.api_key:
            settings_env: dict[str, str] = {
                "ANTHROPIC_MODEL": self.model,
                "ANTHROPIC_DEFAULT_HAIKU_MODEL": self.model,
                "ANTHROPIC_DEFAULT_SONNET_MODEL": self.model,
                "ANTHROPIC_DEFAULT_OPUS_MODEL": self.model,
                "CLAUDE_CODE_SUBAGENT_MODEL": self.model,
            }
            if self.base_url:
                settings_env["ANTHROPIC_BASE_URL"] = self.base_url
            if self.api_key:
                settings_env["ANTHROPIC_API_KEY"] = self.api_key
                settings_env["ANTHROPIC_AUTH_TOKEN"] = self.api_key
            cmd += ["--settings", json.dumps({"env": settings_env})]

        env = os.environ.copy()
        if self.api_key:
            env["ANTHROPIC_API_KEY"] = self.api_key
        if self.base_url:
            env["ANTHROPIC_BASE_URL"] = self.base_url

        logger.info(
            "Running Claude Code adapter | model={} | permission_mode={} | server={}",
            self.model,
            self.permission_mode,
            server_url,
        )

        try:
            proc = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=self.timeout + 30,
                env=env,
                input=prompt,
            )
        except FileNotFoundError:
            logger.error("Claude Code CLI not found in PATH: {}", self.bin)
            self.last_error = f"claude_code_binary_not_found:{self.bin}"
            return ""
        except subprocess.TimeoutExpired:
            logger.error("Claude Code CLI timed out after {}s", self.timeout)
            self.last_error = f"claude_code_timeout:{self.timeout}s"
            return ""

        if proc.returncode != 0:
            logger.error(
                "Claude Code CLI failed | code={} | stderr={} | stdout_tail={}",
                proc.returncode,
                (proc.stderr or "")[-2000:],
                (proc.stdout or "")[-1000:],
            )
            self.last_error = f"claude_code_exit:{proc.returncode}"
            return ""

        return self._extract_cli_text(proc.stdout)

    def _extract_cli_text(self, stdout: str) -> str:
        stdout = (stdout or "").strip()
        if not stdout:
            return ""

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            logger.warning("Claude Code CLI returned non-JSON output")
            return stdout

        if isinstance(data, dict):
            self._record_usage(data)
            if data.get("is_error"):
                logger.warning(
                    "Claude Code reported error result | subtype={}",
                    data.get("subtype"),
                )
            result = data.get("result")
            if isinstance(result, str) and result.strip():
                return result.strip()

        return ""

    def _record_usage(self, data: dict) -> None:
        """从 CLI JSON 提取 token 用量与真实美元成本。

        Claude Code 的 usage 把输入拆成 input / cache_creation / cache_read 三部分，
        全部计入 prompt_tokens；total_cost_usd 是该次运行的精确计费。
        """
        usage = data.get("usage") or {}
        prompt = (
            int(usage.get("input_tokens", 0) or 0)
            + int(usage.get("cache_creation_input_tokens", 0) or 0)
            + int(usage.get("cache_read_input_tokens", 0) or 0)
        )
        completion = int(usage.get("output_tokens", 0) or 0)
        if prompt or completion:
            self.last_usage = {
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": prompt + completion,
            }
        cost = data.get("total_cost_usd")
        if isinstance(cost, (int, float)):
            self.last_cost = float(cost)
