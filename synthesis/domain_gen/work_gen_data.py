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
# Base data JSON (READ ONLY)
# Replace the triple-quoted content below with the provided base data JSON.
# ============================================================
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    BASE_DATA_JSON = f.read()

# ============================================================
# Helpers
# ============================================================
NOW = datetime(2025, 6, 15, 12, 0, 0)
START = datetime(2020, 1, 1, 0, 0, 0)

TABLE_ORDER = [
    'workarrangements',
    'teamactivities',
    'teamactivityparticipants',
    'projects',
    'scheduleeventattendees',
    'todoitems',
    'reminderrules',
    'meetings',
    'okrobjectives',
    'okrkeyresults',
    'workreports',
    'documents',
    'softwareproducts',
    'certifications',
    'examregistrations',
    'managersnapshots',
    'companyinfos',
    'projectmembers',
    'projectmilestones',
    'projecttasks',
    'projectrisks',
    'scheduleevents',
    'meetingparticipants',
    'documentcollaborators',
    'productrequirements',
    'employeecertifications',
    'examschedules',
]

FK_DEPENDENCIES = {
    'workarrangements': [('work_arrangement_ref', 'work_arrangements'), ('employee_ref', 'employees'), ('approved_by_ref', 'approved_bies')],
    'teamactivities': [('team_activity_ref', 'team_activities'), ('organizer_employee_ref', 'organizer_employees'), ('department_ref', 'departments'), ('team_ref', 'teams')],
    'teamactivityparticipants': [('team_activity_participant_ref', 'team_activity_participants'), ('team_activity_ref', 'team_activities'), ('employee_ref', 'employees')],
    'projects': [('project_ref', 'projects'), ('owner_employee_ref', 'owner_employees'), ('department_ref', 'departments'), ('team_ref', 'teams'), ('parent_project_ref', 'parent_projects')],
    'projectmembers': [('project_member_ref', 'project_members'), ('project_ref', 'projects'), ('employee_ref', 'employees')],
    'projectmilestones': [('project_milestone_ref', 'project_milestones'), ('project_ref', 'projects'), ('owner_employee_ref', 'owner_employees')],
    'projecttasks': [('project_task_ref', 'project_tasks'), ('project_ref', 'projects'), ('project_milestone_ref', 'project_milestones'), ('parent_task_ref', 'parent_tasks'), ('assignee_employee_ref', 'assignee_employees'), ('reporter_employee_ref', 'reporter_employees')],
    'projectrisks': [('project_risk_ref', 'project_risks'), ('project_ref', 'projects'), ('owner_employee_ref', 'owner_employees')],
    'scheduleevents': [('schedule_event_ref', 'schedule_events'), ('organizer_employee_ref', 'organizer_employees'), ('meeting_ref', 'meetings'), ('related_resource_ref', 'related_resources')],
    'scheduleeventattendees': [('schedule_event_attendee_ref', 'schedule_event_attendees'), ('schedule_event_ref', 'schedule_events'), ('employee_ref', 'employees')],
    'todoitems': [('todo_item_ref', 'todo_items'), ('owner_employee_ref', 'owner_employees'), ('related_resource_ref', 'related_resources')],
    'reminderrules': [('reminder_rule_ref', 'reminder_rules'), ('employee_ref', 'employees'), ('related_resource_ref', 'related_resources')],
    'meetings': [('meeting_ref', 'meetings'), ('organizer_employee_ref', 'organizer_employees'), ('schedule_event_ref', 'schedule_events'), ('recording_file_ref', 'recording_files')],
    'meetingparticipants': [('meeting_participant_ref', 'meeting_participants'), ('meeting_ref', 'meetings'), ('employee_ref', 'employees')],
    'okrobjectives': [('okr_objective_ref', 'okr_objectives'), ('owner_employee_ref', 'owner_employees'), ('scope_ref', 'scopes'), ('parent_objective_ref', 'parent_objectives')],
    'okrkeyresults': [('okr_key_result_ref', 'okr_key_results'), ('okr_objective_ref', 'okr_objectives'), ('owner_employee_ref', 'owner_employees')],
    'workreports': [('work_report_ref', 'work_reports'), ('author_employee_ref', 'author_employees'), ('related_okr_objective_ref', 'related_okr_objectives'), ('related_project_ref', 'related_projects')],
    'documents': [('document_ref', 'documents'), ('owner_employee_ref', 'owner_employees'), ('scope_ref', 'scopes'), ('parent_document_ref', 'parent_documents'), ('file_attachment_ref', 'file_attachments')],
    'documentcollaborators': [('document_collaborator_ref', 'document_collaborators'), ('document_ref', 'documents'), ('employee_ref', 'employees'), ('granted_by_ref', 'granted_bies')],
    'productrequirements': [('product_requirement_ref', 'product_requirements'), ('owner_employee_ref', 'owner_employees'), ('project_ref', 'projects'), ('software_product_ref', 'software_products'), ('parent_requirement_ref', 'parent_requirements'), ('document_ref', 'documents')],
    'softwareproducts': [('software_product_ref', 'software_products'), ('owner_employee_ref', 'owner_employees'), ('owner_department_ref', 'owner_departments')],
    'certifications': [('certification_ref', 'certifications')],
    'employeecertifications': [('employee_certification_ref', 'employee_certifications'), ('employee_ref', 'employees'), ('certification_ref', 'certifications'), ('certificate_file_ref', 'certificate_files')],
    'examschedules': [('exam_schedule_ref', 'exam_schedules'), ('certification_ref', 'certifications')],
    'examregistrations': [('exam_registration_ref', 'exam_registrations'), ('exam_schedule_ref', 'exam_schedules'), ('employee_ref', 'employees')],
    'managersnapshots': [('manager_snapshot_ref', 'manager_snapshots'), ('manager_employee_ref', 'manager_employees'), ('department_ref', 'departments')],
    'companyinfos': [('company_info_ref', 'company_infos'), ('updated_by_ref', 'updated_bies')],
}

SOFT_REF_FIELDS_ALWAYS_NULL = {
    "meeting_room_booking_ref",
    "repo_ref",
}

TABLE_KEY_MAP = {
    "workarrangements": "work_arrangement",
    "teamactivities": "team_activity",
    "teamactivityparticipants": "team_activity_participant",
    "projects": "project",
    "projectmembers": "project_member",
    "projectmilestones": "project_milestone",
    "projecttasks": "project_task",
    "projectrisks": "project_risk",
    "scheduleevents": "schedule_event",
    "scheduleeventattendees": "schedule_event_attendee",
    "todoitems": "todo_item",
    "reminderrules": "reminder_rule",
    "meetings": "meeting",
    "meetingparticipants": "meeting_participant",
    "okrobjectives": "okr_objective",
    "okrkeyresults": "okr_key_result",
    "workreports": "work_report",
    "documents": "document",
    "documentcollaborators": "document_collaborator",
    "productrequirements": "product_requirement",
    "softwareproducts": "software_product",
    "certifications": "certification",
    "employeecertifications": "employee_certification",
    "examschedules": "exam_schedule",
    "examregistrations": "exam_registration",
    "managersnapshots": "manager_snapshot",
    "companyinfos": "company_info",
}

ID_PREFIX = {
    "workarrangements": "WAR",
    "teamactivities": "TACT",
    "teamactivityparticipants": "TACP",
    "projects": "PROJ",
    "projectmembers": "PMBR",
    "projectmilestones": "PMLS",
    "projecttasks": "PTSK",
    "projectrisks": "PRSK",
    "scheduleevents": "SEVT",
    "scheduleeventattendees": "SEAT",
    "todoitems": "TODO",
    "reminderrules": "RMDR",
    "meetings": "MTG",
    "meetingparticipants": "MPAR",
    "okrobjectives": "OKRO",
    "okrkeyresults": "OKRK",
    "workreports": "WRPT",
    "documents": "DOC",
    "documentcollaborators": "DCOL",
    "productrequirements": "PRD",
    "softwareproducts": "SWP",
    "certifications": "CERT",
    "employeecertifications": "ECERT",
    "examschedules": "EXAM",
    "examregistrations": "EXRG",
    "managersnapshots": "MSNP",
    "companyinfos": "CINF",
}

WORKDAY_VALUES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def dt_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def date_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def random_dt(start_dt: datetime = START, end_dt: datetime = NOW) -> datetime:
    if end_dt <= start_dt:
        return start_dt
    seconds = int((end_dt - start_dt).total_seconds())
    return start_dt + timedelta(seconds=random.randint(0, seconds))


def random_after(dt: datetime, min_minutes=10, max_days=120):
    return dt + timedelta(minutes=random.randint(min_minutes, max_days * 24 * 60))


def chance(p: float) -> bool:
    return random.random() < p


def pick(seq):
    return random.choice(seq) if seq else None


def sample_ids(seq, min_n=1, max_n=3):
    if not seq:
        return []
    n = random.randint(min_n, min(max_n, len(seq)))
    return random.sample(seq, n)


def parse_dt(s: str) -> datetime:
    if len(s) == 10:
        return datetime.strptime(s, "%Y-%m-%d")
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def cn_sentence(words=12):
    return fake.sentence(nb_words=words)


def cn_paragraph(sentences=3):
    return "".join(fake.sentences(nb=sentences))


def rr_weekly(days):
    m = {
        "monday": "MO",
        "tuesday": "TU",
        "wednesday": "WE",
        "thursday": "TH",
        "friday": "FR",
        "saturday": "SA",
        "sunday": "SU",
    }
    return "FREQ=WEEKLY;BYDAY=" + ",".join(m[d] for d in days)


def ensure_base_loaded():
    raw = BASE_DATA_JSON.strip()
    if raw == "PASTE_BASE_DATA_JSON_HERE" or raw == "":
        raise ValueError("Please replace BASE_DATA_JSON with the provided base data JSON content.")
    return json.loads(raw)


# ============================================================
# Load base data
# ============================================================
base = ensure_base_loaded()

employee_map = base["employee"]
department_map = base["department"]
team_map = base["team"]
file_map = base["file_attachment"]
org_config_map = base["org_config"]
position_map = base["position"]
user_profile_map = base["user_profile"]
department_member_map = base["department_member"]
team_member_map = base["team_member"]

employee_ids = list(employee_map.keys())
department_ids = list(department_map.keys())
team_ids = list(team_map.keys())
file_ids = list(file_map.keys())
org_config_ids = list(org_config_map.keys())
position_ids = list(position_map.keys())
user_profile_ids = list(user_profile_map.keys())

active_employee_ids = [
    e for e, v in employee_map.items()
    if v["employment_status"] in ("active", "probation", "on_leave")
]
manager_employee_ids = sorted({
    v["direct_manager_ref"] for v in employee_map.values() if v["direct_manager_ref"] is not None
})
department_head_ids = [
    v["employee_ref"] for v in department_member_map.values()
    if v["membership_role"] in ("head", "deputy_head") and v["status"] == "active"
]
team_owner_ids = sorted({v["owner_employee_ref"] for v in team_map.values()})
team_lead_ids = [
    v["employee_ref"] for v in team_member_map.values()
    if v["team_role"] in ("lead", "tech_lead") and v["status"] == "active"
]
senior_employee_ids = sorted(set(manager_employee_ids + department_head_ids + team_owner_ids + team_lead_ids))
if not senior_employee_ids:
    senior_employee_ids = active_employee_ids[:]

employee_to_dept = {}
for rec in department_member_map.values():
    if rec["is_primary"]:
        employee_to_dept[rec["employee_ref"]] = rec["department_ref"]

employee_to_teams = {}
for rec in team_member_map.values():
    if rec["status"] == "active":
        employee_to_teams.setdefault(rec["employee_ref"], []).append(rec["team_ref"])

employee_to_timezone = {}
for e_id, e in employee_map.items():
    up = user_profile_map.get(e["user_profile_ref"])
    employee_to_timezone[e_id] = up["timezone"] if up else "Asia/Shanghai"

employee_to_locale = {}
for e_id, e in employee_map.items():
    up = user_profile_map.get(e["user_profile_ref"])
    employee_to_locale[e_id] = up["preferred_locale"] if up else "zh-CN"

employee_name_map = {}
for e_id, e in employee_map.items():
    up = user_profile_map.get(e["user_profile_ref"])
    employee_name_map[e_id] = up["display_name"] if up else e_id

# ============================================================
# Dynamic pools for FK resolution
# ============================================================
generated = {k: {} for k in TABLE_KEY_MAP.values()}
counters = {k: 1 for k in TABLE_KEY_MAP.keys()}

pools = {
    "employees": employee_ids,
    "approved_bies": senior_employee_ids,
    "organizer_employees": active_employee_ids,
    "owner_employees": active_employee_ids,
    "assignee_employees": active_employee_ids,
    "reporter_employees": active_employee_ids,
    "author_employees": active_employee_ids,
    "manager_employees": manager_employee_ids if manager_employee_ids else senior_employee_ids,
    "updated_bies": senior_employee_ids,
    "granted_bies": senior_employee_ids,
    "departments": department_ids,
    "owner_departments": department_ids,
    "teams": team_ids,
    "file_attachments": file_ids,
    "recording_files": file_ids,
    "certificate_files": file_ids,
    "related_resources": [],
    "scopes": [],
    "work_arrangements": [],
    "team_activities": [],
    "team_activity_participants": [],
    "projects": [],
    "parent_projects": [],
    "project_members": [],
    "project_milestones": [],
    "project_tasks": [],
    "parent_tasks": [],
    "project_risks": [],
    "schedule_events": [],
    "schedule_event_attendees": [],
    "todo_items": [],
    "reminder_rules": [],
    "meetings": [],
    "meeting_participants": [],
    "okr_objectives": [],
    "parent_objectives": [],
    "okr_key_results": [],
    "work_reports": [],
    "documents": [],
    "parent_documents": [],
    "document_collaborators": [],
    "product_requirements": [],
    "parent_requirements": [],
    "software_products": [],
    "certifications": [],
    "employee_certifications": [],
    "exam_schedules": [],
    "exam_registrations": [],
    "manager_snapshots": [],
    "company_infos": [],
    "related_okr_objectives": [],
    "related_projects": [],
}

# include base resources for "related_resources" and "scopes"
pools["related_resources"].extend(employee_ids + department_ids + team_ids + file_ids + org_config_ids)
pools["scopes"].extend(team_ids + department_ids)

result = {}


def next_id(table_name: str) -> str:
    prefix = ID_PREFIX[table_name]
    i = counters[table_name]
    counters[table_name] += 1
    return f"{prefix}{i:03d}"


def register_pool(table_name: str, new_id: str):
    singular = TABLE_KEY_MAP[table_name]
    result[singular][new_id] = generated[singular][new_id]

    if table_name == "workarrangements":
        pools["work_arrangements"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "teamactivities":
        pools["team_activities"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "teamactivityparticipants":
        pools["team_activity_participants"].append(new_id)
    elif table_name == "projects":
        pools["projects"].append(new_id)
        pools["parent_projects"].append(new_id)
        pools["related_projects"].append(new_id)
        pools["related_resources"].append(new_id)
        pools["scopes"].append(new_id)
    elif table_name == "projectmembers":
        pools["project_members"].append(new_id)
    elif table_name == "projectmilestones":
        pools["project_milestones"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "projecttasks":
        pools["project_tasks"].append(new_id)
        pools["parent_tasks"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "projectrisks":
        pools["project_risks"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "scheduleevents":
        pools["schedule_events"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "scheduleeventattendees":
        pools["schedule_event_attendees"].append(new_id)
    elif table_name == "todoitems":
        pools["todo_items"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "reminderrules":
        pools["reminder_rules"].append(new_id)
    elif table_name == "meetings":
        pools["meetings"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "meetingparticipants":
        pools["meeting_participants"].append(new_id)
    elif table_name == "okrobjectives":
        pools["okr_objectives"].append(new_id)
        pools["parent_objectives"].append(new_id)
        pools["related_okr_objectives"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "okrkeyresults":
        pools["okr_key_results"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "workreports":
        pools["work_reports"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "documents":
        pools["documents"].append(new_id)
        pools["parent_documents"].append(new_id)
        pools["related_resources"].append(new_id)
        pools["scopes"].append(new_id)
    elif table_name == "documentcollaborators":
        pools["document_collaborators"].append(new_id)
    elif table_name == "productrequirements":
        pools["product_requirements"].append(new_id)
        pools["parent_requirements"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "softwareproducts":
        pools["software_products"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "certifications":
        pools["certifications"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "employeecertifications":
        pools["employee_certifications"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "examschedules":
        pools["exam_schedules"].append(new_id)
        pools["related_resources"].append(new_id)
    elif table_name == "examregistrations":
        pools["exam_registrations"].append(new_id)
    elif table_name == "managersnapshots":
        pools["manager_snapshots"].append(new_id)
    elif table_name == "companyinfos":
        pools["company_infos"].append(new_id)
        pools["related_resources"].append(new_id)


def validate_dependencies(table_name: str):
    for _, pool_name in FK_DEPENDENCIES.get(table_name, []):
        if pool_name not in pools:
            raise ValueError(f"Missing FK pool '{pool_name}' for table '{table_name}'.")


for key in TABLE_KEY_MAP.values():
    result[key] = {}

# ============================================================
# Generation sizes
# ============================================================
EMP_COUNT = len(employee_ids)
AT_LEAST_2X = max(EMP_COUNT * 2, SCALE)
AT_LEAST_10 = max(10, SCALE // 10)

# ============================================================
# 1. workarrangements
# ============================================================
validate_dependencies("workarrangements")
for emp_id in employee_ids:
    for _ in range(2):
        rid = next_id("workarrangements")
        tz = employee_to_timezone.get(emp_id, "Asia/Shanghai")
        arr_type = random.choices(
            ["remote", "hybrid", "onsite", "flexible"],
            weights=[20, 35, 35, 10]
        )[0]
        start_date_dt = random_dt(datetime(2022, 1, 1), NOW - timedelta(days=60))
        status = random.choices(
            ["active", "inactive", "pending", "expired"],
            weights=[55, 10, 10, 25]
        )[0]

        end_date = None
        recurrence_rule = None
        approved_by = None
        approved_at = None

        if arr_type == "onsite":
            work_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            work_location = "上海总部办公室"
            location_detail = "上海市浦东新区张江高科技园区智联科技大厦"
        elif arr_type == "remote":
            work_days = random.sample(WORKDAY_VALUES[:5], k=random.randint(3, 5))
            work_days.sort(key=WORKDAY_VALUES.index)
            work_location = "家庭办公"
            location_detail = fake.address().replace("\n", "")
            recurrence_rule = rr_weekly(work_days)
        elif arr_type == "hybrid":
            work_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            work_location = "混合办公"
            location_detail = "每周部分时间在办公室、部分时间远程办公"
            recurrence_rule = "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"
        else:
            work_days = random.sample(WORKDAY_VALUES[:6], k=random.randint(4, 6))
            work_days.sort(key=WORKDAY_VALUES.index)
            work_location = "灵活办公"
            location_detail = "根据项目安排在办公室、客户现场或家庭办公"
            recurrence_rule = rr_weekly(work_days)

        if status == "expired":
            end_dt = random_after(start_date_dt, min_minutes=1440, max_days=300)
            if end_dt > NOW:
                end_dt = NOW - timedelta(days=random.randint(1, 30))
            end_date = date_str(end_dt)
        elif status == "inactive":
            if chance(0.7):
                end_dt = random_after(start_date_dt, min_minutes=1440, max_days=180)
                end_date = date_str(min(end_dt, NOW))
        elif status == "pending":
            approved_by = None
            approved_at = None
        else:
            approved_by = pick(senior_employee_ids)
            approved_dt = random_after(start_date_dt - timedelta(days=random.randint(1, 15)), min_minutes=30, max_days=15)
            approved_at = dt_str(min(approved_dt, NOW))

        if status in ("active", "inactive", "expired") and approved_by is None:
            approved_by = pick(senior_employee_ids)
            approved_at = dt_str(min(random_after(start_date_dt - timedelta(days=3), 10, 7), NOW))

        created_dt = start_date_dt - timedelta(days=random.randint(1, 20))
        if created_dt < START:
            created_dt = START
        updated_dt = max(created_dt, random_after(created_dt, 30, 120))
        if updated_dt > NOW:
            updated_dt = NOW

        generated["work_arrangement"][rid] = {
            "work_arrangement_ref": rid,
            "employee_ref": emp_id,
            "arrangement_type": arr_type,
            "arrangement_status": status,
            "start_date": date_str(start_date_dt),
            "end_date": end_date,
            "recurrence_rule": recurrence_rule,
            "work_days": work_days,
            "work_start_time": random.choice(["08:30", "09:00", "09:30", "10:00"]),
            "work_end_time": random.choice(["17:30", "18:00", "18:30", "19:00"]),
            "timezone": tz,
            "work_location": work_location,
            "location_detail": location_detail,
            "reason": random.choice([
                "提升工作效率与专注度",
                "兼顾项目协作与个人通勤安排",
                "根据岗位职责执行灵活办公政策",
                "因家庭情况申请远程办公安排",
                "根据部门试点政策执行混合办公",
            ]),
            "approved_by_ref": approved_by,
            "approved_at": approved_at,
            "created_at": dt_str(created_dt),
            "updated_at": dt_str(updated_dt),
        }
        register_pool("workarrangements", rid)

# ============================================================
# 2. teamactivities
# ============================================================
validate_dependencies("teamactivities")
activity_names = [
    "季度团建", "新人训练营", "跨部门协作工作坊", "技术分享日", "产品共创会",
    "设计评审训练", "年度庆功会", "团队拓展活动", "创新黑客松", "管理者沟通营"
]
for i in range(AT_LEAST_2X):
    rid = next_id("teamactivities")
    organizer = pick(active_employee_ids)
    dept_ref = employee_to_dept.get(organizer, pick(department_ids))
    linked_team = pick(employee_to_teams.get(organizer, team_ids))
    start_dt = random_dt(datetime(2023, 1, 1), NOW + timedelta(days=120))
    end_dt = start_dt + timedelta(hours=random.randint(2, 10))
    status = random.choices(
        ["draft", "planned", "ongoing", "completed", "cancelled"],
        weights=[10, 35, 5, 40, 10]
    )[0]

    if start_dt > NOW and status in ("ongoing", "completed"):
        status = random.choice(["planned", "draft"])
    if end_dt < NOW and status in ("draft", "planned"):
        status = random.choice(["completed", "cancelled"])

    generated["team_activity"][rid] = {
        "team_activity_ref": rid,
        "activity_name": f"{random.choice(activity_names)}{random.choice(['', '（第1期）', '（专项）', '（夏季场）'])}",
        "activity_type": random.choice(["team_building", "training", "workshop", "celebration", "offsite", "hackathon", "other"]),
        "description": cn_paragraph(2),
        "organizer_employee_ref": organizer,
        "department_ref": dept_ref if chance(0.8) else None,
        "team_ref": linked_team if chance(0.7) else None,
        "venue_name": random.choice(["上海总部多功能厅", "创新中心培训室", "张江会议中心", "公司天台活动区", "杭州研发中心"]),
        "venue_address": fake.address().replace("\n", ""),
        "start_time": dt_str(start_dt),
        "end_time": dt_str(end_dt),
        "headcount_limit": random.randint(15, 120),
        "budget_amount": round(random.uniform(2000, 50000), 2),
        "budget_currency": "CNY",
        "actual_cost": round(random.uniform(1500, 52000), 2) if status in ("completed", "ongoing") and chance(0.7) else None,
        "activity_status": status,
        "agenda": cn_paragraph(2),
        "notes": cn_sentence(14),
        "created_at": dt_str(start_dt - timedelta(days=random.randint(3, 30))),
        "updated_at": dt_str(min(NOW, start_dt - timedelta(days=random.randint(0, 2)) if start_dt > NOW else random_after(start_dt, 30, 30))),
    }
    register_pool("teamactivities", rid)

# ============================================================
# 3. teamactivityparticipants
# ============================================================
validate_dependencies("teamactivityparticipants")
activity_ids = pools["team_activities"][:]
for ta_id in activity_ids:
    activity = generated["team_activity"][ta_id]
    candidates = active_employee_ids[:]
    participants = sample_ids(candidates, 3, 10)
    if activity["organizer_employee_ref"] not in participants:
        participants.append(activity["organizer_employee_ref"])

    for emp_id in participants:
        rid = next_id("teamactivityparticipants")
        role = "organizer" if emp_id == activity["organizer_employee_ref"] else random.choice(["participant", "facilitator", "observer"])
        rsvp = random.choices(["pending", "accepted", "declined", "tentative"], weights=[10, 65, 10, 15])[0]

        start_dt = parse_dt(activity["start_time"])
        check_in_at = None
        if rsvp == "accepted" and activity["activity_status"] in ("ongoing", "completed") and chance(0.7):
            check_in_at = dt_str(start_dt + timedelta(minutes=random.randint(-15, 45)))

        created_dt = parse_dt(activity["created_at"])
        updated_dt = max(created_dt, random_after(created_dt, 10, 20))
        if updated_dt > NOW:
            updated_dt = NOW

        generated["team_activity_participant"][rid] = {
            "team_activity_participant_ref": rid,
            "team_activity_ref": ta_id,
            "employee_ref": emp_id,
            "participant_role": role,
            "rsvp_status": rsvp,
            "check_in_at": check_in_at,
            "notes": cn_sentence(10),
            "created_at": dt_str(created_dt),
            "updated_at": dt_str(updated_dt),
        }
        register_pool("teamactivityparticipants", rid)

# ============================================================
# 4. projects
# ============================================================
validate_dependencies("projects")
project_names = [
    "智能协同平台升级", "数据治理一期", "移动办公优化", "AI问答助手", "国际化改造",
    "统一权限中心", "研发效能提升", "知识库重构", "组织管理中台", "报表分析平台",
    "客户成功运营平台", "财务自动化项目", "新人培训系统", "会议效率提升专项"
]
project_ids_created = []
for i in range(AT_LEAST_2X):
    rid = next_id("projects")
    owner = pick(senior_employee_ids)
    dept_ref = employee_to_dept.get(owner, pick(department_ids)) if chance(0.8) else None
    team_ref = pick(employee_to_teams.get(owner, team_ids)) if chance(0.7) else None

    planned_start = random_dt(datetime(2022, 1, 1), NOW + timedelta(days=120))
    planned_end = planned_start + timedelta(days=random.randint(30, 360))
    status = random.choices(
        ["draft", "active", "on_hold", "completed", "cancelled", "archived"],
        weights=[8, 42, 12, 22, 8, 8]
    )[0]

    actual_start = None
    actual_end = None
    progress = random.randint(0, 100)

    if status in ("active", "on_hold", "completed", "cancelled", "archived"):
        actual_start_dt = planned_start + timedelta(days=random.randint(-7, 15))
        actual_start = date_str(actual_start_dt)
    if status in ("completed", "cancelled", "archived"):
        actual_end_dt = planned_end + timedelta(days=random.randint(-15, 30))
        if actual_start:
            actual_end_dt = max(actual_end_dt, parse_dt(actual_start) + timedelta(days=5))
        actual_end = date_str(actual_end_dt)

    if status == "draft":
        progress = random.randint(0, 15)
    elif status == "active":
        progress = random.randint(10, 85)
    elif status == "on_hold":
        progress = random.randint(20, 80)
    elif status in ("completed", "archived"):
        progress = 100
    elif status == "cancelled":
        progress = random.randint(5, 90)

    parent_project_ref = pick(project_ids_created) if project_ids_created and chance(0.18) else None

    created_dt = planned_start - timedelta(days=random.randint(5, 40))
    updated_dt = min(NOW, random_after(created_dt, 60, 180))

    generated["project"][rid] = {
        "project_ref": rid,
        "project_name": f"{random.choice(project_names)}{random.choice(['', '一期', '二期', '专项'])}",
        "project_code": f"PRJ-{created_dt.year}-{counters['projects']-1:04d}",
        "description": cn_paragraph(2),
        "project_type": random.choice(["development", "research", "infrastructure", "maintenance", "consulting", "other"]),
        "project_status": status,
        "priority": random.choice(["critical", "high", "medium", "low"]),
        "owner_employee_ref": owner,
        "department_ref": dept_ref,
        "team_ref": team_ref,
        "planned_start_date": date_str(planned_start),
        "planned_end_date": date_str(planned_end),
        "actual_start_date": actual_start,
        "actual_end_date": actual_end,
        "progress_percent": progress,
        "budget_amount": round(random.uniform(50000, 3000000), 2) if chance(0.8) else None,
        "budget_currency": "CNY",
        "risk_level": random.choice(["critical", "high", "medium", "low"]),
        "parent_project_ref": parent_project_ref,
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(updated_dt),
    }
    register_pool("projects", rid)
    project_ids_created.append(rid)

# ============================================================
# 5. scheduleeventattendees (generated before scheduleevents per required order)
#    We'll stage them, then materialize after scheduleevents are created.
# ============================================================
validate_dependencies("scheduleeventattendees")
pending_schedule_attendees = []

# ============================================================
# 6. todoitems
# ============================================================
validate_dependencies("todoitems")
todo_titles = ["提交周报", "更新项目方案", "完成设计评审", "处理缺陷单", "准备例会材料", "复盘上线问题", "整理需求清单"]
for emp_id in employee_ids:
    for _ in range(2):
        rid = next_id("todoitems")
        created_dt = random_dt(datetime(2023, 1, 1), NOW)
        status = random.choices(
            ["pending", "in_progress", "completed", "cancelled"],
            weights=[35, 30, 30, 5]
        )[0]
        due_dt = random_after(created_dt, 60, 45)
        completed_at = None
        if status == "completed":
            comp_dt = min(NOW, random_after(created_dt, 60, 35))
            completed_at = dt_str(comp_dt)
        related_ref = pick(pools["related_resources"]) if chance(0.7) else None

        generated["todo_item"][rid] = {
            "todo_item_ref": rid,
            "owner_employee_ref": emp_id,
            "title": random.choice(todo_titles),
            "description": cn_sentence(14),
            "todo_status": status,
            "priority": random.choice(["critical", "high", "medium", "low"]),
            "due_date": dt_str(due_dt),
            "completed_at": completed_at,
            "related_resource_type": "mixed_resource" if related_ref else None,
            "related_resource_ref": related_ref,
            "created_at": dt_str(created_dt),
            "updated_at": dt_str(min(NOW, random_after(created_dt, 20, 40))),
        }
        register_pool("todoitems", rid)

# ============================================================
# 7. reminderrules
# ============================================================
validate_dependencies("reminderrules")
for i in range(AT_LEAST_2X):
    rid = next_id("reminderrules")
    emp_id = pick(employee_ids)
    target_pool_name = random.choice(["todo_items", "projects", "related_okr_objectives", "related_resources"])
    target_pool = pools[target_pool_name]
    related_ref = pick(target_pool) if target_pool else pick(pools["related_resources"])
    remind_at_dt = random_dt(datetime(2024, 1, 1), NOW + timedelta(days=60))
    status = random.choices(["pending", "triggered", "cancelled", "failed"], weights=[60, 20, 15, 5])[0]
    triggered_at = None
    if status == "triggered":
        triggered_at = dt_str(remind_at_dt + timedelta(minutes=random.randint(0, 30)))

    generated["reminder_rule"][rid] = {
        "reminder_rule_ref": rid,
        "employee_ref": emp_id,
        "related_resource_type": random.choice(["schedule_event", "todo_item", "project_task", "okr_objective"]),
        "related_resource_ref": related_ref,
        "remind_at": dt_str(remind_at_dt),
        "offset_minutes": random.choice([5, 10, 15, 30, 60, 120, 1440]),
        "channel": random.choice(["in_app", "email", "sms", "push"]),
        "reminder_status": status,
        "triggered_at": triggered_at,
        "created_at": dt_str(remind_at_dt - timedelta(days=random.randint(1, 20))),
        "updated_at": dt_str(min(NOW, random_after(remind_at_dt - timedelta(days=5), 10, 10))),
    }
    register_pool("reminderrules", rid)

# ============================================================
# 8. meetings
# ============================================================
validate_dependencies("meetings")
meeting_titles = ["项目例会", "技术评审会", "需求澄清会", "周度同步会", "季度复盘会", "管理沟通会"]
for i in range(AT_LEAST_2X):
    rid = next_id("meetings")
    organizer = pick(active_employee_ids)
    start_dt = random_dt(datetime(2024, 1, 1), NOW + timedelta(days=90))
    end_dt = start_dt + timedelta(minutes=random.choice([30, 45, 60, 90, 120]))
    status = random.choices(
        ["scheduled", "in_progress", "completed", "cancelled"],
        weights=[45, 5, 40, 10]
    )[0]

    if start_dt > NOW and status in ("completed", "in_progress"):
        status = "scheduled"
    if end_dt < NOW and status == "scheduled":
        status = random.choice(["completed", "cancelled"])

    recording_file_ref = pick(file_ids) if chance(0.2) and status in ("completed", "in_progress") else None

    generated["meeting"][rid] = {
        "meeting_ref": rid,
        "meeting_title": random.choice(meeting_titles),
        "meeting_type": random.choice(["video", "audio", "in_person", "hybrid"]),
        "meeting_status": status,
        "organizer_employee_ref": organizer,
        "schedule_event_ref": None,  # filled later only if needed; optional
        "start_time": dt_str(start_dt),
        "end_time": dt_str(end_dt),
        "timezone": employee_to_timezone.get(organizer, "Asia/Shanghai"),
        "meeting_platform": random.choice(["internal", "zoom", "teams", "dingtalk", "other"]),
        "meeting_link": f"https://meeting.example.com/{rid.lower()}",
        "meeting_password": str(random.randint(100000, 999999)),
        "meeting_room": random.choice(["A201", "B305", "线上会议室-1", "创新讨论室", "总部大会议室"]),
        "is_recorded": recording_file_ref is not None,
        "recording_file_ref": recording_file_ref,
        "allow_screen_share": chance(0.85),
        "notes": cn_paragraph(2),
        "created_at": dt_str(start_dt - timedelta(days=random.randint(1, 15))),
        "updated_at": dt_str(min(NOW, random_after(start_dt - timedelta(days=5), 10, 10))),
    }
    register_pool("meetings", rid)

# ============================================================
# 9. okrobjectives
# ============================================================
validate_dependencies("okrobjectives")
period_labels = ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-M01", "2025-M02"]
okr_titles = [
    "提升交付效率", "优化产品体验", "增强平台稳定性", "提升客户满意度",
    "建设数据能力", "推进组织协同", "加强人才培养", "提高知识沉淀质量"
]
okr_ids_created = []
for i in range(AT_LEAST_2X):
    rid = next_id("okrobjectives")
    owner = pick(active_employee_ids)
    scope = random.choice(["individual", "team", "department", "company"])
    if scope == "team":
        scope_ref = pick(employee_to_teams.get(owner, team_ids))
    elif scope == "department":
        scope_ref = employee_to_dept.get(owner, pick(department_ids))
    elif scope == "company":
        scope_ref = None
    else:
        scope_ref = None

    period_type = random.choice(["quarterly", "semi_annual", "annual", "monthly"])
    period_label = random.choice(period_labels)
    start_dt = random_dt(datetime(2024, 1, 1), datetime(2025, 5, 1))
    end_dt = start_dt + timedelta(days=random.choice([30, 90, 180, 365]))
    status = random.choices(["draft", "active", "completed", "cancelled", "deferred"], weights=[10, 45, 25, 10, 10])[0]
    progress = random.randint(0, 100)
    score = None
    if status == "draft":
        progress = random.randint(0, 10)
    elif status == "active":
        progress = random.randint(15, 85)
    elif status == "completed":
        progress = 100
        score = round(random.uniform(0.6, 1.0), 2)
    elif status == "cancelled":
        progress = random.randint(0, 70)
    elif status == "deferred":
        progress = random.randint(0, 40)

    parent_objective_ref = pick(okr_ids_created) if okr_ids_created and chance(0.15) else None
    created_dt = start_dt - timedelta(days=random.randint(3, 20))
    updated_dt = min(NOW, random_after(created_dt, 60, 120))

    generated["okr_objective"][rid] = {
        "okr_objective_ref": rid,
        "owner_employee_ref": owner,
        "objective_title": random.choice(okr_titles),
        "description": cn_paragraph(2),
        "okr_scope": scope,
        "scope_ref": scope_ref,
        "period_type": period_type,
        "period_label": period_label,
        "start_date": date_str(start_dt),
        "end_date": date_str(end_dt),
        "parent_objective_ref": parent_objective_ref,
        "progress_percent": progress,
        "objective_status": status,
        "score": score,
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(updated_dt),
    }
    register_pool("okrobjectives", rid)
    okr_ids_created.append(rid)

# ============================================================
# 10. okrkeyresults
# ============================================================
validate_dependencies("okrkeyresults")
kr_titles = ["上线核心功能", "提高覆盖率", "降低故障率", "提升活跃用户数", "完成知识沉淀", "缩短响应时长"]
for okr_id in pools["okr_objectives"]:
    kr_count = random.randint(2, 4)
    obj = generated["okr_objective"][okr_id]
    for _ in range(kr_count):
        rid = next_id("okrkeyresults")
        metric_type = random.choice(["percentage", "number", "currency", "boolean", "milestone"])
        start_value = round(random.uniform(0, 40), 2)
        target_value = round(start_value + random.uniform(10, 120), 2)
        current_value = round(random.uniform(start_value, target_value), 2)
        progress = 0 if target_value == start_value else int(min(100, max(0, ((current_value - start_value) / (target_value - start_value)) * 100)))
        status = random.choices(["active", "completed", "cancelled", "at_risk"], weights=[55, 20, 10, 15])[0]
        score = round(random.uniform(0.5, 1.0), 2) if status == "completed" else None
        owner = obj["owner_employee_ref"] if chance(0.7) else pick(active_employee_ids)

        generated["okr_key_result"][rid] = {
            "okr_key_result_ref": rid,
            "okr_objective_ref": okr_id,
            "key_result_title": random.choice(kr_titles),
            "description": cn_sentence(16),
            "metric_type": metric_type,
            "target_value": target_value,
            "current_value": current_value,
            "start_value": start_value,
            "unit": random.choice(["%", "项", "人", "次", "万元", "小时"]),
            "progress_percent": 100 if status == "completed" else progress,
            "key_result_status": status,
            "owner_employee_ref": owner,
            "score": score,
            "created_at": obj["created_at"],
            "updated_at": dt_str(min(NOW, random_after(parse_dt(obj["created_at"]), 10, 120))),
        }
        register_pool("okrkeyresults", rid)

# ============================================================
# 11. workreports
# ============================================================
validate_dependencies("workreports")
report_titles = ["周工作汇报", "月度工作总结", "项目阶段性复盘", "季度工作回顾"]
for emp_id in employee_ids:
    for _ in range(2):
        rid = next_id("workreports")
        created_dt = random_dt(datetime(2024, 1, 1), NOW)
        report_type = random.choice(["daily", "weekly", "monthly", "quarterly"])
        if report_type == "daily":
            period_start = created_dt - timedelta(days=1)
            period_end = created_dt
        elif report_type == "weekly":
            period_start = created_dt - timedelta(days=7)
            period_end = created_dt
        elif report_type == "monthly":
            period_start = created_dt - timedelta(days=30)
            period_end = created_dt
        else:
            period_start = created_dt - timedelta(days=90)
            period_end = created_dt

        status = random.choices(["draft", "submitted", "reviewed", "returned"], weights=[20, 40, 30, 10])[0]
        submitted_at = dt_str(created_dt + timedelta(hours=random.randint(1, 48))) if status in ("submitted", "reviewed", "returned") else None

        generated["work_report"][rid] = {
            "work_report_ref": rid,
            "author_employee_ref": emp_id,
            "report_type": report_type,
            "report_title": random.choice(report_titles),
            "period_start_date": date_str(period_start),
            "period_end_date": date_str(period_end),
            "summary": cn_paragraph(2),
            "accomplishments": cn_paragraph(2),
            "issues_and_risks": cn_sentence(18),
            "next_period_plan": cn_paragraph(2),
            "report_status": status,
            "submitted_at": submitted_at,
            "related_okr_objective_ref": pick(pools["okr_objectives"]) if chance(0.5) else None,
            "related_project_ref": pick(pools["projects"]) if chance(0.6) else None,
            "recipients": sample_ids(senior_employee_ids if senior_employee_ids else active_employee_ids, 1, 3),
            "created_at": dt_str(created_dt),
            "updated_at": dt_str(min(NOW, random_after(created_dt, 20, 20))),
        }
        register_pool("workreports", rid)

# ============================================================
# 12. documents
# ============================================================
validate_dependencies("documents")
doc_titles = ["技术设计说明书", "接口规范文档", "会议纪要", "项目实施方案", "团队制度说明", "用户使用手册", "流程模板"]
document_ids_created = []
for i in range(AT_LEAST_2X):
    rid = next_id("documents")
    owner = pick(active_employee_ids)
    scope_type = random.choice(["project", "team", "department", "personal", "company", "other"])
    if scope_type == "project":
        scope_ref = pick(pools["projects"]) if pools["projects"] else None
    elif scope_type == "team":
        scope_ref = pick(employee_to_teams.get(owner, team_ids))
    elif scope_type == "department":
        scope_ref = employee_to_dept.get(owner, pick(department_ids))
    elif scope_type in ("personal", "company"):
        scope_ref = None
    else:
        scope_ref = pick(pools["scopes"]) if chance(0.5) else None

    created_dt = random_dt(datetime(2023, 1, 1), NOW)
    status = random.choices(["draft", "in_review", "published", "archived", "deprecated"], weights=[20, 15, 45, 15, 5])[0]
    parent_document_ref = pick(document_ids_created) if document_ids_created and chance(0.12) else None

    generated["document"][rid] = {
        "document_ref": rid,
        "document_title": random.choice(doc_titles),
        "document_type": random.choice(["project", "team", "department", "personal", "company", "other"]),
        "document_category": random.choice([
            "technical_spec", "design_doc", "user_guide", "api_doc", "meeting_notes",
            "policy", "process", "template", "report", "other"
        ]),
        "description": cn_sentence(16),
        "content": cn_paragraph(5),
        "document_status": status,
        "version": f"{random.randint(1,3)}.{random.randint(0,9)}",
        "owner_employee_ref": owner,
        "scope_type": scope_type,
        "scope_ref": scope_ref,
        "parent_document_ref": parent_document_ref,
        "file_attachment_ref": pick(file_ids) if chance(0.45) else None,
        "access_level": random.choice(["public", "internal", "restricted", "confidential"]),
        "tags": sample_ids(["研发", "产品", "设计", "制度", "项目", "复盘", "流程", "培训", "规范"], 1, 4),
        "view_count": random.randint(0, 500),
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(min(NOW, random_after(created_dt, 10, 150))),
    }
    register_pool("documents", rid)
    document_ids_created.append(rid)

# ============================================================
# 13. softwareproducts
# ============================================================
validate_dependencies("softwareproducts")
product_names = ["智联OA", "数据中台", "统一权限平台", "协同知识库", "移动办公端", "智能报表平台", "招聘管理系统", "培训学习平台"]
for i in range(max(AT_LEAST_10, 12)):
    rid = next_id("softwareproducts")
    owner = pick(senior_employee_ids)
    dept_ref = employee_to_dept.get(owner, pick(department_ids)) if chance(0.8) else None
    created_dt = random_dt(datetime(2021, 1, 1), NOW)

    generated["software_product"][rid] = {
        "software_product_ref": rid,
        "product_name": random.choice(product_names),
        "product_code": f"SW-{created_dt.year}-{counters['softwareproducts']-1:03d}",
        "description": cn_paragraph(2),
        "product_type": random.choice(["internal", "external", "platform", "library", "service"]),
        "product_status": random.choice(["active", "deprecated", "retired", "planning"]),
        "current_version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
        "access_url": f"https://product.example.com/{rid.lower()}",
        "documentation_url": f"https://docs.example.com/{rid.lower()}",
        "owner_employee_ref": owner,
        "owner_department_ref": dept_ref,
        "support_contact": f"{employee_name_map.get(owner, owner)} / support@example.com",
        "features_summary": cn_paragraph(2),
        "platform": random.choice(["web", "mobile", "desktop", "api", "cross_platform"]),
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(min(NOW, random_after(created_dt, 60, 180))),
    }
    register_pool("softwareproducts", rid)

# ============================================================
# 14. certifications
# ============================================================
validate_dependencies("certifications")
cert_names = [
    ("数据分析师认证", "Data"),
    ("高级项目管理认证", "Operations"),
    ("云平台工程师认证", "Engineering"),
    ("产品经理专业认证", "Product"),
    ("UI/UX设计认证", "Design"),
    ("信息安全合规认证", "Legal"),
    ("企业培训师认证", "HR"),
    ("财务分析认证", "Finance"),
]
for i in range(max(AT_LEAST_10, 12)):
    rid = next_id("certifications")
    name, job_family = random.choice(cert_names)
    created_dt = random_dt(datetime(2021, 1, 1), NOW)

    generated["certification"][rid] = {
        "certification_ref": rid,
        "certification_name": name,
        "certification_code": f"CERT-{created_dt.year}-{counters['certifications']-1:03d}",
        "issuing_authority": random.choice(["中国软件行业协会", "国家职业资格中心", "企业内部认证委员会", "国际专业认证机构"]),
        "description": cn_paragraph(2),
        "certification_type": random.choice(["professional", "technical", "compliance", "safety", "language", "other"]),
        "validity_period_months": random.choice([12, 24, 36, 60]),
        "exam_required": chance(0.8),
        "training_required": chance(0.7),
        "certification_status": random.choice(["active", "deprecated", "retired"]),
        "related_job_family": job_family,
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(min(NOW, random_after(created_dt, 60, 180))),
    }
    register_pool("certifications", rid)

# ============================================================
# 15. examregistrations (generated before examschedules per required order)
#    We'll stage them, then materialize after examschedules are created.
# ============================================================
validate_dependencies("examregistrations")
pending_exam_registrations = []

# ============================================================
# 16. managersnapshots
# ============================================================
validate_dependencies("managersnapshots")
for mgr_id in (manager_employee_ids if manager_employee_ids else senior_employee_ids):
    for _ in range(2):
        rid = next_id("managersnapshots")
        dept_ref = employee_to_dept.get(mgr_id, pick(department_ids))
        snap_date = random_dt(datetime(2024, 1, 1), NOW)
        snapshot_data = {
            "top_risks": sample_ids(
                ["资源不足", "需求变更频繁", "测试周期紧张", "跨部门协作延迟", "上线窗口受限"], 1, 3
            ),
            "focus_projects": sample_ids(pools["projects"], 1, 3) if pools["projects"] else [],
            "notes": cn_sentence(18),
        }
        generated["manager_snapshot"][rid] = {
            "manager_snapshot_ref": rid,
            "manager_employee_ref": mgr_id,
            "snapshot_date": date_str(snap_date),
            "snapshot_type": random.choice(["daily", "weekly", "monthly"]),
            "department_ref": dept_ref,
            "team_headcount": random.randint(5, 80),
            "active_projects_count": random.randint(0, 12),
            "overdue_tasks_count": random.randint(0, 25),
            "pending_approvals_count": random.randint(0, 15),
            "open_risks_count": random.randint(0, 10),
            "avg_okr_progress_percent": random.randint(10, 95),
            "upcoming_milestones_count": random.randint(0, 8),
            "on_leave_count": random.randint(0, 6),
            "remote_work_count": random.randint(0, 20),
            "snapshot_data": snapshot_data,
            "created_at": dt_str(snap_date),
        }
        register_pool("managersnapshots", rid)

# ============================================================
# 17. companyinfos
# ============================================================
validate_dependencies("companyinfos")
company_info_defs = [
    ("company_name", "智联协同科技有限公司", "string", "basic", True),
    ("company_short_name", "智联协同", "string", "basic", True),
    ("legal_entity", "智联协同科技有限公司", "string", "legal", False),
    ("tax_id", "91310000MA1KXXXXXX", "string", "legal", False),
    ("main_phone", "021-58886688", "string", "contact", True),
    ("main_address", "上海市浦东新区张江高科技园区智联科技大厦", "string", "contact", True),
    ("brand_slogan", "让协作更高效", "string", "branding", True),
    ("official_email", "contact@zhlink.example.com", "string", "contact", True),
    ("default_currency", "CNY", "string", "financial", True),
    ("security_policy", json.dumps({"mfa_required": True, "password_rotate_days": 90}, ensure_ascii=False), "json", "legal", False),
]
for i, item in enumerate(company_info_defs, start=1):
    rid = next_id("companyinfos")
    key, value, itype, category, is_public = item
    updater = pick(senior_employee_ids)
    created_dt = random_dt(datetime(2021, 1, 1), NOW)

    generated["company_info"][rid] = {
        "company_info_ref": rid,
        "info_key": key,
        "info_value": value,
        "info_type": itype,
        "info_category": category,
        "description": f"{key}信息配置",
        "is_public": is_public,
        "updated_by_ref": updater,
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(min(NOW, random_after(created_dt, 60, 180))),
    }
    register_pool("companyinfos", rid)

# ============================================================
# 18. projectmembers
# ============================================================
validate_dependencies("projectmembers")
for proj_id in pools["projects"]:
    proj = generated["project"][proj_id]
    members = sample_ids(active_employee_ids, 3, 8)
    if proj["owner_employee_ref"] not in members:
        members.append(proj["owner_employee_ref"])

    used = set()
    for emp_id in members:
        if emp_id in used:
            continue
        used.add(emp_id)
        rid = next_id("projectmembers")
        role = "owner" if emp_id == proj["owner_employee_ref"] else random.choice(["lead", "member", "observer"])
        joined_dt = max(parse_dt(proj["created_at"]), random_dt(datetime(2022, 1, 1), NOW))
        status = "removed" if chance(0.08) else "active"
        left_at = dt_str(random_after(joined_dt, 1440, 180)) if status == "removed" else None

        generated["project_member"][rid] = {
            "project_member_ref": rid,
            "project_ref": proj_id,
            "employee_ref": emp_id,
            "project_role": role,
            "joined_at": dt_str(joined_dt),
            "left_at": left_at,
            "status": status,
            "created_at": dt_str(joined_dt),
            "updated_at": dt_str(min(NOW, random_after(joined_dt, 30, 120))),
        }
        register_pool("projectmembers", rid)

# ============================================================
# 19. projectmilestones
# ============================================================
validate_dependencies("projectmilestones")
milestone_names = ["需求冻结", "设计完成", "开发完成", "测试通过", "试点上线", "正式发布", "项目验收"]
for proj_id in pools["projects"]:
    proj = generated["project"][proj_id]
    p_start = parse_dt(proj["planned_start_date"])
    for order in range(1, random.randint(3, 6) + 1):
        rid = next_id("projectmilestones")
        planned_dt = p_start + timedelta(days=order * random.randint(10, 40))
        status = random.choices(["pending", "in_progress", "completed", "delayed", "cancelled"], weights=[30, 15, 40, 10, 5])[0]
        actual_date = None
        if status == "completed":
            actual_date = date_str(planned_dt + timedelta(days=random.randint(-3, 10)))
        owner = pick(active_employee_ids)

        generated["project_milestone"][rid] = {
            "project_milestone_ref": rid,
            "project_ref": proj_id,
            "milestone_name": random.choice(milestone_names),
            "description": cn_sentence(14),
            "planned_date": date_str(planned_dt),
            "actual_date": actual_date,
            "milestone_status": status,
            "owner_employee_ref": owner,
            "display_order": order,
            "created_at": proj["created_at"],
            "updated_at": dt_str(min(NOW, random_after(parse_dt(proj["created_at"]), 10, 180))),
        }
        register_pool("projectmilestones", rid)

# ============================================================
# 20. projecttasks
# ============================================================
validate_dependencies("projecttasks")
task_titles = ["接口开发", "页面设计", "用例编写", "需求分析", "代码评审", "缺陷修复", "部署发布", "文档整理"]
task_ids_created = []
milestones_by_project = {}
for mid in pools["project_milestones"]:
    m = generated["project_milestone"][mid]
    milestones_by_project.setdefault(m["project_ref"], []).append(mid)

for proj_id in pools["projects"]:
    proj = generated["project"][proj_id]
    proj_members = [
        v["employee_ref"] for v in generated["project_member"].values()
        if v["project_ref"] == proj_id and v["status"] == "active"
    ]
    if not proj_members:
        proj_members = active_employee_ids[:]

    task_count = random.randint(6, 14)
    parent_candidates = []
    for order in range(1, task_count + 1):
        rid = next_id("projecttasks")
        title = random.choice(task_titles)
        p_start = parse_dt(proj["planned_start_date"])
        planned_start = p_start + timedelta(days=random.randint(0, 120))
        planned_end = planned_start + timedelta(days=random.randint(1, 30))
        status = random.choices(
            ["todo", "in_progress", "in_review", "done", "blocked", "cancelled"],
            weights=[25, 25, 15, 25, 7, 3]
        )[0]
        assignee = pick(proj_members)
        reporter = proj["owner_employee_ref"] if chance(0.7) else pick(proj_members)
        actual_start = None
        actual_end = None
        actual_hours = None

        if status in ("in_progress", "in_review", "done", "blocked"):
            actual_start_dt = planned_start + timedelta(days=random.randint(-1, 5))
            actual_start = date_str(actual_start_dt)
        if status == "done":
            actual_end_dt = planned_end + timedelta(days=random.randint(-2, 7))
            actual_end = date_str(max(actual_end_dt, parse_dt(actual_start) if actual_start else planned_start))
            actual_hours = round(random.uniform(2, 80), 1)
        elif status in ("in_progress", "in_review", "blocked"):
            actual_hours = round(random.uniform(1, 40), 1)

        if status == "todo":
            progress = random.randint(0, 10)
        elif status == "in_progress":
            progress = random.randint(15, 70)
        elif status == "in_review":
            progress = random.randint(70, 95)
        elif status == "done":
            progress = 100
        elif status == "blocked":
            progress = random.randint(10, 80)
        else:
            progress = random.randint(0, 50)

        parent_task_ref = pick(parent_candidates) if parent_candidates and chance(0.18) else None
        if parent_task_ref is None and chance(0.3):
            parent_candidates.append(rid)

        milestone_ref = pick(milestones_by_project.get(proj_id, [])) if chance(0.7) else None

        generated["project_task"][rid] = {
            "project_task_ref": rid,
            "project_ref": proj_id,
            "project_milestone_ref": milestone_ref,
            "parent_task_ref": parent_task_ref,
            "task_title": title,
            "task_description": cn_paragraph(2),
            "task_type": random.choice(["development", "design", "testing", "documentation", "review", "bugfix", "research", "other"]),
            "task_status": status,
            "priority": random.choice(["critical", "high", "medium", "low"]),
            "assignee_employee_ref": assignee,
            "reporter_employee_ref": reporter,
            "planned_start_date": date_str(planned_start),
            "planned_end_date": date_str(planned_end),
            "actual_start_date": actual_start,
            "actual_end_date": actual_end,
            "estimated_hours": round(random.uniform(2, 120), 1),
            "actual_hours": actual_hours,
            "progress_percent": progress,
            "display_order": order,
            "created_at": proj["created_at"],
            "updated_at": dt_str(min(NOW, random_after(parse_dt(proj["created_at"]), 10, 180))),
        }
        register_pool("projecttasks", rid)
        task_ids_created.append(rid)

# ============================================================
# 21. projectrisks
# ============================================================
validate_dependencies("projectrisks")
risk_titles = ["资源不足风险", "进度延期风险", "需求频繁变更", "关键人员依赖", "外部接口不稳定", "上线窗口冲突"]
for proj_id in pools["projects"]:
    risk_count = random.randint(1, 4)
    for _ in range(risk_count):
        rid = next_id("projectrisks")
        created_dt = random_dt(datetime(2024, 1, 1), NOW)
        status = random.choice(["open", "mitigating", "resolved", "accepted", "closed"])
        resolved_at = None
        if status in ("resolved", "closed"):
            resolved_at = dt_str(random_after(created_dt, 1440, 90))

        generated["project_risk"][rid] = {
            "project_risk_ref": rid,
            "project_ref": proj_id,
            "risk_title": random.choice(risk_titles),
            "risk_description": cn_paragraph(2),
            "risk_level": random.choice(["critical", "high", "medium", "low"]),
            "probability": random.choice(["very_high", "high", "medium", "low", "very_low"]),
            "impact": random.choice(["critical", "high", "medium", "low", "negligible"]),
            "mitigation_plan": cn_paragraph(2),
            "owner_employee_ref": pick(active_employee_ids),
            "risk_status": status,
            "identified_at": dt_str(created_dt),
            "resolved_at": resolved_at,
            "created_at": dt_str(created_dt),
            "updated_at": dt_str(min(NOW, random_after(created_dt, 60, 90))),
        }
        register_pool("projectrisks", rid)

# ============================================================
# 22. scheduleevents
# ============================================================
validate_dependencies("scheduleevents")
event_titles = ["部门例会", "项目同步", "产品评审", "一对一沟通", "专注时间", "外出拜访", "事项提醒"]
for emp_id in employee_ids:
    for _ in range(2):
        rid = next_id("scheduleevents")
        event_type = random.choice(["meeting", "appointment", "reminder", "out_of_office", "focus_time", "other"])
        start_dt = random_dt(datetime(2024, 1, 1), NOW + timedelta(days=90))
        duration_minutes = 1440 if chance(0.15) else random.choice([30, 60, 90, 120, 240])
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        status = random.choices(["tentative", "confirmed", "cancelled"], weights=[20, 70, 10])[0]
        is_all_day = duration_minutes >= 1440
        meeting_ref = pick(pools["meetings"]) if event_type == "meeting" and chance(0.65) else None

        related_ref = pick(pools["related_resources"]) if chance(0.5) else None
        recurrence_rule = None
        if chance(0.18):
            recurrence_rule = random.choice([
                "FREQ=DAILY;COUNT=5",
                "FREQ=WEEKLY;BYDAY=MO,WE,FR",
                "FREQ=MONTHLY;BYMONTHDAY=1"
            ])

        rec = {
            "schedule_event_ref": rid,
            "organizer_employee_ref": emp_id,
            "event_title": random.choice(event_titles),
            "event_description": cn_sentence(16),
            "event_type": event_type,
            "event_status": status,
            "start_time": dt_str(start_dt),
            "end_time": dt_str(end_dt),
            "timezone": employee_to_timezone.get(emp_id, "Asia/Shanghai"),
            "is_all_day": is_all_day,
            "recurrence_rule": recurrence_rule,
            "location": random.choice(["上海总部", "线上会议室", "客户现场", "杭州研发中心", "居家办公"]),
            "meeting_ref": meeting_ref,
            "visibility": random.choice(["default", "public", "private", "confidential"]),
            "related_resource_type": "mixed_resource" if related_ref else None,
            "related_resource_ref": related_ref,
            "created_at": dt_str(start_dt - timedelta(days=random.randint(1, 15))),
            "updated_at": dt_str(min(NOW, random_after(start_dt - timedelta(days=3), 30, 10))),
        }
        generated["schedule_event"][rid] = rec
        register_pool("scheduleevents", rid)

        attendees = sample_ids(active_employee_ids, 1, 5)
        if emp_id not in attendees:
            attendees.append(emp_id)
        for attendee in attendees:
            pending_schedule_attendees.append((rid, attendee, emp_id, start_dt))

# backfill meeting.schedule_event_ref if empty
meeting_ids = pools["meetings"][:]
schedule_event_ids = pools["schedule_events"][:]
meeting_events = [sid for sid in schedule_event_ids if generated["schedule_event"][sid]["meeting_ref"]]
for sid in meeting_events:
    mid = generated["schedule_event"][sid]["meeting_ref"]
    if mid in generated["meeting"] and generated["meeting"][mid]["schedule_event_ref"] is None:
        generated["meeting"][mid]["schedule_event_ref"] = sid

# ============================================================
# 23. meetingparticipants
# ============================================================
validate_dependencies("meetingparticipants")
for meeting_id in pools["meetings"]:
    meeting = generated["meeting"][meeting_id]
    participants = sample_ids(active_employee_ids, 2, 8)
    if meeting["organizer_employee_ref"] not in participants:
        participants.append(meeting["organizer_employee_ref"])

    used = set()
    for emp_id in participants:
        if emp_id in used:
            continue
        used.add(emp_id)
        rid = next_id("meetingparticipants")
        role = "host" if emp_id == meeting["organizer_employee_ref"] else random.choice(["co_host", "attendee", "presenter"])
        attendance = random.choices(["invited", "joined", "absent", "excused"], weights=[20, 55, 15, 10])[0]
        join_time = None
        leave_time = None
        start_dt = parse_dt(meeting["start_time"])
        end_dt = parse_dt(meeting["end_time"])
        if attendance == "joined":
            join_dt = start_dt + timedelta(minutes=random.randint(-5, 20))
            leave_dt = min(end_dt + timedelta(minutes=random.randint(0, 30)), join_dt + timedelta(minutes=random.randint(15, 180)))
            join_time = dt_str(join_dt)
            leave_time = dt_str(leave_dt)

        generated["meeting_participant"][rid] = {
            "meeting_participant_ref": rid,
            "meeting_ref": meeting_id,
            "employee_ref": emp_id,
            "participant_role": role,
            "join_time": join_time,
            "leave_time": leave_time,
            "attendance_status": attendance,
            "created_at": meeting["created_at"],
            "updated_at": dt_str(min(NOW, random_after(parse_dt(meeting["created_at"]), 10, 30))),
        }
        register_pool("meetingparticipants", rid)

# ============================================================
# 24. documentcollaborators
# ============================================================
validate_dependencies("documentcollaborators")
for doc_id in pools["documents"]:
    doc = generated["document"][doc_id]
    collaborators = sample_ids(active_employee_ids, 2, 6)
    if doc["owner_employee_ref"] not in collaborators:
        collaborators.append(doc["owner_employee_ref"])

    used = set()
    for emp_id in collaborators:
        if emp_id in used:
            continue
        used.add(emp_id)
        rid = next_id("documentcollaborators")
        role = "owner" if emp_id == doc["owner_employee_ref"] else random.choice(["editor", "commenter", "viewer"])
        granted_dt = parse_dt(doc["created_at"]) + timedelta(minutes=random.randint(5, 5000))
        status = "revoked" if chance(0.08) and role != "owner" else "active"

        generated["document_collaborator"][rid] = {
            "document_collaborator_ref": rid,
            "document_ref": doc_id,
            "employee_ref": emp_id,
            "collaborator_role": role,
            "granted_by_ref": doc["owner_employee_ref"],
            "granted_at": dt_str(granted_dt),
            "status": status,
            "created_at": dt_str(granted_dt),
            "updated_at": dt_str(min(NOW, random_after(granted_dt, 10, 90))),
        }
        register_pool("documentcollaborators", rid)

# ============================================================
# 25. productrequirements
# ============================================================
validate_dependencies("productrequirements")
req_titles = ["新增审批流能力", "优化首页性能", "补充审计能力", "重构权限模型", "支持国际化文案", "增强报表筛选能力"]
req_ids_created = []
for i in range(AT_LEAST_2X):
    rid = next_id("productrequirements")
    created_dt = random_dt(datetime(2024, 1, 1), NOW)
    status = random.choice(["draft", "under_review", "approved", "in_progress", "completed", "voided", "deferred"])
    closed_at = None
    voided_at = None
    if status == "completed":
        closed_at = dt_str(random_after(created_dt, 1440, 120))
    elif status == "voided":
        voided_at = dt_str(random_after(created_dt, 1440, 60))

    generated["product_requirement"][rid] = {
        "product_requirement_ref": rid,
        "requirement_title": random.choice(req_titles),
        "requirement_code": f"REQ-{created_dt.year}-{counters['productrequirements']-1:04d}",
        "description": cn_paragraph(2),
        "requirement_type": random.choice(["feature", "enhancement", "bugfix", "technical_debt", "compliance", "other"]),
        "requirement_status": status,
        "priority": random.choice(["critical", "high", "medium", "low"]),
        "business_value": cn_sentence(18),
        "acceptance_criteria": cn_paragraph(2),
        "owner_employee_ref": pick(active_employee_ids),
        "project_ref": pick(pools["projects"]) if chance(0.65) else None,
        "software_product_ref": pick(pools["software_products"]) if chance(0.7) else None,
        "parent_requirement_ref": pick(req_ids_created) if req_ids_created and chance(0.15) else None,
        "target_version": f"{random.randint(1,5)}.{random.randint(0,9)}",
        "planned_release_date": date_str(created_dt + timedelta(days=random.randint(15, 180))) if chance(0.8) else None,
        "impact_analysis": cn_paragraph(2),
        "change_reason": cn_sentence(12) if chance(0.35) else None,
        "closed_at": closed_at,
        "voided_at": voided_at,
        "document_ref": pick(pools["documents"]) if chance(0.5) else None,
        "created_at": dt_str(created_dt),
        "updated_at": dt_str(min(NOW, random_after(created_dt, 30, 120))),
    }
    register_pool("productrequirements", rid)
    req_ids_created.append(rid)

# ============================================================
# 26. employeecertifications
# ============================================================
validate_dependencies("employeecertifications")
for i in range(AT_LEAST_2X):
    rid = next_id("employeecertifications")
    emp_id = pick(employee_ids)
    cert_id = pick(pools["certifications"])
    obtained_dt = random_dt(datetime(2022, 1, 1), NOW)
    status = random.choice(["active", "expired", "revoked", "pending"])

    expiry_date = None
    if status in ("active", "expired"):
        expiry_dt = obtained_dt + timedelta(days=random.choice([365, 730, 1095]))
        expiry_date = date_str(expiry_dt)
    if status == "expired" and expiry_date and parse_dt(expiry_date) > NOW:
        expiry_date = date_str(NOW - timedelta(days=random.randint(1, 60)))

    generated["employee_certification"][rid] = {
        "employee_certification_ref": rid,
        "employee_ref": emp_id,
        "certification_ref": cert_id,
        "certificate_number": f"EC-{obtained_dt.year}-{random.randint(100000, 999999)}",
        "obtained_date": date_str(obtained_dt),
        "expiry_date": expiry_date,
        "certification_status": status,
        "score": round(random.uniform(60, 100), 1) if chance(0.7) else None,
        "certificate_file_ref": pick(file_ids) if chance(0.5) else None,
        "created_at": dt_str(obtained_dt),
        "updated_at": dt_str(min(NOW, random_after(obtained_dt, 30, 120))),
    }
    register_pool("employeecertifications", rid)

# ============================================================
# 27. examschedules
# ============================================================
validate_dependencies("examschedules")
for i in range(max(AT_LEAST_10, 12)):
    rid = next_id("examschedules")
    cert_id = pick(pools["certifications"])
    exam_dt = random_dt(datetime(2024, 1, 1), NOW + timedelta(days=120))
    deadline_dt = exam_dt - timedelta(days=random.randint(3, 30))
    status = random.choice(["open", "closed", "completed", "cancelled"])
    if exam_dt > NOW and status == "completed":
        status = random.choice(["open", "closed"])
    if exam_dt < NOW and status == "open":
        status = "closed"

    generated["exam_schedule"][rid] = {
        "exam_schedule_ref": rid,
        "certification_ref": cert_id,
        "exam_name": random.choice(["初级认证考试", "专业能力考试", "年度复审考试", "专项技能考试"]),
        "exam_date": dt_str(exam_dt),
        "registration_deadline": dt_str(deadline_dt),
        "location": random.choice(["上海总部考场", "杭州研发中心考场", "线上考试平台", "深圳分部培训室"]),
        "capacity": random.randint(20, 200),
        "exam_status": status,
        "description": cn_paragraph(2),
        "created_at": dt_str(deadline_dt - timedelta(days=random.randint(5, 20))),
        "updated_at": dt_str(min(NOW, random_after(deadline_dt - timedelta(days=1), 30, 20))),
    }
    register_pool("examschedules", rid)

# ============================================================
# Materialize deferred scheduleeventattendees
# ============================================================
for schedule_event_ref, attendee_emp, organizer_emp, start_dt in pending_schedule_attendees:
    rid = next_id("scheduleeventattendees")
    role = "required" if attendee_emp == organizer_emp else random.choice(["required", "optional", "resource"])
    rsvp = random.choices(["pending", "accepted", "declined", "tentative"], weights=[15, 55, 10, 20])[0]
    responded_at = None
    if rsvp != "pending":
        responded_at = dt_str(start_dt - timedelta(hours=random.randint(1, 48))) if start_dt > NOW else dt_str(start_dt - timedelta(hours=random.randint(1, 3)))

    generated["schedule_event_attendee"][rid] = {
        "schedule_event_attendee_ref": rid,
        "schedule_event_ref": schedule_event_ref,
        "employee_ref": attendee_emp,
        "attendee_role": role,
        "rsvp_status": rsvp,
        "responded_at": responded_at,
        "created_at": dt_str(start_dt - timedelta(days=random.randint(1, 10))),
        "updated_at": dt_str(min(NOW, random_after(start_dt - timedelta(days=2), 10, 5))),
    }
    register_pool("scheduleeventattendees", rid)

# ============================================================
# Materialize deferred examregistrations
# ============================================================
for exam_id in pools["exam_schedules"]:
    exam = generated["exam_schedule"][exam_id]
    registrants = sample_ids(active_employee_ids, 3, 12)
    for emp_id in registrants:
        rid = next_id("examregistrations")
        registered_at_dt = parse_dt(exam["registration_deadline"]) - timedelta(days=random.randint(0, 20))
        status = random.choice(["registered", "cancelled", "completed", "no_show"])
        result_val = None
        score = None
        completed_at = None
        exam_dt = parse_dt(exam["exam_date"])

        if status == "completed":
            completed_at = dt_str(exam_dt + timedelta(hours=random.randint(1, 4)))
            result_val = random.choice(["pass", "fail", "pending"])
            score = round(random.uniform(55, 100), 1)
        elif status == "registered" and exam_dt < NOW:
            result_val = "pending"

        generated.setdefault("exam_registration", {})
        generated["exam_registration"][rid] = {
            "exam_registration_ref": rid,
            "exam_schedule_ref": exam_id,
            "employee_ref": emp_id,
            "registration_status": status,
            "exam_result": result_val,
            "score": score,
            "registered_at": dt_str(registered_at_dt),
            "completed_at": completed_at,
            "created_at": dt_str(registered_at_dt),
            "updated_at": dt_str(min(NOW, random_after(registered_at_dt, 30, 60))),
        }
        result["exam_registration"][rid] = generated["exam_registration"][rid]
        pools["exam_registrations"].append(rid)

# ============================================================
# Final cleanup / output mapping
# ============================================================
# Ensure all generated singular keys exist in result
for singular_key, rows in generated.items():
    if singular_key == "exam_registration":
        continue
    result[singular_key] = rows

# soft refs forced null if somehow present
for table_rows in result.values():
    for row in table_rows.values():
        for field in list(row.keys()):
            if field in SOFT_REF_FIELDS_ALWAYS_NULL:
                row[field] = None

print(json.dumps(result, ensure_ascii=False, indent=2))