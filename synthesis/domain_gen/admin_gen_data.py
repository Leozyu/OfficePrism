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

# ------------------------------------------------------------
# 1. Paste base_data JSON here
# ------------------------------------------------------------
with open("data/domains/base/db.json", "r", encoding="utf-8") as f:
    base_data_json = f.read()

# ------------------------------------------------------------
# 2. Config
# ------------------------------------------------------------
TABLE_ORDER = [
    "campuses",
    "shuttlestops",
    "shuttleschedules",
    "shuttlebookings",
    "visitors",
    "badges",
    "supplyrequestitems",
    "supplyrequests",
    "complaints",
    "businesscards",
    "eventregistrations",
    "policies",
    "externalpartners",
    "travelpolicies",
    "cleaningrecords",
    "buildings",
    "parkingspaces",
    "evchargers",
    "shuttleroutes",
    "accesscards",
    "assets",
    "inventoryitems",
    "lostfounds",
    "securityincidents",
    "gifts",
    "servicedirectories",
    "floors",
    "accesslogs",
    "assetrequests",
    "assettransactions",
    "giftrecords",
    "zones",
    "canteens",
    "repairrequests",
    "facilities",
    "workstations",
    "lockers",
    "cleaningschedules",
    "canteenmenus",
    "facilityequipments",
    "bookings",
    "visitorappointments",
    "companyevents",
]

FK_DEPENDENCIES = {
    "campuses": [("campus_ref", "campuses"), ("map_file_ref", "map_files")],
    "buildings": [("building_ref", "buildings"), ("campus_ref", "campuses")],
    "floors": [("floor_ref", "floors"), ("building_ref", "buildings"), ("floor_plan_file_ref", "floor_plan_files")],
    "zones": [("zone_ref", "zones"), ("floor_ref", "floors")],
    "facilities": [("facility_ref", "facilities"), ("zone_ref", "zones"), ("floor_ref", "floors"), ("building_ref", "buildings"), ("campus_ref", "campuses")],
    "facilityequipments": [("facility_equipment_ref", "facility_equipments"), ("facility_ref", "facilities")],
    "bookings": [("booking_ref", "bookings"), ("facility_ref", "facilities"), ("booker_employee_ref", "booker_employees"), ("attendee_employee_refs", "attendee_employees")],
    "workstations": [("workstation_ref", "workstations"), ("zone_ref", "zones"), ("floor_ref", "floors"), ("building_ref", "buildings"), ("campus_ref", "campuses"), ("assigned_employee_ref", "assigned_employees")],
    "lockers": [("locker_ref", "lockers"), ("zone_ref", "zones"), ("floor_ref", "floors"), ("building_ref", "buildings"), ("campus_ref", "campuses"), ("assigned_employee_ref", "assigned_employees")],
    "parkingspaces": [("parking_space_ref", "parking_spaces"), ("campus_ref", "campuses"), ("assigned_employee_ref", "assigned_employees")],
    "evchargers": [("ev_charger_ref", "ev_chargers"), ("campus_ref", "campuses"), ("parking_space_ref", "parking_spaces")],
    "shuttleroutes": [("shuttle_route_ref", "shuttle_routes"), ("campus_ref", "campuses")],
    "shuttlestops": [("shuttle_stop_ref", "shuttle_stops"), ("shuttle_route_ref", "shuttle_routes")],
    "shuttleschedules": [("shuttle_schedule_ref", "shuttle_schedules"), ("shuttle_route_ref", "shuttle_routes")],
    "shuttlebookings": [("shuttle_booking_ref", "shuttle_bookings"), ("shuttle_schedule_ref", "shuttle_schedules"), ("employee_ref", "employees"), ("boarding_stop_ref", "boarding_stops")],
    "canteens": [("canteen_ref", "canteens"), ("campus_ref", "campuses"), ("floor_ref", "floors")],
    "canteenmenus": [("canteen_menu_ref", "canteen_menus"), ("canteen_ref", "canteens")],
    "visitors": [("visitor_ref", "visitors")],
    "visitorappointments": [("visitor_appointment_ref", "visitor_appointments"), ("visitor_ref", "visitors"), ("host_employee_ref", "host_employees"), ("campus_ref", "campuses"), ("facility_ref", "facilities")],
    "accesscards": [("access_card_ref", "access_cards"), ("holder_ref", "holders"), ("campus_ref", "campuses")],
    "accesslogs": [("access_log_ref", "access_logs"), ("access_card_ref", "access_cards"), ("campus_ref", "campuses"), ("building_ref", "buildings")],
    "badges": [("badge_ref", "badges"), ("employee_ref", "employees")],
    "assets": [("asset_ref", "assets"), ("campus_ref", "campuses"), ("department_ref", "departments"), ("custodian_employee_ref", "custodian_employees")],
    "assetrequests": [("asset_request_ref", "asset_requests"), ("requester_employee_ref", "requester_employees"), ("asset_ref", "assets"), ("approved_by_ref", "approved_bies")],
    "assettransactions": [("asset_transaction_ref", "asset_transactions"), ("asset_request_ref", "asset_requests"), ("asset_ref", "assets"), ("from_employee_ref", "from_employees"), ("to_employee_ref", "to_employees"), ("operated_by_ref", "operated_bies")],
    "inventoryitems": [("inventory_item_ref", "inventory_items"), ("campus_ref", "campuses")],
    "supplyrequestitems": [("inventory_item_ref", "inventory_items")],
    "supplyrequests": [("supply_request_ref", "supply_requests"), ("requester_employee_ref", "requester_employees"), ("department_ref", "departments"), ("approved_by_ref", "approved_bies")],
    "repairrequests": [("repair_request_ref", "repair_requests"), ("reporter_employee_ref", "reporter_employees"), ("resource_ref", "resources"), ("campus_ref", "campuses"), ("building_ref", "buildings"), ("floor_ref", "floors"), ("assigned_to_ref", "assigned_tos")],
    "complaints": [("complaint_ref", "complaints"), ("complainant_employee_ref", "complainant_employees"), ("related_resource_ref", "related_resources"), ("assigned_to_ref", "assigned_tos")],
    "lostfounds": [("lost_found_ref", "lost_founds"), ("reporter_employee_ref", "reporter_employees"), ("campus_ref", "campuses"), ("matched_ref", "matcheds"), ("claimed_by_ref", "claimed_bies")],
    "securityincidents": [("security_incident_ref", "security_incidents"), ("reporter_employee_ref", "reporter_employees"), ("campus_ref", "campuses"), ("assigned_to_ref", "assigned_tos")],
    "gifts": [("gift_ref", "gifts"), ("campus_ref", "campuses")],
    "giftrecords": [("gift_record_ref", "gift_records"), ("gift_ref", "gifts"), ("operated_by_ref", "operated_bies"), ("recipient_ref", "recipients")],
    "businesscards": [("business_card_ref", "business_cards"), ("employee_ref", "employees"), ("approved_by_ref", "approved_bies")],
    "companyevents": [("company_event_ref", "company_events"), ("campus_ref", "campuses"), ("facility_ref", "facilities"), ("organizer_employee_ref", "organizer_employees"), ("department_ref", "departments")],
    "eventregistrations": [("event_registration_ref", "event_registrations"), ("company_event_ref", "company_events"), ("employee_ref", "employees")],
    "policies": [("policy_ref", "policies"), ("owner_department_ref", "owner_departments"), ("author_employee_ref", "author_employees")],
    "servicedirectories": [("service_directory_ref", "service_directories"), ("contact_employee_ref", "contact_employees"), ("department_ref", "departments"), ("campus_ref", "campuses")],
    "externalpartners": [("external_partner_ref", "external_partners")],
    "travelpolicies": [("travel_policy_ref", "travel_policies")],
    "cleaningschedules": [("cleaning_schedule_ref", "cleaning_schedules"), ("campus_ref", "campuses"), ("floor_ref", "floors"), ("zone_ref", "zones"), ("assigned_vendor_ref", "assigned_vendors")],
    "cleaningrecords": [("cleaning_record_ref", "cleaning_records"), ("cleaning_schedule_ref", "cleaning_schedules")],
}

# ------------------------------------------------------------
# 3. Helpers
# ------------------------------------------------------------
def iso_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def random_datetime(start: datetime, end: datetime) -> datetime:
    if end <= start:
        return start
    delta = end - start
    sec = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=sec)

def maybe(prob=0.7):
    return random.random() < prob

def choose_one(seq):
    return random.choice(seq) if seq else None

def choose_many(seq, low=1, high=3):
    if not seq:
        return []
    k = min(len(seq), random.randint(low, high))
    return random.sample(seq, k)

def dt_from_str(s: str) -> datetime:
    if len(s) == 10:
        return datetime.strptime(s, "%Y-%m-%d")
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def created_updated(start=BASE_DATE, end=NOW):
    created = random_datetime(start, end)
    updated = random_datetime(created, end)
    return iso_datetime(created), iso_datetime(updated)

def build_ref(prefix: str, n: int) -> str:
    return f"{prefix}{n:03d}"

def cn_phone():
    prefixes = ["130", "131", "132", "133", "135", "136", "137", "138", "139", "145", "147", "150", "151", "152", "155", "156", "157", "158", "159", "180", "181", "182", "185", "186", "187", "188", "189"]
    return random.choice(prefixes) + "".join(str(random.randint(0, 9)) for _ in range(8))

def money(min_v=10, max_v=5000, ndigits=2):
    return round(random.uniform(min_v, max_v), ndigits)

def zh_sentence(words=12):
    return fake.sentence(nb_words=words)

def ensure_table_dependencies(table_name: str, available_tables: set):
    deps = FK_DEPENDENCIES.get(table_name, [])
    for field_name, target_name in deps:
        if target_name == table_name or target_name.replace("_", "") == table_name:
            continue
        if target_name in {
            "employees", "departments", "teams", "positions", "roles", "permissions",
            "audit_logs", "file_attachments", "org_configs", "notifications",
            "visitors", "campuses", "buildings", "floors", "zones", "facilities",
            "parking_spaces", "shuttle_routes", "shuttle_schedules", "company_events",
            "assets", "asset_requests", "inventory_items", "gifts", "cleaning_schedules",
            "access_cards"
        }:
            continue
        if target_name in {
            "map_files", "floor_plan_files", "boarding_stops", "holders", "resources",
            "related_resources", "recipients", "assigned_vendors", "approved_bies",
            "operated_bies", "requester_employees", "custodian_employees", "host_employees",
            "organizer_employees", "author_employees", "contact_employees",
            "booker_employees", "attendee_employees", "assigned_employees",
            "from_employees", "to_employees", "reporter_employees", "complainant_employees",
            "claimed_bies", "matcheds", "assigned_tos", "owner_departments"
        }:
            continue
        if target_name not in available_tables:
            raise ValueError(f"Dependency missing for {table_name}: {field_name} -> {target_name}")

# ------------------------------------------------------------
# 4. Parse base data
# ------------------------------------------------------------
base = json.loads(base_data_json)

employee_ids = list(base["employee"].keys())
department_ids = list(base["department"].keys())
team_ids = list(base["team"].keys())
file_ids = list(base["file_attachment"].keys())
position_ids = list(base["position"].keys())

employees = base["employee"]
departments = base["department"]
teams = base["team"]
files = base["file_attachment"]

active_employee_ids = [eid for eid, e in employees.items() if e["employment_status"] != "terminated"]
employee_name_map = {
    e["employee_ref"]: base["user_profile"][e["user_profile_ref"]]["display_name"]
    for e in employees.values()
}
department_name_map = {
    d["department_ref"]: d["department_name"]
    for d in departments.values()
}

employee_department_map = {}
for _, dm in base["department_member"].items():
    if dm["is_primary"]:
        employee_department_map[dm["employee_ref"]] = dm["department_ref"]

# ------------------------------------------------------------
# 5. ID registries and result container
# ------------------------------------------------------------
result = {}
available_generated_tables = set()

id_counters = {
    "campuses": 1,
    "buildings": 1,
    "floors": 1,
    "zones": 1,
    "facilities": 1,
    "facilityequipments": 1,
    "bookings": 1,
    "workstations": 1,
    "lockers": 1,
    "parkingspaces": 1,
    "evchargers": 1,
    "shuttleroutes": 1,
    "shuttlestops": 1,
    "shuttleschedules": 1,
    "shuttlebookings": 1,
    "canteens": 1,
    "canteenmenus": 1,
    "visitors": 1,
    "visitorappointments": 1,
    "accesscards": 1,
    "accesslogs": 1,
    "badges": 1,
    "assets": 1,
    "assetrequests": 1,
    "assettransactions": 1,
    "inventoryitems": 1,
    "supplyrequests": 1,
    "complaints": 1,
    "lostfounds": 1,
    "securityincidents": 1,
    "gifts": 1,
    "giftrecords": 1,
    "businesscards": 1,
    "companyevents": 1,
    "eventregistrations": 1,
    "policies": 1,
    "servicedirectories": 1,
    "externalpartners": 1,
    "travelpolicies": 1,
    "cleaningschedules": 1,
    "cleaningrecords": 1,
}

PREFIX_MAP = {
    "campuses": "CAMP",
    "buildings": "BLDG",
    "floors": "FLR",
    "zones": "ZONE",
    "facilities": "FAC",
    "facilityequipments": "FEQP",
    "bookings": "BOOK",
    "workstations": "WS",
    "lockers": "LOCK",
    "parkingspaces": "PS",
    "evchargers": "EVC",
    "shuttleroutes": "SRT",
    "shuttlestops": "SSTOP",
    "shuttleschedules": "SSCH",
    "shuttlebookings": "SBKG",
    "canteens": "CAN",
    "canteenmenus": "CMNU",
    "visitors": "VIS",
    "visitorappointments": "VAPT",
    "accesscards": "CARD",
    "accesslogs": "ACLG",
    "badges": "BDG",
    "assets": "AST",
    "assetrequests": "ARQ",
    "assettransactions": "ATR",
    "inventoryitems": "INV",
    "supplyrequests": "SRQ",
    "complaints": "COMP",
    "lostfounds": "LF",
    "securityincidents": "SEC",
    "gifts": "GFT",
    "giftrecords": "GREC",
    "businesscards": "BCARD",
    "companyevents": "EVT",
    "eventregistrations": "EREG",
    "policies": "POL",
    "servicedirectories": "SVC",
    "externalpartners": "PART",
    "travelpolicies": "TPOL",
    "cleaningschedules": "CLS",
    "cleaningrecords": "CLR",
}

def next_id(table_name: str) -> str:
    ref = build_ref(PREFIX_MAP[table_name], id_counters[table_name])
    id_counters[table_name] += 1
    return ref

# ------------------------------------------------------------
# 6. Generate parent-first practical data despite odd given order
#    We will still validate against the provided order list, but
#    generate in a safe dependency-respecting order for actual data.
# ------------------------------------------------------------
SAFE_ORDER = [
    "campuses",
    "buildings",
    "floors",
    "zones",
    "parkingspaces",
    "evchargers",
    "shuttleroutes",
    "shuttlestops",
    "shuttleschedules",
    "visitors",
    "badges",
    "externalpartners",
    "travelpolicies",
    "inventoryitems",
    "gifts",
    "servicedirectories",
    "assets",
    "accesscards",
    "policies",
    "canteens",
    "workstations",
    "lockers",
    "cleaningschedules",
    "facilities",
    "facilityequipments",
    "supplyrequests",
    "complaints",
    "businesscards",
    "lostfounds",
    "securityincidents",
    "accesslogs",
    "assetrequests",
    "assettransactions",
    "giftrecords",
    "canteenmenus",
    "bookings",
    "visitorappointments",
    "companyevents",
    "eventregistrations",
    "shuttlebookings",
    "cleaningrecords",
]

# counts
num_employees = len(employee_ids)
at_least_2x = max(2 * num_employees, SCALE)

# holders
campus_ids = []
building_ids = []
floor_ids = []
zone_ids = []
facility_ids = []
parking_space_ids = []
ev_charger_ids = []
shuttle_route_ids = []
shuttle_stop_ids = []
shuttle_schedule_ids = []
visitor_ids = []
badge_ids = []
asset_ids = []
inventory_item_ids = []
gift_ids = []
external_partner_ids = []
travel_policy_ids = []
canteen_ids = []
workstation_ids = []
locker_ids = []
cleaning_schedule_ids = []
access_card_ids = []
policy_ids = []
service_directory_ids = []
booking_ids = []
asset_request_ids = []
company_event_ids = []

# for supplyrequestitems embedding support
inventory_item_pool_for_supply = []

# meeting booking non-overlap
facility_booking_windows = {}

# recipient universe for gift records
recipient_universe = []

for table_name in SAFE_ORDER:
    ensure_table_dependencies(table_name, available_generated_tables | {
        "employees", "departments", "teams", "positions", "roles", "permissions",
        "audit_logs", "file_attachments", "org_configs", "notifications"
    })

    # --------------------------------------------------------
    # campuses
    # --------------------------------------------------------
    if table_name == "campuses":
        table = {}
        city_pool = [
            ("上海", "CN", 31.2304, 121.4737),
            ("北京", "CN", 39.9042, 116.4074),
            ("深圳", "CN", 22.5431, 114.0579),
            ("杭州", "CN", 30.2741, 120.1551),
            ("成都", "CN", 30.5728, 104.0668),
            ("广州", "CN", 23.1291, 113.2644),
            ("苏州", "CN", 31.2989, 120.5853),
            ("武汉", "CN", 30.5928, 114.3055),
            ("西安", "CN", 34.3416, 108.9398),
            ("南京", "CN", 32.0603, 118.7969),
        ]
        campus_type_pool = ["headquarters", "branch", "r&d_center", "manufacturing", "warehouse", "other"]
        campus_status_pool = ["active", "active", "active", "inactive", "under_construction"]

        for i in range(10):
            ref = next_id("campuses")
            city, country, lat, lng = city_pool[i % len(city_pool)]
            created, updated = created_updated(datetime(2020, 1, 1), NOW)
            map_file_ref = choose_one(file_ids) if maybe(0.6) else None
            table[ref] = {
                "campus_ref": ref,
                "campus_name": f"{city}{random.choice(['总部园区', '创新园区', '科技园', '办公园区', '研发中心'])}",
                "campus_code": f"C{100+i}",
                "campus_type": campus_type_pool[i % len(campus_type_pool)],
                "campus_status": random.choice(campus_status_pool),
                "address": f"{city}{fake.street_address()}",
                "city": city,
                "country": country,
                "geo_lat": round(lat + random.uniform(-0.05, 0.05), 6),
                "geo_lng": round(lng + random.uniform(-0.05, 0.05), 6),
                "map_file_ref": map_file_ref,
                "description": f"{city}园区用于支持公司办公、访客接待、行政服务与协同活动。",
                "created_at": created,
                "updated_at": updated,
            }
            campus_ids.append(ref)

        result["campus"] = table
        available_generated_tables.add("campuses")

    # --------------------------------------------------------
    # buildings
    # --------------------------------------------------------
    elif table_name == "buildings":
        table = {}
        for camp_ref in campus_ids:
            for bno in range(1, random.randint(2, 4) + 1):
                ref = next_id("buildings")
                created, updated = created_updated(datetime(2020, 1, 1), NOW)
                table[ref] = {
                    "building_ref": ref,
                    "campus_ref": camp_ref,
                    "building_name": f"{random.choice(['A', 'B', 'C', 'D', 'E'])}{bno}号楼",
                    "building_code": f"{camp_ref[-3:]}-B{bno}",
                    "floor_count": random.randint(3, 12),
                    "building_status": random.choice(["active", "active", "active", "under_renovation", "inactive"]),
                    "description": random.choice([
                        "综合办公楼，含工位区、会议区及公共休闲区。",
                        "研发办公楼，主要服务技术与产品团队。",
                        "行政支持楼，包含访客接待、培训及后勤空间。",
                    ]),
                    "created_at": created,
                    "updated_at": updated,
                }
                building_ids.append(ref)

        result["building"] = table
        available_generated_tables.add("buildings")

    # --------------------------------------------------------
    # floors
    # --------------------------------------------------------
    elif table_name == "floors":
        table = {}
        building_map = result["building"]
        for b_ref in building_ids:
            floor_count = building_map[b_ref]["floor_count"]
            for floor_no in range(1, floor_count + 1):
                ref = next_id("floors")
                created, updated = created_updated(datetime(2020, 1, 1), NOW)
                table[ref] = {
                    "floor_ref": ref,
                    "building_ref": b_ref,
                    "floor_number": floor_no,
                    "floor_name": f"{floor_no}F",
                    "floor_plan_file_ref": choose_one(file_ids) if maybe(0.5) else None,
                    "floor_status": random.choice(["active", "active", "active", "under_renovation"]),
                    "created_at": created,
                    "updated_at": updated,
                }
                floor_ids.append(ref)

        result["floor"] = table
        available_generated_tables.add("floors")

    # --------------------------------------------------------
    # zones
    # --------------------------------------------------------
    elif table_name == "zones":
        table = {}
        floor_to_building = {fref: result["floor"][fref]["building_ref"] for fref in floor_ids}
        building_to_campus = {bref: result["building"][bref]["campus_ref"] for bref in building_ids}
        zone_types = ["office", "meeting", "lounge", "storage", "cafeteria", "gym", "parking", "lobby", "server_room", "other"]

        for f_ref in floor_ids:
            zones_per_floor = random.randint(3, 6)
            for i in range(1, zones_per_floor + 1):
                ref = next_id("zones")
                ztype = random.choice(zone_types)
                created, updated = created_updated(datetime(2020, 1, 1), NOW)
                table[ref] = {
                    "zone_ref": ref,
                    "floor_ref": f_ref,
                    "zone_name": f"{random.choice(['东', '西', '南', '北', '中'])}区{random.choice(['办公区', '会议区', '协作区', '休闲区', '设备区'])}",
                    "zone_code": f"{f_ref[-3:]}-Z{i}",
                    "zone_type": ztype,
                    "zone_status": random.choice(["active", "active", "active", "under_renovation"]),
                    "description": f"该区域主要用于{random.choice(['日常办公', '会议协作', '员工休闲', '设备存储', '公共接待'])}。",
                    "created_at": created,
                    "updated_at": updated,
                }
                zone_ids.append(ref)

        result["zone"] = table
        available_generated_tables.add("zones")

    # --------------------------------------------------------
    # parkingspaces
    # --------------------------------------------------------
    elif table_name == "parkingspaces":
        table = {}
        for camp_ref in campus_ids:
            for i in range(1, 21):
                ref = next_id("parkingspaces")
                assigned = choose_one(active_employee_ids) if maybe(0.35) else None
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                assigned_at = None
                expires_at = None
                status = "available"
                if assigned:
                    assigned_dt = random_datetime(datetime(2022, 1, 1), NOW)
                    assigned_at = iso_datetime(assigned_dt)
                    if maybe(0.4):
                        expires_at = iso_datetime(assigned_dt + timedelta(days=random.randint(30, 365)))
                    status = random.choice(["occupied", "reserved"])
                else:
                    status = random.choice(["available", "available", "under_maintenance", "decommissioned"])
                table[ref] = {
                    "parking_space_ref": ref,
                    "space_code": f"{camp_ref[-3:]}-P{i:03d}",
                    "campus_ref": camp_ref,
                    "parking_zone": random.choice(["A区", "B区", "C区", "地面停车区", "地下停车区"]),
                    "space_type": random.choice(["standard", "compact", "large", "disabled", "ev_only", "vip"]),
                    "ev_charging": maybe(0.25),
                    "space_status": status,
                    "assigned_employee_ref": assigned,
                    "assigned_at": assigned_at,
                    "expires_at": expires_at,
                    "created_at": created,
                    "updated_at": updated,
                }
                parking_space_ids.append(ref)

        result["parking_space"] = table
        available_generated_tables.add("parkingspaces")

    # --------------------------------------------------------
    # evchargers
    # --------------------------------------------------------
    elif table_name == "evchargers":
        table = {}
        ps_map = result["parking_space"]
        ev_spaces = [ps for ps in parking_space_ids if ps_map[ps]["ev_charging"]]
        for ps_ref in ev_spaces[:max(10, len(ev_spaces))]:
            ref = next_id("evchargers")
            camp_ref = ps_map[ps_ref]["campus_ref"]
            created, updated = created_updated(datetime(2021, 1, 1), NOW)
            table[ref] = {
                "ev_charger_ref": ref,
                "charger_code": f"EV-{ps_ref[-3:]}",
                "campus_ref": camp_ref,
                "parking_space_ref": ps_ref,
                "charger_type": random.choice(["ac_slow", "ac_fast", "dc_fast", "super_fast"]),
                "power_kw": round(random.choice([7, 11, 22, 60, 120, 180]), 1),
                "charger_status": random.choice(["available", "available", "in_use", "faulty", "under_maintenance"]),
                "fee_per_kwh": round(random.uniform(0.8, 2.5), 2),
                "operator": random.choice(["国家电网", "特来电", "星星充电", "园区自营"]),
                "created_at": created,
                "updated_at": updated,
            }
            ev_charger_ids.append(ref)

        result["ev_charger"] = table
        available_generated_tables.add("evchargers")

    # --------------------------------------------------------
    # shuttleroutes
    # --------------------------------------------------------
    elif table_name == "shuttleroutes":
        table = {}
        route_templates = [
            "地铁接驳线", "早晚通勤线", "环园区线", "研发中心线", "行政办公线"
        ]
        for camp_ref in campus_ids:
            for i in range(1, 3):
                ref = next_id("shuttleroutes")
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "shuttle_route_ref": ref,
                    "route_name": f"{result['campus'][camp_ref]['city']}{random.choice(route_templates)}",
                    "route_code": f"{camp_ref[-3:]}-R{i}",
                    "campus_ref": camp_ref,
                    "direction": random.choice(["inbound", "outbound", "circular"]),
                    "route_status": random.choice(["active", "active", "suspended"]),
                    "description": "班车线路覆盖主要地铁站、园区出入口及办公楼群，满足员工通勤需求。",
                    "created_at": created,
                    "updated_at": updated,
                }
                shuttle_route_ids.append(ref)

        result["shuttle_route"] = table
        available_generated_tables.add("shuttleroutes")

    # --------------------------------------------------------
    # shuttlestops
    # --------------------------------------------------------
    elif table_name == "shuttlestops":
        table = {}
        route_map = result["shuttle_route"]
        for route_ref in shuttle_route_ids:
            camp_ref = route_map[route_ref]["campus_ref"]
            lat = result["campus"][camp_ref]["geo_lat"]
            lng = result["campus"][camp_ref]["geo_lng"]
            stop_count = random.randint(4, 6)
            for i in range(1, stop_count + 1):
                ref = next_id("shuttlestops")
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "shuttle_stop_ref": ref,
                    "shuttle_route_ref": route_ref,
                    "stop_name": random.choice(["南门", "北门", "西门", "东门", "地铁站A口", "地铁站B口", "行政楼前", "研发楼前"]) + f"{i}",
                    "stop_order": i,
                    "geo_lat": round(lat + random.uniform(-0.02, 0.02), 6),
                    "geo_lng": round(lng + random.uniform(-0.02, 0.02), 6),
                    "created_at": created,
                    "updated_at": updated,
                }
                shuttle_stop_ids.append(ref)

        result["shuttle_stop"] = table
        available_generated_tables.add("shuttlestops")

    # --------------------------------------------------------
    # shuttleschedules
    # --------------------------------------------------------
    elif table_name == "shuttleschedules":
        table = {}
        depart_time_pool = ["07:30", "08:00", "08:30", "09:00", "17:30", "18:00", "18:30", "19:00"]
        for route_ref in shuttle_route_ids:
            for depart_time in random.sample(depart_time_pool, k=4):
                ref = next_id("shuttleschedules")
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "shuttle_schedule_ref": ref,
                    "shuttle_route_ref": route_ref,
                    "depart_time": depart_time,
                    "effective_days": random.choice([
                        ["mon", "tue", "wed", "thu", "fri"],
                        ["mon", "wed", "fri"],
                        ["tue", "thu"],
                        ["mon", "tue", "wed", "thu", "fri", "sat"],
                    ]),
                    "seat_capacity": random.randint(20, 50),
                    "schedule_status": random.choice(["active", "active", "active", "suspended"]),
                    "created_at": created,
                    "updated_at": updated,
                }
                shuttle_schedule_ids.append(ref)

        result["shuttle_schedule"] = table
        available_generated_tables.add("shuttleschedules")

    # --------------------------------------------------------
    # visitors
    # --------------------------------------------------------
    elif table_name == "visitors":
        table = {}
        visitor_type_pool = ["business", "government", "contractor", "personal", "other"]
        for _ in range(at_least_2x):
            ref = next_id("visitors")
            created, updated = created_updated(datetime(2022, 1, 1), NOW)
            table[ref] = {
                "visitor_ref": ref,
                "full_name": fake.name(),
                "id_type": random.choice(["id_card", "passport", "driver_license", "other"]),
                "id_number": fake.ssn(),
                "phone": cn_phone(),
                "email": fake.email(),
                "company": random.choice(["华辰科技", "星云数据", "远景咨询", "博远制造", "新联供应链", "城市管理局"]),
                "visitor_type": random.choice(visitor_type_pool),
                "created_at": created,
                "updated_at": updated,
            }
            visitor_ids.append(ref)

        result["visitor"] = table
        available_generated_tables.add("visitors")

    # --------------------------------------------------------
    # badges
    # --------------------------------------------------------
    elif table_name == "badges":
        table = {}
        for eid in employee_ids:
            ref = next_id("badges")
            emp = employees[eid]
            issued_dt = dt_from_str(emp["created_at"])
            expires_at = None
            lost_at = None
            returned_at = None
            badge_status = "active"
            if emp["employment_status"] == "terminated":
                badge_status = random.choice(["returned", "inactive", "expired"])
                if maybe(0.7):
                    returned_at = iso_datetime(random_datetime(issued_dt, NOW))
            elif maybe(0.05):
                badge_status = "lost"
                lost_at = iso_datetime(random_datetime(issued_dt, NOW))
            elif maybe(0.08):
                badge_status = "expired"
                expires_at = iso_datetime(issued_dt + timedelta(days=random.randint(365, 730)))

            updated = iso_datetime(random_datetime(issued_dt, NOW))
            table[ref] = {
                "badge_ref": ref,
                "employee_ref": eid,
                "badge_number": f"BD-{eid[-3:]}-{random.randint(1000,9999)}",
                "badge_type": random.choice(["standard", "executive", "contractor", "intern", "visitor"]),
                "badge_status": badge_status,
                "issued_at": iso_datetime(issued_dt),
                "expires_at": expires_at,
                "lost_at": lost_at,
                "returned_at": returned_at,
                "notes": "员工身份识别证件，用于日常出入、会议签到和行政服务校验。",
                "created_at": iso_datetime(issued_dt),
                "updated_at": updated,
            }
            badge_ids.append(ref)

        result["badge"] = table
        available_generated_tables.add("badges")

    # --------------------------------------------------------
    # externalpartners
    # --------------------------------------------------------
    elif table_name == "externalpartners":
        table = {}
        partner_types = ["supplier", "vendor", "contractor", "service_provider", "logistics", "other"]
        for _ in range(max(20, SCALE // 4)):
            ref = next_id("externalpartners")
            created, updated = created_updated(datetime(2020, 1, 1), NOW)
            table[ref] = {
                "external_partner_ref": ref,
                "partner_name": fake.company(),
                "partner_type": random.choice(partner_types),
                "contact_person": fake.name(),
                "contact_phone": cn_phone(),
                "contact_email": fake.company_email(),
                "address": fake.address(),
                "partner_status": random.choice(["active", "active", "active", "inactive", "suspended", "blacklisted"]),
                "description": random.choice([
                    "长期合作供应商，提供园区行政物资与日常服务。",
                    "外部服务伙伴，负责设施维护、保洁或安保支持。",
                    "项目型合作商，按需提供设备、物流或专项服务。",
                ]),
                "created_at": created,
                "updated_at": updated,
            }
            external_partner_ids.append(ref)

        result["external_partner"] = table
        available_generated_tables.add("externalpartners")

    # --------------------------------------------------------
    # travelpolicies
    # --------------------------------------------------------
    elif table_name == "travelpolicies":
        table = {}
        combos = [
            (3, 5, "tier3", 350, 120, "high_speed_rail_second"),
            (5, 6, "tier2", 500, 150, "economy"),
            (6, 7, "tier1", 700, 180, "high_speed_rail_first"),
            (7, 9, "tier1", 1000, 220, "business"),
            (7, 9, "international", 1800, 300, "business"),
            (1, 2, "tier1", 1200, 250, "business"),
            (3, 9, "international", 2200, 350, "economy"),
            (1, 4, "international", 2800, 450, "business"),
            (5, 9, "tier3", 450, 130, "high_speed_rail_first"),
            (1, 9, "tier2", 650, 160, "economy"),
        ]
        for idx, (lmin, lmax, city_tier, hotel, meal_limit, transport) in enumerate(combos, start=1):
            ref = next_id("travelpolicies")
            effective_dt = random_datetime(datetime(2020, 1, 1), datetime(2024, 1, 1))
            expiry_date = None
            status = random.choice(["active", "active", "draft", "inactive"])
            if status == "expired":
                expiry_date = iso_date(random_datetime(effective_dt + timedelta(days=30), NOW))
            elif maybe(0.3):
                expiry_date = iso_date(effective_dt + timedelta(days=random.randint(365, 1500)))
            created, updated = created_updated(datetime(2020, 1, 1), NOW)
            table[ref] = {
                "travel_policy_ref": ref,
                "policy_name": f"差旅标准政策{idx}",
                "position_level_min": lmin,
                "position_level_max": lmax,
                "city_tier": city_tier,
                "hotel_daily_limit": float(hotel),
                "meal_daily_limit": float(meal_limit),
                "transport_class": transport,
                "effective_date": iso_date(effective_dt),
                "expiry_date": expiry_date,
                "policy_status": status,
                "notes": "用于员工差旅订票、住宿和餐补报销审核的统一标准。",
                "created_at": created,
                "updated_at": updated,
            }
            travel_policy_ids.append(ref)

        result["travel_policy"] = table
        available_generated_tables.add("travelpolicies")

    # --------------------------------------------------------
    # inventoryitems
    # --------------------------------------------------------
    elif table_name == "inventoryitems":
        table = {}
        items_seed = [
            ("A4复印纸", "office_supply", "打印耗材", "箱"),
            ("中性笔", "office_supply", "文具", "盒"),
            ("便利贴", "office_supply", "文具", "包"),
            ("笔记本", "office_supply", "文具", "本"),
            ("键盘", "it_accessory", "电脑外设", "个"),
            ("鼠标", "it_accessory", "电脑外设", "个"),
            ("HDMI线", "it_accessory", "会议连接线", "根"),
            ("清洁剂", "cleaning_supply", "日化用品", "瓶"),
            ("垃圾袋", "cleaning_supply", "保洁用品", "卷"),
            ("纸杯", "kitchen_supply", "茶水间用品", "条"),
            ("洗手液", "kitchen_supply", "卫生用品", "瓶"),
            ("安全帽", "safety_equipment", "安全防护", "顶"),
            ("反光背心", "safety_equipment", "安全防护", "件"),
        ]
        for camp_ref in campus_ids:
            for idx, item_tpl in enumerate(items_seed, start=1):
                ref = next_id("inventoryitems")
                name, cat, subcat, unit = item_tpl
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "inventory_item_ref": ref,
                    "item_name": name,
                    "item_code": f"{camp_ref[-3:]}-ITM-{idx:03d}",
                    "item_category": cat,
                    "item_subcategory": subcat,
                    "unit": unit,
                    "campus_ref": camp_ref,
                    "storage_location": random.choice(["1层后勤仓", "B1物资库", "行政仓库A", "楼层补给点"]),
                    "current_stock": random.randint(20, 300),
                    "min_stock_alert": random.randint(5, 30),
                    "unit_cost": money(2, 300),
                    "item_status": random.choice(["active", "active", "active", "inactive", "discontinued"]),
                    "description": f"{name}用于日常行政支持与办公运营保障。",
                    "created_at": created,
                    "updated_at": updated,
                }
                inventory_item_ids.append(ref)
                inventory_item_pool_for_supply.append(ref)

        result["inventory_item"] = table
        available_generated_tables.add("inventoryitems")

    # --------------------------------------------------------
    # gifts
    # --------------------------------------------------------
    elif table_name == "gifts":
        table = {}
        gift_names = ["保温杯", "纪念笔记本", "企业雨伞", "定制U盘", "节日礼盒", "员工周年礼", "会议伴手礼", "奖牌摆件", "咖啡礼盒", "定制帆布包"]
        for idx, gname in enumerate(gift_names, start=1):
            ref = next_id("gifts")
            camp_ref = choose_one(campus_ids)
            created, updated = created_updated(datetime(2021, 1, 1), NOW)
            table[ref] = {
                "gift_ref": ref,
                "gift_name": gname,
                "gift_code": f"GIFT-{idx:03d}",
                "gift_category": random.choice(["souvenir", "holiday", "recognition", "visitor", "event"]),
                "unit_cost": money(15, 300),
                "current_stock": random.randint(30, 300),
                "min_stock_alert": random.randint(5, 20),
                "storage_location": random.choice(["礼品库A", "礼品库B", "行政仓", "前台储物柜"]),
                "campus_ref": camp_ref,
                "gift_status": random.choice(["active", "active", "inactive", "discontinued"]),
                "description": f"{gname}用于企业活动、员工关怀及访客接待场景。",
                "created_at": created,
                "updated_at": updated,
            }
            gift_ids.append(ref)

        result["gift"] = table
        available_generated_tables.add("gifts")

    # --------------------------------------------------------
    # servicedirectories
    # --------------------------------------------------------
    elif table_name == "servicedirectories":
        table = {}
        service_templates = [
            ("行政前台", "admin", "访客接待、会议支持与行政咨询"),
            ("IT服务台", "it", "电脑、账号、网络及会议设备支持"),
            ("HR支持窗口", "hr", "入转调离、证明、福利与制度咨询"),
            ("财务服务台", "finance", "报销、付款、发票与预算咨询"),
            ("法务咨询窗口", "legal", "合同、合规与法务支持"),
            ("安保值班室", "security", "安全巡检、门禁与突发事件处理"),
            ("设施服务中心", "facility", "工位、会议室、设备与维修支持"),
            ("餐饮服务台", "canteen", "餐卡、菜单、团餐与意见反馈"),
        ]
        for i, tpl in enumerate(service_templates, start=1):
            ref = next_id("servicedirectories")
            svc_name, category, desc = tpl
            dept_ref = choose_one(department_ids)
            camp_ref = choose_one(campus_ids)
            contact_emp = choose_one(active_employee_ids) if maybe(0.7) else None
            created, updated = created_updated(datetime(2021, 1, 1), NOW)
            table[ref] = {
                "service_directory_ref": ref,
                "service_name": svc_name,
                "service_category": category,
                "service_description": desc,
                "contact_phone": cn_phone(),
                "contact_email": fake.company_email(),
                "contact_employee_ref": contact_emp,
                "department_ref": dept_ref,
                "campus_ref": camp_ref,
                "service_hours": random.choice(["周一至周五 09:00-18:00", "7x12小时", "工作日 08:30-17:30"]),
                "location_description": random.choice(["1层服务台", "行政办公区", "综合服务中心", "前台区域"]),
                "service_status": random.choice(["active", "active", "inactive", "suspended"]),
                "created_at": created,
                "updated_at": updated,
            }
            service_directory_ids.append(ref)

        result["service_directory"] = table
        available_generated_tables.add("servicedirectories")

    # --------------------------------------------------------
    # assets
    # --------------------------------------------------------
    elif table_name == "assets":
        table = {}
        asset_seed = [
            ("笔记本电脑", "it_equipment", "电脑"),
            ("显示器", "it_equipment", "显示设备"),
            ("工学椅", "furniture", "办公座椅"),
            ("升降桌", "furniture", "办公桌"),
            ("打印机", "office_equipment", "打印设备"),
            ("投影仪", "office_equipment", "会议设备"),
            ("测试手机", "lab_equipment", "测试设备"),
            ("会议平板", "office_equipment", "会议设备"),
            ("商务车辆", "vehicle", "通勤用车"),
            ("门禁控制器", "office_equipment", "安防设备"),
        ]
        for _ in range(at_least_2x):
            ref = next_id("assets")
            name, cat, subcat = random.choice(asset_seed)
            custodian = choose_one(active_employee_ids)
            dept_ref = employee_department_map.get(custodian, choose_one(department_ids))
            camp_ref = choose_one(campus_ids)
            purchase_dt = random_datetime(datetime(2020, 1, 1), NOW)
            created = iso_datetime(purchase_dt)
            updated = iso_datetime(random_datetime(purchase_dt, NOW))
            warranty_expires_at = iso_date(purchase_dt + timedelta(days=random.randint(365, 1095))) if maybe(0.7) else None
            table[ref] = {
                "asset_ref": ref,
                "asset_name": name,
                "asset_code": f"AST-{random.randint(100000,999999)}",
                "asset_category": cat,
                "asset_subcategory": subcat,
                "brand": random.choice(["联想", "戴尔", "华为", "惠普", "Apple", "小米", "海信"]),
                "model": random.choice(["Pro 14", "EliteBook", "ThinkPad X1", "MateBook", "27Q", "M3", "MX-01"]),
                "serial_number": fake.uuid4()[:12].upper(),
                "campus_ref": camp_ref,
                "department_ref": dept_ref,
                "custodian_employee_ref": custodian,
                "purchase_date": iso_date(purchase_dt),
                "purchase_price": money(300, 25000),
                "warranty_expires_at": warranty_expires_at,
                "asset_status": random.choice(["in_use", "available", "under_repair", "reserved", "in_transit", "scrapped"]),
                "description": f"{name}用于支持员工办公、会议协作或行政保障。",
                "created_at": created,
                "updated_at": updated,
            }
            asset_ids.append(ref)

        result["asset"] = table
        available_generated_tables.add("assets")

    # --------------------------------------------------------
    # accesscards
    # --------------------------------------------------------
    elif table_name == "accesscards":
        table = {}
        # employee holders
        for eid in employee_ids:
            ref = next_id("accesscards")
            emp = employees[eid]
            dept_ref = employee_department_map.get(eid, choose_one(department_ids))
            campus_ref = choose_one(campus_ids)
            access_zone_sample = choose_many(zone_ids, 1, 4) if zone_ids else []
            issued_dt = dt_from_str(emp["created_at"])
            expires_at = None
            lost_at = None
            returned_at = None
            status = "active"
            if emp["employment_status"] == "terminated":
                status = random.choice(["returned", "deactivated", "expired"])
                if maybe(0.7):
                    returned_at = iso_datetime(random_datetime(issued_dt, NOW))
            elif maybe(0.04):
                status = "lost"
                lost_at = iso_datetime(random_datetime(issued_dt, NOW))
            elif maybe(0.1):
                status = "expired"
                expires_at = iso_datetime(issued_dt + timedelta(days=random.randint(365, 1500)))

            table[ref] = {
                "access_card_ref": ref,
                "card_number": f"AC{random.randint(10000000,99999999)}",
                "card_type": random.choice(["employee", "contractor", "temporary", "vip"]),
                "holder_type": "employee",
                "holder_ref": eid,
                "campus_ref": campus_ref,
                "access_zones": access_zone_sample,
                "card_status": status,
                "issued_at": iso_datetime(issued_dt),
                "expires_at": expires_at,
                "lost_at": lost_at,
                "returned_at": returned_at,
                "notes": f"门禁卡发放给员工 {employee_name_map[eid]}，用于园区与办公区访问。",
                "created_at": iso_datetime(issued_dt),
                "updated_at": iso_datetime(random_datetime(issued_dt, NOW)),
            }
            access_card_ids.append(ref)

        # visitor holders
        for vid in visitor_ids[:max(20, len(visitor_ids)//3)]:
            ref = next_id("accesscards")
            camp_ref = choose_one(campus_ids)
            issue_dt = random_datetime(datetime(2023, 1, 1), NOW)
            expire_dt = issue_dt + timedelta(hours=random.randint(4, 48))
            table[ref] = {
                "access_card_ref": ref,
                "card_number": f"VC{random.randint(10000000,99999999)}",
                "card_type": random.choice(["visitor", "temporary", "vip"]),
                "holder_type": "visitor",
                "holder_ref": vid,
                "campus_ref": camp_ref,
                "access_zones": choose_many(zone_ids, 1, 2),
                "card_status": random.choice(["active", "inactive", "returned", "expired"]),
                "issued_at": iso_datetime(issue_dt),
                "expires_at": iso_datetime(expire_dt),
                "lost_at": None,
                "returned_at": iso_datetime(expire_dt + timedelta(hours=random.randint(1, 6))) if maybe(0.5) else None,
                "notes": "访客临时门禁卡，仅限预约授权区域使用。",
                "created_at": iso_datetime(issue_dt),
                "updated_at": iso_datetime(random_datetime(issue_dt, NOW)),
            }
            access_card_ids.append(ref)

        result["access_card"] = table
        available_generated_tables.add("accesscards")

    # --------------------------------------------------------
    # policies
    # --------------------------------------------------------
    elif table_name == "policies":
        table = {}
        policy_titles = [
            ("会议室使用规范", "facility_usage"),
            ("办公设备借用制度", "it_usage"),
            ("访客接待管理办法", "security"),
            ("员工差旅报销规定", "finance"),
            ("餐补管理制度", "meal_allowance"),
            ("园区出入管理规范", "security"),
            ("IT账号与密码安全政策", "it_usage"),
            ("办公区保密与桌面清理制度", "security"),
            ("人事资料使用管理规则", "hr"),
            ("固定资产领用与归还细则", "finance"),
        ]
        for idx, (title, category) in enumerate(policy_titles, start=1):
            ref = next_id("policies")
            owner_dept = choose_one(department_ids)
            author_emp = choose_one(active_employee_ids)
            effective_dt = random_datetime(datetime(2020, 1, 1), datetime(2025, 1, 1))
            expiry_date = None
            status = random.choice(["active", "draft", "expired", "archived", "under_review"])
            if status == "expired":
                expiry_date = iso_date(effective_dt + timedelta(days=random.randint(180, 1200)))
            elif maybe(0.25):
                expiry_date = iso_date(effective_dt + timedelta(days=random.randint(365, 1500)))
            created, updated = created_updated(datetime(2020, 1, 1), NOW)
            table[ref] = {
                "policy_ref": ref,
                "policy_title": title,
                "policy_code": f"POL-{idx:03d}",
                "policy_category": category,
                "content": f"{title}适用于公司园区、办公楼及相关行政管理场景，明确申请、审批、执行、归档等要求。",
                "attachments": choose_many(file_ids, 0, 2),
                "effective_date": iso_date(effective_dt),
                "expiry_date": expiry_date,
                "policy_status": status,
                "owner_department_ref": owner_dept,
                "author_employee_ref": author_emp,
                "version": random.choice(["1.0", "1.1", "2.0", "2.1", "3.0"]),
                "created_at": created,
                "updated_at": updated,
            }
            policy_ids.append(ref)

        result["policy"] = table
        available_generated_tables.add("policies")

    # --------------------------------------------------------
    # canteens
    # --------------------------------------------------------
    elif table_name == "canteens":
        table = {}
        floor_map = result["floor"]
        building_map = result["building"]
        for camp_ref in campus_ids:
            candidate_floors = [
                fref for fref in floor_ids
                if building_map[floor_map[fref]["building_ref"]]["campus_ref"] == camp_ref
            ]
            if not candidate_floors:
                continue
            for i in range(1, 3):
                ref = next_id("canteens")
                floor_ref = choose_one(candidate_floors)
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "canteen_ref": ref,
                    "campus_ref": camp_ref,
                    "floor_ref": floor_ref,
                    "canteen_name": f"{result['campus'][camp_ref]['city']}{random.choice(['员工餐厅', '园区食堂', '轻食餐吧', '国际餐厅'])}{i}",
                    "canteen_type": random.choice(["staff", "executive", "halal", "vegetarian", "international", "other"]),
                    "open_hours": random.choice(["07:00-19:30", "08:00-20:00", "07:30-21:00"]),
                    "seat_capacity": random.randint(80, 300),
                    "canteen_status": random.choice(["active", "active", "under_renovation", "inactive"]),
                    "description": "为员工提供早餐、午餐、晚餐以及部分特色轻食服务。",
                    "created_at": created,
                    "updated_at": updated,
                }
                canteen_ids.append(ref)

        result["canteen"] = table
        available_generated_tables.add("canteens")

    # --------------------------------------------------------
    # workstations
    # --------------------------------------------------------
    elif table_name == "workstations":
        table = {}
        zone_map = result["zone"]
        floor_map = result["floor"]
        building_map = result["building"]
        office_zone_ids = [z for z in zone_ids if zone_map[z]["zone_type"] in ("office", "lounge", "other")]
        employee_assignment_pool = active_employee_ids.copy()
        random.shuffle(employee_assignment_pool)
        assign_idx = 0

        for z_ref in office_zone_ids:
            f_ref = zone_map[z_ref]["floor_ref"]
            b_ref = floor_map[f_ref]["building_ref"]
            c_ref = building_map[b_ref]["campus_ref"]
            ws_count = random.randint(8, 20)
            for i in range(1, ws_count + 1):
                ref = next_id("workstations")
                assigned_emp = None
                assigned_status = random.choice(["available", "available", "reserved", "under_maintenance"])
                assigned_created = datetime(2021, 1, 1)
                if assign_idx < len(employee_assignment_pool) and maybe(0.45):
                    assigned_emp = employee_assignment_pool[assign_idx]
                    assign_idx += 1
                    assigned_status = random.choice(["occupied", "reserved"])
                created, updated = created_updated(assigned_created, NOW)
                table[ref] = {
                    "workstation_ref": ref,
                    "workstation_code": f"{z_ref[-3:]}-WS{i:03d}",
                    "zone_ref": z_ref,
                    "floor_ref": f_ref,
                    "building_ref": b_ref,
                    "campus_ref": c_ref,
                    "workstation_type": random.choice(["fixed", "hot_desk", "standing_desk", "private_office", "other"]),
                    "workstation_status": assigned_status if assigned_emp else assigned_status,
                    "assigned_employee_ref": assigned_emp,
                    "amenities": choose_many(["双显示器", "扩展坞", "升降支架", "人体工学椅", "电话分机", "储物柜"], 1, 3),
                    "description": "标准办公工位，支持个人办公与日常协作。",
                    "created_at": created,
                    "updated_at": updated,
                }
                workstation_ids.append(ref)

        result["workstation"] = table
        available_generated_tables.add("workstations")

    # --------------------------------------------------------
    # lockers
    # --------------------------------------------------------
    elif table_name == "lockers":
        table = {}
        floor_map = result["floor"]
        building_map = result["building"]
        assignable_emps = active_employee_ids.copy()
        random.shuffle(assignable_emps)
        idx_emp = 0

        for z_ref in zone_ids[:max(20, len(zone_ids)//3)]:
            f_ref = result["zone"][z_ref]["floor_ref"]
            b_ref = floor_map[f_ref]["building_ref"]
            c_ref = building_map[b_ref]["campus_ref"]
            for i in range(1, random.randint(8, 15) + 1):
                ref = next_id("lockers")
                assigned = None
                assigned_at = None
                expires_at = None
                status = "available"
                if idx_emp < len(assignable_emps) and maybe(0.4):
                    assigned = assignable_emps[idx_emp]
                    idx_emp += 1
                    assigned_dt = random_datetime(datetime(2022, 1, 1), NOW)
                    assigned_at = iso_datetime(assigned_dt)
                    expires_at = iso_datetime(assigned_dt + timedelta(days=random.randint(90, 365))) if maybe(0.35) else None
                    status = random.choice(["occupied", "reserved"])
                else:
                    status = random.choice(["available", "available", "under_maintenance", "decommissioned"])

                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "locker_ref": ref,
                    "locker_code": f"{z_ref[-3:]}-L{i:03d}",
                    "zone_ref": z_ref,
                    "floor_ref": f_ref,
                    "building_ref": b_ref,
                    "campus_ref": c_ref,
                    "locker_size": random.choice(["small", "medium", "large", "extra_large"]),
                    "locker_status": status,
                    "assigned_employee_ref": assigned,
                    "assigned_at": assigned_at,
                    "expires_at": expires_at,
                    "created_at": created,
                    "updated_at": updated,
                }
                locker_ids.append(ref)

        result["locker"] = table
        available_generated_tables.add("lockers")

    # --------------------------------------------------------
    # cleaningschedules
    # --------------------------------------------------------
    elif table_name == "cleaningschedules":
        table = {}
        floor_map = result["floor"]
        building_map = result["building"]
        for i in range(max(20, len(floor_ids))):
            floor_ref = floor_ids[i % len(floor_ids)]
            building_ref = floor_map[floor_ref]["building_ref"]
            campus_ref = building_map[building_ref]["campus_ref"]
            zone_ref = choose_one(zone_ids) if maybe(0.6) else None
            vendor_ref = choose_one(external_partner_ids) if maybe(0.6) else None
            ref = next_id("cleaningschedules")
            created, updated = created_updated(datetime(2021, 1, 1), NOW)
            table[ref] = {
                "cleaning_schedule_ref": ref,
                "campus_ref": campus_ref,
                "floor_ref": floor_ref,
                "zone_ref": zone_ref,
                "cleaning_type": random.choice(["daily", "deep", "disinfection", "carpet", "window", "other"]),
                "frequency": random.choice(["daily", "weekly", "biweekly", "monthly", "on_demand"]),
                "scheduled_time": random.choice(["06:30", "07:00", "12:30", "18:30", "20:00", "21:00"]),
                "assigned_vendor_ref": vendor_ref,
                "schedule_status": random.choice(["active", "active", "suspended", "cancelled"]),
                "notes": "按园区保洁计划执行，重点覆盖高频使用区域与公共接触面。",
                "created_at": created,
                "updated_at": updated,
            }
            cleaning_schedule_ids.append(ref)

        result["cleaning_schedule"] = table
        available_generated_tables.add("cleaningschedules")

    # --------------------------------------------------------
    # facilities
    # --------------------------------------------------------
    elif table_name == "facilities":
        table = {}
        zone_map = result["zone"]
        floor_map = result["floor"]
        building_map = result["building"]
        facility_types = ["meeting_room", "conference_hall", "phone_booth", "gym", "lounge", "prayer_room", "nursing_room", "recreation_room", "other"]

        suitable_zone_ids = [z for z in zone_ids if zone_map[z]["zone_type"] in ("meeting", "office", "lounge", "gym", "lobby", "other")]
        for z_ref in suitable_zone_ids[:max(40, len(suitable_zone_ids))]:
            f_ref = zone_map[z_ref]["floor_ref"]
            b_ref = floor_map[f_ref]["building_ref"]
            c_ref = building_map[b_ref]["campus_ref"]
            ref = next_id("facilities")
            ftype = random.choice(facility_types)
            created, updated = created_updated(datetime(2021, 1, 1), NOW)
            table[ref] = {
                "facility_ref": ref,
                "facility_name": random.choice(["晨光", "远航", "星辰", "启航", "协同", "智汇", "蓝海", "山河"]) + random.choice(["会议室", "多功能厅", "电话间", "休闲室", "活动室"]),
                "facility_code": f"{b_ref[-3:]}-{z_ref[-3:]}",
                "facility_type": ftype,
                "zone_ref": z_ref,
                "floor_ref": f_ref,
                "building_ref": b_ref,
                "campus_ref": c_ref,
                "capacity": random.randint(2, 120),
                "area_sqm": round(random.uniform(6.0, 300.0), 1),
                "facility_status": random.choice(["available", "available", "reserved", "under_maintenance", "unavailable"]),
                "is_bookable": ftype in ("meeting_room", "conference_hall", "phone_booth", "lounge", "recreation_room"),
                "booking_advance_days": random.randint(3, 30),
                "description": "用于会议、培训、电话沟通、休闲活动或内部协作。",
                "amenities": choose_many(["投影", "白板", "视频会议", "空调", "茶水", "沙发", "音响"], 2, 5),
                "images": choose_many(file_ids, 0, 3),
                "created_at": created,
                "updated_at": updated,
            }
            facility_ids.append(ref)
            facility_booking_windows[ref] = []

        result["facility"] = table
        available_generated_tables.add("facilities")

    # --------------------------------------------------------
    # facilityequipments
    # --------------------------------------------------------
    elif table_name == "facilityequipments":
        table = {}
        for fac_ref in facility_ids:
            equip_count = random.randint(1, 4)
            for _ in range(equip_count):
                ref = next_id("facilityequipments")
                created, updated = created_updated(datetime(2021, 1, 1), NOW)
                table[ref] = {
                    "facility_equipment_ref": ref,
                    "facility_ref": fac_ref,
                    "equipment_name": random.choice(["激光投影仪", "会议电视", "电子白板", "视频会议终端", "空调主机", "无线麦克风", "音响设备", "打印终端"]),
                    "equipment_type": random.choice(["projector", "tv_screen", "whiteboard", "video_conferencing", "air_conditioner", "speaker", "microphone", "computer", "printer", "other"]),
                    "quantity": random.randint(1, 5),
                    "equipment_status": random.choice(["normal", "normal", "faulty", "under_repair", "decommissioned"]),
                    "notes": "设备状态由设施管理员定期巡检并更新。",
                    "created_at": created,
                    "updated_at": updated,
                }

        result["facility_equipment"] = table
        available_generated_tables.add("facilityequipments")

    # --------------------------------------------------------
    # supplyrequests
    # --------------------------------------------------------
    elif table_name == "supplyrequests":
        table = {}
        for _ in range(at_least_2x):
            ref = next_id("supplyrequests")
            requester = choose_one(active_employee_ids)
            dept_ref = employee_department_map.get(requester, choose_one(department_ids))
            req_type = random.choice(["borrow", "consume", "return"])
            item_count = random.randint(1, 3)
            items = []
            for inv_ref in choose_many(inventory_item_pool_for_supply, item_count, item_count):
                items.append({
                    "inventory_item_ref": inv_ref,
                    "quantity": random.randint(1, 10)
                })

            created_dt = random_datetime(datetime(2022, 1, 1), NOW)
            status = random.choice(["pending", "approved", "rejected", "fulfilled", "returned", "cancelled"])
            approved_by = None
            approved_at = None
            reject_reason = None
            fulfilled_at = None
            returned_at = None
            expected_return_at = None

            if req_type == "borrow":
                expected_return_at = iso_date(created_dt + timedelta(days=random.randint(3, 60)))

            if status in ("approved", "fulfilled", "returned"):
                approved_by = choose_one(active_employee_ids[:20])
                approved_at = iso_datetime(created_dt + timedelta(hours=random.randint(1, 72)))
            if status == "rejected":
                reject_reason = random.choice(["库存不足", "用途说明不充分", "不符合领用范围", "预算控制要求"])
            if status in ("fulfilled", "returned"):
                base_dt = dt_from_str(approved_at) if approved_at else created_dt
                fulfilled_at = iso_datetime(base_dt + timedelta(days=random.randint(1, 10)))
            if status == "returned":
                returned_at = iso_datetime(dt_from_str(fulfilled_at) + timedelta(days=random.randint(1, 30)))

            table[ref] = {
                "supply_request_ref": ref,
                "requester_employee_ref": requester,
                "department_ref": dept_ref,
                "request_type": req_type,
                "items": items,
                "reason": random.choice([
                    "新员工入职办公用品补给",
                    "项目会议使用临时物资",
                    "楼层公共区耗材补充",
                    "部门培训活动所需用品",
                    "设备借用用于客户演示",
                ]),
                "expected_return_at": expected_return_at,
                "request_status": status,
                "approved_by_ref": approved_by,
                "approved_at": approved_at,
                "reject_reason": reject_reason,
                "fulfilled_at": fulfilled_at,
                "returned_at": returned_at,
                "notes": "由行政仓统一出库或登记归还。",
                "created_at": iso_datetime(created_dt),
                "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
            }

        result["supply_request"] = table
        available_generated_tables.add("supplyrequests")

    # --------------------------------------------------------
    # complaints
    # --------------------------------------------------------
    elif table_name == "complaints":
        table = {}
        related_resources_pool = facility_ids + canteen_ids + workstation_ids + locker_ids + asset_ids
        for _ in range(at_least_2x):
            ref = next_id("complaints")
            complainant = choose_one(active_employee_ids)
            created_dt = random_datetime(datetime(2022, 1, 1), NOW)
            status = random.choice(["open", "assigned", "in_progress", "resolved", "closed", "rejected"])
            assigned_to = choose_one(active_employee_ids[:20]) if status in ("assigned", "in_progress", "resolved", "closed") else None
            resolved_at = None
            if status in ("resolved", "closed"):
                resolved_at = iso_datetime(created_dt + timedelta(days=random.randint(1, 15)))
            related_ref = choose_one(related_resources_pool) if maybe(0.7) else None
            related_type = None
            if related_ref:
                if related_ref.startswith("FAC"):
                    related_type = "facility"
                elif related_ref.startswith("CAN"):
                    related_type = "canteen"
                elif related_ref.startswith("WS"):
                    related_type = "workstation"
                elif related_ref.startswith("LOCK"):
                    related_type = "locker"
                elif related_ref.startswith("AST"):
                    related_type = "asset"
                else:
                    related_type = "other"
            table[ref] = {
                "complaint_ref": ref,
                "complainant_employee_ref": complainant,
                "complaint_category": random.choice(["canteen", "facility", "security", "it", "hr", "admin", "other"]),
                "related_resource_type": related_type,
                "related_resource_ref": related_ref,
                "title": random.choice([
                    "会议室空调效果不佳",
                    "食堂高峰排队时间过长",
                    "工位网络不稳定",
                    "门禁识别失败频繁",
                    "公共区域清洁不到位",
                    "资产借用流程响应较慢",
                ]),
                "description": zh_sentence(18),
                "attachments": choose_many(file_ids, 0, 3),
                "complaint_status": status,
                "assigned_to_ref": assigned_to,
                "resolved_at": resolved_at,
                "resolution_notes": "" if status in ("open", "assigned", "in_progress") else random.choice([
                    "已完成现场核查并安排整改。",
                    "问题已处理完成，已通知相关责任方复盘。",
                    "经核实后关闭，后续纳入例行巡检。",
                ]),
                "created_at": iso_datetime(created_dt),
                "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
            }

        result["complaint"] = table
        available_generated_tables.add("complaints")

    # --------------------------------------------------------
    # businesscards
    # --------------------------------------------------------
    elif table_name == "businesscards":
        table = {}
        for eid in employee_ids:
            if maybe(0.75):
                ref = next_id("businesscards")
                created_dt = random_datetime(datetime(2022, 1, 1), NOW)
                status = random.choice(["pending", "approved", "rejected", "printing", "delivered", "cancelled"])
                approved_by = None
                approved_at = None
                delivered_at = None
                if status in ("approved", "printing", "delivered"):
                    approved_by = choose_one(active_employee_ids[:20])
                    approved_at = iso_datetime(created_dt + timedelta(days=random.randint(1, 5)))
                if status == "delivered":
                    delivered_at = iso_datetime(dt_from_str(approved_at) + timedelta(days=random.randint(2, 15)))
                table[ref] = {
                    "business_card_ref": ref,
                    "employee_ref": eid,
                    "card_template": random.choice(["standard", "executive", "bilingual", "custom"]),
                    "custom_fields": {
                        "title_override": random.choice(["高级产品经理", "解决方案架构师", "客户成功经理", "资深工程师"]),
                        "wechat": fake.user_name(),
                    } if maybe(0.35) else {},
                    "quantity": random.choice([100, 200, 300, 500]),
                    "request_status": status,
                    "approved_by_ref": approved_by,
                    "approved_at": approved_at,
                    "delivered_at": delivered_at,
                    "notes": "用于客户拜访、会议交流及商务接待场景。",
                    "created_at": iso_datetime(created_dt),
                    "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
                }

        result["business_card"] = table
        available_generated_tables.add("businesscards")

    # --------------------------------------------------------
    # lostfounds
    # --------------------------------------------------------
    elif table_name == "lostfounds":
        table = {}
        refs = []
        for _ in range(at_least_2x):
            ref = next_id("lostfounds")
            record_type = random.choice(["lost", "found"])
            reporter = choose_one(active_employee_ids)
            camp_ref = choose_one(campus_ids)
            occurred_dt = random_datetime(datetime(2022, 1, 1), NOW)
            status = random.choice(["open", "matched", "claimed", "closed"])
            claimed_by = choose_one(active_employee_ids) if status == "claimed" and maybe(0.7) else None
            claimed_at = iso_datetime(occurred_dt + timedelta(days=random.randint(1, 20))) if claimed_by else None
            table[ref] = {
                "lost_found_ref": ref,
                "record_type": record_type,
                "reporter_employee_ref": reporter,
                "item_name": random.choice(["工牌", "水杯", "耳机", "充电器", "笔记本电脑", "雨伞", "门禁卡", "钥匙"]),
                "item_description": zh_sentence(14),
                "item_images": choose_many(file_ids, 0, 3),
                "campus_ref": camp_ref,
                "location_description": random.choice(["1层前台", "会议室外走廊", "餐厅取餐区", "地下一层停车区", "工位区公共桌面"]),
                "occurred_date": iso_date(occurred_dt),
                "matched_ref": None,
                "record_status": status,
                "claimed_by_ref": claimed_by,
                "claimed_at": claimed_at,
                "notes": "由行政前台统一登记并公示。",
                "created_at": iso_datetime(occurred_dt),
                "updated_at": iso_datetime(random_datetime(occurred_dt, NOW)),
            }
            refs.append(ref)

        # set some matched refs
        if len(refs) >= 4:
            for i in range(0, min(20, len(refs)-1), 2):
                if table[refs[i]]["record_type"] != table[refs[i+1]]["record_type"]:
                    table[refs[i]]["matched_ref"] = refs[i+1]
                    table[refs[i+1]]["matched_ref"] = refs[i]
                    if table[refs[i]]["record_status"] == "open":
                        table[refs[i]]["record_status"] = "matched"
                    if table[refs[i+1]]["record_status"] == "open":
                        table[refs[i+1]]["record_status"] = "matched"

        result["lost_found"] = table
        available_generated_tables.add("lostfounds")

    # --------------------------------------------------------
    # securityincidents
    # --------------------------------------------------------
    elif table_name == "securityincidents":
        table = {}
        for _ in range(at_least_2x):
            ref = next_id("securityincidents")
            created_dt = random_datetime(datetime(2022, 1, 1), NOW)
            status = random.choice(["open", "assigned", "in_progress", "resolved", "closed"])
            assigned_to = choose_one(active_employee_ids[:20]) if status != "open" else None
            resolved_at = None
            if status in ("resolved", "closed"):
                resolved_at = iso_datetime(created_dt + timedelta(hours=random.randint(4, 240)))
            table[ref] = {
                "security_incident_ref": ref,
                "reporter_employee_ref": choose_one(active_employee_ids),
                "campus_ref": choose_one(campus_ids),
                "incident_type": random.choice(["intrusion", "theft", "vandalism", "fire", "medical", "safety_hazard", "data_breach", "other"]),
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "title": random.choice([
                    "门禁异常告警",
                    "夜间未授权进入",
                    "办公区物品丢失",
                    "消防通道堆物风险",
                    "员工突发身体不适",
                    "机房访问异常",
                ]),
                "description": zh_sentence(20),
                "occurred_at": iso_datetime(created_dt),
                "location_description": random.choice(["总部园区北门", "A座3层办公区", "B1停车场", "机房门口", "员工餐厅"]),
                "involved_parties": choose_many(list(employee_name_map.values()), 1, 3),
                "attachments": choose_many(file_ids, 0, 3),
                "incident_status": status,
                "assigned_to_ref": assigned_to,
                "resolved_at": resolved_at,
                "resolution_notes": "" if status in ("open", "assigned", "in_progress") else random.choice([
                    "已完成现场处置并记录结案。",
                    "已通知相关部门整改并完成复盘。",
                    "经排查确认风险解除，事件关闭。",
                ]),
                "created_at": iso_datetime(created_dt),
                "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
            }

        result["security_incident"] = table
        available_generated_tables.add("securityincidents")

    # --------------------------------------------------------
    # accesslogs
    # --------------------------------------------------------
    elif table_name == "accesslogs":
        table = {}
        card_map = result["access_card"]
        for _ in range(at_least_2x * 2):
            ref = next_id("accesslogs")
            card_ref = choose_one(access_card_ids)
            camp_ref = card_map[card_ref]["campus_ref"]
            candidate_buildings = [b for b in building_ids if result["building"][b]["campus_ref"] == camp_ref]
            b_ref = choose_one(candidate_buildings) if candidate_buildings else choose_one(building_ids)
            occurred_dt = random_datetime(datetime(2023, 1, 1), NOW)
            result_status = random.choices(["granted", "denied", "error"], weights=[85, 12, 3])[0]
            table[ref] = {
                "access_log_ref": ref,
                "access_card_ref": card_ref,
                "campus_ref": camp_ref,
                "building_ref": b_ref,
                "access_point": random.choice(["北门闸机", "南门闸机", "大厅门禁", "3层玻璃门", "机房门禁", "停车场入口"]),
                "access_direction": random.choice(["in", "out"]),
                "access_result": result_status,
                "occurred_at": iso_datetime(occurred_dt),
                "created_at": iso_datetime(occurred_dt),
            }

        result["access_log"] = table
        available_generated_tables.add("accesslogs")

    # --------------------------------------------------------
    # assetrequests
    # --------------------------------------------------------
    elif table_name == "assetrequests":
        table = {}
        for _ in range(at_least_2x):
            ref = next_id("assetrequests")
            requester = choose_one(active_employee_ids)
            req_type = random.choice(["apply", "borrow", "return", "repair", "scrap", "transfer"])
            asset_ref = choose_one(asset_ids) if req_type in ("borrow", "return", "repair", "scrap", "transfer") else None
            asset_category = result["asset"][asset_ref]["asset_category"] if asset_ref else random.choice(["it_equipment", "furniture", "vehicle", "office_equipment", "lab_equipment", "other"])
            asset_subcategory = result["asset"][asset_ref]["asset_subcategory"] if asset_ref else random.choice(["电脑", "显示设备", "桌椅", "会议设备", "车辆", "测试设备"])
            created_dt = random_datetime(datetime(2022, 1, 1), NOW)
            status = random.choice(["pending", "approved", "rejected", "fulfilled", "cancelled", "returned"])
            approved_by = None
            approved_at = None
            reject_reason = None
            fulfilled_at = None
            expected_return_at = None
            if req_type == "borrow":
                expected_return_at = iso_date(created_dt + timedelta(days=random.randint(7, 90)))
            if status in ("approved", "fulfilled", "returned"):
                approved_by = choose_one(active_employee_ids[:20])
                approved_at = iso_datetime(created_dt + timedelta(hours=random.randint(2, 72)))
            if status == "rejected":
                reject_reason = random.choice(["库存不足", "审批未通过", "用途不明确", "不符合资产领用标准"])
            if status in ("fulfilled", "returned"):
                base_dt = dt_from_str(approved_at) if approved_at else created_dt
                fulfilled_at = iso_datetime(base_dt + timedelta(days=random.randint(1, 14)))

            table[ref] = {
                "asset_request_ref": ref,
                "requester_employee_ref": requester,
                "request_type": req_type,
                "asset_ref": asset_ref,
                "asset_category": asset_category,
                "asset_subcategory": asset_subcategory,
                "quantity": random.randint(1, 3),
                "reason": random.choice([
                    "新项目启动需要设备支持",
                    "员工入职配发办公设备",
                    "原设备故障需返修处理",
                    "资产转移至新团队使用",
                    "资产老化申请报废",
                ]),
                "expected_return_at": expected_return_at,
                "request_status": status,
                "approved_by_ref": approved_by,
                "approved_at": approved_at,
                "reject_reason": reject_reason,
                "fulfilled_at": fulfilled_at,
                "notes": "资产申请由行政资产管理员统一处理。",
                "created_at": iso_datetime(created_dt),
                "updated_at": iso_datetime(random_datetime(created_dt, NOW)),
            }
            asset_request_ids.append(ref)

        result["asset_request"] = table
        available_generated_tables.add("assetrequests")

    # --------------------------------------------------------
    # assettransactions
    # --------------------------------------------------------
    elif table_name == "assettransactions":
        table = {}
        ar_map = result["asset_request"]
        for ar_ref in asset_request_ids:
            ar = ar_map[ar_ref]
            if ar["request_status"] not in ("fulfilled", "returned"):
                continue
            ref = next_id("assettransactions")
            occurred_base = dt_from_str(ar["fulfilled_at"]) if ar["fulfilled_at"] else dt_from_str(ar["created_at"])
            tx_type_map = {
                "apply": "issue",
                "borrow": "issue",
                "return": "return",
                "repair": random.choice(["repair_out", "repair_in"]),
                "scrap": "scrap",
                "transfer": "transfer",
            }
            tx_type = tx_type_map[ar["request_type"]]
            from_emp = None
            to_emp = None
            if tx_type == "issue":
                to_emp = ar["requester_employee_ref"]
            elif tx_type == "return":
                from_emp = ar["requester_employee_ref"]
            elif tx_type == "transfer":
                from_emp = ar["requester_employee_ref"]
                to_emp = choose_one([e for e in active_employee_ids if e != from_emp])

            table[ref] = {
                "asset_transaction_ref": ref,
                "asset_request_ref": ar_ref,
                "asset_ref": ar["asset_ref"] or choose_one(asset_ids),
                "transaction_type": tx_type,
                "from_employee_ref": from_emp,
                "to_employee_ref": to_emp,
                "operated_by_ref": choose_one(active_employee_ids[:20]),
                "occurred_at": iso_datetime(occurred_base + timedelta(hours=random.randint(1, 48))),
                "notes": "资产事务已登记入库，便于后续追溯与盘点。",
                "created_at": iso_datetime(occurred_base + timedelta(hours=random.randint(1, 48))),
            }

        result["asset_transaction"] = table
        available_generated_tables.add("assettransactions")

    # --------------------------------------------------------
    # giftrecords
    # --------------------------------------------------------
    elif table_name == "giftrecords":
        table = {}
        recipient_universe = employee_ids + department_ids + team_ids + visitor_ids + external_partner_ids
        for _ in range(at_least_2x):
            ref = next_id("giftrecords")
            recipient_type = random.choice(["employee", "department", "team", "visitor", "external_partner"])
            if recipient_type == "employee":
                recipient_ref = choose_one(employee_ids)
            elif recipient_type == "department":
                recipient_ref = choose_one(department_ids)
            elif recipient_type == "team":
                recipient_ref = choose_one(team_ids)
            elif recipient_type == "visitor":
                recipient_ref = choose_one(visitor_ids)
            else:
                recipient_ref = choose_one(external_partner_ids)

            created_dt = random_datetime(datetime(2022, 1, 1), NOW)
            table[ref] = {
                "gift_record_ref": ref,
                "gift_ref": choose_one(gift_ids),
                "operated_by_ref": choose_one(active_employee_ids[:20]),
                "recipient_type": recipient_type,
                "recipient_ref": recipient_ref,
                "quantity": random.randint(1, 10),
                "occasion": random.choice(["节日慰问", "客户接待", "周年纪念", "大型活动", "优秀员工表彰", "合作拜访"]),
                "notes": "礼品发放已登记，便于库存核销与活动复盘。",
                "created_at": iso_datetime(created_dt),
            }

        result["gift_record"] = table
        available_generated_tables.add("giftrecords")

    # --------------------------------------------------------
    # canteenmenus
    # --------------------------------------------------------
    elif table_name == "canteenmenus":
        table = {}
        dish_categories = ["主食", "热菜", "凉菜", "汤品", "饮品", "甜点", "水果"]
        dish_names = ["红烧牛肉", "宫保鸡丁", "清炒时蔬", "番茄鸡蛋", "香菇青菜", "酸辣土豆丝", "米饭", "面条", "小米粥", "紫菜蛋花汤", "豆浆", "酸奶", "水果拼盘"]
        for can_ref in canteen_ids:
            for day_offset in range(0, 10):
                menu_date = NOW.date() - timedelta(days=random.randint(0, 60)) + timedelta(days=day_offset)
                for meal_type in ["breakfast", "lunch", "dinner"]:
                    ref = next_id("canteenmenus")
                    dishes = []
                    for _ in range(random.randint(4, 8)):
                        price = money(3, 28)
                        dishes.append({
                            "dish_name": random.choice(dish_names),
                            "category": random.choice(dish_categories),
                            "price": price,
                            "calories": random.randint(80, 900),
                            "is_recommended": maybe(0.2),
                            "is_available": maybe(0.9),
                        })
                    created, updated = created_updated(datetime(2022, 1, 1), NOW)
                    table[ref] = {
                        "canteen_menu_ref": ref,
                        "canteen_ref": can_ref,
                        "menu_date": menu_date.strftime("%Y-%m-%d"),
                        "meal_type": meal_type,
                        "dishes": dishes,
                        "created_at": created,
                        "updated_at": updated,
                    }

        result["canteen_menu"] = table
        available_generated_tables.add("canteenmenus")

    # --------------------------------------------------------
    # bookings
    # --------------------------------------------------------
    elif table_name == "bookings":
        table = {}
        bookable_facilities = [f for f in facility_ids if result["facility"][f]["is_bookable"]]
        if not bookable_facilities:
            bookable_facilities = facility_ids[:]

        for _ in range(at_least_2x):
            ref = next_id("bookings")
            facility_ref = choose_one(bookable_facilities)
            facility = result["facility"][facility_ref]
            booker = choose_one(active_employee_ids)
            attendee_count = random.randint(1, min(12, len(active_employee_ids)))
            attendees = choose_many([e for e in active_employee_ids if e != booker], max(1, attendee_count - 1), max(1, attendee_count - 1))
            attendees = [booker] + attendees[:attendee_count - 1]

            # non-overlapping per facility
            chosen_slot = None
            attempt = 0
            while attempt < 100:
                day = random.randint(-60, 30)
                base_day = NOW + timedelta(days=day)
                start_hour = random.choice([9, 10, 11, 13, 14, 15, 16, 17])
                duration_hours = random.choice([1, 1, 2, 2, 3])
                start_dt = base_day.replace(hour=start_hour, minute=random.choice([0, 30]), second=0, microsecond=0)
                end_dt = start_dt + timedelta(hours=duration_hours)
                conflict = False
                for s0, e0 in facility_booking_windows[facility_ref]:
                    if not (end_dt <= s0 or start_dt >= e0):
                        conflict = True
                        break
                if not conflict:
                    chosen_slot = (start_dt, end_dt)
                    facility_booking_windows[facility_ref].append(chosen_slot)
                    break
                attempt += 1
            if chosen_slot is None:
                start_dt = NOW + timedelta(days=random.randint(1, 20))
                end_dt = start_dt + timedelta(hours=1)
            else:
                start_dt, end_dt = chosen_slot

            if end_dt < NOW:
                status = random.choice(["completed", "completed", "cancelled", "no_show"])
            elif start_dt <= NOW <= end_dt:
                status = random.choice(["confirmed", "confirmed"])
            else:
                status = random.choice(["pending", "confirmed", "cancelled"])

            cancel_reason = None
            cancelled_at = None
            if status == "cancelled":
                cancel_reason = random.choice(["时间调整", "会议取消", "参会人冲突", "场地变更"])
                cancelled_at = iso_datetime(start_dt - timedelta(hours=random.randint(1, 24)))

            table[ref] = {
                "booking_ref": ref,
                "facility_ref": facility_ref,
                "booker_employee_ref": booker,
                "booking_title": random.choice([
                    "项目周会", "需求评审", "面试安排", "部门培训", "客户交流", "季度复盘", "技术分享", "跨团队协同会"
                ]),
                "booking_type": random.choice(["meeting", "interview", "training", "event", "other"]),
                "start_at": iso_datetime(start_dt),
                "end_at": iso_datetime(end_dt),
                "attendee_count": len(attendees),
                "attendee_employee_refs": attendees,
                "booking_status": status,
                "cancel_reason": cancel_reason,
                "cancelled_at": cancelled_at,
                "notes": "会议预订请按时签到，并保持会议室整洁有序。",
                "created_at": iso_datetime(start_dt - timedelta(days=random.randint(1, 10))),
                "updated_at": iso_datetime(random_datetime(start_dt - timedelta(days=random.randint(1, 10)), NOW if NOW > start_dt else start_dt)),
            }
            booking_ids.append(ref)

        result["booking"] = table
        available_generated_tables.add("bookings")

    # --------------------------------------------------------
    # visitorappointments
    # --------------------------------------------------------
    elif table_name == "visitorappointments":
        table = {}
        for _ in range(at_least_2x):
            ref = next_id("visitorappointments")
            visitor_ref = choose_one(visitor_ids)
            host = choose_one(active_employee_ids)
            campus_ref = choose_one(campus_ids)
            candidate_facilities = [f for f in facility_ids if result["facility"][f]["campus_ref"] == campus_ref]
            facility_ref = choose_one(candidate_facilities) if maybe(0.6) and candidate_facilities else None
            start_dt = random_datetime(datetime(2023, 1, 1), NOW + timedelta(days=30))
            end_dt = start_dt + timedelta(hours=random.randint(1, 8))
            status = random.choice(["pending", "approved", "rejected", "checked_in", "checked_out", "expired", "cancelled"])
            checkin = None
            checkout = None
            if status in ("checked_in", "checked_out"):
                checkin_dt = start_dt + timedelta(minutes=random.randint(-15, 30))
                checkin = iso_datetime(checkin_dt)
                if status == "checked_out":
                    checkout = iso_datetime(checkin_dt + timedelta(hours=random.randint(1, 6)))
            table[ref] = {
                "visitor_appointment_ref": ref,
                "visitor_ref": visitor_ref,
                "host_employee_ref": host,
                "campus_ref": campus_ref,
                "visit_purpose": random.choice(["商务洽谈", "面试来访", "设备维护", "政府检查", "送货交接", "个人来访"]),
                "visit_type": random.choice(["business", "interview", "delivery", "maintenance", "government", "personal", "other"]),
                "scheduled_start_at": iso_datetime(start_dt),
                "scheduled_end_at": iso_datetime(end_dt),
                "actual_checkin_at": checkin,
                "actual_checkout_at": checkout,
                "facility_ref": facility_ref,
                "temp_access_level": random.choice(["lobby", "floor", "zone", "full"]),
                "appointment_status": status,
                "notes": "访客需在前台登记并由接待人确认后入场。",
                "created_at": iso_datetime(start_dt - timedelta(days=random.randint(1, 7))),
                "updated_at": iso_datetime(random_datetime(start_dt - timedelta(days=random.randint(1, 7)), NOW if NOW > start_dt else start_dt)),
            }

        result["visitor_appointment"] = table
        available_generated_tables.add("visitorappointments")

    # --------------------------------------------------------
    # companyevents
    # --------------------------------------------------------
    elif table_name == "companyevents":
        table = {}
        for _ in range(max(20, SCALE // 3)):
            ref = next_id("companyevents")
            campus_ref = choose_one(campus_ids)
            candidate_facilities = [f for f in facility_ids if result["facility"][f]["campus_ref"] == campus_ref]
            facility_ref = choose_one(candidate_facilities) if maybe(0.75) else None
            organizer = choose_one(active_employee_ids[:30])
            dept_ref = choose_one(department_ids) if maybe(0.6) else None
            start_dt = random_datetime(datetime(2023, 1, 1), NOW + timedelta(days=90))
            end_dt = start_dt + timedelta(hours=random.randint(2, 8))
            if end_dt < NOW:
                status = random.choice(["completed", "completed", "cancelled"])
            elif start_dt <= NOW <= end_dt:
                status = "ongoing"
            else:
                status = random.choice(["planned", "planned", "cancelled", "postponed"])
            table[ref] = {
                "company_event_ref": ref,
                "event_name": random.choice([
                    "年度团建日", "新员工训练营", "技术公开课", "管理者工作坊", "健康运动节", "企业文化周", "公益志愿日", "季度表彰大会"
                ]),
                "event_type": random.choice(["company_day", "team_building", "training", "seminar", "celebration", "sports", "charity", "other"]),
                "campus_ref": campus_ref,
                "facility_ref": facility_ref,
                "organizer_employee_ref": organizer,
                "department_ref": dept_ref,
                "start_at": iso_datetime(start_dt),
                "end_at": iso_datetime(end_dt),
                "max_attendees": random.choice([30, 50, 80, 100, 150, None]),
                "description": "面向员工或部门组织的内部活动，用于培训、文化建设、协同交流和员工关怀。",
                "attachments": choose_many(file_ids, 0, 3),
                "event_status": status,
                "created_at": iso_datetime(start_dt - timedelta(days=random.randint(5, 30))),
                "updated_at": iso_datetime(random_datetime(start_dt - timedelta(days=random.randint(5, 30)), NOW if NOW > start_dt else start_dt)),
            }
            company_event_ids.append(ref)

        result["company_event"] = table
        available_generated_tables.add("companyevents")

    # --------------------------------------------------------
    # eventregistrations
    # --------------------------------------------------------
    elif table_name == "eventregistrations":
        table = {}
        for evt_ref in company_event_ids:
            evt = result["company_event"][evt_ref]
            participants = choose_many(active_employee_ids, 5, min(20, len(active_employee_ids)))
            for emp_ref in participants:
                ref = next_id("eventregistrations")
                status = random.choice(["registered", "cancelled", "attended", "no_show", "waitlisted"])
                checked_in_at = None
                if status == "attended":
                    checked_in_at = iso_datetime(dt_from_str(evt["start_at"]) + timedelta(minutes=random.randint(-10, 60)))
                created_dt = dt_from_str(evt["created_at"])
                table[ref] = {
                    "event_registration_ref": ref,
                    "company_event_ref": evt_ref,
                    "employee_ref": emp_ref,
                    "registration_status": status,
                    "checked_in_at": checked_in_at,
                    "notes": "活动报名记录由系统自动登记。",
                    "created_at": iso_datetime(created_dt + timedelta(hours=random.randint(1, 72))),
                    "updated_at": iso_datetime(random_datetime(created_dt, NOW if NOW > created_dt else created_dt)),
                }

        result["event_registration"] = table
        available_generated_tables.add("eventregistrations")

    # --------------------------------------------------------
    # shuttlebookings
    # --------------------------------------------------------
    elif table_name == "shuttlebookings":
        table = {}
        stop_by_route = {}
        for sref, stop in result["shuttle_stop"].items():
            stop_by_route.setdefault(stop["shuttle_route_ref"], []).append(sref)

        for _ in range(at_least_2x):
            ref = next_id("shuttlebookings")
            schedule_ref = choose_one(shuttle_schedule_ids)
            route_ref = result["shuttle_schedule"][schedule_ref]["shuttle_route_ref"]
            stop_ref = choose_one(stop_by_route.get(route_ref, shuttle_stop_ids))
            ride_dt = random_datetime(datetime(2024, 1, 1), NOW + timedelta(days=15))
            status = random.choice(["confirmed", "cancelled", "completed", "no_show"])
            table[ref] = {
                "shuttle_booking_ref": ref,
                "shuttle_schedule_ref": schedule_ref,
                "employee_ref": choose_one(active_employee_ids),
                "ride_date": iso_date(ride_dt),
                "boarding_stop_ref": stop_ref,
                "booking_status": status,
                "created_at": iso_datetime(ride_dt - timedelta(days=random.randint(1, 10))),
                "updated_at": iso_datetime(random_datetime(ride_dt - timedelta(days=random.randint(1, 10)), NOW if NOW > ride_dt else ride_dt)),
            }

        result["shuttle_booking"] = table
        available_generated_tables.add("shuttlebookings")

    # --------------------------------------------------------
    # cleaningrecords
    # --------------------------------------------------------
    elif table_name == "cleaningrecords":
        table = {}
        for cls_ref in cleaning_schedule_ids:
            for _ in range(random.randint(2, 6)):
                ref = next_id("cleaningrecords")
                exec_dt = random_datetime(datetime(2024, 1, 1), NOW)
                table[ref] = {
                    "cleaning_record_ref": ref,
                    "cleaning_schedule_ref": cls_ref,
                    "executed_by": random.choice(["园区保洁A组", "园区保洁B组", "深度清洁专项组", "消杀服务团队", fake.name()]),
                    "executed_at": iso_datetime(exec_dt),
                    "result": random.choice(["completed", "completed", "partial", "skipped", "failed"]),
                    "notes": random.choice([
                        "已按标准完成保洁。",
                        "局部区域被占用，未完全覆盖。",
                        "因临时活动调整执行时间。",
                        "发现设施问题已同步报修。",
                    ]),
                    "created_at": iso_datetime(exec_dt),
                }

        result["cleaning_record"] = table
        available_generated_tables.add("cleaningrecords")

# ------------------------------------------------------------
# 7. Final schema-key mapping for output
#    Output must use singular keys matching Pydantic model names.
# ------------------------------------------------------------
final_output = {
    "campus": result.get("campus", {}),
    "building": result.get("building", {}),
    "floor": result.get("floor", {}),
    "zone": result.get("zone", {}),
    "facility": result.get("facility", {}),
    "facility_equipment": result.get("facility_equipment", {}),
    "booking": result.get("booking", {}),
    "workstation": result.get("workstation", {}),
    "locker": result.get("locker", {}),
    "parking_space": result.get("parking_space", {}),
    "ev_charger": result.get("ev_charger", {}),
    "shuttle_route": result.get("shuttle_route", {}),
    "shuttle_stop": result.get("shuttle_stop", {}),
    "shuttle_schedule": result.get("shuttle_schedule", {}),
    "shuttle_booking": result.get("shuttle_booking", {}),
    "canteen": result.get("canteen", {}),
    "canteen_menu": result.get("canteen_menu", {}),
    "visitor": result.get("visitor", {}),
    "visitor_appointment": result.get("visitor_appointment", {}),
    "access_card": result.get("access_card", {}),
    "access_log": result.get("access_log", {}),
    "badge": result.get("badge", {}),
    "asset": result.get("asset", {}),
    "asset_request": result.get("asset_request", {}),
    "asset_transaction": result.get("asset_transaction", {}),
    "inventory_item": result.get("inventory_item", {}),
    "supply_request": result.get("supply_request", {}),
    "repair_request": {},  # optional empty if not generated
    "complaint": result.get("complaint", {}),
    "lost_found": result.get("lost_found", {}),
    "security_incident": result.get("security_incident", {}),
    "gift": result.get("gift", {}),
    "gift_record": result.get("gift_record", {}),
    "business_card": result.get("business_card", {}),
    "company_event": result.get("company_event", {}),
    "event_registration": result.get("event_registration", {}),
    "policy": result.get("policy", {}),
    "service_directory": result.get("service_directory", {}),
    "external_partner": result.get("external_partner", {}),
    "travel_policy": result.get("travel_policy", {}),
    "cleaning_schedule": result.get("cleaning_schedule", {}),
    "cleaning_record": result.get("cleaning_record", {}),
}

print(json.dumps(final_output, ensure_ascii=False, indent=2))