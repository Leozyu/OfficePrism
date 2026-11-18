"""PlanExecuteAgent：先规划后执行，第一轮输出计划，后续逐步执行工具调用。"""

from copy import deepcopy
from typing import List, Optional

from loguru import logger
from pydantic import BaseModel

from bench.agent.base import LocalAgent, ValidAgentInputMessage
from bench.agent.prompts import BASE_SYSTEM_PROMPT, PLAN_EXECUTE_INSTRUCTION
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


class PlanExecuteState(BaseModel):
    system_messages: list[SystemMessage]
    messages: list[APICompatibleMessage]
    plan_generated: bool = False


class PlanExecuteAgent(LocalAgent[PlanExecuteState]):

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
            """Call this function when you have completed all planned steps."""
            return f"{self.STOP_TOKEN}\n{result}"
        if self.STOP_FUNCTION_NAME not in {t.name for t in self.tools}:
            self.tools.append(as_tool(done))

    @property
    def system_prompt(self) -> str:
        return BASE_SYSTEM_PROMPT.format(
            domain_policy=self.domain_policy,
            ticket=self.task.ticket or "",
            strategy_instruction=PLAN_EXECUTE_INSTRUCTION,
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

    def get_init_state(self, message_history: Optional[list[Message]] = None) -> PlanExecuteState:
        if message_history is None:
            message_history = []
        return PlanExecuteState(
            system_messages=[SystemMessage(role="system", content=self.system_prompt)],
            messages=message_history,
            plan_generated=False,
        )

    def generate_next_message(
        self, message: Optional[ValidAgentInputMessage], state: PlanExecuteState
    ) -> tuple[AssistantMessage, PlanExecuteState]:
        if isinstance(message, UserMessage):
            raise ValueError("PlanExecuteAgent does not support user messages.")
        if isinstance(message, MultiToolMessage):
            state.messages.extend(message.tool_messages)
        elif message is not None:
            state.messages.append(message)

        messages = state.system_messages + state.messages

        if not state.plan_generated:
            assistant_message = generate(
                model=self.llm,
                tools=self.tools,
                messages=messages,
                llm_config=self.llm_config,
                **self.llm_args,
            )
            state.plan_generated = True

            if assistant_message.is_tool_call():
                assistant_message = self._check_if_stop_toolcall(assistant_message)
            else:
                state.messages.append(assistant_message)
                messages = state.system_messages + state.messages
                assistant_message = generate(
                    model=self.llm,
                    tools=self.tools,
                    messages=messages,
                    tool_choice="required",
                    llm_config=self.llm_config,
                    **self.llm_args,
                )
                if not assistant_message.is_tool_call():
                    raise ValueError("PlanExecuteAgent expects tool call after planning phase.")
                assistant_message = self._check_if_stop_toolcall(assistant_message)
        else:
            assistant_message = generate(
                model=self.llm,
                tools=self.tools,
                messages=messages,
                tool_choice="required",
                llm_config=self.llm_config,
                **self.llm_args,
            )
            if not assistant_message.is_tool_call():
                raise ValueError("PlanExecuteAgent only supports tool calls during execution.")
            assistant_message = self._check_if_stop_toolcall(assistant_message)

        state.messages.append(assistant_message)
        return assistant_message, state

    def set_seed(self, seed: int):
        cur_seed = self.llm_args.get("seed", None)
        if cur_seed is not None:
            logger.warning(f"Seed is already set to {cur_seed}, resetting it to {seed}")
        self.llm_args["seed"] = seed
