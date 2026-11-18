from bench.data_model.message import AssistantMessage, Message, ToolCall, UserMessage
from bench.data_model.simulation import ActionCheck, RewardInfo
from bench.data_model.tasks import Action, RewardType, Task
from bench.evaluator.evaluator_base import EvaluatorBase


class ActionEvaluator(EvaluatorBase):
    """
    Evaluates whether or not the agent communicated the required information.
    """

    @classmethod
    def calculate_reward(
        cls,
        task: Task,
        full_trajectory: list[Message],
    ) -> RewardInfo:
        """
        Calculate the reward based on whether the agent communicated the required information.
        """
        if task.evaluation_criteria is None:
            return RewardInfo(
                reward=1.0,
                action_checks=[],
                info={"note": "No evaluation criteria"},
                reward_breakdown={RewardType.ACTION: 1.0},
            )
        golden_actions = task.evaluation_criteria.actions
        forbidden_tools = set(task.evaluation_criteria.forbidden_tools or [])
        predicted_tool_calls = cls.collect_tool_calls(full_trajectory)
        forbidden_called = sorted(
            {
                tool_call.name
                for tool_call in predicted_tool_calls
                if tool_call.name in forbidden_tools
            }
        )
        forbidden_reward = 0.0 if forbidden_called else 1.0
        if not golden_actions:
            return RewardInfo(
                reward=forbidden_reward,
                info={
                    "note": "No actions to evaluate",
                    "forbidden_called": forbidden_called,
                },
                reward_breakdown={RewardType.ACTION: forbidden_reward},
            )

        action_checks = cls.evaluate_actions(full_trajectory, golden_actions, predicted_tool_calls)

        # Calculate reward: 1 if all expectations are met, 0 otherwise
        all_expectations_met = all(result.action_match for result in action_checks)
        reward = (1.0 if all_expectations_met else 0.0) * forbidden_reward

        return RewardInfo(
            reward=reward,
            action_checks=action_checks,
            info={"forbidden_called": forbidden_called},
            reward_breakdown={RewardType.ACTION: reward},
        )

    @classmethod
    def _normalize_tool_call(cls, tool_call: ToolCall) -> list[ToolCall]:
        """Expand call_tool meta calls into the delegated real business tool."""
        if tool_call.name != "call_tool":
            return [tool_call]
        args = tool_call.arguments or {}
        delegated_name = args.get("name") or args.get("tool_name")
        delegated_args = args.get("arguments") or {}
        if not delegated_name or not isinstance(delegated_args, dict):
            return [tool_call]
        return [
            tool_call,
            ToolCall(
                id=f"{tool_call.id}:delegated",
                name=delegated_name,
                arguments=delegated_args,
                requestor=tool_call.requestor,
            ),
        ]

    @classmethod
    def collect_tool_calls(
        cls,
        full_trajectory: list[Message],
    ) -> list[ToolCall]:
        predicted_tool_calls: list[ToolCall] = []
        for message in full_trajectory:
            if (
                isinstance(message, AssistantMessage)
                or isinstance(message, UserMessage)
            ) and message.is_tool_call():
                for tool_call in message.tool_calls:
                    predicted_tool_calls.extend(cls._normalize_tool_call(tool_call))
        return predicted_tool_calls

    @classmethod
    def evaluate_actions(
        cls,
        full_trajectory: list[Message],
        golden_actions: list[Action],
        predicted_tool_calls: list[ToolCall] | None = None,
    ) -> list[ActionCheck]:
        """
        Evaluate whether the agent communicates the information correctly.
        """
        if len(golden_actions) == 0:
            return []

        if predicted_tool_calls is None:
            predicted_tool_calls = cls.collect_tool_calls(full_trajectory)

        # Gold actions are required capabilities, not a forced global order.
        # Each predicted call can satisfy at most one gold action.
        action_checks = []
        used_predicted: set[int] = set()
        for gold_action in golden_actions:
            found = False
            for idx, pred_tool_call in enumerate(predicted_tool_calls):
                if idx in used_predicted:
                    continue
                if gold_action.compare_with_tool_call(pred_tool_call):
                    found = True
                    used_predicted.add(idx)
                    break
            if not found:
                gold_action_reward = 0.0
                gold_action_match = False
            else:
                gold_action_reward = 1.0
                gold_action_match = True
            action_checks.append(
                ActionCheck(
                    action=gold_action,
                    action_match=gold_action_match,
                    action_reward=gold_action_reward,
                )
            )
        return action_checks
