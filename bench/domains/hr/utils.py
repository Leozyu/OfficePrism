from pathlib import Path

try:
    from bench.config import get_path_config
    
    def get_hr_path(key: str) -> Path:
        """
        功能说明（Description）：
            获取hrpath，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `key` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `Path`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        path = get_path_config(f"domains.hr.{key}")
        if path:
            return Path(path)
        
        defaults = {
            "data_dir": "data/domains/hr",
            "db_path": "data/domains/hr/db.json",
            "base_db_path": "data/domains/base/db.json",
            "policy_path": "data/domains/hr/policy.md",
            "task_set_path": "data/domains/hr/tasks.json",
        }
        return Path(defaults.get(key, ""))
    
    HR_DATA_DIR = get_hr_path("data_dir")
    HR_DB_PATH = get_hr_path("db_path")
    BASE_DB_PATH = get_hr_path("base_db_path")
    HR_POLICY_PATH = get_hr_path("policy_path")
    HR_TASK_SET_PATH = get_hr_path("task_set_path")
    
except ImportError:
    from bench.utils.utils import DATA_DIR
    HR_DATA_DIR = DATA_DIR / "domains" / "hr"
    HR_DB_PATH = HR_DATA_DIR / "db.json"
    BASE_DB_PATH = DATA_DIR / "domains" / "base" / "db.json"
    HR_POLICY_PATH = HR_DATA_DIR / "policy.md"
    HR_TASK_SET_PATH = HR_DATA_DIR / "tasks.json"
