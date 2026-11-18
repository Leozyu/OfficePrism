import json

from bench.config import DEFAULT_LLM_NL_ASSERTIONS, DEFAULT_LLM_NL_ASSERTIONS_ARGS, get_llm_config
from bench.data_model.message import Message, SystemMessage, UserMessage
from bench.data_model.simulation import NLAssertionCheck, RewardInfo
from bench.data_model.tasks import RewardType, Task
from bench.utils.llm_utils import generate


class NLAssertionsEvaluator:
    """
    Judge that evaluates whether a trajectory adheres to all the natural-language assertions.
    """
    
    # 类级别的配置缓存
    _llm_config = None
    
    @classmethod
    def _get_llm_config(cls):
        """获取 evaluator 的 LLM 配置"""
        if cls._llm_config is None:
            try:
                cls._llm_config = get_llm_config("evaluator")
            except Exception:
                cls._llm_config = {}
        return cls._llm_config

    @classmethod
    def calculate_reward(
        cls,
        task: Task,
        full_trajectory: list[Message],
    ) -> RewardInfo:
        """
        Calculate the reward for the simulation by using an LLM to evaluate whether the trajectory adheres to all the natural-language assertions
        """
        if task.evaluation_criteria is None:
            return RewardInfo(
                reward=1.0,
                nl_assertions=[],
                info={"note": "No evaluation criteria"},
                reward_breakdown={RewardType.NL_ASSERTION: 1.0},
            )
        nl_assertions = task.evaluation_criteria.nl_assertions
        if not nl_assertions:
            return RewardInfo(
                reward=1.0,
                nl_assertions=[],
                info={"note": "No nl_assertions to evaluate"},
                reward_breakdown={RewardType.NL_ASSERTION: 1.0},
            )

        nl_assertions_checks = cls.evaluate_nl_assertions(
            full_trajectory, nl_assertions
        )

        nl_assertions_checks = cls._align_checks_to_expected_outcomes(
            nl_assertions,
            nl_assertions_checks,
        )

        # 多条断言按平均分计算；judge 漏返回的断言按失败计。
        reward = sum(1.0 if result.met else 0.0 for result in nl_assertions_checks) / len(nl_assertions)

        return RewardInfo(
            reward=reward,
            nl_assertions=nl_assertions_checks,
            reward_breakdown={RewardType.NL_ASSERTION: reward},
        )

    @classmethod
    def _align_checks_to_expected_outcomes(
        cls,
        nl_assertions: list[str],
        checks: list[NLAssertionCheck],
    ) -> list[NLAssertionCheck]:
        """按输入断言顺序对齐 judge 结果，缺失项显式计为失败。

        单断言（本 benchmark 恒为 1 条）走 AND 聚合路径：那条 nl_assertion 是多点合并答案
        （"1. … 2. … 3. …"），judge 按「逐点判分」指令拆成 N 条子结果，其 echo 字符串≠整条断言，
        严格 == 对齐会全部落空、误记「did not return」= 假非判决。改为把这 N 条子结果 AND 成一条：
        met ⟺ 所有子结果都 met；judge 真返空才保留「did not return」（避免 all([])==True 误判为过）。
        多断言（>1，本 benchmark 不触发）仍走原严格 == 对齐路径，保持既有行为。
        """
        # 单断言：AND 聚合 judge 拆出的所有子结果（与离线 rejudge_nl.py 同口径）
        if len(nl_assertions) == 1:
            assertion = nl_assertions[0]
            if not checks:
                return [
                    NLAssertionCheck(
                        nl_assertion=assertion,
                        met=False,
                        justification="Judge did not return a result for this assertion.",
                    )
                ]
            met = all(c.met for c in checks)
            parts = [f"[{'✓' if c.met else '✗'}] {c.justification}" for c in checks]
            justification = (
                f"（多点答案，judge 拆为 {len(checks)} 点，全部满足才算 met）\n"
                + "\n".join(parts)
            )[:4000]
            return [
                NLAssertionCheck(
                    nl_assertion=assertion, met=met, justification=justification
                )
            ]

        # 多断言：按输入顺序严格对齐，缺失项显式计为失败
        remaining = list(checks)
        aligned: list[NLAssertionCheck] = []
        for assertion in nl_assertions:
            match_idx = next(
                (
                    idx
                    for idx, check in enumerate(remaining)
                    if check.nl_assertion == assertion
                ),
                None,
            )
            if match_idx is None:
                aligned.append(
                    NLAssertionCheck(
                        nl_assertion=assertion,
                        met=False,
                        justification="Judge did not return a result for this assertion.",
                    )
                )
            else:
                aligned.append(remaining.pop(match_idx))
        return aligned

    @classmethod
    def evaluate_nl_assertions(
        cls,
        trajectory: list[Message],
        nl_assertions: list[str],
    ) -> list[NLAssertionCheck]:
        """
        Evaluate whether the trajectory meets each expected outcome.

        Args:
            trajectory: List of messages from the conversation
            nl_assertions: List of natural-language assertions to evaluate

        Returns:
            List of evaluation results for each NL assertion, containing:
            - nl_assertion: The NL assertion being evaluated
            - metExpectation: Boolean indicating if the assertion was met
            - reasoning: Explanation for the evaluation
        """
        trajectory_str = "\n".join(
            [f"{message.role}: {message.content}" for message in trajectory]
        )
        # System prompt similar to the TypeScript implementation
        system_prompt = """
        TASK
        - You will be given a list of expected outcomes and a conversation that was collected during a test case run.
        - The conversation is between an agent and a customer.
        - Your job is to evaluate whether the agent satisfies each of the expected outcomes.
        - Grade each expected outcome individually.

        FORMAT
        - Your response should be a JSON object with the following fields:
        - `reasoning`: a short explanation for your classification
        - `metExpectation`: `true` if the agent satisfies the expected outcomes, `false` otherwise
        - `expectedOutcome`: repeat the expectation from the input that you are grading
        
        Example response structure:
        {
            "results": [
                {
                    "expectedOutcome": "<one of the expected outcomes from the input>",
                    "reasoning": "<reasoning trace>",
                    "metExpectation": <false or true>,
                }
            ]
        }
        """

        user_prompt = f"""
        conversation:
        {trajectory_str}
        
        expectedOutcomes:
        {nl_assertions}
        """

        messages = [
            SystemMessage(role="system", content=system_prompt),
            UserMessage(role="user", content=user_prompt),
        ]

        # 获取配置
        llm_config = cls._get_llm_config()
        
        assistant_message = generate(
            model=llm_config.get("model", DEFAULT_LLM_NL_ASSERTIONS),
            messages=messages,
            role='evaluator',
            provider=llm_config.get("provider", "auto"),
            llm_config=llm_config,
            **DEFAULT_LLM_NL_ASSERTIONS_ARGS,
        )
        try:
            result_data = json.loads(assistant_message.content)
        except:
            result_data = {"results": []}
        checks: list[NLAssertionCheck] = []
        for idx, result in enumerate(result_data.get("results", [])):
            if not isinstance(result, dict):
                continue

            expected_outcome = result.get("expectedOutcome")
            if not expected_outcome and idx < len(nl_assertions):
                expected_outcome = nl_assertions[idx]
            if not expected_outcome:
                continue

            checks.append(
                NLAssertionCheck(
                    nl_assertion=expected_outcome,
                    met=bool(result.get("metExpectation", False)),
                    justification=result.get("reasoning", "Judge result missing reasoning."),
                )
            )

        return checks
