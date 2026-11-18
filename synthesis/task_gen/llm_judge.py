"""任务自动化质检器（LLM-as-a-Judge）：评估生成任务的逻辑、自然度与难度。"""
from typing import Any, Dict, Tuple

from bench.data_model.message import UserMessage
from bench.utils.llm_utils import extract_json_from_llm_response, generate
from loguru import logger

_JUDGE_PROMPT = """你是一个严苛的企业级 AI Agent 评测基准质检员。
你的任务是评估大模型生成的“办公求助任务”是否合格。如果不合格，请严格打低分。

=== 待评估任务信息 ===
难度级别：{level}
提问者：{caller_name}
业务背景 (Scenario)：{scenario}
生成的问题 (Question)：{question}
生成的工具链 (Answer)：{answer}
设计推理过程 (Reasoning)：{reasoning}

=== 评估维度（每项 1-5 分，5分为极佳） ===
1. 逻辑与防作弊 (logic_score)
   - 致命错误：用到 `calculate` 时，里面的数字是否凭空捏造（没有在前置查询工具的返回结果中出现）？如果是，打 1 分。
   - 致命错误：整个question的逻辑性是否顺畅？
2. 自然度与“班味” (naturalness_score)
   - Question 是否像真实的互联网职场人类提问？是否有自然的沟通感？问题是否符合职场逻辑？
   - 致命错误：包含指令泄露（如“视情况而定”、“跨实体”、“条件链”、“聚合”），这会让人觉得像机器人在读题。
   - 致命错误：暴露系统底层（念出表名、字段名、JSON键、工具名或直接报内部ID如 EMP001，但是某些字段适当允许）。
3. 难度对齐 (difficulty_score)
   - 是否符合其 Level 的复杂度？
   - L1 必须是纯线性、单意图；L2 必须有业务因果/依赖关系；L3 必须有宏观盘点/聚合的感觉，而非生硬地缝合几个不相干的 L1 任务。
   
=== 输出要求 ===
请严格以 JSON 格式输出，包含四项得分和一条总评。只有当 logic, naturalness, difficulty 的得分 **全部 >= 4** 时，才算合格 (is_passed = true)：
{{
    "logic_score": int,
    "naturalness_score": int,
    "difficulty_score": int,
    "comments": "简短的扣分理由或肯定评价",
    "is_passed": boolean
}}
特别注意：JSON 字符串（尤其 comments）内部禁止使用未转义的 ASCII 双引号 "。
如需引用短语，请改用中文引号「」或“”；不要输出 Markdown 代码块。
"""

def judge_task(
    task: Dict[str, Any], 
    model: str, 
    llm_config: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any]]:
    """调用 LLM 对生成的任务进行打分质检。"""
    
    prompt = _JUDGE_PROMPT.format(
        level=task.get("level", "Unknown"),
        caller_name=task.get("caller", {}).get("display_name", "Unknown"),
        scenario=task.get("business_scenario", "N/A"),
        question=task.get("question", ""),
        answer=task.get("answer", ""),
        reasoning=task.get("reasoning", "")
    )
    
    try:
        resp = generate(model=model, messages=[UserMessage(content=prompt)], llm_config=llm_config)
        result = extract_json_from_llm_response(resp.content)
        if not isinstance(result, dict):
            raise ValueError("Judge 输出不是 JSON 对象")
        
        # 二次保险计算 is_passed
        logic = result.get("logic_score", 0)
        natural = result.get("naturalness_score", 0)
        diff = result.get("difficulty_score", 0)
        
        passed = (logic >= 4 and natural >= 4 and diff >= 4)
        result["is_passed"] = passed
        
        return passed, result
    except Exception as e:
        logger.error(f"[LLM Judge] 评估请求失败: {e}")
        return False, {"is_passed": False, "comments": f"Request Error: {str(e)}"}