"""端到端 Pipeline：分组 → 批量生成 → 验证（batch_generate）。"""
import asyncio
import json
import os
import pickle
import random
import threading
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from loguru import logger
from omegaconf import OmegaConf

from bench.data_model.message import UserMessage
from bench.environment.toolkit import ToolKitBase, get_tool_signatures
from bench.utils.llm_utils import extract_json_from_llm_response, generate

from .dedup import deduplicate_tasks
from .generator import TaskGenerator
from .llm_judge import judge_task
from .verifier import _parse_tool_chain, verify_task


# ──────────────────────────────────────────────
# 工具分组（Survey）
# ──────────────────────────────────────────────

_SURVEY_PROMPT = """你是一个企业办公系统架构专家。请将提供的工具列表重新分组，用于构建 Agent 评测数据集（Benchmark）。

分组原则：
1. 任务导向（Task-Oriented）：每个组必须能够覆盖一个“端到端的复杂任务场景”。
2. 边界模糊化（Cross-Domain）：允许同一个组内出现不同业务领域（如HR、财务、行政）的工具，因为一个复杂任务通常涉及多系统协作。
3. 状态变迁链路（State Transition）：优先考虑“查询 -> 判断 -> 执行 -> 验证”这种完整的逻辑链路。
4. 包含“异常与补救”：每个组应包含处理该业务可能产生的异常逻辑（如：查询失败、申请被驳回、信息缺失后的转人工）。
{cross_domain_note}

输出结构：
{{
  "scenarios": [
    {{
      "scenario_name": "任务场景名称 (例如：全自动离职结算与档案归档)",
      "complexity_level": "High/Medium/Low",
      "tools": ["涉及的所有跨领域工具"],
      "tables": ["涉及的底层数据库表"],
      "reasoning": "解释为什么这些工具组合在一起可以构建复杂的 Agent 测试用例"
    }}
  ]
}}

=== 工具列表 ===
{tool_list}

=== 数据库表名 ===
{table_names}
"""


def _survey_groups(
    model: str,
    llm_config: Dict[str, Any],
    toolkit: ToolKitBase,
) -> List[Dict[str, Any]]:
    """一次 LLM 调用完成工具分组。"""
    sigs = get_tool_signatures(toolkit)
    tool_list = "\n".join(f"- {name}: {sig.doc}" for name, sig in sigs.items())
    table_names = ", ".join(toolkit.db.model_dump().keys())

    cross_domain_note = ""
    if getattr(toolkit, "is_cross_domain", False):
        cross_domain_note = (
            "\n5. 跨域约束（Cross-Domain-Required）：每个分组尽量覆盖至少两个业务域，"
            "并包含跨域衔接工具链（例如 HR->IT->ADMIN）。"
        )
    prompt = _SURVEY_PROMPT.format(
        tool_list=tool_list,
        table_names=table_names,
        cross_domain_note=cross_domain_note,
    )
    logger.debug(f"[Pipeline] Survey Prompt: {prompt}")
    # 流式：长 Survey 输出时持续有数据可读，减轻网关/客户端「整包等待」超时
    resp = generate(
        model=model,
        messages=[UserMessage(content=prompt)],
        llm_config=llm_config,
        stream=True,
    )
    logger.debug(f"[Pipeline] Survey Response: {resp.content}")
    try:
        result = extract_json_from_llm_response(resp.content)
        if not isinstance(result, dict):
            raise ValueError("Survey 输出不是 JSON 对象")
        # 兼容三种格式：scenarios / business_capabilities / groups
        raw = result.get("scenarios", result.get("business_capabilities", result.get("groups", [])))
        # 统一归一化为 {name, tools, tables, description} 格式
        groups = []
        for item in raw:
            groups.append({
                "name": item.get("scenario_name", item.get("name", "")),
                "tools": item.get("tools", []),
                "tables": item.get("tables", []),
                "description": item.get("reasoning", item.get("description", "")),
            })
        return groups
    except Exception:
        # 兜底：所有工具一组
        return [{"name": "全量", "tools": list(sigs.keys()), "tables": list(toolkit.db.model_dump().keys())}]


# 基础查询工具：跨所有业务组复用，仅用于定位人员/组织，不能是任务核心目标
_BASE_TOOLS: frozenset = frozenset({
    "find_employee_ref_by_name", "get_employee_details", "search_employees",
    "list_employees", "get_employee_manager_chain", "list_direct_reports",
    "list_employee_teams", "list_employee_departments",
    "get_department_details", "list_departments", "list_department_members",
    "find_department_ref_by_name", "get_position_details", "list_positions",
    "get_team_details", "list_teams", "list_team_members", "find_team_ref_by_name",
    "find_role_ref_by_name",
})

# 输出与排序时 L1/L2/L3 的稳定顺序
_LEVEL_ORDER: Dict[str, int] = {"L1": 0, "L2": 1, "L3": 2}


def _is_base_only_group(group: Dict[str, Any]) -> bool:
    """判断一个组是否仅包含基础查询工具（不应单独用于任务生成）。"""
    tools = set(group.get("tools") or [])
    return bool(tools) and tools.issubset(_BASE_TOOLS)


def _merge_groups(groups: List[Dict[str, Any]], n: int = 2) -> Dict[str, Any]:
    """随机合并 n 个闭环组的工具和数据表，用于跨闭环任务生成。"""
    selected = random.sample(groups, min(n, len(groups)))
    merged_tools: List[str] = []
    merged_tables: List[str] = []
    names = []
    for g in selected:
        merged_tools.extend(g.get("tools", []))
        merged_tables.extend(g.get("tables", []))
        names.append(g["name"])
    return {
        "name": " × ".join(names),
        "tools": list(dict.fromkeys(merged_tools)),
        "tables": list(dict.fromkeys(merged_tables)),
    }


def _inject_base_tools(group: Dict[str, Any]) -> Dict[str, Any]:
    """将基础工具注入到分组工具列表中（保序，不重复）。"""
    tools = group.get("tools") or []
    all_tools = list(dict.fromkeys(list(_BASE_TOOLS) + tools))
    return {**group, "tools": all_tools}


def _load_cached_groups(cache_path: str) -> Optional[List[Dict[str, Any]]]:
    """从缓存加载分组结果。支持 exploration_result.json 和 survey-result.pkl。"""
    if not cache_path or not os.path.exists(cache_path):
        return None

    if cache_path.endswith(".json"):
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
        if "groups" in data and isinstance(data["groups"], list):
            return [
                {
                    "name": g.get("group_name", g.get("name", "")),
                    "tools": g.get("tools", []),
                    "tables": g.get("tables", []),
                    "description": g.get("description", ""),
                }
                for g in data["groups"]
            ]
        return None

    if cache_path.endswith(".pkl"):
        with open(cache_path, "rb") as f:
            survey = pickle.load(f)
        return survey.get("groups", [])

    return None


def _sorted_target_levels(target_counts: Dict[str, int]) -> List[str]:
    """按 L1→L2→L3 顺序返回 target_counts 中出现的级别键。"""
    keys = [k for k in target_counts if target_counts[k] > 0]
    return sorted(keys, key=lambda k: _LEVEL_ORDER.get(k, 99))


def _init_generation_level_stats(levels: List[str], target_counts: Dict[str, int], n_groups: int) -> Dict[str, Dict[str, Any]]:
    """初始化批量生成阶段的分级统计容器。"""
    stats: Dict[str, Dict[str, Any]] = {}
    for level in levels:
        stats[level] = {
            "planned_slots": int(target_counts.get(level, 0)) * n_groups,
            "success_slots": 0,
            "failed_slots": 0,
            "generator_fail_count": 0,
            "verify_fail_count": 0,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "logic_sum": 0.0,
            "naturalness_sum": 0.0,
            "difficulty_sum": 0.0,
            "score_sum": 0.0,
            "score_count": 0,
            "error_count": 0,
        }
    return stats


def _accumulate_judge_stats(level_stat: Dict[str, Any], passed_judge: bool, judge_result: Dict[str, Any]) -> None:
    """累计一次 LLM Judge 的统计结果（含失败样本）。"""
    level_stat["total"] += 1
    level_stat["passed"] += 1 if passed_judge else 0
    level_stat["failed"] += 0 if passed_judge else 1

    logic = judge_result.get("logic_score")
    naturalness = judge_result.get("naturalness_score")
    difficulty = judge_result.get("difficulty_score")
    if not all(isinstance(x, (int, float)) for x in (logic, naturalness, difficulty)):
        level_stat["error_count"] += 1
        return

    logic = float(logic)
    naturalness = float(naturalness)
    difficulty = float(difficulty)
    level_stat["logic_sum"] += logic
    level_stat["naturalness_sum"] += naturalness
    level_stat["difficulty_sum"] += difficulty
    level_stat["score_sum"] += (logic + naturalness + difficulty) / 3.0
    level_stat["score_count"] += 1


def _finalize_generation_stats(
    *,
    name: str,
    output_path: Optional[str],
    task_count: int,
    levels: List[str],
    generation_stats: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """将生成期统计整理为可落盘 JSON。"""
    levels_result: Dict[str, Dict[str, Any]] = {}
    for level in ("L1", "L2", "L3"):
        st = generation_stats.get(level)
        if st is None:
            levels_result[level] = {
                "planned_slots": 0,
                "success_slots": 0,
                "failed_slots": 0,
                "generator_fail_count": 0,
                "verify_fail_count": 0,
                "total": 0,
                "passed": 0,
                "failed": 0,
                "pass_rate": 0.0,
                "filter_rate": 0.0,
                "avg_logic": None,
                "avg_naturalness": None,
                "avg_difficulty": None,
                "avg_score_5": None,
                "avg_score_100": None,
                "score_count": 0,
                "error_count": 0,
            }
            continue

        total = st["total"]
        passed = st["passed"]
        failed = st["failed"]
        score_count = st["score_count"]
        levels_result[level] = {
            "planned_slots": st["planned_slots"],
            "success_slots": st["success_slots"],
            "failed_slots": st["failed_slots"],
            "generator_fail_count": st["generator_fail_count"],
            "verify_fail_count": st["verify_fail_count"],
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) if total else 0.0,
            "filter_rate": (failed / total) if total else 0.0,
            "avg_logic": (st["logic_sum"] / score_count) if score_count else None,
            "avg_naturalness": (st["naturalness_sum"] / score_count) if score_count else None,
            "avg_difficulty": (st["difficulty_sum"] / score_count) if score_count else None,
            "avg_score_5": (st["score_sum"] / score_count) if score_count else None,
            "avg_score_100": ((st["score_sum"] / score_count) * 20) if score_count else None,
            "score_count": score_count,
            "error_count": st["error_count"],
        }

    planned_slots = sum(generation_stats.get(level, {}).get("planned_slots", 0) for level in levels)
    success_slots = sum(generation_stats.get(level, {}).get("success_slots", 0) for level in levels)
    failed_slots = sum(generation_stats.get(level, {}).get("failed_slots", 0) for level in levels)
    generator_fail_count = sum(generation_stats.get(level, {}).get("generator_fail_count", 0) for level in levels)
    verify_fail_count = sum(generation_stats.get(level, {}).get("verify_fail_count", 0) for level in levels)
    total = sum(generation_stats.get(level, {}).get("total", 0) for level in levels)
    passed = sum(generation_stats.get(level, {}).get("passed", 0) for level in levels)
    failed = sum(generation_stats.get(level, {}).get("failed", 0) for level in levels)
    score_count = sum(generation_stats.get(level, {}).get("score_count", 0) for level in levels)
    score_sum = sum(generation_stats.get(level, {}).get("score_sum", 0.0) for level in levels)

    return {
        "name": name,
        "path": output_path or "",
        "task_count": task_count,
        "levels": levels_result,
        "overall": {
            "planned_slots": planned_slots,
            "success_slots": success_slots,
            "failed_slots": failed_slots,
            "generator_fail_count": generator_fail_count,
            "verify_fail_count": verify_fail_count,
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total) if total else 0.0,
            "filter_rate": (failed / total) if total else 0.0,
            "avg_score_5": (score_sum / score_count) if score_count else None,
            "avg_score_100": ((score_sum / score_count) * 20) if score_count else None,
            "score_count": score_count,
        },
    }


def _extract_task_tools(task: Dict[str, Any]) -> List[str]:
    try:
        calls = _parse_tool_chain(task.get("answer", ""))
        return [str(item.get("name", "")) for item in calls if isinstance(item, dict) and item.get("name")]
    except Exception:
        return []


def _build_coverage_report(tasks: List[Dict[str, Any]], toolkit: ToolKitBase) -> Dict[str, Any]:
    all_tools = set(get_tool_signatures(toolkit).keys())
    all_tables = set(toolkit.db.model_dump().keys())
    tool_counter: Counter[str] = Counter()
    table_counter: Counter[str] = Counter()
    level_counter: Counter[str] = Counter()

    for task in tasks:
        level_counter[str(task.get("level", "UNKNOWN")).upper()] += 1
        for name in _extract_task_tools(task):
            tool_counter[name] += 1
        tables = (task.get("metadata") or {}).get("table_subset") or []
        if isinstance(tables, list):
            for table in tables:
                table_counter[str(table)] += 1

    return {
        "tool_usage": dict(sorted(tool_counter.items(), key=lambda kv: kv[0])),
        "table_usage": dict(sorted(table_counter.items(), key=lambda kv: kv[0])),
        "unused_tools": sorted(all_tools - set(tool_counter.keys())),
        "unused_tables": sorted(all_tables - set(table_counter.keys())),
        "level_distribution": dict(sorted(level_counter.items(), key=lambda kv: kv[0])),
    }


# ──────────────────────────────────────────────
# Pipeline 主类
# ──────────────────────────────────────────────

class TaskGenPipeline:
    """GAIA 风格任务生成 Pipeline。

    用法：
        pipeline = TaskGenPipeline.from_config("configs/app.yaml", toolkit)
        # target_counts：每个分组在各级别要生成的任务数（非全库合计）
        tasks = pipeline.batch_generate(
            target_counts={"L1": 5, "L2": 5, "L3": 5},
            max_concurrent=5,
        )
    """

    def __init__(self, model: str, llm_config: Dict[str, Any], toolkit: ToolKitBase, domain: str = "HR"):
        self.model = model
        self.llm_config = llm_config
        self.toolkit = toolkit
        self.domain = domain
        self.generator = TaskGenerator(model, llm_config, toolkit, domain=domain)
        self._groups: Optional[List[Dict[str, Any]]] = None
        self.last_generation_stats: Optional[Dict[str, Any]] = None

    def get_groups(self, cache_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取工具分组（优先缓存 → LLM survey）。"""
        if self._groups:
            return self._groups

        if cache_path:
            cached = _load_cached_groups(cache_path)
            if cached:
                self._groups = cached
                logger.info(f"[Pipeline] 从缓存加载 {len(cached)} 个分组")
                return self._groups

        logger.info("[Pipeline] 执行 LLM survey 分组...")
        all_groups = _survey_groups(self.model, self.llm_config, self.toolkit)
        # 过滤掉纯基础查询组，它们的工具会通过 _inject_base_tools 注入到其他组
        self._groups = [g for g in all_groups if not _is_base_only_group(g)]
        logger.info(f"[Pipeline] 分组完成：{len(self._groups)} 组（已过滤纯查询组）")

        # 将结果写入缓存文件，下次直接读取跳过 LLM 调用
        if cache_path and cache_path.endswith(".json"):
            os.makedirs(os.path.dirname(os.path.abspath(cache_path)), exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({"groups": self._groups}, f, ensure_ascii=False, indent=2)
            logger.info(f"[Pipeline] 分组结果已缓存至 {cache_path}")

        return self._groups

    def _resolve_gen_group(self, level: str, group: Dict[str, Any], all_groups: List[Dict[str, Any]]) -> Dict[str, Any]:
        """L3 跨闭环合并多组；其余难度使用当前业务组。"""
        if level == "L3" and len(all_groups) > 1:
            gen_group = _merge_groups(all_groups, n=3)
        else:
            gen_group = group
        return _inject_base_tools(gen_group)

    def _sync_generate_slot(
        self,
        level: str,
        group: Dict[str, Any],
        all_groups: List[Dict[str, Any]],
        max_retry: int,
        generation_stats: Optional[Dict[str, Dict[str, Any]]] = None,
        stats_lock: Optional[threading.Lock] = None,
    ) -> Optional[Dict[str, Any]]:
        """单槽位：带重试的生成 + 验证 + 质检，成功返回任务 dict，否则 None。"""
        level_stat = generation_stats.get(level) if generation_stats else None

        def _update_stat(update_func) -> None:
            if level_stat is None:
                return
            if stats_lock is None:
                update_func(level_stat)
                return
            with stats_lock:
                update_func(level_stat)

        gen_group = self._resolve_gen_group(level, group, all_groups)
        for _ in range(max_retry):
            task = self.generator.generate_one(
                level=level,
                tool_names=gen_group.get("tools"),
                table_names=gen_group.get("tables"),
                base_tool_names=list(_BASE_TOOLS),
            )
            if task is None:
                _update_stat(lambda st: st.__setitem__("generator_fail_count", st["generator_fail_count"] + 1))
                continue
            passed_verify, errors = verify_task(task, self.toolkit)
            if not passed_verify:
                logger.debug(f"[Batch] 验证失败: {errors}")
                _update_stat(lambda st: st.__setitem__("verify_fail_count", st["verify_fail_count"] + 1))
                continue

            passed_judge, judge_result = judge_task(task, self.model, self.llm_config)
            _update_stat(lambda st: _accumulate_judge_stats(st, passed_judge, judge_result))
            if not passed_judge:
                logger.debug(f"[Batch] 质检不通过: {judge_result.get('comments', '')}")
                continue

            task["domain"] = self.domain
            task["verified"] = True
            task["judge_result"] = judge_result
            task["metadata"]["group"] = gen_group["name"]
            _update_stat(lambda st: st.__setitem__("success_slots", st["success_slots"] + 1))
            return task
        logger.warning(f"[Batch] {level} @ {group.get('name', '?')} 生成失败（已重试 {max_retry} 次）")
        _update_stat(lambda st: st.__setitem__("failed_slots", st["failed_slots"] + 1))
        return None

    def _build_work_items(
        self,
        groups: List[Dict[str, Any]],
        target_counts: Dict[str, int],
    ) -> List[Tuple[int, int, int, Dict[str, Any], str]]:
        """(组序号, 难度序号, 槽位, group, level)，用于稳定排序与并行调度。"""
        items: List[Tuple[int, int, int, Dict[str, Any], str]] = []
        levels = _sorted_target_levels(target_counts)
        for gi, group in enumerate(groups):
            for level in levels:
                n = target_counts[level]
                li = _LEVEL_ORDER.get(level, 99)
                for slot in range(n):
                    items.append((gi, li, slot, group, level))
        return items

    def _build_work_items_from_totals(
        self,
        groups: List[Dict[str, Any]],
        remaining_totals: Dict[str, int],
    ) -> List[Tuple[int, int, int, Dict[str, Any], str]]:
        """按 level 剩余总配额构造任务槽位，保证补生成时分布均衡。"""
        items: List[Tuple[int, int, int, Dict[str, Any], str]] = []
        n_groups = len(groups)
        if n_groups <= 0:
            return items
        for level in _sorted_target_levels(remaining_totals):
            li = _LEVEL_ORDER.get(level, 99)
            count = int(remaining_totals.get(level, 0))
            for idx in range(count):
                gi = idx % n_groups
                slot = idx // n_groups
                items.append((gi, li, slot, groups[gi], level))
        return items

    async def _batch_generate_async(
        self,
        work_items: List[Tuple[int, int, int, Dict[str, Any], str]],
        all_groups: List[Dict[str, Any]],
        max_concurrent: int,
        max_retry: int,
        generation_stats: Dict[str, Dict[str, Any]],
        stats_lock: threading.Lock,
    ) -> List[Tuple[int, int, int, Optional[Dict[str, Any]]]]:
        sem = asyncio.Semaphore(max_concurrent)

        async def bounded(item: Tuple[int, int, int, Dict[str, Any], str]) -> Tuple[int, int, int, Optional[Dict[str, Any]]]:
            gi, li, slot, group, level = item
            async with sem:
                task = await asyncio.to_thread(
                    self._sync_generate_slot,
                    level,
                    group,
                    all_groups,
                    max_retry,
                    generation_stats,
                    stats_lock,
                )
            return gi, li, slot, task

        return list(await asyncio.gather(*(bounded(it) for it in work_items)))

    def batch_generate(
        self,
        target_counts: Optional[Dict[str, int]] = None,
        cache_path: Optional[str] = None,
        max_retry: int = 3,
        max_generation_rounds: int = 3,
        output_path: Optional[str] = None,
        stats_output_path: Optional[str] = None,
        max_concurrent: int = 1,
        dedup_enabled: bool = True,
        dedup_semantic_threshold: float = 0.85,
        dedup_embedding_model: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """批量生成：每个分组在各级别各生成 target_counts[level] 条任务。

        Args:
            target_counts: 每个分组在 L1/L2/L3 上的任务数，例如 {"L1": 5, "L2": 5, "L3": 5}
                表示每组各难度 5 条；全库合计为该数 × 分组数。
            cache_path: 分组缓存路径
            max_retry: 每个槽位最大重试次数
            max_generation_rounds: 难度配额补生成轮次上限
            output_path: 输出 JSON 路径（None 则不保存）
            stats_output_path: 生成期统计输出路径（None 则不落盘）
            max_concurrent: 并发槽位数；1 为串行。>1 时用 asyncio + 线程跑同步 LLM，结果仍按组/难度/槽位排序。
            dedup_enabled: 是否对生成结果做去重
            dedup_semantic_threshold: 语义去重阈值
            dedup_embedding_model: 可选 sentence-transformers embedding 模型名
        """
        if target_counts is None:
            target_counts = {"L1": 2, "L2": 2, "L3": 1}

        if max_concurrent < 1:
            max_concurrent = 1

        groups = self.get_groups(cache_path)
        if not groups:
            logger.warning("[Batch] 无可用分组，跳过生成")
            return []

        n_groups = len(groups)
        levels = _sorted_target_levels(target_counts)
        generation_stats = _init_generation_level_stats(levels, target_counts, n_groups)
        stats_lock = threading.Lock()
        for level in levels:
            c = target_counts[level]
            logger.info(f"[Batch] {level}: 每组 {c} 个 × {n_groups} 组 → 合计 {c * n_groups} 个")

        target_totals = {level: int(target_counts[level]) * n_groups for level in levels}
        success_totals = {level: 0 for level in levels}
        all_tasks: List[Dict[str, Any]] = []

        if max_concurrent > 1:
            logger.info(
                f"[Batch] 并发 max_concurrent={max_concurrent}，"
                "输出顺序按组索引/难度/槽位固定；完成先后与日志时间可能不一致"
            )

        for round_idx in range(1, max(1, max_generation_rounds) + 1):
            remaining_totals = {
                level: max(0, target_totals[level] - success_totals[level])
                for level in levels
            }
            if not any(remaining_totals.values()):
                break

            logger.info(f"[Batch] 配额补生成 round={round_idx}，remaining={remaining_totals}")
            work_items = self._build_work_items_from_totals(groups, remaining_totals)
            if not work_items:
                break

            if max_concurrent <= 1:
                round_results: List[Tuple[int, int, int, Optional[Dict[str, Any]]]] = []
                for it in work_items:
                    gi, li, slot, group, level = it
                    task = self._sync_generate_slot(
                        level, group, groups, max_retry, generation_stats, stats_lock
                    )
                    round_results.append((gi, li, slot, task))
            else:
                round_results = asyncio.run(
                    self._batch_generate_async(
                        work_items, groups, max_concurrent, max_retry, generation_stats, stats_lock
                    )
                )

            round_results.sort(key=lambda x: (x[0], x[1], x[2]))
            round_tasks = [t for (_, _, _, t) in round_results if t is not None]
            all_tasks.extend(round_tasks)
            for task in round_tasks:
                level = str(task.get("level", "")).upper()
                if level in success_totals:
                    success_totals[level] += 1

        for level in levels:
            planned = target_totals[level]
            done = success_totals[level]
            logger.info(f"[Batch] {level}: 计划 {planned}，成功 {done}")

        if dedup_enabled and all_tasks:
            deduped, dedup_report = deduplicate_tasks(
                all_tasks,
                semantic_threshold=dedup_semantic_threshold,
                embedding_model=dedup_embedding_model,
            )
            logger.info(
                f"[Batch] 去重完成：{len(all_tasks)} -> {len(deduped)} "
                f"(结构去重={dedup_report.removed_structural}, 语义去重={dedup_report.removed_semantic})"
            )
            all_tasks = deduped
        else:
            dedup_report = None

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_tasks, f, ensure_ascii=False, indent=2)
            logger.info(f"[Batch] {len(all_tasks)} 个任务已写入 {output_path}")

        generation_summary = _finalize_generation_stats(
            name="generated",
            output_path=output_path,
            task_count=len(all_tasks),
            levels=levels,
            generation_stats=generation_stats,
        )
        generation_summary["coverage"] = _build_coverage_report(all_tasks, self.toolkit)
        if dedup_report is not None:
            generation_summary["dedup"] = dedup_report.to_dict()
        self.last_generation_stats = generation_summary

        for level in ("L1", "L2", "L3"):
            stat = generation_summary["levels"][level]
            if stat["planned_slots"] <= 0:
                continue
            logger.info(
                f"[Batch] {level}: judge总数={stat['total']}, 通过={stat['passed']}, "
                f"丢弃={stat['failed']}, 丢弃率={stat['filter_rate'] * 100:.2f}%, "
                f"槽位成功={stat['success_slots']}/{stat['planned_slots']}"
            )

        if stats_output_path:
            os.makedirs(os.path.dirname(os.path.abspath(stats_output_path)), exist_ok=True)
            with open(stats_output_path, "w", encoding="utf-8") as f:
                json.dump({"generated": generation_summary}, f, ensure_ascii=False, indent=2)
            logger.info(f"[Batch] 生成期统计已写入 {stats_output_path}")

        return all_tasks

    @staticmethod
    def from_config(
        config_path: str,
        toolkit: ToolKitBase,
        domain: str = "HR",
    ) -> "TaskGenPipeline":
        """从 configs/app.yaml 加载 LLM 配置并初始化 Pipeline。"""
        load_dotenv()
        cfg = OmegaConf.to_container(OmegaConf.load(config_path), resolve=True)
        llm = cfg.get("synthesis", {}).get("llm", {})
        model = llm.get("model_name") or llm.get("model", "gpt-4o")
        llm_config = {
            "api_key": llm.get("api_key", "dummy"),
            "base_url": llm.get("base_url"),
            "temperature": llm.get("temperature", 0.7),
            "max_tokens": llm.get("max_tokens", 64000),
        }
        return TaskGenPipeline(model=model, llm_config=llm_config, toolkit=toolkit, domain=domain)


if __name__ == "__main__":
    import argparse
    import os

    from bench.domains.admin.environment import get_environment as get_admin_env
    from bench.domains.cross_domain.environment import get_environment as get_cross_env
    from bench.domains.finance.environment import get_environment as get_finance_env
    from bench.domains.hr.environment import get_environment as get_hr_env
    from bench.domains.it.environment import get_environment as get_it_env
    from bench.domains.law.environment import get_environment as get_law_env
    from bench.domains.purchase.environment import get_environment as get_purchase_env
    from bench.domains.work.environment import get_environment as get_work_env

    _ENV_LOADERS = {
        "hr": get_hr_env,
        "it": get_it_env,
        "admin": get_admin_env,
        "finance": get_finance_env,
        "law": get_law_env,
        "purchase": get_purchase_env,
        "work": get_work_env,
        "cross": get_cross_env,
    }

    # 各域的默认分组缓存路径（无则触发 LLM survey）
    _DEFAULT_CACHES: Dict[str, Optional[str]] = { key: f"synthesis/exploration_memory/{key}/exploration_result.json" for key in _ENV_LOADERS.keys() }

    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="hr", choices=list(_ENV_LOADERS), help="业务域")
    parser.add_argument("--cache", default=None, help="分组缓存路径（.json）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认 tasks_{domain}.json）")
    parser.add_argument("--stats-output", default=None, help="生成统计输出路径（可选）")
    parser.add_argument("--max-concurrent", type=int, default=5, help="并发生成槽位数")
    parser.add_argument("--max-rounds", type=int, default=3, help="按难度配额补生成轮次上限")
    parser.add_argument(
        "--cross-domains",
        default=None,
        help="仅在 --domain cross 时生效，指定跨域子集，逗号分隔，例如 hr,it,admin",
    )
    parser.add_argument("--disable-dedup", action="store_true", help="关闭任务去重")
    parser.add_argument("--dedup-threshold", type=float, default=0.85, help="语义去重阈值")
    parser.add_argument("--dedup-embedding-model", default=None, help="可选 sentence-transformers 模型名")
    args = parser.parse_args()

    if args.domain == "cross" and args.cross_domains:
        raw_domains = [item.strip().lower() for item in args.cross_domains.split(",") if item.strip()]
        allowed = {"hr", "it", "admin", "finance", "law", "purchase", "work"}
        invalid = [name for name in raw_domains if name not in allowed]
        if invalid:
            raise ValueError(f"非法 cross domain: {invalid}，允许值: {sorted(allowed)}")
        if not raw_domains:
            raise ValueError("--cross-domains 不能为空")
        env = _ENV_LOADERS["cross"](domains=raw_domains)
    else:
        env = _ENV_LOADERS[args.domain]()
    cache = args.cache or _DEFAULT_CACHES.get(args.domain)
    output = args.output or f"tasks_{args.domain}.json"
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "configs", "app.yaml")
    pipeline = TaskGenPipeline.from_config(config_path, env.tools, domain=args.domain)
    tasks = pipeline.batch_generate(
        target_counts={"L1": 1, "L2": 1, "L3": 1},
        cache_path=cache,
        output_path=output,
        stats_output_path=args.stats_output,
        max_concurrent=max(1, args.max_concurrent),
        max_generation_rounds=max(1, args.max_rounds),
        dedup_enabled=not args.disable_dedup,
        dedup_semantic_threshold=args.dedup_threshold,
        dedup_embedding_model=args.dedup_embedding_model,
    )
    print(tasks)
