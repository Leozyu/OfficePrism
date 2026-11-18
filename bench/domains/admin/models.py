from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.environment.db import DB
from bench.domains.base.models import OfficeDB


# --- Enum Literal types for ADMIN domain ---

CampusType = Literal["headquarters", "branch", "r&d_center", "manufacturing", "warehouse", "other"]
CampusStatus = Literal["active", "inactive", "closed", "under_construction"]

BuildingStatus = Literal["active", "inactive", "under_renovation", "demolished"]

FloorStatus = Literal["active", "inactive", "under_renovation"]

ZoneType = Literal["office", "meeting", "lounge", "storage", "cafeteria", "gym", "parking", "lobby", "server_room", "other"]
ZoneStatus = Literal["active", "inactive", "under_renovation"]

FacilityType = Literal["meeting_room", "conference_hall", "phone_booth", "gym", "lounge", "prayer_room", "nursing_room", "recreation_room", "other"]
FacilityStatus = Literal["available", "unavailable", "under_maintenance", "reserved", "decommissioned"]

EquipmentType = Literal["projector", "tv_screen", "whiteboard", "video_conferencing", "air_conditioner", "speaker", "microphone", "computer", "printer", "other"]
EquipmentStatus = Literal["normal", "faulty", "under_repair", "decommissioned"]

BookingType = Literal["meeting", "interview", "training", "event", "other"]
BookingStatus = Literal["pending", "confirmed", "cancelled", "completed", "no_show"]

WorkstationType = Literal["fixed", "hot_desk", "standing_desk", "private_office", "other"]
WorkstationStatus = Literal["available", "occupied", "reserved", "under_maintenance", "decommissioned"]

LockerSize = Literal["small", "medium", "large", "extra_large"]
LockerStatus = Literal["available", "occupied", "reserved", "under_maintenance", "decommissioned"]

SpaceType = Literal["standard", "compact", "large", "disabled", "ev_only", "vip"]
ParkingSpaceStatus = Literal["available", "occupied", "reserved", "under_maintenance", "decommissioned"]

ChargerType = Literal["ac_slow", "ac_fast", "dc_fast", "super_fast"]
ChargerStatus = Literal["available", "in_use", "faulty", "under_maintenance", "decommissioned"]

ShuttleDirection = Literal["inbound", "outbound", "circular"]
ShuttleRouteStatus = Literal["active", "suspended", "cancelled"]

ShuttleScheduleStatus = Literal["active", "suspended", "cancelled"]

EffectiveDay = Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

ShuttleBookingStatus = Literal["confirmed", "cancelled", "completed", "no_show"]

CanteenType = Literal["staff", "executive", "halal", "vegetarian", "international", "other"]
CanteenStatus = Literal["active", "inactive", "under_renovation", "closed"]

MealType = Literal["breakfast", "lunch", "dinner", "afternoon_tea", "supper"]

VisitorIdType = Literal["id_card", "passport", "driver_license", "other"]
VisitorType = Literal["business", "government", "contractor", "personal", "other"]

VisitType = Literal["business", "interview", "delivery", "maintenance", "government", "personal", "other"]
TempAccessLevel = Literal["lobby", "floor", "zone", "full"]
AppointmentStatus = Literal["pending", "approved", "rejected", "checked_in", "checked_out", "expired", "cancelled"]

CardType = Literal["employee", "visitor", "contractor", "temporary", "vip"]
HolderType = Literal["employee", "visitor", "contractor"]
CardStatus = Literal["active", "inactive", "lost", "expired", "returned", "deactivated"]

AccessDirection = Literal["in", "out"]
AccessResult = Literal["granted", "denied", "error"]

BadgeType = Literal["standard", "executive", "contractor", "intern", "visitor"]
BadgeStatus = Literal["active", "inactive", "lost", "expired", "returned"]

AssetCategory = Literal["it_equipment", "furniture", "vehicle", "office_equipment", "lab_equipment", "other"]
AssetStatus = Literal["in_use", "available", "under_repair", "scrapped", "lost", "reserved", "in_transit"]

AssetRequestType = Literal["apply", "borrow", "return", "repair", "scrap", "transfer"]
AssetRequestStatus = Literal["pending", "approved", "rejected", "fulfilled", "cancelled", "returned"]

AssetTransactionType = Literal["issue", "return", "transfer", "repair_out", "repair_in", "scrap"]

ItemCategory = Literal["office_supply", "cleaning_supply", "it_accessory", "kitchen_supply", "safety_equipment", "other"]
ItemStatus = Literal["active", "inactive", "discontinued"]

SupplyRequestType = Literal["borrow", "consume", "return"]
SupplyRequestStatus = Literal["pending", "approved", "rejected", "fulfilled", "returned", "cancelled"]

ResourceType = Literal["facility", "workstation", "equipment", "building", "zone", "other"]
RepairUrgency = Literal["low", "normal", "high", "critical"]
RepairStatus = Literal["pending", "assigned", "in_progress", "completed", "cancelled", "on_hold"]

ComplaintCategory = Literal["canteen", "facility", "security", "it", "hr", "admin", "other"]
ComplaintStatus = Literal["open", "assigned", "in_progress", "resolved", "closed", "rejected"]

LostFoundRecordType = Literal["lost", "found"]
LostFoundStatus = Literal["open", "matched", "claimed", "closed"]

SecurityIncidentType = Literal["intrusion", "theft", "vandalism", "fire", "medical", "safety_hazard", "data_breach", "other"]
IncidentSeverity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["open", "assigned", "in_progress", "resolved", "closed"]

GiftStatus = Literal["active", "inactive", "discontinued"]

RecipientType = Literal["employee", "department", "team", "visitor", "external_partner"]

CardTemplate = Literal["standard", "executive", "bilingual", "custom"]
BusinessCardRequestStatus = Literal["pending", "approved", "rejected", "printing", "delivered", "cancelled"]

CompanyEventType = Literal["company_day", "team_building", "training", "seminar", "celebration", "sports", "charity", "other"]
EventStatus = Literal["planned", "ongoing", "completed", "cancelled", "postponed"]

EventRegistrationStatus = Literal["registered", "cancelled", "attended", "no_show", "waitlisted"]

PolicyCategory = Literal["meal_allowance", "travel", "it_usage", "security", "facility_usage", "hr", "finance", "other"]
PolicyStatus = Literal["active", "draft", "expired", "archived", "under_review"]

ServiceCategory = Literal["admin", "it", "hr", "finance", "legal", "security", "facility", "canteen", "other"]
ServiceStatus = Literal["active", "inactive", "suspended"]

PartnerType = Literal["supplier", "vendor", "contractor", "service_provider", "logistics", "other"]
PartnerStatus = Literal["active", "inactive", "suspended", "blacklisted"]

CityTier = Literal["tier1", "tier2", "tier3", "international"]
TransportClass = Literal["economy", "business", "first", "high_speed_rail_second", "high_speed_rail_first"]
TravelPolicyStatus = Literal["active", "inactive", "expired", "draft"]

CleaningType = Literal["daily", "deep", "disinfection", "carpet", "window", "other"]
CleaningFrequency = Literal["daily", "weekly", "biweekly", "monthly", "on_demand"]
CleaningScheduleStatus = Literal["active", "suspended", "cancelled"]

CleaningResult = Literal["completed", "partial", "skipped", "failed"]


# --- ADMIN Models ---


class Campus(BaseModel):
    """Represents a physical campus location with geographic and status information"""

    campus_ref: str = Field(description="Unique identifier for the campus")
    campus_name: str = Field(description="Name of the campus")
    campus_code: str = Field(description="Short code for the campus")
    campus_type: CampusType = Field(
        description="Type of campus (headquarters, branch, r&d_center, manufacturing, warehouse, other)"
    )
    campus_status: CampusStatus = Field(
        description="Current status of the campus (active, inactive, closed, under_construction)"
    )
    address: str = Field(description="Full street address of the campus")
    city: str = Field(description="City where the campus is located")
    country: str = Field(description="Country code where the campus is located (e.g., CN, US)")
    geo_lat: float = Field(description="Geographic latitude coordinate of the campus")
    geo_lng: float = Field(description="Geographic longitude coordinate of the campus")
    map_file_ref: Optional[str] = Field(
        description="Reference to the file attachment used as campus map, null if not set",
        default=None,
    )
    description: str = Field(description="Description of the campus")
    created_at: str = Field(description="Timestamp when the campus record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the campus record was last updated (ISO 8601)")


class Building(BaseModel):
    """Represents a building within a campus"""

    building_ref: str = Field(description="Unique identifier for the building")
    campus_ref: str = Field(description="Reference to the campus this building belongs to")
    building_name: str = Field(description="Name of the building")
    building_code: str = Field(description="Short code for the building")
    floor_count: int = Field(description="Total number of floors in the building")
    building_status: BuildingStatus = Field(
        description="Current status of the building (active, inactive, under_renovation, demolished)"
    )
    description: str = Field(description="Description of the building")
    created_at: str = Field(description="Timestamp when the building record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the building record was last updated (ISO 8601)")


class Floor(BaseModel):
    """Represents a floor within a building"""

    floor_ref: str = Field(description="Unique identifier for the floor")
    building_ref: str = Field(description="Reference to the building this floor belongs to")
    floor_number: int = Field(description="Numeric floor number (e.g., 1, 2, -1 for basement)")
    floor_name: str = Field(description="Display name for the floor (e.g., 1F, B1, Lobby)")
    floor_plan_file_ref: Optional[str] = Field(
        description="Reference to the file attachment used as floor plan, null if not set",
        default=None,
    )
    floor_status: FloorStatus = Field(
        description="Current status of the floor (active, inactive, under_renovation)"
    )
    created_at: str = Field(description="Timestamp when the floor record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the floor record was last updated (ISO 8601)")


class Zone(BaseModel):
    """Represents a functional zone within a floor"""

    zone_ref: str = Field(description="Unique identifier for the zone")
    floor_ref: str = Field(description="Reference to the floor this zone belongs to")
    zone_name: str = Field(description="Name of the zone")
    zone_code: str = Field(description="Short code for the zone")
    zone_type: ZoneType = Field(
        description="Type of zone (office, meeting, lounge, storage, cafeteria, gym, parking, lobby, server_room, other)"
    )
    zone_status: ZoneStatus = Field(
        description="Current status of the zone (active, inactive, under_renovation)"
    )
    description: str = Field(description="Description of the zone's purpose")
    created_at: str = Field(description="Timestamp when the zone record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the zone record was last updated (ISO 8601)")


class Facility(BaseModel):
    """Represents a bookable or managed facility such as a meeting room or conference hall"""

    facility_ref: str = Field(description="Unique identifier for the facility")
    facility_name: str = Field(description="Name of the facility")
    facility_code: str = Field(description="Short code for the facility")
    facility_type: FacilityType = Field(
        description="Type of facility (meeting_room, conference_hall, phone_booth, gym, lounge, prayer_room, nursing_room, recreation_room, other)"
    )
    zone_ref: str = Field(description="Reference to the zone this facility is located in")
    floor_ref: str = Field(description="Reference to the floor this facility is located on")
    building_ref: str = Field(description="Reference to the building this facility is located in")
    campus_ref: str = Field(description="Reference to the campus this facility is located at")
    capacity: int = Field(description="Maximum number of people the facility can accommodate")
    area_sqm: float = Field(description="Area of the facility in square meters")
    facility_status: FacilityStatus = Field(
        description="Current status of the facility (available, unavailable, under_maintenance, reserved, decommissioned)"
    )
    is_bookable: bool = Field(description="Whether the facility can be booked by employees")
    booking_advance_days: int = Field(
        description="Maximum number of days in advance the facility can be booked"
    )
    description: str = Field(description="Description of the facility")
    amenities: List[str] = Field(description="List of amenities available in the facility")
    images: List[str] = Field(
        description="List of file attachment references for facility images"
    )
    created_at: str = Field(description="Timestamp when the facility record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the facility record was last updated (ISO 8601)")


class FacilityEquipment(BaseModel):
    """Represents a piece of equipment installed in a facility"""

    facility_equipment_ref: str = Field(description="Unique identifier for the facility equipment record")
    facility_ref: str = Field(description="Reference to the facility this equipment belongs to")
    equipment_name: str = Field(description="Name of the equipment")
    equipment_type: EquipmentType = Field(
        description="Type of equipment (projector, tv_screen, whiteboard, video_conferencing, air_conditioner, speaker, microphone, computer, printer, other)"
    )
    quantity: int = Field(description="Number of units of this equipment in the facility")
    equipment_status: EquipmentStatus = Field(
        description="Current status of the equipment (normal, faulty, under_repair, decommissioned)"
    )
    notes: str = Field(description="Additional notes about the equipment")
    created_at: str = Field(description="Timestamp when the equipment record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the equipment record was last updated (ISO 8601)")


class Booking(BaseModel):
    """Represents a facility booking made by an employee"""

    booking_ref: str = Field(description="Unique identifier for the booking")
    facility_ref: str = Field(description="Reference to the facility being booked")
    booker_employee_ref: str = Field(description="Employee reference of the person making the booking")
    booking_title: str = Field(description="Title or subject of the booking")
    booking_type: BookingType = Field(
        description="Type of booking (meeting, interview, training, event, other)"
    )
    start_at: str = Field(description="Timestamp when the booking starts (ISO 8601)")
    end_at: str = Field(description="Timestamp when the booking ends (ISO 8601)")
    attendee_count: int = Field(description="Expected number of attendees")
    attendee_employee_refs: List[str] = Field(
        description="List of employee references for expected attendees"
    )
    booking_status: BookingStatus = Field(
        description="Current status of the booking (pending, confirmed, cancelled, completed, no_show)"
    )
    cancel_reason: Optional[str] = Field(
        description="Reason for cancellation, null if not cancelled",
        default=None,
    )
    cancelled_at: Optional[str] = Field(
        description="Timestamp when the booking was cancelled, null if not cancelled (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the booking")
    created_at: str = Field(description="Timestamp when the booking record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the booking record was last updated (ISO 8601)")


class Workstation(BaseModel):
    """Represents a workstation or desk within a zone"""

    workstation_ref: str = Field(description="Unique identifier for the workstation")
    workstation_code: str = Field(description="Short code or label for the workstation")
    zone_ref: str = Field(description="Reference to the zone this workstation is located in")
    floor_ref: str = Field(description="Reference to the floor this workstation is located on")
    building_ref: str = Field(description="Reference to the building this workstation is located in")
    campus_ref: str = Field(description="Reference to the campus this workstation is located at")
    workstation_type: WorkstationType = Field(
        description="Type of workstation (fixed, hot_desk, standing_desk, private_office, other)"
    )
    workstation_status: WorkstationStatus = Field(
        description="Current status of the workstation (available, occupied, reserved, under_maintenance, decommissioned)"
    )
    assigned_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned employee, null if unassigned",
        default=None,
    )
    amenities: List[str] = Field(description="List of amenities available at this workstation")
    description: str = Field(description="Description of the workstation")
    created_at: str = Field(description="Timestamp when the workstation record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the workstation record was last updated (ISO 8601)")


class Locker(BaseModel):
    """Represents a storage locker assigned to or available for employees"""

    locker_ref: str = Field(description="Unique identifier for the locker")
    locker_code: str = Field(description="Short code or label for the locker")
    zone_ref: str = Field(description="Reference to the zone this locker is located in")
    floor_ref: str = Field(description="Reference to the floor this locker is located on")
    building_ref: str = Field(description="Reference to the building this locker is located in")
    campus_ref: str = Field(description="Reference to the campus this locker is located at")
    locker_size: LockerSize = Field(
        description="Size of the locker (small, medium, large, extra_large)"
    )
    locker_status: LockerStatus = Field(
        description="Current status of the locker (available, occupied, reserved, under_maintenance, decommissioned)"
    )
    assigned_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned employee, null if unassigned",
        default=None,
    )
    assigned_at: Optional[str] = Field(
        description="Timestamp when the locker was assigned, null if unassigned (ISO 8601)",
        default=None,
    )
    expires_at: Optional[str] = Field(
        description="Timestamp when the locker assignment expires, null if no expiration (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the locker record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the locker record was last updated (ISO 8601)")


class ParkingSpace(BaseModel):
    """Represents a parking space within a campus"""

    parking_space_ref: str = Field(description="Unique identifier for the parking space")
    space_code: str = Field(description="Short code or label for the parking space")
    campus_ref: str = Field(description="Reference to the campus this parking space belongs to")
    parking_zone: str = Field(description="Parking zone or area designation within the campus")
    space_type: SpaceType = Field(
        description="Type of parking space (standard, compact, large, disabled, ev_only, vip)"
    )
    ev_charging: bool = Field(description="Whether the parking space has EV charging capability")
    space_status: ParkingSpaceStatus = Field(
        description="Current status of the parking space (available, occupied, reserved, under_maintenance, decommissioned)"
    )
    assigned_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned employee, null if unassigned",
        default=None,
    )
    assigned_at: Optional[str] = Field(
        description="Timestamp when the space was assigned, null if unassigned (ISO 8601)",
        default=None,
    )
    expires_at: Optional[str] = Field(
        description="Timestamp when the parking assignment expires, null if no expiration (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the parking space record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the parking space record was last updated (ISO 8601)")


class EvCharger(BaseModel):
    """Represents an EV charging station associated with a parking space"""

    ev_charger_ref: str = Field(description="Unique identifier for the EV charger")
    charger_code: str = Field(description="Short code or label for the EV charger")
    campus_ref: str = Field(description="Reference to the campus this EV charger is located at")
    parking_space_ref: str = Field(description="Reference to the parking space this charger is installed at")
    charger_type: ChargerType = Field(
        description="Type of charger (ac_slow, ac_fast, dc_fast, super_fast)"
    )
    power_kw: float = Field(description="Power output of the charger in kilowatts")
    charger_status: ChargerStatus = Field(
        description="Current status of the charger (available, in_use, faulty, under_maintenance, decommissioned)"
    )
    fee_per_kwh: float = Field(description="Charging fee per kilowatt-hour in local currency")
    operator: str = Field(description="Name of the operator or vendor managing the charger")
    created_at: str = Field(description="Timestamp when the EV charger record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the EV charger record was last updated (ISO 8601)")


class ShuttleRoute(BaseModel):
    """Represents a shuttle bus route serving a campus"""

    shuttle_route_ref: str = Field(description="Unique identifier for the shuttle route")
    route_name: str = Field(description="Name of the shuttle route")
    route_code: str = Field(description="Short code for the shuttle route")
    campus_ref: str = Field(description="Reference to the campus this shuttle route serves")
    direction: ShuttleDirection = Field(
        description="Direction of the shuttle route (inbound, outbound, circular)"
    )
    route_status: ShuttleRouteStatus = Field(
        description="Current status of the shuttle route (active, suspended, cancelled)"
    )
    description: str = Field(description="Description of the shuttle route")
    created_at: str = Field(description="Timestamp when the shuttle route record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the shuttle route record was last updated (ISO 8601)")


class ShuttleStop(BaseModel):
    """Represents a stop along a shuttle route"""

    shuttle_stop_ref: str = Field(description="Unique identifier for the shuttle stop")
    shuttle_route_ref: str = Field(description="Reference to the shuttle route this stop belongs to")
    stop_name: str = Field(description="Name of the shuttle stop")
    stop_order: int = Field(description="Sequential order of this stop along the route")
    geo_lat: float = Field(description="Geographic latitude coordinate of the stop")
    geo_lng: float = Field(description="Geographic longitude coordinate of the stop")
    created_at: str = Field(description="Timestamp when the shuttle stop record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the shuttle stop record was last updated (ISO 8601)")


class ShuttleSchedule(BaseModel):
    """Represents a scheduled shuttle departure for a route"""

    shuttle_schedule_ref: str = Field(description="Unique identifier for the shuttle schedule")
    shuttle_route_ref: str = Field(description="Reference to the shuttle route this schedule belongs to")
    depart_time: str = Field(description="Departure time in HH:MM format")
    effective_days: List[EffectiveDay] = Field(
        description="List of days this schedule is effective (mon, tue, wed, thu, fri, sat, sun)"
    )
    seat_capacity: int = Field(description="Total seat capacity for this scheduled departure")
    schedule_status: ShuttleScheduleStatus = Field(
        description="Current status of the schedule (active, suspended, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the schedule record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the schedule record was last updated (ISO 8601)")


class ShuttleBooking(BaseModel):
    """Represents an employee's booking for a shuttle schedule on a specific date"""

    shuttle_booking_ref: str = Field(description="Unique identifier for the shuttle booking")
    shuttle_schedule_ref: str = Field(description="Reference to the shuttle schedule being booked")
    employee_ref: str = Field(description="Reference to the employee making the booking")
    ride_date: str = Field(description="Date of the shuttle ride (ISO 8601 date)")
    boarding_stop_ref: str = Field(description="Reference to the shuttle stop where the employee will board")
    booking_status: ShuttleBookingStatus = Field(
        description="Current status of the shuttle booking (confirmed, cancelled, completed, no_show)"
    )
    created_at: str = Field(description="Timestamp when the shuttle booking record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the shuttle booking record was last updated (ISO 8601)")


class Canteen(BaseModel):
    """Represents a canteen or cafeteria within a campus"""

    canteen_ref: str = Field(description="Unique identifier for the canteen")
    campus_ref: str = Field(description="Reference to the campus this canteen is located at")
    floor_ref: str = Field(description="Reference to the floor this canteen is located on")
    canteen_name: str = Field(description="Name of the canteen")
    canteen_type: CanteenType = Field(
        description="Type of canteen (staff, executive, halal, vegetarian, international, other)"
    )
    open_hours: str = Field(description="Operating hours of the canteen (e.g., 07:00-21:00)")
    seat_capacity: int = Field(description="Total seating capacity of the canteen")
    canteen_status: CanteenStatus = Field(
        description="Current status of the canteen (active, inactive, under_renovation, closed)"
    )
    description: str = Field(description="Description of the canteen")
    created_at: str = Field(description="Timestamp when the canteen record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the canteen record was last updated (ISO 8601)")


class DishItem(BaseModel):
    """Represents a single dish item within a canteen menu"""

    dish_name: str = Field(description="Name of the dish")
    category: str = Field(description="Category of the dish (e.g., main course, soup, dessert)")
    price: float = Field(description="Price of the dish in local currency")
    calories: int = Field(description="Caloric content of the dish in kcal")
    is_recommended: bool = Field(description="Whether the dish is a recommended item")
    is_available: bool = Field(description="Whether the dish is currently available")


class CanteenMenu(BaseModel):
    """Represents a daily menu for a specific canteen and meal type"""

    canteen_menu_ref: str = Field(description="Unique identifier for the canteen menu")
    canteen_ref: str = Field(description="Reference to the canteen this menu belongs to")
    menu_date: str = Field(description="Date for which this menu is applicable (ISO 8601 date)")
    meal_type: MealType = Field(
        description="Type of meal (breakfast, lunch, dinner, afternoon_tea, supper)"
    )
    dishes: List[DishItem] = Field(description="List of dish items available in this menu")
    created_at: str = Field(description="Timestamp when the canteen menu record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the canteen menu record was last updated (ISO 8601)")


class Visitor(BaseModel):
    """Represents a visitor with identity and contact information"""

    visitor_ref: str = Field(description="Unique identifier for the visitor")
    full_name: str = Field(description="Full name of the visitor")
    id_type: VisitorIdType = Field(
        description="Type of identification document (id_card, passport, driver_license, other)"
    )
    id_number: str = Field(description="Identification document number")
    phone: str = Field(description="Visitor's phone number")
    email: str = Field(description="Visitor's email address")
    company: str = Field(description="Company or organization the visitor represents")
    visitor_type: VisitorType = Field(
        description="Type of visitor (business, government, contractor, personal, other)"
    )
    created_at: str = Field(description="Timestamp when the visitor record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the visitor record was last updated (ISO 8601)")


class VisitorAppointment(BaseModel):
    """Represents a scheduled visitor appointment with a host employee"""

    visitor_appointment_ref: str = Field(description="Unique identifier for the visitor appointment")
    visitor_ref: str = Field(description="Reference to the visitor")
    host_employee_ref: str = Field(description="Employee reference of the host employee")
    campus_ref: str = Field(description="Reference to the campus where the visit will take place")
    visit_purpose: str = Field(description="Purpose of the visit")
    visit_type: VisitType = Field(
        description="Type of visit (business, interview, delivery, maintenance, government, personal, other)"
    )
    scheduled_start_at: str = Field(description="Scheduled start timestamp of the visit (ISO 8601)")
    scheduled_end_at: str = Field(description="Scheduled end timestamp of the visit (ISO 8601)")
    actual_checkin_at: Optional[str] = Field(
        description="Actual check-in timestamp, null if not yet checked in (ISO 8601)",
        default=None,
    )
    actual_checkout_at: Optional[str] = Field(
        description="Actual check-out timestamp, null if not yet checked out (ISO 8601)",
        default=None,
    )
    facility_ref: Optional[str] = Field(
        description="Reference to the facility where the meeting will take place, null if not specified",
        default=None,
    )
    temp_access_level: TempAccessLevel = Field(
        description="Temporary access level granted to the visitor (lobby, floor, zone, full)"
    )
    appointment_status: AppointmentStatus = Field(
        description="Current status of the appointment (pending, approved, rejected, checked_in, checked_out, expired, cancelled)"
    )
    notes: str = Field(description="Additional notes about the visit")
    created_at: str = Field(description="Timestamp when the appointment record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the appointment record was last updated (ISO 8601)")


class AccessCard(BaseModel):
    """Represents an access card issued to an employee or visitor"""

    access_card_ref: str = Field(description="Unique identifier for the access card")
    card_number: str = Field(description="Physical card number printed on the card")
    card_type: CardType = Field(
        description="Type of access card (employee, visitor, contractor, temporary, vip)"
    )
    holder_type: HolderType = Field(
        description="Type of card holder (employee, visitor, contractor)"
    )
    holder_ref: str = Field(description="Reference to the card holder (employee_ref or visitor_ref)")
    campus_ref: str = Field(description="Reference to the campus this card is issued for")
    access_zones: List[str] = Field(
        description="List of zone references this card grants access to"
    )
    card_status: CardStatus = Field(
        description="Current status of the access card (active, inactive, lost, expired, returned, deactivated)"
    )
    issued_at: str = Field(description="Timestamp when the card was issued (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the card, null if no expiration (ISO 8601)",
        default=None,
    )
    lost_at: Optional[str] = Field(
        description="Timestamp when the card was reported lost, null if not lost (ISO 8601)",
        default=None,
    )
    returned_at: Optional[str] = Field(
        description="Timestamp when the card was returned, null if not returned (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the access card")
    created_at: str = Field(description="Timestamp when the access card record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the access card record was last updated (ISO 8601)")


class AccessLog(BaseModel):
    """Represents a single access control event recorded at an access point"""

    access_log_ref: str = Field(description="Unique identifier for the access log entry")
    access_card_ref: str = Field(description="Reference to the access card used")
    campus_ref: str = Field(description="Reference to the campus where access was attempted")
    building_ref: str = Field(description="Reference to the building where access was attempted")
    access_point: str = Field(description="Description or identifier of the access point (e.g., gate, door)")
    access_direction: AccessDirection = Field(
        description="Direction of access (in, out)"
    )
    access_result: AccessResult = Field(
        description="Result of the access attempt (granted, denied, error)"
    )
    occurred_at: str = Field(description="Timestamp when the access event occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the access log record was created (ISO 8601)")


class Badge(BaseModel):
    """Represents an employee badge issued for identification purposes"""

    badge_ref: str = Field(description="Unique identifier for the badge")
    employee_ref: str = Field(description="Reference to the employee this badge belongs to")
    badge_number: str = Field(description="Physical badge number printed on the badge")
    badge_type: BadgeType = Field(
        description="Type of badge (standard, executive, contractor, intern, visitor)"
    )
    badge_status: BadgeStatus = Field(
        description="Current status of the badge (active, inactive, lost, expired, returned)"
    )
    issued_at: str = Field(description="Timestamp when the badge was issued (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the badge, null if no expiration (ISO 8601)",
        default=None,
    )
    lost_at: Optional[str] = Field(
        description="Timestamp when the badge was reported lost, null if not lost (ISO 8601)",
        default=None,
    )
    returned_at: Optional[str] = Field(
        description="Timestamp when the badge was returned, null if not returned (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the badge")
    created_at: str = Field(description="Timestamp when the badge record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the badge record was last updated (ISO 8601)")


class Asset(BaseModel):
    """Represents a physical asset owned by the organization"""

    asset_ref: str = Field(description="Unique identifier for the asset")
    asset_name: str = Field(description="Name or description of the asset")
    asset_code: str = Field(description="Short code or serial label for the asset")
    asset_category: AssetCategory = Field(
        description="Category of the asset (it_equipment, furniture, vehicle, office_equipment, lab_equipment, other)"
    )
    asset_subcategory: str = Field(description="Subcategory or specific type of the asset")
    brand: str = Field(description="Brand or manufacturer of the asset")
    model: str = Field(description="Model name or number of the asset")
    serial_number: str = Field(description="Serial number of the asset")
    campus_ref: str = Field(description="Reference to the campus where the asset is located")
    department_ref: str = Field(description="Reference to the department responsible for the asset")
    custodian_employee_ref: str = Field(
        description="Employee reference of the current custodian of the asset"
    )
    purchase_date: str = Field(description="Date the asset was purchased (ISO 8601 date)")
    purchase_price: float = Field(description="Purchase price of the asset in local currency")
    warranty_expires_at: Optional[str] = Field(
        description="Date when the warranty expires, null if no warranty (ISO 8601 date)",
        default=None,
    )
    asset_status: AssetStatus = Field(
        description="Current status of the asset (in_use, available, under_repair, scrapped, lost, reserved, in_transit)"
    )
    description: str = Field(description="Additional description or notes about the asset")
    created_at: str = Field(description="Timestamp when the asset record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the asset record was last updated (ISO 8601)")


class AssetRequest(BaseModel):
    """Represents an employee request for an asset (apply, borrow, return, repair, or scrap)"""

    asset_request_ref: str = Field(description="Unique identifier for the asset request")
    requester_employee_ref: str = Field(description="Employee reference of the requester")
    request_type: AssetRequestType = Field(
        description="Type of asset request (apply, borrow, return, repair, scrap, transfer)"
    )
    asset_ref: Optional[str] = Field(
        description="Reference to the specific asset, null if requesting a new asset",
        default=None,
    )
    asset_category: AssetCategory = Field(
        description="Category of the requested asset (it_equipment, furniture, vehicle, office_equipment, lab_equipment, other)"
    )
    asset_subcategory: str = Field(description="Subcategory or specific type of the requested asset")
    quantity: int = Field(description="Number of asset units requested")
    reason: str = Field(description="Reason for the asset request")
    expected_return_at: Optional[str] = Field(
        description="Expected return date for borrowed assets, null if not applicable (ISO 8601 date)",
        default=None,
    )
    request_status: AssetRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, fulfilled, cancelled, returned)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the request was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    reject_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    fulfilled_at: Optional[str] = Field(
        description="Timestamp when the request was fulfilled, null if not yet fulfilled (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the asset request")
    created_at: str = Field(description="Timestamp when the asset request record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the asset request record was last updated (ISO 8601)")


class AssetTransaction(BaseModel):
    """Represents a physical asset transaction such as issue, return, or transfer"""

    asset_transaction_ref: str = Field(description="Unique identifier for the asset transaction")
    asset_request_ref: str = Field(description="Reference to the asset request that triggered this transaction")
    asset_ref: str = Field(description="Reference to the asset involved in the transaction")
    transaction_type: AssetTransactionType = Field(
        description="Type of transaction (issue, return, transfer, repair_out, repair_in, scrap)"
    )
    from_employee_ref: Optional[str] = Field(
        description="Employee reference of the sender, null if asset is being issued from inventory",
        default=None,
    )
    to_employee_ref: Optional[str] = Field(
        description="Employee reference of the receiver, null if asset is being returned to inventory",
        default=None,
    )
    operated_by_ref: str = Field(
        description="Employee reference of the person who performed the transaction"
    )
    occurred_at: str = Field(description="Timestamp when the transaction occurred (ISO 8601)")
    notes: str = Field(description="Additional notes about the transaction")
    created_at: str = Field(description="Timestamp when the asset transaction record was created (ISO 8601)")


class InventoryItem(BaseModel):
    """Represents a consumable or borrowable inventory item managed by the admin team"""

    inventory_item_ref: str = Field(description="Unique identifier for the inventory item")
    item_name: str = Field(description="Name of the inventory item")
    item_code: str = Field(description="Short code for the inventory item")
    item_category: ItemCategory = Field(
        description="Category of the item (office_supply, cleaning_supply, it_accessory, kitchen_supply, safety_equipment, other)"
    )
    item_subcategory: str = Field(description="Subcategory or specific type of the item")
    unit: str = Field(description="Unit of measurement for the item (e.g., pcs, box, roll, pack)")
    campus_ref: str = Field(description="Reference to the campus where the item is stored")
    storage_location: str = Field(description="Physical storage location description within the campus")
    current_stock: int = Field(description="Current stock quantity of the item")
    min_stock_alert: int = Field(
        description="Minimum stock level that triggers a low-stock alert"
    )
    unit_cost: float = Field(description="Cost per unit of the item in local currency")
    item_status: ItemStatus = Field(
        description="Current status of the item (active, inactive, discontinued)"
    )
    description: str = Field(description="Description of the inventory item")
    created_at: str = Field(description="Timestamp when the inventory item record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the inventory item record was last updated (ISO 8601)")


class SupplyRequestItem(BaseModel):
    """Represents a single item line within a supply request"""

    inventory_item_ref: str = Field(description="Reference to the inventory item being requested")
    quantity: int = Field(description="Quantity of the item being requested")


class SupplyRequest(BaseModel):
    """Represents an employee request for office supplies or consumables"""

    supply_request_ref: str = Field(description="Unique identifier for the supply request")
    requester_employee_ref: str = Field(description="Employee reference of the requester")
    department_ref: str = Field(description="Reference to the department making the request")
    request_type: SupplyRequestType = Field(
        description="Type of supply request (borrow, consume, return)"
    )
    items: List[SupplyRequestItem] = Field(description="List of items being requested")
    reason: str = Field(description="Reason for the supply request")
    expected_return_at: Optional[str] = Field(
        description="Expected return date for borrowed items, null if not applicable (ISO 8601 date)",
        default=None,
    )
    request_status: SupplyRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, fulfilled, returned, cancelled)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the request was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    reject_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    fulfilled_at: Optional[str] = Field(
        description="Timestamp when the request was fulfilled, null if not yet fulfilled (ISO 8601)",
        default=None,
    )
    returned_at: Optional[str] = Field(
        description="Timestamp when borrowed items were returned, null if not returned (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the supply request")
    created_at: str = Field(description="Timestamp when the supply request record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the supply request record was last updated (ISO 8601)")


class RepairRequest(BaseModel):
    """Represents a facility or equipment repair request submitted by an employee"""

    repair_request_ref: str = Field(description="Unique identifier for the repair request")
    reporter_employee_ref: str = Field(description="Employee reference of the reporter")
    resource_type: ResourceType = Field(
        description="Type of resource requiring repair (facility, workstation, equipment, building, zone, other)"
    )
    resource_ref: str = Field(description="Reference to the resource requiring repair")
    campus_ref: str = Field(description="Reference to the campus where the repair is needed")
    building_ref: str = Field(description="Reference to the building where the repair is needed")
    floor_ref: str = Field(description="Reference to the floor where the repair is needed")
    fault_description: str = Field(description="Description of the fault or issue")
    fault_images: List[str] = Field(
        description="List of file attachment references for fault images"
    )
    urgency: RepairUrgency = Field(
        description="Urgency level of the repair (low, normal, high, critical)"
    )
    repair_status: RepairStatus = Field(
        description="Current status of the repair request (pending, assigned, in_progress, completed, cancelled, on_hold)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the assigned technician, null if not yet assigned",
        default=None,
    )
    scheduled_at: Optional[str] = Field(
        description="Timestamp when the repair is scheduled, null if not yet scheduled (ISO 8601)",
        default=None,
    )
    completed_at: Optional[str] = Field(
        description="Timestamp when the repair was completed, null if not yet completed (ISO 8601)",
        default=None,
    )
    resolution_notes: str = Field(description="Notes describing the resolution or repair outcome")
    created_at: str = Field(description="Timestamp when the repair request record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the repair request record was last updated (ISO 8601)")


class Complaint(BaseModel):
    """Represents a complaint submitted by an employee about a service or facility"""

    complaint_ref: str = Field(description="Unique identifier for the complaint")
    complainant_employee_ref: str = Field(description="Employee reference of the complainant")
    complaint_category: ComplaintCategory = Field(
        description="Category of the complaint (canteen, facility, security, it, hr, admin, other)"
    )
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource (e.g., facility, canteen, workstation), null if not applicable",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference to the related resource, null if not applicable",
        default=None,
    )
    title: str = Field(description="Title or subject of the complaint")
    description: str = Field(description="Detailed description of the complaint")
    attachments: List[str] = Field(
        description="List of file attachment references supporting the complaint"
    )
    complaint_status: ComplaintStatus = Field(
        description="Current status of the complaint (open, assigned, in_progress, resolved, closed, rejected)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the assigned handler, null if not yet assigned",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the complaint was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    resolution_notes: str = Field(description="Notes describing the resolution")
    created_at: str = Field(description="Timestamp when the complaint record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the complaint record was last updated (ISO 8601)")


class LostFound(BaseModel):
    """Represents a lost or found item record submitted by an employee"""

    lost_found_ref: str = Field(description="Unique identifier for the lost and found record")
    record_type: LostFoundRecordType = Field(
        description="Type of record (lost, found)"
    )
    reporter_employee_ref: str = Field(description="Employee reference of the reporter")
    item_name: str = Field(description="Name or brief description of the item")
    item_description: str = Field(description="Detailed description of the item")
    item_images: List[str] = Field(
        description="List of file attachment references for item images"
    )
    campus_ref: str = Field(description="Reference to the campus where the item was lost or found")
    location_description: str = Field(
        description="Description of the specific location where the item was lost or found"
    )
    occurred_date: str = Field(description="Date when the item was lost or found (ISO 8601 date)")
    matched_ref: Optional[str] = Field(
        description="Reference to the matching lost_found record, null if no match yet",
        default=None,
    )
    record_status: LostFoundStatus = Field(
        description="Current status of the record (open, matched, claimed, closed)"
    )
    claimed_by_ref: Optional[str] = Field(
        description="Employee reference of the person who claimed the item, null if not claimed",
        default=None,
    )
    claimed_at: Optional[str] = Field(
        description="Timestamp when the item was claimed, null if not claimed (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the lost or found item")
    created_at: str = Field(description="Timestamp when the lost and found record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the lost and found record was last updated (ISO 8601)")


class SecurityIncident(BaseModel):
    """Represents a security incident reported at a campus"""

    security_incident_ref: str = Field(description="Unique identifier for the security incident")
    reporter_employee_ref: str = Field(description="Employee reference of the reporter")
    campus_ref: str = Field(description="Reference to the campus where the incident occurred")
    incident_type: SecurityIncidentType = Field(
        description="Type of security incident (intrusion, theft, vandalism, fire, medical, safety_hazard, data_breach, other)"
    )
    severity: IncidentSeverity = Field(
        description="Severity level of the incident (low, medium, high, critical)"
    )
    title: str = Field(description="Title or brief description of the incident")
    description: str = Field(description="Detailed description of the security incident")
    occurred_at: str = Field(description="Timestamp when the incident occurred (ISO 8601)")
    location_description: str = Field(description="Description of the specific location of the incident")
    involved_parties: List[str] = Field(
        description="List of names or references of parties involved in the incident"
    )
    attachments: List[str] = Field(
        description="List of file attachment references supporting the incident report"
    )
    incident_status: IncidentStatus = Field(
        description="Current status of the incident (open, assigned, in_progress, resolved, closed)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the assigned security officer, null if not yet assigned",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the incident was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    resolution_notes: str = Field(description="Notes describing the resolution of the incident")
    created_at: str = Field(description="Timestamp when the security incident record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the security incident record was last updated (ISO 8601)")


class Gift(BaseModel):
    """Represents a gift item managed in the admin gift inventory"""

    gift_ref: str = Field(description="Unique identifier for the gift")
    gift_name: str = Field(description="Name of the gift item")
    gift_code: str = Field(description="Short code for the gift item")
    gift_category: str = Field(description="Category of the gift (e.g., souvenir, holiday, recognition)")
    unit_cost: float = Field(description="Cost per unit of the gift in local currency")
    current_stock: int = Field(description="Current stock quantity of the gift")
    min_stock_alert: int = Field(
        description="Minimum stock level that triggers a low-stock alert"
    )
    storage_location: str = Field(description="Physical storage location of the gift")
    campus_ref: str = Field(description="Reference to the campus where the gift is stored")
    gift_status: GiftStatus = Field(
        description="Current status of the gift (active, inactive, discontinued)"
    )
    description: str = Field(description="Description of the gift item")
    created_at: str = Field(description="Timestamp when the gift record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the gift record was last updated (ISO 8601)")


class GiftRecord(BaseModel):
    """Represents a record of a gift given to an employee or external party"""

    gift_record_ref: str = Field(description="Unique identifier for the gift record")
    gift_ref: str = Field(description="Reference to the gift item given")
    operated_by_ref: str = Field(description="Employee reference of the person who gave the gift")
    recipient_type: RecipientType = Field(
        description="Type of recipient (employee, department, team, visitor, external_partner)"
    )
    recipient_ref: str = Field(
        description="Reference to the recipient (employee_ref, department_ref, team_ref, visitor_ref, or external_partner_ref)"
    )
    quantity: int = Field(description="Number of gift units given")
    occasion: str = Field(description="Occasion or reason for giving the gift")
    notes: str = Field(description="Additional notes about the gift record")
    created_at: str = Field(description="Timestamp when the gift record was created (ISO 8601)")


class BusinessCard(BaseModel):
    """Represents a business card print request made by an employee"""

    business_card_ref: str = Field(description="Unique identifier for the business card request")
    employee_ref: str = Field(description="Reference to the employee requesting the business card")
    card_template: CardTemplate = Field(
        description="Template used for the business card (standard, executive, bilingual, custom)"
    )
    custom_fields: Dict[str, str] = Field(
        description="Dictionary of custom fields to be printed on the card (e.g., title overrides, social handles)"
    )
    quantity: int = Field(description="Number of business cards requested")
    request_status: BusinessCardRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, printing, delivered, cancelled)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the request was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    delivered_at: Optional[str] = Field(
        description="Timestamp when the business cards were delivered, null if not yet delivered (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the business card request")
    created_at: str = Field(description="Timestamp when the business card request record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the business card request record was last updated (ISO 8601)")


class CompanyEvent(BaseModel):
    """Represents a company-wide or department-level event organized by the admin team"""

    company_event_ref: str = Field(description="Unique identifier for the company event")
    event_name: str = Field(description="Name of the company event")
    event_type: CompanyEventType = Field(
        description="Type of event (company_day, team_building, training, seminar, celebration, sports, charity, other)"
    )
    campus_ref: str = Field(description="Reference to the campus where the event will take place")
    facility_ref: Optional[str] = Field(
        description="Reference to the specific facility for the event, null if not facility-specific",
        default=None,
    )
    organizer_employee_ref: str = Field(
        description="Employee reference of the event organizer"
    )
    department_ref: Optional[str] = Field(
        description="Reference to the organizing department, null if company-wide event",
        default=None,
    )
    start_at: str = Field(description="Timestamp when the event starts (ISO 8601)")
    end_at: str = Field(description="Timestamp when the event ends (ISO 8601)")
    max_attendees: Optional[int] = Field(
        description="Maximum number of attendees allowed, null if no limit",
        default=None,
    )
    description: str = Field(description="Description of the company event")
    attachments: List[str] = Field(
        description="List of file attachment references for event materials"
    )
    event_status: EventStatus = Field(
        description="Current status of the event (planned, ongoing, completed, cancelled, postponed)"
    )
    created_at: str = Field(description="Timestamp when the company event record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the company event record was last updated (ISO 8601)")


class EventRegistration(BaseModel):
    """Represents an employee's registration for a company event"""

    event_registration_ref: str = Field(description="Unique identifier for the event registration")
    company_event_ref: str = Field(description="Reference to the company event")
    employee_ref: str = Field(description="Reference to the registering employee")
    registration_status: EventRegistrationStatus = Field(
        description="Current status of the registration (registered, cancelled, attended, no_show, waitlisted)"
    )
    checked_in_at: Optional[str] = Field(
        description="Timestamp when the employee checked in to the event, null if not checked in (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the registration")
    created_at: str = Field(description="Timestamp when the event registration record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the event registration record was last updated (ISO 8601)")


class Policy(BaseModel):
    """Represents an organizational policy document managed by the admin team"""

    policy_ref: str = Field(description="Unique identifier for the policy")
    policy_title: str = Field(description="Title of the policy document")
    policy_code: str = Field(description="Short code for the policy")
    policy_category: PolicyCategory = Field(
        description="Category of the policy (meal_allowance, travel, it_usage, security, facility_usage, hr, finance, other)"
    )
    content: str = Field(description="Full content or body of the policy document")
    attachments: List[str] = Field(
        description="List of file attachment references for policy documents"
    )
    effective_date: str = Field(description="Date from which the policy is effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the policy expires, null if no expiry (ISO 8601 date)",
        default=None,
    )
    policy_status: PolicyStatus = Field(
        description="Current status of the policy (active, draft, expired, archived, under_review)"
    )
    owner_department_ref: str = Field(
        description="Reference to the department that owns this policy"
    )
    author_employee_ref: str = Field(
        description="Employee reference of the policy author"
    )
    version: str = Field(description="Version number of the policy document (e.g., 1.0, 2.1)")
    created_at: str = Field(description="Timestamp when the policy record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the policy record was last updated (ISO 8601)")


class ServiceDirectory(BaseModel):
    """Represents an entry in the admin service directory for internal services"""

    service_directory_ref: str = Field(description="Unique identifier for the service directory entry")
    service_name: str = Field(description="Name of the service")
    service_category: ServiceCategory = Field(
        description="Category of the service (admin, it, hr, finance, legal, security, facility, canteen, other)"
    )
    service_description: str = Field(description="Description of the service provided")
    contact_phone: str = Field(description="Contact phone number for the service")
    contact_email: str = Field(description="Contact email address for the service")
    contact_employee_ref: Optional[str] = Field(
        description="Employee reference of the primary contact person, null if not applicable",
        default=None,
    )
    department_ref: str = Field(description="Reference to the department providing the service")
    campus_ref: str = Field(description="Reference to the campus where the service is available")
    service_hours: str = Field(description="Operating hours of the service (e.g., Mon-Fri 09:00-18:00)")
    location_description: str = Field(description="Physical location description of the service")
    service_status: ServiceStatus = Field(
        description="Current status of the service (active, inactive, suspended)"
    )
    created_at: str = Field(description="Timestamp when the service directory record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the service directory record was last updated (ISO 8601)")


class ExternalPartner(BaseModel):
    """Represents an external partner, vendor, or supplier engaged by the organization"""

    external_partner_ref: str = Field(description="Unique identifier for the external partner")
    partner_name: str = Field(description="Name of the external partner organization")
    partner_type: PartnerType = Field(
        description="Type of partner (supplier, vendor, contractor, service_provider, logistics, other)"
    )
    contact_person: str = Field(description="Name of the primary contact person at the partner")
    contact_phone: str = Field(description="Contact phone number for the partner")
    contact_email: str = Field(description="Contact email address for the partner")
    address: str = Field(description="Physical address of the partner organization")
    partner_status: PartnerStatus = Field(
        description="Current status of the partner (active, inactive, suspended, blacklisted)"
    )
    description: str = Field(description="Description of the partner and the nature of engagement")
    created_at: str = Field(description="Timestamp when the external partner record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the external partner record was last updated (ISO 8601)")


class TravelPolicy(BaseModel):
    """Represents a travel reimbursement policy applicable to employees based on position level and city tier"""

    travel_policy_ref: str = Field(description="Unique identifier for the travel policy")
    policy_name: str = Field(description="Name of the travel policy")
    position_level_min: int = Field(
        description="Minimum position level this policy applies to (inclusive)"
    )
    position_level_max: int = Field(
        description="Maximum position level this policy applies to (inclusive)"
    )
    city_tier: CityTier = Field(
        description="City tier classification this policy applies to (tier1, tier2, tier3, international)"
    )
    hotel_daily_limit: float = Field(
        description="Maximum hotel expense per day in local currency"
    )
    meal_daily_limit: float = Field(
        description="Maximum meal expense per day in local currency"
    )
    transport_class: TransportClass = Field(
        description="Allowed transport class (economy, business, first, high_speed_rail_second, high_speed_rail_first)"
    )
    effective_date: str = Field(description="Date from which this travel policy is effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when this travel policy expires, null if no expiry (ISO 8601 date)",
        default=None,
    )
    policy_status: TravelPolicyStatus = Field(
        description="Current status of the travel policy (active, inactive, expired, draft)"
    )
    notes: str = Field(description="Additional notes about the travel policy")
    created_at: str = Field(description="Timestamp when the travel policy record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the travel policy record was last updated (ISO 8601)")


class CleaningSchedule(BaseModel):
    """Represents a scheduled cleaning task for a campus floor or zone"""

    cleaning_schedule_ref: str = Field(description="Unique identifier for the cleaning schedule")
    campus_ref: str = Field(description="Reference to the campus this cleaning schedule applies to")
    floor_ref: str = Field(description="Reference to the floor this cleaning schedule applies to")
    zone_ref: Optional[str] = Field(
        description="Reference to the specific zone, null if the entire floor is covered",
        default=None,
    )
    cleaning_type: CleaningType = Field(
        description="Type of cleaning (daily, deep, disinfection, carpet, window, other)"
    )
    frequency: CleaningFrequency = Field(
        description="Frequency of the cleaning (daily, weekly, biweekly, monthly, on_demand)"
    )
    scheduled_time: str = Field(description="Scheduled time for the cleaning in HH:MM format")
    assigned_vendor_ref: Optional[str] = Field(
        description="Reference to the external partner (vendor) assigned for cleaning, null if internal",
        default=None,
    )
    schedule_status: CleaningScheduleStatus = Field(
        description="Current status of the cleaning schedule (active, suspended, cancelled)"
    )
    notes: str = Field(description="Additional notes about the cleaning schedule")
    created_at: str = Field(description="Timestamp when the cleaning schedule record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the cleaning schedule record was last updated (ISO 8601)")


class CleaningRecord(BaseModel):
    """Represents an executed cleaning task record linked to a cleaning schedule"""

    cleaning_record_ref: str = Field(description="Unique identifier for the cleaning record")
    cleaning_schedule_ref: str = Field(description="Reference to the cleaning schedule this record fulfills")
    executed_by: str = Field(description="Name or identifier of the person or team who executed the cleaning")
    executed_at: str = Field(description="Timestamp when the cleaning was executed (ISO 8601)")
    result: CleaningResult = Field(
        description="Result of the cleaning execution (completed, partial, skipped, failed)"
    )
    notes: str = Field(description="Additional notes about the cleaning execution")
    created_at: str = Field(description="Timestamp when the cleaning record was created (ISO 8601)")


# --- AdminDB ---


class AdminDB(OfficeDB):
    """Database containing all base office collaboration data plus ADMIN-specific facility, asset, visitor and operations data"""

    campus: Dict[str, Campus] = Field(
        description="Dictionary of all campuses indexed by campus_ref"
    )
    building: Dict[str, Building] = Field(
        description="Dictionary of all buildings indexed by building_ref"
    )
    floor: Dict[str, Floor] = Field(
        description="Dictionary of all floors indexed by floor_ref"
    )
    zone: Dict[str, Zone] = Field(
        description="Dictionary of all zones indexed by zone_ref"
    )
    facility: Dict[str, Facility] = Field(
        description="Dictionary of all facilities indexed by facility_ref"
    )
    facility_equipment: Dict[str, FacilityEquipment] = Field(
        description="Dictionary of all facility equipment records indexed by facility_equipment_ref"
    )
    booking: Dict[str, Booking] = Field(
        description="Dictionary of all facility bookings indexed by booking_ref"
    )
    workstation: Dict[str, Workstation] = Field(
        description="Dictionary of all workstations indexed by workstation_ref"
    )
    locker: Dict[str, Locker] = Field(
        description="Dictionary of all lockers indexed by locker_ref"
    )
    parking_space: Dict[str, ParkingSpace] = Field(
        description="Dictionary of all parking spaces indexed by parking_space_ref"
    )
    ev_charger: Dict[str, EvCharger] = Field(
        description="Dictionary of all EV chargers indexed by ev_charger_ref"
    )
    shuttle_route: Dict[str, ShuttleRoute] = Field(
        description="Dictionary of all shuttle routes indexed by shuttle_route_ref"
    )
    shuttle_stop: Dict[str, ShuttleStop] = Field(
        description="Dictionary of all shuttle stops indexed by shuttle_stop_ref"
    )
    shuttle_schedule: Dict[str, ShuttleSchedule] = Field(
        description="Dictionary of all shuttle schedules indexed by shuttle_schedule_ref"
    )
    shuttle_booking: Dict[str, ShuttleBooking] = Field(
        description="Dictionary of all shuttle bookings indexed by shuttle_booking_ref"
    )
    canteen: Dict[str, Canteen] = Field(
        description="Dictionary of all canteens indexed by canteen_ref"
    )
    canteen_menu: Dict[str, CanteenMenu] = Field(
        description="Dictionary of all canteen menus indexed by canteen_menu_ref"
    )
    visitor: Dict[str, Visitor] = Field(
        description="Dictionary of all visitors indexed by visitor_ref"
    )
    visitor_appointment: Dict[str, VisitorAppointment] = Field(
        description="Dictionary of all visitor appointments indexed by visitor_appointment_ref"
    )
    access_card: Dict[str, AccessCard] = Field(
        description="Dictionary of all access cards indexed by access_card_ref"
    )
    access_log: Dict[str, AccessLog] = Field(
        description="Dictionary of all access log entries indexed by access_log_ref"
    )
    badge: Dict[str, Badge] = Field(
        description="Dictionary of all badges indexed by badge_ref"
    )
    asset: Dict[str, Asset] = Field(
        description="Dictionary of all assets indexed by asset_ref"
    )
    asset_request: Dict[str, AssetRequest] = Field(
        description="Dictionary of all asset requests indexed by asset_request_ref"
    )
    asset_transaction: Dict[str, AssetTransaction] = Field(
        description="Dictionary of all asset transactions indexed by asset_transaction_ref"
    )
    inventory_item: Dict[str, InventoryItem] = Field(
        description="Dictionary of all inventory items indexed by inventory_item_ref"
    )
    supply_request: Dict[str, SupplyRequest] = Field(
        description="Dictionary of all supply requests indexed by supply_request_ref"
    )
    repair_request: Dict[str, RepairRequest] = Field(
        description="Dictionary of all repair requests indexed by repair_request_ref"
    )
    complaint: Dict[str, Complaint] = Field(
        description="Dictionary of all complaints indexed by complaint_ref"
    )
    lost_found: Dict[str, LostFound] = Field(
        description="Dictionary of all lost and found records indexed by lost_found_ref"
    )
    security_incident: Dict[str, SecurityIncident] = Field(
        description="Dictionary of all security incidents indexed by security_incident_ref"
    )
    gift: Dict[str, Gift] = Field(
        description="Dictionary of all gifts indexed by gift_ref"
    )
    gift_record: Dict[str, GiftRecord] = Field(
        description="Dictionary of all gift records indexed by gift_record_ref"
    )
    business_card: Dict[str, BusinessCard] = Field(
        description="Dictionary of all business card requests indexed by business_card_ref"
    )
    company_event: Dict[str, CompanyEvent] = Field(
        description="Dictionary of all company events indexed by company_event_ref"
    )
    event_registration: Dict[str, EventRegistration] = Field(
        description="Dictionary of all event registrations indexed by event_registration_ref"
    )
    policy: Dict[str, Policy] = Field(
        description="Dictionary of all policies indexed by policy_ref"
    )
    service_directory: Dict[str, ServiceDirectory] = Field(
        description="Dictionary of all service directory entries indexed by service_directory_ref"
    )
    external_partner: Dict[str, ExternalPartner] = Field(
        description="Dictionary of all external partners indexed by external_partner_ref"
    )
    travel_policy: Dict[str, TravelPolicy] = Field(
        description="Dictionary of all travel policies indexed by travel_policy_ref"
    )
    cleaning_schedule: Dict[str, CleaningSchedule] = Field(
        description="Dictionary of all cleaning schedules indexed by cleaning_schedule_ref"
    )
    cleaning_record: Dict[str, CleaningRecord] = Field(
        description="Dictionary of all cleaning records indexed by cleaning_record_ref"
    )

    def get_statistics(self) -> Dict[str, Any]:
        """
        功能说明（Description）：
            获取ADMIN模块统计信息，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `Dict[str, Any]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        base_stats = super().get_statistics()
        admin_stats = {
            "num_campuses": len(self.campus),
            "num_buildings": len(self.building),
            "num_floors": len(self.floor),
            "num_zones": len(self.zone),
            "num_facilities": len(self.facility),
            "num_facility_equipment": len(self.facility_equipment),
            "num_bookings": len(self.booking),
            "num_workstations": len(self.workstation),
            "num_lockers": len(self.locker),
            "num_parking_spaces": len(self.parking_space),
            "num_ev_chargers": len(self.ev_charger),
            "num_shuttle_routes": len(self.shuttle_route),
            "num_shuttle_stops": len(self.shuttle_stop),
            "num_shuttle_schedules": len(self.shuttle_schedule),
            "num_shuttle_bookings": len(self.shuttle_booking),
            "num_canteens": len(self.canteen),
            "num_canteen_menus": len(self.canteen_menu),
            "num_visitors": len(self.visitor),
            "num_visitor_appointments": len(self.visitor_appointment),
            "num_access_cards": len(self.access_card),
            "num_access_logs": len(self.access_log),
            "num_badges": len(self.badge),
            "num_assets": len(self.asset),
            "num_asset_requests": len(self.asset_request),
            "num_asset_transactions": len(self.asset_transaction),
            "num_inventory_items": len(self.inventory_item),
            "num_supply_requests": len(self.supply_request),
            "num_repair_requests": len(self.repair_request),
            "num_complaints": len(self.complaint),
            "num_lost_found": len(self.lost_found),
            "num_security_incidents": len(self.security_incident),
            "num_gifts": len(self.gift),
            "num_gift_records": len(self.gift_record),
            "num_business_cards": len(self.business_card),
            "num_company_events": len(self.company_event),
            "num_event_registrations": len(self.event_registration),
            "num_policies": len(self.policy),
            "num_service_directory": len(self.service_directory),
            "num_external_partners": len(self.external_partner),
            "num_travel_policies": len(self.travel_policy),
            "num_cleaning_schedules": len(self.cleaning_schedule),
            "num_cleaning_records": len(self.cleaning_record),
        }
        return {**base_stats, **admin_stats}