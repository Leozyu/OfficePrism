from pathlib import Path

from bench.domains.admin.models import AdminDB as DatabaseModel
from bench.domains.admin.tools import AdminTools as DomainTools
from bench.environment.environment import Environment
from bench.utils import load_file

BASE_DB_PATH = Path("data/domains/base/db.json")
ADMIN_DB_PATH = Path("data/domains/admin/db.json")
ADMIN_POLICY_PATH = Path("data/domains/admin/policy.md")


def _load_policy() -> str:
    try:
        with open(ADMIN_POLICY_PATH, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        return "Admin Domain Policy"


def get_environment(db: DatabaseModel = None) -> Environment:
    if db is None:
        merged = {**load_file(BASE_DB_PATH), **load_file(ADMIN_DB_PATH)}
        db = DatabaseModel.model_validate(merged)

    tools = DomainTools(db)
    return Environment(domain_name="admin", policy=_load_policy(), tools=tools)
