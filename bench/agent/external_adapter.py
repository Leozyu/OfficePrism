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

import inspect
import threading
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

    STOP_FUNCTION_NAME = "done"
    STOP_TOKEN = "###STOP###"

    def __init__(self, agent: ExternalAgentProtocol, max_steps: int = 200):
        self.agent = agent
        self.max_steps = max_steps

    def run_task(self, task: Task, environment: Environment) -> SimulationRun:
        tools_schema = [t.openai_schema for t in environment.get_tools()]
        if self.STOP_FUNCTION_NAME not in {
            schema.get("function", schema).get("name") for schema in tools_schema
        }:
            tools_schema.append(self._stop_tool_schema())
        trace: list[Message] = []
        step_count = 0
        start_time = get_now()
        start_perf = time.perf_counter()
        termination = TerminationReason.AGENT_STOP
        final_answer = ""
        # deepagents/LangGraph 的 ToolNode 会用线程池并发执行同一 AI 轮的多个工具调用，
        # 而下面的 call_tool 把 (assistant, tool) 成对 append 到共享 trace 且改动共享 env DB。
        # 无锁并发会让两次调用交错，产生相邻的两条 assistant 消息，令后续 set_state 的
        # get_actions_from_messages 抛 "Tool message expected. Got AssistantMessage"；并发改
        # DB 也不安全。用每任务一把锁把整个回调串行化：模型仍可发并行 tool_calls，只是执行
        # 被串行化为干净、可回放的成对轨迹（对顺序型 agent 无竞争、零行为改变）。
        call_lock = threading.Lock()

        def call_tool(name: str, arguments: dict) -> str:
            nonlocal step_count, termination, final_answer
            with call_lock:
                step_count += 1
                if step_count > self.max_steps:
                    termination = TerminationReason.MAX_STEPS
                    raise StopIteration("Max steps exceeded")

                stop_arguments = arguments
                if (
                    name == "call_tool"
                    and isinstance(arguments, dict)
                    and arguments.get("name") == self.STOP_FUNCTION_NAME
                ):
                    stop_arguments = arguments.get("arguments") or {}

                if name == self.STOP_FUNCTION_NAME or stop_arguments is not arguments:
                    result = str((stop_arguments or {}).get("result", "")).strip()
                    if not final_answer:
                        final_answer = result
                    return f"{self.STOP_TOKEN}\n{final_answer}".strip()

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
            solve_kwargs = {
                "task": task.ticket or "",
                "tools": tools_schema,
                "call_tool": call_tool,
            }
            if "task_obj" in inspect.signature(self.agent.solve).parameters:
                solve_kwargs["task_obj"] = task
            answer = self.agent.solve(**solve_kwargs)
        except StopIteration:
            logger.warning(f"External agent hit max_steps ({self.max_steps})")
        except Exception as e:
            logger.error(f"External agent error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            termination = TerminationReason.TOO_MANY_ERRORS

        # 外部适配器（如 Claude Code）在 solve 后可暴露真实 token/成本，挂到最终
        # assistant 消息上，让下游 get_token_usage / get_cost 能统一记账。
        last_usage = getattr(self.agent, "last_usage", None)
        last_cost = getattr(self.agent, "last_cost", None)

        answer = final_answer or answer
        if answer:
            final_msg = AssistantMessage(
                role="assistant",
                content=f"{self.STOP_TOKEN}\n{answer}",
                timestamp=get_now(),
                usage=last_usage,
                cost=last_cost,
            )
            trace.append(final_msg)
        elif last_usage is not None or last_cost is not None:
            trace.append(
                AssistantMessage(
                    role="assistant",
                    content="",
                    timestamp=get_now(),
                    usage=last_usage,
                    cost=last_cost,
                )
            )

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

    @classmethod
    def _stop_tool_schema(cls) -> dict:
        return {
            "type": "function",
            "function": {
                "name": cls.STOP_FUNCTION_NAME,
                "description": "完成任务后调用此工具。result 参数填写最终结论文本。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "string",
                            "description": "面向用户的最终结论文本。",
                        }
                    },
                    "required": ["result"],
                },
            },
        }
