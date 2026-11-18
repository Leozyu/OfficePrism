import ast
import json
import os
import re
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple, Union

from loguru import logger


def save_generated_file(path: str, content: str):
    """保存生成的代码或 JSON"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def load_json(path: str) -> Any:
    """加载 JSON 文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_code_block(response: str) -> str:
    """从 LLM 响应中提取 ``` 包裹的代码块，无代码块则返回原文本"""
    pattern = r'```(?:\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, response, re.DOTALL)
    return matches[0].strip() if matches else response.strip()


def verify_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """验证 Python 代码语法，返回 (是否有效, 错误信息)"""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"第 {e.lineno} 行：{e.msg}"
    except Exception as e:
        return False, str(e)


def verify_json_structure(data_str: str) -> Tuple[bool, Union[Dict[Any, Any], str]]:
    """验证 JSON 格式，返回 (是否有效, 解析结果或错误信息)"""
    try:
        res = json.loads(data_str)
        return True, res
    except json.JSONDecodeError as e:
        return False, f"第 {e.lineno} 列 {e.colno}：{e.msg}"
    except Exception as e:
        return False, str(e)


def parse_ref_fields(model_code: str, db_class=None) -> Dict[str, List[Tuple[str, str]]]:
    """
    从 model 代码中解析外键引用字段（*_ref / *_refs）及其目标表。

    Returns:
        Dict[table_name, List[(ref_field, target_table)]]
        例如: {"assets": [("department_ref", "departments")], ...}
    """
    ref_map = {}
    class_pattern = r'class\s+(\w+)\(BaseModel\):'
    field_pattern = r'(\w+_refs?)\s*:\s*(?:Optional\[)?(?:str|List\[str\])'

    classes = re.findall(class_pattern, model_code)
    for class_name in classes:
        if class_name.endswith('DB'):
            continue
        class_block_pattern = rf'class\s+{class_name}\(BaseModel\):.*?(?=class\s+\w+|$)'
        class_match = re.search(class_block_pattern, model_code, re.DOTALL)
        if not class_match:
            continue
        class_block = class_match.group(0)
        ref_fields = re.findall(field_pattern, class_block)
        if ref_fields:
            table_name = _class_to_table_name(class_name)
            ref_map[table_name] = [
                (ref_field, _ref_field_to_table_name(ref_field))
                for ref_field in ref_fields
            ]
    return ref_map


def _class_to_table_name(class_name: str) -> str:
    """将 PascalCase 类名转换为 snake_case 复数表名，例如 Asset -> assets"""
    name = class_name.lower()
    if name.endswith('y') and name[-2] not in 'aeiou':
        return name[:-1] + 'ies'
    elif name.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return name + 'es'
    elif name.endswith('is'):
        return name[:-2] + 'es'
    else:
        return name + 's'


def _ref_field_to_table_name(ref_field: str) -> str:
    """从引用字段名推导目标表名，例如 department_ref -> departments"""
    if ref_field.endswith('_refs'):
        base = ref_field[:-5]
    elif ref_field.endswith('_ref'):
        base = ref_field[:-4]
    else:
        base = ref_field

    if base.endswith('y') and base[-2] not in 'aeiou':
        return base[:-1] + 'ies'
    elif base.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return base + 'es'
    elif not base.endswith('s'):
        return base + 's'
    else:
        return base


def topological_sort(tables: List[str], ref_map: Dict[str, List[Tuple[str, str]]]) -> List[str]:
    """
    按外键依赖对表做拓扑排序，父表排在前面。

    Args:
        tables: 所有表名列表
        ref_map: parse_ref_fields 返回的依赖映射
    """
    dependencies = defaultdict(set)
    in_degree = {table: 0 for table in tables}

    for table, refs in ref_map.items():
        if table not in tables:
            continue
        for _, target_table in refs:
            if target_table == table or target_table not in tables:
                continue
            dependencies[table].add(target_table)
            in_degree[table] += 1

    queue = deque([t for t in tables if in_degree[t] == 0])
    sorted_tables = []

    while queue:
        current = queue.popleft()
        sorted_tables.append(current)
        for table in tables:
            if current in dependencies[table]:
                in_degree[table] -= 1
                if in_degree[table] == 0:
                    queue.append(table)

    # 处理循环依赖：将未排序的表追加到末尾
    remaining = set(tables) - set(sorted_tables)
    if remaining:
        logger.warning(f"检测到循环依赖，未排序的表: {remaining}")
        sorted_tables.extend(remaining)

    return sorted_tables


def validate_foreign_keys(
    data: Dict[str, Any],
    ref_map: Dict[str, List[Tuple[str, str]]]
) -> Tuple[bool, List[str]]:
    """
    验证数据中所有外键引用是否指向已存在的记录。

    Returns:
        (全部通过, 错误信息列表)
    """
    errors = []
    for table_name, refs in ref_map.items():
        if table_name not in data:
            continue
        table_data = data[table_name]
        if not isinstance(table_data, dict):
            continue
        for record_id, record in table_data.items():
            if not isinstance(record, dict):
                continue
            for ref_field, target_table in refs:
                if ref_field not in record:
                    continue
                ref_value = record[ref_field]
                # List[str] 类型的多值引用（*_refs）
                if isinstance(ref_value, list):
                    for ref_id in ref_value:
                        if ref_id is None:
                            continue
                        if target_table not in data:
                            errors.append(
                                f"表 {table_name} 记录 {record_id} 字段 {ref_field} "
                                f"引用了不存在的表 {target_table}"
                            )
                        elif ref_id not in data[target_table]:
                            errors.append(
                                f"表 {table_name} 记录 {record_id} 字段 {ref_field} "
                                f"引用了不存在的 ID {ref_id}（目标表 {target_table}）"
                            )
                elif ref_value is not None:
                    if target_table not in data:
                        errors.append(
                            f"表 {table_name} 记录 {record_id} 字段 {ref_field} "
                            f"引用了不存在的表 {target_table}"
                        )
                    elif ref_value not in data[target_table]:
                        errors.append(
                            f"表 {table_name} 记录 {record_id} 字段 {ref_field} "
                            f"引用了不存在的 ID {ref_value}（目标表 {target_table}）"
                        )
    return len(errors) == 0, errors


def calculate_coverage_statistics(
    data: Dict[str, Any],
    base_data: Dict[str, Any],
    ref_map: Dict[str, List[Tuple[str, str]]]
) -> Dict[str, Any]:
    """
    计算数据覆盖度统计（表记录数 + 每个员工关联记录数）。
    """
    stats: Dict[str, Any] = {
        "table_counts": {},
        "employee_coverage": {},
        "total_records": 0,
    }
    for table_name, table_data in data.items():
        if isinstance(table_data, dict):
            count = len(table_data)
            stats["table_counts"][table_name] = count
            stats["total_records"] += count

    if "employees" in base_data:
        for emp_id in base_data["employees"]:
            stats["employee_coverage"][emp_id] = 0
        for table_data in data.values():
            if not isinstance(table_data, dict):
                continue
            for record in table_data.values():
                if not isinstance(record, dict):
                    continue
                for field_name, ref_value in record.items():
                    if (field_name == "employee_ref" or field_name.endswith("_employee_ref")) \
                            and ref_value and ref_value in stats["employee_coverage"]:
                        stats["employee_coverage"][ref_value] += 1

    return stats


def format_validation_report(
    fk_valid: bool,
    fk_errors: List[str],
    coverage_stats: Dict[str, Any],
    min_records_per_table: int = 3,
    min_records_per_employee: int = 3
) -> str:
    """格式化验证报告，仅输出关键错误摘要。"""
    issues = []

    if not fk_valid:
        issues.append(f"外键引用错误 ({len(fk_errors)} 处):")
        for error in fk_errors[:5]:
            issues.append(f"  - {error}")
        if len(fk_errors) > 5:
            issues.append(f"  ... 还有 {len(fk_errors) - 5} 处错误")

    low_count_tables = [
        (t, c) for t, c in coverage_stats["table_counts"].items()
        if c < min_records_per_table
    ]
    if low_count_tables:
        issues.append(f"\n表记录数不足（最少 {min_records_per_table} 条）:")
        for table, count in low_count_tables:
            issues.append(f"  - {table}: {count} 条")

    if "employee_coverage" in coverage_stats:
        low_emp = [
            (e, c) for e, c in coverage_stats["employee_coverage"].items()
            if c < min_records_per_employee
        ]
        if low_emp:
            issues.append(f"\n员工关联记录不足（最少 {min_records_per_employee} 条）:")
            for emp_id, count in low_emp[:10]:
                issues.append(f"  - {emp_id}: {count} 条")
            if len(low_emp) > 10:
                issues.append(f"  ... 还有 {len(low_emp) - 10} 个员工")

    return "✓ 所有验证通过" if not issues else "\n".join(issues)


def sample_db(db: dict, max_per_table: int = 5) -> dict:
    """从每张表中最多取 max_per_table 条记录，用于 BASE 等通用均匀采样"""
    return {t: dict(list(r.items())[:max_per_table]) for t, r in db.items()}


