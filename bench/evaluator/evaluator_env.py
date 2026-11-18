import inspect
from typing import Callable

from loguru import logger

from bench.data_model.message import AssistantMessage, Message, ToolCall, UserMessage
from bench.data_model.simulation import DBCheck, EnvAssertionCheck, RewardInfo
from bench.data_model.tasks import RewardType, Task
from bench.environment.environment import Environment
from bench.evaluator.evaluator_base import EvaluatorBase
from bench.evaluator.evaluator_db_text import SOFT_KEYS, judge_db_text

# 结构分口径:把自由文本软字段并入 DB 哈希豁免集,使结构分只校验非文本写入是否正确;
# 文本内容的对错改由 db_text(LLM 文案分)把关。模块加载时一次性生效。
from bench.environment import toolkit as _toolkit
_toolkit._UNSTABLE_FIELDS |= SOFT_KEYS


class EnvironmentEvaluator(EvaluatorBase):
    """
    Evaluator focuses on endstate of the simulation environment.
    """

    _llm_config = None

    @classmethod
    def _get_llm_config(cls):
        """懒加载 evaluator 的 LLM 配置(供 db_text 文案分调用)。"""
        if cls._llm_config is None:
            from bench.config import get_llm_config
            try:
                cls._llm_config = get_llm_config("evaluator")
            except Exception:
                cls._llm_config = {}
        return cls._llm_config

    @classmethod
    def _construct_environment(
        cls,
        environment_constructor: Callable[[], Environment],
        *,
        solo_mode: bool = False,
        tool_mode: str | None = None,
    ) -> Environment:
        signature = inspect.signature(environment_constructor)
        kwargs = {}
        if "solo_mode" in signature.parameters:
            kwargs["solo_mode"] = solo_mode
        if tool_mode is not None and "tool_mode" in signature.parameters:
            kwargs["tool_mode"] = tool_mode
        return environment_constructor(**kwargs)

    @classmethod
    def calculate_reward(
        cls,
        environment_constructor: Callable[[], Environment],
        task: Task,
        full_trajectory: list[
            Message
        ],
        solo_mode: bool = False,
        tool_mode: str = "full",
        strict_responses: bool = True,
    ) -> RewardInfo:
        """
        Calculate the reward for the simulation.
        Args:
            environment_constructor: Callable[[], Environment]
            task: Task
            full_trajectory: list[Message] (Must include the message history from task initial state)
            solo_mode: bool
        Returns:
            RewardInfo
        """
        if task.evaluation_criteria is None:
            return RewardInfo(
                reward=1.0,
                info={"note": "No evaluation criteria"},
            )
        expected_actions = task.evaluation_criteria.actions
        env_assertions = task.evaluation_criteria.env_assertions
        if expected_actions is None and env_assertions is None:
            return RewardInfo(
                reward=1.0,
                db_check=DBCheck(db_match=True, db_reward=1.0),
                info={"note": "No expected actions or env assertions"},
            )

        initialization_data = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_data is not None
        ):
            initialization_data = task.initial_state.initialization_data

        initialization_actions = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_actions is not None
        ):
            initialization_actions = task.initial_state.initialization_actions

        message_history = []
        if (
            task.initial_state is not None
            and task.initial_state.message_history is not None
        ):
            message_history = task.initial_state.message_history

        predicted_environment = cls._construct_environment(
            environment_constructor,
            solo_mode=solo_mode,
            tool_mode=tool_mode,
        )
        predicted_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=full_trajectory,
            strict_responses=strict_responses,
        )
        predicted_tool_calls: list[ToolCall] = []
        for message in full_trajectory:
            if (
                isinstance(message, AssistantMessage)
                or isinstance(message, UserMessage)
            ) and message.is_tool_call():
                predicted_tool_calls.extend(message.tool_calls)

        # Setting up gold environment
        gold_environment = cls._construct_environment(environment_constructor)
        gold_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=message_history,
        )
        golden_actions = task.evaluation_criteria.actions or []
        for action in golden_actions:
            try:
                gold_environment.make_tool_call(
                    tool_name=action.name,
                    requestor=action.requestor,
                    **action.arguments,
                )
            except Exception as e:
                print(
                    f"Error in golden actions {action.name}({action.arguments}): {e}"
                )

        # Comparing the environments
        agent_db_hash = gold_environment.get_db_hash()
        user_db_hash = gold_environment.get_user_db_hash()
        predicted_agent_db_hash = predicted_environment.get_db_hash()
        predicted_user_db_hash = predicted_environment.get_user_db_hash()
        agent_db_match = agent_db_hash == predicted_agent_db_hash
        user_db_match = user_db_hash == predicted_user_db_hash
        if agent_db_match and user_db_match:
            db_struct = 1.0
            db_match = True
        else:
            db_struct = 0.0
            db_match = False

        # 文案分:golden 工具链含中文自由文本字段时,用 evaluator LLM 判 agent 写入文本是否合格;
        # 无自由文本则恒为 1.0(退化为纯结构分)。db_status = 结构分 × 文案分。
        db_text_detail: list = []
        db_text = judge_db_text(
            task, predicted_tool_calls, cls._get_llm_config(), details_out=db_text_detail
        )
        db_reward = db_struct * db_text

        db_check = DBCheck(
            db_match=db_match, db_reward=db_reward,
            db_struct=db_struct, db_text=db_text,
            db_text_detail=db_text_detail or None,
        )

        # Run env assertions
        env_assertions = task.evaluation_criteria.env_assertions or []
        env_assertion_checks = []
        env_assertion_reward = 1.0
        for env_assertion in env_assertions:
            success = predicted_environment.run_env_assertion(
                env_assertion,
                raise_assertion_error=False,
            )
            res = EnvAssertionCheck(
                env_assertion=env_assertion,
                met=success,
                reward=1.0 if success else 0.0,
            )
            env_assertion_checks.append(res)
            env_assertion_reward *= res.reward

        reward = 1.0
        reward_breakdown = {}
        if RewardType.DB in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.DB] = db_reward
            reward *= db_reward
        if RewardType.ENV_ASSERTION in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.ENV_ASSERTION] = env_assertion_reward
            reward *= env_assertion_reward

        return RewardInfo(
            reward=reward,
            db_check=db_check,
            env_assertions=env_assertion_checks,
            reward_basis=task.evaluation_criteria.reward_basis,
            reward_breakdown=reward_breakdown,
        )
