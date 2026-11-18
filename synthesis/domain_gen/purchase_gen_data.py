import json
import random
from datetime import datetime, timedelta
from faker import Faker

SEED = 42
SCALE = 100

random.seed(SEED)
fake = Faker("zh_CN")
Faker.seed(SEED)

BASE_DATE = datetime(2020, 1, 1, 0, 0, 0)
NOW = datetime(2025, 6, 15, 12, 0, 0)

# =========================
# Base data: READ ONLY
# =========================
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    base_data_json = f.read()
# =========================
# Helpers
# =========================
def iso_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def parse_dt(v: str) -> datetime:
    return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")

def parse_date(v: str) -> datetime:
    return datetime.strptime(v, "%Y-%m-%d")

def random_datetime(start: datetime, end: datetime) -> datetime:
    if end <= start:
        return start
    delta = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta))

def created_updated(earliest: datetime = None, latest: datetime = None):
    earliest = earliest or BASE_DATE
    latest = latest or NOW
    created = random_datetime(earliest, latest)
    updated = random_datetime(created, latest)
    return iso_datetime(created), iso_datetime(updated)

def maybe(value, probability=0.7):
    return value if random.random() < probability else None

def choice(seq):
    return random.choice(seq)

def sample(seq, k):
    if not seq:
        return []
    k = min(k, len(seq))
    return random.sample(seq, k)

def rand_amount(min_v=1000, max_v=500000, nd=2):
    return round(random.uniform(min_v, max_v), nd)

def cn_company_name():
    suffix = choice(["科技", "信息", "电子", "贸易", "工业", "设备", "材料", "网络", "咨询", "供应链"])
    ending = choice(["有限公司", "股份有限公司", "科技有限公司"])
    return fake.company() + suffix + ending

def cn_bank():
    return choice([
        "中国工商银行", "中国建设银行", "中国农业银行", "中国银行",
        "招商银行", "交通银行", "浦发银行", "中信银行"
    ])

def cn_currency():
    return "CNY"

def social_credit_code():
    chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    return "".join(random.choice(chars) for _ in range(18))

def tax_id():
    return "".join(random.choice("0123456789") for _ in range(15))

def bank_account():
    return "".join(random.choice("0123456789") for _ in range(18))

def phone():
    return "1" + "".join(random.choice("0123456789") for _ in range(10))

def email(name_cn="user"):
    local = "proc" + "".join(random.choice("0123456789abcdefghijklmnopqrstuvwxyz") for _ in range(6))
    return f"{local}@{choice(['qq.com', '163.com', '126.com', 'example.com', 'corp.cn'])}"

def period_label(dt: datetime) -> str:
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"

def weighted_choice(pairs):
    vals = [p[0] for p in pairs]
    ws = [p[1] for p in pairs]
    return random.choices(vals, weights=ws, k=1)[0]

def ensure(condition, message):
    if not condition:
        raise ValueError(message)

# =========================
# Parse base data
# =========================
base = json.loads(base_data_json)

employees = base["employee"]
departments = base["department"]
roles = base["role"]
file_attachments = base["file_attachment"]
team_members = base["team_member"]
department_members = base["department_member"]
employee_roles = base["employee_role"]

employee_ids = list(employees.keys())
active_employee_ids = [k for k, v in employees.items() if v["employment_status"] in ("active", "probation", "on_leave")]
non_terminated_employee_ids = [k for k, v in employees.items() if v["employment_status"] != "terminated"]
department_ids = list(departments.keys())
role_ids = list(roles.keys())
file_ids = list(file_attachments.keys())

employee_department_map = {}
for _, row in department_members.items():
    if row["is_primary"]:
        employee_department_map[row["employee_ref"]] = row["department_ref"]

employee_team_map = {}
for _, row in team_members.items():
    employee_team_map.setdefault(row["employee_ref"], []).append(row["team_ref"])

employee_role_map = {}
for _, row in employee_roles.items():
    if row["status"] == "active":
        employee_role_map.setdefault(row["employee_ref"], []).append(row["role_ref"])

ensure(employee_ids, "Base employee data missing")
ensure(department_ids, "Base department data missing")
ensure(role_ids, "Base role data missing")

# =========================
# ID generator
# =========================
id_counters = {}

def next_id(prefix: str) -> str:
    id_counters[prefix] = id_counters.get(prefix, 0) + 1
    return f"{prefix}{id_counters[prefix]:03d}"

# =========================
# Result + registry
# =========================
result = {}

registry = {
    "employees": employee_ids,
    "departments": department_ids,
    "roles": role_ids,
    "file_attachments": file_ids,
}

# =========================
# Volume planning
# =========================
NUM_EMP = len(employee_ids)
min_per_employee = 2

TABLE_ORDER = [
    "procurementcategories",
    "suppliers",
    "sourcingprojects",
    "purchaserequisitions",
    "requisitionitems",
    "contractitems",
    "purchaseorderitems",
    "purchasechangerequests",
    "goodsreceiptitems",
    "acceptancerecords",
    "acceptanceitems",
    "approvalflowtemplates",
    "approvalflownodes",
    "approvalinstances",
    "approvalactions",
    "procurementpermissionrules",
    "procurementtrainingcourses",
    "procurementtrainingrecords",
    "procurementissuetickets",
    "suppliercontacts",
    "supplierqualifications",
    "suppliercategories",
    "supplierevaluations",
    "sourcingsuppliers",
    "quotations",
    "purchasecontracts",
    "purchaseorders",
    "goodsreceipts",
    "quotationitems",
]

FK_DEPENDENCIES = {
    'procurementcategories': [('procurement_category_ref', 'procurement_categories'), ('parent_category_ref', 'parent_categories')],
    'suppliers': [('supplier_ref', 'suppliers'), ('registered_by_ref', 'registered_bies'), ('approved_by_ref', 'approved_bies')],
    'suppliercontacts': [('supplier_contact_ref', 'supplier_contacts'), ('supplier_ref', 'suppliers')],
    'supplierqualifications': [('supplier_qualification_ref', 'supplier_qualifications'), ('supplier_ref', 'suppliers'), ('file_attachment_ref', 'file_attachments'), ('verified_by_ref', 'verified_bies')],
    'suppliercategories': [('supplier_category_ref', 'supplier_categories'), ('supplier_ref', 'suppliers'), ('procurement_category_ref', 'procurement_categories')],
    'supplierevaluations': [('supplier_evaluation_ref', 'supplier_evaluations'), ('supplier_ref', 'suppliers'), ('evaluator_ref', 'evaluators')],
    'sourcingprojects': [('sourcing_project_ref', 'sourcing_projects'), ('procurement_category_ref', 'procurement_categories'), ('bid_document_file_ref', 'bid_document_files'), ('owner_employee_ref', 'owner_employees'), ('awarded_supplier_ref', 'awarded_suppliers')],
    'sourcingsuppliers': [('sourcing_supplier_ref', 'sourcing_suppliers'), ('sourcing_project_ref', 'sourcing_projects'), ('supplier_ref', 'suppliers')],
    'quotations': [('quotation_ref', 'quotations'), ('sourcing_project_ref', 'sourcing_projects'), ('supplier_ref', 'suppliers'), ('procurement_category_ref', 'procurement_categories'), ('quotation_file_ref', 'quotation_files'), ('submitted_by_ref', 'submitted_bies')],
    'quotationitems': [('quotation_item_ref', 'quotation_items'), ('quotation_ref', 'quotations')],
    'purchaserequisitions': [('purchase_requisition_ref', 'purchase_requisitions'), ('procurement_category_ref', 'procurement_categories'), ('department_ref', 'departments'), ('requestor_ref', 'requestors'), ('suggested_supplier_ref', 'suggested_suppliers')],
    'requisitionitems': [('requisition_item_ref', 'requisition_items'), ('purchase_requisition_ref', 'purchase_requisitions')],
    'purchasecontracts': [('purchase_contract_ref', 'purchase_contracts'), ('supplier_ref', 'suppliers'), ('procurement_category_ref', 'procurement_categories'), ('sourcing_project_ref', 'sourcing_projects'), ('contract_file_ref', 'contract_files'), ('owner_employee_ref', 'owner_employees'), ('signer_employee_ref', 'signer_employees')],
    'contractitems': [('contract_item_ref', 'contract_items'), ('purchase_contract_ref', 'purchase_contracts')],
    'purchaseorders': [('purchase_order_ref', 'purchase_orders'), ('purchase_requisition_ref', 'purchase_requisitions'), ('purchase_contract_ref', 'purchase_contracts'), ('supplier_ref', 'suppliers'), ('procurement_category_ref', 'procurement_categories'), ('department_ref', 'departments'), ('requestor_ref', 'requestors'), ('buyer_ref', 'buyers')],
    'purchaseorderitems': [('purchase_order_item_ref', 'purchase_order_items'), ('purchase_order_ref', 'purchase_orders'), ('contract_item_ref', 'contract_items'), ('requisition_item_ref', 'requisition_items')],
    'purchasechangerequests': [('purchase_change_request_ref', 'purchase_change_requests'), ('change_target_ref', 'change_targets'), ('requestor_ref', 'requestors')],
    'goodsreceipts': [('goods_receipt_ref', 'goods_receipts'), ('purchase_order_ref', 'purchase_orders'), ('supplier_ref', 'suppliers'), ('receiver_ref', 'receivers')],
    'goodsreceiptitems': [('goods_receipt_item_ref', 'goods_receipt_items'), ('goods_receipt_ref', 'goods_receipts'), ('purchase_order_item_ref', 'purchase_order_items')],
    'acceptancerecords': [('acceptance_record_ref', 'acceptance_records'), ('goods_receipt_ref', 'goods_receipts'), ('purchase_order_ref', 'purchase_orders'), ('inspector_ref', 'inspectors'), ('acceptance_report_file_ref', 'acceptance_report_files')],
    'acceptanceitems': [('acceptance_item_ref', 'acceptance_items'), ('acceptance_record_ref', 'acceptance_records'), ('goods_receipt_item_ref', 'goods_receipt_items')],
    'approvalflowtemplates': [('approval_flow_template_ref', 'approval_flow_templates'), ('created_by_ref', 'created_bies')],
    'approvalflownodes': [('approval_flow_node_ref', 'approval_flow_nodes'), ('approval_flow_template_ref', 'approval_flow_templates'), ('approver_ref', 'approvers'), ('fallback_approver_ref', 'fallback_approvers')],
    'approvalinstances': [('approval_instance_ref', 'approval_instances'), ('approval_flow_template_ref', 'approval_flow_templates'), ('target_ref', 'targets'), ('initiator_ref', 'initiators')],
    'approvalactions': [('approval_action_ref', 'approval_actions'), ('approval_instance_ref', 'approval_instances'), ('approver_ref', 'approvers')],
    'procurementpermissionrules': [('procurement_permission_rule_ref', 'procurement_permission_rules'), ('employee_ref', 'employees'), ('role_ref', 'roles'), ('department_ref', 'departments'), ('procurement_category_ref', 'procurement_categories'), ('created_by_ref', 'created_bies')],
    'procurementtrainingcourses': [('procurement_training_course_ref', 'procurement_training_courses'), ('material_file_ref', 'material_files'), ('created_by_ref', 'created_bies')],
    'procurementtrainingrecords': [('procurement_training_record_ref', 'procurement_training_records'), ('procurement_training_course_ref', 'procurement_training_courses'), ('employee_ref', 'employees'), ('certificate_file_ref', 'certificate_files')],
    'procurementissuetickets': [('procurement_issue_ticket_ref', 'procurement_issue_tickets'), ('related_resource_ref', 'related_resources'), ('reporter_ref', 'reporters'), ('assignee_ref', 'assignees')]
}

REGISTRY_NAME_MAP = {
    "procurement_categories": "procurement_category",
    "parent_categories": "procurement_category",
    "suppliers": "supplier",
    "supplier_contacts": "supplier_contact",
    "supplier_qualifications": "supplier_qualification",
    "supplier_categories": "supplier_category",
    "supplier_evaluations": "supplier_evaluation",
    "sourcing_projects": "sourcing_project",
    "sourcing_suppliers": "sourcing_supplier",
    "quotations": "quotation",
    "quotation_items": "quotation_item",
    "purchase_requisitions": "purchase_requisition",
    "requisition_items": "requisition_item",
    "purchase_contracts": "purchase_contract",
    "contract_items": "contract_item",
    "purchase_orders": "purchase_order",
    "purchase_order_items": "purchase_order_item",
    "purchase_change_requests": "purchase_change_request",
    "goods_receipts": "goods_receipt",
    "goods_receipt_items": "goods_receipt_item",
    "acceptance_records": "acceptance_record",
    "acceptance_items": "acceptance_item",
    "approval_flow_templates": "approval_flow_template",
    "approval_flow_nodes": "approval_flow_node",
    "approval_instances": "approval_instance",
    "approval_actions": "approval_action",
    "procurement_permission_rules": "procurement_permission_rule",
    "procurement_training_courses": "procurement_training_course",
    "procurement_training_records": "procurement_training_record",
    "procurement_issue_tickets": "procurement_issue_ticket",
    "employees": "employees",
    "departments": "departments",
    "roles": "roles",
    "file_attachments": "file_attachments",
    "registered_bies": "employees",
    "approved_bies": "employees",
    "verified_bies": "employees",
    "evaluators": "employees",
    "owner_employees": "employees",
    "awarded_suppliers": "supplier",
    "bid_document_files": "file_attachments",
    "quotation_files": "file_attachments",
    "submitted_bies": "employees",
    "requestors": "employees",
    "suggested_suppliers": "supplier",
    "contract_files": "file_attachments",
    "signer_employees": "employees",
    "buyers": "employees",
    "change_targets": "change_targets",
    "receivers": "employees",
    "inspectors": "employees",
    "acceptance_report_files": "file_attachments",
    "created_bies": "employees",
    "approvers": "approver_targets",
    "fallback_approvers": "employees",
    "targets": "approval_targets",
    "initiators": "employees",
    "material_files": "file_attachments",
    "certificate_files": "file_attachments",
    "related_resources": "issue_related_targets",
    "reporters": "employees",
    "assignees": "employees",
}

# 采购域内部注册表名集合：这些表可能存在 placeholder 循环引用，不作严格顺序检查
_PURCHASE_INTERNAL_REGISTRY_NAMES = {
    v for v in REGISTRY_NAME_MAP.values()
    if v not in ("employees", "departments", "roles", "file_attachments",
                 "change_targets", "approval_targets", "issue_related_targets", "approver_targets")
}
_BASE_EXTERNAL_DEPS = {"employees", "departments", "roles", "file_attachments"}

def validate_dependencies(table_key):
    deps = FK_DEPENDENCIES.get(table_key, [])
    if not deps:
        return
    # 第一个FK条目始终是自身引用，跳过所有指向自身的自引用依赖检查
    self_registry_key = REGISTRY_NAME_MAP.get(deps[0][1])
    for _, target in deps:
        mapped = REGISTRY_NAME_MAP.get(target)
        if mapped == self_registry_key:
            continue
        if mapped in ("change_targets", "approval_targets", "issue_related_targets", "approver_targets"):
            continue
        # 采购域内部表可能通过 placeholder 机制处理循环依赖，只强制检查外部基础依赖
        if mapped in _PURCHASE_INTERNAL_REGISTRY_NAMES:
            continue
        ensure(mapped in registry or mapped in _BASE_EXTERNAL_DEPS,
               f"Dependency missing for {table_key}: {target} -> {mapped}")

def register_table(table_name, rows, ref_field):
    result[table_name] = rows
    registry[table_name] = [v[ref_field] for v in rows.values()]

# =========================
# Common controlled vocab
# =========================
units = ["台", "套", "件", "个", "箱", "批", "人天", "项", "米", "吨"]
countries = ["CN", "CN", "CN", "CN", "US", "JP", "DE"]
payment_terms_pool = [
    "验收后30天付款",
    "月结30天",
    "预付30%，到货付70%",
    "验收后60天付款",
    "季度结算"
]
delivery_terms_pool = [
    "送货上门",
    "含安装调试",
    "供应商负责运输",
    "仓库自提",
    "分批交付"
]
warehouse_locations = ["上海一号仓", "深圳南山仓", "北京顺义仓", "杭州滨江仓", "成都高新仓"]
delivery_addresses = [
    "上海市浦东新区张江路100号",
    "北京市海淀区中关村大街88号",
    "深圳市南山区科技园一路66号",
    "杭州市滨江区江南大道18号",
    "成都市高新区天府大道北段999号"
]
contact_titles = ["销售经理", "客户经理", "商务总监", "区域经理", "项目经理", "售前顾问"]
spec_words = ["高性能", "企业级", "标准版", "定制版", "工业级", "商用级"]

# =========================
# 1. procurement_category
# =========================
validate_dependencies("procurementcategories")
procurement_categories = {}

root_categories = [
    ("电子设备", "CAT-EL"),
    ("软件服务", "CAT-SW"),
    ("办公用品", "CAT-OF"),
    ("市场服务", "CAT-MK"),
    ("人力服务", "CAT-HR"),
    ("基础设施", "CAT-IN"),
    ("数据服务", "CAT-DT"),
    ("培训咨询", "CAT-TR"),
    ("安防设备", "CAT-SC"),
    ("后勤物资", "CAT-LG"),
]

child_map = {
    "电子设备": ["服务器", "网络设备", "终端设备", "存储设备"],
    "软件服务": ["SaaS订阅", "开发工具", "安全软件", "数据库软件"],
    "办公用品": ["文具耗材", "办公家具", "打印设备", "行政采购"],
    "市场服务": ["广告投放", "活动策划", "品牌设计", "媒体公关"],
    "人力服务": ["招聘服务", "外包服务", "劳务派遣", "背景调查"],
    "基础设施": ["机房建设", "云资源", "弱电工程", "网络布线"],
    "数据服务": ["数据采集", "数据标注", "数据清洗", "数据分析"],
    "培训咨询": ["内训服务", "合规培训", "管理咨询", "技术认证"],
    "安防设备": ["监控设备", "门禁系统", "消防设备", "应急物资"],
    "后勤物资": ["保洁用品", "餐饮供应", "差旅服务", "劳保用品"],
}

for idx, (name, code) in enumerate(root_categories, 1):
    ref = next_id("PCAT")
    created, updated = created_updated(datetime(2020, 1, 1), datetime(2023, 1, 1))
    procurement_categories[ref] = {
        "procurement_category_ref": ref,
        "category_name": name,
        "category_code": code,
        "parent_category_ref": None,
        "category_level": 1,
        "category_status": weighted_choice([("active", 90), ("inactive", 10)]),
        "description": f"{name}类采购目录，用于归集相似采购需求与供应资源。",
        "display_order": idx,
        "created_at": created,
        "updated_at": updated,
    }

root_name_to_ref = {v["category_name"]: k for k, v in procurement_categories.items()}
for root_name, children in child_map.items():
    parent_ref = root_name_to_ref[root_name]
    for idx, cname in enumerate(children, 1):
        ref = next_id("PCAT")
        parent_created = parse_dt(procurement_categories[parent_ref]["created_at"])
        created, updated = created_updated(parent_created, NOW)
        procurement_categories[ref] = {
            "procurement_category_ref": ref,
            "category_name": cname,
            "category_code": f"{procurement_categories[parent_ref]['category_code']}-{idx:02d}",
            "parent_category_ref": parent_ref,
            "category_level": 2,
            "category_status": weighted_choice([("active", 92), ("inactive", 8)]),
            "description": f"{cname}为{root_name}下的二级采购分类。",
            "display_order": idx,
            "created_at": created,
            "updated_at": updated,
        }

register_table("procurement_category", procurement_categories, "procurement_category_ref")
procurement_category_ids = registry["procurement_category"]
active_procurement_category_ids = [
    k for k, v in procurement_categories.items() if v["category_status"] == "active"
]

# =========================
# 2. supplier
# =========================
validate_dependencies("suppliers")
suppliers = {}
supplier_count = max(30, NUM_EMP * 2)

for i in range(supplier_count):
    ref = next_id("SUP")
    created_dt = random_datetime(datetime(2021, 1, 1), NOW - timedelta(days=30))
    coop_status = weighted_choice([
        ("approved", 65), ("pending", 15), ("suspended", 10), ("blacklisted", 10)
    ])
    risk_level = weighted_choice([
        ("low", 40), ("medium", 35), ("high", 20), ("critical", 5)
    ])
    registered_by = choice(active_employee_ids)
    approved_by = None
    onboarding_date = None
    blacklist_reason = None

    if coop_status in ("approved", "suspended", "blacklisted"):
        approved_by = choice(active_employee_ids)
        onboard_dt = random_datetime(created_dt, NOW - timedelta(days=1))
        onboarding_date = iso_date(onboard_dt)
    if coop_status == "blacklisted":
        blacklist_reason = choice([
            "多次交付延迟且无改善",
            "质量问题严重，复检不合格",
            "存在商业合规风险",
            "售后响应长期不达标"
        ])
        risk_level = choice(["high", "critical"])

    suppliers[ref] = {
        "supplier_ref": ref,
        "supplier_name": cn_company_name(),
        "supplier_code": f"VEND-{created_dt.year}-{i+1:04d}",
        "supplier_type": weighted_choice([("standard", 65), ("strategic", 20), ("occasional", 15)]),
        "unified_social_credit_code": social_credit_code(),
        "legal_representative": fake.name(),
        "registered_address": fake.address().replace("\n", ""),
        "business_address": fake.address().replace("\n", ""),
        "country": choice(countries),
        "bank_name": cn_bank(),
        "bank_account": bank_account(),
        "tax_id": tax_id(),
        "cooperation_status": coop_status,
        "risk_level": risk_level,
        "onboarding_date": onboarding_date,
        "blacklist_reason": blacklist_reason,
        "notes": choice([
            "配合度较高，商务沟通顺畅。",
            "具备全国交付能力。",
            "在重点项目中表现稳定。",
            "需持续关注价格波动。",
            "已纳入年度供应商池。"
        ]),
        "registered_by_ref": registered_by,
        "approved_by_ref": approved_by,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("supplier", suppliers, "supplier_ref")
supplier_ids = registry["supplier"]
approved_supplier_ids = [k for k, v in suppliers.items() if v["cooperation_status"] == "approved"]
active_supplier_ids = [k for k, v in suppliers.items() if v["cooperation_status"] in ("approved", "pending", "suspended")]

# =========================
# 3. sourcing_project
# =========================
validate_dependencies("sourcingprojects")
sourcing_projects = {}
sourcing_project_count = max(20, NUM_EMP // 2)

for i in range(sourcing_project_count):
    ref = next_id("SPRJ")
    created_dt = random_datetime(datetime(2022, 1, 1), NOW - timedelta(days=10))
    owner = choice(active_employee_ids)
    cat = choice(active_procurement_category_ids)
    status = weighted_choice([
        ("draft", 15), ("open", 20), ("evaluation", 15),
        ("awarded", 20), ("cancelled", 10), ("closed", 20)
    ])
    submission_deadline_dt = created_dt + timedelta(days=random.randint(7, 45))
    awarded_supplier_ref = None
    award_date = None
    cancel_reason = None

    if status in ("awarded", "closed"):
        awarded_supplier_ref = choice(approved_supplier_ids) if approved_supplier_ids else None
        award_dt = random_datetime(submission_deadline_dt, NOW)
        award_date = iso_date(award_dt)
    if status == "cancelled":
        cancel_reason = choice([
            "需求取消", "预算冻结", "供应商响应不足", "技术方案发生重大变更"
        ])

    sourcing_projects[ref] = {
        "sourcing_project_ref": ref,
        "project_title": choice([
            "企业云资源年度采购项目", "办公终端集中采购项目", "网络安全软件采购项目",
            "品牌推广服务招采项目", "数据标注服务采购项目", "机房设备更新项目"
        ]) + f"-{i+1}",
        "project_code": f"SRC-{created_dt.year}-{i+1:04d}",
        "sourcing_type": weighted_choice([
            ("competitive_bid", 35), ("negotiation", 20), ("sole_source", 10),
            ("framework_agreement", 25), ("reverse_auction", 10)
        ]),
        "procurement_category_ref": cat,
        "procurement_method": weighted_choice([("centralized", 50), ("decentralized", 25), ("hybrid", 25)]),
        "budget_amount": rand_amount(50000, 3000000),
        "currency": cn_currency(),
        "description": "本项目用于满足业务部门阶段性或年度性采购需求，覆盖商务、交付与质量要求。",
        "requirements": "供应商需具备稳定交付能力、相应资质文件，并满足售后服务与实施支持要求。",
        "bid_document_file_ref": maybe(choice(file_ids), 0.6),
        "submission_deadline": iso_datetime(submission_deadline_dt),
        "evaluation_criteria": {
            "price": choice([30, 35, 40]),
            "quality": choice([25, 30, 35]),
            "delivery": choice([15, 20, 25]),
            "service": choice([10, 15, 20]),
        },
        "owner_employee_ref": owner,
        "project_status": status,
        "awarded_supplier_ref": awarded_supplier_ref,
        "award_date": award_date,
        "cancel_reason": cancel_reason,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("sourcing_project", sourcing_projects, "sourcing_project_ref")
sourcing_project_ids = registry["sourcing_project"]
awarded_sourcing_project_ids = [k for k, v in sourcing_projects.items() if v["project_status"] in ("awarded", "closed")]
open_sourcing_project_ids = [k for k, v in sourcing_projects.items() if v["project_status"] in ("open", "evaluation", "awarded", "closed")]

# =========================
# 4. purchase_requisition
# =========================
validate_dependencies("purchaserequisitions")
purchase_requisitions = {}
purchase_requisition_count = max(NUM_EMP * 2, SCALE)

for i in range(purchase_requisition_count):
    ref = next_id("PRQ")
    requestor = choice(active_employee_ids)
    dept = employee_department_map.get(requestor, choice(department_ids))
    created_dt = random_datetime(datetime(2022, 1, 1), NOW - timedelta(days=5))
    req_status = weighted_choice([
        ("draft", 10), ("submitted", 15), ("under_review", 15),
        ("approved", 35), ("rejected", 10), ("cancelled", 5), ("fulfilled", 10)
    ])
    submitted_at = None
    approved_at = None
    rejected_reason = None

    if req_status in ("submitted", "under_review", "approved", "rejected", "fulfilled", "cancelled"):
        sub_dt = random_datetime(created_dt, NOW)
        submitted_at = iso_datetime(sub_dt)
    if req_status in ("approved", "fulfilled"):
        base_dt = parse_dt(submitted_at) if submitted_at else created_dt
        approved_at = iso_datetime(random_datetime(base_dt, NOW))
    if req_status == "rejected":
        rejected_reason = choice(["预算不足", "需求描述不完整", "采购范围不明确", "缺少必要审批依据"])

    purchase_requisitions[ref] = {
        "purchase_requisition_ref": ref,
        "requisition_code": f"PR-{created_dt.year}-{i+1:05d}",
        "requisition_type": weighted_choice([
            ("standard", 55), ("urgent", 20), ("blanket", 10), ("service", 15)
        ]),
        "procurement_category_ref": choice(active_procurement_category_ids),
        "department_ref": dept,
        "requestor_ref": requestor,
        "procurement_method": weighted_choice([("centralized", 45), ("decentralized", 35), ("hybrid", 20)]),
        "currency": cn_currency(),
        "estimated_amount": rand_amount(2000, 800000),
        "required_date": iso_date(created_dt + timedelta(days=random.randint(7, 120))),
        "business_justification": choice([
            "支持年度项目推进所需采购。",
            "满足新业务上线对系统及设备的需求。",
            "用于替换老旧设备，提升稳定性。",
            "满足部门日常运营与交付要求。"
        ]),
        "special_requirements": choice([
            "要求原厂授权及售后支持。",
            "要求支持分批交付。",
            "需提供现场实施服务。",
            "需满足公司信息安全规范。",
            "无特殊要求。"
        ]),
        "suggested_supplier_ref": maybe(choice(active_supplier_ids), 0.5),
        "requisition_status": req_status,
        "submitted_at": submitted_at,
        "approved_at": approved_at,
        "rejected_reason": rejected_reason,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("purchase_requisition", purchase_requisitions, "purchase_requisition_ref")
purchase_requisition_ids = registry["purchase_requisition"]
approved_requisition_ids = [k for k, v in purchase_requisitions.items() if v["requisition_status"] in ("approved", "fulfilled")]
requisition_approved_supplier_pref = {
    k: v["suggested_supplier_ref"] for k, v in purchase_requisitions.items()
}

# =========================
# 5. requisition_item
# =========================
validate_dependencies("requisitionitems")
requisition_items = {}
req_item_per_req = [1, 2, 3, 4]

for req_id in purchase_requisition_ids:
    req = purchase_requisitions[req_id]
    item_count = choice(req_item_per_req)
    for _ in range(item_count):
        ref = next_id("RQI")
        qty = random.randint(1, 50)
        unit_price = rand_amount(100, 50000)
        requisition_items[ref] = {
            "requisition_item_ref": ref,
            "purchase_requisition_ref": req_id,
            "item_name": choice([
                "服务器设备", "办公笔记本", "交换机", "数据库授权", "安全防火墙",
                "设计服务", "培训服务", "宣传物料", "工位家具", "数据标注服务"
            ]),
            "item_description": "用于支持部门采购需求的标准化采购条目。",
            "specification": choice(spec_words) + choice(["/16核32G", "/千兆", "/企业版", "/三年服务", "/标准套餐"]),
            "unit": choice(units),
            "quantity": qty,
            "estimated_unit_price": unit_price,
            "estimated_line_amount": round(qty * unit_price, 2),
            "required_date": req["required_date"],
            "notes": choice(["优先国产品牌", "支持上门安装", "要求含培训", "需兼容现有系统", ""]),
            "created_at": req["created_at"],
            "updated_at": iso_datetime(random_datetime(parse_dt(req["created_at"]), NOW)),
        }

register_table("requisition_item", requisition_items, "requisition_item_ref")
requisition_item_ids = registry["requisition_item"]
requisition_items_by_req = {}
for k, v in requisition_items.items():
    requisition_items_by_req.setdefault(v["purchase_requisition_ref"], []).append(k)

# =========================
# 6. contract_item
# Must exist before purchase_contract per required order.
# We create placeholder parent refs now and finalize parent contract table later.
# =========================
validate_dependencies("contractitems")
contract_items = {}
placeholder_contract_refs = [f"PCON_PLACEHOLDER_{i:03d}" for i in range(max(20, NUM_EMP // 2))]
placeholder_contract_map = {}

for pcref in placeholder_contract_refs:
    placeholder_contract_map[pcref] = []

for pcref in placeholder_contract_refs:
    item_count = random.randint(1, 4)
    for _ in range(item_count):
        ref = next_id("CTI")
        qty = random.randint(10, 500)
        unit_price = rand_amount(50, 30000)
        row = {
            "contract_item_ref": ref,
            "purchase_contract_ref": pcref,
            "item_name": choice([
                "云服务器资源", "软件授权", "办公终端", "网络设备", "数据服务包",
                "安全运维服务", "招聘服务", "培训课程包"
            ]),
            "item_description": "合同约定采购或服务交付范围内的明细项。",
            "specification": choice(spec_words) + choice(["/年度", "/基础版", "/增强版", "/企业版", "/驻场"]),
            "unit": choice(units),
            "contracted_quantity": qty,
            "unit_price": unit_price,
            "line_amount": round(qty * unit_price, 2),
            "ordered_quantity": random.randint(0, qty // 2),
            "received_quantity": random.randint(0, qty // 3),
            "notes": choice(["按批次释放", "价格锁定一年", "可追加采购", "交付需验收"]),
            "created_at": iso_datetime(random_datetime(datetime(2022, 1, 1), NOW - timedelta(days=30))),
            "updated_at": iso_datetime(random_datetime(datetime(2022, 1, 1), NOW)),
        }
        contract_items[ref] = row
        placeholder_contract_map[pcref].append(ref)

register_table("contract_item", contract_items, "contract_item_ref")
contract_item_ids = registry["contract_item"]

# =========================
# 7. purchase_order_item
# Must exist before purchase_order in required order.
# Create placeholder purchase order refs now and reconcile later.
# =========================
validate_dependencies("purchaseorderitems")
purchase_order_items = {}
placeholder_po_refs = [f"PORD_PLACEHOLDER_{i:03d}" for i in range(max(40, NUM_EMP))]
placeholder_po_item_map = {}

approved_req_ids_for_po = approved_requisition_ids or purchase_requisition_ids
usable_contract_item_ids = contract_item_ids[:]

for poref in placeholder_po_refs:
    placeholder_po_item_map[poref] = []
    item_count = random.randint(1, 4)
    related_req = choice(approved_req_ids_for_po)
    related_req_item_candidates = requisition_items_by_req.get(related_req, requisition_item_ids)
    for _ in range(item_count):
        ref = next_id("POI")
        req_item_ref = maybe(choice(related_req_item_candidates), 0.8)
        contract_item_ref = maybe(choice(usable_contract_item_ids), 0.6)
        qty = random.randint(1, 80)
        unit_price = rand_amount(100, 50000)
        received_qty = random.randint(0, qty)
        accepted_qty = random.randint(0, received_qty)
        if accepted_qty == qty:
            item_status = "accepted"
        elif received_qty == qty and accepted_qty < qty:
            item_status = choice(["received", "rejected"])
        elif received_qty > 0:
            item_status = "partially_received"
        else:
            item_status = "pending"

        row = {
            "purchase_order_item_ref": ref,
            "purchase_order_ref": poref,
            "contract_item_ref": contract_item_ref,
            "requisition_item_ref": req_item_ref,
            "item_name": choice([
                "服务器设备", "办公笔记本", "交换机", "数据库授权", "安全防火墙",
                "市场推广服务", "数据标注服务", "培训服务"
            ]),
            "item_description": "采购订单中的具体明细项。",
            "specification": choice(spec_words) + choice(["/标准", "/增强", "/年度", "/项目制", "/企业级"]),
            "unit": choice(units),
            "quantity": qty,
            "unit_price": unit_price,
            "line_amount": round(qty * unit_price, 2),
            "received_quantity": received_qty,
            "accepted_quantity": accepted_qty,
            "expected_delivery_date": iso_date(random_datetime(datetime(2023, 1, 1), NOW + timedelta(days=90))),
            "item_status": item_status,
            "notes": choice(["按计划交付", "优先验收", "需现场支持", "支持分批收货", ""]),
            "created_at": iso_datetime(random_datetime(datetime(2023, 1, 1), NOW - timedelta(days=10))),
            "updated_at": iso_datetime(random_datetime(datetime(2023, 1, 1), NOW)),
        }
        purchase_order_items[ref] = row
        placeholder_po_item_map[poref].append(ref)

register_table("purchase_order_item", purchase_order_items, "purchase_order_item_ref")
purchase_order_item_ids = registry["purchase_order_item"]

# =========================
# 8. purchase_change_request
# =========================
validate_dependencies("purchasechangerequests")
purchase_change_requests = {}
purchase_change_request_count = max(30, NUM_EMP)

change_target_candidates = []
for x in placeholder_po_refs:
    change_target_candidates.append(("purchase_order", x))
for x in placeholder_contract_refs:
    change_target_candidates.append(("purchase_contract", x))

for i in range(purchase_change_request_count):
    ref = next_id("PCR")
    target_type, target_ref = choice(change_target_candidates)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = weighted_choice([
        ("pending", 20), ("approved", 25), ("rejected", 15),
        ("executed", 20), ("cancelled", 10), ("approved", 10)
    ])
    approved_at = None
    rejected_reason = None
    executed_at = None

    if status in ("approved", "executed"):
        approved_dt = random_datetime(created_dt, NOW)
        approved_at = iso_datetime(approved_dt)
    if status == "executed":
        executed_at = iso_datetime(random_datetime(parse_dt(approved_at), NOW))
    if status == "rejected":
        rejected_reason = choice(["变更依据不足", "对预算影响过大", "与合同条款冲突", "审批未通过"])

    purchase_change_requests[ref] = {
        "purchase_change_request_ref": ref,
        "change_code": f"CHG-{created_dt.year}-{i+1:04d}",
        "change_target_type": target_type,
        "change_target_ref": target_ref,
        "change_type": weighted_choice([
            ("quantity_adjustment", 25), ("price_adjustment", 20), ("delivery_date_change", 20),
            ("item_addition", 10), ("item_removal", 10), ("cancellation", 5), ("other", 10)
        ]),
        "change_reason": choice([
            "需求范围调整", "预算优化", "供应商交期变更", "项目进度调整", "现场实施条件变化"
        ]),
        "change_details": {
            "quantity": {"before": random.randint(1, 50), "after": random.randint(1, 80)},
            "delivery_date": {"before": iso_date(created_dt + timedelta(days=15)), "after": iso_date(created_dt + timedelta(days=30))}
        },
        "impact_amount": rand_amount(-50000, 200000),
        "requestor_ref": choice(active_employee_ids),
        "change_status": status,
        "approved_at": approved_at,
        "rejected_reason": rejected_reason,
        "executed_at": executed_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("purchase_change_request", purchase_change_requests, "purchase_change_request_ref")
purchase_change_request_ids = registry["purchase_change_request"]

# =========================
# 9. goods_receipt_item
# Must exist before goods_receipt in required order.
# Create placeholder GR refs and reconcile later.
# =========================
validate_dependencies("goodsreceiptitems")
goods_receipt_items = {}
placeholder_gr_refs = [f"GRC_PLACEHOLDER_{i:03d}" for i in range(max(30, NUM_EMP // 2))]
placeholder_gr_item_map = {}

for grref in placeholder_gr_refs:
    placeholder_gr_item_map[grref] = []
    item_count = random.randint(1, 4)
    po_item_candidates = sample(purchase_order_item_ids, item_count)
    for poi in po_item_candidates:
        poi_row = purchase_order_items[poi]
        max_received = max(1, poi_row["quantity"])
        received_qty = random.randint(1, max_received)
        rejected_qty = random.randint(0, min(received_qty, max(1, received_qty // 4)))
        ref = next_id("GRI")
        row = {
            "goods_receipt_item_ref": ref,
            "goods_receipt_ref": grref,
            "purchase_order_item_ref": poi,
            "item_name": poi_row["item_name"],
            "received_quantity": received_qty,
            "rejected_quantity": rejected_qty,
            "unit": poi_row["unit"],
            "item_condition": weighted_choice([
                ("good", 70), ("damaged", 10), ("defective", 10), ("wrong_item", 10)
            ]),
            "notes": choice(["外包装完好", "需复检", "数量待确认", "存在轻微瑕疵", ""]),
            "created_at": iso_datetime(random_datetime(datetime(2023, 1, 1), NOW)),
            "updated_at": iso_datetime(random_datetime(datetime(2023, 1, 1), NOW)),
        }
        goods_receipt_items[ref] = row
        placeholder_gr_item_map[grref].append(ref)

register_table("goods_receipt_item", goods_receipt_items, "goods_receipt_item_ref")
goods_receipt_item_ids = registry["goods_receipt_item"]

# =========================
# 10. acceptance_record
# Placeholder goods_receipt_ref / purchase_order_ref allowed now, reconciled later where possible
# =========================
validate_dependencies("acceptancerecords")
acceptance_records = {}
acceptance_record_count = max(25, NUM_EMP // 2)

for i in range(acceptance_record_count):
    ref = next_id("ACC")
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    overall_result = weighted_choice([
        ("accepted", 55), ("partially_accepted", 20), ("rejected", 10), ("conditional", 15)
    ])
    accepted_quantity = random.randint(1, 100)
    rejected_quantity = 0 if overall_result == "accepted" else random.randint(0, 20)
    acceptance_records[ref] = {
        "acceptance_record_ref": ref,
        "acceptance_code": f"ACPT-{created_dt.year}-{i+1:04d}",
        "goods_receipt_ref": choice(placeholder_gr_refs),
        "purchase_order_ref": choice(placeholder_po_refs),
        "inspector_ref": choice(active_employee_ids),
        "inspection_date": iso_date(created_dt),
        "inspection_type": weighted_choice([
            ("full", 35), ("sampling", 30), ("visual", 15), ("functional", 15), ("skip", 5)
        ]),
        "overall_result": overall_result,
        "accepted_quantity": accepted_quantity,
        "rejected_quantity": rejected_quantity,
        "defect_description": None if overall_result == "accepted" else choice([
            "存在外观损伤", "参数与规格不符", "功能测试异常", "部分批次存在缺陷"
        ]),
        "corrective_action": None if overall_result == "accepted" else choice([
            "退货重发", "供应商补货", "降级使用并索赔", "返工整改"
        ]),
        "acceptance_report_file_ref": maybe(choice(file_ids), 0.5),
        "acceptance_status": weighted_choice([
            ("pending", 10), ("in_progress", 20), ("completed", 65), ("cancelled", 5)
        ]),
        "notes": choice(["按标准流程执行验收", "需跟进供应商整改", "已同步业务部门", ""]),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("acceptance_record", acceptance_records, "acceptance_record_ref")
acceptance_record_ids = registry["acceptance_record"]

# =========================
# 11. acceptance_item
# =========================
validate_dependencies("acceptanceitems")
acceptance_items = {}
for acc_id in acceptance_record_ids:
    acc = acceptance_records[acc_id]
    item_candidates = sample(goods_receipt_item_ids, random.randint(1, 3))
    for gri in item_candidates:
        gri_row = goods_receipt_items[gri]
        inspected = gri_row["received_quantity"]
        accepted_qty = random.randint(0, inspected)
        rejected_qty = inspected - accepted_qty
        if rejected_qty == 0:
            result_status = "accepted"
        elif accepted_qty == 0:
            result_status = "rejected"
        else:
            result_status = "conditional"

        ref = next_id("ACI")
        acceptance_items[ref] = {
            "acceptance_item_ref": ref,
            "acceptance_record_ref": acc_id,
            "goods_receipt_item_ref": gri,
            "item_name": gri_row["item_name"],
            "inspected_quantity": inspected,
            "accepted_quantity": accepted_qty,
            "rejected_quantity": rejected_qty,
            "result": result_status,
            "defect_description": None if result_status == "accepted" else choice([
                "包装破损", "批次差异", "型号不符", "性能不稳定"
            ]),
            "notes": choice(["需补充资料", "已拍照留档", "建议复验", ""]),
            "created_at": acc["created_at"],
            "updated_at": iso_datetime(random_datetime(parse_dt(acc["created_at"]), NOW)),
        }

register_table("acceptance_item", acceptance_items, "acceptance_item_ref")
acceptance_item_ids = registry["acceptance_item"]

# =========================
# 12. approval_flow_template
# =========================
validate_dependencies("approvalflowtemplates")
approval_flow_templates = {}
applicable_types = [
    "purchase_requisition", "purchase_order", "purchase_contract",
    "purchase_change_request", "supplier_onboarding"
]

template_count = max(10, len(applicable_types) * 3)
for i in range(template_count):
    ref = next_id("AFT")
    created_dt = random_datetime(datetime(2021, 1, 1), NOW)
    applicable = applicable_types[i % len(applicable_types)]
    approval_flow_templates[ref] = {
        "approval_flow_template_ref": ref,
        "template_name": f"{applicable}审批流程模板{i+1}",
        "template_code": f"AFT-{applicable[:3].upper()}-{i+1:03d}",
        "applicable_type": applicable,
        "condition_rules": {
            "amount_threshold": rand_amount(5000, 500000),
            "department_ref": maybe(choice(department_ids), 0.5),
            "procurement_category_ref": maybe(choice(procurement_category_ids), 0.5)
        },
        "priority": random.randint(1, 100),
        "template_status": weighted_choice([("active", 70), ("inactive", 20), ("deprecated", 10)]),
        "description": "用于采购业务审批路径自动匹配的流程模板。",
        "created_by_ref": choice(active_employee_ids),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("approval_flow_template", approval_flow_templates, "approval_flow_template_ref")
approval_flow_template_ids = registry["approval_flow_template"]

# =========================
# 13. approval_flow_node
# =========================
validate_dependencies("approvalflownodes")
approval_flow_nodes = {}
for tmpl_id in approval_flow_template_ids:
    node_count = random.randint(2, 4)
    created_dt = parse_dt(approval_flow_templates[tmpl_id]["created_at"])
    for seq in range(1, node_count + 1):
        ref = next_id("AFN")
        approver_type = weighted_choice([
            ("employee", 25), ("role", 25), ("department_head", 25), ("direct_manager", 25)
        ])
        approver_ref = None
        if approver_type == "employee":
            approver_ref = choice(active_employee_ids)
        elif approver_type == "role":
            approver_ref = choice(role_ids)

        approval_flow_nodes[ref] = {
            "approval_flow_node_ref": ref,
            "approval_flow_template_ref": tmpl_id,
            "node_sequence": seq,
            "node_name": choice(["直属主管审批", "部门负责人审批", "采购复核", "财务审批", "总经理审批"]),
            "approver_type": approver_type,
            "approver_ref": approver_ref,
            "fallback_approver_ref": maybe(choice(active_employee_ids), 0.3),
            "auto_approve_hours": maybe(random.choice([24, 48, 72, 96]), 0.3),
            "created_at": iso_datetime(created_dt + timedelta(minutes=seq)),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }

register_table("approval_flow_node", approval_flow_nodes, "approval_flow_node_ref")
approval_flow_node_ids = registry["approval_flow_node"]

# =========================
# 14. approval_instance
# =========================
validate_dependencies("approvalinstances")
approval_instances = {}
approval_target_pool = []
for x in purchase_requisition_ids:
    approval_target_pool.append(("purchase_requisition", x))
for x in purchase_change_request_ids:
    approval_target_pool.append(("purchase_change_request", x))
for x in placeholder_po_refs[:20]:
    approval_target_pool.append(("purchase_order", x))
for x in placeholder_contract_refs[:20]:
    approval_target_pool.append(("purchase_contract", x))
for x in supplier_ids[:20]:
    approval_target_pool.append(("supplier_onboarding", x))

approval_instance_count = max(40, NUM_EMP)
for i in range(approval_instance_count):
    ref = next_id("API")
    template_id = choice(approval_flow_template_ids)
    ttype, tref = choice(approval_target_pool)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = weighted_choice([
        ("in_progress", 35), ("approved", 35), ("rejected", 15), ("cancelled", 10), ("withdrawn", 5)
    ])
    completed_at = None
    if status != "in_progress":
        completed_at = iso_datetime(random_datetime(created_dt, NOW))

    approval_instances[ref] = {
        "approval_instance_ref": ref,
        "approval_flow_template_ref": template_id,
        "target_type": ttype,
        "target_ref": tref,
        "initiator_ref": choice(active_employee_ids),
        "current_node_sequence": random.randint(1, 4),
        "approval_status": status,
        "submitted_at": iso_datetime(created_dt),
        "completed_at": completed_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("approval_instance", approval_instances, "approval_instance_ref")
approval_instance_ids = registry["approval_instance"]

# =========================
# 15. approval_action
# =========================
validate_dependencies("approvalactions")
approval_actions = {}
for ai_id in approval_instance_ids:
    ai = approval_instances[ai_id]
    action_count = random.randint(1, 3 if ai["approval_status"] != "in_progress" else 2)
    base_dt = parse_dt(ai["submitted_at"])
    for seq in range(1, action_count + 1):
        ref = next_id("APA")
        acted_dt = random_datetime(base_dt, NOW)
        action = weighted_choice([
            ("approve", 50), ("reject", 15), ("return", 10), ("delegate", 10), ("comment", 15)
        ])
        if ai["approval_status"] == "approved":
            action = choice(["approve", "comment"])
        elif ai["approval_status"] == "rejected":
            action = choice(["reject", "comment"])
        approval_actions[ref] = {
            "approval_action_ref": ref,
            "approval_instance_ref": ai_id,
            "node_sequence": seq,
            "approver_ref": choice(active_employee_ids),
            "action": action,
            "comments": choice([
                "同意，按流程继续推进。",
                "请补充报价对比材料。",
                "预算影响需要进一步说明。",
                "审批通过。",
                "请根据意见修改后重提。"
            ]),
            "acted_at": iso_datetime(acted_dt),
            "created_at": iso_datetime(acted_dt),
        }

register_table("approval_action", approval_actions, "approval_action_ref")
approval_action_ids = registry["approval_action"]

# =========================
# 16. procurement_permission_rule
# =========================
validate_dependencies("procurementpermissionrules")
procurement_permission_rules = {}
permission_rule_count = max(20, NUM_EMP // 2)
allowed_ops_pool = [
    "create_requisition", "create_order", "approve", "create_contract",
    "manage_supplier", "view_reports", "export_data"
]
for i in range(permission_rule_count):
    ref = next_id("PPR")
    created_dt = random_datetime(datetime(2021, 1, 1), NOW)
    employee_ref = maybe(choice(active_employee_ids), 0.35)
    role_ref = None if employee_ref else maybe(choice(role_ids), 0.7)
    department_ref = maybe(choice(department_ids), 0.5)
    category_ref = maybe(choice(procurement_category_ids), 0.5)
    procurement_permission_rules[ref] = {
        "procurement_permission_rule_ref": ref,
        "rule_name": f"采购权限规则{i+1}",
        "rule_code": f"PPR-{i+1:03d}",
        "employee_ref": employee_ref,
        "role_ref": role_ref,
        "department_ref": department_ref,
        "procurement_category_ref": category_ref,
        "max_single_amount": maybe(rand_amount(5000, 1000000), 0.8),
        "max_monthly_amount": maybe(rand_amount(50000, 5000000), 0.7),
        "currency": cn_currency(),
        "allowed_operations": sample(allowed_ops_pool, random.randint(1, 4)),
        "rule_status": weighted_choice([("active", 70), ("inactive", 20), ("expired", 10)]),
        "created_by_ref": choice(active_employee_ids),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("procurement_permission_rule", procurement_permission_rules, "procurement_permission_rule_ref")
procurement_permission_rule_ids = registry["procurement_permission_rule"]

# =========================
# 17. procurement_training_course
# =========================
validate_dependencies("procurementtrainingcourses")
procurement_training_courses = {}
course_count = max(12, NUM_EMP // 6)
for i in range(course_count):
    ref = next_id("PTC")
    created_dt = random_datetime(datetime(2021, 1, 1), NOW)
    ctype = weighted_choice([
        ("process_training", 30), ("system_training", 30), ("compliance", 20), ("skill_development", 20)
    ])
    cert_required = random.random() < 0.6
    procurement_training_courses[ref] = {
        "procurement_training_course_ref": ref,
        "course_title": choice([
            "采购流程与制度基础", "供应商准入与评估", "采购系统操作实务",
            "合同合规风险控制", "验收与质量管理", "招采谈判技巧"
        ]) + f"-{i+1}",
        "course_code": f"COURSE-{i+1:03d}",
        "course_type": ctype,
        "content_summary": "课程覆盖采购流程、审批规则、合同控制、系统操作及合规要求。",
        "duration_hours": random.choice([2, 4, 6, 8, 12]),
        "is_certification_required": cert_required,
        "certification_validity_months": random.choice([12, 24, 36]) if cert_required else None,
        "material_file_ref": maybe(choice(file_ids), 0.5),
        "course_status": weighted_choice([("active", 70), ("archived", 15), ("draft", 15)]),
        "created_by_ref": choice(active_employee_ids),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("procurement_training_course", procurement_training_courses, "procurement_training_course_ref")
procurement_training_course_ids = registry["procurement_training_course"]

# =========================
# 18. procurement_training_record
# =========================
validate_dependencies("procurementtrainingrecords")
procurement_training_records = {}
training_record_count = max(NUM_EMP * 2, SCALE)

for i in range(training_record_count):
    ref = next_id("PTR")
    course_id = choice(procurement_training_course_ids)
    emp_id = choice(employee_ids)
    enroll_dt = random_datetime(datetime(2022, 1, 1), NOW)
    status = weighted_choice([
        ("enrolled", 15), ("in_progress", 20), ("completed", 45), ("failed", 10), ("cancelled", 10)
    ])
    completion_date = None
    score = None
    cert_no = None
    cert_expiry = None
    cert_file = None

    course = procurement_training_courses[course_id]
    if status in ("completed", "failed"):
        complete_dt = random_datetime(enroll_dt, NOW)
        completion_date = iso_date(complete_dt)
        score = round(random.uniform(60, 99), 2) if status == "completed" else round(random.uniform(30, 59), 2)
        if status == "completed" and course["is_certification_required"]:
            cert_no = f"CERT-{complete_dt.year}-{i+1:05d}"
            cert_expiry = iso_date(complete_dt + timedelta(days=30 * (course["certification_validity_months"] or 12)))
            cert_file = maybe(choice(file_ids), 0.5)

    procurement_training_records[ref] = {
        "procurement_training_record_ref": ref,
        "procurement_training_course_ref": course_id,
        "employee_ref": emp_id,
        "enrollment_date": iso_date(enroll_dt),
        "completion_date": completion_date,
        "score": score,
        "certification_number": cert_no,
        "certification_expiry_date": cert_expiry,
        "certificate_file_ref": cert_file,
        "record_status": status,
        "created_at": iso_datetime(enroll_dt),
        "updated_at": iso_datetime(random_datetime(enroll_dt, NOW)),
    }

register_table("procurement_training_record", procurement_training_records, "procurement_training_record_ref")
procurement_training_record_ids = registry["procurement_training_record"]

# =========================
# 19. procurement_issue_ticket
# =========================
validate_dependencies("procurementissuetickets")
procurement_issue_tickets = {}
issue_target_pool = []
for x in purchase_requisition_ids[:50]:
    issue_target_pool.append(("purchase_requisition", x))
for x in supplier_ids[:50]:
    issue_target_pool.append(("supplier", x))
for x in placeholder_po_refs[:50]:
    issue_target_pool.append(("purchase_order", x))
for x in placeholder_gr_refs[:50]:
    issue_target_pool.append(("goods_receipt", x))

ticket_count = max(NUM_EMP * 2, SCALE)
for i in range(ticket_count):
    ref = next_id("PIT")
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = weighted_choice([
        ("open", 25), ("in_progress", 25), ("resolved", 25), ("closed", 15), ("cancelled", 10)
    ])
    rel_type, rel_ref = choice(issue_target_pool) if random.random() < 0.8 else (None, None)
    resolved_at = None
    resolution = None
    if status in ("resolved", "closed"):
        rdt = random_datetime(created_dt, NOW)
        resolved_at = iso_datetime(rdt)
        resolution = choice([
            "已修复系统配置并恢复流程。",
            "已与供应商沟通完成补货。",
            "已完成质量复检并关闭问题。",
            "已优化流程说明并重新发起审批。"
        ])

    procurement_issue_tickets[ref] = {
        "procurement_issue_ticket_ref": ref,
        "ticket_code": f"TIC-{created_dt.year}-{i+1:05d}",
        "issue_type": weighted_choice([
            ("system_error", 15), ("process_issue", 20), ("supplier_complaint", 15),
            ("delivery_issue", 20), ("quality_issue", 20), ("other", 10)
        ]),
        "related_resource_type": rel_type,
        "related_resource_ref": rel_ref,
        "title": choice([
            "供应商交付异常", "采购审批卡点", "验收结果争议",
            "系统下单失败", "合同金额不一致", "到货数量差异"
        ]),
        "description": "问题发生于采购业务执行过程中，已提交相关证据与说明，待跟进处理。",
        "severity": weighted_choice([("low", 25), ("medium", 40), ("high", 25), ("critical", 10)]),
        "reporter_ref": choice(employee_ids),
        "assignee_ref": maybe(choice(active_employee_ids), 0.7),
        "resolution": resolution,
        "ticket_status": status,
        "resolved_at": resolved_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("procurement_issue_ticket", procurement_issue_tickets, "procurement_issue_ticket_ref")
procurement_issue_ticket_ids = registry["procurement_issue_ticket"]

# =========================
# 20. supplier_contact
# =========================
validate_dependencies("suppliercontacts")
supplier_contacts = {}
for sup_id in supplier_ids:
    contact_count = random.randint(1, 3)
    primary_used = False
    created_dt = parse_dt(suppliers[sup_id]["created_at"])
    for idx in range(contact_count):
        ref = next_id("SPC")
        is_primary = False
        if not primary_used:
            is_primary = True
            primary_used = True
        supplier_contacts[ref] = {
            "supplier_contact_ref": ref,
            "supplier_ref": sup_id,
            "contact_name": fake.name(),
            "contact_title": choice(contact_titles),
            "phone": phone(),
            "email": email(),
            "is_primary": is_primary,
            "status": weighted_choice([("active", 85), ("inactive", 15)]),
            "created_at": iso_datetime(random_datetime(created_dt, NOW)),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }

register_table("supplier_contact", supplier_contacts, "supplier_contact_ref")
supplier_contact_ids = registry["supplier_contact"]

# =========================
# 21. supplier_qualification
# =========================
validate_dependencies("supplierqualifications")
supplier_qualifications = {}
qualification_types = [
    "business_license", "tax_registration", "iso_certification",
    "industry_permit", "safety_certification", "environmental_certification", "other"
]
for sup_id in supplier_ids:
    q_count = random.randint(1, 4)
    created_dt = parse_dt(suppliers[sup_id]["created_at"])
    for _ in range(q_count):
        ref = next_id("SPQ")
        issue_dt = random_datetime(datetime(2020, 1, 1), NOW - timedelta(days=30))
        expiry_dt = issue_dt + timedelta(days=random.randint(365, 1460))
        verification_status = weighted_choice([
            ("pending", 15), ("verified", 60), ("rejected", 10), ("expired", 15)
        ])
        if expiry_dt < NOW:
            verification_status = "expired"
        verified_by = None
        verified_at = None
        if verification_status in ("verified", "rejected", "expired"):
            verified_by = choice(active_employee_ids)
            verified_at = iso_datetime(random_datetime(issue_dt, min(expiry_dt, NOW)))
        supplier_qualifications[ref] = {
            "supplier_qualification_ref": ref,
            "supplier_ref": sup_id,
            "qualification_type": choice(qualification_types),
            "qualification_name": choice([
                "营业执照", "税务登记证明", "ISO9001质量体系认证", "行业经营许可",
                "安全生产许可证", "环保合规证明", "其他资质文件"
            ]),
            "certificate_number": "CERT" + "".join(random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10)),
            "issuing_authority": choice(["市场监督管理局", "税务局", "认证中心", "行业主管部门", "第三方认证机构"]),
            "issue_date": iso_date(issue_dt),
            "expiry_date": iso_date(expiry_dt),
            "file_attachment_ref": maybe(choice(file_ids), 0.6),
            "verification_status": verification_status,
            "verified_by_ref": verified_by,
            "verified_at": verified_at,
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }

register_table("supplier_qualification", supplier_qualifications, "supplier_qualification_ref")
supplier_qualification_ids = registry["supplier_qualification"]

# =========================
# 22. supplier_category
# =========================
validate_dependencies("suppliercategories")
supplier_categories = {}
for sup_id in supplier_ids:
    categories = sample(procurement_category_ids, random.randint(1, 4))
    for cat_id in categories:
        ref = next_id("SPCG")
        created_dt = parse_dt(suppliers[sup_id]["created_at"])
        supplier_categories[ref] = {
            "supplier_category_ref": ref,
            "supplier_ref": sup_id,
            "procurement_category_ref": cat_id,
            "is_preferred": random.random() < 0.3,
            "status": weighted_choice([("active", 85), ("removed", 15)]),
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }

register_table("supplier_category", supplier_categories, "supplier_category_ref")
supplier_category_ids = registry["supplier_category"]

# =========================
# 23. supplier_evaluation
# =========================
validate_dependencies("supplierevaluations")
supplier_evaluations = {}
evaluation_periods = [period_label(datetime(2024, m, 1)) for m in [1, 4, 7, 10]] + [period_label(datetime(2025, m, 1)) for m in [1, 4]]
for sup_id in supplier_ids:
    eval_count = random.randint(1, 3)
    periods = sample(evaluation_periods, eval_count)
    for p in periods:
        ref = next_id("SPE")
        quality = round(random.uniform(60, 98), 2)
        delivery = round(random.uniform(55, 98), 2)
        price = round(random.uniform(50, 98), 2)
        service = round(random.uniform(60, 98), 2)
        overall = round(quality * 0.3 + delivery * 0.25 + price * 0.2 + service * 0.25, 2)
        if overall >= 90:
            rating = "A"
        elif overall >= 80:
            rating = "B"
        elif overall >= 70:
            rating = "C"
        elif overall >= 60:
            rating = "D"
        else:
            rating = "E"
        created_dt = random_datetime(datetime(2024, 1, 1), NOW)
        supplier_evaluations[ref] = {
            "supplier_evaluation_ref": ref,
            "supplier_ref": sup_id,
            "evaluation_period": p,
            "quality_score": quality,
            "delivery_score": delivery,
            "price_score": price,
            "service_score": service,
            "overall_score": overall,
            "rating": rating,
            "evaluator_ref": choice(active_employee_ids),
            "comments": choice([
                "整体交付表现稳定，建议保持合作。",
                "价格竞争力较强，但服务响应仍需提升。",
                "质量表现良好，适合纳入优选池。",
                "交付存在波动，建议持续观察。"
            ]),
            "status": weighted_choice([("draft", 10), ("submitted", 30), ("approved", 50), ("rejected", 10)]),
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }

register_table("supplier_evaluation", supplier_evaluations, "supplier_evaluation_ref")
supplier_evaluation_ids = registry["supplier_evaluation"]

# =========================
# 24. sourcing_supplier
# =========================
validate_dependencies("sourcingsuppliers")
sourcing_suppliers = {}
for sprj_id in sourcing_project_ids:
    participants = sample(active_supplier_ids, random.randint(2, min(6, len(active_supplier_ids))))
    invited_dt = parse_dt(sourcing_projects[sprj_id]["created_at"])
    rank_pool = list(range(1, len(participants) + 1))
    random.shuffle(rank_pool)
    for idx, sup_id in enumerate(participants):
        ref = next_id("SSP")
        inv_status = weighted_choice([
            ("invited", 20), ("accepted", 45), ("declined", 15), ("no_response", 20)
        ])
        qual_check = weighted_choice([("pending", 20), ("passed", 65), ("failed", 15)])
        eval_score = None
        eval_rank = None
        responded_at = None
        status = "active"

        if inv_status in ("accepted", "declined"):
            responded_at = iso_datetime(random_datetime(invited_dt, NOW))
        if inv_status == "accepted" and qual_check == "passed":
            eval_score = round(random.uniform(60, 98), 2)
            eval_rank = rank_pool[idx]
        if qual_check == "failed":
            status = "disqualified"
        if inv_status == "declined":
            status = "withdrawn"

        sourcing_suppliers[ref] = {
            "sourcing_supplier_ref": ref,
            "sourcing_project_ref": sprj_id,
            "supplier_ref": sup_id,
            "invitation_status": inv_status,
            "qualification_check": qual_check,
            "evaluation_score": eval_score,
            "evaluation_rank": eval_rank,
            "evaluation_comments": choice([
                "资质满足要求。", "商务条款具备竞争力。", "交付能力需进一步核实。", "历史合作记录良好。"
            ]),
            "status": status,
            "invited_at": iso_datetime(invited_dt),
            "responded_at": responded_at,
            "created_at": iso_datetime(invited_dt),
            "updated_at": iso_datetime(random_datetime(invited_dt, NOW)),
        }

register_table("sourcing_supplier", sourcing_suppliers, "sourcing_supplier_ref")
sourcing_supplier_ids = registry["sourcing_supplier"]

# =========================
# 25. quotation
# =========================
validate_dependencies("quotations")
quotations = {}
quotation_count = max(50, NUM_EMP)

for i in range(quotation_count):
    ref = next_id("QUO")
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    project_ref = maybe(choice(sourcing_project_ids), 0.7)
    supplier_ref = choice(active_supplier_ids)
    cat = sourcing_projects[project_ref]["procurement_category_ref"] if project_ref else choice(procurement_category_ids)
    total = rand_amount(5000, 1000000)
    tax_rate = choice([0.06, 0.09, 0.13])
    status = weighted_choice([
        ("draft", 10), ("submitted", 30), ("under_review", 20),
        ("accepted", 15), ("rejected", 10), ("expired", 10), ("withdrawn", 5)
    ])
    quotations[ref] = {
        "quotation_ref": ref,
        "quotation_code": f"QUO-{created_dt.year}-{i+1:05d}",
        "sourcing_project_ref": project_ref,
        "supplier_ref": supplier_ref,
        "procurement_category_ref": cat,
        "currency": cn_currency(),
        "total_amount": total,
        "tax_rate": tax_rate,
        "tax_amount": round(total * tax_rate, 2),
        "validity_date": iso_date(created_dt + timedelta(days=random.randint(15, 90))),
        "payment_terms": choice(payment_terms_pool),
        "delivery_terms": choice(delivery_terms_pool),
        "quotation_file_ref": maybe(choice(file_ids), 0.6),
        "submitted_by_ref": choice(active_employee_ids),
        "quotation_status": status,
        "notes": choice([
            "报价含税含运费。", "报价有效期内可锁价。", "交付周期可协商优化。", "需结合最终采购量调整。"
        ]),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

register_table("quotation", quotations, "quotation_ref")
quotation_ids = registry["quotation"]

# =========================
# 26. purchase_contract
# Reconcile contract_items placeholder refs -> real contract refs
# =========================
validate_dependencies("purchasecontracts")
purchase_contracts = {}
contract_count = len(placeholder_contract_refs)
real_contract_refs = []

for i, placeholder_ref in enumerate(placeholder_contract_refs, 1):
    ref = next_id("PCON")
    real_contract_refs.append(ref)
    created_dt = random_datetime(datetime(2022, 1, 1), NOW)
    supplier_ref = choice(approved_supplier_ids) if approved_supplier_ids else choice(active_supplier_ids)
    status = weighted_choice([
        ("draft", 10), ("pending_approval", 15), ("active", 35),
        ("suspended", 10), ("expired", 10), ("terminated", 10), ("completed", 10)
    ])
    effective_dt = created_dt + timedelta(days=random.randint(1, 30))
    expiry_dt = effective_dt + timedelta(days=random.randint(180, 1095))
    signed_at = None
    if status in ("active", "suspended", "expired", "terminated", "completed"):
        signed_at = iso_datetime(random_datetime(created_dt, effective_dt))
    termination_reason = None
    if status == "terminated":
        termination_reason = choice(["违约终止", "合作终止", "项目取消", "长期履约不达标"])

    sourcing_ref = maybe(choice(awarded_sourcing_project_ids), 0.5)
    purchase_contracts[ref] = {
        "purchase_contract_ref": ref,
        "contract_code": f"CON-{effective_dt.year}-{i:04d}",
        "contract_title": choice([
            "年度框架采购合同", "软件授权采购合同", "设备采购合同", "技术服务合同", "运维服务合同"
        ]) + f"-{i}",
        "contract_type": weighted_choice([
            ("fixed_price", 35), ("cost_plus", 10), ("time_and_materials", 15), ("framework", 25), ("blanket", 15)
        ]),
        "supplier_ref": supplier_ref,
        "procurement_category_ref": choice(procurement_category_ids),
        "sourcing_project_ref": sourcing_ref,
        "currency": cn_currency(),
        "total_amount": rand_amount(50000, 5000000),
        "tax_rate": choice([0.06, 0.09, 0.13]),
        "payment_terms": choice(payment_terms_pool),
        "delivery_terms": choice(delivery_terms_pool),
        "effective_date": iso_date(effective_dt),
        "expiry_date": iso_date(expiry_dt),
        "auto_renew": random.random() < 0.3,
        "contract_file_ref": maybe(choice(file_ids), 0.7),
        "owner_employee_ref": choice(active_employee_ids),
        "signer_employee_ref": choice(active_employee_ids),
        "signed_at": signed_at,
        "contract_status": status,
        "consumed_amount": rand_amount(0, 2000000),
        "termination_reason": termination_reason,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

# reconcile contract item refs
placeholder_to_real_contract = dict(zip(placeholder_contract_refs, real_contract_refs))
for _, row in contract_items.items():
    row["purchase_contract_ref"] = placeholder_to_real_contract[row["purchase_contract_ref"]]

register_table("purchase_contract", purchase_contracts, "purchase_contract_ref")
purchase_contract_ids = registry["purchase_contract"]
contract_items_by_contract = {}
for cid, row in contract_items.items():
    contract_items_by_contract.setdefault(row["purchase_contract_ref"], []).append(cid)

# =========================
# 27. purchase_order
# Reconcile purchase_order_items placeholder refs -> real PO refs
# =========================
validate_dependencies("purchaseorders")
purchase_orders = {}
order_count = len(placeholder_po_refs)
real_po_refs = []

approved_reqs_list = approved_requisition_ids or purchase_requisition_ids

for i, placeholder_po in enumerate(placeholder_po_refs, 1):
    ref = next_id("PORD")
    real_po_refs.append(ref)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    req_ref = maybe(choice(approved_reqs_list), 0.8)
    contract_ref = maybe(choice(purchase_contract_ids), 0.5)
    supplier_ref = None
    if req_ref and requisition_approved_supplier_pref.get(req_ref):
        supplier_ref = requisition_approved_supplier_pref[req_ref]
    if not supplier_ref:
        supplier_ref = purchase_contracts[contract_ref]["supplier_ref"] if contract_ref else choice(approved_supplier_ids or active_supplier_ids)
    requestor_ref = purchase_requisitions[req_ref]["requestor_ref"] if req_ref else choice(active_employee_ids)
    dept_ref = purchase_requisitions[req_ref]["department_ref"] if req_ref else employee_department_map.get(requestor_ref, choice(department_ids))
    cat_ref = purchase_requisitions[req_ref]["procurement_category_ref"] if req_ref else choice(procurement_category_ids)
    status = weighted_choice([
        ("draft", 10), ("submitted", 10), ("approved", 15), ("rejected", 10),
        ("sent_to_supplier", 15), ("confirmed", 15), ("partially_received", 10),
        ("completed", 10), ("cancelled", 5)
    ])
    submitted_at = approved_at = sent_to_supplier_at = supplier_confirmed_at = completed_at = cancelled_at = None
    cancel_reason = None

    cursor = created_dt
    if status in ("submitted", "approved", "rejected", "sent_to_supplier", "confirmed", "partially_received", "completed", "cancelled"):
        submitted_at = iso_datetime(cursor := random_datetime(cursor, NOW))
    if status in ("approved", "sent_to_supplier", "confirmed", "partially_received", "completed", "cancelled"):
        approved_at = iso_datetime(cursor := random_datetime(parse_dt(submitted_at), NOW))
    if status in ("sent_to_supplier", "confirmed", "partially_received", "completed"):
        sent_to_supplier_at = iso_datetime(cursor := random_datetime(parse_dt(approved_at), NOW))
    if status in ("confirmed", "partially_received", "completed"):
        supplier_confirmed_at = iso_datetime(cursor := random_datetime(parse_dt(sent_to_supplier_at), NOW))
    if status == "completed":
        completed_at = iso_datetime(random_datetime(parse_dt(supplier_confirmed_at), NOW))
    if status == "cancelled":
        cancelled_at = iso_datetime(random_datetime(parse_dt(submitted_at or iso_datetime(created_dt)), NOW))
        cancel_reason = choice(["需求取消", "供应商无法履约", "审批未通过", "预算调整"])

    total_amount = 0.0
    for poi in placeholder_po_item_map[placeholder_po]:
        total_amount += purchase_order_items[poi]["line_amount"]

    tax_rate = choice([0.06, 0.09, 0.13])

    purchase_orders[ref] = {
        "purchase_order_ref": ref,
        "order_code": f"PO-{created_dt.year}-{i:05d}",
        "order_type": weighted_choice([
            ("standard", 55), ("blanket_release", 15), ("emergency", 15), ("service", 15)
        ]),
        "purchase_requisition_ref": req_ref,
        "purchase_contract_ref": contract_ref,
        "supplier_ref": supplier_ref,
        "procurement_category_ref": cat_ref,
        "department_ref": dept_ref,
        "requestor_ref": requestor_ref,
        "buyer_ref": choice(active_employee_ids),
        "currency": cn_currency(),
        "total_amount": round(total_amount, 2),
        "tax_rate": tax_rate,
        "tax_amount": round(total_amount * tax_rate, 2),
        "payment_terms": choice(payment_terms_pool),
        "delivery_address": choice(delivery_addresses),
        "expected_delivery_date": iso_date(created_dt + timedelta(days=random.randint(7, 60))),
        "priority": weighted_choice([("low", 10), ("normal", 55), ("high", 25), ("urgent", 10)]),
        "order_status": status,
        "submitted_at": submitted_at,
        "approved_at": approved_at,
        "sent_to_supplier_at": sent_to_supplier_at,
        "supplier_confirmed_at": supplier_confirmed_at,
        "completed_at": completed_at,
        "cancelled_at": cancelled_at,
        "cancel_reason": cancel_reason,
        "notes": choice(["请按合同条款执行。", "需优先安排交付。", "请同步物流信息。", ""]),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

placeholder_to_real_po = dict(zip(placeholder_po_refs, real_po_refs))
for _, row in purchase_order_items.items():
    row["purchase_order_ref"] = placeholder_to_real_po[row["purchase_order_ref"]]

register_table("purchase_order", purchase_orders, "purchase_order_ref")
purchase_order_ids = registry["purchase_order"]
purchase_order_items_by_po = {}
for poi_id, row in purchase_order_items.items():
    purchase_order_items_by_po.setdefault(row["purchase_order_ref"], []).append(poi_id)

# reconcile change target refs to real ids when possible
for _, row in purchase_change_requests.items():
    if row["change_target_type"] == "purchase_order" and row["change_target_ref"] in placeholder_to_real_po:
        row["change_target_ref"] = placeholder_to_real_po[row["change_target_ref"]]
    if row["change_target_type"] == "purchase_contract" and row["change_target_ref"] in placeholder_to_real_contract:
        row["change_target_ref"] = placeholder_to_real_contract[row["change_target_ref"]]

# reconcile approval instances / issue tickets / acceptance records refs where placeholder was used
for _, row in approval_instances.items():
    if row["target_type"] == "purchase_order" and row["target_ref"] in placeholder_to_real_po:
        row["target_ref"] = placeholder_to_real_po[row["target_ref"]]
    if row["target_type"] == "purchase_contract" and row["target_ref"] in placeholder_to_real_contract:
        row["target_ref"] = placeholder_to_real_contract[row["target_ref"]]

for _, row in procurement_issue_tickets.items():
    if row["related_resource_type"] == "purchase_order" and row["related_resource_ref"] in placeholder_to_real_po:
        row["related_resource_ref"] = placeholder_to_real_po[row["related_resource_ref"]]

# =========================
# 28. goods_receipt
# Reconcile goods_receipt_items placeholder refs -> real GR refs
# =========================
validate_dependencies("goodsreceipts")
goods_receipts = {}
goods_receipt_count = len(placeholder_gr_refs)
real_gr_refs = []

for i, placeholder_gr in enumerate(placeholder_gr_refs, 1):
    ref = next_id("GRC")
    real_gr_refs.append(ref)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    po_ref = choice(purchase_order_ids)
    supplier_ref = purchase_orders[po_ref]["supplier_ref"]
    status = weighted_choice([
        ("pending_inspection", 20), ("inspected", 15), ("accepted", 25),
        ("partially_accepted", 20), ("rejected", 10), ("completed", 10)
    ])
    goods_receipts[ref] = {
        "goods_receipt_ref": ref,
        "receipt_code": f"GR-{created_dt.year}-{i:05d}",
        "purchase_order_ref": po_ref,
        "supplier_ref": supplier_ref,
        "receiver_ref": choice(active_employee_ids),
        "receipt_date": iso_date(created_dt),
        "delivery_note_number": "DN" + "".join(random.choice("0123456789") for _ in range(8)),
        "warehouse_location": choice(warehouse_locations),
        "receipt_status": status,
        "notes": choice(["货物已清点", "待质检", "部分到货", "附送清单已收齐", ""]),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }

placeholder_to_real_gr = dict(zip(placeholder_gr_refs, real_gr_refs))
for _, row in goods_receipt_items.items():
    row["goods_receipt_ref"] = placeholder_to_real_gr[row["goods_receipt_ref"]]

register_table("goods_receipt", goods_receipts, "goods_receipt_ref")
goods_receipt_ids = registry["goods_receipt"]

# reconcile acceptance records now
for _, row in acceptance_records.items():
    if row["goods_receipt_ref"] in placeholder_to_real_gr:
        row["goods_receipt_ref"] = placeholder_to_real_gr[row["goods_receipt_ref"]]
    if row["purchase_order_ref"] in placeholder_to_real_po:
        row["purchase_order_ref"] = placeholder_to_real_po[row["purchase_order_ref"]]

# reconcile issue ticket goods_receipt refs
for _, row in procurement_issue_tickets.items():
    if row["related_resource_type"] == "goods_receipt" and row["related_resource_ref"] in placeholder_to_real_gr:
        row["related_resource_ref"] = placeholder_to_real_gr[row["related_resource_ref"]]

# =========================
# 29. quotation_item
# =========================
validate_dependencies("quotationitems")
quotation_items = {}
for quo_id in quotation_ids:
    q = quotations[quo_id]
    item_count = random.randint(1, 4)
    remaining_amount = q["total_amount"]
    for idx in range(item_count):
        ref = next_id("QTI")
        if idx == item_count - 1:
            qty = random.randint(1, 20)
            unit_price = round(max(1.0, remaining_amount / qty), 2)
            line_amount = round(qty * unit_price, 2)
        else:
            qty = random.randint(1, 20)
            unit_price = rand_amount(100, 50000)
            line_amount = round(qty * unit_price, 2)
            remaining_amount = max(0, remaining_amount - line_amount)

        quotation_items[ref] = {
            "quotation_item_ref": ref,
            "quotation_ref": quo_id,
            "item_name": choice([
                "服务器节点", "软件许可", "交换机设备", "咨询服务", "培训实施",
                "工位家具", "运维服务", "安全模块"
            ]),
            "item_description": "报价单中的明细报价项。",
            "specification": choice(spec_words) + choice(["/年度授权", "/标准配置", "/增强配置", "/含实施", "/现场服务"]),
            "unit": choice(units),
            "quantity": qty,
            "unit_price": unit_price,
            "line_amount": line_amount,
            "delivery_days": random.randint(3, 60),
            "notes": choice(["可分批交付", "含售后支持", "价格可谈", "需配合验收", ""]),
            "created_at": q["created_at"],
            "updated_at": iso_datetime(random_datetime(parse_dt(q["created_at"]), NOW)),
        }

register_table("quotation_item", quotation_items, "quotation_item_ref")

# =========================
# Final validation
# =========================
def assert_fk_exists(value, valid_ids, field_name):
    if value is not None and value not in valid_ids:
        raise ValueError(f"Invalid FK {field_name}: {value}")

for _, row in result.get("supplier_contact", {}).items():
    assert_fk_exists(row["supplier_ref"], supplier_ids, "supplier_contact.supplier_ref")

for _, row in result.get("supplier_qualification", {}).items():
    assert_fk_exists(row["supplier_ref"], supplier_ids, "supplier_qualification.supplier_ref")
    assert_fk_exists(row["file_attachment_ref"], file_ids, "supplier_qualification.file_attachment_ref")
    assert_fk_exists(row["verified_by_ref"], employee_ids, "supplier_qualification.verified_by_ref")

for _, row in result.get("supplier_category", {}).items():
    assert_fk_exists(row["supplier_ref"], supplier_ids, "supplier_category.supplier_ref")
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "supplier_category.procurement_category_ref")

for _, row in result.get("supplier_evaluation", {}).items():
    assert_fk_exists(row["supplier_ref"], supplier_ids, "supplier_evaluation.supplier_ref")
    assert_fk_exists(row["evaluator_ref"], employee_ids, "supplier_evaluation.evaluator_ref")

for _, row in result.get("sourcing_project", {}).items():
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "sourcing_project.procurement_category_ref")
    assert_fk_exists(row["bid_document_file_ref"], file_ids, "sourcing_project.bid_document_file_ref")
    assert_fk_exists(row["owner_employee_ref"], employee_ids, "sourcing_project.owner_employee_ref")
    assert_fk_exists(row["awarded_supplier_ref"], supplier_ids, "sourcing_project.awarded_supplier_ref")

for _, row in result.get("purchase_requisition", {}).items():
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "purchase_requisition.procurement_category_ref")
    assert_fk_exists(row["department_ref"], department_ids, "purchase_requisition.department_ref")
    assert_fk_exists(row["requestor_ref"], employee_ids, "purchase_requisition.requestor_ref")
    assert_fk_exists(row["suggested_supplier_ref"], supplier_ids, "purchase_requisition.suggested_supplier_ref")

for _, row in result.get("requisition_item", {}).items():
    assert_fk_exists(row["purchase_requisition_ref"], purchase_requisition_ids, "requisition_item.purchase_requisition_ref")

for _, row in result.get("purchase_contract", {}).items():
    assert_fk_exists(row["supplier_ref"], supplier_ids, "purchase_contract.supplier_ref")
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "purchase_contract.procurement_category_ref")
    assert_fk_exists(row["sourcing_project_ref"], sourcing_project_ids, "purchase_contract.sourcing_project_ref")
    assert_fk_exists(row["contract_file_ref"], file_ids, "purchase_contract.contract_file_ref")
    assert_fk_exists(row["owner_employee_ref"], employee_ids, "purchase_contract.owner_employee_ref")
    assert_fk_exists(row["signer_employee_ref"], employee_ids, "purchase_contract.signer_employee_ref")

for _, row in result.get("contract_item", {}).items():
    assert_fk_exists(row["purchase_contract_ref"], purchase_contract_ids, "contract_item.purchase_contract_ref")

for _, row in result.get("purchase_order", {}).items():
    assert_fk_exists(row["purchase_requisition_ref"], purchase_requisition_ids, "purchase_order.purchase_requisition_ref")
    assert_fk_exists(row["purchase_contract_ref"], purchase_contract_ids, "purchase_order.purchase_contract_ref")
    assert_fk_exists(row["supplier_ref"], supplier_ids, "purchase_order.supplier_ref")
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "purchase_order.procurement_category_ref")
    assert_fk_exists(row["department_ref"], department_ids, "purchase_order.department_ref")
    assert_fk_exists(row["requestor_ref"], employee_ids, "purchase_order.requestor_ref")
    assert_fk_exists(row["buyer_ref"], employee_ids, "purchase_order.buyer_ref")

for _, row in result.get("purchase_order_item", {}).items():
    assert_fk_exists(row["purchase_order_ref"], purchase_order_ids, "purchase_order_item.purchase_order_ref")
    assert_fk_exists(row["contract_item_ref"], contract_item_ids, "purchase_order_item.contract_item_ref")
    assert_fk_exists(row["requisition_item_ref"], requisition_item_ids, "purchase_order_item.requisition_item_ref")

for _, row in result.get("purchase_change_request", {}).items():
    assert_fk_exists(row["requestor_ref"], employee_ids, "purchase_change_request.requestor_ref")
    if row["change_target_type"] == "purchase_order":
        assert_fk_exists(row["change_target_ref"], purchase_order_ids, "purchase_change_request.change_target_ref")
    else:
        assert_fk_exists(row["change_target_ref"], purchase_contract_ids, "purchase_change_request.change_target_ref")

for _, row in result.get("goods_receipt", {}).items():
    assert_fk_exists(row["purchase_order_ref"], purchase_order_ids, "goods_receipt.purchase_order_ref")
    assert_fk_exists(row["supplier_ref"], supplier_ids, "goods_receipt.supplier_ref")
    assert_fk_exists(row["receiver_ref"], employee_ids, "goods_receipt.receiver_ref")

for _, row in result.get("goods_receipt_item", {}).items():
    assert_fk_exists(row["goods_receipt_ref"], goods_receipt_ids, "goods_receipt_item.goods_receipt_ref")
    assert_fk_exists(row["purchase_order_item_ref"], purchase_order_item_ids, "goods_receipt_item.purchase_order_item_ref")

for _, row in result.get("acceptance_record", {}).items():
    assert_fk_exists(row["goods_receipt_ref"], goods_receipt_ids, "acceptance_record.goods_receipt_ref")
    assert_fk_exists(row["purchase_order_ref"], purchase_order_ids, "acceptance_record.purchase_order_ref")
    assert_fk_exists(row["inspector_ref"], employee_ids, "acceptance_record.inspector_ref")
    assert_fk_exists(row["acceptance_report_file_ref"], file_ids, "acceptance_record.acceptance_report_file_ref")

for _, row in result.get("acceptance_item", {}).items():
    assert_fk_exists(row["acceptance_record_ref"], acceptance_record_ids, "acceptance_item.acceptance_record_ref")
    assert_fk_exists(row["goods_receipt_item_ref"], goods_receipt_item_ids, "acceptance_item.goods_receipt_item_ref")

for _, row in result.get("approval_flow_template", {}).items():
    assert_fk_exists(row["created_by_ref"], employee_ids, "approval_flow_template.created_by_ref")

for _, row in result.get("approval_flow_node", {}).items():
    assert_fk_exists(row["approval_flow_template_ref"], approval_flow_template_ids, "approval_flow_node.approval_flow_template_ref")
    if row["approver_type"] == "employee":
        assert_fk_exists(row["approver_ref"], employee_ids, "approval_flow_node.approver_ref")
    elif row["approver_type"] == "role":
        assert_fk_exists(row["approver_ref"], role_ids, "approval_flow_node.approver_ref")
    assert_fk_exists(row["fallback_approver_ref"], employee_ids, "approval_flow_node.fallback_approver_ref")

for _, row in result.get("approval_instance", {}).items():
    assert_fk_exists(row["approval_flow_template_ref"], approval_flow_template_ids, "approval_instance.approval_flow_template_ref")
    assert_fk_exists(row["initiator_ref"], employee_ids, "approval_instance.initiator_ref")

for _, row in result.get("approval_action", {}).items():
    assert_fk_exists(row["approval_instance_ref"], approval_instance_ids, "approval_action.approval_instance_ref")
    assert_fk_exists(row["approver_ref"], employee_ids, "approval_action.approver_ref")

for _, row in result.get("procurement_permission_rule", {}).items():
    assert_fk_exists(row["employee_ref"], employee_ids, "procurement_permission_rule.employee_ref")
    assert_fk_exists(row["role_ref"], role_ids, "procurement_permission_rule.role_ref")
    assert_fk_exists(row["department_ref"], department_ids, "procurement_permission_rule.department_ref")
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "procurement_permission_rule.procurement_category_ref")
    assert_fk_exists(row["created_by_ref"], employee_ids, "procurement_permission_rule.created_by_ref")

for _, row in result.get("procurement_training_course", {}).items():
    assert_fk_exists(row["material_file_ref"], file_ids, "procurement_training_course.material_file_ref")
    assert_fk_exists(row["created_by_ref"], employee_ids, "procurement_training_course.created_by_ref")

for _, row in result.get("procurement_training_record", {}).items():
    assert_fk_exists(row["procurement_training_course_ref"], procurement_training_course_ids, "procurement_training_record.procurement_training_course_ref")
    assert_fk_exists(row["employee_ref"], employee_ids, "procurement_training_record.employee_ref")
    assert_fk_exists(row["certificate_file_ref"], file_ids, "procurement_training_record.certificate_file_ref")

for _, row in result.get("procurement_issue_ticket", {}).items():
    assert_fk_exists(row["reporter_ref"], employee_ids, "procurement_issue_ticket.reporter_ref")
    assert_fk_exists(row["assignee_ref"], employee_ids, "procurement_issue_ticket.assignee_ref")

for _, row in result.get("quotation", {}).items():
    assert_fk_exists(row["sourcing_project_ref"], sourcing_project_ids, "quotation.sourcing_project_ref")
    assert_fk_exists(row["supplier_ref"], supplier_ids, "quotation.supplier_ref")
    assert_fk_exists(row["procurement_category_ref"], procurement_category_ids, "quotation.procurement_category_ref")
    assert_fk_exists(row["quotation_file_ref"], file_ids, "quotation.quotation_file_ref")
    assert_fk_exists(row["submitted_by_ref"], employee_ids, "quotation.submitted_by_ref")

for _, row in result.get("quotation_item", {}).items():
    assert_fk_exists(row["quotation_ref"], quotation_ids, "quotation_item.quotation_ref")

print(json.dumps(result, ensure_ascii=False, indent=2))