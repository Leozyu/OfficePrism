import json
import random
from datetime import datetime, timedelta
from faker import Faker

SEED = 42
SCALE = 100  # adjustable

random.seed(SEED)
fake = Faker("zh_CN")
Faker.seed(SEED)

# ============================================================
# Base Data: READ ONLY
# ============================================================
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    BASE_DATA_JSON = f.read()

# ============================================================
# Config
# ============================================================
BASE_DATE = datetime(2020, 1, 1, 0, 0, 0)
NOW = datetime(2025, 6, 15, 12, 0, 0)

SOFT_REF_FIELD_NAMES = {
    "trip_ref",  # explicit cross-domain / absent in provided base
}

CURRENCIES = ["CNY", "USD", "EUR", "GBP", "JPY", "HKD", "SGD", "KRW", "TWD"]
CHINA_CURRENCIES = ["CNY", "CNY", "CNY", "HKD", "USD"]

FINANCE_ACCOUNT_TYPES = ["settlement", "payroll", "petty_cash", "escrow", "investment", "tax"]
FINANCE_ACCOUNT_PURPOSES = ["general", "operating", "capital", "reserve"]
FINANCE_ACCOUNT_STATUSES = ["active", "frozen", "closed"]

BUDGET_TYPES = ["department", "project", "company", "special"]
BUDGET_SCOPE_TYPES = ["department", "team", "company", "project"]
BUDGET_STATUSES = ["draft", "submitted", "approved", "rejected", "closed", "frozen"]
FISCAL_PERIODS = ["Q1", "Q2", "Q3", "Q4", "H1", "H2", "annual"]

EXPENSE_CATEGORIES = [
    "travel", "accommodation", "meals", "transportation", "office_supplies",
    "software", "hardware", "training", "entertainment", "communication",
    "marketing", "consulting", "other"
]
EXPENSE_TYPES = ["travel", "daily", "project", "entertainment", "training", "other"]
EXPENSE_REPORT_STATUSES = [
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "paid", "cancelled"
]
EXPENSE_LINE_STATUSES = ["pending", "approved", "rejected", "partial_approved"]

INVOICE_TYPES = [
    "vat_special", "vat_general", "electronic", "receipt",
    "train_ticket", "air_ticket", "toll", "other"
]
INVOICE_DIRECTIONS = ["inbound", "outbound"]
INVOICE_VERIFICATION_STATUSES = ["unverified", "verified", "failed", "expired"]
INVOICE_STATUSES = ["active", "voided", "lost", "archived"]

INVOICE_HEADER_TYPES = ["company", "individual"]
INVOICE_HEADER_STATUSES = ["active", "inactive"]

PAYMENT_TYPES = [
    "procurement", "service", "reimbursement", "salary",
    "bonus", "refund", "loan_disbursement", "other"
]
PAYMENT_METHODS = ["bank_transfer", "check", "cash", "alipay", "wechat_pay", "internal_transfer"]
PAYMENT_REQUEST_STATUSES = [
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "completed", "cancelled"
]
PAYMENT_URGENCIES = ["normal", "urgent", "critical"]

PAYMENT_CHANNELS = ["bank_transfer", "check", "cash", "alipay", "wechat_pay", "internal_transfer"]
PAYMENT_EXECUTION_STATUSES = ["pending", "processing", "completed", "failed", "reversed"]

RECEIPT_CHANNELS = ["bank_transfer", "check", "cash", "alipay", "wechat_pay", "pos", "other"]
RECEIPT_TYPES = ["sales", "service", "refund_return", "investment", "loan_repayment", "other"]
RECONCILIATION_STATUSES = ["unmatched", "matched", "partial_matched", "disputed"]

REFUND_TYPES = ["customer_return", "service_cancellation", "overcharge", "duplicate_payment", "other"]
REFUND_REASON_CATEGORIES = [
    "product_defect", "service_issue", "customer_request",
    "billing_error", "policy_compliance", "other"
]
REFUND_METHODS = ["original_channel", "bank_transfer", "cash", "credit_note"]
REFUND_STATUSES = [
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "completed", "cancelled"
]

LOAN_PURPOSES = ["travel_advance", "project_advance", "emergency", "other"]
EMPLOYEE_LOAN_STATUSES = ["draft", "submitted", "approved", "rejected", "active", "settled", "overdue", "written_off"]
REPAYMENT_METHODS = ["salary_deduction", "bank_transfer", "cash", "expense_offset"]

SETTLEMENT_COUNTERPARTY_TYPES = ["supplier", "customer", "partner", "employee"]
SETTLEMENT_STATUSES = ["draft", "submitted", "approved", "rejected", "settled", "cancelled"]

FUND_TRANSFER_STATUSES = ["draft", "submitted", "approved", "rejected", "executed", "failed", "cancelled"]

EXCHANGE_RATE_TYPES = ["central_bank", "commercial", "internal"]

TAX_TYPES = [
    "corporate_income", "vat", "individual_income", "stamp_duty",
    "urban_maintenance", "education_surcharge", "other"
]
TAX_FILING_STATUSES = ["draft", "prepared", "filed", "accepted", "rejected", "amended"]

INCOME_TYPES = ["salary", "bonus", "equity", "allowance", "severance", "other"]
EMPLOYEE_TAX_FILING_STATUSES = ["withheld", "filed", "adjusted", "finalized"]

ACCRUAL_TYPES = ["expense_accrual", "revenue_accrual", "provision", "prepaid_amortization"]
ACCRUAL_ENTRY_STATUSES = ["draft", "posted", "reversed", "cancelled"]

CITY_TIERS = ["tier_1", "new_tier_1", "tier_2", "tier_3", "other"]
EXPENSE_POLICY_STATUSES = ["active", "inactive", "deprecated"]

FINANCE_TICKET_CATEGORIES = [
    "reimbursement", "payment", "invoice", "budget", "tax",
    "loan", "settlement", "account", "other"
]
FINANCE_TICKET_SUBCATEGORIES = [
    "policy_inquiry", "status_inquiry", "correction", "dispute",
    "system_issue", "approval_escalation", "other"
]
FINANCE_TICKET_PRIORITIES = ["low", "normal", "high", "critical"]
FINANCE_TICKET_STATUSES = ["open", "in_progress", "pending_info", "resolved", "closed", "cancelled"]

CREDIT_PRODUCT_TYPES = ["personal_loan", "housing_loan", "education_loan", "emergency_loan", "other"]
CREDIT_REPAYMENT_METHODS = ["equal_installment", "equal_principal", "bullet", "custom"]
CREDIT_APPLICATION_STATUSES = [
    "draft", "submitted", "under_review", "approved", "rejected",
    "disbursed", "repaying", "settled", "overdue", "defaulted", "cancelled"
]
CREDIT_RISK_LEVELS = ["low", "medium", "high", "very_high"]
CREDIT_SCHEDULE_STATUSES = ["pending", "paid", "overdue", "partial_paid", "waived"]

STOCK_BROKERAGES = ["boci", "cicc", "citic", "huatai", "guotai", "other"]
STOCK_MARKETS = ["SSE", "SZSE", "HKEX", "NYSE", "NASDAQ", "other"]
TRADE_DIRECTIONS = ["buy", "sell"]
ORDER_TYPES = ["limit", "market", "stop", "stop_limit"]
STOCK_ORDER_STATUSES = ["draft", "submitted", "partial_filled", "filled", "cancelled", "rejected", "expired"]

FINANCE_APPROVAL_SOURCE_TYPES = [
    "expense_report", "payment_request", "refund", "employee_loan",
    "settlement", "fund_transfer", "budget", "credit_application", "tax_filing"
]
FINANCE_APPROVER_ROLES = [
    "direct_manager", "department_head", "finance_manager",
    "finance_director", "cfo", "ceo", "custom"
]
FINANCE_APPROVAL_ACTIONS = ["pending", "approved", "rejected", "returned", "delegated", "skipped"]

# ============================================================
# Helpers
# ============================================================
def iso_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")

def random_datetime(start: datetime, end: datetime) -> datetime:
    if start >= end:
        return start
    delta = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta))

def later_datetime(start: datetime, min_days=1, max_days=180, hard_end=NOW) -> datetime:
    dt = start + timedelta(days=random.randint(min_days, max_days), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    return min(dt, hard_end)

def maybe(prob=0.7) -> bool:
    return random.random() < prob

def choose(seq):
    return random.choice(seq)

def sample_n(seq, min_n=1, max_n=3):
    if not seq:
        return []
    n = min(len(seq), random.randint(min_n, max_n))
    return random.sample(seq, n)

def clamp_non_negative(v):
    return round(max(0.0, v), 2)

def money(v):
    return round(float(v), 2)

def zh_sentence(min_words=8, max_words=20):
    return fake.sentence(nb_words=random.randint(min_words, max_words))

def zh_title(prefix):
    return f"{prefix}{fake.word()}"

def sequential_ref(prefix: str, idx: int, width: int = 3) -> str:
    return f"{prefix}{idx:0{width}d}"

def bank_account_no():
    return "".join(str(random.randint(0, 9)) for _ in range(16 + random.randint(0, 3)))

def tax_id():
    return "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(18))

def company_name():
    suffix = random.choice(["有限公司", "科技有限公司", "信息技术有限公司", "商贸有限公司", "咨询有限公司"])
    return fake.company() + suffix if not fake.company().endswith(("有限公司", "集团")) else fake.company()

def person_name():
    return fake.name()

def request_number(prefix, idx):
    return f"{prefix}-{random.randint(2023, 2025)}-{idx:06d}"

def month_period():
    year = random.randint(2023, 2025)
    month = random.randint(1, 12)
    return f"{year}-{month:02d}"

def fiscal_period_for_month(month: int):
    if month in (1, 2, 3):
        return "Q1"
    if month in (4, 5, 6):
        return "Q2"
    if month in (7, 8, 9):
        return "Q3"
    return "Q4"

def build_file_ref_pool(base):
    return list(base.get("file_attachment", {}).keys())

# ============================================================
# Parse Base
# ============================================================
base = json.loads(BASE_DATA_JSON)

# base table aliases
employees = base["employee"]
departments = base["department"]
positions = base["position"]
teams = base["team"]
file_attachments = base["file_attachment"]
department_members = base["department_member"]

employee_ids = list(employees.keys())
department_ids = list(departments.keys())
team_ids = list(teams.keys())
file_ids = list(file_attachments.keys())
position_ids = list(positions.keys())

active_employee_ids = [k for k, v in employees.items() if v["employment_status"] == "active"]
non_terminated_employee_ids = [k for k, v in employees.items() if v["employment_status"] != "terminated"]
finance_department_ids = [d for d, v in departments.items() if v["department_code"] == "FIN"] or department_ids

employee_primary_department = {}
for _, dm in department_members.items():
    if dm["is_primary"]:
        employee_primary_department[dm["employee_ref"]] = dm["department_ref"]

employee_position_level = {
    e_id: positions[emp["position_ref"]]["position_level"]
    for e_id, emp in employees.items()
    if emp["position_ref"] in positions
}

# ============================================================
# Dependency maps / output containers
# ============================================================
result = {}

table_generation_order = [
    "financeaccounts", "budgets", "invoices", "invoiceheaders", "paymentexecutions",
    "receiptrecords", "refunds", "employeeloans", "loanrepayments", "settlements",
    "fundtransfers", "exchangerates", "taxfilings", "employeetaxrecords", "accrualentries",
    "expensepolicies", "financetickets", "creditapplications", "creditrepaymentschedules",
    "stocktradeorders", "financeapprovalflows", "budgetlines", "expensereports",
    "paymentrequests", "expenselines", "settlementlines"
]

fk_dependencies = {
    "financeaccounts": [("department_ref", "departments"), ("managed_by_ref", "employees")],
    "budgets": [("scope_ref", "scopes"), ("parent_budget_ref", "budgets"), ("approved_by_ref", "employees")],
    "budgetlines": [("budget_ref", "budgets")],
    "expensereports": [("applicant_ref", "employees"), ("department_ref", "departments"), ("trip_ref", "trips"), ("budget_ref", "budgets"), ("current_approver_ref", "employees")],
    "expenselines": [("expense_report_ref", "expensereports"), ("invoice_ref", "invoices"), ("receipt_file_ref", "file_attachment")],
    "invoices": [("associated_resource_ref", "associated_resources"), ("invoice_file_ref", "file_attachment"), ("recorded_by_ref", "employees")],
    "invoiceheaders": [],
    "paymentrequests": [("applicant_ref", "employees"), ("department_ref", "departments"), ("source_account_ref", "financeaccounts"), ("associated_resource_ref", "associated_resources"), ("budget_ref", "budgets"), ("current_approver_ref", "employees")],
    "paymentexecutions": [("payment_request_ref", "paymentrequests"), ("source_account_ref", "financeaccounts"), ("executed_by_ref", "employees")],
    "receiptrecords": [("finance_account_ref", "financeaccounts"), ("matched_resource_ref", "matched_resources"), ("recorded_by_ref", "employees")],
    "refunds": [("applicant_ref", "employees"), ("original_payment_ref", "paymentexecutions"), ("original_receipt_ref", "receiptrecords"), ("current_approver_ref", "employees")],
    "employeeloans": [("borrower_ref", "employees"), ("department_ref", "departments"), ("current_approver_ref", "employees"), ("offset_expense_report_ref", "expensereports")],
    "loanrepayments": [("employee_loan_ref", "employeeloans")],
    "settlements": [("current_approver_ref", "employees"), ("payment_request_ref", "paymentrequests"), ("prepared_by_ref", "employees")],
    "settlementlines": [("settlement_ref", "settlements"), ("invoice_ref", "invoices")],
    "fundtransfers": [("applicant_ref", "employees"), ("source_account_ref", "financeaccounts"), ("target_account_ref", "financeaccounts"), ("current_approver_ref", "employees")],
    "exchangerates": [],
    "taxfilings": [("filed_by_ref", "employees"), ("attachment_file_ref", "file_attachment")],
    "employeetaxrecords": [("employee_ref", "employees")],
    "accrualentries": [("department_ref", "departments"), ("prepared_by_ref", "employees"), ("approved_by_ref", "employees")],
    "expensepolicies": [],
    "financetickets": [("requester_ref", "employees"), ("assigned_to_ref", "employees"), ("related_resource_ref", "related_resources")],
    "creditapplications": [("applicant_ref", "employees"), ("reviewed_by_ref", "employees")],
    "creditrepaymentschedules": [("credit_application_ref", "creditapplications")],
    "stocktradeorders": [("employee_ref", "employees")],
    "financeapprovalflows": [("source_ref", "sources"), ("approver_ref", "employees")],
}

# ============================================================
# Registry helpers
# ============================================================
generated_id_registry = {
    "employees": employee_ids,
    "departments": department_ids,
    "teams": team_ids,
    "file_attachment": file_ids,
    "positions": position_ids,
    "budgets": [],
    "financeaccounts": [],
    "invoices": [],
    "invoiceheaders": [],
    "paymentexecutions": [],
    "receiptrecords": [],
    "refunds": [],
    "employeeloans": [],
    "loanrepayments": [],
    "settlements": [],
    "fundtransfers": [],
    "exchangerates": [],
    "taxfilings": [],
    "employeetaxrecords": [],
    "accrualentries": [],
    "expensepolicies": [],
    "financetickets": [],
    "creditapplications": [],
    "creditrepaymentschedules": [],
    "stocktradeorders": [],
    "financeapprovalflows": [],
    "budgetlines": [],
    "expensereports": [],
    "paymentrequests": [],
    "expenselines": [],
    "settlementlines": [],
}

associated_resource_pools = {
    "expense_report": lambda: generated_id_registry["expensereports"],
    "payment_request": lambda: generated_id_registry["paymentrequests"],
    "refund": lambda: generated_id_registry["refunds"],
    "employee_loan": lambda: generated_id_registry["employeeloans"],
    "settlement": lambda: generated_id_registry["settlements"],
    "fund_transfer": lambda: generated_id_registry["fundtransfers"],
    "budget": lambda: generated_id_registry["budgets"],
    "credit_application": lambda: generated_id_registry["creditapplications"],
    "tax_filing": lambda: generated_id_registry["taxfilings"],
    "invoice": lambda: generated_id_registry["invoices"],
    "receipt_record": lambda: generated_id_registry["receiptrecords"],
    "payment_execution": lambda: generated_id_registry["paymentexecutions"],
}

def dependency_exists(dep_name: str) -> bool:
    if dep_name in {"employees", "departments", "teams", "file_attachment", "positions"}:
        return True
    if dep_name in generated_id_registry:
        return len(generated_id_registry[dep_name]) >= 0
    if dep_name in {"scopes", "associated_resources", "matched_resources", "sources", "related_resources"}:
        return True
    if dep_name in {"trips"}:
        return True
    return False

def validate_dependencies(table_name: str):
    deps = fk_dependencies.get(table_name, [])
    missing = [target for _, target in deps if not dependency_exists(target)]
    if missing:
        raise ValueError(f"Missing dependencies before generating {table_name}: {missing}")

def register_table_ids(table_name: str, data: dict):
    generated_id_registry[table_name] = list(data.keys())

def random_employee(active_only=False, non_terminated=False):
    if active_only:
        return choose(active_employee_ids)
    if non_terminated:
        return choose(non_terminated_employee_ids)
    return choose(employee_ids)

def random_department():
    return choose(department_ids)

def random_team():
    return choose(team_ids)

def random_file(optional_prob=0.7):
    return choose(file_ids) if file_ids and maybe(optional_prob) else None

def random_scope_pair():
    scope_type = random.choice(BUDGET_SCOPE_TYPES)
    if scope_type == "department":
        return scope_type, random_department()
    if scope_type == "team":
        return scope_type, random_team()
    if scope_type == "company":
        return scope_type, None
    # project scope has no project table in provided/base, so keep null to satisfy soft scope design
    return scope_type, None

def random_associated_resource():
    choices = []
    for k, getter in associated_resource_pools.items():
        ids = getter()
        if ids:
            choices.append((k, ids))
    if not choices:
        return None, None
    rtype, ids = random.choice(choices)
    return rtype, choose(ids)

def build_finance_approver_chain(employee_ref):
    dept = employee_primary_department.get(employee_ref, random_department())
    manager = employees[employee_ref].get("direct_manager_ref")
    approver = manager if manager else random.choice(active_employee_ids[:10])
    return dept, approver

# ============================================================
# Volume planning
# ============================================================
EMP_COUNT = len(employee_ids)
MIN_PER_EMP = 2
HEAVY_COUNT = max(EMP_COUNT * MIN_PER_EMP, SCALE * 2)
CONFIG_MIN = 10

TABLE_COUNTS = {
    "financeaccounts": max(CONFIG_MIN, 20),
    "budgets": max(CONFIG_MIN, 24),
    "invoices": HEAVY_COUNT,
    "invoiceheaders": max(CONFIG_MIN, 20),
    "paymentexecutions": HEAVY_COUNT,
    "receiptrecords": HEAVY_COUNT,
    "refunds": HEAVY_COUNT,
    "employeeloans": HEAVY_COUNT,
    "loanrepayments": HEAVY_COUNT,
    "settlements": HEAVY_COUNT,
    "fundtransfers": HEAVY_COUNT,
    "exchangerates": max(CONFIG_MIN, 40),
    "taxfilings": HEAVY_COUNT,
    "employeetaxrecords": HEAVY_COUNT,
    "accrualentries": HEAVY_COUNT,
    "expensepolicies": max(CONFIG_MIN, 30),
    "financetickets": HEAVY_COUNT,
    "creditapplications": HEAVY_COUNT,
    "creditrepaymentschedules": HEAVY_COUNT,
    "stocktradeorders": HEAVY_COUNT,
    "financeapprovalflows": HEAVY_COUNT,
    "budgetlines": HEAVY_COUNT,
    "expensereports": HEAVY_COUNT,
    "paymentrequests": HEAVY_COUNT,
    "expenselines": HEAVY_COUNT,
    "settlementlines": HEAVY_COUNT,
}

# ============================================================
# 1. financeaccounts
# ============================================================
validate_dependencies("financeaccounts")
finance_account = {}
for i in range(1, TABLE_COUNTS["financeaccounts"] + 1):
    ref = sequential_ref("FACCT", i, 3)
    department_ref = random.choice(finance_department_ids) if maybe(0.6) else random_department()
    managed_by_ref = random_employee(active_only=True)
    currency = random.choice(CHINA_CURRENCIES)
    account_type = random.choice(FINANCE_ACCOUNT_TYPES)
    account_purpose = random.choice(FINANCE_ACCOUNT_PURPOSES)

    created_dt = random_datetime(datetime(2020, 1, 1), datetime(2025, 3, 1))
    balance_updated_at_dt = later_datetime(created_dt, 1, 120)
    updated_dt = later_datetime(balance_updated_at_dt, 0, 60)

    status = random.choices(FINANCE_ACCOUNT_STATUSES, weights=[80, 10, 10])[0]
    balance = round(random.uniform(10000, 5000000), 2)
    if status == "closed":
        balance = round(random.uniform(0, 10000), 2)

    finance_account[ref] = {
        "finance_account_ref": ref,
        "account_name": f"{departments[department_ref]['department_name']}{random.choice(['结算户', '运营户', '备用金账户', '工资账户', '税务账户'])}",
        "account_number": bank_account_no(),
        "bank_name": random.choice(["中国工商银行", "中国建设银行", "中国银行", "招商银行", "交通银行", "浦发银行"]),
        "bank_branch": fake.address().replace("\n", " ")[:30],
        "swift_code": fake.bothify(text="AAAA##BB###") if currency != "CNY" and maybe(0.7) else None,
        "currency": currency,
        "account_type": account_type,
        "account_purpose": account_purpose,
        "account_status": status,
        "balance": money(balance),
        "balance_updated_at": iso_datetime(balance_updated_at_dt),
        "department_ref": department_ref if maybe(0.8) else None,
        "managed_by_ref": managed_by_ref,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(updated_dt),
    }
result["finance_account"] = finance_account
register_table_ids("financeaccounts", finance_account)

# ============================================================
# 2. budgets
# ============================================================
validate_dependencies("budgets")
budget = {}
budget_refs = []
for i in range(1, TABLE_COUNTS["budgets"] + 1):
    ref = sequential_ref("BUDG", i, 3)
    year = random.choice([2024, 2025, 2026])
    month_pick = random.randint(1, 12)
    fiscal_period = random.choice([fiscal_period_for_month(month_pick), "H1", "H2", "annual"])
    budget_type = random.choice(BUDGET_TYPES)
    scope_type, scope_ref = random_scope_pair()

    parent_budget_ref = None
    if budget_refs and maybe(0.25):
        parent_budget_ref = choose(budget_refs)

    created_dt = random_datetime(datetime(2023, 1, 1), datetime(2025, 4, 1))
    submitted_dt = later_datetime(created_dt, 1, 30) if maybe(0.75) else None
    approved_dt = None

    status = random.choices(BUDGET_STATUSES, weights=[10, 10, 55, 5, 10, 10])[0]
    approved_by_ref = None
    if status in ("approved", "closed", "frozen"):
        approved_by_ref = random_employee(active_only=True)
        if submitted_dt is None:
            submitted_dt = later_datetime(created_dt, 1, 15)
        approved_dt = later_datetime(submitted_dt, 1, 20)
    elif status == "rejected":
        approved_by_ref = random_employee(active_only=True)
        if submitted_dt is None:
            submitted_dt = later_datetime(created_dt, 1, 15)
        approved_dt = later_datetime(submitted_dt, 1, 10)

    total_amount = money(random.uniform(50000, 3000000))
    allocated_amount = money(total_amount * random.uniform(0.3, 1.0))
    spent_amount = money(allocated_amount * random.uniform(0.0, 0.9))
    frozen_amount = money(max(0.0, allocated_amount - spent_amount) * random.uniform(0.0, 0.5))
    updated_dt = later_datetime(approved_dt or submitted_dt or created_dt, 0, 120)

    budget[ref] = {
        "budget_ref": ref,
        "budget_name": f"{year}年{random.choice(['部门', '项目', '专项', '经营'])}预算-{fake.word()}",
        "budget_code": f"BG-{year}-{i:04d}",
        "fiscal_year": year,
        "fiscal_period": fiscal_period,
        "budget_type": budget_type,
        "scope_type": scope_type,
        "scope_ref": scope_ref,
        "parent_budget_ref": parent_budget_ref,
        "currency": "CNY",
        "total_amount": total_amount,
        "allocated_amount": min(allocated_amount, total_amount),
        "spent_amount": min(spent_amount, allocated_amount),
        "frozen_amount": frozen_amount,
        "budget_status": status,
        "approved_by_ref": approved_by_ref,
        "approved_at": iso_datetime(approved_dt) if approved_dt else None,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(updated_dt),
    }
    budget_refs.append(ref)
result["budget"] = budget
register_table_ids("budgets", budget)

# ============================================================
# 3. invoices
# ============================================================
validate_dependencies("invoices")
invoice = {}
invoice_refs = []
for i in range(1, TABLE_COUNTS["invoices"] + 1):
    ref = sequential_ref("INV", i, 3)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW - timedelta(days=1))
    invoice_date_dt = created_dt - timedelta(days=random.randint(0, 20))
    recorded_by_ref = random_employee(non_terminated=True)

    amount_without_tax = money(random.uniform(100, 30000))
    tax_rate = random.choice([0.0, 0.01, 0.03, 0.06, 0.09, 0.13])
    tax_amount = money(amount_without_tax * tax_rate)
    total_amount = money(amount_without_tax + tax_amount)

    associated_resource_type, associated_resource_ref = (None, None)
    if maybe(0.5):
        associated_resource_type, associated_resource_ref = random_associated_resource()

    verification_status = random.choices(INVOICE_VERIFICATION_STATUSES, weights=[20, 65, 10, 5])[0]
    invoice_status = random.choices(INVOICE_STATUSES, weights=[80, 5, 5, 10])[0]

    updated_dt = later_datetime(created_dt, 0, 90)

    invoice[ref] = {
        "invoice_ref": ref,
        "invoice_number": "".join(str(random.randint(0, 9)) for _ in range(8)),
        "invoice_code": "".join(str(random.randint(0, 9)) for _ in range(10)),
        "invoice_type": random.choice(INVOICE_TYPES),
        "invoice_direction": random.choice(INVOICE_DIRECTIONS),
        "invoice_date": iso_date(invoice_date_dt),
        "currency": "CNY",
        "amount_without_tax": amount_without_tax,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "tax_rate": tax_rate,
        "seller_name": company_name(),
        "seller_tax_id": tax_id(),
        "buyer_name": random.choice(["智联科技有限公司", "智联科技集团", company_name()]),
        "buyer_tax_id": tax_id(),
        "items_summary": f"{random.choice(['技术服务', '办公用品', '软件许可', '培训服务', '差旅服务', '咨询服务'])}费用",
        "verification_status": verification_status,
        "verification_code": "".join(str(random.randint(0, 9)) for _ in range(20)) if maybe(0.6) else None,
        "associated_resource_type": associated_resource_type,
        "associated_resource_ref": associated_resource_ref,
        "invoice_file_ref": random_file(0.7),
        "invoice_status": invoice_status,
        "recorded_by_ref": recorded_by_ref,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(updated_dt),
    }
    invoice_refs.append(ref)
result["invoice"] = invoice
register_table_ids("invoices", invoice)

# ============================================================
# 4. invoiceheaders
# ============================================================
validate_dependencies("invoiceheaders")
invoice_header = {}
for i in range(1, TABLE_COUNTS["invoiceheaders"] + 1):
    ref = sequential_ref("IHDR", i, 3)
    created_dt = random_datetime(datetime(2021, 1, 1), NOW - timedelta(days=30))
    updated_dt = later_datetime(created_dt, 0, 120)

    header_type = random.choices(INVOICE_HEADER_TYPES, weights=[85, 15])[0]
    is_default = (i == 1)
    invoice_header[ref] = {
        "invoice_header_ref": ref,
        "header_type": header_type,
        "company_name": "智联科技有限公司" if header_type == "company" else person_name(),
        "tax_id": tax_id(),
        "registered_address": fake.address().replace("\n", " "),
        "registered_phone": fake.phone_number(),
        "bank_name": random.choice(["中国工商银行", "招商银行", "中国建设银行", "中国银行"]),
        "bank_account": bank_account_no(),
        "is_default": is_default,
        "header_status": random.choices(INVOICE_HEADER_STATUSES, weights=[85, 15])[0],
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(updated_dt),
    }
result["invoice_header"] = invoice_header
register_table_ids("invoiceheaders", invoice_header)

# ============================================================
# 5. paymentexecutions
# ============================================================
validate_dependencies("paymentexecutions")
payment_execution = {}
for i in range(1, TABLE_COUNTS["paymentexecutions"] + 1):
    ref = sequential_ref("PEXE", i, 3)
    source_account_ref = choose(generated_id_registry["financeaccounts"])
    source_account = finance_account[source_account_ref]
    created_dt = random_datetime(datetime(2023, 1, 1), NOW - timedelta(days=1))
    status = random.choices(PAYMENT_EXECUTION_STATUSES, weights=[10, 20, 55, 10, 5])[0]

    amount = money(random.uniform(200, 100000))
    currency = source_account["currency"]
    settlement_currency = None
    settlement_amount = None
    exchange_rate = None

    if maybe(0.15) and currency != "USD":
        settlement_currency = "USD"
        exchange_rate = round(random.uniform(0.12, 1.5), 6)
        settlement_amount = money(amount * exchange_rate)

    executed_at = None
    failure_reason = None
    if status in ("completed", "reversed"):
        executed_at = iso_datetime(later_datetime(created_dt, 1, 20))
    elif status == "failed":
        executed_at = iso_datetime(later_datetime(created_dt, 1, 10))
        failure_reason = random.choice(["账户信息错误", "余额不足", "银行通道异常", "风控拦截"])

    updated_dt = parse_dt(executed_at) if executed_at else later_datetime(created_dt, 0, 30)

    payment_execution[ref] = {
        "payment_execution_ref": ref,
        "payment_request_ref": None,  # requests generated later; keep null-safe by post generation impossible in strict order
        "source_account_ref": source_account_ref,
        "transaction_number": f"TXN{random.randint(10000000, 99999999)}",
        "currency": currency,
        "amount": amount,
        "exchange_rate": exchange_rate,
        "settlement_currency": settlement_currency,
        "settlement_amount": settlement_amount,
        "payee_name": person_name() if maybe(0.4) else company_name(),
        "payee_account": bank_account_no(),
        "payee_bank": random.choice(["中国银行", "建设银行", "工商银行", "招商银行", "支付宝", "微信支付"]),
        "payment_channel": random.choice(PAYMENT_CHANNELS),
        "execution_status": status,
        "executed_at": executed_at,
        "executed_by_ref": random_employee(active_only=True),
        "failure_reason": failure_reason,
        "bank_reference": f"BK{random.randint(1000000, 9999999)}" if maybe(0.8) else None,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(updated_dt),
    }
result["payment_execution"] = payment_execution
register_table_ids("paymentexecutions", payment_execution)

# ============================================================
# 6. receiptrecords
# ============================================================
validate_dependencies("receiptrecords")
receipt_record = {}
for i in range(1, TABLE_COUNTS["receiptrecords"] + 1):
    ref = sequential_ref("RCPT", i, 3)
    finance_account_ref = choose(generated_id_registry["financeaccounts"])
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    receipt_date_dt = created_dt - timedelta(days=random.randint(0, 7))
    reconciliation_status = random.choices(RECONCILIATION_STATUSES, weights=[30, 50, 10, 10])[0]

    matched_resource_type = None
    matched_resource_ref = None
    if reconciliation_status in ("matched", "partial_matched", "disputed"):
        matched_resource_type, matched_resource_ref = random_associated_resource()

    receipt_record[ref] = {
        "receipt_record_ref": ref,
        "receipt_number": request_number("RR", i),
        "finance_account_ref": finance_account_ref,
        "payer_name": company_name() if maybe(0.7) else person_name(),
        "payer_account": bank_account_no(),
        "currency": finance_account[finance_account_ref]["currency"],
        "amount": money(random.uniform(500, 300000)),
        "receipt_date": iso_date(receipt_date_dt),
        "receipt_channel": random.choice(RECEIPT_CHANNELS),
        "receipt_type": random.choice(RECEIPT_TYPES),
        "reconciliation_status": reconciliation_status,
        "matched_resource_type": matched_resource_type,
        "matched_resource_ref": matched_resource_ref,
        "bank_reference": f"IN{random.randint(1000000, 9999999)}" if maybe(0.7) else None,
        "notes": zh_sentence(),
        "recorded_by_ref": random_employee(non_terminated=True),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(later_datetime(created_dt, 0, 20)),
    }
result["receipt_record"] = receipt_record
register_table_ids("receiptrecords", receipt_record)

# ============================================================
# 7. refunds
# ============================================================
validate_dependencies("refunds")
refund = {}
for i in range(1, TABLE_COUNTS["refunds"] + 1):
    ref = sequential_ref("RFND", i, 3)
    applicant_ref = random_employee(non_terminated=True)
    dept_ref, approver_ref = build_finance_approver_chain(applicant_ref)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    submitted_at = later_datetime(created_dt, 1, 15) if maybe(0.8) else None
    status = random.choices(REFUND_STATUSES, weights=[10, 10, 15, 20, 5, 15, 20, 5])[0]

    approved_at = None
    executed_at = None
    rejected_reason = None
    if status in ("approved", "processing", "completed"):
        if submitted_at is None:
            submitted_at = later_datetime(created_dt, 1, 10)
        approved_at = later_datetime(submitted_at, 1, 15)
        if status == "completed":
            executed_at = later_datetime(approved_at, 1, 15)
    elif status == "rejected":
        if submitted_at is None:
            submitted_at = later_datetime(created_dt, 1, 8)
        rejected_reason = random.choice(["资料不完整", "超出退款政策范围", "原始交易无法核实"])

    original_payment_ref = choose(generated_id_registry["paymentexecutions"]) if maybe(0.5) else None
    original_receipt_ref = choose(generated_id_registry["receiptrecords"]) if maybe(0.5) else None
    refund_method = random.choice(REFUND_METHODS)

    refund[ref] = {
        "refund_ref": ref,
        "refund_number": request_number("RF", i),
        "applicant_ref": applicant_ref,
        "refund_type": random.choice(REFUND_TYPES),
        "customer_name": company_name() if maybe(0.7) else person_name(),
        "original_payment_ref": original_payment_ref,
        "original_receipt_ref": original_receipt_ref,
        "currency": "CNY",
        "refund_amount": money(random.uniform(100, 50000)),
        "reason_category": random.choice(REFUND_REASON_CATEGORIES),
        "reason_detail": zh_sentence(),
        "refund_method": refund_method,
        "target_account": bank_account_no() if refund_method in ("bank_transfer",) and maybe(0.8) else None,
        "refund_status": status,
        "current_approver_ref": approver_ref if status in ("submitted", "under_review") else None,
        "submitted_at": iso_datetime(submitted_at) if submitted_at else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "executed_at": iso_datetime(executed_at) if executed_at else None,
        "rejected_reason": rejected_reason,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(executed_at or approved_at or submitted_at or later_datetime(created_dt, 0, 10)),
    }
result["refund"] = refund
register_table_ids("refunds", refund)

# ============================================================
# 8. employeeloans
# ============================================================
validate_dependencies("employeeloans")
employee_loan = {}
loan_refs = []
for i in range(1, TABLE_COUNTS["employeeloans"] + 1):
    ref = sequential_ref("ELOAN", i, 3)
    borrower_ref = choose(non_terminated_employee_ids)
    department_ref = employee_primary_department.get(borrower_ref, random_department())
    current_approver_ref = employees[borrower_ref].get("direct_manager_ref") or random_employee(active_only=True)

    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    loan_date_dt = created_dt + timedelta(days=random.randint(0, 7))
    due_date_dt = loan_date_dt + timedelta(days=random.randint(30, 180))
    status = random.choices(EMPLOYEE_LOAN_STATUSES, weights=[8, 8, 14, 4, 36, 20, 8, 2])[0]

    loan_amount = money(random.uniform(1000, 50000))
    repaid_amount = 0.0
    approved_at = None
    disbursed_at = None
    settled_at = None

    if status in ("approved", "active", "settled", "overdue", "written_off"):
        approved_at = later_datetime(created_dt, 1, 15)
    if status in ("active", "settled", "overdue", "written_off"):
        disbursed_at = later_datetime(approved_at, 1, 10)
    if status == "settled":
        repaid_amount = loan_amount
        settled_at = later_datetime(disbursed_at, 20, 180)
    elif status == "active":
        repaid_amount = money(loan_amount * random.uniform(0.0, 0.8))
    elif status == "overdue":
        repaid_amount = money(loan_amount * random.uniform(0.0, 0.5))
        due_date_dt = NOW - timedelta(days=random.randint(1, 120))
    elif status == "written_off":
        repaid_amount = money(loan_amount * random.uniform(0.0, 0.3))

    outstanding_amount = money(loan_amount - repaid_amount)

    employee_loan[ref] = {
        "employee_loan_ref": ref,
        "loan_number": request_number("EL", i),
        "borrower_ref": borrower_ref,
        "department_ref": department_ref,
        "loan_purpose": random.choice(LOAN_PURPOSES),
        "currency": "CNY",
        "loan_amount": loan_amount,
        "repaid_amount": repaid_amount,
        "outstanding_amount": outstanding_amount,
        "loan_date": iso_date(loan_date_dt),
        "due_date": iso_date(due_date_dt),
        "loan_status": status,
        "current_approver_ref": current_approver_ref if status in ("submitted", "approved") else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "disbursed_at": iso_datetime(disbursed_at) if disbursed_at else None,
        "settled_at": iso_datetime(settled_at) if settled_at else None,
        "offset_expense_report_ref": None,  # generated later; keep null in initial load
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(settled_at or disbursed_at or approved_at or later_datetime(created_dt, 0, 30)),
    }
    loan_refs.append(ref)
result["employee_loan"] = employee_loan
register_table_ids("employeeloans", employee_loan)

# ============================================================
# 9. loanrepayments
# ============================================================
validate_dependencies("loanrepayments")
loan_repayment = {}
for i in range(1, TABLE_COUNTS["loanrepayments"] + 1):
    ref = sequential_ref("LREP", i, 3)
    loan_ref = choose(loan_refs)
    loan = employee_loan[loan_ref]
    created_dt = random_datetime(parse_dt(loan["created_at"]), NOW)

    max_amt = max(100.0, loan["loan_amount"] * 0.5)
    repay_amt = money(random.uniform(100, max_amt))

    loan_repayment[ref] = {
        "loan_repayment_ref": ref,
        "employee_loan_ref": loan_ref,
        "repayment_amount": repay_amt,
        "repayment_method": random.choice(REPAYMENT_METHODS),
        "repayment_date": iso_date(created_dt),
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
    }
result["loan_repayment"] = loan_repayment
register_table_ids("loanrepayments", loan_repayment)

# ============================================================
# 10. settlements
# ============================================================
validate_dependencies("settlements")
settlement = {}
settlement_refs = []
for i in range(1, TABLE_COUNTS["settlements"] + 1):
    ref = sequential_ref("STLM", i, 3)
    prepared_by_ref = random_employee(non_terminated=True)
    period_start = random_datetime(datetime(2023, 1, 1), NOW - timedelta(days=30))
    period_end = period_start + timedelta(days=random.randint(15, 60))
    created_dt = later_datetime(period_end, 1, 20)

    gross_amount = money(random.uniform(2000, 500000))
    adjustment_amount = money(random.uniform(-5000, 5000))
    net_amount = money(max(0, gross_amount + adjustment_amount))
    status = random.choices(SETTLEMENT_STATUSES, weights=[8, 12, 25, 5, 40, 10])[0]

    submitted_at = later_datetime(created_dt, 1, 15) if status != "draft" else None
    approved_at = later_datetime(submitted_at, 1, 15) if status in ("approved", "settled") and submitted_at else None
    settled_at = later_datetime(approved_at, 1, 20) if status == "settled" and approved_at else None

    settlement[ref] = {
        "settlement_ref": ref,
        "settlement_number": request_number("ST", i),
        "counterparty_type": random.choice(SETTLEMENT_COUNTERPARTY_TYPES),
        "counterparty_name": company_name() if maybe(0.8) else person_name(),
        "counterparty_id": tax_id(),
        "settlement_period_start": iso_date(period_start),
        "settlement_period_end": iso_date(period_end),
        "currency": "CNY",
        "gross_amount": gross_amount,
        "adjustment_amount": adjustment_amount,
        "net_amount": net_amount,
        "settlement_status": status,
        "current_approver_ref": random_employee(active_only=True) if status in ("submitted", "approved") else None,
        "submitted_at": iso_datetime(submitted_at) if submitted_at else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "settled_at": iso_datetime(settled_at) if settled_at else None,
        "payment_request_ref": None,  # generated later
        "notes": zh_sentence(),
        "prepared_by_ref": prepared_by_ref,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(settled_at or approved_at or submitted_at or later_datetime(created_dt, 0, 30)),
    }
    settlement_refs.append(ref)
result["settlement"] = settlement
register_table_ids("settlements", settlement)

# ============================================================
# 11. fundtransfers
# ============================================================
validate_dependencies("fundtransfers")
fund_transfer = {}
for i in range(1, TABLE_COUNTS["fundtransfers"] + 1):
    ref = sequential_ref("FTRN", i, 3)
    applicant_ref = random_employee(non_terminated=True)
    source_account_ref = choose(generated_id_registry["financeaccounts"])
    target_account_ref = choose(generated_id_registry["financeaccounts"])
    while target_account_ref == source_account_ref:
        target_account_ref = choose(generated_id_registry["financeaccounts"])

    source_currency = finance_account[source_account_ref]["currency"]
    target_currency = finance_account[target_account_ref]["currency"]

    amount = money(random.uniform(1000, 300000))
    exchange_rate = None
    target_amount = None
    target_currency_field = None
    if source_currency != target_currency:
        exchange_rate = round(random.uniform(0.1, 10.0), 6)
        target_currency_field = target_currency
        target_amount = money(amount * exchange_rate)

    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(FUND_TRANSFER_STATUSES, weights=[10, 10, 20, 5, 40, 10, 5])[0]
    approved_at = later_datetime(created_dt, 1, 10) if status in ("approved", "executed") else None
    executed_at = later_datetime(approved_at, 1, 10) if status == "executed" and approved_at else None

    fund_transfer[ref] = {
        "fund_transfer_ref": ref,
        "transfer_number": request_number("FT", i),
        "applicant_ref": applicant_ref,
        "source_account_ref": source_account_ref,
        "target_account_ref": target_account_ref,
        "currency": source_currency,
        "amount": amount,
        "exchange_rate": exchange_rate,
        "target_currency": target_currency_field,
        "target_amount": target_amount,
        "transfer_reason": zh_sentence(),
        "transfer_status": status,
        "current_approver_ref": random_employee(active_only=True) if status in ("submitted", "approved") else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "executed_at": iso_datetime(executed_at) if executed_at else None,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(executed_at or approved_at or later_datetime(created_dt, 0, 15)),
    }
result["fund_transfer"] = fund_transfer
register_table_ids("fundtransfers", fund_transfer)

# ============================================================
# 12. exchangerates
# ============================================================
validate_dependencies("exchangerates")
exchange_rate = {}
pairs = [
    ("USD", "CNY"), ("EUR", "CNY"), ("GBP", "CNY"), ("JPY", "CNY"),
    ("HKD", "CNY"), ("SGD", "CNY"), ("KRW", "CNY"), ("TWD", "CNY"),
    ("USD", "HKD"), ("EUR", "USD")
]
for i in range(1, TABLE_COUNTS["exchangerates"] + 1):
    ref = sequential_ref("EXRT", i, 3)
    src, tgt = pairs[(i - 1) % len(pairs)]
    effective_dt = random_datetime(datetime(2023, 1, 1), NOW)

    rate_base = {
        ("USD", "CNY"): 7.2,
        ("EUR", "CNY"): 7.8,
        ("GBP", "CNY"): 9.0,
        ("JPY", "CNY"): 0.048,
        ("HKD", "CNY"): 0.92,
        ("SGD", "CNY"): 5.3,
        ("KRW", "CNY"): 0.0054,
        ("TWD", "CNY"): 0.23,
        ("USD", "HKD"): 7.8,
        ("EUR", "USD"): 1.08,
    }.get((src, tgt), random.uniform(0.1, 10))
    rate = round(rate_base * random.uniform(0.95, 1.05), 6)

    exchange_rate[ref] = {
        "exchange_rate_ref": ref,
        "source_currency": src,
        "target_currency": tgt,
        "rate": rate,
        "rate_type": random.choice(EXCHANGE_RATE_TYPES),
        "effective_date": iso_date(effective_dt),
        "created_at": iso_datetime(effective_dt),
    }
result["exchange_rate"] = exchange_rate
register_table_ids("exchangerates", exchange_rate)

# ============================================================
# 13. taxfilings
# ============================================================
validate_dependencies("taxfilings")
tax_filing = {}
tax_filing_refs = []
for i in range(1, TABLE_COUNTS["taxfilings"] + 1):
    ref = sequential_ref("TFLG", i, 3)
    start_dt = random_datetime(datetime(2023, 1, 1), NOW - timedelta(days=60))
    end_dt = start_dt + timedelta(days=random.choice([29, 30, 31, 89, 179]))
    deadline_dt = end_dt + timedelta(days=random.randint(10, 30))
    created_dt = later_datetime(start_dt, 0, 15, hard_end=end_dt)
    status = random.choices(TAX_FILING_STATUSES, weights=[10, 15, 30, 30, 10, 5])[0]

    taxable_amount = money(random.uniform(10000, 1000000))
    tax_rate_val = random.choice([0.03, 0.06, 0.09, 0.13, 0.20, 0.25])
    tax_amount_val = money(taxable_amount * tax_rate_val)
    deductions_amount = money(tax_amount_val * random.uniform(0.0, 0.3))
    payable_amount = money(max(0, tax_amount_val - deductions_amount))

    filed_at = later_datetime(created_dt, 1, 20) if status in ("filed", "accepted", "rejected", "amended") else None
    confirmation_number = f"TAX{random.randint(100000, 999999)}" if filed_at and maybe(0.8) else None

    tax_filing[ref] = {
        "tax_filing_ref": ref,
        "filing_number": request_number("TF", i),
        "tax_type": random.choice(TAX_TYPES),
        "filing_period_start": iso_date(start_dt),
        "filing_period_end": iso_date(end_dt),
        "filing_deadline": iso_date(deadline_dt),
        "currency": "CNY",
        "taxable_amount": taxable_amount,
        "tax_rate": tax_rate_val,
        "tax_amount": tax_amount_val,
        "deductions_amount": deductions_amount,
        "payable_amount": payable_amount,
        "filing_status": status,
        "filed_at": iso_datetime(filed_at) if filed_at else None,
        "filed_by_ref": random_employee(active_only=True),
        "confirmation_number": confirmation_number,
        "attachment_file_ref": random_file(0.6),
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(filed_at or later_datetime(created_dt, 0, 20)),
    }
    tax_filing_refs.append(ref)
result["tax_filing"] = tax_filing
register_table_ids("taxfilings", tax_filing)

# ============================================================
# 14. employeetaxrecords
# ============================================================
validate_dependencies("employeetaxrecords")
employee_tax_record = {}
for i in range(1, TABLE_COUNTS["employeetaxrecords"] + 1):
    ref = sequential_ref("ETAX", i, 3)
    employee_ref = employee_ids[(i - 1) % len(employee_ids)]
    tax_period = month_period()
    gross_income = money(random.uniform(5000, 80000))
    taxable_income = money(gross_income * random.uniform(0.6, 0.95))
    social = money(gross_income * random.uniform(0.08, 0.12))
    housing = money(gross_income * random.uniform(0.05, 0.12))
    special = {
        "children_education": money(random.choice([0, 1000, 2000])),
        "continuing_education": money(random.choice([0, 400, 800])),
        "housing_loan_interest": money(random.choice([0, 1000])),
        "housing_rent": money(random.choice([0, 800, 1100, 1500])),
        "elderly_care": money(random.choice([0, 1000, 2000, 3000])),
        "infant_care": money(random.choice([0, 1000, 2000])),
        "serious_illness": money(random.choice([0, 500, 1000, 2000])),
    }
    other_ded = money(random.uniform(0, 1000))
    cumulative_income_ytd = money(gross_income * random.uniform(2, 12))
    tax_rate_applied = random.choice([0.03, 0.10, 0.20, 0.25])
    quick_deduction = random.choice([0, 210, 1410, 2660])
    tax_withheld = money(max(0, taxable_income * tax_rate_applied - quick_deduction))
    tax_paid = tax_withheld if maybe(0.9) else money(tax_withheld * random.uniform(0.5, 1.0))
    cumulative_tax_ytd = money(tax_paid * random.uniform(2, 12))
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)

    employee_tax_record[ref] = {
        "employee_tax_record_ref": ref,
        "employee_ref": employee_ref,
        "tax_period": tax_period,
        "gross_income": gross_income,
        "income_type": random.choice(INCOME_TYPES),
        "taxable_income": taxable_income,
        "tax_exempt_amount": 5000.0,
        "social_insurance_deduction": social,
        "housing_fund_deduction": housing,
        "special_additional_deductions": special,
        "other_deductions": other_ded,
        "cumulative_income_ytd": cumulative_income_ytd,
        "cumulative_tax_ytd": cumulative_tax_ytd,
        "tax_rate_applied": tax_rate_applied,
        "quick_deduction": quick_deduction,
        "tax_withheld": tax_withheld,
        "tax_paid": tax_paid,
        "filing_status": random.choice(EMPLOYEE_TAX_FILING_STATUSES),
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(later_datetime(created_dt, 0, 15)),
    }
result["employee_tax_record"] = employee_tax_record
register_table_ids("employeetaxrecords", employee_tax_record)

# ============================================================
# 15. accrualentries
# ============================================================
validate_dependencies("accrualentries")
accrual_entry = {}
for i in range(1, TABLE_COUNTS["accrualentries"] + 1):
    ref = sequential_ref("ACRL", i, 3)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(ACCRUAL_ENTRY_STATUSES, weights=[10, 60, 20, 10])[0]
    posted_or_reversed_dt = later_datetime(created_dt, 1, 20)

    approved_by_ref = random_employee(active_only=True) if status in ("posted", "reversed") else None
    reversed_at = iso_datetime(later_datetime(posted_or_reversed_dt, 1, 25)) if status == "reversed" else None

    accrual_entry[ref] = {
        "accrual_entry_ref": ref,
        "entry_number": request_number("AC", i),
        "accrual_type": random.choice(ACCRUAL_TYPES),
        "accounting_period": month_period(),
        "department_ref": random_department() if maybe(0.8) else None,
        "expense_category": random.choice(EXPENSE_CATEGORIES),
        "description": zh_sentence(),
        "currency": "CNY",
        "amount": money(random.uniform(1000, 200000)),
        "reversal_period": month_period() if maybe(0.5) else None,
        "is_reversed": status == "reversed",
        "reversed_at": reversed_at,
        "entry_status": status,
        "prepared_by_ref": random_employee(non_terminated=True),
        "approved_by_ref": approved_by_ref,
        "created_at": iso_datetime(created_dt),
        "updated_at": reversed_at or iso_datetime(posted_or_reversed_dt if status != "draft" else later_datetime(created_dt, 0, 10)),
    }
result["accrual_entry"] = accrual_entry
register_table_ids("accrualentries", accrual_entry)

# ============================================================
# 16. expensepolicies
# ============================================================
validate_dependencies("expensepolicies")
expense_policy = {}
for i in range(1, TABLE_COUNTS["expensepolicies"] + 1):
    ref = sequential_ref("EPOL", i, 3)
    created_dt = random_datetime(datetime(2022, 1, 1), NOW - timedelta(days=90))
    effective_from_dt = later_datetime(created_dt, 0, 30)
    effective_to_dt = later_datetime(effective_from_dt, 180, 720) if maybe(0.3) else None

    expense_policy[ref] = {
        "expense_policy_ref": ref,
        "policy_name": f"{random.choice(['差旅', '住宿', '餐饮', '培训', '交通'])}报销政策-{i}",
        "policy_code": f"POL-{i:04d}",
        "expense_category": random.choice(EXPENSE_CATEGORIES),
        "applicable_position_levels": sorted(sample_n(list(range(1, 10)), 1, 4)),
        "applicable_worker_types": sample_n(["full_time", "intern", "campus_recruit", "campus_intern", "contractor"], 1, 3),
        "city_tier": random.choice(CITY_TIERS),
        "currency": "CNY",
        "daily_limit": money(random.uniform(100, 2000)) if maybe(0.8) else None,
        "per_occurrence_limit": money(random.uniform(50, 5000)) if maybe(0.8) else None,
        "monthly_limit": money(random.uniform(500, 10000)) if maybe(0.5) else None,
        "requires_invoice": maybe(0.85),
        "requires_pre_approval": maybe(0.4),
        "policy_detail": zh_sentence(15, 25),
        "effective_from": iso_date(effective_from_dt),
        "effective_to": iso_date(effective_to_dt) if effective_to_dt else None,
        "policy_status": random.choices(EXPENSE_POLICY_STATUSES, weights=[75, 15, 10])[0],
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(later_datetime(created_dt, 0, 60)),
    }
result["expense_policy"] = expense_policy
register_table_ids("expensepolicies", expense_policy)

# ============================================================
# 17. financetickets
# ============================================================
validate_dependencies("financetickets")
finance_ticket = {}
for i in range(1, TABLE_COUNTS["financetickets"] + 1):
    ref = sequential_ref("FTKT", i, 3)
    requester_ref = random_employee(non_terminated=True)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(FINANCE_TICKET_STATUSES, weights=[20, 20, 10, 25, 20, 5])[0]

    assigned_to_ref = random_employee(active_only=True) if status != "open" or maybe(0.6) else None
    related_resource_type, related_resource_ref = (None, None)
    if maybe(0.6):
        related_resource_type, related_resource_ref = random_associated_resource()

    resolved_at = None
    resolution = None
    if status in ("resolved", "closed"):
        resolved_dt = later_datetime(created_dt, 1, 20)
        resolved_at = iso_datetime(resolved_dt)
        resolution = random.choice([
            "已核实并完成修正",
            "已按财务政策解释处理",
            "已补充资料并通过复核",
            "系统问题已转开发修复"
        ])

    finance_ticket[ref] = {
        "finance_ticket_ref": ref,
        "ticket_number": request_number("TK", i),
        "requester_ref": requester_ref,
        "ticket_category": random.choice(FINANCE_TICKET_CATEGORIES),
        "ticket_subcategory": random.choice(FINANCE_TICKET_SUBCATEGORIES),
        "subject": zh_title("财务问题："),
        "description": zh_sentence(15, 30),
        "priority": random.choices(FINANCE_TICKET_PRIORITIES, weights=[10, 60, 20, 10])[0],
        "ticket_status": status,
        "assigned_to_ref": assigned_to_ref,
        "related_resource_type": related_resource_type,
        "related_resource_ref": related_resource_ref,
        "resolution": resolution,
        "resolved_at": resolved_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": resolved_at or iso_datetime(later_datetime(created_dt, 0, 15)),
    }
result["finance_ticket"] = finance_ticket
register_table_ids("financetickets", finance_ticket)

# ============================================================
# 18. creditapplications
# ============================================================
validate_dependencies("creditapplications")
credit_application = {}
credit_app_refs = []
for i in range(1, TABLE_COUNTS["creditapplications"] + 1):
    ref = sequential_ref("CAPP", i, 3)
    applicant_ref = random_employee(non_terminated=True)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(CREDIT_APPLICATION_STATUSES, weights=[8, 10, 12, 15, 5, 10, 20, 10, 5, 3, 2])[0]

    requested_amount = money(random.uniform(5000, 500000))
    approved_amount = None
    interest_rate = None
    credit_score = random.randint(450, 850) if maybe(0.9) else None
    risk_level = random.choice(CREDIT_RISK_LEVELS) if credit_score else None
    reviewed_by_ref = random_employee(active_only=True) if status not in ("draft", "submitted") else None

    approved_at = None
    disbursed_at = None
    maturity_date = None
    outstanding_balance = None
    next_payment_date = None
    next_payment_amount = None
    loan_term_months = random.choice([6, 12, 24, 36, 48, 60])

    if status in ("approved", "disbursed", "repaying", "settled", "overdue", "defaulted"):
        approved_amount = money(requested_amount * random.uniform(0.6, 1.0))
        interest_rate = round(random.uniform(0.032, 0.12), 4)
        approved_at = later_datetime(created_dt, 1, 20)
        maturity_date = iso_date(approved_at + timedelta(days=loan_term_months * 30))
    if status in ("disbursed", "repaying", "settled", "overdue", "defaulted"):
        disbursed_at = later_datetime(approved_at, 1, 10)
        outstanding_balance = money(approved_amount * random.uniform(0.1, 1.0))
        next_payment_date = iso_date(disbursed_at + timedelta(days=30))
        next_payment_amount = money(approved_amount / loan_term_months)

    if status == "settled":
        outstanding_balance = 0.0
        next_payment_date = None
        next_payment_amount = None

    credit_application[ref] = {
        "credit_application_ref": ref,
        "application_number": request_number("CA", i),
        "applicant_ref": applicant_ref,
        "product_type": random.choice(CREDIT_PRODUCT_TYPES),
        "currency": "CNY",
        "requested_amount": requested_amount,
        "approved_amount": approved_amount,
        "interest_rate": interest_rate,
        "loan_term_months": loan_term_months,
        "repayment_method": random.choice(CREDIT_REPAYMENT_METHODS),
        "purpose": zh_sentence(),
        "credit_score": credit_score,
        "risk_level": risk_level,
        "application_status": status,
        "reviewed_by_ref": reviewed_by_ref,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "disbursed_at": iso_datetime(disbursed_at) if disbursed_at else None,
        "maturity_date": maturity_date,
        "outstanding_balance": outstanding_balance,
        "next_payment_date": next_payment_date,
        "next_payment_amount": next_payment_amount,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(disbursed_at or approved_at or later_datetime(created_dt, 0, 20)),
    }
    credit_app_refs.append(ref)
result["credit_application"] = credit_application
register_table_ids("creditapplications", credit_application)

# ============================================================
# 19. creditrepaymentschedules
# ============================================================
validate_dependencies("creditrepaymentschedules")
credit_repayment_schedule = {}
for i in range(1, TABLE_COUNTS["creditrepaymentschedules"] + 1):
    ref = sequential_ref("CRPS", i, 3)
    app_ref = choose(credit_app_refs)
    app = credit_application[app_ref]
    created_dt = parse_dt(app["created_at"])
    installment_number = random.randint(1, max(1, app["loan_term_months"]))
    due_date_dt = created_dt + timedelta(days=installment_number * 30)

    principal_amount = money((app["approved_amount"] or app["requested_amount"]) / max(1, app["loan_term_months"]))
    interest_amount = money(principal_amount * random.uniform(0.002, 0.01))
    total_amount = money(principal_amount + interest_amount)
    status = random.choices(CREDIT_SCHEDULE_STATUSES, weights=[40, 35, 10, 10, 5])[0]
    paid_amount = 0.0
    paid_at = None
    if status == "paid":
        paid_amount = total_amount
        paid_at = iso_datetime(later_datetime(due_date_dt - timedelta(days=15), 0, 20))
    elif status == "partial_paid":
        paid_amount = money(total_amount * random.uniform(0.2, 0.8))
        paid_at = iso_datetime(later_datetime(due_date_dt - timedelta(days=10), 0, 20))
    elif status == "waived":
        paid_amount = 0.0

    credit_repayment_schedule[ref] = {
        "credit_repayment_schedule_ref": ref,
        "credit_application_ref": app_ref,
        "installment_number": installment_number,
        "due_date": iso_date(due_date_dt),
        "principal_amount": principal_amount,
        "interest_amount": interest_amount,
        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "paid_at": paid_at,
        "schedule_status": status,
        "created_at": iso_datetime(created_dt),
    }
result["credit_repayment_schedule"] = credit_repayment_schedule
register_table_ids("creditrepaymentschedules", credit_repayment_schedule)

# ============================================================
# 20. stocktradeorders
# ============================================================
validate_dependencies("stocktradeorders")
stock_trade_order = {}
stock_pool = [
    ("600519", "贵州茅台", "SSE", "CNY"),
    ("000858", "五粮液", "SZSE", "CNY"),
    ("00700", "腾讯控股", "HKEX", "HKD"),
    ("09988", "阿里巴巴", "HKEX", "HKD"),
    ("AAPL", "苹果", "NASDAQ", "USD"),
    ("MSFT", "微软", "NASDAQ", "USD"),
]
for i in range(1, TABLE_COUNTS["stocktradeorders"] + 1):
    ref = sequential_ref("STOD", i, 3)
    code, name, market, currency = random.choice(stock_pool)
    employee_ref = random_employee(non_terminated=True)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    direction = random.choice(TRADE_DIRECTIONS)
    quantity = random.choice([100, 200, 500, 1000, 1500])
    price = money(random.uniform(10, 2000))
    status = random.choices(STOCK_ORDER_STATUSES, weights=[5, 15, 15, 35, 10, 10, 10])[0]

    submitted_at = later_datetime(created_dt, 0, 3) if status != "draft" else None
    filled_quantity = 0
    filled_avg_price = 0.0
    filled_at = None
    cancelled_at = None
    if status == "partial_filled":
        filled_quantity = random.randint(1, quantity - 1)
        filled_avg_price = money(price * random.uniform(0.98, 1.02))
        filled_at = later_datetime(submitted_at, 0, 5)
    elif status == "filled":
        filled_quantity = quantity
        filled_avg_price = money(price * random.uniform(0.98, 1.02))
        filled_at = later_datetime(submitted_at, 0, 5)
    elif status == "cancelled":
        cancelled_at = later_datetime(submitted_at, 0, 3)

    total_amount = money((filled_quantity if filled_quantity else quantity) * price)
    commission = money(total_amount * random.uniform(0.0003, 0.002))
    stamp_duty = money(total_amount * (0.001 if direction == "sell" else 0.0))

    stock_trade_order[ref] = {
        "stock_trade_order_ref": ref,
        "order_number": request_number("SO", i),
        "employee_ref": employee_ref,
        "brokerage": random.choice(STOCK_BROKERAGES),
        "stock_code": f"{code}.{market}" if market in ("SSE", "SZSE", "HKEX") else code,
        "stock_name": name,
        "market": market,
        "trade_direction": direction,
        "order_type": random.choice(ORDER_TYPES),
        "currency": currency,
        "quantity": quantity,
        "price": price,
        "filled_quantity": filled_quantity,
        "filled_avg_price": filled_avg_price,
        "total_amount": total_amount,
        "commission": commission,
        "stamp_duty": stamp_duty,
        "order_status": status,
        "submitted_at": iso_datetime(submitted_at) if submitted_at else None,
        "filled_at": iso_datetime(filled_at) if filled_at else None,
        "cancelled_at": iso_datetime(cancelled_at) if cancelled_at else None,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(cancelled_at or filled_at or submitted_at or created_dt),
    }
result["stock_trade_order"] = stock_trade_order
register_table_ids("stocktradeorders", stock_trade_order)

# ============================================================
# 21. financeapprovalflows
# ============================================================
validate_dependencies("financeapprovalflows")
finance_approval_flow = {}
approval_sources = []

def add_source_pairs(source_type, ids):
    for x in ids:
        approval_sources.append((source_type, x))

add_source_pairs("refund", generated_id_registry["refunds"])
add_source_pairs("employee_loan", generated_id_registry["employeeloans"])
add_source_pairs("settlement", generated_id_registry["settlements"])
add_source_pairs("fund_transfer", generated_id_registry["fundtransfers"])
add_source_pairs("budget", generated_id_registry["budgets"])
add_source_pairs("credit_application", generated_id_registry["creditapplications"])
add_source_pairs("tax_filing", generated_id_registry["taxfilings"])

for i in range(1, TABLE_COUNTS["financeapprovalflows"] + 1):
    ref = sequential_ref("FAPR", i, 3)
    source_type, source_ref = approval_sources[(i - 1) % len(approval_sources)]
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    action = random.choices(FINANCE_APPROVAL_ACTIONS, weights=[20, 50, 10, 8, 5, 7])[0]
    acted_at = iso_datetime(later_datetime(created_dt, 0, 7)) if action != "pending" else None

    finance_approval_flow[ref] = {
        "finance_approval_flow_ref": ref,
        "source_type": source_type,
        "source_ref": source_ref,
        "step_order": random.randint(1, 5),
        "approver_ref": random_employee(active_only=True),
        "approver_role": random.choice(FINANCE_APPROVER_ROLES),
        "approval_action": action,
        "comments": zh_sentence(),
        "acted_at": acted_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": acted_at or iso_datetime(later_datetime(created_dt, 0, 5)),
    }
result["finance_approval_flow"] = finance_approval_flow
register_table_ids("financeapprovalflows", finance_approval_flow)

# ============================================================
# 22. budgetlines
# ============================================================
validate_dependencies("budgetlines")
budget_line = {}
budget_id_list = generated_id_registry["budgets"]
for i in range(1, TABLE_COUNTS["budgetlines"] + 1):
    ref = sequential_ref("BLIN", i, 3)
    budget_ref = budget_id_list[(i - 1) % len(budget_id_list)]
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    planned_amount = money(random.uniform(1000, 300000))
    spent_amount = money(planned_amount * random.uniform(0.0, 0.9))
    frozen_amount = money((planned_amount - spent_amount) * random.uniform(0.0, 0.5))
    budget_line[ref] = {
        "budget_line_ref": ref,
        "budget_ref": budget_ref,
        "expense_category": random.choice(EXPENSE_CATEGORIES),
        "line_label": f"{random.choice(['差旅', '办公', '培训', '市场', '技术'])}预算项-{i}",
        "planned_amount": planned_amount,
        "spent_amount": spent_amount,
        "frozen_amount": frozen_amount,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(later_datetime(created_dt, 0, 20)),
    }
result["budget_line"] = budget_line
register_table_ids("budgetlines", budget_line)

# ============================================================
# 23. expensereports
# ============================================================
validate_dependencies("expensereports")
expense_report = {}
expense_report_refs = []
for i in range(1, TABLE_COUNTS["expensereports"] + 1):
    ref = sequential_ref("EXPR", i, 3)
    applicant_ref = employee_ids[(i - 1) % len(employee_ids)]
    department_ref = employee_primary_department.get(applicant_ref, random_department())
    _, default_approver = build_finance_approver_chain(applicant_ref)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(EXPENSE_REPORT_STATUSES, weights=[10, 12, 15, 20, 5, 10, 20, 8])[0]
    total_amount = money(random.uniform(100, 30000))
    approved_amount = 0.0
    submitted_at = None
    approved_at = None
    paid_at = None
    rejected_reason = None

    if status != "draft":
        submitted_at = later_datetime(created_dt, 1, 10)
    if status in ("approved", "processing", "paid"):
        approved_at = later_datetime(submitted_at, 1, 10)
        approved_amount = money(total_amount * random.uniform(0.7, 1.0))
    if status == "paid":
        paid_at = later_datetime(approved_at, 1, 15)
    if status == "rejected":
        rejected_reason = random.choice(["缺少发票", "超出报销标准", "费用归属不明确"])
        approved_amount = 0.0

    budget_ref = choose(generated_id_registry["budgets"]) if maybe(0.6) else None

    expense_report[ref] = {
        "expense_report_ref": ref,
        "report_number": request_number("ER", i),
        "applicant_ref": applicant_ref,
        "department_ref": department_ref,
        "expense_type": random.choice(EXPENSE_TYPES),
        "title": zh_title("报销单："),
        "currency": "CNY",
        "total_amount": total_amount,
        "approved_amount": approved_amount,
        "trip_ref": None,  # cross-domain soft ref
        "budget_ref": budget_ref,
        "report_status": status,
        "current_approver_ref": default_approver if status in ("submitted", "under_review") else None,
        "submitted_at": iso_datetime(submitted_at) if submitted_at else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "paid_at": iso_datetime(paid_at) if paid_at else None,
        "rejected_reason": rejected_reason,
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(paid_at or approved_at or submitted_at or later_datetime(created_dt, 0, 10)),
    }
    expense_report_refs.append(ref)
result["expense_report"] = expense_report
register_table_ids("expensereports", expense_report)

# ============================================================
# 24. paymentrequests
# ============================================================
validate_dependencies("paymentrequests")
payment_request = {}
payment_request_refs = []
for i in range(1, TABLE_COUNTS["paymentrequests"] + 1):
    ref = sequential_ref("PYRQ", i, 3)
    applicant_ref = employee_ids[(i - 1) % len(employee_ids)]
    department_ref = employee_primary_department.get(applicant_ref, random_department())
    source_account_ref = choose(generated_id_registry["financeaccounts"]) if maybe(0.75) else None
    budget_ref = choose(generated_id_registry["budgets"]) if maybe(0.5) else None
    associated_resource_type, associated_resource_ref = random_associated_resource() if maybe(0.5) else (None, None)

    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    planned_payment_date_dt = later_datetime(created_dt, 3, 30)
    status = random.choices(PAYMENT_REQUEST_STATUSES, weights=[10, 12, 15, 20, 5, 10, 20, 8])[0]

    submitted_at = later_datetime(created_dt, 1, 10) if status != "draft" else None
    approved_at = later_datetime(submitted_at, 1, 10) if status in ("approved", "processing", "completed") and submitted_at else None
    rejected_reason = random.choice(["预算不足", "付款依据不完整", "收款信息异常"]) if status == "rejected" else None

    payment_request[ref] = {
        "payment_request_ref": ref,
        "request_number": request_number("PR", i),
        "applicant_ref": applicant_ref,
        "department_ref": department_ref,
        "payment_type": random.choice(PAYMENT_TYPES),
        "payment_method": random.choice(PAYMENT_METHODS),
        "currency": "CNY",
        "amount": money(random.uniform(500, 200000)),
        "payee_name": company_name() if maybe(0.7) else person_name(),
        "payee_account": bank_account_no(),
        "payee_bank": random.choice(["中国银行", "招商银行", "建设银行", "工商银行", "支付宝", "微信支付"]),
        "source_account_ref": source_account_ref,
        "associated_resource_type": associated_resource_type,
        "associated_resource_ref": associated_resource_ref,
        "budget_ref": budget_ref,
        "purpose": zh_sentence(),
        "planned_payment_date": iso_date(planned_payment_date_dt),
        "request_status": status,
        "current_approver_ref": (employees[applicant_ref].get("direct_manager_ref") or random_employee(active_only=True)) if status in ("submitted", "under_review") else None,
        "submitted_at": iso_datetime(submitted_at) if submitted_at else None,
        "approved_at": iso_datetime(approved_at) if approved_at else None,
        "rejected_reason": rejected_reason,
        "urgency": random.choices(PAYMENT_URGENCIES, weights=[70, 20, 10])[0],
        "notes": zh_sentence(),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(approved_at or submitted_at or later_datetime(created_dt, 0, 10)),
    }
    payment_request_refs.append(ref)
result["payment_request"] = payment_request
register_table_ids("paymentrequests", payment_request)

# 回填 payment_execution.payment_request_ref（因为 paymentrequests 在 paymentexecutions 之后生成）
pexe_keys = list(payment_execution.keys())
for idx, pexe_ref in enumerate(pexe_keys):
    payment_execution[pexe_ref]["payment_request_ref"] = payment_request_refs[idx % len(payment_request_refs)]

# ============================================================
# 25. expenselines
# ============================================================
validate_dependencies("expenselines")
expense_line = {}
for i in range(1, TABLE_COUNTS["expenselines"] + 1):
    ref = sequential_ref("ELIN", i, 3)
    expense_report_ref = expense_report_refs[(i - 1) % len(expense_report_refs)]
    report = expense_report[expense_report_ref]
    created_dt = random_datetime(parse_dt(report["created_at"]), NOW)
    amount = money(random.uniform(50, 5000))
    status = random.choices(EXPENSE_LINE_STATUSES, weights=[20, 55, 10, 15])[0]
    approved_amount = amount if status == "approved" else money(amount * random.uniform(0.3, 0.9)) if status == "partial_approved" else 0.0
    rejection_reason = random.choice(["票据不清晰", "超标", "与业务无关"]) if status == "rejected" else None

    expense_line[ref] = {
        "expense_line_ref": ref,
        "expense_report_ref": expense_report_ref,
        "expense_category": random.choice(EXPENSE_CATEGORIES),
        "expense_subcategory": random.choice(["机票", "火车票", "出租车", "酒店", "餐费", "办公耗材", "软件订阅", "培训费"]),
        "description": zh_sentence(),
        "currency": report["currency"],
        "amount": amount,
        "approved_amount": approved_amount,
        "expense_date": iso_date(created_dt - timedelta(days=random.randint(0, 15))),
        "invoice_ref": choose(generated_id_registry["invoices"]) if maybe(0.7) else None,
        "receipt_file_ref": random_file(0.75),
        "line_status": status,
        "rejection_reason": rejection_reason,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(later_datetime(created_dt, 0, 10)),
    }
result["expense_line"] = expense_line
register_table_ids("expenselines", expense_line)

# ============================================================
# 26. settlementlines
# ============================================================
validate_dependencies("settlementlines")
settlement_line = {}
for i in range(1, TABLE_COUNTS["settlementlines"] + 1):
    ref = sequential_ref("SLIN", i, 3)
    settlement_ref = settlement_refs[(i - 1) % len(settlement_refs)]
    created_dt = random_datetime(parse_dt(settlement[settlement_ref]["created_at"]), NOW)
    quantity = random.randint(1, 100)
    unit_price = money(random.uniform(50, 5000))
    amount = money(quantity * unit_price)
    tax_rate_val = random.choice([0.03, 0.06, 0.09, 0.13])
    tax_amount_val = money(amount * tax_rate_val)

    settlement_line[ref] = {
        "settlement_line_ref": ref,
        "settlement_ref": settlement_ref,
        "description": random.choice(["项目服务费", "系统实施费", "技术支持费", "咨询顾问费", "维护费"]) + f"-{i}",
        "quantity": quantity,
        "unit_price": unit_price,
        "amount": amount,
        "tax_rate": tax_rate_val,
        "tax_amount": tax_amount_val,
        "invoice_ref": choose(generated_id_registry["invoices"]) if maybe(0.7) else None,
        "created_at": iso_datetime(created_dt),
    }
result["settlement_line"] = settlement_line
register_table_ids("settlementlines", settlement_line)

# ============================================================
# Final validation
# ============================================================
def validate_ref(record, field_name, value, pool):
    if value is None:
        return
    if value not in pool:
        raise ValueError(f"Invalid FK: field={field_name}, value={value}")

def validate_output():
    # base/generator pools
    pools = {
        "employees": set(employee_ids),
        "departments": set(department_ids),
        "teams": set(team_ids),
        "file_attachment": set(file_ids),
        "financeaccounts": set(generated_id_registry["financeaccounts"]),
        "budgets": set(generated_id_registry["budgets"]),
        "invoices": set(generated_id_registry["invoices"]),
        "paymentexecutions": set(generated_id_registry["paymentexecutions"]),
        "receiptrecords": set(generated_id_registry["receiptrecords"]),
        "employeeloans": set(generated_id_registry["employeeloans"]),
        "settlements": set(generated_id_registry["settlements"]),
        "taxfilings": set(generated_id_registry["taxfilings"]),
        "creditapplications": set(generated_id_registry["creditapplications"]),
        "expensereports": set(generated_id_registry["expensereports"]),
        "paymentrequests": set(generated_id_registry["paymentrequests"]),
    }

    # representative validations
    for _, row in result["finance_account"].items():
        validate_ref(row, "department_ref", row["department_ref"], pools["departments"])
        validate_ref(row, "managed_by_ref", row["managed_by_ref"], pools["employees"])

    for _, row in result["budget"].items():
        if row["scope_type"] == "department" and row["scope_ref"] is not None:
            validate_ref(row, "scope_ref", row["scope_ref"], pools["departments"])
        if row["scope_type"] == "team" and row["scope_ref"] is not None:
            validate_ref(row, "scope_ref", row["scope_ref"], pools["teams"])
        if row["parent_budget_ref"] is not None:
            validate_ref(row, "parent_budget_ref", row["parent_budget_ref"], pools["budgets"])
        if row["approved_by_ref"] is not None:
            validate_ref(row, "approved_by_ref", row["approved_by_ref"], pools["employees"])

    for _, row in result["expense_report"].items():
        validate_ref(row, "applicant_ref", row["applicant_ref"], pools["employees"])
        validate_ref(row, "department_ref", row["department_ref"], pools["departments"])
        if row["budget_ref"] is not None:
            validate_ref(row, "budget_ref", row["budget_ref"], pools["budgets"])

    for _, row in result["expense_line"].items():
        validate_ref(row, "expense_report_ref", row["expense_report_ref"], pools["expensereports"])
        if row["invoice_ref"] is not None:
            validate_ref(row, "invoice_ref", row["invoice_ref"], pools["invoices"])
        if row["receipt_file_ref"] is not None:
            validate_ref(row, "receipt_file_ref", row["receipt_file_ref"], pools["file_attachment"])

validate_output()

# ============================================================
# Print only finance domain tables, no base tables
# ============================================================
print(json.dumps(result, ensure_ascii=False, indent=2))