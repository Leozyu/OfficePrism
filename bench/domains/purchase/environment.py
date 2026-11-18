from pathlib import Path

from bench.domains.purchase.models import PurchaseDB as DatabaseModel
from bench.domains.purchase.tools import PurchaseTools as DomainTools
from bench.environment.environment import Environment
from bench.utils import load_file

BASE_DB_PATH = Path("data/domains/base/db.json")
PURCHASE_DB_PATH = Path("data/domains/purchase/db.json")
PURCHASE_POLICY_PATH = Path("data/domains/purchase/policy.md")


def _load_policy() -> str:
    try:
        with open(PURCHASE_POLICY_PATH, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        return "Purchase Domain Policy"


def get_environment(db: DatabaseModel = None) -> Environment:
    if db is None:
        merged = {**load_file(BASE_DB_PATH), **load_file(PURCHASE_DB_PATH)}
        db = DatabaseModel.model_validate(merged)

    tools = DomainTools(db)
    return Environment(domain_name="purchase", policy=_load_policy(), tools=tools)
