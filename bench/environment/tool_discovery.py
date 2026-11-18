"""Tool discovery wrapper for large tool sets.

This wrapper exposes only two meta tools to the agent:
- tool_search: find relevant real tools by name/doc/parameter text
- call_tool: dispatch to a selected real tool

The underlying toolkit remains the source of truth for execution and DB state.
"""

import json
from typing import Any, Optional

from bench.environment.toolkit import ToolKitBase, ToolType, get_tool_signatures, is_tool


_QUERY_ALIASES: dict[str, tuple[str, ...]] = {
    "员工": ("employee", "staff", "person"),
    "同事": ("employee", "staff"),
    "人员": ("employee", "staff"),
    "详情": ("details", "detail", "get"),
    "记录": ("record", "records", "list", "get"),
    "查询": ("get", "list", "search"),
    "内推": ("referral", "referrals", "recommendation"),
    "推荐": ("referral", "referrals", "recommendation"),
    "奖金": ("bonus", "reward", "payment"),
    "申请": ("request", "requests", "submit", "create"),
    "证明": ("certificate", "certificates", "proof"),
    "在职": ("employment", "employment_proof", "certificate", "proof"),
    "报销": ("expense", "expenses", "reimbursement"),
    "预算": ("budget", "budgets"),
    "会议室": ("booking", "bookings", "meeting", "room"),
    "账号": ("account", "accounts"),
    "邮件": ("email", "mail"),
    "合同": ("contract", "contracts"),
    "采购": ("purchase", "procurement"),
    "供应商": ("supplier", "suppliers"),
    "项目": ("project", "projects"),
    "待办": ("todo", "task", "tasks"),
}


def _expand_query_terms(query_text: str) -> list[str]:
    terms = [term for term in query_text.replace("_", " ").split() if term]
    expanded_terms = list(terms)
    for term in terms:
        if term.endswith("s") and len(term) > 3:
            expanded_terms.append(term[:-1])
    for zh, aliases in _QUERY_ALIASES.items():
        if zh in query_text:
            expanded_terms.extend(aliases)
    if not expanded_terms and query_text:
        expanded_terms.append(query_text)
    return list(dict.fromkeys(expanded_terms))


def _name_alias_boost(query_text: str, tool_name: str) -> int:
    score = 0
    name_text = tool_name.lower().replace("_", " ")
    for zh, aliases in _QUERY_ALIASES.items():
        if zh not in query_text:
            continue
        if any(alias in name_text for alias in aliases):
            score += 3
    return score


def _intent_boost(query_text: str, tool_name: str) -> int:
    name_text = tool_name.lower()
    score = 0
    if any(term in query_text for term in ("list", "查询", "查一下", "列出")):
        if name_text.startswith(("list_", "get_", "find_", "search_")):
            score += 2
    if any(term in query_text for term in ("submit", "create", "申请", "提交")):
        if name_text.startswith(("submit_", "create_", "add_")):
            score += 2
    return score


class ToolDiscoveryToolkit(ToolKitBase):
    """Expose search/dispatch tools while hiding the full real tool list."""

    def __init__(self, wrapped: ToolKitBase):
        super().__init__(db=wrapped.db)
        self.wrapped = wrapped
        self.is_tool_discovery = True

    @is_tool(ToolType.GENERIC)
    def tool_search(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 10,
    ) -> str:
        """Search available business tools by name, description, and parameters."""
        query_text = str(query or "").strip().lower()
        terms = _expand_query_terms(query_text)
        limit = max(1, min(int(top_k or 10), 30))
        domain_filter = str(domain).strip().lower() if domain else None

        results: list[dict[str, Any]] = []
        for name, signature in get_tool_signatures(self.wrapped).items():
            tool_domain = getattr(self.wrapped, "tool_domain", lambda _: None)(name)
            tool_domain_normalized = str(tool_domain).strip().lower() if tool_domain else None
            if domain_filter and tool_domain_normalized and tool_domain_normalized != domain_filter:
                continue
            params = signature.params or {}
            param_names = " ".join((params.get("properties") or {}).keys())
            name_text = name.lower().replace("_", " ")
            doc_text = str(signature.doc or "").lower().replace("_", " ")
            param_text = param_names.lower().replace("_", " ")
            domain_text = tool_domain_normalized or ""
            score = 0
            for term in terms:
                if term in name_text:
                    score += 4
                if term in param_text:
                    score += 2
                if term in doc_text:
                    score += 1
                if term and term == domain_text:
                    score += 3
            score += _name_alias_boost(query_text, name)
            score += _intent_boost(query_text, name)
            haystack = f"{name_text} {doc_text} {param_text} {domain_text}"
            if query_text and query_text in name_text:
                score += 6
            elif query_text and query_text in haystack:
                score += 2
            if score == 0:
                continue
            results.append(
                {
                    "score": score,
                    "domain": tool_domain,
                    "name": name,
                    "tool_type": self.wrapped.tool_type(name).value,
                    "description": signature.doc,
                    "parameters": signature.params,
                }
            )

        results.sort(key=lambda item: (-item["score"], item["name"]))
        return json.dumps(results[:limit], ensure_ascii=False)

    @is_tool(ToolType.GENERIC)
    def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """Call a real business tool returned by tool_search."""
        if name in {"tool_search", "call_tool"}:
            raise ValueError(f"Cannot dispatch meta tool through call_tool: {name}")
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be a dictionary")
        return self.wrapped.use_tool(name, **arguments)

    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use meta tools, while tolerating direct calls to discovered real tools."""
        if tool_name in self.tools:
            return super().use_tool(tool_name, **kwargs)
        if self.wrapped.has_tool(tool_name):
            return self.wrapped.use_tool(tool_name, **kwargs)
        raise ValueError(f"Tool '{tool_name}' not found.")

    def get_db_hash(self) -> str:
        return self.wrapped.get_db_hash()

    def update_db(self, update_data: Optional[dict[str, Any]] = None):
        self.wrapped.update_db(update_data)
        self.db = self.wrapped.db
