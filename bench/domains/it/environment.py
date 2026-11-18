from pathlib import Path

from bench.domains.it.models import ITDB as DatabaseModel
from bench.domains.it.tools import ITTools as DomainTools
from bench.environment.environment import Environment
from bench.environment.tool_discovery import ToolDiscoveryToolkit
from bench.utils import load_file

BASE_DB_PATH = Path("data/domains/base/db.json")
IT_DB_PATH = Path("data/domains/it/db.json")
IT_POLICY_PATH = Path("data/domains/it/policy.md")


def _load_policy() -> str:
    try:
        with open(IT_POLICY_PATH, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        return "IT Domain Policy"


def get_environment(db: DatabaseModel = None, tool_mode: str = "full") -> Environment:
    if db is None:
        merged = {**load_file(BASE_DB_PATH), **load_file(IT_DB_PATH)}
        db = DatabaseModel.model_validate(merged)

    tools = DomainTools(db)
    if tool_mode == "search":
        tools = ToolDiscoveryToolkit(tools)
    return Environment(domain_name="it", policy=_load_policy(), tools=tools)
