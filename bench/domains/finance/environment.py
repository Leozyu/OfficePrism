from pathlib import Path

from bench.domains.finance.models import FinanceDB as DatabaseModel
from bench.domains.finance.tools import FinanceTools as DomainTools
from bench.environment.environment import Environment
from bench.environment.tool_discovery import ToolDiscoveryToolkit
from bench.utils import load_file

BASE_DB_PATH = Path("data/domains/base/db.json")
FINANCE_DB_PATH = Path("data/domains/finance/db.json")
FINANCE_POLICY_PATH = Path("data/domains/finance/policy.md")


def _load_policy() -> str:
    try:
        with open(FINANCE_POLICY_PATH, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        return "Finance Domain Policy"


def get_environment(db: DatabaseModel = None, tool_mode: str = "full") -> Environment:
    if db is None:
        merged = {**load_file(BASE_DB_PATH), **load_file(FINANCE_DB_PATH)}
        db = DatabaseModel.model_validate(merged)

    tools = DomainTools(db)
    if tool_mode == "search":
        tools = ToolDiscoveryToolkit(tools)
    return Environment(domain_name="finance", policy=_load_policy(), tools=tools)
