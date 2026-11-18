"""
Evaluation configuration - 兼容层
从 config.config_loader 重新导出所有配置函数和常量，保持向后兼容。

推荐直接使用: from config.config_loader import get_llm_config, get_path_config
"""

# 从 config_loader 导入所有功能
from configs.config_loader import (
    get_llm_config,
    get_path_config,
    get_eval_constants,
)

# 加载并导出所有常量（向后兼容）
_constants = get_eval_constants()

# 导出所有常量到模块级别
DEFAULT_MAX_STEPS = _constants["DEFAULT_MAX_STEPS"]
DEFAULT_MAX_ERRORS = 10
DEFAULT_SEED = 300
DEFAULT_MAX_CONCURRENCY = 64
DEFAULT_NUM_TRIALS = 1
DEFAULT_SAVE_TO = None
DEFAULT_LOG_LEVEL = "ERROR"

# LLM
DEFAULT_AGENT_IMPLEMENTATION = "llm_agent"
DEFAULT_USER_IMPLEMENTATION = "user_simulator"
DEFAULT_LLM_AGENT = "gpt-5"
DEFAULT_LLM_USER = "gpt-5"
DEFAULT_LLM_TEMPERATURE_AGENT = 1.0
DEFAULT_LLM_TEMPERATURE_USER = 1.0
DEFAULT_LLM_ARGS_AGENT = {"temperature": DEFAULT_LLM_TEMPERATURE_AGENT}
DEFAULT_LLM_ARGS_USER = {"temperature": DEFAULT_LLM_TEMPERATURE_USER}

DEFAULT_LLM_NL_ASSERTIONS = "gpt-5"
DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE = 1.0
DEFAULT_LLM_NL_ASSERTIONS_ARGS = {"temperature": DEFAULT_LLM_NL_ASSERTIONS_TEMPERATURE}

DEFAULT_LLM_ENV_INTERFACE = "gpt-5"
DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE = 1.0
DEFAULT_LLM_ENV_INTERFACE_ARGS = {"temperature": DEFAULT_LLM_ENV_INTERFACE_TEMPERATURE}

# LITELLM
DEFAULT_MAX_RETRIES = 3
LLM_CACHE_ENABLED = False
DEFAULT_LLM_CACHE_TYPE = "redis"

# REDIS CACHE
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
REDIS_PREFIX = "tau2"
REDIS_CACHE_VERSION = "v1"
REDIS_CACHE_TTL = 60 * 60 * 24 * 30

# LANGFUSE
USE_LANGFUSE = False  # If True, make sure all the env variables are set for langfuse.

# API
API_PORT = 8000
