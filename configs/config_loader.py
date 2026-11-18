"""Configuration loader using OmegaConf (simpler than Hydra)."""

from pathlib import Path
from typing import Any, Optional

from omegaconf import OmegaConf


# 全局配置实例
_global_config = None
_app_config_dict = None


def load_config(config_file: str = None) -> dict:
    """
    加载配置文件并返回字典
    
    Args:
        config_file: 配置文件路径（如果为None，自动查找config/app.yaml）
    
    Returns:
        配置字典
    """
    global _global_config, _app_config_dict
    if _global_config is None:
        _global_config = Config(config_file)
        # 将 OmegaConf 对象转换为普通字典
        _app_config_dict = OmegaConf.to_container(_global_config._cfg, resolve=True)
    return _app_config_dict


# ============================================================================
# Evaluation 配置加载函数
# ============================================================================

def get_llm_config(role: str = "agent"):
    """
    获取指定角色的 LLM 配置，直接从 evaluation.llm.<role> 读取。

    Args:
        role: 角色类型，可选值: 'agent', 'evaluator'
    """
    app_config = load_config()
    return app_config.get("evaluation", {}).get("llm", {}).get(role, {})


def get_path_config(path_key: str = None):
    """
    获取路径配置
    
    Args:
        path_key: 路径键，如 'data_dir', 'output_dir', 'domains.mock.db_path'
                  如果为 None，返回所有路径配置
                  支持点分隔的嵌套键访问
    
    Returns:
        路径字符串或路径配置字典
    
    Examples:
        >>> get_path_config("data_dir")
        'data'
        >>> get_path_config("domains.mock.db_path")
        'data/domains/mock/db.json'
    """
    app_config = load_config()
    eval_config = app_config.get("evaluation", {})
    paths_config = eval_config.get("paths", {})
    
    if path_key is None:
        return paths_config
    
    # 支持点分隔的嵌套键，如 'domains.mock.db_path'
    keys = path_key.split('.')
    result = paths_config
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return None
    
    return result


def get_eval_constants():
    """
    获取所有 evaluation 相关的常量
    用于向后兼容
    
    Returns:
        包含所有常量的字典
    """
    app_config = load_config()
    eval_config = app_config.get("evaluation", {})
    
    # SIMULATION
    simulation = eval_config.get("simulation", {})
    DEFAULT_MAX_STEPS = simulation.get("max_steps", 200)
    DEFAULT_MAX_ERRORS = simulation.get("max_errors", 10)
    DEFAULT_SEED = simulation.get("seed", 300)
    DEFAULT_MAX_CONCURRENCY = simulation.get("max_concurrency", 64)
    DEFAULT_NUM_TRIALS = simulation.get("num_trials", 1)
    DEFAULT_SAVE_TO = simulation.get("save_to", None)
    DEFAULT_LOG_LEVEL = simulation.get("log_level", "ERROR")
    
    # LLM
    llm_config = eval_config.get("llm", {})
    agent_config = llm_config.get("agent", {})
    user_config = llm_config.get("user", {})
    evaluator_config = llm_config.get("evaluator", {})
    
    DEFAULT_AGENT_IMPLEMENTATION = agent_config.get("implementation", "llm_agent")
    DEFAULT_USER_IMPLEMENTATION = user_config.get("implementation", "user_simulator")
    DEFAULT_LLM_AGENT = agent_config.get("model", "gpt-5")
    DEFAULT_LLM_USER = user_config.get("model", "gpt-5")
    DEFAULT_LLM_TEMPERATURE_AGENT = agent_config.get("temperature", 1.0)
    DEFAULT_LLM_TEMPERATURE_USER = user_config.get("temperature", 1.0)
    DEFAULT_LLM_ARGS_AGENT = {"temperature": DEFAULT_LLM_TEMPERATURE_AGENT}
    DEFAULT_LLM_ARGS_USER = {"temperature": DEFAULT_LLM_TEMPERATURE_USER}
    
    DEFAULT_LLM_NL_ASSERTIONS = evaluator_config.get("nl_assertions_model", "gpt-5")
    DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE = evaluator_config.get("nl_assertions_temperature", 1.0)
    DEFAULT_LLM_NL_ASSERTIONS_ARGS = {"temperature": DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE}
    
    DEFAULT_LLM_ENV_INTERFACE = evaluator_config.get("env_interface_model", "gpt-5")
    DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE = evaluator_config.get("env_interface_temperature", 1.0)
    DEFAULT_LLM_ENV_INTERFACE_ARGS = {"temperature": DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE}
    
    # LITELLM
    litellm_config = eval_config.get("litellm", {})
    DEFAULT_MAX_RETRIES = litellm_config.get("max_retries", 3)
    LLM_CACHE_ENABLED = litellm_config.get("cache_enabled", False)
    DEFAULT_LLM_CACHE_TYPE = litellm_config.get("cache_type", "redis")
    
    # REDIS CACHE
    redis_config = eval_config.get("redis", {})
    REDIS_HOST = redis_config.get("host", "localhost")
    REDIS_PORT = redis_config.get("port", 6379)
    REDIS_PASSWORD = redis_config.get("password", "")
    REDIS_PREFIX = redis_config.get("prefix", "tau2")
    REDIS_CACHE_VERSION = redis_config.get("cache_version", "v1")
    REDIS_CACHE_TTL = redis_config.get("cache_ttl", 60 * 60 * 24 * 30)
    
    # LANGFUSE
    langfuse_config = eval_config.get("langfuse", {})
    USE_LANGFUSE = langfuse_config.get("enabled", False)
    
    # 路径
    DATA_DIR = get_path_config("data_dir") or "data"
    OUTPUT_DIR = get_path_config("output_dir") or "data/results"
    
    return {
        "DEFAULT_MAX_STEPS": DEFAULT_MAX_STEPS,
        "DEFAULT_MAX_ERRORS": DEFAULT_MAX_ERRORS,
        "DEFAULT_SEED": DEFAULT_SEED,
        "DEFAULT_MAX_CONCURRENCY": DEFAULT_MAX_CONCURRENCY,
        "DEFAULT_NUM_TRIALS": DEFAULT_NUM_TRIALS,
        "DEFAULT_SAVE_TO": DEFAULT_SAVE_TO,
        "DEFAULT_LOG_LEVEL": DEFAULT_LOG_LEVEL,
        "DEFAULT_AGENT_IMPLEMENTATION": DEFAULT_AGENT_IMPLEMENTATION,
        "DEFAULT_USER_IMPLEMENTATION": DEFAULT_USER_IMPLEMENTATION,
        "DEFAULT_LLM_AGENT": DEFAULT_LLM_AGENT,
        "DEFAULT_LLM_USER": DEFAULT_LLM_USER,
        "DEFAULT_LLM_TEMPERATURE_AGENT": DEFAULT_LLM_TEMPERATURE_AGENT,
        "DEFAULT_LLM_TEMPERATURE_USER": DEFAULT_LLM_TEMPERATURE_USER,
        "DEFAULT_LLM_ARGS_AGENT": DEFAULT_LLM_ARGS_AGENT,
        "DEFAULT_LLM_ARGS_USER": DEFAULT_LLM_ARGS_USER,
        "DEFAULT_LLM_NL_ASSERTIONS": DEFAULT_LLM_NL_ASSERTIONS,
        "DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE": DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE,
        "DEFAULT_LLM_NL_ASSERTIONS_ARGS": DEFAULT_LLM_NL_ASSERTIONS_ARGS,
        "DEFAULT_LLM_ENV_INTERFACE": DEFAULT_LLM_ENV_INTERFACE,
        "DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE": DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE,
        "DEFAULT_LLM_ENV_INTERFACE_ARGS": DEFAULT_LLM_ENV_INTERFACE_ARGS,
        "DEFAULT_MAX_RETRIES": DEFAULT_MAX_RETRIES,
        "LLM_CACHE_ENABLED": LLM_CACHE_ENABLED,
        "DEFAULT_LLM_CACHE_TYPE": DEFAULT_LLM_CACHE_TYPE,
        "REDIS_HOST": REDIS_HOST,
        "REDIS_PORT": REDIS_PORT,
        "REDIS_PASSWORD": REDIS_PASSWORD,
        "REDIS_PREFIX": REDIS_PREFIX,
        "REDIS_CACHE_VERSION": REDIS_CACHE_VERSION,
        "REDIS_CACHE_TTL": REDIS_CACHE_TTL,
        "USE_LANGFUSE": USE_LANGFUSE,
        "DATA_DIR": DATA_DIR,
        "OUTPUT_DIR": OUTPUT_DIR,
        "API_PORT": 8000,
    }


class Config:
    """配置对象，使用 OmegaConf 加载，支持点号访问"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径（如果为None，自动查找config/app.yaml）
        """
        # 查找项目根目录和配置文件
        self.project_root = self._find_project_root()
        if config_file is None:
            config_file = self.project_root / "configs" / "app.yaml"
        else:
            config_file = Path(config_file)
        
        self.config_file = config_file
        self._cfg = self._load()
    
    def _find_project_root(self) -> Path:
        """查找项目根目录（包含config目录的目录）"""
        current = Path(__file__).parent
        while current != current.parent:
            if (current / "config").exists():
                return current
            current = current.parent
        return Path(__file__).parent.parent
    
    def _load(self):
        """加载配置"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        return OmegaConf.load(self.config_file)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值（支持点号路径）
        
        Args:
            key_path: 配置路径，如 "app.name" 或 "paths.seed_data_file"
            default: 默认值
            
        Returns:
            配置值
        """
        value = OmegaConf.select(self._cfg, key_path)
        return value if value is not None else default
    
    def __getattr__(self, name: str) -> Any:
        """支持直接属性访问，如 config.paths.seed_data_file"""
        # 1. 检查类中是否定义了该 property (如 seed_data_file)
        # 使用 getattr 会触发递归，所以检查 __dict__ 或者用 object.__getattribute__
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass
            
        # 2. 检查配置对象
        if hasattr(self._cfg, name):
            return getattr(self._cfg, name)
            
        raise AttributeError(f"配置中没有 '{name}'")
    
    # ============ 路径相关便捷属性 ============
    
    def _get_project_root(self) -> Path:
        """获取项目根目录（从配置或默认）"""
        root_path = self.get("paths.project_root", None)
        if root_path:
            if Path(root_path).is_absolute():
                return Path(root_path).resolve()
            return (self.config_file.parent / root_path).resolve()
        return self.project_root
    
    def _resolve_path(self, path_value: str) -> Path:
        """解析路径（相对路径基于项目根目录）"""
        if Path(path_value).is_absolute():
            return Path(path_value).resolve()
        return (self._get_project_root() / path_value).resolve()
    
    @property
    def seed_data_file(self) -> Path:
        """种子数据文件路径"""
        path = self.get("paths.seed_data_file", "resources/data/seeds/default.json")
        return self._resolve_path(path)
    
    @property
    def task_templates_file(self) -> Path:
        """任务模板文件路径"""
        path = self.get("paths.task_templates_file", "resources/templates/hr.yaml")
        return self._resolve_path(path)
    
    @property
    def hr_domain_config_file(self) -> Path:
        """HR域配置文件路径"""
        path = self.get("paths.hr_domain_config_file", "config/hr_domain.yaml")
        return self._resolve_path(path)
    
    @property
    def generated_templates_file(self) -> Path:
        """LLM生成的任务模板文件路径"""
        path = self.get("paths.generated_templates_file", "resources/templates/hr_generated.yaml")
        return self._resolve_path(path)
    
    @property
    def query_mapping_file(self) -> Path:
        """查询到模板的映射文件路径"""
        path = self.get("paths.query_mapping_file", "resources/templates/query_mapping.json")
        return self._resolve_path(path)
    
    @property
    def workflows_file(self) -> Path:
        """工作流标准序列文件路径"""
        path = self.get("paths.workflows_file", "resources/templates/workflows.json")
        return self._resolve_path(path)
    
    @property
    def resources_dir(self) -> Path:
        """资源目录路径"""
        path = self.get("paths.resources_dir", "resources")
        return self._resolve_path(path)

    @property
    def seeds_dir(self) -> Path:
        """种子数据目录路径"""
        path = self.get("paths.seeds_dir", "resources/data/seeds")
        return self._resolve_path(path)


# 全局配置实例
config = Config()
