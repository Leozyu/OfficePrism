"""ReActAgent：每步显式推理后调用工具。"""

from copy import deepcopy
from typing import List, Optional

from loguru import logger
from pydantic import BaseModel

from bench.agent.base import LocalAgent, ValidAgentInputMessage, is_valid_agent_history_message
from bench.agent.prompts import BASE_SYSTEM_PROMPT, FORCE_TOOL_INSTRUCTION, REACT_INSTRUCTION
from bench.data_model.message import (
    APICompatibleMessage,
    AssistantMessage,
    Message,
    MultiToolMessage,
    SystemMessage,
    UserMessage,
)
from bench.data_model.tasks import Task
from bench.environment.tool import Tool, as_tool
from bench.utils.llm_utils import generate


class ReactAgentState(BaseModel):
    system_messages: list[SystemMessage]
    messages: list[APICompatibleMessage]


class ReActAgent(LocalAgent[ReactAgentState]):

    STOP_FUNCTION_NAME = "done"
    STOP_TOKEN = "###STOP###"

    def __init__(
        self,
        tools: List[Tool],
        domain_policy: str,
        task: Task,
        llm: Optional[str] = None,
        llm_args: Optional[dict] = None,
        llm_config: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(tools=tools, domain_policy=domain_policy)
        assert task.ticket is not None or task.evaluation_criteria is not None, (
            f"Task {task.id} must have ticket or evaluation_criteria"
        )
        self.task = task
        if llm_config is None:
            try:
                from bench.config import get_llm_config
                llm_config = get_llm_config("agent")
            except ImportError:
                llm_config = {}
        self.llm = llm_config.get("model", llm or "gpt-4")
        self.llm_config = llm_config
        self.llm_args = deepcopy(llm_args) if llm_args is not None else {}
        self._add_stop_tool()

    def _add_stop_tool(self) -> None:
        def done(result: str) -> str:
            """Call this function when you have solved the ticket."""
            return f"{self.STOP_TOKEN}\n{result}"
        if self.STOP_FUNCTION_NAME not in {t.name for t in self.tools}:
            self.tools.append(as_tool(done))

    @property
    def system_prompt(self) -> str:
        return BASE_SYSTEM_PROMPT.format(
            domain_policy=self.domain_policy,
            ticket=self.task.ticket or "",
            strategy_instruction=REACT_INSTRUCTION,
            stop_function_name=self.STOP_FUNCTION_NAME,
        )

    @property
    def _force_tool_system_prompt(self) -> str:
        """强制工具调用用的系统提示：去掉 <thought> 导向，仅保留 policy/ticket/规则。"""
        return BASE_SYSTEM_PROMPT.format(
            domain_policy=self.domain_policy,
            ticket=self.task.ticket or "",
            strategy_instruction=FORCE_TOOL_INSTRUCTION,
            stop_function_name=self.STOP_FUNCTION_NAME,
        )

    @classmethod
    def is_stop(cls, message: AssistantMessage) -> bool:
        return bool(message.content and cls.STOP_TOKEN in message.content)

    def _check_if_stop_toolcall(self, message: AssistantMessage) -> AssistantMessage:
        if not message.tool_calls:
            return message
        for tc in message.tool_calls:
            if tc.name == self.STOP_FUNCTION_NAME:
                result = tc.arguments.get("result", "") if tc.arguments else ""
                message.content = f"{self.STOP_TOKEN}\n{result}".strip()
                message.tool_calls = None
                return message
        return message

    def get_init_state(self, message_history: Optional[list[Message]] = None) -> ReactAgentState:
        if message_history is None:
            message_history = []
        messages: list[APICompatibleMessage] = list(message_history)
        if not messages:
            # Anthropic 协议（网关 对 claude-* 走 litellm→Anthropic）要求至少一条
            # 非 system 消息；纯 system 起始会 400。OpenAI 协议无此限制，补一条
            # kickoff user 消息对两种协议都安全，且让模型明确从工单开始执行。
            messages = [
                UserMessage(
                    role="user",
                    content="请根据以上 policy 与工单开始执行任务，直接调用工具完成，无需与用户对话。",
                )
            ]
        return ReactAgentState(
            system_messages=[SystemMessage(role="system", content=self.system_prompt)],
            messages=messages,
        )

    def generate_next_message(
        self, message: Optional[ValidAgentInputMessage], state: ReactAgentState
    ) -> tuple[AssistantMessage, ReactAgentState]:
        if isinstance(message, UserMessage):
            raise ValueError("ReActAgent does not support user messages during execution.")
        if isinstance(message, MultiToolMessage):
            state.messages.extend(message.tool_messages)
        elif message is not None:
            state.messages.append(message)

        messages = state.system_messages + state.messages
        assistant_message = generate(
            model=self.llm,
            tools=self.tools,
            messages=messages,
            llm_config=self.llm_config,
            **self.llm_args,
        )
        # 有的模型（如 网关 上的 gpt-5.5）会只输出 <thought> 文本就停，且网关未真正
        # 强制 tool_choice=required。用「追加显式 nudge 消息 + tool_choice=required」逼它
        # 回到工具调用，给若干次机会；claude 等首次即调用工具的模型不会进入此分支。
        max_tool_retries = 3
        retry = 0
        while not assistant_message.is_tool_call() and retry < max_tool_retries:
            retry += 1
            logger.warning(
                f"ReActAgent: model returned text without tool call (retry {retry}/{max_tool_retries}) "
                f"| content={assistant_message.content!r}"
            )
            # 空/纯空白 content 的 assistant 消息一旦进历史，Anthropic 协议网关会以
            # "text content blocks must contain non-whitespace text" 拒绝后续所有请求
            # （网关 显式 400，网关 表现为全通道 AllModelsFailed 500），该 case 会
            # 确定性卡死；入历史前替换为占位文本。
            if not (assistant_message.content or "").strip():
                assistant_message.content = "(empty response)"
            state.messages.append(assistant_message)
            # 必须再补一条 user 消息：若对话以 assistant 结尾直接重发，Anthropic 协议
            # 视为 prefill，部分供应商通道直接 400 "does not support assistant message
            # prefill"，导致该 case 确定性卡死。
            state.messages.append(
                UserMessage(
                    role="user",
                    content="请不要输出纯文本回复，直接调用工具继续完成任务；任务完成时调用停止工具。",
                )
            )
            # 用去掉 <thought> 导向的强制系统提示重发：推理模型（gpt-5.5）在带 <thought>
            # 的系统提示下即便 required 也不产工具调用，换成强制提示即可逼出。
            force_system = [SystemMessage(role="system", content=self._force_tool_system_prompt)]
            messages = force_system + state.messages
            assistant_message = generate(
                model=self.llm,
                tools=self.tools,
                messages=messages,
                llm_config=self.llm_config,
                tool_choice="required",
                **self.llm_args,
            )
        if not assistant_message.is_tool_call():
            raise ValueError(
                "ReActAgent only supports tool calls. "
                f"model={self.llm} content={assistant_message.content!r}"
            )
        assistant_message = self._check_if_stop_toolcall(assistant_message)
        state.messages.append(assistant_message)
        return assistant_message, state

    def set_seed(self, seed: int):
        cur_seed = self.llm_args.get("seed", None)
        if cur_seed is not None:
            logger.warning(f"Seed is already set to {cur_seed}, resetting it to {seed}")
        self.llm_args["seed"] = seed
