import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path

from deepdiff import DeepDiff
from dotenv import load_dotenv
from loguru import logger

res = load_dotenv()
# if not res:
#     logger.warning("No .env file found")

# 从配置加载 DATA_DIR
try:
    from bench.config import get_path_config
    _data_dir = get_path_config("data_dir")
    DATA_DIR = Path(_data_dir) if _data_dir else Path('data')
except ImportError:
    # 回退到默认值（避免循环导入）
    DATA_DIR = Path('data')


def get_dict_hash(obj: dict) -> str:
    """
    Generate a unique hash for dict.
    Returns a hex string representation of the hash.
    """
    hash_string = json.dumps(obj, sort_keys=True, default=str)
    return hashlib.sha256(hash_string.encode()).hexdigest()


def show_dict_diff(dict1: dict, dict2: dict) -> str:
    """
    Show the difference between two dictionaries.
    """
    diff = DeepDiff(dict1, dict2)
    return diff


def get_now() -> str:
    """
    Returns the current date and time in the format YYYYMMDD_HHMMSS.
    """
    now = datetime.now()
    return format_time(now)


def format_time(time: datetime) -> str:
    """
    Format the time in the format YYYYMMDD_HHMMSS.
    """
    return time.isoformat()


def get_commit_hash() -> str:
    """
    Get the commit hash of the current directory.
    """
    try:
        commit_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], text=True)
            .strip()
            .split("\n")[0]
        )
    except Exception as e:
        logger.error(f"Failed to get git hash: {e}")
        commit_hash = "unknown"
    return commit_hash
