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
# Paste the provided base data JSON here as a raw triple-quoted string
# NOTE:
# 1) Base tables are READ ONLY.
# 2) The script does NOT modify or output base tables.
# ============================================================
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    BASE_DATA_JSON = f.read()


# ============================================================
# Constants / Config
# ============================================================
NOW = datetime(2025, 6, 15, 12, 0, 0)
BASE_DATE = datetime(2020, 1, 1)

TABLE_ORDER = [
    'itsystems', 'itsystemaccounts', 'itsystemaccountpermissions', 'accessanomalies',
    'accountmigrations', 'emailaccounts', 'emaildistributionlists',
    'emaildistributionlistmembers', 'emailsecurityevents', 'coderepositories',
    'coderepositorymembers', 'codebranches', 'mergerequests',
    'mergerequestreviewers', 'mergerequestactivities', 'cicdpipelines',
    'pipelineexecutions', 'deployments', 'deployenvironments', 'itresources',
    'itresourcerequests', 'devenvironments', 'datasources', 'dataaccessgrants',
    'dataassets', 'datatransferjobs', 'networkzones', 'vpnconnections',
    'guestwificredentials', 'networkaccessrules', 'networkincidents',
    'softwarecatalogs', 'softwarelicenses', 'softwarelicenseassignments',
    'softwareinstallations', 'softwarefilings', 'printers', 'filetransfers',
    'filesecuritypolicies', 'itservicetickets', 'itserviceticketcomments',
    'itservicecontacts', 'itknowledgearticles', 'printersupplies',
    'printerincidents'
]

FK_DEPENDENCIES = {
    'itsystems': [('owner_employee_ref', 'employees'), ('admin_employee_ref', 'employees'), ('department_ref', 'departments')],
    'itsystemaccounts': [('it_system_ref', 'itsystems'), ('employee_ref', 'employees')],
    'itsystemaccountpermissions': [('it_system_account_ref', 'itsystemaccounts'), ('granted_by_ref', 'employees')],
    'accessanomalies': [('it_system_ref', 'itsystems'), ('it_system_account_ref', 'itsystemaccounts'), ('employee_ref', 'employees'), ('resolved_by_ref', 'employees')],
    'accountmigrations': [('employee_ref', 'employees'), ('source_system_ref', 'itsystems'), ('source_account_ref', 'itsystemaccounts'), ('target_system_ref', 'itsystems'), ('target_account_ref', 'itsystemaccounts'), ('requested_by_ref', 'employees'), ('executed_by_ref', 'employees')],
    'emailaccounts': [('employee_ref', 'employees')],
    'emaildistributionlists': [('owner_employee_ref', 'employees'), ('department_ref', 'departments')],
    'emaildistributionlistmembers': [('email_distribution_list_ref', 'emaildistributionlists'), ('email_account_ref', 'emailaccounts'), ('added_by_ref', 'employees')],
    'emailsecurityevents': [('email_account_ref', 'emailaccounts'), ('resolved_by_ref', 'employees')],
    'coderepositories': [('owner_employee_ref', 'employees'), ('team_ref', 'teams'), ('department_ref', 'departments')],
    'coderepositorymembers': [('code_repository_ref', 'coderepositories'), ('employee_ref', 'employees'), ('granted_by_ref', 'employees')],
    'codebranches': [('code_repository_ref', 'coderepositories'), ('created_by_ref', 'employees')],
    'mergerequests': [('code_repository_ref', 'coderepositories'), ('author_employee_ref', 'employees'), ('assignee_employee_ref', 'employees'), ('merged_by_ref', 'employees'), ('closed_by_ref', 'employees')],
    'mergerequestreviewers': [('merge_request_ref', 'mergerequests'), ('reviewer_employee_ref', 'employees'), ('assigned_by_ref', 'employees')],
    'mergerequestactivities': [('merge_request_ref', 'mergerequests'), ('actor_employee_ref', 'employees')],
    'cicdpipelines': [('code_repository_ref', 'coderepositories'), ('owner_employee_ref', 'employees')],
    'pipelineexecutions': [('ci_cd_pipeline_ref', 'cicdpipelines'), ('triggered_by_ref', 'employees')],
    'deployments': [('pipeline_execution_ref', 'pipelineexecutions'), ('deploy_environment_ref', 'deployenvironments'), ('deployed_by_ref', 'employees')],
    'deployenvironments': [('owner_employee_ref', 'employees'), ('team_ref', 'teams')],
    'itresources': [('owner_employee_ref', 'employees'), ('department_ref', 'departments')],
    'itresourcerequests': [('requester_employee_ref', 'employees'), ('approved_by_ref', 'employees'), ('fulfilled_resource_ref', 'itresources')],
    'devenvironments': [('employee_ref', 'employees')],
    'datasources': [('owner_employee_ref', 'employees'), ('department_ref', 'departments')],
    'dataaccessgrants': [('data_source_ref', 'datasources'), ('grantee_employee_ref', 'employees'), ('granted_by_ref', 'employees')],
    'dataassets': [('data_source_ref', 'datasources'), ('owner_employee_ref', 'employees'), ('steward_employee_ref', 'employees'), ('department_ref', 'departments')],
    'datatransferjobs': [('source_data_source_ref', 'datasources'), ('target_data_source_ref', 'datasources'), ('source_file_ref', 'file_attachments'), ('target_file_ref', 'file_attachments'), ('initiated_by_ref', 'employees')],
    'vpnconnections': [('employee_ref', 'employees')],
    'guestwificredentials': [('host_employee_ref', 'employees'), ('network_zone_ref', 'networkzones')],
    'networkaccessrules': [('network_zone_ref', 'networkzones'), ('granted_by_ref', 'employees')],
    'networkincidents': [('reporter_employee_ref', 'employees'), ('network_zone_ref', 'networkzones'), ('assigned_to_ref', 'employees')],
    'softwarelicenses': [('software_catalog_ref', 'softwarecatalogs'), ('managed_by_ref', 'employees')],
    'softwarelicenseassignments': [('software_license_ref', 'softwarelicenses'), ('employee_ref', 'employees'), ('assigned_by_ref', 'employees')],
    'softwareinstallations': [('software_catalog_ref', 'softwarecatalogs'), ('employee_ref', 'employees')],
    'softwarefilings': [('software_catalog_ref', 'softwarecatalogs'), ('filed_by_ref', 'employees'), ('department_ref', 'departments'), ('reviewed_by_ref', 'employees')],
    'printers': [('department_ref', 'departments'), ('managed_by_ref', 'employees')],
    'filetransfers': [('file_attachment_ref', 'file_attachments'), ('initiated_by_ref', 'employees')],
    'filesecuritypolicies': [('department_ref', 'departments')],
    'itservicetickets': [('requester_employee_ref', 'employees'), ('related_system_ref', 'itsystems'), ('related_printer_ref', 'printers'), ('related_email_account_ref', 'emailaccounts'), ('assigned_to_ref', 'employees')],
    'itserviceticketcomments': [('it_service_ticket_ref', 'itservicetickets'), ('author_employee_ref', 'employees')],
    'itknowledgearticles': [('author_employee_ref', 'employees')],
    'printersupplies': [('printer_ref', 'printers')],
    'printerincidents': [('printer_ref', 'printers'), ('reporter_employee_ref', 'employees'), ('assigned_to_ref', 'employees')],
}

DOMAIN_TABLE_KEY_MAP = {
    'itsystems': 'it_system',
    'itsystemaccounts': 'it_system_account',
    'itsystemaccountpermissions': 'it_system_account_permission',
    'accessanomalies': 'access_anomaly',
    'accountmigrations': 'account_migration',
    'emailaccounts': 'email_account',
    'emaildistributionlists': 'email_distribution_list',
    'emaildistributionlistmembers': 'email_distribution_list_member',
    'emailsecurityevents': 'email_security_event',
    'coderepositories': 'code_repository',
    'coderepositorymembers': 'code_repository_member',
    'codebranches': 'code_branch',
    'mergerequests': 'merge_request',
    'mergerequestreviewers': 'merge_request_reviewer',
    'mergerequestactivities': 'merge_request_activity',
    'cicdpipelines': 'ci_cd_pipeline',
    'pipelineexecutions': 'pipeline_execution',
    'deployments': 'deployment',
    'deployenvironments': 'deploy_environment',
    'itresources': 'it_resource',
    'itresourcerequests': 'it_resource_request',
    'devenvironments': 'dev_environment',
    'datasources': 'data_source',
    'dataaccessgrants': 'data_access_grant',
    'dataassets': 'data_asset',
    'datatransferjobs': 'data_transfer_job',
    'networkzones': 'network_zone',
    'vpnconnections': 'vpn_connection',
    'guestwificredentials': 'guest_wifi_credential',
    'networkaccessrules': 'network_access_rule',
    'networkincidents': 'network_incident',
    'softwarecatalogs': 'software_catalog',
    'softwarelicenses': 'software_license',
    'softwarelicenseassignments': 'software_license_assignment',
    'softwareinstallations': 'software_installation',
    'softwarefilings': 'software_filing',
    'printers': 'printer',
    'filetransfers': 'file_transfer',
    'filesecuritypolicies': 'file_security_policy',
    'itservicetickets': 'it_service_ticket',
    'itserviceticketcomments': 'it_service_ticket_comment',
    'itservicecontacts': 'it_service_contact',
    'itknowledgearticles': 'it_knowledge_article',
    'printersupplies': 'printer_supply',
    'printerincidents': 'printer_incident',
}

TABLE_PREFIX = {
    'itsystems': 'ITSYS',
    'itsystemaccounts': 'ITACC',
    'itsystemaccountpermissions': 'ITPRM',
    'accessanomalies': 'ANOM',
    'accountmigrations': 'MIGR',
    'emailaccounts': 'EMAC',
    'emaildistributionlists': 'EDL',
    'emaildistributionlistmembers': 'EDLM',
    'emailsecurityevents': 'ESEV',
    'coderepositories': 'REPO',
    'coderepositorymembers': 'REPM',
    'codebranches': 'BRCH',
    'mergerequests': 'MR',
    'mergerequestreviewers': 'MRRV',
    'mergerequestactivities': 'MRA',
    'cicdpipelines': 'PIPE',
    'pipelineexecutions': 'PEXE',
    'deployments': 'DEPL',
    'deployenvironments': 'DENV',
    'itresources': 'ITRS',
    'itresourcerequests': 'ITRQ',
    'devenvironments': 'DEVENV',
    'datasources': 'DSRC',
    'dataaccessgrants': 'DAGR',
    'dataassets': 'DAST',
    'datatransferjobs': 'DTJ',
    'networkzones': 'NWZ',
    'vpnconnections': 'VPN',
    'guestwificredentials': 'GWIFI',
    'networkaccessrules': 'NAR',
    'networkincidents': 'NINC',
    'softwarecatalogs': 'SWC',
    'softwarelicenses': 'SWL',
    'softwarelicenseassignments': 'SWLA',
    'softwareinstallations': 'SWI',
    'softwarefilings': 'SWF',
    'printers': 'PRN',
    'filetransfers': 'FTR',
    'filesecuritypolicies': 'FSP',
    'itservicetickets': 'TKT',
    'itserviceticketcomments': 'TKTC',
    'itservicecontacts': 'ITSC',
    'itknowledgearticles': 'ITKA',
    'printersupplies': 'PSUP',
    'printerincidents': 'PINC',
}

CNY = "CNY"

# ============================================================
# Helpers
# ============================================================
def iso_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def random_datetime(start: datetime, end: datetime) -> datetime:
    if end <= start:
        return start
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def random_after(dt: datetime, max_days: int = 180) -> datetime:
    return dt + timedelta(days=random.randint(1, max_days), seconds=random.randint(0, 86400))

def created_updated(earliest=None, latest=None):
    earliest = earliest or BASE_DATE
    latest = latest or NOW
    created = random_datetime(earliest, latest)
    updated = random_datetime(created, latest)
    return iso_datetime(created), iso_datetime(updated)

def optional_value(prob=0.7):
    return random.random() < prob

def gen_ref(table_name: str, counters: dict) -> str:
    counters[table_name] = counters.get(table_name, 0) + 1
    return f"{TABLE_PREFIX[table_name]}{counters[table_name]:03d}"

def weighted_choice(items):
    return random.choice(items)

def safe_sample(seq, k):
    seq = list(seq)
    if not seq:
        return []
    return random.sample(seq, min(k, len(seq)))

def pick_one(seq):
    seq = list(seq)
    if not seq:
        return None
    return random.choice(seq)

def chinese_sentence(min_words=8, max_words=18):
    return fake.sentence(nb_words=random.randint(min_words, max_words))

def chinese_paragraph(sentences=3):
    return "".join(fake.sentence(nb_words=random.randint(8, 16)) for _ in range(sentences))

def login_name_from_employee(emp):
    profile_ref = emp["user_profile_ref"]
    p = base["user_profile"][profile_ref]
    gn = p.get("given_name", "")
    fn = p.get("family_name", "")
    return f"{fn}{gn}".lower()

def company_mail_localpart(emp):
    profile_ref = emp["user_profile_ref"]
    p = base["user_profile"][profile_ref]
    return f"{p['family_name']}{p['given_name']}{emp['employee_ref'][-3:]}".lower()

def ensure_dependencies_exist(table_name, pools):
    for _, target in FK_DEPENDENCIES.get(table_name, []):
        if target not in pools:
            raise ValueError(f"Cannot generate {table_name}: missing dependency pool '{target}'")

# ============================================================
# Parse Base Data
# ============================================================
base = json.loads(BASE_DATA_JSON)

# Base read-only pools
employee_ids = list(base["employee"].keys())
department_ids = list(base["department"].keys())
team_ids = list(base["team"].keys())
file_attachment_ids = list(base["file_attachment"].keys())
role_ids = list(base["role"].keys())
permission_ids = list(base["permission"].keys())
audit_log_ids = list(base["audit_log"].keys())
notification_ids = list(base["notification"].keys())
position_ids = list(base["position"].keys())
user_profile_ids = list(base["user_profile"].keys())

active_employee_ids = [
    k for k, v in base["employee"].items()
    if v["employment_status"] in ("active", "probation", "on_leave")
]
manager_employee_ids = [
    k for k, v in base["employee"].items()
    if v["position_ref"] in ("POS022", "POS023", "POS024", "POS025")
]
tech_employee_ids = [
    k for k, v in base["employee"].items()
    if v["position_ref"] in ("POS001", "POS002", "POS003", "POS004", "POS005", "POS006", "POS007", "POS008", "POS014", "POS015", "POS028")
]
data_employee_ids = [
    k for k, v in base["employee"].items()
    if v["position_ref"] in ("POS013", "POS014", "POS015", "POS028")
]
hr_employee_ids = [k for k, v in base["employee"].items() if v["position_ref"] in ("POS016", "POS017")]
finance_employee_ids = [k for k, v in base["employee"].items() if v["position_ref"] in ("POS018", "POS019")]
product_employee_ids = [k for k, v in base["employee"].items() if v["position_ref"] in ("POS009", "POS010")]
design_employee_ids = [k for k, v in base["employee"].items() if v["position_ref"] in ("POS011", "POS012")]
marketing_employee_ids = [k for k, v in base["employee"].items() if v["position_ref"] == "POS020"]

# Derived generation volumes
EMP_COUNT = len(employee_ids)
MIN_PER_EMP = 2
DEFAULT_HEAVY_COUNT = max(SCALE, EMP_COUNT * MIN_PER_EMP)
DEFAULT_MEDIUM_COUNT = max(SCALE // 2, EMP_COUNT)
POLICY_MIN_COUNT = 10

# ============================================================
# Pools registry
# Keys must match FK target aliases used above
# ============================================================
pools = {
    "employees": employee_ids,
    "departments": department_ids,
    "teams": team_ids,
    "file_attachments": file_attachment_ids,
    "roles": role_ids,
    "permissions": permission_ids,
    "audit_logs": audit_log_ids,
    "notifications": notification_ids,
    "positions": position_ids,
    "user_profiles": user_profile_ids,
}

result = {}
counters = {}

# ============================================================
# 1. itsystems
# ============================================================
ensure_dependencies_exist("itsystems", pools)
it_system = {}
system_types = ["business_app", "infrastructure", "platform", "tool", "saas"]
system_statuses = ["active", "inactive", "deprecated", "maintenance"]
system_name_prefixes = [
    "统一身份认证平台", "研发效能平台", "工单服务系统", "邮件安全网关", "代码托管平台",
    "数据治理平台", "知识库系统", "VPN接入平台", "资产管理系统", "日志审计平台",
    "容器发布平台", "报表分析系统", "运维监控平台", "权限治理平台", "打印管理平台"
]
system_domains = [
    "https://sso.zhiliankj.com", "https://devops.zhiliankj.com", "https://itsm.zhiliankj.com",
    "https://mailsec.zhiliankj.com", "https://git.zhiliankj.com", "https://data.zhiliankj.com",
    "https://kb.zhiliankj.com", "https://vpn.zhiliankj.com", "https://asset.zhiliankj.com",
    "https://audit.zhiliankj.com"
]

for i in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("itsystems", counters)
    dept_ref = random.choice(department_ids)
    owner = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
    admin = pick_one(tech_employee_ids) or pick_one(active_employee_ids)
    created, updated = created_updated(datetime(2021, 1, 1), NOW)
    name = random.choice(system_name_prefixes) + str(i + 1)
    code = f"SYS-{i+1:03d}"
    status = random.choices(system_statuses, weights=[70, 10, 10, 10])[0]
    it_system[ref] = {
        "it_system_ref": ref,
        "system_name": name,
        "system_code": code,
        "system_type": random.choice(system_types),
        "system_url": random.choice(system_domains) + f"/{i+1}",
        "system_status": status,
        "owner_employee_ref": owner,
        "admin_employee_ref": admin,
        "department_ref": dept_ref,
        "description": f"{name}用于支持企业内部IT管理、协同办公与流程治理，服务于{base['department'][dept_ref]['department_name']}等组织场景。",
        "sso_enabled": random.random() < 0.8,
        "mfa_required": random.random() < 0.65,
        "created_at": created,
        "updated_at": updated,
    }
result["it_system"] = it_system
pools["itsystems"] = list(it_system.keys())

# ============================================================
# 2. itsystemaccounts
# ============================================================
ensure_dependencies_exist("itsystemaccounts", pools)
it_system_account = {}
it_account_types = ["personal", "service", "shared", "admin"]
it_account_statuses = ["active", "disabled", "locked", "deprovisioned"]
it_account_roles = ["user", "admin", "power_user", "readonly"]

for emp_id in employee_ids:
    per_emp_count = 2 + random.randint(0, 2)
    for _ in range(per_emp_count):
        ref = gen_ref("itsystemaccounts", counters)
        emp = base["employee"][emp_id]
        sys_ref = random.choice(pools["itsystems"])
        provisioned_dt = random_datetime(datetime.strptime(emp["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        pwd_changed_dt = random_datetime(provisioned_dt, NOW)
        status = random.choices(it_account_statuses, weights=[75, 10, 8, 7])[0]
        last_login_at = None
        locked_at = None
        lock_reason = None
        deprovisioned_at = None
        expires_at = None

        if status in ("active", "disabled", "locked"):
            if random.random() < 0.85:
                last_login_at = iso_datetime(random_datetime(provisioned_dt, NOW))
            if random.random() < 0.5:
                expires_at = iso_datetime(random_after(pwd_changed_dt, 180))
        if status == "locked":
            locked_at_dt = random_datetime(pwd_changed_dt, NOW)
            locked_at = iso_datetime(locked_at_dt)
            lock_reason = random.choice(["连续登录失败", "检测到异常登录行为", "管理员安全锁定"])
        if status == "deprovisioned":
            deprov_dt = random_datetime(provisioned_dt, NOW)
            deprovisioned_at = iso_datetime(deprov_dt)
            if last_login_at is not None:
                # keep logical ordering if possible
                last_login_dt = datetime.strptime(last_login_at, "%Y-%m-%d %H:%M:%S")
                if last_login_dt > deprov_dt:
                    last_login_at = iso_datetime(random_datetime(provisioned_dt, deprov_dt))

        account_type = random.choices(it_account_types, weights=[78, 6, 8, 8])[0]
        role_in_system = random.choices(it_account_roles, weights=[70, 10, 10, 10])[0]
        if account_type == "admin":
            role_in_system = random.choice(["admin", "power_user"])
        if account_type == "service":
            last_login_at = None

        username = f"{company_mail_localpart(emp)}_{random.randint(1,99)}"
        created_at = iso_datetime(provisioned_dt)
        updated_at = iso_datetime(random_datetime(provisioned_dt, NOW))

        it_system_account[ref] = {
            "it_system_account_ref": ref,
            "it_system_ref": sys_ref,
            "employee_ref": emp_id,
            "account_username": username,
            "account_type": account_type,
            "account_status": status,
            "role_in_system": role_in_system,
            "password_last_changed_at": iso_datetime(pwd_changed_dt),
            "password_expires_at": expires_at,
            "last_login_at": last_login_at,
            "mfa_enabled": random.random() < 0.7,
            "locked_at": locked_at,
            "lock_reason": lock_reason,
            "provisioned_at": created_at,
            "deprovisioned_at": deprovisioned_at,
            "created_at": created_at,
            "updated_at": updated_at,
        }
result["it_system_account"] = it_system_account
pools["itsystemaccounts"] = list(it_system_account.keys())

# ============================================================
# 3. itsystemaccountpermissions
# ============================================================
ensure_dependencies_exist("itsystemaccountpermissions", pools)
it_system_account_permission = {}
permission_levels = ["read", "write", "admin", "full"]
permission_scopes = [
    "基础功能", "报表中心", "用户管理", "权限管理", "配置中心",
    "日志查询", "审批流", "工单模块", "代码仓库", "资产台账"
]

for acc_ref, acc in it_system_account.items():
    count = random.randint(1, 3)
    for _ in range(count):
        ref = gen_ref("itsystemaccountpermissions", counters)
        granted_dt = random_datetime(datetime.strptime(acc["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(["active", "revoked", "expired"], weights=[75, 10, 15])[0]
        expires_at = None
        if status in ("active", "expired") and random.random() < 0.45:
            expires_dt = random_after(granted_dt, 365)
            expires_at = iso_datetime(expires_dt)
            if status == "expired" and expires_dt > NOW:
                expires_at = iso_datetime(random_datetime(granted_dt, NOW))
        it_system_account_permission[ref] = {
            "it_system_account_permission_ref": ref,
            "it_system_account_ref": acc_ref,
            "permission_name": random.choice(["查看", "编辑", "管理", "导出", "审批", "配置", "审计查看"]),
            "permission_level": random.choice(permission_levels),
            "scope": random.choice(permission_scopes),
            "granted_by_ref": pick_one(manager_employee_ids) or pick_one(active_employee_ids),
            "granted_at": iso_datetime(granted_dt),
            "expires_at": expires_at,
            "status": status,
            "created_at": iso_datetime(granted_dt),
            "updated_at": iso_datetime(random_datetime(granted_dt, NOW)),
        }
result["it_system_account_permission"] = it_system_account_permission
pools["itsystemaccountpermissions"] = list(it_system_account_permission.keys())

# ============================================================
# 4. accessanomalies
# ============================================================
ensure_dependencies_exist("accessanomalies", pools)
access_anomaly = {}
anomaly_types = ["login_failure", "unusual_access", "privilege_escalation", "geo_anomaly", "brute_force", "data_exfiltration"]
anomaly_severity = ["low", "medium", "high", "critical"]
anomaly_statuses = ["open", "investigating", "resolved", "dismissed"]
anomaly_ips = [f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(200)]
ua_pool = [
    "OA-API-Client/2.1.0",
    "DingTalk/7.5.0 (iOS 17.2)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14) Mobile Chrome/120.0"
]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("accessanomalies", counters)
    acc_ref = random.choice(pools["itsystemaccounts"])
    acc = it_system_account[acc_ref]
    occurred_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(anomaly_statuses, weights=[35, 25, 30, 10])[0]
    resolved_by = None
    resolved_at = None
    resolution_notes = None
    if status in ("resolved", "dismissed"):
        resolved_by = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
        resolved_dt = random_datetime(occurred_dt, NOW)
        resolved_at = iso_datetime(resolved_dt)
        resolution_notes = random.choice([
            "已确认系员工正常出差访问，风险解除。",
            "已重置账户密码并启用MFA。",
            "经排查为误报，已关闭告警。",
            "已封禁异常IP并通知系统管理员。"
        ])
    access_anomaly[ref] = {
        "access_anomaly_ref": ref,
        "it_system_ref": acc["it_system_ref"],
        "it_system_account_ref": acc_ref,
        "employee_ref": acc["employee_ref"],
        "anomaly_type": random.choice(anomaly_types),
        "severity": random.choices(anomaly_severity, weights=[25, 35, 25, 15])[0],
        "source_ip": random.choice(anomaly_ips),
        "user_agent": random.choice(ua_pool),
        "description": random.choice([
            "检测到异常登录失败次数过高，疑似暴力破解。",
            "检测到账户在非常用时段从新设备登录。",
            "检测到权限变更后存在高风险访问行为。",
            "检测到跨地域快速切换访问，疑似账号共享。"
        ]),
        "resolution_status": status,
        "resolved_by_ref": resolved_by,
        "resolved_at": resolved_at,
        "resolution_notes": resolution_notes,
        "occurred_at": iso_datetime(occurred_dt),
        "created_at": iso_datetime(random_datetime(occurred_dt, NOW)),
        "updated_at": iso_datetime(random_datetime(occurred_dt, NOW)),
    }
result["access_anomaly"] = access_anomaly
pools["accessanomalies"] = list(access_anomaly.keys())

# ============================================================
# 5. accountmigrations
# ============================================================
ensure_dependencies_exist("accountmigrations", pools)
account_migration = {}
migration_types = ["transfer", "clone", "merge", "archive"]
migration_statuses = ["pending", "in_progress", "completed", "failed", "cancelled"]

for _ in range(max(EMP_COUNT, SCALE // 2)):
    ref = gen_ref("accountmigrations", counters)
    src_acc_ref = random.choice(pools["itsystemaccounts"])
    tgt_acc_ref = random.choice(pools["itsystemaccounts"])
    src_acc = it_system_account[src_acc_ref]
    tgt_acc = it_system_account[tgt_acc_ref]
    emp_ref = src_acc["employee_ref"]
    req_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(migration_statuses, weights=[20, 20, 35, 15, 10])[0]
    executed_by = None
    completed_at = None
    target_account_ref = None if status in ("pending", "cancelled") and random.random() < 0.5 else tgt_acc_ref
    if status in ("in_progress", "completed", "failed"):
        executed_by = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
    if status == "completed":
        completed_at = iso_datetime(random_datetime(req_dt, NOW))
    account_migration[ref] = {
        "account_migration_ref": ref,
        "employee_ref": emp_ref,
        "source_system_ref": src_acc["it_system_ref"],
        "source_account_ref": src_acc_ref,
        "target_system_ref": tgt_acc["it_system_ref"],
        "target_account_ref": target_account_ref,
        "migration_type": random.choice(migration_types),
        "migration_status": status,
        "data_scope": random.choice(["账户权限与角色", "历史配置与收藏", "账号归档信息", "访问策略与审计映射"]),
        "requested_by_ref": emp_ref,
        "executed_by_ref": executed_by,
        "requested_at": iso_datetime(req_dt),
        "completed_at": completed_at,
        "notes": random.choice([
            "因系统整合需要进行账号迁移。",
            "因组织调整需要将原账号权限同步到新平台。",
            "为统一身份认证策略，执行账户合并处理。",
            "历史系统下线，需完成账号归档。"
        ]),
        "created_at": iso_datetime(req_dt),
        "updated_at": iso_datetime(random_datetime(req_dt, NOW)),
    }
result["account_migration"] = account_migration
pools["accountmigrations"] = list(account_migration.keys())

# ============================================================
# 6. emailaccounts
# ============================================================
ensure_dependencies_exist("emailaccounts", pools)
email_account = {}
email_types = ["primary", "alias", "shared", "service"]
providers = ["exchange", "gmail", "o365", "other"]
email_statuses = ["active", "suspended", "deactivated", "archived"]
security_levels = ["standard", "enhanced", "high"]
spam_levels = ["low", "medium", "high", "custom"]

for emp_id in employee_ids:
    cnt = 2
    # primary + alias/shared
    for idx in range(cnt):
        ref = gen_ref("emailaccounts", counters)
        localpart = company_mail_localpart(base["employee"][emp_id])
        email_type = "primary" if idx == 0 else random.choice(["alias", "shared", "service"])
        email_addr = f"{localpart}@zhiliankj.com" if idx == 0 else f"{localpart}.{idx+1}@zhiliankj.com"
        created_dt = random_datetime(datetime.strptime(base["employee"][emp_id]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        quota = random.choice([5, 10, 20, 50]) * 1024 * 1024 * 1024
        used = random.randint(int(quota * 0.05), int(quota * 0.95))
        status = random.choices(email_statuses, weights=[75, 8, 7, 10])[0]
        last_login = None
        if email_type in ("primary", "alias") and status in ("active", "suspended") and random.random() < 0.9:
            last_login = iso_datetime(random_datetime(created_dt, NOW))
        auto_reply_enabled = random.random() < 0.15
        auto_reply_message = "您好，我目前暂时无法及时回复邮件，收到后会尽快处理。" if auto_reply_enabled else None
        forwarding_address = None
        if random.random() < 0.15:
            forwarding_address = f"{localpart}@mail.zhiliankj.cn"

        email_account[ref] = {
            "email_account_ref": ref,
            "employee_ref": emp_id,
            "email_address": email_addr,
            "email_type": email_type,
            "mailbox_provider": random.choice(providers),
            "account_status": status,
            "quota_bytes": quota,
            "used_bytes": used,
            "forwarding_address": forwarding_address,
            "auto_reply_enabled": auto_reply_enabled,
            "auto_reply_message": auto_reply_message,
            "last_login_at": last_login,
            "security_level": random.choices(security_levels, weights=[45, 35, 20])[0],
            "spam_filter_level": random.choices(spam_levels, weights=[10, 50, 30, 10])[0],
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }
result["email_account"] = email_account
pools["emailaccounts"] = list(email_account.keys())

# ============================================================
# 7. emaildistributionlists
# ============================================================
ensure_dependencies_exist("emaildistributionlists", pools)
email_distribution_list = {}
dl_types = ["department", "team", "project", "custom", "all_company"]
dl_statuses = ["active", "archived", "dissolved"]

# department lists
for dept_id in department_ids:
    ref = gen_ref("emaildistributionlists", counters)
    dept = base["department"][dept_id]
    created, updated = created_updated(datetime(2022, 1, 1), NOW)
    email_distribution_list[ref] = {
        "email_distribution_list_ref": ref,
        "list_address": f"{dept['department_code'].lower()}@groups.zhiliankj.com",
        "list_name": f"{dept['department_name']}邮件组",
        "list_type": "department",
        "owner_employee_ref": pick_one(manager_employee_ids) or pick_one(active_employee_ids),
        "department_ref": dept_id,
        "member_count": random.randint(5, 30),
        "status": random.choices(dl_statuses, weights=[80, 15, 5])[0],
        "description": f"用于{dept['department_name']}内部通知、制度发布和日常协作沟通。",
        "created_at": created,
        "updated_at": updated,
    }

# some team/custom/project lists
for i in range(max(10, SCALE // 10)):
    ref = gen_ref("emaildistributionlists", counters)
    t = random.choice(dl_types)
    owner = pick_one(active_employee_ids)
    dept_ref = random.choice(department_ids) if t == "department" else (random.choice(department_ids) if random.random() < 0.3 else None)
    created, updated = created_updated(datetime(2022, 1, 1), NOW)
    slug = f"group{i+1}"
    email_distribution_list[ref] = {
        "email_distribution_list_ref": ref,
        "list_address": f"{slug}@groups.zhiliankj.com",
        "list_name": random.choice(["项目沟通组", "专项推进组", "全员通知组", "周报订阅组", "系统运维组"]) + str(i+1),
        "list_type": t,
        "owner_employee_ref": owner,
        "department_ref": dept_ref,
        "member_count": random.randint(3, 50),
        "status": random.choices(dl_statuses, weights=[75, 15, 10])[0],
        "description": "用于特定主题、项目或组织场景下的邮件群发和协作沟通。",
        "created_at": created,
        "updated_at": updated,
    }
result["email_distribution_list"] = email_distribution_list
pools["emaildistributionlists"] = list(email_distribution_list.keys())

# ============================================================
# 8. emaildistributionlistmembers
# ============================================================
ensure_dependencies_exist("emaildistributionlistmembers", pools)
email_distribution_list_member = {}
dl_member_roles = ["member", "moderator", "owner"]
dl_member_statuses = ["active", "removed"]

email_accounts_by_employee = {}
for k, v in email_account.items():
    email_accounts_by_employee.setdefault(v["employee_ref"], []).append(k)

for dl_ref, dl in email_distribution_list.items():
    member_size = random.randint(3, 12)
    chosen_email_accounts = safe_sample(pools["emailaccounts"], member_size)
    for idx, ea_ref in enumerate(chosen_email_accounts):
        ref = gen_ref("emaildistributionlistmembers", counters)
        added_dt = random_datetime(datetime.strptime(dl["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(dl_member_statuses, weights=[85, 15])[0]
        removed_at = None
        role = "owner" if idx == 0 else random.choices(dl_member_roles, weights=[80, 10, 10])[0]
        if status == "removed":
            removed_at = iso_datetime(random_datetime(added_dt, NOW))
        email_distribution_list_member[ref] = {
            "email_distribution_list_member_ref": ref,
            "email_distribution_list_ref": dl_ref,
            "email_account_ref": ea_ref,
            "role": role,
            "status": status,
            "added_by_ref": dl["owner_employee_ref"],
            "added_at": iso_datetime(added_dt),
            "removed_at": removed_at,
            "created_at": iso_datetime(added_dt),
            "updated_at": iso_datetime(random_datetime(added_dt, NOW)),
        }
result["email_distribution_list_member"] = email_distribution_list_member
pools["emaildistributionlistmembers"] = list(email_distribution_list_member.keys())

# ============================================================
# 9. emailsecurityevents
# ============================================================
ensure_dependencies_exist("emailsecurityevents", pools)
email_security_event = {}
event_types = ["phishing_detected", "spam_detected", "malware_detected", "unauthorized_forwarding", "policy_violation", "suspicious_attachment"]
event_severity = ["low", "medium", "high", "critical"]
actions_taken = ["quarantined", "blocked", "flagged", "deleted", "allowed"]
event_statuses = ["open", "investigating", "resolved", "dismissed"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("emailsecurityevents", counters)
    ea_ref = random.choice(pools["emailaccounts"])
    occurred_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(event_statuses, weights=[35, 25, 30, 10])[0]
    resolved_by = None
    resolved_at = None
    if status in ("resolved", "dismissed"):
        resolved_by = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
        resolved_at = iso_datetime(random_datetime(occurred_dt, NOW))
    email_security_event[ref] = {
        "email_security_event_ref": ref,
        "email_account_ref": ea_ref,
        "event_type": random.choice(event_types),
        "severity": random.choices(event_severity, weights=[25, 35, 25, 15])[0],
        "source_address": fake.email(),
        "subject": random.choice(["发票确认通知", "账户安全预警", "合同资料下载", "紧急付款申请", "共享文档访问邀请"]),
        "description": random.choice([
            "邮件内容命中钓鱼特征规则，疑似仿冒内部通知。",
            "检测到可疑附件行为，已进入沙箱分析。",
            "检测到异常自动转发配置，可能存在数据外发风险。",
            "发件域名信誉较低，触发高风险策略。"
        ]),
        "action_taken": random.choice(actions_taken),
        "status": status,
        "resolved_by_ref": resolved_by,
        "resolved_at": resolved_at,
        "occurred_at": iso_datetime(occurred_dt),
        "created_at": iso_datetime(random_datetime(occurred_dt, NOW)),
        "updated_at": iso_datetime(random_datetime(occurred_dt, NOW)),
    }
result["email_security_event"] = email_security_event
pools["emailsecurityevents"] = list(email_security_event.keys())

# ============================================================
# 10. coderepositories
# ============================================================
ensure_dependencies_exist("coderepositories", pools)
code_repository = {}
platforms = ["gitlab", "github", "bitbucket", "gitee"]
visibilities = ["public", "internal", "private"]
repo_statuses = ["active", "archived", "deleted"]
langs = ["Python", "Java", "Go", "TypeScript", "JavaScript", "Shell", "SQL", "Rust"]

repo_names = [
    "oa-core", "itsm-service", "email-gateway", "audit-center", "asset-platform",
    "devops-agent", "data-governance", "auth-center", "print-manager", "vpn-portal",
    "kb-service", "ops-monitor", "infra-automation", "resource-center", "ticket-engine"
]

for i in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("coderepositories", counters)
    owner = pick_one(tech_employee_ids) or pick_one(active_employee_ids)
    team_ref = random.choice(team_ids) if random.random() < 0.6 else None
    dept_ref = random.choice(department_ids) if random.random() < 0.6 else None
    created, updated = created_updated(datetime(2021, 1, 1), NOW)
    slug = f"{random.choice(repo_names)}-{i+1}"
    code_repository[ref] = {
        "code_repository_ref": ref,
        "repository_name": slug,
        "repository_slug": slug,
        "repository_url": f"https://git.zhiliankj.com/{slug}",
        "platform": random.choice(platforms),
        "visibility": random.choices(visibilities, weights=[10, 35, 55])[0],
        "default_branch": random.choice(["main", "master", "develop"]),
        "owner_employee_ref": owner,
        "team_ref": team_ref,
        "department_ref": dept_ref,
        "language_primary": random.choice(langs),
        "description": "用于承载企业IT平台、内部工具、自动化脚本或数据服务的源代码与协作开发流程。",
        "repository_status": random.choices(repo_statuses, weights=[80, 15, 5])[0],
        "created_at": created,
        "updated_at": updated,
    }
result["code_repository"] = code_repository
pools["coderepositories"] = list(code_repository.keys())

# ============================================================
# 11. coderepositorymembers
# ============================================================
ensure_dependencies_exist("coderepositorymembers", pools)
code_repository_member = {}
access_levels = ["guest", "reporter", "developer", "maintainer", "owner"]
member_statuses = ["active", "revoked"]

for repo_ref, repo in code_repository.items():
    member_count = random.randint(3, 10)
    members = safe_sample(active_employee_ids, member_count)
    if repo["owner_employee_ref"] not in members:
        members = [repo["owner_employee_ref"]] + members[:-1] if members else [repo["owner_employee_ref"]]
    for emp_id in members:
        ref = gen_ref("coderepositorymembers", counters)
        granted_dt = random_datetime(datetime.strptime(repo["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(member_statuses, weights=[85, 15])[0]
        revoked_at = None
        level = "owner" if emp_id == repo["owner_employee_ref"] else random.choices(access_levels, weights=[10, 15, 45, 20, 10])[0]
        if status == "revoked":
            revoked_at = iso_datetime(random_datetime(granted_dt, NOW))
        code_repository_member[ref] = {
            "code_repository_member_ref": ref,
            "code_repository_ref": repo_ref,
            "employee_ref": emp_id,
            "access_level": level,
            "granted_by_ref": repo["owner_employee_ref"],
            "granted_at": iso_datetime(granted_dt),
            "revoked_at": revoked_at,
            "status": status,
            "created_at": iso_datetime(granted_dt),
            "updated_at": iso_datetime(random_datetime(granted_dt, NOW)),
        }
result["code_repository_member"] = code_repository_member
pools["coderepositorymembers"] = list(code_repository_member.keys())

# ============================================================
# 12. codebranches
# ============================================================
ensure_dependencies_exist("codebranches", pools)
code_branch = {}
branch_types = ["feature", "bugfix", "hotfix", "release", "main", "develop"]
branch_statuses = ["active", "merged", "deleted"]

for repo_ref, repo in code_repository.items():
    base_branches = [("main", "main"), ("develop", "develop")]
    for branch_name, branch_type in base_branches:
        ref = gen_ref("codebranches", counters)
        created_dt = random_datetime(datetime.strptime(repo["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        code_branch[ref] = {
            "code_branch_ref": ref,
            "code_repository_ref": repo_ref,
            "branch_name": branch_name,
            "branch_type": branch_type,
            "source_branch": branch_name,
            "created_by_ref": repo["owner_employee_ref"],
            "is_protected": True,
            "status": "active",
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }
    extra_count = random.randint(3, 7)
    for i in range(extra_count):
        ref = gen_ref("codebranches", counters)
        bt = random.choice(["feature", "bugfix", "hotfix", "release"])
        created_dt = random_datetime(datetime.strptime(repo["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        branch_name = f"{bt}/{fake.word()}-{random.randint(100,999)}"
        code_branch[ref] = {
            "code_branch_ref": ref,
            "code_repository_ref": repo_ref,
            "branch_name": branch_name,
            "branch_type": bt,
            "source_branch": random.choice(["main", "develop"]),
            "created_by_ref": pick_one(tech_employee_ids) or repo["owner_employee_ref"],
            "is_protected": random.random() < 0.2,
            "status": random.choices(branch_statuses, weights=[60, 25, 15])[0],
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }
result["code_branch"] = code_branch
pools["codebranches"] = list(code_branch.keys())

# ============================================================
# 13. mergerequests
# ============================================================
ensure_dependencies_exist("mergerequests", pools)
merge_request = {}
mr_statuses = ["open", "merged", "closed"]
merge_status_values = ["can_be_merged", "cannot_be_merged", "checking", "unchecked"]
close_reasons = ["completed", "superseded", "abandoned", "duplicate", "other"]

repo_branches = {}
for br in code_branch.values():
    repo_branches.setdefault(br["code_repository_ref"], []).append(br)

for i in range(DEFAULT_HEAVY_COUNT):
    ref = gen_ref("mergerequests", counters)
    repo_ref = random.choice(pools["coderepositories"])
    branches = repo_branches.get(repo_ref, [])
    source_br = pick_one([b for b in branches if b["branch_type"] in ("feature", "bugfix", "hotfix", "release")]) or pick_one(branches)
    target_branch = random.choice(["develop", "main"])
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(mr_statuses, weights=[35, 35, 30])[0]
    assignee = pick_one(tech_employee_ids) if optional_value(0.7) else None
    merged_by = None
    merged_at = None
    closed_by = None
    closed_at = None
    close_reason = None
    if status == "merged":
        merged_by = pick_one(manager_employee_ids) or pick_one(tech_employee_ids)
        merged_at_dt = random_datetime(created_dt, NOW)
        merged_at = iso_datetime(merged_at_dt)
    elif status == "closed":
        closed_by = pick_one(manager_employee_ids) or pick_one(tech_employee_ids)
        closed_at_dt = random_datetime(created_dt, NOW)
        closed_at = iso_datetime(closed_at_dt)
        close_reason = random.choice(close_reasons)

    related_refs = safe_sample(pools["mergerequests"], random.randint(0, 2)) if pools.get("mergerequests") else []
    parent_ref = pick_one(pools["mergerequests"]) if pools.get("mergerequests") and random.random() < 0.15 else None
    pipeline_ref = pick_one(pools["cicdpipelines"]) if pools.get("cicdpipelines") and random.random() < 0.3 else None

    merge_request[ref] = {
        "merge_request_ref": ref,
        "code_repository_ref": repo_ref,
        "merge_request_number": i + 1,
        "title": random.choice(["修复登录异常", "优化权限校验", "新增审计导出能力", "重构邮件通知模块", "提升数据同步稳定性"]) + f" #{i+1}",
        "description": chinese_paragraph(3),
        "source_branch": source_br["branch_name"] if source_br else "feature/default",
        "target_branch": target_branch,
        "author_employee_ref": pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "assignee_employee_ref": assignee,
        "merge_request_status": status,
        "merge_status": random.choice(merge_status_values),
        "is_draft": random.random() < 0.2,
        "labels": safe_sample(["bugfix", "feature", "security", "infra", "urgent", "refactor", "data"], random.randint(1, 3)),
        "parent_merge_request_ref": parent_ref,
        "related_merge_request_refs": related_refs,
        "pipeline_ref": pipeline_ref,
        "merged_by_ref": merged_by,
        "merged_at": merged_at,
        "closed_by_ref": closed_by,
        "closed_at": closed_at,
        "close_reason": close_reason,
        "lines_added": random.randint(10, 1500),
        "lines_removed": random.randint(0, 800),
        "files_changed": random.randint(1, 35),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["merge_request"] = merge_request
pools["mergerequests"] = list(merge_request.keys())

# ============================================================
# 14. mergerequestreviewers
# ============================================================
ensure_dependencies_exist("mergerequestreviewers", pools)
merge_request_reviewer = {}
reviewer_roles = ["reviewer", "approver", "code_owner"]
review_statuses = ["pending", "approved", "changes_requested", "commented"]

for mr_ref, mr in merge_request.items():
    reviewers = safe_sample([e for e in tech_employee_ids if e != mr["author_employee_ref"]], random.randint(1, 3))
    for reviewer in reviewers:
        ref = gen_ref("mergerequestreviewers", counters)
        assigned_dt = random_datetime(datetime.strptime(mr["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choice(review_statuses)
        reviewed_at = None
        review_comment = None
        if status != "pending":
            reviewed_at = iso_datetime(random_datetime(assigned_dt, NOW))
            review_comment = random.choice([
                "代码结构清晰，可以合并。",
                "建议补充边界条件处理。",
                "请完善异常日志与单元测试。",
                "实现符合预期，但建议优化命名。"
            ])
        merge_request_reviewer[ref] = {
            "merge_request_reviewer_ref": ref,
            "merge_request_ref": mr_ref,
            "reviewer_employee_ref": reviewer,
            "reviewer_role": random.choice(reviewer_roles),
            "review_status": status,
            "review_comment": review_comment,
            "assigned_by_ref": mr["author_employee_ref"],
            "assigned_at": iso_datetime(assigned_dt),
            "reviewed_at": reviewed_at,
            "created_at": iso_datetime(assigned_dt),
            "updated_at": iso_datetime(random_datetime(assigned_dt, NOW)),
        }
result["merge_request_reviewer"] = merge_request_reviewer
pools["mergerequestreviewers"] = list(merge_request_reviewer.keys())

# ============================================================
# 15. mergerequestactivities
# ============================================================
ensure_dependencies_exist("mergerequestactivities", pools)
merge_request_activity = {}
activity_types = ["created", "commented", "approved", "changes_requested", "merged", "closed", "reopened", "assigned", "label_changed", "status_changed"]

for mr_ref, mr in merge_request.items():
    act_count = random.randint(2, 6)
    base_dt = datetime.strptime(mr["created_at"], "%Y-%m-%d %H:%M:%S")
    for idx in range(act_count):
        ref = gen_ref("mergerequestactivities", counters)
        occurred_dt = random_datetime(base_dt, NOW)
        atype = "created" if idx == 0 else random.choice(activity_types)
        actor = mr["author_employee_ref"] if atype == "created" else pick_one(active_employee_ids)
        changes = None
        if atype in ("label_changed", "status_changed", "assigned"):
            changes = {
                "before": random.choice(["旧值", "未设置", "pending"]),
                "after": random.choice(["新值", "assigned", "approved", "security"])
            }
        merge_request_activity[ref] = {
            "merge_request_activity_ref": ref,
            "merge_request_ref": mr_ref,
            "actor_employee_ref": actor,
            "activity_type": atype,
            "description": random.choice([
                "创建了合并请求。",
                "补充了代码评审意见。",
                "更新了标签与状态。",
                "完成了合并操作。",
                "重新指派了负责人。"
            ]),
            "changes": changes,
            "occurred_at": iso_datetime(occurred_dt),
            "created_at": iso_datetime(occurred_dt),
        }
result["merge_request_activity"] = merge_request_activity
pools["mergerequestactivities"] = list(merge_request_activity.keys())

# ============================================================
# 16. cicdpipelines
# ============================================================
ensure_dependencies_exist("cicdpipelines", pools)
ci_cd_pipeline = {}
pipeline_types = ["ci", "cd", "ci_cd"]
trigger_types = ["push", "merge_request", "schedule", "manual", "tag", "api"]
pipeline_statuses = ["active", "disabled", "archived"]

for repo_ref, repo in code_repository.items():
    cnt = random.randint(1, 2)
    for i in range(cnt):
        ref = gen_ref("cicdpipelines", counters)
        created, updated = created_updated(datetime.strptime(repo["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        ci_cd_pipeline[ref] = {
            "ci_cd_pipeline_ref": ref,
            "pipeline_name": f"{repo['repository_name']}-pipeline-{i+1}",
            "code_repository_ref": repo_ref,
            "pipeline_type": random.choice(pipeline_types),
            "config_file_path": random.choice([".gitlab-ci.yml", ".github/workflows/build.yml", "pipeline.yaml"]),
            "trigger_type": random.choice(trigger_types),
            "owner_employee_ref": repo["owner_employee_ref"],
            "status": random.choices(pipeline_statuses, weights=[80, 10, 10])[0],
            "description": "用于代码构建、测试、发布及部署流程自动化编排。",
            "created_at": created,
            "updated_at": updated,
        }
result["ci_cd_pipeline"] = ci_cd_pipeline
pools["cicdpipelines"] = list(ci_cd_pipeline.keys())

# ============================================================
# 17. pipelineexecutions
# ============================================================
ensure_dependencies_exist("pipelineexecutions", pools)
pipeline_execution = {}
execution_statuses = ["pending", "running", "success", "failed", "cancelled", "skipped"]

for pipe_ref, pipe in ci_cd_pipeline.items():
    cnt = random.randint(2, 5)
    for num in range(1, cnt + 1):
        ref = gen_ref("pipelineexecutions", counters)
        started_dt = random_datetime(datetime.strptime(pipe["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(execution_statuses, weights=[5, 10, 55, 15, 8, 7])[0]
        finished_at = None
        duration = None
        err = None
        if status not in ("pending", "running"):
            fin_dt = random_after(started_dt, 2)
            if fin_dt > NOW:
                fin_dt = NOW
            finished_at = iso_datetime(fin_dt)
            duration = max(1, int((fin_dt - started_dt).total_seconds()))
        if status == "failed":
            err = random.choice(["单元测试未通过", "镜像构建失败", "制品上传超时", "部署脚本执行异常"])
        artifact_refs = safe_sample(file_attachment_ids, random.randint(0, 3))
        pipeline_execution[ref] = {
            "pipeline_execution_ref": ref,
            "ci_cd_pipeline_ref": pipe_ref,
            "execution_number": num,
            "trigger_type": random.choice(trigger_types),
            "trigger_ref": f"TRG-{fake.uuid4()[:8]}",
            "branch": random.choice(["main", "develop", "release", "feature/demo"]),
            "commit_sha": fake.sha1()[:40],
            "triggered_by_ref": pick_one(tech_employee_ids) or pipe["owner_employee_ref"],
            "execution_status": status,
            "started_at": iso_datetime(started_dt),
            "finished_at": finished_at,
            "duration_seconds": duration,
            "artifact_file_refs": artifact_refs,
            "log_uri": f"oss://oa-files/pipeline-logs/{ref}.log",
            "error_message": err,
            "created_at": iso_datetime(started_dt),
            "updated_at": iso_datetime(random_datetime(started_dt, NOW)),
        }
result["pipeline_execution"] = pipeline_execution
pools["pipelineexecutions"] = list(pipeline_execution.keys())

# ============================================================
# 18. deployments
# ============================================================
deployment = {}
deployment_statuses = ["pending", "in_progress", "success", "failed", "rolled_back", "cancelled"]
strategies = ["rolling", "blue_green", "canary", "recreate", "manual"]

# 提前生成 deploy_environment，解决 deployments 依赖 deployenvironments 的顺序问题
pre_deploy_environment_records = {}
pre_deploy_environment_ids = []

# prebuild environments now, store, and officially publish them at step 19
env_types = ["development", "staging", "production", "testing", "demo"]
env_statuses = ["active", "inactive", "maintenance", "decommissioned"]
for i in range(max(12, SCALE // 8)):
    env_ref = f"{TABLE_PREFIX['deployenvironments']}{i+1:03d}"
    if env_ref not in pre_deploy_environment_records:
        owner = pick_one(tech_employee_ids) or pick_one(active_employee_ids)
        team_ref = random.choice(team_ids) if random.random() < 0.7 else None
        created, updated = created_updated(datetime(2021, 1, 1), NOW)
        pre_deploy_environment_records[env_ref] = {
            "deploy_environment_ref": env_ref,
            "environment_name": random.choice(["开发环境", "测试环境", "预发环境", "生产环境", "演示环境"]) + str(i+1),
            "environment_code": f"ENV-{i+1:03d}",
            "environment_type": random.choice(env_types),
            "environment_url": f"https://env{i+1}.zhiliankj.com",
            "owner_employee_ref": owner,
            "team_ref": team_ref,
            "status": random.choices(env_statuses, weights=[65, 10, 20, 5])[0],
            "description": "用于应用构建验证、联调测试或生产发布的运行环境。",
            "config_params": {
                "region": random.choice(["cn-east-1", "cn-north-1", "ap-southeast-1"]),
                "namespace": f"ns-{i+1}",
                "replicas": random.randint(1, 8)
            },
            "created_at": created,
            "updated_at": updated,
        }
        pre_deploy_environment_ids.append(env_ref)

# 提前写入 pool，ensure_dependencies_exist 检查在此之后
pools["deployenvironments"] = pre_deploy_environment_ids
ensure_dependencies_exist("deployments", pools)

for _ in range(max(EMP_COUNT, SCALE // 2)):
    ref = gen_ref("deployments", counters)
    pexec_ref = random.choice(pools["pipelineexecutions"])
    started_dt = random_datetime(datetime.strptime(pipeline_execution[pexec_ref]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
    status = random.choices(deployment_statuses, weights=[8, 12, 45, 15, 10, 10])[0]
    finished_at = None
    rollback_ref = None
    if status not in ("pending", "in_progress"):
        finished_at = iso_datetime(random_after(started_dt, 3 if status == "success" else 1))
        if datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S") > NOW:
            finished_at = iso_datetime(NOW)
    if status == "rolled_back" and result.get("deployment"):
        rollback_ref = pick_one(list(result["deployment"].keys()))
    deployment[ref] = {
        "deployment_ref": ref,
        "pipeline_execution_ref": pexec_ref,
        "deploy_environment_ref": random.choice(pre_deploy_environment_ids),
        "version_tag": f"v{random.randint(1,5)}.{random.randint(0,20)}.{random.randint(0,50)}",
        "commit_sha": fake.sha1()[:40],
        "deployed_by_ref": pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "deployment_status": status,
        "deployment_strategy": random.choice(strategies),
        "rollback_ref": rollback_ref,
        "started_at": iso_datetime(started_dt),
        "finished_at": finished_at,
        "notes": random.choice([
            "常规版本发布。",
            "修复线上高优先级问题后紧急发布。",
            "按发布窗口执行灰度投产。",
            "因依赖变更进行环境重建部署。"
        ]),
        "created_at": iso_datetime(started_dt),
        "updated_at": iso_datetime(random_datetime(started_dt, NOW)),
    }
result["deployment"] = deployment
pools["deployments"] = list(deployment.keys())

# ============================================================
# 19. deployenvironments
# ============================================================
deploy_environment = pre_deploy_environment_records
result["deploy_environment"] = deploy_environment
pools["deployenvironments"] = list(deploy_environment.keys())

# ============================================================
# 20. itresources
# ============================================================
ensure_dependencies_exist("itresources", pools)
it_resource = {}
resource_types = ["server", "vm", "container", "storage", "database", "load_balancer", "gpu", "other"]
resource_statuses = ["available", "in_use", "maintenance", "decommissioned", "reserved"]
alloc_types = ["employee", "team", "department", "project"]

for i in range(DEFAULT_HEAVY_COUNT):
    ref = gen_ref("itresources", counters)
    rtype = random.choice(resource_types)
    status = random.choices(resource_statuses, weights=[20, 45, 15, 5, 15])[0]
    allocated_to_ref = None
    allocated_to_type = None
    if status in ("in_use", "reserved") and random.random() < 0.8:
        allocated_to_type = random.choice(["employee", "team", "department"])
        if allocated_to_type == "employee":
            allocated_to_ref = random.choice(active_employee_ids)
        elif allocated_to_type == "team":
            allocated_to_ref = random.choice(team_ids)
        else:
            allocated_to_ref = random.choice(department_ids)
    created, updated = created_updated(datetime(2021, 1, 1), NOW)
    spec = {
        "cpu": random.choice(["4C", "8C", "16C", "32C"]),
        "memory_gb": random.choice([8, 16, 32, 64, 128]),
        "storage_gb": random.choice([100, 200, 500, 1000, 2000]),
        "os": random.choice(["Linux", "Windows Server", "Ubuntu", "CentOS", "Debian"])
    }
    if rtype == "gpu":
        spec["gpu_model"] = random.choice(["T4", "A10", "V100", "A100"])
    it_resource[ref] = {
        "it_resource_ref": ref,
        "resource_name": f"{random.choice(['计算节点', '数据库实例', '应用容器', '共享存储', '网关节点'])}{i+1}",
        "resource_type": rtype,
        "resource_identifier": f"RID-{fake.uuid4()[:12].upper()}",
        "specification": spec,
        "location": random.choice(["上海数据中心A区", "北京机房B区", "杭州云资源池", "深圳边缘节点"]),
        "owner_employee_ref": pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "department_ref": random.choice(department_ids) if random.random() < 0.7 else None,
        "resource_status": status,
        "allocated_to_ref": allocated_to_ref,
        "allocated_to_type": allocated_to_type,
        "description": "用于承载企业IT应用、数据服务、容器运行时或共享基础设施能力的资源对象。",
        "created_at": created,
        "updated_at": updated,
    }
result["it_resource"] = it_resource
pools["itresources"] = list(it_resource.keys())

# ============================================================
# 21. itresourcerequests
# ============================================================
ensure_dependencies_exist("itresourcerequests", pools)
it_resource_request = {}
req_categories = ["new_allocation", "upgrade", "replacement", "decommission", "temporary"]
urgencies = ["low", "normal", "high", "critical"]
req_statuses = ["pending", "approved", "rejected", "fulfilled", "cancelled"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("itresourcerequests", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(req_statuses, weights=[30, 20, 15, 25, 10])[0]
    approved_by = None
    approved_at = None
    fulfilled_resource_ref = None
    fulfilled_at = None
    rejected_reason = None
    expires_at = None
    if status in ("approved", "fulfilled"):
        approved_by = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
        appr_dt = random_datetime(created_dt, NOW)
        approved_at = iso_datetime(appr_dt)
        if status == "fulfilled":
            fulfilled_resource_ref = random.choice(pools["itresources"])
            fulf_dt = random_datetime(appr_dt, NOW)
            fulfilled_at = iso_datetime(fulf_dt)
    elif status == "rejected":
        rejected_reason = random.choice(["预算不足", "当前资源池容量不足", "业务理由不充分", "已有等效资源可复用"])
    if random.random() < 0.35:
        expires_at = iso_datetime(random_after(created_dt, 60))
    it_resource_request[ref] = {
        "it_resource_request_ref": ref,
        "requester_employee_ref": random.choice(employee_ids),
        "resource_type": random.choice(resource_types),
        "request_category": random.choice(req_categories),
        "title": random.choice(["申请新增计算资源", "申请扩容数据库", "申请临时测试环境", "申请替换老旧设备"]),
        "description": chinese_paragraph(2),
        "specifications": {
            "cpu": random.choice(["4C", "8C", "16C"]),
            "memory_gb": random.choice([8, 16, 32, 64]),
            "storage_gb": random.choice([100, 200, 500, 1000])
        },
        "business_justification": random.choice([
            "支持新项目上线与压测需求。",
            "现有资源已接近瓶颈，需要扩容保障稳定性。",
            "为满足安全整改要求，需要替换旧资源。",
            "临时活动期间需短期增加算力。"
        ]),
        "urgency": random.choices(urgencies, weights=[15, 45, 25, 15])[0],
        "request_status": status,
        "approved_by_ref": approved_by,
        "approved_at": approved_at,
        "fulfilled_resource_ref": fulfilled_resource_ref,
        "fulfilled_at": fulfilled_at,
        "rejected_reason": rejected_reason,
        "expires_at": expires_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["it_resource_request"] = it_resource_request
pools["itresourcerequests"] = list(it_resource_request.keys())

# ============================================================
# 22. devenvironments
# ============================================================
ensure_dependencies_exist("devenvironments", pools)
dev_environment = {}
dev_types = ["local", "remote", "cloud", "container"]
os_types = ["macos", "windows", "linux", "other"]
dev_statuses = ["active", "inactive", "archived"]

for emp_id in employee_ids:
    cnt = 2
    for i in range(cnt):
        ref = gen_ref("devenvironments", counters)
        created_dt = random_datetime(datetime.strptime(base["employee"][emp_id]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        dev_environment[ref] = {
            "dev_environment_ref": ref,
            "environment_name": random.choice(["个人开发环境", "远程调试环境", "容器实验环境", "云开发工作台"]) + f"-{i+1}",
            "environment_type": random.choice(dev_types),
            "employee_ref": emp_id,
            "os_type": random.choice(os_types),
            "os_version": random.choice(["macOS 14", "Windows 11", "Ubuntu 22.04", "CentOS 7", "Debian 12"]),
            "tools_installed": safe_sample(["Python", "Docker", "kubectl", "Node.js", "JDK", "VSCode", "PyCharm", "Git", "Terraform"], random.randint(3, 6)),
            "env_variables": {
                "APP_ENV": random.choice(["dev", "test", "staging"]),
                "TZ": "Asia/Shanghai",
                "LANG": "zh_CN.UTF-8"
            },
            "database_connections": safe_sample(["mysql-dev", "pgsql-test", "redis-qa", "es-staging", "mongo-dev"], random.randint(1, 3)),
            "status": random.choices(dev_statuses, weights=[75, 15, 10])[0],
            "notes": "用于日常开发、调试、联调和问题复现的个人或共享开发环境。",
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }
result["dev_environment"] = dev_environment
pools["devenvironments"] = list(dev_environment.keys())

# ============================================================
# 23. datasources
# ============================================================
ensure_dependencies_exist("datasources", pools)
data_source = {}
source_types = ["database", "api", "file", "stream", "data_warehouse", "data_lake"]
conn_types = ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "kafka", "http", "s3", "other"]
sens_levels = ["public", "internal", "confidential", "restricted"]
ds_statuses = ["active", "inactive", "deprecated", "maintenance"]

for i in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("datasources", counters)
    host = random.choice(["db-dev.zhiliankj.local", "pg-prod.zhiliankj.local", "api-data.zhiliankj.com", "s3.zhiliankj.com", "kafka.zhiliankj.local"])
    ctype = random.choice(conn_types)
    data_source[ref] = {
        "data_source_ref": ref,
        "source_name": random.choice(["员工主数据源", "工单事实库", "审计日志仓库", "行为分析流", "邮件数据接口", "资产明细库"]) + str(i+1),
        "source_type": random.choice(source_types),
        "connection_type": ctype,
        "host": host,
        "port": random.choice([80, 443, 3306, 5432, 6379, 9200, 9092]),
        "database_name": random.choice(["hr_db", "itsm_dw", "audit_log", "mail_api", "asset_db", "ods_center"]),
        "owner_employee_ref": pick_one(data_employee_ids) or pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "department_ref": random.choice(department_ids) if random.random() < 0.7 else None,
        "sensitivity_level": random.choices(sens_levels, weights=[10, 40, 35, 15])[0],
        "status": random.choices(ds_statuses, weights=[75, 10, 5, 10])[0],
        "description": "用于业务分析、数据集成、指标计算、审计取数或应用服务访问的标准化数据源。",
        "created_at": created_updated(datetime(2021, 1, 1), NOW)[0],
        "updated_at": created_updated(datetime(2021, 1, 1), NOW)[1],
    }
result["data_source"] = data_source
pools["datasources"] = list(data_source.keys())

# ============================================================
# 24. dataaccessgrants
# ============================================================
ensure_dependencies_exist("dataaccessgrants", pools)
data_access_grant = {}
grant_levels = ["read", "write", "admin", "full"]
grant_statuses = ["active", "revoked", "expired"]

for _ in range(DEFAULT_HEAVY_COUNT):
    ref = gen_ref("dataaccessgrants", counters)
    granted_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(grant_statuses, weights=[70, 15, 15])[0]
    expires_at = None
    if status in ("active", "expired") and random.random() < 0.4:
        exdt = random_after(granted_dt, 365)
        if status == "expired" and exdt > NOW:
            exdt = random_datetime(granted_dt, NOW)
        expires_at = iso_datetime(exdt)
    data_access_grant[ref] = {
        "data_access_grant_ref": ref,
        "data_source_ref": random.choice(pools["datasources"]),
        "grantee_employee_ref": random.choice(employee_ids),
        "access_level": random.choices(grant_levels, weights=[45, 25, 20, 10])[0],
        "scope": random.choice(["只读分析", "报表开发", "数据维护", "全库访问", "接口调用"]),
        "granted_by_ref": pick_one(manager_employee_ids) or pick_one(data_employee_ids) or pick_one(active_employee_ids),
        "granted_at": iso_datetime(granted_dt),
        "expires_at": expires_at,
        "status": status,
        "business_justification": random.choice([
            "支持日常经营分析与月度报表制作。",
            "支持数据治理、质量排查与问题修复。",
            "支持接口联调与系统集成测试。",
            "满足项目临时取数和验证需要。"
        ]),
        "created_at": iso_datetime(granted_dt),
        "updated_at": iso_datetime(random_datetime(granted_dt, NOW)),
    }
result["data_access_grant"] = data_access_grant
pools["dataaccessgrants"] = list(data_access_grant.keys())

# ============================================================
# 25. dataassets
# ============================================================
ensure_dependencies_exist("dataassets", pools)
data_asset = {}
asset_types = ["table", "view", "collection", "index", "topic", "bucket", "file", "api_endpoint"]
asset_sens = ["public", "internal", "confidential", "restricted"]
freqs = ["realtime", "hourly", "daily", "weekly", "monthly", "manual", "unknown"]
asset_statuses = ["active", "deprecated", "archived"]

for i in range(DEFAULT_HEAVY_COUNT):
    ref = gen_ref("dataassets", counters)
    created_dt = random_datetime(datetime(2022, 1, 1), NOW)
    last_updated = iso_datetime(random_datetime(created_dt, NOW)) if random.random() < 0.8 else None
    data_asset[ref] = {
        "data_asset_ref": ref,
        "data_source_ref": random.choice(pools["datasources"]),
        "asset_name": random.choice(["employee_profile", "ticket_fact", "access_log", "mail_event", "resource_usage", "dept_dim"]) + f"_{i+1}",
        "asset_type": random.choice(asset_types),
        "schema_name": random.choice(["public", "ods", "dwd", "mart", "audit", "system"]),
        "field_definitions": [
            {"name": "id", "type": "string", "nullable": False},
            {"name": "created_at", "type": "datetime", "nullable": False},
            {"name": "updated_at", "type": "datetime", "nullable": True},
        ],
        "owner_employee_ref": pick_one(data_employee_ids) or pick_one(active_employee_ids),
        "steward_employee_ref": pick_one(data_employee_ids) if optional_value(0.6) else None,
        "department_ref": random.choice(department_ids) if random.random() < 0.6 else None,
        "sensitivity_level": random.choices(asset_sens, weights=[10, 40, 35, 15])[0],
        "update_frequency": random.choice(freqs),
        "row_count": random.randint(100, 5_000_000) if random.random() < 0.8 else None,
        "last_updated_at": last_updated,
        "tags": safe_sample(["主数据", "审计", "邮件", "工单", "资产", "研发", "安全", "指标"], random.randint(1, 4)),
        "description": "用于承载结构化或半结构化业务数据，可被分析、服务或治理流程消费的数据资产。",
        "status": random.choices(asset_statuses, weights=[80, 10, 10])[0],
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["data_asset"] = data_asset
pools["dataassets"] = list(data_asset.keys())

# ============================================================
# 26. datatransferjobs
# ============================================================
ensure_dependencies_exist("datatransferjobs", pools)
data_transfer_job = {}
transfer_types = ["import", "export", "sync", "migration", "backup"]
formats = ["csv", "json", "parquet", "avro", "xml", "sql", "excel", "other"]
job_statuses = ["pending", "running", "completed", "failed", "cancelled"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("datatransferjobs", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(job_statuses, weights=[20, 15, 45, 10, 10])[0]
    started_at = None
    completed_at = None
    record_count = None
    file_size_bytes = None
    error_message = None
    if status in ("running", "completed", "failed", "cancelled"):
        started_dt = random_datetime(created_dt, NOW)
        started_at = iso_datetime(started_dt)
    if status in ("completed", "failed", "cancelled"):
        comp_dt = random_datetime(started_dt or created_dt, NOW)
        completed_at = iso_datetime(comp_dt)
    if status == "completed":
        record_count = random.randint(100, 5_000_000)
        file_size_bytes = random.randint(10_000, 2_000_000_000)
    if status == "failed":
        error_message = random.choice(["源端连接失败", "目标端写入超时", "数据格式校验失败", "磁盘空间不足"])
    data_transfer_job[ref] = {
        "data_transfer_job_ref": ref,
        "job_name": random.choice(["工单数据同步", "审计日志归档", "员工主数据导入", "资产台账导出", "周报快照备份"]) + str(random.randint(1, 999)),
        "transfer_type": random.choice(transfer_types),
        "source_data_source_ref": random.choice(pools["datasources"]) if optional_value(0.8) else None,
        "target_data_source_ref": random.choice(pools["datasources"]) if optional_value(0.8) else None,
        "source_file_ref": random.choice(file_attachment_ids) if optional_value(0.3) else None,
        "target_file_ref": random.choice(file_attachment_ids) if optional_value(0.3) else None,
        "data_format": random.choice(formats),
        "record_count": record_count,
        "file_size_bytes": file_size_bytes,
        "initiated_by_ref": pick_one(data_employee_ids) or pick_one(active_employee_ids),
        "job_status": status,
        "started_at": started_at,
        "completed_at": completed_at,
        "error_message": error_message,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["data_transfer_job"] = data_transfer_job
pools["datatransferjobs"] = list(data_transfer_job.keys())

# ============================================================
# 27. networkzones
# ============================================================
network_zone = {}
zone_types = ["corporate", "dmz", "guest", "production", "development", "restricted"]
zone_statuses = ["active", "inactive", "maintenance"]

for i in range(max(POLICY_MIN_COUNT, SCALE // 10)):
    ref = gen_ref("networkzones", counters)
    network_zone[ref] = {
        "network_zone_ref": ref,
        "zone_name": random.choice(["办公网区", "访客网区", "生产网区", "研发网区", "受限访问区", "DMZ区"]) + str(i+1),
        "zone_type": random.choice(zone_types),
        "cidr_range": f"10.{i%250}.{random.randint(0,254)}.0/24",
        "location": random.choice(["上海总部", "北京分部", "杭州云区", "深圳机房"]),
        "vlan_id": random.randint(100, 4094) if random.random() < 0.8 else None,
        "gateway": f"10.{i%250}.{random.randint(0,254)}.1",
        "dns_servers": [f"10.{i%250}.0.10", f"10.{i%250}.0.11"],
        "status": random.choices(zone_statuses, weights=[75, 10, 15])[0],
        "description": "用于隔离办公、生产、测试、访客或高敏感访问场景的网络区域。",
        "created_at": created_updated(datetime(2021, 1, 1), NOW)[0],
        "updated_at": created_updated(datetime(2021, 1, 1), NOW)[1],
    }
result["network_zone"] = network_zone
pools["networkzones"] = list(network_zone.keys())

# ============================================================
# 28. vpnconnections
# ============================================================
ensure_dependencies_exist("vpnconnections", pools)
vpn_connection = {}
vpn_statuses = ["connected", "disconnected", "error"]

for emp_id in employee_ids:
    cnt = 2
    for i in range(cnt):
        ref = gen_ref("vpnconnections", counters)
        created_dt = random_datetime(datetime.strptime(base["employee"][emp_id]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(vpn_statuses, weights=[30, 60, 10])[0]
        last_connected = iso_datetime(random_datetime(created_dt, NOW)) if random.random() < 0.85 else None
        last_disconnected = None
        if status != "connected" and last_connected:
            lcdt = datetime.strptime(last_connected, "%Y-%m-%d %H:%M:%S")
            last_disconnected = iso_datetime(random_datetime(lcdt, NOW))
        vpn_connection[ref] = {
            "vpn_connection_ref": ref,
            "employee_ref": emp_id,
            "vpn_profile": random.choice(["默认办公接入", "研发专线接入", "高权限堡垒接入"]),
            "assigned_ip": f"172.16.{random.randint(1,254)}.{random.randint(2,254)}",
            "connection_status": status,
            "last_connected_at": last_connected,
            "last_disconnected_at": last_disconnected,
            "created_at": iso_datetime(created_dt),
            "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
        }
result["vpn_connection"] = vpn_connection
pools["vpnconnections"] = list(vpn_connection.keys())

# ============================================================
# 29. guestwificredentials
# ============================================================
ensure_dependencies_exist("guestwificredentials", pools)
guest_wifi_credential = {}
gw_statuses = ["active", "expired", "revoked"]

for _ in range(max(POLICY_MIN_COUNT, SCALE // 8)):
    ref = gen_ref("guestwificredentials", counters)
    valid_from_dt = random_datetime(datetime(2024, 1, 1), NOW)
    valid_until_dt = random_after(valid_from_dt, 7)
    status = "active" if valid_until_dt > NOW and random.random() < 0.5 else random.choice(["expired", "revoked"])
    if status == "active" and valid_until_dt < NOW:
        valid_until_dt = random_after(NOW, 7)
    guest_wifi_credential[ref] = {
        "guest_wifi_credential_ref": ref,
        "guest_name": fake.name(),
        "guest_company": random.choice(["华曜咨询", "启辰软件", "云数科技", "安信服务", "未来网络"]),
        "guest_phone": fake.phone_number(),
        "host_employee_ref": random.choice(active_employee_ids),
        "ssid": random.choice(["ZLKJ-GUEST", "ZLKJ-VISITOR", "ZLKJ-MEETING"]),
        "access_code": fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True),
        "network_zone_ref": random.choice(pools["networkzones"]) if random.random() < 0.8 else None,
        "valid_from": iso_datetime(valid_from_dt),
        "valid_until": iso_datetime(valid_until_dt),
        "max_devices": random.randint(1, 5),
        "bandwidth_limit_mbps": random.choice([10, 20, 50, 100]) if random.random() < 0.7 else None,
        "status": status,
        "created_at": iso_datetime(valid_from_dt),
        "updated_at": iso_datetime(random_datetime(valid_from_dt, NOW)),
    }
result["guest_wifi_credential"] = guest_wifi_credential
pools["guestwificredentials"] = list(guest_wifi_credential.keys())

# ============================================================
# 30. networkaccessrules
# ============================================================
ensure_dependencies_exist("networkaccessrules", pools)
network_access_rule = {}
subject_types = ["employee", "team", "department", "role", "ip_range"]
protocols = ["tcp", "udp", "icmp", "any"]
actions = ["allow", "deny"]
rule_statuses = ["active", "disabled", "expired"]

for i in range(max(POLICY_MIN_COUNT * 2, SCALE // 5)):
    ref = gen_ref("networkaccessrules", counters)
    subject_type = random.choice(subject_types)
    if subject_type == "employee":
        subject_ref = random.choice(employee_ids)
    elif subject_type == "team":
        subject_ref = random.choice(team_ids)
    elif subject_type == "department":
        subject_ref = random.choice(department_ids)
    elif subject_type == "role":
        subject_ref = random.choice(role_ids)
    else:
        subject_ref = f"192.168.{random.randint(0,255)}.0/24"
    created_dt = random_datetime(datetime(2022, 1, 1), NOW)
    status = random.choices(rule_statuses, weights=[75, 15, 10])[0]
    expires_at = None
    if status == "expired" or random.random() < 0.2:
        exdt = random_after(created_dt, 180)
        if status == "expired" and exdt > NOW:
            exdt = random_datetime(created_dt, NOW)
        expires_at = iso_datetime(exdt)
    network_access_rule[ref] = {
        "network_access_rule_ref": ref,
        "rule_name": random.choice(["办公网访问数据库", "研发区访问缓存", "访客网限制外连", "生产区仅白名单访问", "VPN访问审计平台"]) + str(i+1),
        "subject_type": subject_type,
        "subject_ref": subject_ref,
        "network_zone_ref": random.choice(pools["networkzones"]),
        "target_resource": random.choice(["mysql-prod:3306", "redis-cache:6379", "k8s-api:6443", "vpn-gateway", "audit-web:443"]),
        "protocol": random.choice(protocols),
        "port_range": random.choice(["80", "443", "3306", "6379", "8080-8090", "any"]),
        "action": random.choices(actions, weights=[70, 30])[0],
        "priority": i + 1,
        "status": status,
        "granted_by_ref": pick_one(manager_employee_ids) or pick_one(active_employee_ids),
        "expires_at": expires_at,
        "description": "用于规范不同主体访问指定网络区域或服务资源的访问控制规则。",
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["network_access_rule"] = network_access_rule
pools["networkaccessrules"] = list(network_access_rule.keys())

# ============================================================
# 31. networkincidents
# ============================================================
ensure_dependencies_exist("networkincidents", pools)
network_incident = {}
incident_types = ["connectivity_loss", "performance_degradation", "security_breach", "dns_failure", "hardware_failure", "configuration_error"]
incident_severity = ["low", "medium", "high", "critical"]
incident_statuses = ["open", "investigating", "resolved", "closed"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("networkincidents", counters)
    occurred_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(incident_statuses, weights=[30, 25, 25, 20])[0]
    resolved_at = None
    if status in ("resolved", "closed"):
        resolved_at = iso_datetime(random_datetime(occurred_dt, NOW))
    network_incident[ref] = {
        "network_incident_ref": ref,
        "reporter_employee_ref": random.choice(employee_ids),
        "network_zone_ref": random.choice(pools["networkzones"]) if random.random() < 0.8 else None,
        "incident_type": random.choice(incident_types),
        "severity": random.choices(incident_severity, weights=[20, 35, 30, 15])[0],
        "affected_scope": random.choice(["单个办公区域", "研发团队", "跨部门访问", "总部网络", "生产集群"]),
        "description": random.choice([
            "网络延迟明显升高，影响业务访问体验。",
            "DNS解析异常导致多个系统不可访问。",
            "边界设备故障导致区域网络中断。",
            "配置变更后出现访问控制异常。"
        ]),
        "diagnosis": random.choice(["初步判断为链路抖动", "疑似交换机配置异常", "疑似DNS服务过载", None]),
        "resolution": random.choice(["已切换备份链路", "已回滚错误配置", "已更换故障硬件", None]),
        "status": status,
        "assigned_to_ref": pick_one(tech_employee_ids) if optional_value(0.7) else None,
        "resolved_at": resolved_at,
        "occurred_at": iso_datetime(occurred_dt),
        "created_at": iso_datetime(occurred_dt),
        "updated_at": iso_datetime(random_datetime(occurred_dt, NOW)),
    }
result["network_incident"] = network_incident
pools["networkincidents"] = list(network_incident.keys())

# ============================================================
# 32. softwarecatalogs
# ============================================================
software_catalog = {}
soft_categories = ["office", "development", "design", "communication", "security", "database", "monitoring", "analytics", "other"]
compliance_statuses = ["approved", "pending_review", "rejected", "conditional"]
catalog_statuses = ["active", "deprecated", "retired"]

software_seed = [
    ("Visual Studio Code", "Microsoft"),
    ("PyCharm", "JetBrains"),
    ("DataGrip", "JetBrains"),
    ("Docker Desktop", "Docker"),
    ("Google Chrome", "Google"),
    ("企业微信", "Tencent"),
    ("钉钉", "Alibaba"),
    ("Postman", "Postman"),
    ("Navicat Premium", "PremiumSoft"),
    ("Wireshark", "Wireshark Foundation"),
    ("Notion", "Notion"),
    ("Grafana", "Grafana Labs"),
    ("Prometheus", "CNCF"),
    ("Tableau", "Salesforce"),
    ("飞书", "ByteDance"),
]

for i in range(max(POLICY_MIN_COUNT * 2, SCALE // 5)):
    ref = gen_ref("softwarecatalogs", counters)
    sname, vendor = software_seed[i % len(software_seed)]
    category = random.choice(soft_categories)
    created, updated = created_updated(datetime(2021, 1, 1), NOW)
    software_catalog[ref] = {
        "software_catalog_ref": ref,
        "software_name": sname,
        "software_code": f"SW-{i+1:03d}",
        "vendor": vendor,
        "category": category,
        "current_version": f"{random.randint(1,10)}.{random.randint(0,20)}.{random.randint(0,50)}",
        "supported_os": safe_sample(["Windows", "macOS", "Linux"], random.randint(1, 3)),
        "download_uri": f"https://downloads.zhiliankj.com/software/{i+1}",
        "installation_guide_uri": f"https://kb.zhiliankj.com/software/install/{i+1}" if random.random() < 0.7 else None,
        "is_core": random.random() < 0.35,
        "requires_license": random.random() < 0.65,
        "requires_approval": random.random() < 0.55,
        "security_reviewed": random.random() < 0.8,
        "compliance_status": random.choices(compliance_statuses, weights=[65, 15, 5, 15])[0],
        "description": "纳入企业软件目录管理的标准软件，可用于办公、研发、分析、设计或运维场景。",
        "status": random.choices(catalog_statuses, weights=[80, 10, 10])[0],
        "created_at": created,
        "updated_at": updated,
    }
result["software_catalog"] = software_catalog
pools["softwarecatalogs"] = list(software_catalog.keys())

# ============================================================
# 33. softwarelicenses
# ============================================================
ensure_dependencies_exist("softwarelicenses", pools)
software_license = {}
license_types = ["per_seat", "per_device", "site", "enterprise", "open_source", "trial", "subscription"]
license_statuses = ["active", "expired", "cancelled", "pending_renewal"]

for i in range(max(POLICY_MIN_COUNT, SCALE // 8)):
    ref = gen_ref("softwarelicenses", counters)
    purchase_dt = random_datetime(datetime(2022, 1, 1), NOW)
    expiry_dt = random_after(purchase_dt, 720)
    status = random.choices(license_statuses, weights=[65, 15, 5, 15])[0]
    if status == "expired" and expiry_dt > NOW:
        expiry_dt = random_datetime(purchase_dt, NOW)
    software_license[ref] = {
        "software_license_ref": ref,
        "software_catalog_ref": random.choice(pools["softwarecatalogs"]),
        "license_key": fake.uuid4().upper(),
        "license_type": random.choice(license_types),
        "total_seats": random.randint(10, 500),
        "used_seats": random.randint(0, 300),
        "vendor_contract_ref": f"VCTR-{i+1:03d}",
        "purchase_date": iso_date(purchase_dt),
        "expiry_date": iso_date(expiry_dt),
        "cost_per_unit": round(random.uniform(99, 4999), 2),
        "currency": CNY,
        "auto_renew": random.random() < 0.5,
        "status": status,
        "managed_by_ref": pick_one(finance_employee_ids) or pick_one(manager_employee_ids) or pick_one(active_employee_ids),
        "notes": random.choice(["年度采购合同", "专项项目授权", "部门共享许可证", "统一企业订阅协议"]),
        "created_at": iso_datetime(purchase_dt),
        "updated_at": iso_datetime(random_datetime(purchase_dt, NOW)),
    }
result["software_license"] = software_license
pools["softwarelicenses"] = list(software_license.keys())

# ============================================================
# 34. softwarelicenseassignments
# ============================================================
ensure_dependencies_exist("softwarelicenseassignments", pools)
software_license_assignment = {}
sla_statuses = ["active", "revoked"]

for emp_id in employee_ids:
    cnt = 2
    for _ in range(cnt):
        ref = gen_ref("softwarelicenseassignments", counters)
        assigned_dt = random_datetime(datetime.strptime(base["employee"][emp_id]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(sla_statuses, weights=[85, 15])[0]
        revoked_at = iso_datetime(random_datetime(assigned_dt, NOW)) if status == "revoked" else None
        software_license_assignment[ref] = {
            "software_license_assignment_ref": ref,
            "software_license_ref": random.choice(pools["softwarelicenses"]),
            "employee_ref": emp_id,
            "assigned_by_ref": pick_one(manager_employee_ids) or pick_one(active_employee_ids),
            "assigned_at": iso_datetime(assigned_dt),
            "revoked_at": revoked_at,
            "status": status,
            "created_at": iso_datetime(assigned_dt),
            "updated_at": iso_datetime(random_datetime(assigned_dt, NOW)),
        }
result["software_license_assignment"] = software_license_assignment
pools["softwarelicenseassignments"] = list(software_license_assignment.keys())

# ============================================================
# 35. softwareinstallations
# ============================================================
ensure_dependencies_exist("softwareinstallations", pools)
software_installation = {}
install_statuses = ["installed", "pending", "failed", "uninstalled"]
device_prefix = ["NB", "WS", "MAC", "PC", "VM"]

for emp_id in employee_ids:
    cnt = 2 + random.randint(0, 2)
    for _ in range(cnt):
        ref = gen_ref("softwareinstallations", counters)
        installed_dt = random_datetime(datetime.strptime(base["employee"][emp_id]["created_at"], "%Y-%m-%d %H:%M:%S"), NOW)
        status = random.choices(install_statuses, weights=[70, 10, 10, 10])[0]
        uninstalled_at = None
        if status == "uninstalled":
            uninstalled_at = iso_datetime(random_datetime(installed_dt, NOW))
        sw_ref = random.choice(pools["softwarecatalogs"])
        software_installation[ref] = {
            "software_installation_ref": ref,
            "software_catalog_ref": sw_ref,
            "employee_ref": emp_id,
            "device_name": f"{random.choice(device_prefix)}-{emp_id[-3:]}-{random.randint(100,999)}",
            "installed_version": software_catalog[sw_ref]["current_version"],
            "installation_status": status,
            "installed_at": iso_datetime(installed_dt),
            "uninstalled_at": uninstalled_at,
            "created_at": iso_datetime(installed_dt),
            "updated_at": iso_datetime(random_datetime(installed_dt, NOW)),
        }
result["software_installation"] = software_installation
pools["softwareinstallations"] = list(software_installation.keys())

# ============================================================
# 36. softwarefilings
# ============================================================
ensure_dependencies_exist("softwarefilings", pools)
software_filing = {}
review_statuses = ["pending", "approved", "rejected"]
filing_statuses = ["pending", "approved", "rejected", "withdrawn"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("softwarefilings", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    sec_review = random.choices(review_statuses, weights=[35, 50, 15])[0]
    comp_review = random.choices(review_statuses, weights=[35, 50, 15])[0]
    filing_status = random.choices(filing_statuses, weights=[25, 45, 20, 10])[0]
    reviewed_by = None
    reviewed_at = None
    rejection_reason = None
    if filing_status in ("approved", "rejected"):
        reviewed_by = pick_one(manager_employee_ids) or pick_one(active_employee_ids)
        reviewed_at = iso_datetime(random_datetime(created_dt, NOW))
    if filing_status == "rejected":
        rejection_reason = random.choice(["存在合规风险", "已有替代软件", "安全评估未通过", "用途描述不充分"])
    software_filing[ref] = {
        "software_filing_ref": ref,
        "software_catalog_ref": random.choice(pools["softwarecatalogs"]) if random.random() < 0.6 else None,
        "software_name": random.choice(["截图工具Pro", "远程协作助手", "建模分析器", "流程绘图器", "终端增强工具"]),
        "vendor": random.choice(["启创软件", "云桥科技", "北辰信息", "数图软件", "智程网络"]),
        "version": f"{random.randint(1,8)}.{random.randint(0,20)}",
        "purpose": random.choice(["支持项目交付", "提升研发效率", "满足数据分析需求", "用于跨团队协作", "满足设计输出需要"]),
        "data_sensitivity": random.choice(["public", "internal", "confidential", "restricted"]),
        "filed_by_ref": random.choice(employee_ids),
        "department_ref": random.choice(department_ids),
        "security_review_status": sec_review,
        "compliance_review_status": comp_review,
        "reviewed_by_ref": reviewed_by,
        "reviewed_at": reviewed_at,
        "filing_status": filing_status,
        "rejection_reason": rejection_reason,
        "notes": "软件引入需经安全与合规双重评估，方可纳入正式使用范围。",
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["software_filing"] = software_filing
pools["softwarefilings"] = list(software_filing.keys())

# ============================================================
# 37. printers
# ============================================================
ensure_dependencies_exist("printers", pools)
printer = {}
printer_statuses = ["online", "offline", "error", "maintenance", "decommissioned"]

for i in range(max(POLICY_MIN_COUNT, SCALE // 8)):
    ref = gen_ref("printers", counters)
    printer[ref] = {
        "printer_ref": ref,
        "printer_name": f"办公打印机-{i+1}",
        "printer_model": random.choice(["HP LaserJet MFP E52645", "Canon iR-ADV 4525", "Fuji Apeos C3060", "Brother HL-L6400DW"]),
        "manufacturer": random.choice(["HP", "Canon", "Fuji", "Brother"]),
        "serial_number": f"SN-{fake.uuid4()[:12].upper()}",
        "ip_address": f"10.10.{random.randint(1,254)}.{random.randint(2,254)}",
        "location_building": random.choice(["A座", "B座", "研发楼", "运营楼"]),
        "location_floor": f"{random.randint(1,12)}F",
        "location_area": random.choice(["前台区", "开放办公区", "会议室旁", "财务办公室", "研发工位区"]),
        "capabilities": safe_sample(["print", "scan", "copy", "fax", "secure_print"], random.randint(2, 5)),
        "supports_color": random.random() < 0.5,
        "supports_duplex": random.random() < 0.9,
        "supports_scan": random.random() < 0.8,
        "driver_download_uri": f"https://downloads.zhiliankj.com/printer/{i+1}",
        "printer_status": random.choices(printer_statuses, weights=[65, 10, 10, 10, 5])[0],
        "department_ref": random.choice(department_ids) if random.random() < 0.8 else None,
        "managed_by_ref": pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "description": "用于满足部门日常打印、扫描、复印及安全输出等办公需求的共享打印设备。",
        "created_at": created_updated(datetime(2021, 1, 1), NOW)[0],
        "updated_at": created_updated(datetime(2021, 1, 1), NOW)[1],
    }
result["printer"] = printer
pools["printers"] = list(printer.keys())

# ============================================================
# 38. filetransfers
# ============================================================
ensure_dependencies_exist("filetransfers", pools)
file_transfer = {}
transfer_types2 = ["upload", "download", "share", "sync"]
transfer_statuses = ["pending", "in_progress", "completed", "failed", "expired"]

for _ in range(DEFAULT_MEDIUM_COUNT):
    ref = gen_ref("filetransfers", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(transfer_statuses, weights=[20, 15, 45, 10, 10])[0]
    expires_at = None
    if status in ("expired", "completed") and random.random() < 0.4:
        exdt = random_after(created_dt, 30)
        if status == "expired" and exdt > NOW:
            exdt = random_datetime(created_dt, NOW)
        expires_at = iso_datetime(exdt)
    recipients = safe_sample(employee_ids, random.randint(1, 3))
    file_ref = random.choice(file_attachment_ids)
    file_transfer[ref] = {
        "file_transfer_ref": ref,
        "file_attachment_ref": file_ref,
        "transfer_type": random.choice(transfer_types2),
        "source": random.choice(["本地终端", "对象存储", "共享盘", "邮件附件", "业务系统"]),
        "destination": random.choice(["对象存储", "外部协作空间", "员工邮箱", "共享目录", "归档库"]),
        "initiated_by_ref": random.choice(employee_ids),
        "recipient_employee_refs": recipients,
        "encryption_applied": random.random() < 0.65,
        "encryption_method": random.choice(["AES-256", "SM4", "TLS"]) if random.random() < 0.65 else None,
        "transfer_status": status,
        "file_size_bytes": base["file_attachment"].get(file_ref, {}).get("file_size_bytes", random.randint(10000, 100000000)),
        "expires_at": expires_at,
        "access_password_set": random.random() < 0.5,
        "download_count": random.randint(0, 20),
        "max_downloads": random.choice([1, 3, 5, 10, None]),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["file_transfer"] = file_transfer
pools["filetransfers"] = list(file_transfer.keys())

# ============================================================
# 39. filesecuritypolicies
# ============================================================
ensure_dependencies_exist("filesecuritypolicies", pools)
file_security_policy = {}
class_levels = ["public", "internal", "confidential", "restricted", "top_secret"]
share_scopes = ["public", "company", "department", "team", "individual"]
policy_statuses = ["active", "disabled", "archived"]

for i in range(max(POLICY_MIN_COUNT, SCALE // 10)):
    ref = gen_ref("filesecuritypolicies", counters)
    level = class_levels[min(i % len(class_levels), len(class_levels)-1)]
    file_security_policy[ref] = {
        "file_security_policy_ref": ref,
        "policy_name": f"{level}文件安全策略{i+1}",
        "classification_level": level,
        "encryption_required": random.random() < 0.8,
        "encryption_algorithm": random.choice(["AES-256", "SM4", "RSA+AES"]),
        "allowed_share_scope": random.choice(share_scopes),
        "watermark_required": random.random() < 0.5,
        "download_restricted": random.random() < 0.4,
        "print_restricted": random.random() < 0.35,
        "retention_days": random.choice([30, 90, 180, 365, None]),
        "applicable_file_types": safe_sample(["pdf", "docx", "xlsx", "csv", "png", "jpg", "zip"], random.randint(2, 5)),
        "department_ref": random.choice(department_ids) if random.random() < 0.6 else None,
        "status": random.choices(policy_statuses, weights=[75, 15, 10])[0],
        "description": "用于规范不同密级文件在分享、下载、打印、加密和保留周期方面的安全要求。",
        "created_at": created_updated(datetime(2021, 1, 1), NOW)[0],
        "updated_at": created_updated(datetime(2021, 1, 1), NOW)[1],
    }
result["file_security_policy"] = file_security_policy
pools["filesecuritypolicies"] = list(file_security_policy.keys())

# ============================================================
# 40. itservicetickets
# ============================================================
ensure_dependencies_exist("itservicetickets", pools)
it_service_ticket = {}
ticket_categories = ["incident", "service_request", "change_request", "problem", "inquiry"]
ticket_subcategories = [
    "software_fault", "hardware_fault", "network_issue", "access_request",
    "account_issue", "email_issue", "printer_issue", "vpn_issue",
    "security_concern", "data_request", "new_equipment", "software_install",
    "general_inquiry", "other"
]
ticket_urgencies = ["low", "medium", "high", "critical"]
ticket_impacts = ["individual", "team", "department", "company"]
ticket_priorities = ["P1", "P2", "P3", "P4"]
ticket_statuses = ["open", "in_progress", "pending", "resolved", "closed", "cancelled"]
resolution_categories = ["fixed", "workaround", "known_issue", "user_education", "no_fault_found", "escalated", "other"]

for i in range(DEFAULT_HEAVY_COUNT):
    ref = gen_ref("itservicetickets", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(ticket_statuses, weights=[20, 20, 15, 20, 20, 5])[0]
    assigned_to = pick_one(tech_employee_ids) if optional_value(0.75) else None
    first_responded_at = iso_datetime(random_datetime(created_dt, NOW)) if optional_value(0.7) else None
    resolved_at = None
    closed_at = None
    resolution_summary = None
    resolution_category = None
    rating = None
    rating_comment = None
    if status in ("resolved", "closed"):
        res_dt = random_datetime(created_dt, NOW)
        resolved_at = iso_datetime(res_dt)
        resolution_summary = random.choice([
            "已修复配置错误并恢复服务。",
            "已完成权限开通并通知申请人验证。",
            "已指导用户完成客户端重装并恢复使用。",
            "已更换故障设备并通过回归验证。"
        ])
        resolution_category = random.choice(resolution_categories)
    if status == "closed":
        close_base = datetime.strptime(resolved_at, "%Y-%m-%d %H:%M:%S") if resolved_at else created_dt
        closed_at = iso_datetime(random_datetime(close_base, NOW))
        if random.random() < 0.5:
            rating = random.randint(3, 5)
            rating_comment = random.choice(["处理及时，沟通清晰。", "问题已解决，满意。", "希望后续响应更快一些。"])
    it_service_ticket[ref] = {
        "it_service_ticket_ref": ref,
        "ticket_number": f"IT-{created_dt.year}-{i+1:05d}",
        "requester_employee_ref": random.choice(employee_ids),
        "ticket_category": random.choice(ticket_categories),
        "ticket_subcategory": random.choice(ticket_subcategories),
        "related_system_ref": random.choice(pools["itsystems"]) if random.random() < 0.5 else None,
        "related_printer_ref": random.choice(pools["printers"]) if random.random() < 0.2 else None,
        "related_email_account_ref": random.choice(pools["emailaccounts"]) if random.random() < 0.3 else None,
        "title": random.choice(["系统无法登录", "申请新增账号权限", "打印机无法连接", "邮箱可疑邮件咨询", "VPN访问异常", "申请安装软件"]),
        "description": chinese_paragraph(2),
        "urgency": random.choices(ticket_urgencies, weights=[15, 45, 25, 15])[0],
        "impact": random.choices(ticket_impacts, weights=[50, 25, 15, 10])[0],
        "priority": random.choices(ticket_priorities, weights=[10, 25, 35, 30])[0],
        "ticket_status": status,
        "assigned_to_ref": assigned_to,
        "assigned_group": random.choice(["服务台", "基础设施组", "网络组", "邮箱与协作组", "终端支持组"]) if assigned_to else None,
        "escalation_level": random.randint(0, 3),
        "resolution_summary": resolution_summary,
        "resolution_category": resolution_category,
        "satisfaction_rating": rating,
        "satisfaction_comment": rating_comment,
        "sla_due_at": iso_datetime(random_after(created_dt, 5)),
        "first_responded_at": first_responded_at,
        "resolved_at": resolved_at,
        "closed_at": closed_at,
        "reopened_count": random.randint(0, 2),
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["it_service_ticket"] = it_service_ticket
pools["itservicetickets"] = list(it_service_ticket.keys())

# ============================================================
# 41. itserviceticketcomments
# ============================================================
ensure_dependencies_exist("itserviceticketcomments", pools)
it_service_ticket_comment = {}
comment_types = ["reply", "note", "resolution", "escalation", "system"]

for ticket_ref, ticket in it_service_ticket.items():
    cnt = random.randint(1, 4)
    base_dt = datetime.strptime(ticket["created_at"], "%Y-%m-%d %H:%M:%S")
    for _ in range(cnt):
        ref = gen_ref("itserviceticketcomments", counters)
        cdt = random_datetime(base_dt, NOW)
        it_service_ticket_comment[ref] = {
            "it_service_ticket_comment_ref": ref,
            "it_service_ticket_ref": ticket_ref,
            "author_employee_ref": ticket["assigned_to_ref"] or ticket["requester_employee_ref"],
            "comment_type": random.choice(comment_types),
            "content": random.choice([
                "已收到问题，正在排查，请稍候。",
                "请补充报错截图与操作时间。",
                "问题已定位，正在执行修复。",
                "已完成处理，请您确认是否恢复正常。",
                "根据SLA规则，工单已升级处理。"
            ]),
            "is_internal": random.random() < 0.35,
            "attachment_file_refs": safe_sample(file_attachment_ids, random.randint(0, 2)),
            "created_at": iso_datetime(cdt),
            "updated_at": iso_datetime(random_datetime(cdt, NOW)),
        }
result["it_service_ticket_comment"] = it_service_ticket_comment
pools["itserviceticketcomments"] = list(it_service_ticket_comment.keys())

# ============================================================
# 42. itservicecontacts
# ============================================================
it_service_contact = {}
contact_types = ["hotline", "email", "chat", "walk_in", "self_service"]
contact_statuses = ["active", "inactive"]

for i in range(max(POLICY_MIN_COUNT, 10)):
    ref = gen_ref("itservicecontacts", counters)
    created, updated = created_updated(datetime(2021, 1, 1), NOW)
    it_service_contact[ref] = {
        "it_service_contact_ref": ref,
        "contact_name": random.choice(["IT服务台", "网络支持热线", "终端支持窗口", "邮箱协作支持", "自助服务门户"]) + str(i+1),
        "contact_type": random.choice(contact_types),
        "phone_number": "400-800-1234",
        "email": f"it-support{i+1}@zhiliankj.com",
        "service_hours": random.choice(["工作日 09:00-18:00", "7x12服务", "7x24值守"]),
        "location": random.choice(["A座1层服务台", "B座2层IT办公室", "线上自助门户", "企业IM在线支持"]),
        "supported_categories": safe_sample(ticket_subcategories, random.randint(3, 7)),
        "description": "为员工提供故障报修、权限申请、设备支持和一般IT咨询的服务接入点。",
        "status": random.choices(contact_statuses, weights=[85, 15])[0],
        "created_at": created,
        "updated_at": updated,
    }
result["it_service_contact"] = it_service_contact
pools["itservicecontacts"] = list(it_service_contact.keys())

# ============================================================
# 43. itknowledgearticles
# ============================================================
ensure_dependencies_exist("itknowledgearticles", pools)
it_knowledge_article = {}
article_categories = ["faq", "how_to", "troubleshooting", "policy", "announcement", "best_practice"]
article_statuses = ["draft", "published", "archived", "deprecated"]

for i in range(max(DEFAULT_MEDIUM_COUNT, 50)):
    ref = gen_ref("itknowledgearticles", counters)
    created_dt = random_datetime(datetime(2022, 1, 1), NOW)
    status = random.choices(article_statuses, weights=[20, 55, 15, 10])[0]
    published_at = None
    if status in ("published", "archived", "deprecated"):
        published_at = iso_datetime(random_datetime(created_dt, NOW))
    it_knowledge_article[ref] = {
        "it_knowledge_article_ref": ref,
        "article_title": random.choice([
            "如何重置企业邮箱密码",
            "VPN连接失败排查指南",
            "打印机脱机问题处理办法",
            "申请系统权限的标准流程",
            "常见软件安装失败解决方案",
            "文件外发安全规范说明"
        ]) + f" {i+1}",
        "article_category": random.choice(article_categories),
        "related_categories": safe_sample(["账号", "网络", "打印", "安全", "软件", "邮箱", "权限"], random.randint(2, 4)),
        "content": chinese_paragraph(6),
        "author_employee_ref": pick_one(tech_employee_ids) or pick_one(active_employee_ids),
        "view_count": random.randint(0, 10000),
        "helpful_count": random.randint(0, 5000),
        "tags": safe_sample(["FAQ", "操作指南", "安全", "网络", "邮件", "打印", "自助服务"], random.randint(2, 5)),
        "status": status,
        "published_at": published_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["it_knowledge_article"] = it_knowledge_article
pools["itknowledgearticles"] = list(it_knowledge_article.keys())

# ============================================================
# 44. printersupplies
# ============================================================
ensure_dependencies_exist("printersupplies", pools)
printer_supply = {}
supply_types = ["toner", "ink", "drum", "paper", "fuser", "waste_container", "other"]
supply_statuses = ["normal", "low", "critical", "empty", "replaced"]

for printer_ref in pools["printers"]:
    cnt = random.randint(2, 4)
    for _ in range(cnt):
        ref = gen_ref("printersupplies", counters)
        last_replaced_dt = random_datetime(datetime(2023, 1, 1), NOW) if random.random() < 0.75 else None
        printer_supply[ref] = {
            "printer_supply_ref": ref,
            "printer_ref": printer_ref,
            "supply_type": random.choice(supply_types),
            "supply_name": random.choice(["黑色墨粉", "彩色墨盒", "成像鼓", "A4纸盒", "定影组件"]),
            "supply_model": f"SUP-{random.randint(1000,9999)}",
            "remaining_percent": random.randint(0, 100),
            "stock_quantity": random.randint(0, 20),
            "reorder_threshold": random.randint(1, 5),
            "unit_cost": round(random.uniform(20, 1200), 2),
            "currency": CNY,
            "supplier": random.choice(["晨光办公", "京东企业购", "震旦办公", "天章耗材"]),
            "last_replaced_at": iso_datetime(last_replaced_dt) if last_replaced_dt else None,
            "status": random.choice(supply_statuses),
            "created_at": created_updated(datetime(2022, 1, 1), NOW)[0],
            "updated_at": created_updated(datetime(2022, 1, 1), NOW)[1],
        }
result["printer_supply"] = printer_supply
pools["printersupplies"] = list(printer_supply.keys())

# ============================================================
# 45. printerincidents
# ============================================================
ensure_dependencies_exist("printerincidents", pools)
printer_incident = {}
printer_incident_types = ["paper_jam", "toner_issue", "connectivity", "print_quality", "hardware_failure", "driver_issue", "other"]
printer_incident_statuses = ["open", "in_progress", "resolved", "closed"]

for _ in range(max(EMP_COUNT, SCALE // 2)):
    ref = gen_ref("printerincidents", counters)
    created_dt = random_datetime(datetime(2023, 1, 1), NOW)
    status = random.choices(printer_incident_statuses, weights=[25, 25, 30, 20])[0]
    resolved_at = None
    if status in ("resolved", "closed"):
        resolved_at = iso_datetime(random_datetime(created_dt, NOW))
    printer_incident[ref] = {
        "printer_incident_ref": ref,
        "printer_ref": random.choice(pools["printers"]),
        "reporter_employee_ref": random.choice(employee_ids),
        "incident_type": random.choice(printer_incident_types),
        "description": random.choice([
            "打印作业发送后无响应。",
            "打印过程中反复卡纸。",
            "扫描到邮箱失败，提示认证异常。",
            "输出内容出现重影或色块。"
        ]),
        "diagnosis": random.choice(["纸路阻塞", "墨粉余量过低", "网络连接异常", "驱动版本不兼容", None]),
        "resolution": random.choice(["已清理卡纸并复位", "已更换耗材", "已重新部署驱动", "已恢复网络连接", None]),
        "status": status,
        "assigned_to_ref": pick_one(tech_employee_ids) if optional_value(0.7) else None,
        "resolved_at": resolved_at,
        "created_at": iso_datetime(created_dt),
        "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
    }
result["printer_incident"] = printer_incident
pools["printerincidents"] = list(printer_incident.keys())

# ============================================================
# Final validation
# ============================================================
# Only domain tables in output; no base tables.
# Validate top-level table coverage
expected_output_keys = set(DOMAIN_TABLE_KEY_MAP.values())
actual_output_keys = set(result.keys())
missing = expected_output_keys - actual_output_keys
if missing:
    raise ValueError(f"Missing generated domain tables: {missing}")

print(json.dumps(result, ensure_ascii=False, indent=2))