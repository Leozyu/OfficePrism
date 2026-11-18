"""DB 文案分:golden 工具链含自由文本字段时,用 evaluator LLM 判 agent 写入的文本是否合格。

口径(与 scripts/rescore_db_freetext_set420.py 一致):
- 只对 golden 工具链里含中文自由文本字段(SOFT_KEYS)的写调用生效;无则跳过(退化为纯结构分)。
- 配对: golden 写调用 → agent 同名工具调用中「非软字段硬参数最匹配」的一条,取其对应软字段值。
- 判定: 摊平全部 (工具,字段,golden值,agent值) 条目,一次 LLM judge 逐条判 0/1,全过(AND)才给 1。
  仅罚 写错/捏造事实、意图与参考不一致、核心对象无法辨认、未填写;详略与措辞差异不罚。
- 全部 agent 值为空 → 直接判 0,不调 LLM。

结构分侧的软字段哈希豁免由 evaluator_env 在模块加载时把 SOFT_KEYS 并入 toolkit._UNSTABLE_FIELDS 完成;
db_status = 结构分 × 文案分。
"""
import json
import re
import time

from bench.data_model.message import SystemMessage, UserMessage
from bench.data_model.tasks import Task

# 自由文本软字段:agent 自由填写,golden 用占位/示例文本,无法精确哈希匹配,改由 LLM 判文案。
SOFT_KEYS = {
    "title", "description", "subject", "reason", "summary", "accomplishments",
    "issues_and_risks", "next_period_plan", "risk_description", "mitigation_plan",
    "diagnosis", "resolution", "business_justification", "additional_info", "purpose",
    "review_scope", "review_title", "risk_title", "affected_clause", "report_title",
    "comment", "manager_comment", "notes", "bio",
}

_CJK = re.compile(r"[一-鿿]")


def extract_gold_soft_fields(task: Task):
    """从 golden 工具链(evaluation_criteria.actions)提取含中文自由文本的软字段。

    返回 [(tool_name, full_kwargs, {soft_key: gold_val})];为空表示该任务无自由文本,应跳过文案判定。
    """
    if task.evaluation_criteria is None or not task.evaluation_criteria.actions:
        return []
    fields = []
    for action in task.evaluation_criteria.actions:
        kwargs = action.arguments or {}
        softs = {k: v for k, v in kwargs.items()
                 if k in SOFT_KEYS and isinstance(v, str) and _CJK.search(v)}
        if softs:
            fields.append((action.name, kwargs, softs))
    return fields


def _unwrap_tool_call(tc):
    """还原 search 模式的 discovery 元工具包装:
    call_tool(name=真实工具, arguments={...}) → (真实工具名, 真实参数)。
    full 模式直接调用则原样返回。"""
    args = tc.arguments or {}
    if tc.name == "call_tool" and isinstance(args.get("arguments"), dict):
        return str(args.get("name") or ""), args["arguments"]
    return tc.name, args


def _match_agent_value(gold_tool, gold_kwargs, soft_key, predicted_tool_calls):
    """在 agent 实际调用里找与该 golden 写调用对应的一条(同名工具、非软字段硬参数最匹配),取其软字段值。"""
    best, best_score = None, -1
    for tc in predicted_tool_calls:
        name, args = _unwrap_tool_call(tc)
        if name != gold_tool:
            continue
        score = sum(1 for k, v in gold_kwargs.items()
                    if k not in SOFT_KEYS and args.get(k) == v)
        if score > best_score:
            best, best_score = args, score
    if best is None:
        return ""
    return str(best.get(soft_key, "") or "")


def judge_db_text(task: Task, predicted_tool_calls, llm_config, details_out=None) -> float:
    """返回文案分 0/1。无软字段返回 1.0(不触发);全空返回 0.0;否则一次 LLM judge 逐条 AND。

    details_out: 传入 list 时,追加逐条判定明细
    {tool, field, gold, agent, pass, reason},用于结果落盘与错误归因。
    """
    from bench.utils.llm_utils import generate

    fields = extract_gold_soft_fields(task)
    if not fields:
        return 1.0

    items = []  # (tool, key, gold_val, agent_val)
    for tool, gold_kwargs, softs in fields:
        for key, gold_val in softs.items():
            agent_val = _match_agent_value(tool, gold_kwargs, key, predicted_tool_calls)
            items.append((tool, key, gold_val, agent_val))

    if all(not av for _, _, _, av in items):
        if details_out is not None:
            details_out.extend(
                {"tool": n, "field": k, "gold": gv, "agent": av,
                 "pass": 0, "reason": "agent 未填写任何自由文本字段"}
                for n, k, gv, av in items)
        return 0.0

    lines = [f"{i}. 工具{n} 字段{k}\n   参考: {gv}\n   agent: {av or '(未填写)'}"
             for i, (n, k, gv, av) in enumerate(items, 1)]
    question = ""
    if task.description is not None and task.description.purpose:
        question = task.description.purpose
    prompt = (
        "任务背景(用户请求):\n" + question +
        "\n\n判断 agent 写入系统记录的自由文本是否合格。判0的条件仅限:"
        "①事实写错或捏造(编号/人名/日期/数量/状态与参考或背景矛盾);"
        "②意图与参考不一致(不是同一件事/诉求);③核心对象无法辨认;④未填写。"
        "详略差异、省略部分细节、措辞不同、补充正确的额外信息 → 都判1。\n\n" +
        "\n".join(lines) +
        "\n\n只输出JSON: {\"results\":[{\"idx\":1,\"pass\":0或1,\"reason\":\"一句话判定理由\"},...]}"
    )
    cfg = llm_config or {}
    for _ in range(3):
        try:
            msg = generate(
                model=cfg.get("model"),
                messages=[SystemMessage(role="system", content="你是严格但公允的评测员,只输出JSON。"),
                          UserMessage(role="user", content=prompt)],
                llm_config=cfg, temperature=0)
            m = re.search(r"\{.*\}", msg.content or "", re.S)
            res = json.loads(m.group(0))["results"]
            ok = len(res) == len(items) and all(int(x.get("pass", 0)) == 1 for x in res)
            if details_out is not None:
                for i, (n, k, gv, av) in enumerate(items):
                    r = res[i] if i < len(res) else {}
                    details_out.append(
                        {"tool": n, "field": k, "gold": gv, "agent": av,
                         "pass": int(r.get("pass", 0)),
                         "reason": str(r.get("reason", ""))})
            return 1.0 if ok else 0.0
        except Exception:  # noqa: BLE001 —— 重试兜底,最终失败向上层暴露为文案分不可得
            time.sleep(2)
    raise RuntimeError("db_text judge failed after 3 retries")
