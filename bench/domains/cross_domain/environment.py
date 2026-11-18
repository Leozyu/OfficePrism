from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from bench.domains.admin.models import AdminDB
from bench.domains.admin.tools import AdminTools
from bench.domains.finance.models import FinanceDB
from bench.domains.finance.tools import FinanceTools
from bench.domains.hr.models import HRDB
from bench.domains.hr.tools import HRTools
from bench.domains.it.models import ITDB
from bench.domains.it.tools import ITTools
from bench.domains.law.models import LawDB
from bench.domains.law.tools import LawTools
from bench.domains.purchase.models import PurchaseDB
from bench.domains.purchase.tools import PurchaseTools
from bench.domains.work.models import WorkDB
from bench.domains.work.tools import WorkTools
from bench.environment.environment import Environment
from bench.environment.tool_discovery import ToolDiscoveryToolkit
from bench.environment.toolkit import ToolKitBase, ToolType
from bench.utils import load_file

BASE_DB_PATH = Path("data/domains/base/db.json")


@dataclass
class _DomainSpec:
    name: str
    db_path: Path
    policy_path: Path
    db_model: Any
    tool_cls: Any


_DOMAIN_SPECS: Dict[str, _DomainSpec] = {
    "hr": _DomainSpec(
        name="hr",
        db_path=Path("data/domains/hr/db.json"),
        policy_path=Path("data/domains/hr/policy.md"),
        db_model=HRDB,
        tool_cls=HRTools,
    ),
    "it": _DomainSpec(
        name="it",
        db_path=Path("data/domains/it/db.json"),
        policy_path=Path("data/domains/it/policy.md"),
        db_model=ITDB,
        tool_cls=ITTools,
    ),
    "admin": _DomainSpec(
        name="admin",
        db_path=Path("data/domains/admin/db.json"),
        policy_path=Path("data/domains/admin/policy.md"),
        db_model=AdminDB,
        tool_cls=AdminTools,
    ),
    "finance": _DomainSpec(
        name="finance",
        db_path=Path("data/domains/finance/db.json"),
        policy_path=Path("data/domains/finance/policy.md"),
        db_model=FinanceDB,
        tool_cls=FinanceTools,
    ),
    "law": _DomainSpec(
        name="law",
        db_path=Path("data/domains/law/db.json"),
        policy_path=Path("data/domains/law/policy.md"),
        db_model=LawDB,
        tool_cls=LawTools,
    ),
    "purchase": _DomainSpec(
        name="purchase",
        db_path=Path("data/domains/purchase/db.json"),
        policy_path=Path("data/domains/purchase/policy.md"),
        db_model=PurchaseDB,
        tool_cls=PurchaseTools,
    ),
    "work": _DomainSpec(
        name="work",
        db_path=Path("data/domains/work/db.json"),
        policy_path=Path("data/domains/work/policy.md"),
        db_model=WorkDB,
        tool_cls=WorkTools,
    ),
}


class _MergedDBView:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def model_dump(self) -> Dict[str, Any]:
        return self._data


class CrossDomainToolKit(ToolKitBase):
    """将多个域工具合并到单一 toolkit 视图。"""

    def __init__(self, domain_toolkits: Dict[str, ToolKitBase], merged_db: Dict[str, Any]):
        super().__init__(db=_MergedDBView(merged_db))
        self._domain_toolkits = domain_toolkits
        self._tools: Dict[str, Any] = {}
        self._tool_types: Dict[str, ToolType] = {}
        self._tool_objs: Dict[str, Any] = {}
        self._tool_domains: Dict[str, str] = {}
        self.is_cross_domain = True
        for domain_name, toolkit in domain_toolkits.items():
            for name, fn in toolkit.tools.items():
                if name in self._tools:
                    continue
                self._tools[name] = fn
                self._tool_types[name] = toolkit.tool_type(name)
                self._tool_domains[name] = domain_name
            for name, obj in toolkit.get_tools().items():
                self._tool_objs.setdefault(name, obj)

    @property
    def tools(self) -> Dict[str, Any]:
        return self._tools

    def use_tool(self, tool_name: str, **kwargs) -> str:
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self._tools[tool_name](**kwargs)

    def get_tools(self) -> Dict[str, Any]:
        return self._tool_objs

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self._tools

    def tool_type(self, tool_name: str) -> ToolType:
        return self._tool_types[tool_name]

    def tool_domain(self, tool_name: str) -> Optional[str]:
        return self._tool_domains.get(tool_name)


def _load_policy(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        return ""


def get_environment(
    domains: Optional[List[str]] = None,
    tool_mode: str = "full",
    policy_domains: Optional[List[str]] = None,
    solo_mode: bool = True,
) -> Environment:
    """构造跨域环境。

    domains: 参与合并（工具池/DB）的域；None 表示全部 7 域。
    policy_domains: 只把哪些域的 policy 拼进 prompt；None 表示与 domains 相同。
        tool-scaling 实验用它把 policy 固定为本域，只让可发现工具池随 domains 变化。
    """
    selected = domains or list(_DOMAIN_SPECS.keys())
    policy_selected = policy_domains if policy_domains is not None else selected
    base_data = load_file(BASE_DB_PATH)
    merged_data: Dict[str, Any] = dict(base_data)
    domain_toolkits: Dict[str, ToolKitBase] = {}
    policies: List[str] = []

    for domain in selected:
        spec = _DOMAIN_SPECS[domain]
        domain_data = load_file(spec.db_path)
        merged = {**base_data, **domain_data}
        domain_db = spec.db_model.model_validate(merged)
        domain_toolkits[domain] = spec.tool_cls(domain_db)
        merged_data.update(domain_data)
        if domain in policy_selected:
            policy_text = _load_policy(spec.policy_path).strip()
            if policy_text:
                policies.append(f"[{domain.upper()}]\n{policy_text}")

    toolkit = CrossDomainToolKit(domain_toolkits=domain_toolkits, merged_db=merged_data)
    if tool_mode == "search":
        toolkit = ToolDiscoveryToolkit(toolkit)
    policy = "\n\n".join(policies) if policies else "Cross Domain Policy"
    env = Environment(domain_name="cross", policy=policy, tools=toolkit)
    if solo_mode:
        env.set_solo_mode(True)
    return env
