"""外部 Agent 适配层。

提供 ExternalAgentProtocol + ExternalAgentRunner，让 GAIA 榜单等开源 Agent
通过实现一个 solve() 方法即可接入 OfficePrism 评测。

用法示例::

    class MyGaiaAgent:
        def solve(self, task, tools, call_tool):
            # 自管工具循环
            result = call_tool("get_employee_details", {"employee_ref": "EMP001"})
            return f"查询结果：{result}"

    runner = ExternalAgentRunner(MyGaiaAgent())
    sim_run = runner.run_task(task, environment)
    reward_info = evaluate_simulation(sim_run, task, ...)
"""

import time
import uuid
from typing import Callable, Protocol, runtime_checkable

from loguru import logger

from bench.data_model.message import (
    AssistantMessage,
    Message,
    ToolCall,
    ToolMessage,
)
from bench.data_model.simulation import SimulationRun, TerminationReason
from bench.data_model.tasks import Task
from bench.environment.environment import Environment
from bench.utils.utils import format_time, get_now


@runtime_checkable
class ExternalAgentProtocol(Protocol):
    """外部 Agent 只需实现此方法即可接入评测。"""

    def solve(
        self,
        task: str,
        tools: list[dict],
        call_tool: Callable[[str, dict], str],
    ) -> str:
        """
        执行任务并返回最终答案。

        Args:
            task: ticket 文本描述
            tools: OpenAI function schema 列表
            call_tool: 调用工具的回调，call_tool(tool_name, arguments) -> result_string

        Returns:
            最终答案字符串
        """
        ...


class ExternalAgentRunner:
    """将 ExternalAgentProtocol 包装为可评测的 runner，绕过 Orchestrator。"""

    def __init__(self, agent: ExternalAgentProtocol, max_steps: int = 200):
        self.agent = agent
        self.max_steps = max_steps

    def run_task(self, task: Task, environment: Environment) -> SimulationRun:
        tools_schema = [t.openai_schema for t in environment.get_tools()]
        trace: list[Message] = []
        step_count = 0
        start_time = get_now()
        start_perf = time.perf_counter()
        termination = TerminationReason.AGENT_STOP

        def call_tool(name: str, arguments: dict) -> str:
            nonlocal step_count, termination
            step_count += 1
            if step_count > self.max_steps:
                termination = TerminationReason.MAX_STEPS
                raise StopIteration("Max steps exceeded")

            tool_call = ToolCall(
                id=str(uuid.uuid4()), name=name, arguments=arguments
            )
            assistant_msg = AssistantMessage(
                role="assistant",
                content=None,
                tool_calls=[tool_call],
                timestamp=get_now(),
            )
            trace.append(assistant_msg)

            tool_msg = environment.get_response(tool_call)
            trace.append(tool_msg)
            return tool_msg.content

        answer = ""
        try:
            answer = self.agent.solve(
                task=task.ticket or "",
                tools=tools_schema,
                call_tool=call_tool,
            )
        except StopIteration:
            logger.warning(f"External agent hit max_steps ({self.max_steps})")
        except Exception as e:
            logger.error(f"External agent error: {e}")
            termination = TerminationReason.TOO_MANY_ERRORS

        if answer:
            final_msg = AssistantMessage(
                role="assistant",
                content=f"###STOP###\n{answer}",
                timestamp=get_now(),
            )
            trace.append(final_msg)

        duration = time.perf_counter() - start_perf
        return SimulationRun(
            id=str(uuid.uuid4()),
            task_id=task.id,
            start_time=start_time,
            end_time=get_now(),
            duration=duration,
            termination_reason=termination,
            reward_info=None,
            messages=trace,
        )
