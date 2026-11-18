import json
import random
from datetime import datetime, timedelta
from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker("zh_CN")
Faker.seed(SEED)

result = {}

# Helper functions
def iso_datetime(dt):
    """
    功能说明（Description）：
        格式化datetime，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `dt` (Any): 业务入参，按函数语义传入。
    返回（Returns）：
        - `Any`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_date(dt):
    """
    功能说明（Description）：
        格式化date，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `dt` (Any): 业务入参，按函数语义传入。
    返回（Returns）：
        - `Any`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    return dt.strftime("%Y-%m-%d")

def random_datetime(start, end):
    """
    功能说明（Description）：
        随机生成datetime，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `start` (Any): 业务入参，按函数语义传入。
        - `end` (Any): 业务入参，按函数语义传入。
    返回（Returns）：
        - `Any`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)

BASE_DATE = datetime(2020, 1, 1)
NOW = datetime(2025, 6, 15, 12, 0, 0)

def created_updated(earliest=None, latest=None):
    """
    功能说明（Description）：
        处理updated，并返回可供后续流程使用的结果。
    参数（Parameters）：
        - `earliest` (Any): 业务入参，按函数语义传入。 默认值为 `None`。
        - `latest` (Any): 业务入参，按函数语义传入。 默认值为 `None`。
    返回（Returns）：
        - `Any`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
    异常（Raises）：
        - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
        - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
    """
    if earliest is None:
        earliest = BASE_DATE
    if latest is None:
        latest = NOW
    created = random_datetime(earliest, latest)
    updated = random_datetime(created, latest)
    return iso_datetime(created), iso_datetime(updated)

# ============================================================
# 1. user_profile (no FK deps except avatar_file_ref which we set to None initially)
# ============================================================
user_profiles = {}
NUM_USERS = 75

timezones = ["Asia/Shanghai", "Asia/Shanghai", "Asia/Shanghai", "Asia/Chongqing", "Asia/Hong_Kong"]
locales_choices = ["zh-CN", "zh-CN", "zh-CN", "en-US", "ja-JP"]

for i in range(1, NUM_USERS + 1):
    ref = f"UPROF{i:03d}"
    given = fake.first_name()
    family = fake.last_name()
    display = family + given
    status = "active"
    if i > 70:
        status = random.choice(["inactive", "suspended"])
    created, updated = created_updated()
    user_profiles[ref] = {
        "user_profile_ref": ref,
        "given_name": given,
        "family_name": family,
        "display_name": display,
        "avatar_file_ref": None,  # will be updated after file_attachments
        "bio": fake.sentence(nb_words=10),
        "phone": fake.phone_number(),
        "account_status": status,
        "preferred_locale": random.choice(locales_choices),
        "timezone": random.choice(timezones),
        "created_at": created,
        "updated_at": updated,
    }
result["user_profile"] = user_profiles

user_profile_refs = list(user_profiles.keys())
active_user_refs = [r for r, u in user_profiles.items() if u["account_status"] == "active"]

# ============================================================
# 2. departments (self-referencing hierarchy)
# ============================================================
departments = {}

dept_structure = [
    # Level 1 - root
    {"ref": "DEPT001", "name": "智联科技集团", "code": "ROOT", "parent": None, "level": 1, "type": "business", "order": 1},
    # Level 2 - business lines
    {"ref": "DEPT002", "name": "工程技术部", "code": "ENG", "parent": "DEPT001", "level": 2, "type": "business", "order": 1},
    {"ref": "DEPT003", "name": "产品部", "code": "PROD", "parent": "DEPT001", "level": 2, "type": "business", "order": 2},
    {"ref": "DEPT004", "name": "设计部", "code": "DESIGN", "parent": "DEPT001", "level": 2, "type": "business", "order": 3},
    {"ref": "DEPT005", "name": "人力资源部", "code": "HR", "parent": "DEPT001", "level": 2, "type": "functional", "order": 4},
    {"ref": "DEPT006", "name": "财务部", "code": "FIN", "parent": "DEPT001", "level": 2, "type": "functional", "order": 5},
    {"ref": "DEPT007", "name": "市场营销部", "code": "MKT", "parent": "DEPT001", "level": 2, "type": "business", "order": 6},
    {"ref": "DEPT008", "name": "数据智能部", "code": "DATA", "parent": "DEPT001", "level": 2, "type": "business", "order": 7},
    # Level 3 - sub-teams
    {"ref": "DEPT009", "name": "后端开发组", "code": "ENG-BE", "parent": "DEPT002", "level": 3, "type": "business", "order": 1},
    {"ref": "DEPT010", "name": "前端开发组", "code": "ENG-FE", "parent": "DEPT002", "level": 3, "type": "business", "order": 2},
    {"ref": "DEPT011", "name": "基础架构组", "code": "ENG-INFRA", "parent": "DEPT002", "level": 3, "type": "business", "order": 3},
    {"ref": "DEPT012", "name": "数据工程组", "code": "DATA-ENG", "parent": "DEPT008", "level": 3, "type": "business", "order": 1},
]

for d in dept_structure:
    created, updated = created_updated(BASE_DATE, datetime(2021, 6, 1))
    departments[d["ref"]] = {
        "department_ref": d["ref"],
        "department_name": d["name"],
        "department_code": d["code"],
        "parent_department_ref": d["parent"],
        "department_level": d["level"],
        "department_type": d["type"],
        "department_status": "active",
        "description": f"{d['name']}负责公司相关业务和职能",
        "display_order": d["order"],
        "created_at": created,
        "updated_at": updated,
    }
result["department"] = departments
department_refs = list(departments.keys())

# ============================================================
# 3. positions
# ============================================================
positions = {}

position_defs = [
    # P-track Engineering
    ("POS001", "初级工程师", "P5-ENG", "P", 5, "Engineering", "Backend", "active"),
    ("POS002", "中级工程师", "P6-ENG", "P", 6, "Engineering", "Backend", "active"),
    ("POS003", "高级工程师", "P7-ENG", "P", 7, "Engineering", "Backend", "active"),
    ("POS004", "资深工程师", "P8-ENG", "P", 8, "Engineering", "Backend", "active"),
    ("POS005", "首席工程师", "P9-ENG", "P", 9, "Engineering", "Backend", "active"),
    ("POS006", "前端工程师", "P6-FE", "P", 6, "Engineering", "Frontend", "active"),
    ("POS007", "高级前端工程师", "P7-FE", "P", 7, "Engineering", "Frontend", "active"),
    ("POS008", "基础架构工程师", "P7-INFRA", "P", 7, "Engineering", "Infrastructure", "active"),
    # P-track Product
    ("POS009", "产品经理", "P6-PM", "P", 6, "Product", "Product Management", "active"),
    ("POS010", "高级产品经理", "P7-PM", "P", 7, "Product", "Product Management", "active"),
    # P-track Design
    ("POS011", "UI设计师", "P5-UI", "P", 5, "Design", "UI Design", "active"),
    ("POS012", "高级UX设计师", "P7-UX", "P", 7, "Design", "UX Design", "active"),
    # P-track Data
    ("POS013", "数据分析师", "P6-DA", "P", 6, "Data", "Data Analysis", "active"),
    ("POS014", "高级数据工程师", "P7-DE", "P", 7, "Data", "Data Engineering", "active"),
    ("POS015", "ML工程师", "P7-ML", "P", 7, "Engineering", "ML", "active"),
    # P-track HR/Finance/Marketing/Legal
    ("POS016", "HR专员", "P5-HR", "P", 5, "HR", "HR Operations", "active"),
    ("POS017", "高级HR", "P7-HR", "P", 7, "HR", "HR Business Partner", "active"),
    ("POS018", "财务专员", "P5-FIN", "P", 5, "Finance", "Accounting", "active"),
    ("POS019", "高级财务", "P7-FIN", "P", 7, "Finance", "Financial Planning", "active"),
    ("POS020", "市场专员", "P5-MKT", "P", 5, "Marketing", "Digital Marketing", "active"),
    ("POS021", "法务专员", "P6-LEG", "P", 6, "Legal", "Corporate Legal", "active"),
    # M-track
    ("POS022", "团队主管", "M1-MGR", "M", 1, "Engineering", "Management", "active"),
    ("POS023", "部门经理", "M2-MGR", "M", 2, "Engineering", "Management", "active"),
    ("POS024", "高级总监", "M3-DIR", "M", 3, "Operations", "Management", "active"),
    ("POS025", "副总裁", "M4-VP", "M", 4, "Operations", "Executive", "active"),
    # Intern
    ("POS026", "实习生", "P3-INT", "P", 3, "Engineering", "Intern", "active"),
    ("POS027", "运营专员", "P5-OPS", "P", 5, "Operations", "Operations", "active"),
    ("POS028", "研究员", "P7-RES", "P", 7, "Research", "AI Research", "active"),
]

for pdef in position_defs:
    ref, title, code, track, level, family, subfamily, status = pdef
    created, updated = created_updated(BASE_DATE, datetime(2021, 1, 1))
    positions[ref] = {
        "position_ref": ref,
        "position_title": title,
        "position_code": code,
        "position_track": track,
        "position_level": level,
        "job_family": family,
        "job_subfamily": subfamily,
        "position_status": status,
        "description": f"{title}岗位，属于{family}职能族，{subfamily}方向",
        "created_at": created,
        "updated_at": updated,
    }
result["position"] = positions
position_refs = list(positions.keys())

# ============================================================
# 4. teams (depends on owner_employee_ref - but employees not created yet)
# We'll create teams with placeholder owners and fix after employees
# Actually, per generation order, teams come before employees.
# We need to handle this: teams reference owner_employee_ref but employees aren't created yet.
# Looking at the generation order: teams come before employees.
# We'll generate employee refs in advance and use them.
# ============================================================

# Pre-generate employee refs
NUM_EMPLOYEES = 75
employee_refs_list = [f"EMP{i:03d}" for i in range(1, NUM_EMPLOYEES + 1)]

# We'll define team structures
teams = {}
team_defs = [
    ("TEAM001", "核心平台项目组", "CORE-PLAT", "project", None),
    ("TEAM002", "移动端项目组", "MOBILE", "project", None),
    ("TEAM003", "数据平台项目组", "DATA-PLAT", "project", None),
    ("TEAM004", "AI算法项目组", "AI-ALGO", "project", None),
    ("TEAM005", "用户增长项目组", "USR-GROW", "project", None),
    ("TEAM006", "安全攻防项目组", "SEC-OPS", "project", None),
    ("TEAM007", "技术委员会", "TECH-COM", "committee", None),
    ("TEAM008", "文化建设委员会", "CULT-COM", "committee", None),
    ("TEAM009", "新人培训工作组", "ONBOARD-TF", "taskforce", None),
    ("TEAM010", "年度大会筹备组", "ANNUAL-TF", "taskforce", None),
    ("TEAM011", "篮球兴趣小组", "BASKETBALL", "interest", None),
    ("TEAM012", "摄影兴趣小组", "PHOTO", "interest", None),
    ("TEAM013", "读书会", "BOOK-CLUB", "interest", None),
    ("TEAM014", "后端架构子组", "BE-ARCH", "project", "TEAM001"),
    ("TEAM015", "前端架构子组", "FE-ARCH", "project", "TEAM001"),
    ("TEAM016", "数据治理子组", "DATA-GOV", "project", "TEAM003"),
    ("TEAM017", "产品体验优化组", "UX-OPT", "project", None),
    ("TEAM018", "DevOps工作组", "DEVOPS-TF", "taskforce", None),
    ("TEAM019", "开源推进委员会", "OSS-COM", "committee", None),
    ("TEAM020", "国际化项目组", "I18N", "project", None),
    ("TEAM021", "质量保障项目组", "QA-PROJ", "project", None),
    ("TEAM022", "羽毛球兴趣小组", "BADMINTON", "interest", None),
]

for tdef in team_defs:
    ref, name, code, ttype, parent = tdef
    owner = random.choice(employee_refs_list[:20])  # pick from senior employees
    created, updated = created_updated(datetime(2021, 1, 1), datetime(2024, 6, 1))
    status = "active"
    if ref in ("TEAM010",):
        status = "archived"
    teams[ref] = {
        "team_ref": ref,
        "team_name": name,
        "team_code": code,
        "team_type": ttype,
        "team_status": status,
        "description": f"{name}，负责相关工作的推进和协调",
        "owner_employee_ref": owner,
        "parent_team_ref": parent,
        "created_at": created,
        "updated_at": updated,
    }
result["team"] = teams
team_refs = list(teams.keys())

# ============================================================
# 5. mentorships (depends on mentor_ref, mentee_ref -> employees, not yet created)
# We'll use pre-generated employee refs
# ============================================================
mentorships = {}
mentorship_types = ["onboarding", "career", "technical", "leadership"]
mentorship_statuses = ["active", "completed", "terminated"]

used_pairs = set()
for i in range(1, 21):
    ref = f"MNTR{i:03d}"
    while True:
        mentor = random.choice(employee_refs_list[:30])  # senior employees as mentors
        mentee = random.choice(employee_refs_list[20:])   # junior employees as mentees
        if mentor != mentee and (mentor, mentee) not in used_pairs:
            used_pairs.add((mentor, mentee))
            break
    
    mtype = random.choice(mentorship_types)
    start = random_datetime(datetime(2022, 1, 1), datetime(2024, 12, 1))
    status = random.choice(mentorship_statuses)
    end_date = None
    if status in ("completed", "terminated"):
        end_date = iso_date(start + timedelta(days=random.randint(30, 365)))
    
    created, updated = created_updated(start, NOW)
    mentorships[ref] = {
        "mentorship_ref": ref,
        "mentor_ref": mentor,
        "mentee_ref": mentee,
        "mentorship_type": mtype,
        "start_date": iso_date(start),
        "end_date": end_date,
        "status": status,
        "notes": f"{mtype}类型导师辅导，帮助学员成长和发展",
        "created_at": created,
        "updated_at": updated,
    }
result["mentorship"] = mentorships

# ============================================================
# 6. roles
# ============================================================
roles = {}
role_defs = [
    ("ROLE001", "系统管理员", "SYS_ADMIN", "system", "active", "系统管理员，拥有全部系统权限", True),
    ("ROLE002", "HR管理员", "HR_MANAGER", "system", "active", "HR管理员，管理员工信息和组织架构", False),
    ("ROLE003", "普通员工", "EMPLOYEE", "system", "active", "普通员工角色，基础访问权限", True),
    ("ROLE004", "实习生", "INTERN", "system", "active", "实习生角色，受限访问权限", False),
    ("ROLE005", "部门主管", "DEPT_HEAD", "custom", "active", "部门主管，管理部门内事务", False),
    ("ROLE006", "团队负责人", "TEAM_LEAD", "custom", "active", "团队负责人，管理团队成员和任务", False),
    ("ROLE007", "财务管理员", "FIN_ADMIN", "custom", "active", "财务管理员，管理财务相关数据", False),
    ("ROLE008", "审计员", "AUDITOR", "custom", "active", "审计员，查看审计日志和系统操作记录", False),
]

for rdef in role_defs:
    ref, name, code, rtype, status, desc, is_default = rdef
    created, updated = created_updated(BASE_DATE, datetime(2021, 1, 1))
    roles[ref] = {
        "role_ref": ref,
        "role_name": name,
        "role_code": code,
        "role_type": rtype,
        "role_status": status,
        "description": desc,
        "is_default": is_default,
        "created_at": created,
        "updated_at": updated,
    }
result["role"] = roles
role_refs = list(roles.keys())

# ============================================================
# 7. permissions
# ============================================================
permissions = {}
perm_counter = 0

resources_actions = [
    ("employee", ["create", "read", "update", "delete", "export"]),
    ("department", ["create", "read", "update", "delete"]),
    ("team", ["create", "read", "update", "delete"]),
    ("file_attachment", ["create", "read", "update", "delete", "export"]),
    ("audit_log", ["read", "export"]),
    ("role", ["create", "read", "update", "delete"]),
    ("permission", ["read"]),
    ("notification", ["create", "read"]),
    ("org_config", ["read", "update"]),
]

scope_map = {
    "employee:create": "all",
    "employee:read": "department",
    "employee:update": "self",
    "employee:delete": "all",
    "employee:export": "department",
    "department:create": "all",
    "department:read": "all",
    "department:update": "department",
    "department:delete": "all",
    "team:create": "all",
    "team:read": "all",
    "team:update": "team",
    "team:delete": "all",
    "file_attachment:create": "self",
    "file_attachment:read": "department",
    "file_attachment:update": "self",
    "file_attachment:delete": "self",
    "file_attachment:export": "department",
    "audit_log:read": "all",
    "audit_log:export": "all",
    "role:create": "all",
    "role:read": "all",
    "role:update": "all",
    "role:delete": "all",
    "permission:read": "all",
    "notification:create": "all",
    "notification:read": "self",
    "org_config:read": "all",
    "org_config:update": "all",
}

for resource, actions in resources_actions:
    for action in actions:
        perm_counter += 1
        ref = f"PERM{perm_counter:03d}"
        code = f"{resource}:{action}"
        scope = scope_map.get(code, "self")
        created, updated = created_updated(BASE_DATE, datetime(2021, 1, 1))
        permissions[ref] = {
            "permission_ref": ref,
            "permission_code": code,
            "resource": resource,
            "action": action,
            "scope_constraint": scope,
            "description": f"允许对{resource}资源执行{action}操作",
            "permission_status": "active",
            "created_at": created,
            "updated_at": updated,
        }
result["permission"] = permissions
permission_refs = list(permissions.keys())

# ============================================================
# 8. audit_logs (depends on actor_employee_ref -> employees, resource_ref -> various)
# Use pre-generated employee refs
# ============================================================
audit_logs = {}
audit_actions = ["create", "update", "login", "logout", "approve", "assign", "export", "delete", "read"]
resource_types = ["employee", "department", "team", "role", "permission", "file_attachment", "org_config"]

ip_pool = [f"10.0.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(20)]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14) Mobile Chrome/120.0",
    "DingTalk/7.5.0 (iOS 17.2)",
    "OA-API-Client/2.1.0",
]

for i in range(1, 41):
    ref = f"ALOG{i:03d}"
    action = random.choice(audit_actions)
    actor_type = random.choices(["employee", "system", "api_client"], weights=[70, 20, 10])[0]
    actor_emp = None
    ip = None
    ua = None
    req_id = None
    
    if actor_type == "employee":
        actor_emp = random.choice(employee_refs_list)
        ip = random.choice(ip_pool)
        ua = random.choice(user_agents)
        req_id = f"req-{fake.uuid4()[:8]}-{fake.uuid4()[:4]}"
    elif actor_type == "api_client":
        ip = random.choice(ip_pool)
        ua = "OA-API-Client/2.1.0"
        req_id = f"api-{fake.uuid4()[:8]}"
    
    res_type = random.choice(resource_types)
    # Generate a plausible resource_ref
    if res_type == "employee":
        res_ref = random.choice(employee_refs_list)
    elif res_type == "department":
        res_ref = random.choice(department_refs)
    elif res_type == "team":
        res_ref = random.choice(team_refs)
    elif res_type == "role":
        res_ref = random.choice(role_refs)
    elif res_type == "permission":
        res_ref = random.choice(permission_refs)
    elif res_type == "file_attachment":
        res_ref = f"FILE{random.randint(1,20):03d}"
    else:
        res_ref = f"OCFG{random.randint(1,10):03d}"
    
    occurred = random_datetime(datetime(2023, 1, 1), NOW)
    
    changes = {}
    if action in ("create", "update"):
        field_name = random.choice(["display_name", "employment_status", "department_ref", "position_ref", "phone"])
        if action == "create":
            changes[field_name] = {"before": None, "after": fake.word()}
        else:
            changes[field_name] = {"before": fake.word(), "after": fake.word()}
    
    audit_logs[ref] = {
        "audit_log_ref": ref,
        "actor_employee_ref": actor_emp,
        "actor_type": actor_type,
        "action": action,
        "resource_type": res_type,
        "resource_ref": res_ref,
        "description": f"{actor_type}对{res_type}({res_ref})执行了{action}操作",
        "changes": changes,
        "ip_address": ip,
        "user_agent": ua,
        "request_id": req_id,
        "result": random.choices(["success", "failure", "partial"], weights=[85, 10, 5])[0],
        "occurred_at": iso_datetime(occurred),
        "created_at": iso_datetime(occurred + timedelta(seconds=random.randint(0, 2))),
    }
result["audit_log"] = audit_logs

# ============================================================
# 9. file_attachments (depends on uploaded_by_ref -> employees, associated_resource_ref -> various)
# ============================================================
file_attachments = {}

file_defs = [
    ("avatar", "png", "image/png", 50000, 200000),
    ("avatar", "jpg", "image/jpeg", 30000, 150000),
    ("document", "pdf", "application/pdf", 100000, 5000000),
    ("document", "docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 50000, 3000000),
    ("contract", "pdf", "application/pdf", 200000, 8000000),
    ("certificate", "pdf", "application/pdf", 100000, 2000000),
    ("attachment", "xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 20000, 1000000),
    ("export", "csv", "text/csv", 10000, 500000),
    ("other", "zip", "application/zip", 500000, 50000000),
]

for i in range(1, 26):
    ref = f"FILE{i:03d}"
    fdef = random.choice(file_defs)
    purpose, ext, mime, min_size, max_size = fdef
    
    uploader = random.choice(employee_refs_list)
    
    # Associated resource
    assoc_types = ["employee", "department", "team", "user_profile"]
    assoc_type = random.choice(assoc_types)
    if assoc_type == "employee":
        assoc_ref = random.choice(employee_refs_list)
    elif assoc_type == "department":
        assoc_ref = random.choice(department_refs)
    elif assoc_type == "team":
        assoc_ref = random.choice(team_refs)
    else:
        assoc_ref = random.choice(user_profile_refs)
    
    file_size = random.randint(min_size, max_size)
    checksum = fake.sha256()
    uploaded_at = random_datetime(datetime(2022, 1, 1), NOW)
    created, updated = iso_datetime(uploaded_at), iso_datetime(random_datetime(uploaded_at, NOW))
    
    file_name = f"{fake.word()}_{i:03d}.{ext}"
    bucket = random.choice(["oss://oa-files", "s3://oa-attachments"])
    storage_uri = f"{bucket}/{purpose}/{uploaded_at.strftime('%Y/%m')}/{ref}_{file_name}"
    
    file_attachments[ref] = {
        "file_attachment_ref": ref,
        "file_name": file_name,
        "file_extension": ext,
        "mime_type": mime,
        "file_size_bytes": file_size,
        "storage_uri": storage_uri,
        "checksum": checksum,
        "uploaded_by_ref": uploader,
        "associated_resource_type": assoc_type,
        "associated_resource_ref": assoc_ref,
        "file_purpose": purpose,
        "file_status": random.choices(["active", "archived", "deleted"], weights=[80, 15, 5])[0],
        "uploaded_at": iso_datetime(uploaded_at),
        "created_at": created,
        "updated_at": updated,
    }
result["file_attachment"] = file_attachments
file_refs = list(file_attachments.keys())

# Update some user profiles with avatar file refs
avatar_files = [r for r, f in file_attachments.items() if f["file_purpose"] == "avatar"]
for idx, aref in enumerate(avatar_files):
    if idx < len(user_profile_refs):
        user_profiles[user_profile_refs[idx]]["avatar_file_ref"] = aref

# ============================================================
# 10. org_configs (depends on updated_by_ref -> employees)
# ============================================================
org_configs = {}
config_defs = [
    ("OCFG001", "company_name", "智联科技有限公司", "string", "公司名称"),
    ("OCFG002", "company_short_name", "智联科技", "string", "公司简称"),
    ("OCFG003", "logo_file_ref", "FILE001", "string", "公司Logo文件引用"),
    ("OCFG004", "default_timezone", "Asia/Shanghai", "string", "默认时区"),
    ("OCFG005", "default_locale", "zh-CN", "string", "默认语言区域"),
    ("OCFG006", "fiscal_year_start", "01-01", "string", "财年起始日期"),
    ("OCFG007", "max_team_size", "50", "integer", "团队最大人数限制"),
    ("OCFG008", "probation_period_days", "90", "integer", "试用期天数"),
    ("OCFG009", "enable_sso", "true", "boolean", "是否启用SSO单点登录"),
    ("OCFG010", "password_policy", '{"min_length":8,"require_upper":true,"require_number":true,"require_special":true}', "json", "密码策略配置"),
    ("OCFG011", "attendance_start_time", "09:00", "string", "考勤开始时间"),
    ("OCFG012", "attendance_end_time", "18:00", "string", "考勤结束时间"),
    ("OCFG013", "annual_leave_days", "15", "integer", "年假天数"),
    ("OCFG014", "enable_mentorship", "true", "boolean", "是否启用导师制度"),
]

for cdef in config_defs:
    ref, key, value, ctype, desc = cdef
    updater = random.choice(employee_refs_list[:5])  # senior employees
    created, updated = created_updated(BASE_DATE, datetime(2022, 1, 1))
    org_configs[ref] = {
        "org_config_ref": ref,
        "config_key": key,
        "config_value": value,
        "config_type": ctype,
        "description": desc,
        "updated_by_ref": updater,
        "created_at": created,
        "updated_at": updated,
    }
result["org_config"] = org_configs

# ============================================================
# 11. notifications (depends on recipient_employee_ref, sender_employee_ref -> employees)
# ============================================================
notifications = {}
notif_types = ["system", "mention", "approval", "assignment", "reminder", "announcement"]
channels = ["in_app", "email", "sms", "push"]
read_statuses = ["unread", "read", "dismissed"]

notif_templates = [
    ("系统维护通知", "系统将于本周末进行维护升级，届时部分功能可能不可用", "system"),
    ("您被提及了", "{}在评论中提到了您，请查看", "mention"),
    ("审批请求", "您有一个新的{}审批待处理", "approval"),
    ("任务分配", "您被分配了一个新任务：{}", "assignment"),
    ("提醒", "您的{}即将到期，请及时处理", "reminder"),
    ("公告", "公司发布了新的{}公告，请查阅", "announcement"),
]

for i in range(1, 41):
    ref = f"NOTF{i:03d}"
    recipient = random.choice(employee_refs_list)
    sender_type = random.choice(["system", "employee"])
    sender_emp = None
    if sender_type == "employee":
        sender_emp = random.choice(employee_refs_list)
        while sender_emp == recipient:
            sender_emp = random.choice(employee_refs_list)
    
    template = random.choice(notif_templates)
    title = template[0]
    ntype = template[2]
    body = template[1].format(fake.word())
    
    channel = random.choice(channels)
    read_st = random.choices(read_statuses, weights=[40, 50, 10])[0]
    
    created_dt = random_datetime(datetime(2024, 1, 1), NOW)
    read_at = None
    if read_st in ("read", "dismissed"):
        read_at = iso_datetime(random_datetime(created_dt, NOW))
    
    # Related resource
    rel_type = None
    rel_ref = None
    if random.random() < 0.7:
        rel_type = random.choice(["employee", "team", "department", "audit_log"])
        if rel_type == "employee":
            rel_ref = random.choice(employee_refs_list)
        elif rel_type == "team":
            rel_ref = random.choice(team_refs)
        elif rel_type == "department":
            rel_ref = random.choice(department_refs)
        else:
            rel_ref = f"ALOG{random.randint(1,40):03d}"
    
    notifications[ref] = {
        "notification_ref": ref,
        "recipient_employee_ref": recipient,
        "sender_type": sender_type,
        "sender_employee_ref": sender_emp,
        "notification_type": ntype,
        "channel": channel,
        "title": title,
        "body": body,
        "related_resource_type": rel_type,
        "related_resource_ref": rel_ref,
        "read_status": read_st,
        "read_at": read_at,
        "created_at": iso_datetime(created_dt),
    }
result["notification"] = notifications

# ============================================================
# 12. employees (depends on user_profile, position)
# ============================================================
employees = {}

# Define position assignments for employees
# First few employees are senior managers
worker_types = ["full_time", "intern", "campus_recruit", "campus_intern", "contractor"]

# Build manager hierarchy
# EMP001 = VP (top, no manager)
# EMP002-EMP005 = Directors (M3), report to EMP001
# EMP006-EMP012 = Managers (M2/M1), report to directors
# Rest = individual contributors

# Position assignment plan
emp_position_map = {}
emp_manager_map = {}

# EMP001 - VP
emp_position_map["EMP001"] = "POS025"  # M4-VP
emp_manager_map["EMP001"] = None

# EMP002-005 - Directors
for e in ["EMP002", "EMP003", "EMP004", "EMP005"]:
    emp_position_map[e] = "POS024"  # M3-DIR
    emp_manager_map[e] = "EMP001"

# EMP006-012 - Managers
manager_positions = ["POS023", "POS023", "POS022", "POS022", "POS022", "POS022", "POS022"]
director_assignments = ["EMP002", "EMP002", "EMP003", "EMP003", "EMP004", "EMP005", "EMP005"]
for idx, e in enumerate([f"EMP{i:03d}" for i in range(6, 13)]):
    emp_position_map[e] = manager_positions[idx]
    emp_manager_map[e] = director_assignments[idx]

# EMP013-070 - Individual contributors
ic_positions = [
    "POS001", "POS002", "POS003", "POS004", "POS005",  # Backend eng
    "POS006", "POS007",  # Frontend
    "POS008",  # Infra
    "POS009", "POS010",  # Product
    "POS011", "POS012",  # Design
    "POS013", "POS014", "POS015",  # Data/ML
    "POS016", "POS017",  # HR
    "POS018", "POS019",  # Finance
    "POS020",  # Marketing
    "POS021",  # Legal
    "POS027",  # Operations
    "POS028",  # Research
]

# Map departments to managers
dept_manager_map = {
    "DEPT002": "EMP006",  # Engineering
    "DEPT003": "EMP007",  # Product
    "DEPT004": "EMP008",  # Design
    "DEPT005": "EMP009",  # HR
    "DEPT006": "EMP010",  # Finance
    "DEPT007": "EMP011",  # Marketing
    "DEPT008": "EMP012",  # Data
    "DEPT009": "EMP006",  # Backend (under ENG)
    "DEPT010": "EMP006",  # Frontend (under ENG)
    "DEPT011": "EMP006",  # Infra (under ENG)
    "DEPT012": "EMP012",  # Data Eng (under DATA)
}

# Assign departments to employees
emp_dept_map = {}
emp_dept_map["EMP001"] = "DEPT001"  # VP -> root
for i, e in enumerate(["EMP002", "EMP003", "EMP004", "EMP005"]):
    emp_dept_map[e] = "DEPT001"  # Directors at root level

emp_dept_map["EMP006"] = "DEPT002"  # Eng manager
emp_dept_map["EMP007"] = "DEPT003"  # Product manager
emp_dept_map["EMP008"] = "DEPT004"  # Design manager
emp_dept_map["EMP009"] = "DEPT005"  # HR manager
emp_dept_map["EMP010"] = "DEPT006"  # Finance manager
emp_dept_map["EMP011"] = "DEPT007"  # Marketing manager
emp_dept_map["EMP012"] = "DEPT008"  # Data manager

# Assign remaining employees to departments
level3_depts = ["DEPT009", "DEPT010", "DEPT011", "DEPT012"]
level2_depts = ["DEPT002", "DEPT003", "DEPT004", "DEPT005", "DEPT006", "DEPT007", "DEPT008"]
all_leaf_depts = level3_depts + ["DEPT003", "DEPT004", "DEPT005", "DEPT006", "DEPT007"]

# Department to position family mapping
dept_position_map = {
    "DEPT009": ["POS001", "POS002", "POS003", "POS004", "POS005"],  # Backend
    "DEPT010": ["POS006", "POS007"],  # Frontend
    "DEPT011": ["POS008"],  # Infra
    "DEPT012": ["POS013", "POS014"],  # Data Eng
    "DEPT003": ["POS009", "POS010"],  # Product
    "DEPT004": ["POS011", "POS012"],  # Design
    "DEPT005": ["POS016", "POS017"],  # HR
    "DEPT006": ["POS018", "POS019"],  # Finance
    "DEPT007": ["POS020"],  # Marketing
}

# Manager for each department
dept_to_manager = {
    "DEPT009": "EMP006",
    "DEPT010": "EMP006",
    "DEPT011": "EMP006",
    "DEPT012": "EMP012",
    "DEPT003": "EMP007",
    "DEPT004": "EMP008",
    "DEPT005": "EMP009",
    "DEPT006": "EMP010",
    "DEPT007": "EMP011",
}

# Distribute ICs across departments
ic_emp_ids = [f"EMP{i:03d}" for i in range(13, NUM_EMPLOYEES + 1)]
dept_keys = list(dept_position_map.keys())

for idx, emp_id in enumerate(ic_emp_ids):
    dept = dept_keys[idx % len(dept_keys)]
    emp_dept_map[emp_id] = dept
    pos = random.choice(dept_position_map[dept])
    emp_position_map[emp_id] = pos
    emp_manager_map[emp_id] = dept_to_manager[dept]

# Now create employee records
for i in range(1, NUM_EMPLOYEES + 1):
    emp_ref = f"EMP{i:03d}"
    uprof_ref = f"UPROF{i:03d}"
    
    # Worker type
    if i <= 60:
        wtype = "full_time"
    elif i <= 65:
        wtype = "intern"
    elif i <= 68:
        wtype = "campus_recruit"
    elif i <= 70:
        wtype = "campus_intern"
    else:
        wtype = "contractor"
    
    hire_date = random_datetime(datetime(2019, 1, 1), datetime(2024, 12, 1))
    
    # Employment status：明确指定几个员工状态，避免纯随机跑空
    TERMINATED_IDS = {70, 71, 72}   # 确保至少 3 个离职
    ON_LEAVE_IDS   = {68, 69}       # 确保至少 2 个请假中
    PROBATION_IDS  = {65, 66, 67}   # 确保至少 3 个试用期

    if i <= 3 or (i > 5 and i <= 12):
        estatus = "active"
    elif i in TERMINATED_IDS:
        estatus = "terminated"
    elif i in ON_LEAVE_IDS:
        estatus = "on_leave"
    elif i in PROBATION_IDS or wtype in ("intern", "campus_intern"):
        estatus = "probation"
    elif random.random() < 0.04:
        estatus = "on_leave"
    else:
        estatus = "active"
    
    term_date = None
    if estatus == "terminated":
        term_date = iso_date(hire_date + timedelta(days=random.randint(180, 1500)))
    
    pos_ref = emp_position_map.get(emp_ref, random.choice(ic_positions))
    mgr_ref = emp_manager_map.get(emp_ref, None)
    
    emp_number = f"AI-{hire_date.year}-{i:04d}"
    
    external_ids = {
        "hris_person_ref": f"HRIS-{fake.uuid4()[:8].upper()}",
    }
    if random.random() < 0.5:
        external_ids["asset_profile_ref"] = f"ASSET-{fake.uuid4()[:8].upper()}"
    
    created = iso_datetime(hire_date)
    updated = iso_datetime(random_datetime(hire_date, NOW))
    
    employees[emp_ref] = {
        "employee_ref": emp_ref,
        "user_profile_ref": uprof_ref,
        "employee_number": emp_number,
        "worker_type": wtype,
        "hire_date": iso_date(hire_date),
        "termination_date": term_date,
        "employment_status": estatus,
        "direct_manager_ref": mgr_ref,
        "position_ref": pos_ref,
        "external_ids": external_ids,
        "created_at": created,
        "updated_at": updated,
    }

result["employee"] = employees

# Get active employee refs for downstream use
active_employee_refs = [r for r, e in employees.items() if e["employment_status"] != "terminated"]

# ============================================================
# 13. role_permissions (depends on roles, permissions, granted_by_ref -> employees)
# ============================================================
role_permissions = {}
rp_counter = 0

# RBAC bindings
role_perm_bindings = {
    "ROLE001": list(permission_refs),  # sys_admin gets all
    "ROLE002": [r for r, p in permissions.items() if p["resource"] in ("employee", "department") or p["permission_code"] == "audit_log:read"],
    "ROLE003": [r for r, p in permissions.items() if p["action"] == "read" and p["resource"] in ("employee", "department", "team", "notification", "org_config")],
    "ROLE004": [r for r, p in permissions.items() if p["action"] == "read" and p["resource"] in ("employee", "team", "notification")],
    "ROLE005": [r for r, p in permissions.items() if p["resource"] in ("employee", "department", "team") and p["action"] in ("read", "update")],
    "ROLE006": [r for r, p in permissions.items() if p["resource"] in ("team",) or (p["resource"] == "employee" and p["action"] == "read")],
    "ROLE007": [r for r, p in permissions.items() if p["resource"] in ("employee",) and p["action"] in ("read", "export")],
    "ROLE008": [r for r, p in permissions.items() if p["resource"] in ("audit_log",)],
}

for role_ref, perm_list in role_perm_bindings.items():
    for perm_ref in perm_list:
        rp_counter += 1
        ref = f"RPRM{rp_counter:03d}"
        granted_by = random.choice(active_employee_refs[:5])
        granted_at = random_datetime(datetime(2021, 1, 1), datetime(2023, 1, 1))
        created = iso_datetime(granted_at)
        updated = iso_datetime(random_datetime(granted_at, NOW))
        
        expires = None
        status = "active"
        if random.random() < 0.05:
            expires = iso_datetime(random_datetime(NOW, NOW + timedelta(days=365)))
        
        role_permissions[ref] = {
            "role_permission_ref": ref,
            "role_ref": role_ref,
            "permission_ref": perm_ref,
            "granted_by_ref": granted_by,
            "granted_at": created,
            "expires_at": expires,
            "status": status,
            "created_at": created,
            "updated_at": updated,
        }
result["role_permission"] = role_permissions

# ============================================================
# 14. department_members (depends on departments, employees)
# ============================================================
department_members = {}
dm_counter = 0

# Every active employee must appear in exactly one department
for emp_ref, dept_ref in emp_dept_map.items():
    dm_counter += 1
    ref = f"DMBR{dm_counter:03d}"
    
    emp = employees.get(emp_ref)
    if emp is None:
        continue
    
    # Determine membership role
    if emp_ref == "EMP001":
        mrole = "head"  # VP is head of root
    elif emp_ref in ["EMP002", "EMP003", "EMP004", "EMP005"]:
        mrole = "deputy_head"  # Directors are deputy heads at root
    elif emp_ref in dept_manager_map.values():
        mrole = "head"
    else:
        mrole = "member"
    
    hire_date_str = emp["hire_date"]
    hire_dt = datetime.strptime(hire_date_str, "%Y-%m-%d")
    joined = iso_datetime(hire_dt + timedelta(days=random.randint(0, 3)))
    
    status = "active"
    left = None
    if emp["employment_status"] == "terminated":
        status = "removed"
        if emp["termination_date"]:
            left = emp["termination_date"] + " 18:00:00"
    
    created = joined
    updated = iso_datetime(random_datetime(hire_dt, NOW))
    
    department_members[ref] = {
        "department_member_ref": ref,
        "department_ref": dept_ref,
        "employee_ref": emp_ref,
        "membership_role": mrole,
        "is_primary": True,
        "joined_at": joined,
        "left_at": left,
        "status": status,
        "created_at": created,
        "updated_at": updated,
    }
result["department_member"] = department_members

# ============================================================
# 15. team_members (depends on teams, employees)
# ============================================================
team_members = {}
tm_counter = 0

# Ensure each employee belongs to at least one team
# Each team has 3-8 members
employee_team_assignments = {e: [] for e in employee_refs_list}
team_member_lists = {t: [] for t in team_refs}

# First, assign team owners as leads
for t_ref, t_data in teams.items():
    owner = t_data["owner_employee_ref"]
    if len(team_member_lists[t_ref]) < 8:
        team_member_lists[t_ref].append((owner, "lead"))
        employee_team_assignments[owner].append(t_ref)

# Fill teams to have 3-8 members
for t_ref in team_refs:
    current_members = [m[0] for m in team_member_lists[t_ref]]
    target_size = random.randint(3, 8)
    remaining = target_size - len(current_members)
    
    available = [e for e in active_employee_refs if e not in current_members]
    if remaining > 0 and available:
        chosen = random.sample(available, min(remaining, len(available)))
        for emp in chosen:
            role = random.choices(["tech_lead", "member", "observer"], weights=[10, 80, 10])[0]
            team_member_lists[t_ref].append((emp, role))
            employee_team_assignments[emp].append(t_ref)

# Ensure every active employee is in at least one team
for emp_ref in active_employee_refs:
    if not employee_team_assignments[emp_ref]:
        # Assign to a random team
        t_ref = random.choice(team_refs)
        team_member_lists[t_ref].append((emp_ref, "member"))
        employee_team_assignments[emp_ref].append(t_ref)

# Create team member records
for t_ref, members in team_member_lists.items():
    for emp_ref, trole in members:
        tm_counter += 1
        ref = f"TMBR{tm_counter:03d}"
        
        emp = employees.get(emp_ref)
        if emp is None:
            continue
        
        joined_dt = random_datetime(datetime(2021, 6, 1), datetime(2024, 12, 1))
        joined = iso_datetime(joined_dt)
        
        status = "active"
        left = None
        if emp["employment_status"] == "terminated":
            status = "removed"
            if emp["termination_date"]:
                left = emp["termination_date"] + " 18:00:00"
        elif random.random() < 0.05:
            status = "removed"
            left = iso_datetime(random_datetime(joined_dt, NOW))
        
        created = joined
        updated = iso_datetime(random_datetime(joined_dt, NOW))
        
        team_members[ref] = {
            "team_member_ref": ref,
            "team_ref": t_ref,
            "employee_ref": emp_ref,
            "team_role": trole,
            "joined_at": joined,
            "left_at": left,
            "status": status,
            "created_at": created,
            "updated_at": updated,
        }
result["team_member"] = team_members

# ============================================================
# 16. employee_roles (depends on employees, roles)
# ============================================================
employee_roles = {}
er_counter = 0

# Every employee gets at least one role
for emp_ref in employee_refs_list:
    emp = employees[emp_ref]
    assigned_roles = []
    
    # Default role based on worker type
    if emp["worker_type"] in ("intern", "campus_intern"):
        assigned_roles.append(("ROLE004", "global", None))  # Intern
    else:
        assigned_roles.append(("ROLE003", "global", None))  # Employee
    
    # Special roles
    if emp_ref == "EMP001":
        assigned_roles.append(("ROLE001", "global", None))  # Sys admin
    
    if emp_ref in ["EMP009"]:
        assigned_roles.append(("ROLE002", "global", None))  # HR manager
    
    if emp_ref in ["EMP010"]:
        assigned_roles.append(("ROLE007", "global", None))  # Finance admin
    
    # Department heads get dept_head role
    if emp_ref in dept_manager_map.values():
        dept_for_head = [d for d, m in dept_manager_map.items() if m == emp_ref]
        for d in dept_for_head:
            assigned_roles.append(("ROLE005", "department", d))
    
    # Team leads get team_lead role
    for t_ref, t_data in teams.items():
        if t_data["owner_employee_ref"] == emp_ref:
            assigned_roles.append(("ROLE006", "team", t_ref))
    
    # Some senior employees get auditor role
    if emp_ref in ["EMP002", "EMP003"]:
        assigned_roles.append(("ROLE008", "global", None))
    
    for role_ref, scope, scope_ref in assigned_roles:
        er_counter += 1
        ref = f"EMRL{er_counter:03d}"
        assigned_by = random.choice(active_employee_refs[:5])
        assigned_dt = random_datetime(datetime(2021, 1, 1), datetime(2024, 6, 1))
        assigned_at = iso_datetime(assigned_dt)
        
        expires = None
        status = "active"
        if emp["employment_status"] == "terminated":
            status = "revoked"
        elif random.random() < 0.03:
            expires = iso_datetime(random_datetime(NOW, NOW + timedelta(days=365)))
        
        created = assigned_at
        updated = iso_datetime(random_datetime(assigned_dt, NOW))
        
        employee_roles[ref] = {
            "employee_role_ref": ref,
            "employee_ref": emp_ref,
            "role_ref": role_ref,
            "scope": scope,
            "scope_ref": scope_ref,
            "assigned_by_ref": assigned_by,
            "assigned_at": assigned_at,
            "expires_at": expires,
            "status": status,
            "created_at": created,
            "updated_at": updated,
        }
result["employee_role"] = employee_roles

# ============================================================
# Final output
# ============================================================
print(json.dumps(result, ensure_ascii=False, indent=2))