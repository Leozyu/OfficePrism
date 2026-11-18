import json
import random
from datetime import datetime, timedelta
from faker import Faker

SEED = 42
SCALE = 100

random.seed(SEED)
fake = Faker("zh_CN")
Faker.seed(SEED)

# ============================================================
# Base data JSON (READ ONLY)
# ============================================================
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    BASE_DATA_JSON = f.read()

# ============================================================
# Constants / Enums
# ============================================================
NOW = datetime(2025, 6, 15, 12, 0, 0)
BASE_START = datetime(2020, 1, 1, 0, 0, 0)

TABLE_ORDER = [
    'lawcontracttemplates', 'lawcontractparties', 'lawcontracts', 'lawcontractpartylinks',
    'lawcontractamendments', 'lawcontracttransfers', 'lawcontractmilestones', 'lawcontractrisks',
    'lawcontractloans', 'lawapprovalflows', 'lawapprovalsteps', 'lawseals', 'lawsealusagerequests',
    'lawipassets', 'lawipinventors', 'lawipapplications', 'lawipauthorizations', 'lawiprewards',
    'lawintegritydeclarations', 'lawviolationreports', 'lawlegalcases', 'lawcaseevents',
    'lawevidences', 'lawlegalconsultations', 'lawcompliancereviews', 'lawcorporateentities',
    'lawentitychanges', 'lawqualificationcertificates', 'lawlicenseusagerequests',
    'lawrelatedparties', 'lawrelatedpartytransactions', 'lawinnovationproposals',
    'lawsupplierassessments', 'lawhighrisksoftwares', 'lawbusinessrisks', 'lawpolicies',
    'lawdomainassets'
]

TABLE_KEY_MAP = {
    "lawcontracttemplates": "law_contract_template",
    "lawcontractparties": "law_contract_party",
    "lawcontracts": "law_contract",
    "lawcontractpartylinks": "law_contract_party_link",
    "lawcontractamendments": "law_contract_amendment",
    "lawcontracttransfers": "law_contract_transfer",
    "lawcontractmilestones": "law_contract_milestone",
    "lawcontractrisks": "law_contract_risk",
    "lawcontractloans": "law_contract_loan",
    "lawapprovalflows": "law_approval_flow",
    "lawapprovalsteps": "law_approval_step",
    "lawseals": "law_seal",
    "lawsealusagerequests": "law_seal_usage_request",
    "lawipassets": "law_ip_asset",
    "lawipinventors": "law_ip_inventor",
    "lawipapplications": "law_ip_application",
    "lawipauthorizations": "law_ip_authorization",
    "lawiprewards": "law_ip_reward",
    "lawintegritydeclarations": "law_integrity_declaration",
    "lawviolationreports": "law_violation_report",
    "lawlegalcases": "law_legal_case",
    "lawcaseevents": "law_case_event",
    "lawevidences": "law_evidence",
    "lawlegalconsultations": "law_legal_consultation",
    "lawcompliancereviews": "law_compliance_review",
    "lawcorporateentities": "law_corporate_entity",
    "lawentitychanges": "law_entity_change",
    "lawqualificationcertificates": "law_qualification_certificate",
    "lawlicenseusagerequests": "law_license_usage_request",
    "lawrelatedparties": "law_related_party",
    "lawrelatedpartytransactions": "law_related_party_transaction",
    "lawinnovationproposals": "law_innovation_proposal",
    "lawsupplierassessments": "law_supplier_assessment",
    "lawhighrisksoftwares": "law_high_risk_software",
    "lawbusinessrisks": "law_business_risk",
    "lawpolicies": "law_policy",
    "lawdomainassets": "law_domain_asset",
}

PREFIX_MAP = {
    "lawcontracttemplates": "LCTMPL",
    "lawcontractparties": "LCPRTY",
    "lawcontracts": "LCT",
    "lawcontractpartylinks": "LCPLK",
    "lawcontractamendments": "LCAMD",
    "lawcontracttransfers": "LCTRF",
    "lawcontractmilestones": "LCMS",
    "lawcontractrisks": "LCRSK",
    "lawcontractloans": "LCLN",
    "lawapprovalflows": "LAF",
    "lawapprovalsteps": "LASTP",
    "lawseals": "LSEAL",
    "lawsealusagerequests": "LSUR",
    "lawipassets": "LIPA",
    "lawipinventors": "LIPI",
    "lawipapplications": "LIPAPP",
    "lawipauthorizations": "LIPAUTH",
    "lawiprewards": "LIPRWD",
    "lawintegritydeclarations": "LINTD",
    "lawviolationreports": "LVR",
    "lawlegalcases": "LLC",
    "lawcaseevents": "LCEVT",
    "lawevidences": "LEVD",
    "lawlegalconsultations": "LLCONS",
    "lawcompliancereviews": "LCREV",
    "lawcorporateentities": "LENT",
    "lawentitychanges": "LENTC",
    "lawqualificationcertificates": "LQC",
    "lawlicenseusagerequests": "LLUR",
    "lawrelatedparties": "LRP",
    "lawrelatedpartytransactions": "LRPTX",
    "lawinnovationproposals": "LINNOV",
    "lawsupplierassessments": "LSA",
    "lawhighrisksoftwares": "LHRSW",
    "lawbusinessrisks": "LBR",
    "lawpolicies": "LPOL",
    "lawdomainassets": "LDOM",
}

SOFT_REF_FIELDS = {
    "meeting_room_booking_ref", "repo_ref"
}

CONTRACT_CATEGORIES = ["sales", "procurement", "service", "lease", "employment", "nda", "partnership", "licensing", "construction", "other"]
CONTRACT_TEMPLATE_STATUS = ["active", "inactive", "deprecated"]
CONTRACT_PARTY_TYPE = ["enterprise", "individual", "government", "ngo"]
CONTRACT_PARTY_STATUS = ["active", "inactive", "blacklisted"]
RISK_LEVELS = ["low", "medium", "high", "critical"]
CONTRACT_TYPES = ["standard", "framework", "supplementary", "renewal"]
CONTRACT_STATUS = ["draft", "pending_approval", "approved", "signed", "active", "suspended", "expired", "terminated", "cancelled"]
CURRENCIES = ["CNY", "USD", "EUR", "GBP", "JPY", "HKD"]
PARTY_ROLES = ["party_a", "party_b", "party_c", "guarantor", "witness"]
SIGNING_STATUS = ["pending", "signed", "rejected"]
AMENDMENT_TYPES = ["modification", "supplement", "renewal", "termination"]
AMENDMENT_STATUS = ["draft", "pending_approval", "approved", "rejected", "effective"]
TRANSFER_TYPES = ["owner_change", "department_change", "both"]
TRANSFER_STATUS = ["pending", "approved", "rejected", "completed"]
MILESTONE_TYPES = ["payment", "delivery", "review", "acceptance", "other"]
MILESTONE_STATUS = ["pending", "in_progress", "completed", "overdue", "cancelled"]
CONTRACT_RISK_CATEGORY = ["legal", "financial", "operational", "compliance", "reputational"]
CONTRACT_RISK_STATUS = ["open", "mitigating", "resolved", "accepted", "closed"]
CONTRACT_LOAN_STATUS = ["pending", "approved", "borrowed", "returned", "overdue", "rejected"]
APPROVAL_FLOW_SUBJECT_TYPE = ["contract", "amendment", "seal_usage", "ip_application", "license_usage", "entity_change", "other"]
APPROVAL_FLOW_TYPE = ["contract_approval", "amendment_approval", "seal_approval", "ip_approval", "license_approval", "entity_change_approval", "general"]
APPROVAL_FLOW_STATUS = ["in_progress", "approved", "rejected", "cancelled", "withdrawn"]
APPROVAL_STEP_STATUS = ["pending", "approved", "rejected", "skipped"]
APPROVAL_DECISION = ["approve", "reject", "abstain"]
SEAL_TYPES = ["corporate", "contract", "finance", "legal", "hr", "custom"]
SEAL_STATUS = ["active", "inactive", "destroyed"]
SEAL_USAGE_TYPES = ["contract", "certificate", "letter", "report", "other"]
SEAL_USAGE_STATUS = ["pending", "approved", "rejected", "used", "cancelled"]
IP_TYPES = ["patent", "trademark", "copyright", "trade_secret", "domain", "other"]
IP_STATUS = ["active", "pending", "expired", "abandoned", "transferred"]
IP_OWNER_TYPE = ["company", "employee", "joint"]
IP_INVENTOR_ROLE = ["primary", "co_inventor", "contributor"]
IP_APPLICATION_TYPE = ["new_registration", "renewal", "change", "transfer", "opposition"]
IP_APPLICATION_STATUS = ["drafting", "internal_review", "submitted", "under_examination", "accepted", "granted", "rejected", "withdrawn"]
IP_AUTH_TYPE = ["license", "assignment", "pledge", "cross_license"]
IP_AUTH_STATUS = ["active", "expired", "terminated", "pending"]
IP_REWARD_TYPE = ["application_bonus", "grant_bonus", "commercialization_bonus", "annual_award"]
IP_REWARD_STATUS = ["pending", "approved", "paid", "rejected"]
INTEGRITY_DECL_TYPE = ["commitment", "conflict_of_interest", "gift_disclosure", "annual_review"]
INTEGRITY_DECL_STATUS = ["draft", "submitted", "under_review", "approved", "rejected", "returned"]
INTEGRITY_REVIEW_RESULT = ["pass", "fail", "conditional_pass"]
VIOLATION_TYPE = ["bribery", "conflict_of_interest", "fraud", "embezzlement", "data_breach", "policy_violation", "harassment", "other"]
VIOLATION_STATUS = ["submitted", "under_investigation", "substantiated", "unsubstantiated", "closed", "dismissed"]
VIOLATION_SEVERITY = ["low", "medium", "high", "critical"]
LEGAL_CASE_TYPE = ["litigation", "arbitration", "administrative", "mediation"]
LEGAL_CASE_CATEGORY = ["contract_dispute", "ip_infringement", "labor_dispute", "tort", "regulatory", "other"]
OUR_ROLE = ["plaintiff", "defendant", "applicant", "respondent", "third_party"]
LEGAL_CASE_STATUS = ["filed", "in_progress", "hearing", "awaiting_judgment", "won", "lost", "settled", "withdrawn", "closed"]
CASE_EVENT_TYPE = ["hearing", "filing", "evidence_submission", "mediation", "judgment", "appeal", "settlement", "other"]
EVIDENCE_TYPE = ["document", "electronic", "physical", "testimony", "expert_opinion", "other"]
EVIDENCE_NOTARIZATION = ["none", "pending", "notarized"]
EVIDENCE_STATUS = ["active", "archived", "withdrawn"]
EVIDENCE_RESOURCE_TYPE = ["legal_case", "violation_report", "contract", "other"]
CONSULTATION_TYPE = ["contract_review", "compliance_advice", "ip_consultation", "labor_law", "regulatory", "general"]
CONSULTATION_CHANNEL = ["service_desk", "email", "phone", "meeting", "im"]
CONSULTATION_URGENCY = ["low", "normal", "high", "urgent"]
CONSULTATION_STATUS = ["open", "assigned", "in_progress", "resolved", "closed"]
COMPLIANCE_REVIEW_TYPE = ["business_compliance", "data_privacy", "export_control", "anti_corruption", "environmental", "general"]
COMPLIANCE_REVIEW_STATUS = ["planned", "in_progress", "completed", "cancelled"]
COMPLIANCE_REVIEW_RESULT = ["compliant", "non_compliant", "partially_compliant"]
CORP_ENTITY_TYPE = ["subsidiary", "branch", "joint_venture", "holding", "representative_office"]
CORP_ENTITY_STATUS = ["active", "inactive", "dissolved", "merging", "liquidating"]
ENTITY_CHANGE_TYPE = ["name_change", "address_change", "capital_change", "scope_change", "representative_change", "shareholder_change", "other"]
ENTITY_CHANGE_STATUS = ["pending", "approved", "rejected", "completed", "cancelled"]
CERT_TYPE = ["business_license", "tax_registration", "safety_permit", "quality_certification", "industry_license", "professional_license", "other"]
CERT_HOLDER_TYPE = ["company", "employee"]
CERT_STATUS = ["active", "expired", "revoked", "pending_renewal"]
LICENSE_USAGE_TYPE = ["original", "copy", "scan"]
LICENSE_USAGE_STATUS = ["pending", "approved", "rejected", "borrowed", "returned", "overdue"]
RELATED_PARTY_TYPE = ["enterprise", "individual", "government"]
RELATIONSHIP_TYPE = ["shareholder", "subsidiary", "affiliate", "key_personnel", "family_member", "business_partner", "other"]
RELATED_PARTY_STATUS = ["active", "inactive", "under_review"]
RELATED_PARTY_RISK = ["low", "medium", "high", "critical"]
RELATED_TX_TYPE = ["procurement", "sales", "service", "lease", "loan", "guarantee", "asset_transfer", "other"]
RELATED_TX_STATUS = ["pending_review", "approved", "rejected", "flagged"]
INNOVATION_CATEGORY = ["product", "process", "technology", "management", "service", "other"]
INNOVATION_STATUS = ["submitted", "under_review", "approved", "rejected", "in_progress", "completed", "archived"]
SUPPLIER_ASSESS_TYPE = ["qualification", "annual_review", "incident_review", "exit_review"]
SUPPLIER_ASSESS_STATUS = ["planned", "in_progress", "completed", "cancelled"]
HIGH_RISK_SW_LEVEL = ["medium", "high", "critical"]
HIGH_RISK_SW_CATEGORY = ["security_vulnerability", "license_violation", "data_leakage", "compliance_issue", "supply_chain_risk", "other"]
HIGH_RISK_SW_USAGE = ["restricted", "prohibited", "approved_with_conditions", "under_review"]
HIGH_RISK_SW_COMPLIANCE = ["compliant", "non_compliant", "pending_review", "exempted"]
BUSINESS_RISK_CATEGORY = ["market", "operational", "financial", "legal", "compliance", "strategic", "reputational", "technology"]
BUSINESS_RISK_LEVEL = ["low", "medium", "high", "critical"]
BUSINESS_RISK_PROB = ["low", "medium", "high", "very_high"]
BUSINESS_RISK_IMPACT = ["low", "medium", "high", "critical"]
BUSINESS_RISK_STATUS = ["open", "mitigating", "resolved", "accepted", "closed"]
POLICY_CATEGORY = ["parking", "travel", "expense", "procurement", "data_privacy", "information_security", "hr", "compliance", "safety", "other"]
POLICY_SCOPE = ["company_wide", "department", "team", "region"]
POLICY_STATUS = ["draft", "active", "expired", "superseded", "archived"]
DOMAIN_STATUS = ["active", "expired", "transferring", "suspended", "reserved"]

# ============================================================
# Helpers
# ============================================================
def dt_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def d_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def parse_dt(s: str) -> datetime:
    if len(s) == 10:
        return datetime.strptime(s, "%Y-%m-%d")
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def random_datetime(start: datetime, end: datetime) -> datetime:
    if end <= start:
        return start
    delta = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta))

def random_date(start: datetime, end: datetime) -> datetime:
    return random_datetime(start, end)

def created_updated(earliest=None, latest=None):
    earliest = earliest or BASE_START
    latest = latest or NOW
    c = random_datetime(earliest, latest)
    u = random_datetime(c, latest)
    return dt_str(c), dt_str(u)

def maybe(value, prob=0.7):
    return value if random.random() < prob else None

def sample_one(seq):
    return random.choice(seq) if seq else None

def sample_many(seq, kmin=1, kmax=3):
    if not seq:
        return []
    k = random.randint(kmin, min(kmax, len(seq)))
    return random.sample(seq, k)

def cn_money_amount(min_v=1000, max_v=5000000):
    return round(random.uniform(min_v, max_v), 2)

def safe_phone():
    return "1" + "".join(random.choices("0123456789", k=10))

def safe_email(name=None):
    prefix = (name or fake.pystr(min_chars=6, max_chars=10)).lower()
    return f"{prefix}@{random.choice(['qq.com', '163.com', 'example.com', 'corp.cn'])}"

def zh_sentence(words=12):
    return fake.sentence(nb_words=words).replace("。", "").replace(".", "") + "。"

def zh_paragraph():
    return "".join([zh_sentence(random.randint(8, 15)) for _ in range(random.randint(2, 4))])

def gen_seq_id(table_name, idx):
    return f"{PREFIX_MAP[table_name]}{idx:03d}"

def ensure_dependencies(dep_names, available_pool, current_table):
    missing = [d for d in dep_names if d not in available_pool]
    if missing:
        raise ValueError(f"生成表 {current_table} 前依赖缺失: {missing}")

def weighted_status(pairs):
    vals, weights = zip(*pairs)
    return random.choices(vals, weights=weights, k=1)[0]

# ============================================================
# Parse base data
# ============================================================
base = json.loads(BASE_DATA_JSON)

employee_ids = list(base["employee"].keys())
department_ids = list(base["department"].keys())
team_ids = list(base["team"].keys())
file_ids = list(base["file_attachment"].keys())
role_ids = list(base["role"].keys())
permission_ids = list(base["permission"].keys())
audit_log_ids = list(base["audit_log"].keys())
notification_ids = list(base["notification"].keys())
user_profile_ids = list(base["user_profile"].keys())

active_employee_ids = [
    k for k, v in base["employee"].items()
    if v.get("employment_status") in ("active", "probation", "on_leave")
]

active_department_ids = [
    k for k, v in base["department"].items()
    if v.get("department_status") == "active"
]

root_departments = [k for k, v in base["department"].items() if v.get("department_level") == 1]
leaf_departments = [k for k, v in base["department"].items() if v.get("department_level") >= 2]

employee_to_department = {}
for _, dm in base["department_member"].items():
    if dm.get("is_primary") and dm.get("status") == "active":
        employee_to_department[dm["employee_ref"]] = dm["department_ref"]

employee_to_team = {}
for _, tm in base["team_member"].items():
    if tm.get("status") == "active":
        employee_to_team.setdefault(tm["employee_ref"], []).append(tm["team_ref"])

# ============================================================
# Volumes
# ============================================================
EMP_COUNT = len(employee_ids)
MIN_PER_EMP = 2

def scaled_count(multiplier_per_emp=2, extra=0):
    return max(EMP_COUNT * multiplier_per_emp, int(EMP_COUNT * multiplier_per_emp * SCALE / 100)) + extra

def config_count(minimum=10, factor=0.2):
    return max(minimum, int(EMP_COUNT * factor * SCALE / 100))

# ============================================================
# Result / FK pools
# ============================================================
result = {}
generated_pools = {
    "employees": employee_ids,
    "departments": department_ids,
    "teams": team_ids,
    "file_attachments": file_ids,
    "files": file_ids,
    "contract_files": file_ids,
    "template_files": file_ids,
    "amendment_files": file_ids,
    "document_files": file_ids,
    "stamped_files": file_ids,
    "application_files": file_ids,
    "declaration_files": file_ids,
    "report_files": file_ids,
    "certificate_files": file_ids,
    "policy_files": file_ids,
    "proposal_files": file_ids,
    "notarized_files": file_ids,
    "subjects": [],
    "target_resources": [],
    "related_resources": [],
    "owner_entities": [],
    "holder_entities": [],
    "related_entities": [],
    "parent_entities": [],
    "counterparty_parties": [],
    "licensee_parties": [],
    "supplier_parties": [],
    "contracts": [],
    "contract_parties": [],
    "contract_templates": [],
    "contract_party_links": [],
    "contract_amendments": [],
    "contract_transfers": [],
    "contract_milestones": [],
    "contract_risks": [],
    "contract_loans": [],
    "approval_flows": [],
    "approval_steps": [],
    "seals": [],
    "seal_usage_requests": [],
    "ip_assets": [],
    "ip_inventors": [],
    "ip_applications": [],
    "ip_authorizations": [],
    "ip_rewards": [],
    "integrity_declarations": [],
    "violation_reports": [],
    "legal_cases": [],
    "case_events": [],
    "evidences": [],
    "legal_consultations": [],
    "compliance_reviews": [],
    "corporate_entities": [],
    "entity_changes": [],
    "qualification_certificates": [],
    "license_usage_requests": [],
    "related_parties": [],
    "related_party_transactions": [],
    "innovation_proposals": [],
    "supplier_assessments": [],
    "high_risk_softwares": [],
    "business_risks": [],
    "policies": [],
    "domain_assets": [],
    "created_bies": employee_ids,
    "initiated_bies": employee_ids,
    "from_employees": employee_ids,
    "to_employees": employee_ids,
    "responsible_employees": employee_ids,
    "identified_bies": employee_ids,
    "borrower_employees": employee_ids,
    "approved_bies": employee_ids,
    "approver_employees": employee_ids,
    "custodian_employees": employee_ids,
    "applicant_employees": employee_ids,
    "reviewed_bies": employee_ids,
    "reporter_employees": employee_ids,
    "reported_employees": employee_ids,
    "investigator_employees": employee_ids,
    "recorded_bies": employee_ids,
    "submitted_bies": employee_ids,
    "requester_employees": employee_ids,
    "assigned_tos": employee_ids,
    "reviewer_employees": employee_ids,
    "applied_bies": employee_ids,
    "holder_employees": employee_ids,
    "related_employees": employee_ids,
    "proposer_employees": employee_ids,
    "assessor_employees": employee_ids,
    "assessed_bies": employee_ids,
    "owner_employees": employee_ids,
    "our_entities": [],
    "templates": [],
    "parent_contracts": [],
    "supersedeses": [],
    "scope_departments": department_ids,
    "affected_departments": department_ids,
    "reported_departments": department_ids,
    "from_departments": department_ids,
    "to_departments": department_ids,
}

# ============================================================
# Generators
# ============================================================
def generate_lawcontracttemplates():
    table = "lawcontracttemplates"
    key = TABLE_KEY_MAP[table]
    count = config_count(10, 0.3)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        c_at, u_at = created_updated(datetime(2020, 1, 1), datetime(2025, 3, 1))
        title = random.choice(["销售合同", "采购合同", "服务协议", "保密协议", "租赁协议", "合作协议", "软件许可协议"])
        version_major = random.randint(1, 4)
        version_minor = random.randint(0, 9)
        rows[rid] = {
            "contract_template_ref": rid,
            "template_name": f"{title}模板V{version_major}.{version_minor}",
            "template_code": f"TMPL-{random.choice(['SALE','PROC','SERV','NDA','LEASE','COOP','LIC'])}-{i:03d}",
            "contract_category": random.choice(CONTRACT_CATEGORIES),
            "template_version": f"{version_major}.{version_minor}",
            "template_content": zh_paragraph(),
            "template_file_ref": maybe(sample_one(file_ids), 0.7),
            "template_status": weighted_status([("active", 70), ("inactive", 20), ("deprecated", 10)]),
            "created_by_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "created_at": c_at,
            "updated_at": u_at,
        }
    result[key] = rows
    generated_pools["contract_templates"] = list(rows.keys())
    generated_pools["templates"] = list(rows.keys())

def generate_lawcontractparties():
    table = "lawcontractparties"
    key = TABLE_KEY_MAP[table]
    count = scaled_count(2, 20)
    rows = {}
    company_suffix = ["科技有限公司", "信息技术有限公司", "贸易有限公司", "咨询有限公司", "制造有限公司", "电子商务有限公司"]
    gov_units = ["某市市场监督管理局", "某区税务局", "某省商务厅"]
    ngo_units = ["行业协会", "公益基金会", "研究促进会"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        ptype = weighted_status([("enterprise", 70), ("individual", 15), ("government", 8), ("ngo", 7)])
        if ptype == "enterprise":
            pname = fake.company() + random.choice(company_suffix)
            uscc = "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=18))
            legal_rep = fake.name()
            reg_addr = fake.address()
        elif ptype == "individual":
            pname = fake.name()
            uscc = ""
            legal_rep = pname
            reg_addr = fake.address()
        elif ptype == "government":
            pname = random.choice(gov_units)
            uscc = "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=18))
            legal_rep = fake.name()
            reg_addr = fake.address()
        else:
            pname = fake.company() + random.choice(ngo_units)
            uscc = "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=18))
            legal_rep = fake.name()
            reg_addr = fake.address()

        c_at, u_at = created_updated(datetime(2020, 1, 1), NOW)
        risk = weighted_status([("low", 50), ("medium", 30), ("high", 15), ("critical", 5)])
        status = "active" if risk in ("low", "medium") else weighted_status([("active", 60), ("inactive", 20), ("blacklisted", 20)])
        rows[rid] = {
            "contract_party_ref": rid,
            "party_name": pname,
            "party_type": ptype,
            "unified_social_credit_code": uscc,
            "legal_representative": legal_rep,
            "registered_address": reg_addr,
            "contact_name": fake.name(),
            "contact_phone": safe_phone(),
            "contact_email": safe_email(fake.pystr(min_chars=6, max_chars=8)),
            "bank_name": random.choice(["中国工商银行", "中国建设银行", "中国农业银行", "招商银行", "交通银行"]),
            "bank_account": "".join(random.choices("0123456789", k=19)),
            "party_status": status,
            "risk_level": risk,
            "notes": zh_sentence(10),
            "created_at": c_at,
            "updated_at": u_at,
        }
    result[key] = rows
    generated_pools["contract_parties"] = list(rows.keys())
    generated_pools["counterparty_parties"] = list(rows.keys())
    generated_pools["licensee_parties"] = list(rows.keys())
    generated_pools["supplier_parties"] = list(rows.keys())

def generate_lawcorporateentities():
    table = "lawcorporateentities"
    key = TABLE_KEY_MAP[table]
    count = config_count(10, 0.2)
    rows = {}
    created_ids = []
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        c_at, u_at = created_updated(datetime(2020, 1, 1), NOW)
        establishment = random_date(datetime(2010, 1, 1), datetime(2024, 12, 31))
        parent = None
        if created_ids and random.random() < 0.4:
            parent = sample_one(created_ids)
        rows[rid] = {
            "corporate_entity_ref": rid,
            "entity_name": fake.company() + random.choice(["科技有限公司", "软件有限公司", "数据有限公司", "智能科技有限公司"]),
            "entity_type": weighted_status([("subsidiary", 45), ("branch", 25), ("joint_venture", 10), ("holding", 10), ("representative_office", 10)]),
            "unified_social_credit_code": "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=18)),
            "legal_representative": fake.name(),
            "registered_capital": f"{random.randint(100, 10000)}万元人民币",
            "registered_address": fake.address(),
            "business_scope": zh_sentence(12),
            "establishment_date": d_str(establishment),
            "entity_status": weighted_status([("active", 70), ("inactive", 10), ("dissolved", 5), ("merging", 8), ("liquidating", 7)]),
            "parent_entity_ref": parent,
            "responsible_employee_ref": sample_one(active_employee_ids[:30] or active_employee_ids),
            "notes": zh_sentence(10),
            "created_at": c_at,
            "updated_at": u_at,
        }
        created_ids.append(rid)
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["corporate_entities"] = ids
    generated_pools["owner_entities"] = ids
    generated_pools["holder_entities"] = ids
    generated_pools["related_entities"] = ids
    generated_pools["parent_entities"] = ids
    generated_pools["our_entities"] = ids

def generate_lawcontracts():
    table = "lawcontracts"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contract_templates", "owner_entities", "employees", "departments", "files"], generated_pools, table)
    count = scaled_count(2, 30)
    rows = {}
    created_ids = []
    categories_cn = {
        "sales": "销售", "procurement": "采购", "service": "服务", "lease": "租赁", "employment": "劳动",
        "nda": "保密", "partnership": "合作", "licensing": "许可", "construction": "建设", "other": "综合"
    }
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        category = random.choice(CONTRACT_CATEGORIES)
        cdt = random_datetime(datetime(2021, 1, 1), datetime(2025, 2, 1))
        effective = cdt.date() + timedelta(days=random.randint(1, 45))
        expiry = effective + timedelta(days=random.randint(180, 1460))
        status = weighted_status([
            ("draft", 8), ("pending_approval", 10), ("approved", 8), ("signed", 12),
            ("active", 40), ("suspended", 5), ("expired", 10), ("terminated", 5), ("cancelled", 2)
        ])
        signing_date = None
        termination_date = None

        if status in ("approved", "signed", "active", "suspended", "expired", "terminated"):
            signing_date = d_str(cdt + timedelta(days=random.randint(1, 30)))
        if status == "expired":
            expiry = min(expiry, NOW.date() - timedelta(days=random.randint(1, 180)))
        if status == "terminated":
            termination_date = d_str(parse_dt(dt_str(cdt)) + timedelta(days=random.randint(60, 600)))
        if status in ("draft", "pending_approval", "cancelled"):
            signing_date = None

        updated_at = random_datetime(cdt, NOW)
        parent = None
        ctype = random.choice(CONTRACT_TYPES)
        if created_ids and ctype in ("supplementary", "renewal") and random.random() < 0.6:
            parent = sample_one(created_ids)

        dept = sample_one(leaf_departments or active_department_ids)
        owner = sample_one(active_employee_ids)
        rows[rid] = {
            "contract_ref": rid,
            "contract_number": f"HT-{cdt.year}-{i:05d}",
            "contract_title": f"{categories_cn[category]}{random.choice(['合作协议', '框架协议', '采购合同', '服务合同', '实施合同'])}",
            "contract_category": category,
            "contract_type": ctype,
            "template_ref": maybe(sample_one(generated_pools["contract_templates"]), 0.75),
            "parent_contract_ref": parent,
            "our_entity_ref": maybe(sample_one(generated_pools["owner_entities"]), 0.85),
            "currency": weighted_status([("CNY", 80), ("USD", 10), ("HKD", 5), ("EUR", 3), ("JPY", 2)]),
            "total_amount": cn_money_amount(5000, 10000000),
            "effective_date": d_str(datetime.combine(effective, datetime.min.time())),
            "expiry_date": d_str(datetime.combine(expiry, datetime.min.time())),
            "signing_date": signing_date,
            "termination_date": termination_date,
            "contract_status": status,
            "risk_level": weighted_status([("low", 35), ("medium", 35), ("high", 20), ("critical", 10)]),
            "owner_employee_ref": owner,
            "department_ref": dept,
            "contract_file_ref": maybe(sample_one(file_ids), 0.8),
            "summary": zh_sentence(12),
            "special_terms": zh_paragraph(),
            "created_at": dt_str(cdt),
            "updated_at": dt_str(updated_at),
        }
        created_ids.append(rid)
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["contracts"] = ids
    generated_pools["related_contracts"] = ids
    generated_pools["parent_contracts"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)
    generated_pools["target_resources"].extend(ids)

def generate_lawcontractpartylinks():
    table = "lawcontractpartylinks"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "contract_parties"], generated_pools, table)
    rows = {}
    idx = 1
    for contract_id in generated_pools["contracts"]:
        parties = sample_many(generated_pools["contract_parties"], 2, 3)
        assigned_roles = PARTY_ROLES[:]
        random.shuffle(assigned_roles)
        for p_i, party_id in enumerate(parties):
            rid = gen_seq_id(table, idx)
            idx += 1
            contract_created = parse_dt(result["law_contract"][contract_id]["created_at"])
            sign_status = weighted_status([("pending", 25), ("signed", 65), ("rejected", 10)])
            signed_at = None
            signer_name = fake.name()
            if sign_status == "signed":
                signed_at = dt_str(random_datetime(contract_created, NOW))
            c_at, u_at = created_updated(contract_created, NOW)
            rows[rid] = {
                "contract_party_link_ref": rid,
                "contract_ref": contract_id,
                "contract_party_ref": party_id,
                "party_role": assigned_roles[p_i] if p_i < len(assigned_roles) else random.choice(PARTY_ROLES),
                "signing_status": sign_status,
                "signed_at": signed_at,
                "signer_name": signer_name,
                "created_at": c_at,
                "updated_at": u_at,
            }
    result[key] = rows
    generated_pools["contract_party_links"] = list(rows.keys())

def generate_lawcontractamendments():
    table = "lawcontractamendments"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "employees", "files"], generated_pools, table)
    count = max(config_count(10, 0.3), int(len(generated_pools["contracts"]) * 0.4))
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        contract_id = sample_one(generated_pools["contracts"])
        contract = result["law_contract"][contract_id]
        contract_created = parse_dt(contract["created_at"])
        amend_created = random_datetime(contract_created + timedelta(days=5), NOW)
        status = weighted_status([("draft", 15), ("pending_approval", 20), ("approved", 20), ("rejected", 15), ("effective", 30)])
        effective_date = None
        rejected_reason = None
        new_expiry_date = None
        if random.random() < 0.5:
            old_exp = parse_dt(contract["expiry_date"])
            new_expiry_date = d_str(old_exp + timedelta(days=random.randint(30, 365)))
        if status == "effective":
            effective_date = d_str(amend_created + timedelta(days=random.randint(3, 30)))
        c_at = dt_str(amend_created)
        u_at = dt_str(random_datetime(amend_created, NOW))
        rows[rid] = {
            "contract_amendment_ref": rid,
            "contract_ref": contract_id,
            "amendment_type": random.choice(AMENDMENT_TYPES),
            "amendment_number": f"AMD-{contract['contract_number']}-{i:02d}",
            "amendment_title": f"{contract['contract_title']}补充协议{i}",
            "reason": zh_sentence(10),
            "changes_summary": zh_paragraph(),
            "amount_change": round(random.uniform(-500000, 800000), 2),
            "new_expiry_date": new_expiry_date,
            "amendment_status": status,
            "amendment_file_ref": maybe(sample_one(file_ids), 0.75),
            "initiated_by_ref": sample_one(active_employee_ids),
            "effective_date": effective_date,
            "created_at": c_at,
            "updated_at": u_at,
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["contract_amendments"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)

def generate_lawcontracttransfers():
    table = "lawcontracttransfers"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "employees", "departments"], generated_pools, table)
    count = config_count(10, 0.15)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        contract_id = sample_one(generated_pools["contracts"])
        contract = result["law_contract"][contract_id]
        transfer_type = random.choice(TRANSFER_TYPES)
        from_emp = contract["owner_employee_ref"]
        to_emp = sample_one([e for e in active_employee_ids if e != from_emp]) or from_emp
        from_dept = contract["department_ref"] if transfer_type in ("department_change", "both") else None
        to_dept = sample_one([d for d in active_department_ids if d != from_dept]) if from_dept else None
        cdt = random_datetime(parse_dt(contract["created_at"]), NOW)
        status = weighted_status([("pending", 25), ("approved", 20), ("rejected", 15), ("completed", 40)])
        transferred_at = None
        if status == "completed":
            transferred_at = dt_str(random_datetime(cdt + timedelta(days=1), NOW))
        rows[rid] = {
            "contract_transfer_ref": rid,
            "contract_ref": contract_id,
            "transfer_type": transfer_type,
            "from_employee_ref": from_emp,
            "to_employee_ref": to_emp,
            "from_department_ref": from_dept,
            "to_department_ref": to_dept,
            "reason": zh_sentence(10),
            "transfer_status": status,
            "transferred_at": transferred_at,
            "created_at": dt_str(cdt),
            "updated_at": dt_str(random_datetime(cdt, NOW)),
        }
    result[key] = rows
    generated_pools["contract_transfers"] = list(rows.keys())

def generate_lawcontractmilestones():
    table = "lawcontractmilestones"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "employees"], generated_pools, table)
    rows = {}
    idx = 1
    for contract_id in generated_pools["contracts"]:
        contract = result["law_contract"][contract_id]
        eff = parse_dt(contract["effective_date"])
        total = contract["total_amount"]
        milestone_count = random.randint(2, 4)
        for j in range(milestone_count):
            rid = gen_seq_id(table, idx)
            idx += 1
            due = eff + timedelta(days=30 * (j + 1) + random.randint(0, 25))
            status = weighted_status([("pending", 20), ("in_progress", 15), ("completed", 45), ("overdue", 15), ("cancelled", 5)])
            completed = None
            if status == "completed":
                completed = d_str(due - timedelta(days=random.randint(0, 10)))
            elif status == "overdue":
                if due > NOW:
                    due = NOW - timedelta(days=random.randint(1, 30))
            rows[rid] = {
                "contract_milestone_ref": rid,
                "contract_ref": contract_id,
                "milestone_title": random.choice(["首付款", "中期交付", "验收确认", "尾款支付", "阶段评审"]),
                "milestone_type": random.choice(MILESTONE_TYPES),
                "due_date": d_str(due),
                "completed_date": completed,
                "amount": round(total / milestone_count * random.uniform(0.7, 1.2), 2),
                "milestone_status": status,
                "responsible_employee_ref": sample_one(active_employee_ids),
                "description": zh_sentence(12),
                "created_at": dt_str(random_datetime(parse_dt(contract["created_at"]), NOW)),
                "updated_at": dt_str(random_datetime(parse_dt(contract["created_at"]), NOW)),
            }
    result[key] = rows
    generated_pools["contract_milestones"] = list(rows.keys())

def generate_lawcontractrisks():
    table = "lawcontractrisks"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "employees"], generated_pools, table)
    count = max(config_count(10, 0.25), int(len(generated_pools["contracts"]) * 0.5))
    rows = {}
    clauses = ["付款条款", "违约责任", "保密条款", "交付条款", "知识产权条款", "争议解决条款"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        contract_id = sample_one(generated_pools["contracts"])
        c_created = parse_dt(result["law_contract"][contract_id]["created_at"])
        identified_at = random_datetime(c_created, NOW)
        status = weighted_status([("open", 30), ("mitigating", 25), ("resolved", 20), ("accepted", 15), ("closed", 10)])
        resolved_at = None
        if status in ("resolved", "closed"):
            resolved_at = dt_str(random_datetime(identified_at + timedelta(days=1), NOW))
        rows[rid] = {
            "contract_risk_ref": rid,
            "contract_ref": contract_id,
            "risk_title": random.choice(["付款回收风险", "交付延期风险", "知识产权争议风险", "履约能力风险", "合规审查风险"]),
            "risk_category": random.choice(CONTRACT_RISK_CATEGORY),
            "risk_level": weighted_status([("low", 25), ("medium", 35), ("high", 25), ("critical", 15)]),
            "risk_description": zh_paragraph(),
            "affected_clause": random.choice(clauses),
            "mitigation_plan": zh_paragraph(),
            "risk_status": status,
            "identified_by_ref": sample_one(active_employee_ids),
            "identified_at": dt_str(identified_at),
            "resolved_at": resolved_at,
            "created_at": dt_str(identified_at),
            "updated_at": dt_str(random_datetime(identified_at, NOW)),
        }
    result[key] = rows
    generated_pools["contract_risks"] = list(rows.keys())

def generate_lawcontractloans():
    table = "lawcontractloans"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["contracts", "employees"], generated_pools, table)
    count = config_count(10, 0.2)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        contract_id = sample_one(generated_pools["contracts"])
        contract_created = parse_dt(result["law_contract"][contract_id]["created_at"])
        created = random_datetime(contract_created, NOW)
        status = weighted_status([("pending", 15), ("approved", 15), ("borrowed", 25), ("returned", 30), ("overdue", 10), ("rejected", 5)])
        approved_by = None
        borrowed_at = None
        due_return_at = None
        returned_at = None
        if status in ("approved", "borrowed", "returned", "overdue"):
            approved_by = sample_one(active_employee_ids[:15] or active_employee_ids)
        if status in ("borrowed", "returned", "overdue"):
            borrowed_at_dt = random_datetime(created + timedelta(days=1), NOW)
            borrowed_at = dt_str(borrowed_at_dt)
            due_return_dt = borrowed_at_dt + timedelta(days=random.randint(3, 30))
            due_return_at = dt_str(due_return_dt)
            if status == "returned":
                returned_at = dt_str(random_datetime(borrowed_at_dt, due_return_dt + timedelta(days=5)))
            if status == "overdue" and due_return_dt > NOW:
                due_return_at = dt_str(NOW - timedelta(days=random.randint(1, 20)))
        rows[rid] = {
            "contract_loan_ref": rid,
            "contract_ref": contract_id,
            "borrower_employee_ref": sample_one(active_employee_ids),
            "loan_purpose": random.choice(["审计核查", "项目归档", "法务复印", "商务谈判", "外部送审"]),
            "loan_status": status,
            "approved_by_ref": approved_by,
            "borrowed_at": borrowed_at,
            "due_return_at": due_return_at,
            "returned_at": returned_at,
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    generated_pools["contract_loans"] = list(rows.keys())

def generate_lawapprovalflows():
    table = "lawapprovalflows"
    key = TABLE_KEY_MAP[table]
    subject_pool = (
        generated_pools["contracts"] +
        generated_pools["contract_amendments"] +
        generated_pools["contract_loans"]
    )
    ensure_dependencies(["employees"], generated_pools, table)
    rows = {}
    count = max(config_count(10, 0.3), int(len(subject_pool) * 0.5))
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        subject_type = random.choice(APPROVAL_FLOW_SUBJECT_TYPE)
        if subject_type == "contract" and generated_pools["contracts"]:
            subject_ref = sample_one(generated_pools["contracts"])
            flow_type = "contract_approval"
        elif subject_type == "amendment" and generated_pools["contract_amendments"]:
            subject_ref = sample_one(generated_pools["contract_amendments"])
            flow_type = "amendment_approval"
        elif subject_type == "seal_usage" and generated_pools["seal_usage_requests"]:
            subject_ref = sample_one(generated_pools["seal_usage_requests"])
            flow_type = "seal_approval"
        elif subject_type == "ip_application" and generated_pools["ip_applications"]:
            subject_ref = sample_one(generated_pools["ip_applications"])
            flow_type = "ip_approval"
        elif subject_type == "license_usage" and generated_pools["license_usage_requests"]:
            subject_ref = sample_one(generated_pools["license_usage_requests"])
            flow_type = "license_approval"
        elif subject_type == "entity_change" and generated_pools["entity_changes"]:
            subject_ref = sample_one(generated_pools["entity_changes"])
            flow_type = "entity_change_approval"
        else:
            subject_ref = sample_one(subject_pool) if subject_pool else sample_one(generated_pools["contracts"])
            flow_type = "general"

        initiated = random_datetime(datetime(2021, 1, 1), NOW)
        total_steps = random.randint(2, 4)
        status = weighted_status([("in_progress", 30), ("approved", 40), ("rejected", 20), ("cancelled", 5), ("withdrawn", 5)])
        if status == "in_progress":
            current_step = random.randint(1, total_steps)
            completed_at = None
        else:
            current_step = total_steps
            completed_at = dt_str(random_datetime(initiated + timedelta(days=1), NOW))
        rows[rid] = {
            "approval_flow_ref": rid,
            "subject_type": subject_type,
            "subject_ref": subject_ref,
            "flow_title": f"{random.choice(['合同', '用章', '知识产权', '证照', '事项'])}审批流程",
            "flow_type": flow_type,
            "flow_status": status,
            "initiated_by_ref": sample_one(active_employee_ids),
            "current_step": current_step,
            "total_steps": total_steps,
            "initiated_at": dt_str(initiated),
            "completed_at": completed_at,
            "created_at": dt_str(initiated),
            "updated_at": dt_str(random_datetime(initiated, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["approval_flows"] = ids
    generated_pools["subjects"].extend(ids)

def generate_lawapprovalsteps():
    table = "lawapprovalsteps"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["approval_flows", "employees"], generated_pools, table)
    rows = {}
    idx = 1
    for flow_id, flow in result["law_approval_flow"].items():
        total_steps = flow["total_steps"]
        initiated_at = parse_dt(flow["initiated_at"])
        final_status = flow["flow_status"]
        current_step = flow["current_step"]
        for order in range(1, total_steps + 1):
            rid = gen_seq_id(table, idx)
            idx += 1
            step_status = "pending"
            decision = None
            decided_at = None
            if final_status == "in_progress":
                if order < current_step:
                    step_status = weighted_status([("approved", 80), ("skipped", 20)])
                    decision = "approve" if step_status == "approved" else None
                    decided_at = dt_str(random_datetime(initiated_at, NOW))
                elif order == current_step:
                    step_status = "pending"
                else:
                    step_status = "pending"
            elif final_status == "approved":
                step_status = weighted_status([("approved", 85), ("skipped", 15)])
                decision = "approve" if step_status == "approved" else None
                decided_at = dt_str(random_datetime(initiated_at, NOW))
            elif final_status == "rejected":
                if order < total_steps:
                    step_status = "approved"
                    decision = "approve"
                    decided_at = dt_str(random_datetime(initiated_at, NOW))
                else:
                    step_status = "rejected"
                    decision = "reject"
                    decided_at = dt_str(random_datetime(initiated_at, NOW))
            else:
                if order < current_step:
                    step_status = "approved"
                    decision = "approve"
                    decided_at = dt_str(random_datetime(initiated_at, NOW))
                else:
                    step_status = "skipped"

            rows[rid] = {
                "approval_step_ref": rid,
                "approval_flow_ref": flow_id,
                "step_order": order,
                "step_name": f"第{order}级审批",
                "approver_employee_ref": sample_one(active_employee_ids[:25] or active_employee_ids),
                "step_status": step_status,
                "decision": decision,
                "comments": zh_sentence(10) if step_status in ("approved", "rejected") else "",
                "decided_at": decided_at,
                "created_at": dt_str(initiated_at),
                "updated_at": dt_str(random_datetime(initiated_at, NOW)),
            }
    result[key] = rows
    generated_pools["approval_steps"] = list(rows.keys())

def generate_lawseals():
    table = "lawseals"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees", "departments"], generated_pools, table)
    rows = {}
    count = config_count(10, 0.15)
    used_codes = set()
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        code = f"SEAL-{i:03d}"
        while code in used_codes:
            code = f"SEAL-{random.randint(1,999):03d}"
        used_codes.add(code)
        c_at, u_at = created_updated(datetime(2020, 1, 1), NOW)
        rows[rid] = {
            "seal_ref": rid,
            "seal_name": random.choice(["公司公章", "合同专用章", "财务专用章", "法务专用章", "人事专用章", "项目专用章"]),
            "seal_type": random.choice(SEAL_TYPES),
            "seal_code": code,
            "custodian_employee_ref": sample_one(active_employee_ids[:30] or active_employee_ids),
            "department_ref": sample_one(active_department_ids),
            "seal_status": weighted_status([("active", 75), ("inactive", 20), ("destroyed", 5)]),
            "description": zh_sentence(10),
            "created_at": c_at,
            "updated_at": u_at,
        }
    result[key] = rows
    generated_pools["seals"] = list(rows.keys())

def generate_lawsealusagerequests():
    table = "lawsealusagerequests"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["seals", "employees"], generated_pools, table)
    count = scaled_count(2, 10)
    rows = {}
    related_types = ["contract", "certificate", "letter", "report", "other"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2021, 1, 1), NOW)
        status = weighted_status([("pending", 20), ("approved", 20), ("rejected", 10), ("used", 40), ("cancelled", 10)])
        used_at = None
        if status == "used":
            used_at = dt_str(random_datetime(created + timedelta(days=1), NOW))
        rtype = random.choice(related_types)
        if rtype == "contract" and generated_pools["contracts"]:
            related_ref = sample_one(generated_pools["contracts"])
        elif rtype == "report":
            related_ref = sample_one(audit_log_ids)
        elif rtype == "certificate":
            related_ref = sample_one(file_ids)
        else:
            related_ref = sample_one(notification_ids + team_ids + department_ids)
        rows[rid] = {
            "seal_usage_request_ref": rid,
            "seal_ref": sample_one(generated_pools["seals"]),
            "applicant_employee_ref": sample_one(active_employee_ids),
            "usage_type": random.choice(SEAL_USAGE_TYPES),
            "related_resource_type": rtype,
            "related_resource_ref": related_ref,
            "document_title": random.choice(["合同正文", "情况说明", "授权委托书", "证明文件", "报告文件"]),
            "usage_purpose": zh_sentence(10),
            "copies_count": random.randint(1, 8),
            "request_status": status,
            "used_at": used_at,
            "document_file_ref": maybe(sample_one(file_ids), 0.8),
            "stamped_file_ref": maybe(sample_one(file_ids), 0.6 if status == "used" else 0.2),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["seal_usage_requests"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)

def generate_lawipassets():
    table = "lawipassets"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["owner_entities", "employees", "departments"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        ip_type = random.choice(IP_TYPES)
        app_date = maybe(d_str(random_date(datetime(2020, 1, 1), datetime(2025, 3, 1))), 0.85)
        grant_date = None
        expiry_date = None
        status = weighted_status([("active", 45), ("pending", 20), ("expired", 15), ("abandoned", 10), ("transferred", 10)])
        if status in ("active", "expired", "transferred") and app_date:
            app_dt = parse_dt(app_date)
            grant_dt = app_dt + timedelta(days=random.randint(60, 720))
            grant_date = d_str(grant_dt)
            if ip_type in ("patent", "trademark", "domain"):
                expiry_date = d_str(grant_dt + timedelta(days=random.randint(365 * 5, 365 * 20)))
                if status == "expired":
                    expiry_date = d_str(min(parse_dt(expiry_date), NOW - timedelta(days=30)))
        c_at, u_at = created_updated(datetime(2020, 1, 1), NOW)
        rows[rid] = {
            "ip_asset_ref": rid,
            "ip_type": ip_type,
            "ip_name": random.choice(["智能排班系统", "数据中台架构", "企业协同平台", "供应商风控引擎", "审计分析模型"]) + random.choice(["发明", "商标", "著作权", "专利"]),
            "ip_number": f"IP-{random.randint(2020,2025)}-{i:04d}",
            "registration_number": f"REG{random.randint(10000000,99999999)}",
            "ip_status": status,
            "application_date": app_date,
            "grant_date": grant_date,
            "expiry_date": expiry_date,
            "owner_type": random.choice(IP_OWNER_TYPE),
            "owner_entity_ref": maybe(sample_one(generated_pools["owner_entities"]), 0.8),
            "responsible_employee_ref": sample_one(active_employee_ids),
            "department_ref": sample_one(active_department_ids),
            "ip_class": random.choice(["G06F", "H04L", "35", "42", "9", "41"]),
            "description": zh_paragraph(),
            "certificate_file_ref": maybe(sample_one(file_ids), 0.7),
            "created_at": c_at,
            "updated_at": u_at,
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["ip_assets"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)
    generated_pools["target_resources"].extend(ids)

def generate_lawipinventors():
    table = "lawipinventors"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["ip_assets", "employees"], generated_pools, table)
    rows = {}
    idx = 1
    for ip_id in generated_pools["ip_assets"]:
        inventors = sample_many(active_employee_ids, 1, 3)
        ratios = []
        if len(inventors) == 1:
            ratios = [100.0]
        elif len(inventors) == 2:
            first = random.choice([50.0, 60.0, 70.0])
            ratios = [first, round(100.0 - first, 2)]
        else:
            a = random.choice([40.0, 50.0, 60.0])
            b = random.choice([20.0, 30.0])
            c = round(100.0 - a - b, 2)
            ratios = [a, b, c]
        for j, emp_id in enumerate(inventors):
            rid = gen_seq_id(table, idx)
            idx += 1
            c_at, u_at = created_updated(datetime(2020, 1, 1), NOW)
            rows[rid] = {
                "ip_inventor_ref": rid,
                "ip_asset_ref": ip_id,
                "employee_ref": emp_id,
                "inventor_role": "primary" if j == 0 else random.choice(["co_inventor", "contributor"]),
                "contribution_ratio": ratios[j],
                "created_at": c_at,
                "updated_at": u_at,
            }
    result[key] = rows
    generated_pools["ip_inventors"] = list(rows.keys())

def generate_lawipapplications():
    table = "lawipapplications"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["ip_assets", "employees", "files"], generated_pools, table)
    count = max(config_count(10, 0.25), int(len(generated_pools["ip_assets"]) * 0.6))
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        ip_id = sample_one(generated_pools["ip_assets"])
        created = random_datetime(datetime(2020, 1, 1), NOW)
        status = weighted_status([("drafting", 10), ("internal_review", 15), ("submitted", 20), ("under_examination", 20), ("accepted", 10), ("granted", 15), ("rejected", 7), ("withdrawn", 3)])
        submitted_at = accepted_at = granted_at = rejected_at = None
        rejection_reason = None
        if status in ("submitted", "under_examination", "accepted", "granted", "rejected", "withdrawn"):
            submitted_dt = random_datetime(created + timedelta(days=1), NOW)
            submitted_at = dt_str(submitted_dt)
            if status in ("accepted", "granted", "rejected"):
                accepted_dt = submitted_dt + timedelta(days=random.randint(10, 120))
                accepted_at = dt_str(min(accepted_dt, NOW))
            if status == "granted" and accepted_at:
                granted_at = dt_str(min(parse_dt(accepted_at) + timedelta(days=random.randint(30, 300)), NOW))
            if status == "rejected":
                rejected_at = dt_str(min((parse_dt(accepted_at) if accepted_at else submitted_dt) + timedelta(days=random.randint(5, 60)), NOW))
                rejection_reason = zh_sentence(10)
        rows[rid] = {
            "ip_application_ref": rid,
            "ip_asset_ref": ip_id,
            "application_type": random.choice(IP_APPLICATION_TYPE),
            "applicant_employee_ref": sample_one(active_employee_ids),
            "agency_name": random.choice(["北京某知识产权代理事务所", "上海某专利代理有限公司", "深圳某商标服务机构"]),
            "application_status": status,
            "submitted_at": submitted_at,
            "accepted_at": accepted_at,
            "granted_at": granted_at,
            "rejected_at": rejected_at,
            "rejection_reason": rejection_reason,
            "application_file_ref": maybe(sample_one(file_ids), 0.75),
            "estimated_cost": cn_money_amount(2000, 50000),
            "actual_cost": cn_money_amount(1500, 60000),
            "notes": zh_sentence(10),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["ip_applications"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)

def generate_lawipauthorizations():
    table = "lawipauthorizations"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["ip_assets", "licensee_parties", "contracts"], generated_pools, table)
    count = config_count(10, 0.15)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        start = random_date(datetime(2021, 1, 1), datetime(2025, 1, 1))
        end = start + timedelta(days=random.randint(180, 1800))
        status = weighted_status([("active", 55), ("expired", 20), ("terminated", 15), ("pending", 10)])
        if status == "expired":
            end = min(end, NOW - timedelta(days=random.randint(1, 180)))
        rows[rid] = {
            "ip_authorization_ref": rid,
            "ip_asset_ref": sample_one(generated_pools["ip_assets"]),
            "authorization_type": random.choice(IP_AUTH_TYPE),
            "licensee_name": fake.company() + random.choice(["科技有限公司", "信息有限公司", "贸易有限公司"]),
            "licensee_party_ref": maybe(sample_one(generated_pools["licensee_parties"]), 0.8),
            "scope": zh_sentence(8),
            "territory": random.choice(["中国大陆", "大中华区", "亚太地区", "全球", "华东地区"]),
            "exclusive": random.random() < 0.35,
            "effective_date": d_str(start),
            "expiry_date": d_str(end),
            "fee": cn_money_amount(5000, 3000000),
            "authorization_status": status,
            "contract_ref": maybe(sample_one(generated_pools["contracts"]), 0.7),
            "created_at": dt_str(start),
            "updated_at": dt_str(random_datetime(start, NOW)),
        }
    result[key] = rows
    generated_pools["ip_authorizations"] = list(rows.keys())

def generate_lawiprewards():
    table = "lawiprewards"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["ip_assets", "employees"], generated_pools, table)
    count = config_count(10, 0.2)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2021, 1, 1), NOW)
        status = weighted_status([("pending", 20), ("approved", 25), ("paid", 45), ("rejected", 10)])
        approved_by = sample_one(active_employee_ids[:20] or active_employee_ids) if status in ("approved", "paid") else None
        paid_at = dt_str(random_datetime(created + timedelta(days=3), NOW)) if status == "paid" else None
        rows[rid] = {
            "ip_reward_ref": rid,
            "ip_asset_ref": sample_one(generated_pools["ip_assets"]),
            "employee_ref": sample_one(active_employee_ids),
            "reward_type": random.choice(IP_REWARD_TYPE),
            "reward_amount": cn_money_amount(1000, 100000),
            "reward_status": status,
            "approved_by_ref": approved_by,
            "paid_at": paid_at,
            "notes": zh_sentence(10),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    generated_pools["ip_rewards"] = list(rows.keys())

def generate_lawintegritydeclarations():
    table = "lawintegritydeclarations"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees", "files"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    periods = ["2024", "2025", "2024-Q4", "2025-Q1", "2025-H1"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2023, 1, 1), NOW)
        status = weighted_status([("draft", 10), ("submitted", 20), ("under_review", 15), ("approved", 35), ("rejected", 10), ("returned", 10)])
        submitted_at = reviewed_by = reviewed_at = review_result = None
        if status in ("submitted", "under_review", "approved", "rejected", "returned"):
            submitted_dt = random_datetime(created + timedelta(days=1), NOW)
            submitted_at = dt_str(submitted_dt)
        if status in ("approved", "rejected", "returned"):
            reviewed_by = sample_one(active_employee_ids[:25] or active_employee_ids)
            reviewed_dt = random_datetime(parse_dt(submitted_at), NOW)
            reviewed_at = dt_str(reviewed_dt)
            if status == "approved":
                review_result = random.choice(["pass", "conditional_pass"])
            else:
                review_result = "fail"
        rows[rid] = {
            "integrity_declaration_ref": rid,
            "employee_ref": sample_one(employee_ids),
            "declaration_type": random.choice(INTEGRITY_DECL_TYPE),
            "declaration_period": random.choice(periods),
            "declaration_content": {
                "has_conflict": random.random() < 0.2,
                "received_gifts": random.random() < 0.1,
                "remarks": zh_sentence(8)
            },
            "declaration_status": status,
            "submitted_at": submitted_at,
            "reviewed_by_ref": reviewed_by,
            "reviewed_at": reviewed_at,
            "review_result": review_result,
            "review_comments": zh_sentence(10) if reviewed_at else "",
            "declaration_file_ref": maybe(sample_one(file_ids), 0.7),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["integrity_declarations"] = ids
    generated_pools["related_resources"].extend(ids)

def generate_lawviolationreports():
    table = "lawviolationreports"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees", "departments"], generated_pools, table)
    count = config_count(10, 0.15)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2022, 1, 1), NOW)
        anonymous = random.random() < 0.25
        status = weighted_status([("submitted", 20), ("under_investigation", 25), ("substantiated", 20), ("unsubstantiated", 15), ("closed", 15), ("dismissed", 5)])
        investigator = sample_one(active_employee_ids[:20] or active_employee_ids) if status in ("under_investigation", "substantiated", "unsubstantiated", "closed") else None
        closed_at = None
        if status in ("closed", "dismissed", "substantiated", "unsubstantiated"):
            closed_at = dt_str(random_datetime(created + timedelta(days=5), NOW))
        rows[rid] = {
            "violation_report_ref": rid,
            "reporter_employee_ref": None if anonymous else sample_one(active_employee_ids),
            "is_anonymous": anonymous,
            "violation_type": random.choice(VIOLATION_TYPE),
            "reported_employee_ref": maybe(sample_one(employee_ids), 0.65),
            "reported_department_ref": maybe(sample_one(department_ids), 0.6),
            "title": random.choice(["疑似利益冲突举报", "疑似违规采购举报", "疑似数据泄露举报", "疑似舞弊举报"]),
            "description": zh_paragraph(),
            "occurred_at": dt_str(random_datetime(datetime(2022, 1, 1), created)),
            "evidence_summary": zh_sentence(12),
            "report_status": status,
            "severity": random.choice(VIOLATION_SEVERITY),
            "investigator_employee_ref": investigator,
            "investigation_result": zh_sentence(10) if status in ("substantiated", "unsubstantiated", "closed") else None,
            "investigation_notes": zh_sentence(10),
            "closed_at": closed_at,
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["violation_reports"] = ids
    generated_pools["related_resources"].extend(ids)

def generate_lawlegalcases():
    table = "lawlegalcases"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["counterparty_parties", "employees", "contracts"], generated_pools, table)
    count = config_count(10, 0.12)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        filing_date = maybe(d_str(random_date(datetime(2021, 1, 1), NOW)), 0.85)
        hearing_date = maybe(d_str(random_date(datetime(2024, 1, 1), datetime(2026, 12, 31))), 0.55)
        status = weighted_status([("filed", 15), ("in_progress", 20), ("hearing", 15), ("awaiting_judgment", 10), ("won", 10), ("lost", 10), ("settled", 10), ("withdrawn", 5), ("closed", 5)])
        closed_at = None
        outcome = None
        settlement_amount = None
        if status in ("won", "lost", "settled", "withdrawn", "closed"):
            closed_at = dt_str(random_datetime(datetime(2022, 1, 1), NOW))
            outcome = random.choice(["我方胜诉", "我方败诉", "双方和解", "申请撤回", "案件结案"])
            if status == "settled":
                settlement_amount = cn_money_amount(10000, 2000000)
        created = random_datetime(datetime(2021, 1, 1), NOW)
        rows[rid] = {
            "legal_case_ref": rid,
            "case_number": f"（{random.randint(2021,2025)}）法字第{random.randint(1000,9999)}号",
            "case_title": random.choice(["合同纠纷案件", "知识产权侵权案件", "劳动争议案件", "监管处罚复议案件"]),
            "case_type": random.choice(LEGAL_CASE_TYPE),
            "case_category": random.choice(LEGAL_CASE_CATEGORY),
            "our_role": random.choice(OUR_ROLE),
            "counterparty_name": fake.company() + random.choice(["科技有限公司", "贸易有限公司", "信息有限公司"]),
            "counterparty_party_ref": maybe(sample_one(generated_pools["counterparty_parties"]), 0.8),
            "court_or_institution": random.choice(["北京市朝阳区人民法院", "上海国际仲裁中心", "深圳市南山区人民法院", "广州仲裁委员会"]),
            "jurisdiction": random.choice(["北京", "上海", "深圳", "广州", "杭州"]),
            "filing_date": filing_date,
            "hearing_date": hearing_date,
            "claim_amount": cn_money_amount(50000, 5000000),
            "case_status": status,
            "risk_level": random.choice(RISK_LEVELS),
            "responsible_employee_ref": sample_one(active_employee_ids[:25] or active_employee_ids),
            "external_counsel": random.choice(["北京某律师事务所", "上海某律师事务所", "广东某律师事务所"]),
            "related_contract_ref": maybe(sample_one(generated_pools["contracts"]), 0.65),
            "outcome": outcome,
            "outcome_summary": zh_sentence(12),
            "settlement_amount": settlement_amount,
            "closed_at": closed_at,
            "notes": zh_sentence(10),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["legal_cases"] = ids
    generated_pools["related_resources"].extend(ids)
    generated_pools["target_resources"].extend(ids)

def generate_lawcaseevents():
    table = "lawcaseevents"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["legal_cases", "employees", "files"], generated_pools, table)
    rows = {}
    idx = 1
    for case_id in generated_pools["legal_cases"]:
        event_count = random.randint(2, 4)
        case_created = parse_dt(result["law_legal_case"][case_id]["created_at"])
        for _ in range(event_count):
            rid = gen_seq_id(table, idx)
            idx += 1
            event_date = random_datetime(case_created, NOW)
            rows[rid] = {
                "case_event_ref": rid,
                "legal_case_ref": case_id,
                "event_type": random.choice(CASE_EVENT_TYPE),
                "event_title": random.choice(["立案", "开庭", "提交证据", "调解会议", "法院判决", "上诉申请"]),
                "event_date": dt_str(event_date),
                "description": zh_paragraph(),
                "outcome": zh_sentence(8),
                "document_file_ref": maybe(sample_one(file_ids), 0.7),
                "recorded_by_ref": sample_one(active_employee_ids),
                "created_at": dt_str(event_date),
                "updated_at": dt_str(random_datetime(event_date, NOW)),
            }
    result[key] = rows
    generated_pools["case_events"] = list(rows.keys())
    generated_pools["related_resources"].extend(list(rows.keys()))

def generate_lawevidences():
    table = "lawevidences"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["related_resources", "file_attachments", "employees"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    related_resource_pool = (
        generated_pools["legal_cases"] +
        generated_pools["violation_reports"] +
        generated_pools["contracts"]
    )
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        rtype = random.choice(EVIDENCE_RESOURCE_TYPE)
        if rtype == "legal_case" and generated_pools["legal_cases"]:
            rref = sample_one(generated_pools["legal_cases"])
        elif rtype == "violation_report" and generated_pools["violation_reports"]:
            rref = sample_one(generated_pools["violation_reports"])
        elif rtype == "contract" and generated_pools["contracts"]:
            rref = sample_one(generated_pools["contracts"])
        else:
            rref = sample_one(related_resource_pool)
        notarization = weighted_status([("none", 55), ("pending", 15), ("notarized", 30)])
        notarization_number = notarization_date = notarization_inst = notarized_file_ref = None
        if notarization == "notarized":
            notarization_number = f"GZ-{random.randint(2023,2025)}-{random.randint(10000,99999)}"
            nd = random_date(datetime(2023, 1, 1), NOW)
            notarization_date = d_str(nd)
            notarization_inst = random.choice(["北京市公证处", "上海市公证处", "深圳市公证处"])
            notarized_file_ref = maybe(sample_one(file_ids), 0.85)
        created = random_datetime(datetime(2022, 1, 1), NOW)
        rows[rid] = {
            "evidence_ref": rid,
            "related_resource_type": rtype,
            "related_resource_ref": rref,
            "evidence_title": random.choice(["合同扫描件", "邮件往来记录", "付款凭证", "会议纪要", "聊天记录截图", "专家意见书"]),
            "evidence_type": random.choice(EVIDENCE_TYPE),
            "evidence_description": zh_paragraph(),
            "file_attachment_ref": sample_one(file_ids),
            "notarization_status": notarization,
            "notarization_number": notarization_number,
            "notarization_date": notarization_date,
            "notarization_institution": notarization_inst,
            "notarized_file_ref": notarized_file_ref,
            "submitted_by_ref": sample_one(active_employee_ids),
            "evidence_status": weighted_status([("active", 75), ("archived", 20), ("withdrawn", 5)]),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    generated_pools["evidences"] = list(rows.keys())
    generated_pools["related_resources"].extend(list(rows.keys()))

def generate_lawlegalconsultations():
    table = "lawlegalconsultations"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    related_pool = generated_pools["contracts"] + generated_pools["legal_cases"] + generated_pools["violation_reports"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2022, 1, 1), NOW)
        status = weighted_status([("open", 15), ("assigned", 20), ("in_progress", 25), ("resolved", 25), ("closed", 15)])
        assigned = sample_one(active_employee_ids[:20] or active_employee_ids) if status in ("assigned", "in_progress", "resolved", "closed") else None
        resolved_at = dt_str(random_datetime(created + timedelta(days=1), NOW)) if status in ("resolved", "closed") else None
        rating = random.randint(3, 5) if status == "closed" and random.random() < 0.7 else None
        related_resource_type = None
        related_resource_ref = None
        if related_pool and random.random() < 0.6:
            if generated_pools["contracts"] and random.random() < 0.5:
                related_resource_type = "contract"
                related_resource_ref = sample_one(generated_pools["contracts"])
            elif generated_pools["legal_cases"] and random.random() < 0.5:
                related_resource_type = "legal_case"
                related_resource_ref = sample_one(generated_pools["legal_cases"])
            else:
                related_resource_type = "violation_report"
                related_resource_ref = sample_one(generated_pools["violation_reports"]) if generated_pools["violation_reports"] else None
        rows[rid] = {
            "legal_consultation_ref": rid,
            "requester_employee_ref": sample_one(active_employee_ids),
            "consultation_type": random.choice(CONSULTATION_TYPE),
            "channel": random.choice(CONSULTATION_CHANNEL),
            "title": random.choice(["合同条款咨询", "合规事项咨询", "知识产权咨询", "劳动法咨询", "数据隐私咨询"]),
            "description": zh_paragraph(),
            "urgency": random.choice(CONSULTATION_URGENCY),
            "assigned_to_ref": assigned,
            "consultation_status": status,
            "response_summary": zh_sentence(12) if status in ("resolved", "closed") else "",
            "related_resource_type": related_resource_type,
            "related_resource_ref": related_resource_ref,
            "resolved_at": resolved_at,
            "satisfaction_rating": rating,
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    generated_pools["legal_consultations"] = list(rows.keys())

def generate_lawcompliancereviews():
    table = "lawcompliancereviews"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["departments", "employees"], generated_pools, table)
    count = config_count(10, 0.18)
    rows = {}
    target_pool = generated_pools["contracts"] + generated_pools["ip_assets"] + generated_pools["policies"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        review_date = random_date(datetime(2022, 1, 1), NOW)
        status = weighted_status([("planned", 10), ("in_progress", 20), ("completed", 60), ("cancelled", 10)])
        review_result = None
        if status == "completed":
            review_result = random.choice(COMPLIANCE_REVIEW_RESULT)
        target_resource_type = None
        target_resource_ref = None
        if target_pool and random.random() < 0.65:
            choice = random.choice(["contract", "ip_asset", "policy"])
            if choice == "contract" and generated_pools["contracts"]:
                target_resource_type = "contract"
                target_resource_ref = sample_one(generated_pools["contracts"])
            elif choice == "ip_asset" and generated_pools["ip_assets"]:
                target_resource_type = "ip_asset"
                target_resource_ref = sample_one(generated_pools["ip_assets"])
            elif generated_pools["policies"]:
                target_resource_type = "policy"
                target_resource_ref = sample_one(generated_pools["policies"])
        rows[rid] = {
            "compliance_review_ref": rid,
            "review_title": random.choice(["年度合规检查", "数据隐私专项检查", "反商业贿赂检查", "合同流程合规审查"]),
            "review_type": random.choice(COMPLIANCE_REVIEW_TYPE),
            "review_scope": zh_sentence(10),
            "target_resource_type": target_resource_type,
            "target_resource_ref": target_resource_ref,
            "department_ref": maybe(sample_one(department_ids), 0.75),
            "reviewer_employee_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "review_status": status,
            "risk_level": random.choice(RISK_LEVELS),
            "findings": zh_paragraph(),
            "recommendations": zh_paragraph(),
            "review_result": review_result,
            "review_date": d_str(review_date),
            "next_review_date": maybe(d_str(review_date + timedelta(days=random.randint(90, 365))), 0.8),
            "report_file_ref": maybe(sample_one(file_ids), 0.7),
            "created_at": dt_str(review_date),
            "updated_at": dt_str(random_datetime(review_date, NOW)),
        }
    result[key] = rows
    generated_pools["compliance_reviews"] = list(rows.keys())

def generate_lawentitychanges():
    table = "lawentitychanges"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["corporate_entities", "employees", "files"], generated_pools, table)
    count = config_count(10, 0.18)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2021, 1, 1), NOW)
        status = weighted_status([("pending", 15), ("approved", 20), ("rejected", 10), ("completed", 45), ("cancelled", 10)])
        effective_date = approved_at = None
        if status in ("approved", "completed"):
            approved_dt = random_datetime(created + timedelta(days=1), NOW)
            approved_at = dt_str(approved_dt)
            if status == "completed":
                effective_date = d_str(approved_dt + timedelta(days=random.randint(1, 30)))
        rows[rid] = {
            "entity_change_ref": rid,
            "corporate_entity_ref": sample_one(generated_pools["corporate_entities"]),
            "change_type": random.choice(ENTITY_CHANGE_TYPE),
            "change_description": zh_sentence(12),
            "before_value": zh_sentence(6),
            "after_value": zh_sentence(6),
            "change_status": status,
            "effective_date": effective_date,
            "applied_by_ref": sample_one(active_employee_ids),
            "approved_at": approved_at,
            "document_file_ref": maybe(sample_one(file_ids), 0.75),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["entity_changes"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)

def generate_lawqualificationcertificates():
    table = "lawqualificationcertificates"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["holder_entities", "holder_employees", "files", "employees"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        issue = random_date(datetime(2020, 1, 1), datetime(2025, 1, 1))
        expiry = issue + timedelta(days=random.randint(365, 3650))
        status = weighted_status([("active", 60), ("expired", 15), ("revoked", 5), ("pending_renewal", 20)])
        if status == "expired":
            expiry = min(expiry, NOW - timedelta(days=random.randint(1, 180)))
        holder_type = random.choice(CERT_HOLDER_TYPE)
        holder_entity = sample_one(generated_pools["holder_entities"]) if holder_type == "company" else None
        holder_employee = sample_one(employee_ids) if holder_type == "employee" else None
        rows[rid] = {
            "qualification_certificate_ref": rid,
            "certificate_name": random.choice(["营业执照", "税务登记证", "安全生产许可证", "质量管理体系认证", "行业资质证书", "专业资格证书"]),
            "certificate_type": random.choice(CERT_TYPE),
            "certificate_number": f"CERT-{random.randint(100000,999999)}",
            "issuing_authority": random.choice(["国家市场监督管理总局", "地方住建局", "行业协会", "认证中心"]),
            "holder_type": holder_type,
            "holder_entity_ref": holder_entity,
            "holder_employee_ref": holder_employee,
            "issue_date": d_str(issue),
            "expiry_date": d_str(expiry),
            "renewal_reminder_days": random.choice([30, 60, 90]),
            "certificate_status": status,
            "certificate_file_ref": maybe(sample_one(file_ids), 0.8),
            "custodian_employee_ref": sample_one(active_employee_ids),
            "storage_location": random.choice(["法务档案室A柜", "综合档案室B柜", "行政资料室C柜", "电子档案系统"]),
            "notes": zh_sentence(10),
            "created_at": dt_str(issue),
            "updated_at": dt_str(random_datetime(issue, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["qualification_certificates"] = ids
    generated_pools["related_resources"].extend(ids)

def generate_lawlicenseusagerequests():
    table = "lawlicenseusagerequests"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["qualification_certificates", "employees"], generated_pools, table)
    count = config_count(10, 0.2)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        start = random_date(datetime(2022, 1, 1), NOW)
        end = start + timedelta(days=random.randint(1, 30))
        status = weighted_status([("pending", 15), ("approved", 15), ("rejected", 10), ("borrowed", 25), ("returned", 25), ("overdue", 10)])
        approved_by = borrowed_at = returned_at = None
        if status in ("approved", "borrowed", "returned", "overdue"):
            approved_by = sample_one(active_employee_ids[:20] or active_employee_ids)
        if status in ("borrowed", "returned", "overdue"):
            bdt = random_datetime(start, NOW)
            borrowed_at = dt_str(bdt)
            if status == "returned":
                returned_at = dt_str(random_datetime(bdt, min(NOW, end + timedelta(days=5))))
        rows[rid] = {
            "license_usage_request_ref": rid,
            "qualification_certificate_ref": sample_one(generated_pools["qualification_certificates"]),
            "applicant_employee_ref": sample_one(active_employee_ids),
            "usage_purpose": zh_sentence(10),
            "usage_type": random.choice(LICENSE_USAGE_TYPE),
            "usage_start_date": d_str(start),
            "usage_end_date": d_str(end),
            "request_status": status,
            "approved_by_ref": approved_by,
            "borrowed_at": borrowed_at,
            "returned_at": returned_at,
            "created_at": dt_str(start),
            "updated_at": dt_str(random_datetime(start, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["license_usage_requests"] = ids
    generated_pools["subjects"].extend(ids)
    generated_pools["related_resources"].extend(ids)

def generate_lawrelatedparties():
    table = "lawrelatedparties"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["related_entities", "related_employees", "employees"], generated_pools, table)
    count = config_count(10, 0.18)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        ptype = random.choice(RELATED_PARTY_TYPE)
        created = random_datetime(datetime(2021, 1, 1), NOW)
        rows[rid] = {
            "related_party_ref": rid,
            "party_name": fake.company() + random.choice(["科技有限公司", "贸易有限公司", "咨询有限公司"]) if ptype == "enterprise" else (fake.name() if ptype == "individual" else random.choice(["某区财政局", "某市发改委", "某地国资委"])),
            "party_type": ptype,
            "relationship_type": random.choice(RELATIONSHIP_TYPE),
            "relationship_description": zh_sentence(10),
            "related_entity_ref": maybe(sample_one(generated_pools["related_entities"]), 0.45),
            "related_employee_ref": maybe(sample_one(employee_ids), 0.45),
            "contact_info": f"{safe_phone()} / {safe_email(fake.pystr(min_chars=5, max_chars=7))}",
            "party_status": random.choice(RELATED_PARTY_STATUS),
            "risk_level": random.choice(RELATED_PARTY_RISK),
            "identified_by_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "identified_at": dt_str(created),
            "notes": zh_sentence(10),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["related_parties"] = ids
    generated_pools["related_resources"].extend(ids)

def generate_lawrelatedpartytransactions():
    table = "lawrelatedpartytransactions"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["related_parties", "contracts", "employees"], generated_pools, table)
    count = config_count(10, 0.2)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        tx_date = random_date(datetime(2022, 1, 1), NOW)
        status = random.choice(RELATED_TX_STATUS)
        reviewed_by = reviewed_at = None
        if status in ("approved", "rejected", "flagged"):
            reviewed_by = sample_one(active_employee_ids[:20] or active_employee_ids)
            reviewed_at = dt_str(random_datetime(tx_date, NOW))
        rows[rid] = {
            "related_party_transaction_ref": rid,
            "related_party_ref": sample_one(generated_pools["related_parties"]),
            "transaction_type": random.choice(RELATED_TX_TYPE),
            "transaction_description": zh_sentence(12),
            "transaction_amount": cn_money_amount(10000, 5000000),
            "currency": weighted_status([("CNY", 85), ("USD", 10), ("HKD", 5)]),
            "transaction_date": d_str(tx_date),
            "contract_ref": maybe(sample_one(generated_pools["contracts"]), 0.75),
            "compliance_status": status,
            "reviewed_by_ref": reviewed_by,
            "reviewed_at": reviewed_at,
            "review_comments": zh_sentence(10) if reviewed_at else "",
            "created_at": dt_str(tx_date),
            "updated_at": dt_str(random_datetime(tx_date, NOW)),
        }
    result[key] = rows
    generated_pools["related_party_transactions"] = list(rows.keys())

def generate_lawinnovationproposals():
    table = "lawinnovationproposals"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees", "departments", "ip_assets", "files"], generated_pools, table)
    count = scaled_count(2, 20)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        created = random_datetime(datetime(2022, 1, 1), NOW)
        status = random.choice(INNOVATION_STATUS)
        reviewer = sample_one(active_employee_ids[:20] or active_employee_ids) if status in ("under_review", "approved", "rejected", "in_progress", "completed") else None
        review_score = round(random.uniform(60, 98), 2) if reviewer else None
        rows[rid] = {
            "innovation_proposal_ref": rid,
            "proposer_employee_ref": sample_one(active_employee_ids),
            "department_ref": sample_one(active_department_ids),
            "proposal_title": random.choice(["流程自动化优化建议", "数据治理改进方案", "合同审批效率提升方案", "知识产权管理创新建议", "合规监测平台构想"]),
            "proposal_category": random.choice(INNOVATION_CATEGORY),
            "description": zh_paragraph(),
            "expected_benefit": zh_sentence(12),
            "feasibility_assessment": zh_sentence(12),
            "proposal_status": status,
            "reviewer_employee_ref": reviewer,
            "review_score": review_score,
            "review_comments": zh_sentence(10) if reviewer else "",
            "ip_asset_ref": maybe(sample_one(generated_pools["ip_assets"]), 0.3 if status in ("approved", "completed") else 0.05),
            "proposal_file_ref": maybe(sample_one(file_ids), 0.7),
            "created_at": dt_str(created),
            "updated_at": dt_str(random_datetime(created, NOW)),
        }
    result[key] = rows
    generated_pools["innovation_proposals"] = list(rows.keys())

def generate_lawsupplierassessments():
    table = "lawsupplierassessments"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["supplier_parties", "employees", "files"], generated_pools, table)
    count = config_count(10, 0.18)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        adate = random_date(datetime(2022, 1, 1), NOW)
        fs = round(random.uniform(60, 98), 2)
        cs = round(random.uniform(55, 98), 2)
        qs = round(random.uniform(60, 99), 2)
        os = round((fs + cs + qs) / 3, 2)
        rows[rid] = {
            "supplier_assessment_ref": rid,
            "supplier_name": fake.company() + random.choice(["供应链有限公司", "科技有限公司", "设备有限公司"]),
            "supplier_party_ref": maybe(sample_one(generated_pools["supplier_parties"]), 0.85),
            "assessment_type": random.choice(SUPPLIER_ASSESS_TYPE),
            "assessor_employee_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "assessment_date": d_str(adate),
            "financial_score": fs,
            "compliance_score": cs,
            "quality_score": qs,
            "overall_score": os,
            "risk_level": weighted_status([("low", 35), ("medium", 35), ("high", 20), ("critical", 10)]),
            "risk_findings": zh_sentence(12),
            "recommendations": zh_sentence(12),
            "assessment_status": random.choice(SUPPLIER_ASSESS_STATUS),
            "report_file_ref": maybe(sample_one(file_ids), 0.75),
            "next_assessment_date": maybe(d_str(adate + timedelta(days=random.randint(180, 365))), 0.8),
            "created_at": dt_str(adate),
            "updated_at": dt_str(random_datetime(adate, NOW)),
        }
    result[key] = rows
    generated_pools["supplier_assessments"] = list(rows.keys())

def generate_lawhighrisksoftwares():
    table = "lawhighrisksoftwares"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["employees", "departments"], generated_pools, table)
    count = config_count(10, 0.15)
    rows = {}
    sw_names = ["远程控制工具", "数据抓取工具", "开源组件库", "外部同步客户端", "文件共享软件", "测试代理工具"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        assessed = random_datetime(datetime(2022, 1, 1), NOW)
        rows[rid] = {
            "high_risk_software_ref": rid,
            "software_name": random.choice(sw_names),
            "software_version": f"{random.randint(1,9)}.{random.randint(0,9)}.{random.randint(0,9)}",
            "vendor": fake.company() + random.choice(["软件公司", "科技公司", "系统公司"]),
            "risk_level": random.choice(HIGH_RISK_SW_LEVEL),
            "risk_category": random.choice(HIGH_RISK_SW_CATEGORY),
            "risk_description": zh_paragraph(),
            "affected_departments": sample_many(department_ids, 1, 3),
            "usage_status": random.choice(HIGH_RISK_SW_USAGE),
            "mitigation_measures": zh_sentence(12),
            "alternative_software": random.choice(["企业版替代方案", "国产替代软件", "内部自研系统", "受控白名单软件"]),
            "compliance_status": random.choice(HIGH_RISK_SW_COMPLIANCE),
            "assessed_by_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "assessed_at": dt_str(assessed),
            "review_due_date": maybe(d_str(assessed + timedelta(days=random.randint(60, 365))), 0.85),
            "created_at": dt_str(assessed),
            "updated_at": dt_str(random_datetime(assessed, NOW)),
        }
    result[key] = rows
    generated_pools["high_risk_softwares"] = list(rows.keys())

def generate_lawbusinessrisks():
    table = "lawbusinessrisks"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["departments", "employees"], generated_pools, table)
    count = scaled_count(2, 15)
    rows = {}
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        identified = random_datetime(datetime(2021, 1, 1), NOW)
        status = random.choice(BUSINESS_RISK_STATUS)
        resolved_at = None
        if status in ("resolved", "closed"):
            resolved_at = dt_str(random_datetime(identified + timedelta(days=5), NOW))
        rows[rid] = {
            "business_risk_ref": rid,
            "risk_title": random.choice(["市场需求波动风险", "核心供应中断风险", "合规处罚风险", "系统稳定性风险", "关键人员流失风险"]),
            "risk_category": random.choice(BUSINESS_RISK_CATEGORY),
            "risk_level": random.choice(BUSINESS_RISK_LEVEL),
            "risk_description": zh_paragraph(),
            "risk_source": random.choice(["外部监管变化", "供应链不稳定", "内部流程缺陷", "技术平台老化", "市场竞争加剧"]),
            "affected_department_ref": maybe(sample_one(department_ids), 0.7),
            "probability": random.choice(BUSINESS_RISK_PROB),
            "impact": random.choice(BUSINESS_RISK_IMPACT),
            "mitigation_plan": zh_paragraph(),
            "contingency_plan": zh_sentence(12),
            "risk_status": status,
            "owner_employee_ref": sample_one(active_employee_ids),
            "identified_at": dt_str(identified),
            "review_due_date": maybe(d_str(identified + timedelta(days=random.randint(30, 180))), 0.85),
            "resolved_at": resolved_at,
            "created_at": dt_str(identified),
            "updated_at": dt_str(random_datetime(identified, NOW)),
        }
    result[key] = rows
    generated_pools["business_risks"] = list(rows.keys())

def generate_lawpolicies():
    table = "lawpolicies"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["departments", "employees", "files"], generated_pools, table)
    count = config_count(10, 0.2)
    rows = {}
    created_ids = []
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        effective = random_date(datetime(2021, 1, 1), datetime(2025, 3, 1))
        scope = random.choice(POLICY_SCOPE)
        scope_dept = sample_one(department_ids) if scope == "department" else None
        status = random.choice(POLICY_STATUS)
        expiry = None
        if random.random() < 0.45:
            expiry = d_str(effective + timedelta(days=random.randint(180, 1460)))
        supersedes = sample_one(created_ids) if created_ids and status == "superseded" and random.random() < 0.7 else None
        approved_by = maybe(sample_one(active_employee_ids[:20] or active_employee_ids), 0.75)
        rows[rid] = {
            "policy_ref": rid,
            "policy_title": random.choice(["差旅管理制度", "费用报销制度", "采购合规管理办法", "数据隐私保护制度", "信息安全管理规范", "反舞弊管理规定"]),
            "policy_code": f"POL-{random.randint(2021,2025)}-{i:03d}",
            "policy_category": random.choice(POLICY_CATEGORY),
            "policy_scope": scope,
            "scope_department_ref": scope_dept,
            "content": zh_paragraph(),
            "version": f"{random.randint(1,4)}.{random.randint(0,9)}",
            "effective_date": d_str(effective),
            "expiry_date": expiry,
            "policy_status": status,
            "issued_by_ref": sample_one(active_employee_ids[:20] or active_employee_ids),
            "approved_by_ref": approved_by,
            "policy_file_ref": maybe(sample_one(file_ids), 0.8),
            "supersedes_ref": supersedes,
            "created_at": dt_str(effective),
            "updated_at": dt_str(random_datetime(effective, NOW)),
        }
        created_ids.append(rid)
    result[key] = rows
    ids = list(rows.keys())
    generated_pools["policies"] = ids
    generated_pools["supersedeses"] = ids
    generated_pools["related_resources"].extend(ids)
    generated_pools["target_resources"].extend(ids)

def generate_lawdomainassets():
    table = "lawdomainassets"
    key = TABLE_KEY_MAP[table]
    ensure_dependencies(["owner_entities", "employees"], generated_pools, table)
    count = config_count(10, 0.15)
    rows = {}
    domains = ["example", "zhilian", "oa", "corp", "datahub", "lawdesk", "riskcenter", "workbench"]
    for i in range(1, count + 1):
        rid = gen_seq_id(table, i)
        reg = random_date(datetime(2020, 1, 1), datetime(2025, 1, 1))
        exp = reg + timedelta(days=random.randint(365, 3650))
        ssl_exp = maybe(d_str(reg + timedelta(days=random.randint(180, 900))), 0.75)
        rows[rid] = {
            "domain_asset_ref": rid,
            "domain_name": f"{random.choice(domains)}{i}.com",
            "registrar": random.choice(["阿里云", "腾讯云", "新网", "GoDaddy", "Namecheap"]),
            "registration_date": d_str(reg),
            "expiry_date": d_str(exp),
            "auto_renew": random.random() < 0.7,
            "dns_provider": random.choice(["阿里云解析", "腾讯云DNS", "Cloudflare", "DNSPod"]),
            "ssl_certificate_expiry": ssl_exp,
            "owner_entity_ref": maybe(sample_one(generated_pools["owner_entities"]), 0.8),
            "responsible_employee_ref": sample_one(active_employee_ids),
            "domain_status": random.choice(DOMAIN_STATUS),
            "usage_purpose": random.choice(["官网展示", "内部系统访问", "数据接口服务", "活动宣传", "测试环境"]),
            "notes": zh_sentence(10),
            "created_at": dt_str(reg),
            "updated_at": dt_str(random_datetime(reg, NOW)),
        }
    result[key] = rows
    generated_pools["domain_assets"] = list(rows.keys())

# ============================================================
# Table dispatcher
# ============================================================
DISPATCHER = {
    "lawcontracttemplates": generate_lawcontracttemplates,
    "lawcontractparties": generate_lawcontractparties,
    "lawcontracts": generate_lawcontracts,
    "lawcontractpartylinks": generate_lawcontractpartylinks,
    "lawcontractamendments": generate_lawcontractamendments,
    "lawcontracttransfers": generate_lawcontracttransfers,
    "lawcontractmilestones": generate_lawcontractmilestones,
    "lawcontractrisks": generate_lawcontractrisks,
    "lawcontractloans": generate_lawcontractloans,
    "lawapprovalflows": generate_lawapprovalflows,
    "lawapprovalsteps": generate_lawapprovalsteps,
    "lawseals": generate_lawseals,
    "lawsealusagerequests": generate_lawsealusagerequests,
    "lawipassets": generate_lawipassets,
    "lawipinventors": generate_lawipinventors,
    "lawipapplications": generate_lawipapplications,
    "lawipauthorizations": generate_lawipauthorizations,
    "lawiprewards": generate_lawiprewards,
    "lawintegritydeclarations": generate_lawintegritydeclarations,
    "lawviolationreports": generate_lawviolationreports,
    "lawlegalcases": generate_lawlegalcases,
    "lawcaseevents": generate_lawcaseevents,
    "lawevidences": generate_lawevidences,
    "lawlegalconsultations": generate_lawlegalconsultations,
    "lawcompliancereviews": generate_lawcompliancereviews,
    "lawcorporateentities": generate_lawcorporateentities,
    "lawentitychanges": generate_lawentitychanges,
    "lawqualificationcertificates": generate_lawqualificationcertificates,
    "lawlicenseusagerequests": generate_lawlicenseusagerequests,
    "lawrelatedparties": generate_lawrelatedparties,
    "lawrelatedpartytransactions": generate_lawrelatedpartytransactions,
    "lawinnovationproposals": generate_lawinnovationproposals,
    "lawsupplierassessments": generate_lawsupplierassessments,
    "lawhighrisksoftwares": generate_lawhighrisksoftwares,
    "lawbusinessrisks": generate_lawbusinessrisks,
    "lawpolicies": generate_lawpolicies,
    "lawdomainassets": generate_lawdomainassets,
}

# ============================================================
# Main generation in strict order
# ============================================================
for table in TABLE_ORDER:
    if table == "lawcorporateentities":
        # According to requested order this comes later,
        # but lawcontracts/lawipassets may need entities.
        # To maintain strict order output while ensuring FKs,
        # pre-generate entities lazily before dependent tables if absent.
        pass

    # Lazy pre-generation for entity dependency
    if table in {"lawcontracts", "lawipassets"} and not generated_pools["owner_entities"]:
        generate_lawcorporateentities()

    # Lazy pre-generation for policies dependency in compliance review target pools
    if table == "lawcompliancereviews" and "law_policy" not in result:
        # optional target, no need to prebuild
        pass

    DISPATCHER[table]()

# Remove corporate entities duplicate if generated earlier and again by order
# If the ordered generation already ran after lazy pre-generation,
# preserve existing result and do not overwrite counts.
# Since dispatcher already executed in order, the earlier lazy call populated the same key.
# The ordered call has also run. To prevent that in a production version,
# guard with a generated-set. Kept simple here because dispatcher output is deterministic enough.

# NOTE:
# If lazy + ordered duplicate generation is undesirable, replace above loop with a generated flag set.
# Safer implementation below rebuilds exact ordered output from already-populated result structure.

# Re-run with proper generation guard for cleanliness
result = {}
generated_pools.update({
    "owner_entities": [],
    "holder_entities": [],
    "related_entities": [],
    "parent_entities": [],
    "our_entities": [],
    "contracts": [],
    "related_contracts": [],
    "parent_contracts": [],
    "contract_templates": [],
    "templates": [],
    "contract_parties": [],
    "counterparty_parties": [],
    "licensee_parties": [],
    "supplier_parties": [],
    "contract_party_links": [],
    "contract_amendments": [],
    "contract_transfers": [],
    "contract_milestones": [],
    "contract_risks": [],
    "contract_loans": [],
    "approval_flows": [],
    "approval_steps": [],
    "seals": [],
    "seal_usage_requests": [],
    "ip_assets": [],
    "ip_inventors": [],
    "ip_applications": [],
    "ip_authorizations": [],
    "ip_rewards": [],
    "integrity_declarations": [],
    "violation_reports": [],
    "legal_cases": [],
    "case_events": [],
    "evidences": [],
    "legal_consultations": [],
    "compliance_reviews": [],
    "corporate_entities": [],
    "entity_changes": [],
    "qualification_certificates": [],
    "license_usage_requests": [],
    "related_parties": [],
    "related_party_transactions": [],
    "innovation_proposals": [],
    "supplier_assessments": [],
    "high_risk_softwares": [],
    "business_risks": [],
    "policies": [],
    "domain_assets": [],
    "subjects": [],
    "related_resources": [],
    "target_resources": [],
    "supersedeses": [],
})

generated_once = set()

for table in TABLE_ORDER:
    if table in {"lawcontracts", "lawipassets", "lawqualificationcertificates", "lawrelatedparties", "lawdomainassets"}:
        if "lawcorporateentities" not in generated_once:
            generate_lawcorporateentities()
            generated_once.add("lawcorporateentities")

    if table == "lawcompliancereviews":
        # optional dependency target_resources can be empty
        pass

    if table not in generated_once:
        DISPATCHER[table]()
        generated_once.add(table)

# Ensure no base tables are included
final_output = {k: v for k, v in result.items() if k in TABLE_KEY_MAP.values()}

print(json.dumps(final_output, ensure_ascii=False, indent=2))