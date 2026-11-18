"""ADMIN 域工具集：在 OfficeTools 之上扩展行政后勤相关操作。"""
from typing import Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.admin.models import (
    AdminDB,
    Campus,
    Building,
    Floor,
    Zone,
    Facility,
    FacilityEquipment,
    Booking,
    Workstation,
    Locker,
    ParkingSpace,
    EvCharger,
    ShuttleRoute,
    ShuttleStop,
    ShuttleSchedule,
    ShuttleBooking,
    Canteen,
    CanteenMenu,
    Visitor,
    VisitorAppointment,
    AccessCard,
    AccessLog,
    Badge,
    Asset,
    AssetRequest,
    AssetTransaction,
    InventoryItem,
    SupplyRequest,
    SupplyRequestItem,
    RepairRequest,
    Complaint,
    LostFound,
    SecurityIncident,
    Gift,
    GiftRecord,
    BusinessCard,
    CompanyEvent,
    EventRegistration,
    Policy,
    ServiceDirectory,
    ExternalPartner,
    TravelPolicy,
    CleaningSchedule,
    CleaningRecord,
)


class AdminTools(OfficeTools):
    """ADMIN 域工具集：在 OfficeTools 之上扩展行政后勤相关操作。"""

    db: AdminDB

    def __init__(self, db: AdminDB) -> None:
        """
        功能说明（Description）：
            初始化对象并绑定所需依赖。
        参数（Parameters）：
            - `db` (AdminDB): 数据库对象实例；为空时通常会走默认加载逻辑。
        返回（Returns）：
            - `None`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        super().__init__(db)

    # -----------------------
    # 内部辅助方法
    # -----------------------

    def _get_campus(self, campus_ref: str) -> Campus:
        """
        功能说明（Description）：
            获取园区，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `campus_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Campus`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref not in self.db.campus:
            raise ValueError("Campus not found")
        return self.db.campus[campus_ref]

    def _get_building(self, building_ref: str) -> Building:
        """
        功能说明（Description）：
            获取楼宇，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `building_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Building`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if building_ref not in self.db.building:
            raise ValueError("Building not found")
        return self.db.building[building_ref]

    def _get_floor(self, floor_ref: str) -> Floor:
        """
        功能说明（Description）：
            获取楼层，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `floor_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Floor`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if floor_ref not in self.db.floor:
            raise ValueError("Floor not found")
        return self.db.floor[floor_ref]

    def _get_zone(self, zone_ref: str) -> Zone:
        """
        功能说明（Description）：
            获取区域，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `zone_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Zone`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if zone_ref not in self.db.zone:
            raise ValueError("Zone not found")
        return self.db.zone[zone_ref]

    def _get_facility(self, facility_ref: str) -> Facility:
        """
        功能说明（Description）：
            获取场地/设施，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `facility_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Facility`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if facility_ref not in self.db.facility:
            raise ValueError("Facility not found")
        return self.db.facility[facility_ref]

    def _get_facility_equipment(self, facility_equipment_ref: str) -> FacilityEquipment:
        """
        功能说明（Description）：
            获取设施设备，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `facility_equipment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `FacilityEquipment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if facility_equipment_ref not in self.db.facility_equipment:
            raise ValueError("Facility equipment not found")
        return self.db.facility_equipment[facility_equipment_ref]

    def _get_booking(self, booking_ref: str) -> Booking:
        """
        功能说明（Description）：
            获取场地预订，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `booking_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Booking`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if booking_ref not in self.db.booking:
            raise ValueError("Booking not found")
        return self.db.booking[booking_ref]

    def _get_workstation(self, workstation_ref: str) -> Workstation:
        """
        功能说明（Description）：
            获取工位，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `workstation_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Workstation`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if workstation_ref not in self.db.workstation:
            raise ValueError("Workstation not found")
        return self.db.workstation[workstation_ref]

    def _get_locker(self, locker_ref: str) -> Locker:
        """
        功能说明（Description）：
            获取储物柜，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `locker_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Locker`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if locker_ref not in self.db.locker:
            raise ValueError("Locker not found")
        return self.db.locker[locker_ref]

    def _get_parking_space(self, parking_space_ref: str) -> ParkingSpace:
        """
        功能说明（Description）：
            获取停车位，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `parking_space_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ParkingSpace`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if parking_space_ref not in self.db.parking_space:
            raise ValueError("Parking space not found")
        return self.db.parking_space[parking_space_ref]

    def _get_ev_charger(self, ev_charger_ref: str) -> EvCharger:
        """
        功能说明（Description）：
            获取充电桩，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ev_charger_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EvCharger`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ev_charger_ref not in self.db.ev_charger:
            raise ValueError("EV charger not found")
        return self.db.ev_charger[ev_charger_ref]

    def _get_shuttle_route(self, shuttle_route_ref: str) -> ShuttleRoute:
        """
        功能说明（Description）：
            获取班车线路，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `shuttle_route_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleRoute`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if shuttle_route_ref not in self.db.shuttle_route:
            raise ValueError("Shuttle route not found")
        return self.db.shuttle_route[shuttle_route_ref]

    def _get_shuttle_stop(self, shuttle_stop_ref: str) -> ShuttleStop:
        """
        功能说明（Description）：
            获取班车站点，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `shuttle_stop_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleStop`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if shuttle_stop_ref not in self.db.shuttle_stop:
            raise ValueError("Shuttle stop not found")
        return self.db.shuttle_stop[shuttle_stop_ref]

    def _get_shuttle_schedule(self, shuttle_schedule_ref: str) -> ShuttleSchedule:
        """
        功能说明（Description）：
            获取班车班次，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `shuttle_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if shuttle_schedule_ref not in self.db.shuttle_schedule:
            raise ValueError("Shuttle schedule not found")
        return self.db.shuttle_schedule[shuttle_schedule_ref]

    def _get_shuttle_booking(self, shuttle_booking_ref: str) -> ShuttleBooking:
        """
        功能说明（Description）：
            获取班车预订，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `shuttle_booking_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleBooking`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if shuttle_booking_ref not in self.db.shuttle_booking:
            raise ValueError("Shuttle booking not found")
        return self.db.shuttle_booking[shuttle_booking_ref]

    def _get_canteen(self, canteen_ref: str) -> Canteen:
        """
        功能说明（Description）：
            获取食堂，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `canteen_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Canteen`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if canteen_ref not in self.db.canteen:
            raise ValueError("Canteen not found")
        return self.db.canteen[canteen_ref]

    def _get_canteen_menu(self, canteen_menu_ref: str) -> CanteenMenu:
        """
        功能说明（Description）：
            获取食堂菜单，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `canteen_menu_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CanteenMenu`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if canteen_menu_ref not in self.db.canteen_menu:
            raise ValueError("Canteen menu not found")
        return self.db.canteen_menu[canteen_menu_ref]

    def _get_visitor(self, visitor_ref: str) -> Visitor:
        """
        功能说明（Description）：
            获取访客，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `visitor_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Visitor`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if visitor_ref not in self.db.visitor:
            raise ValueError("Visitor not found")
        return self.db.visitor[visitor_ref]

    def _get_visitor_appointment(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            获取访客预约，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `visitor_appointment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `VisitorAppointment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if visitor_appointment_ref not in self.db.visitor_appointment:
            raise ValueError("Visitor appointment not found")
        return self.db.visitor_appointment[visitor_appointment_ref]

    def _get_access_card(self, access_card_ref: str) -> AccessCard:
        """
        功能说明（Description）：
            获取门禁卡，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `access_card_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `AccessCard`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if access_card_ref not in self.db.access_card:
            raise ValueError("Access card not found")
        return self.db.access_card[access_card_ref]

    def _get_badge(self, badge_ref: str) -> Badge:
        """
        功能说明（Description）：
            获取工牌，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `badge_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Badge`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if badge_ref not in self.db.badge:
            raise ValueError("Badge not found")
        return self.db.badge[badge_ref]

    def _get_asset(self, asset_ref: str) -> Asset:
        """
        功能说明（Description）：
            获取资产，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `asset_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Asset`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if asset_ref not in self.db.asset:
            raise ValueError("Asset not found")
        return self.db.asset[asset_ref]

    def _get_asset_request(self, asset_request_ref: str) -> AssetRequest:
        """
        功能说明（Description）：
            获取资产申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `asset_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `AssetRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if asset_request_ref not in self.db.asset_request:
            raise ValueError("Asset request not found")
        return self.db.asset_request[asset_request_ref]

    def _get_inventory_item(self, inventory_item_ref: str) -> InventoryItem:
        """
        功能说明（Description）：
            获取库存物料，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `inventory_item_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `InventoryItem`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if inventory_item_ref not in self.db.inventory_item:
            raise ValueError("Inventory item not found")
        return self.db.inventory_item[inventory_item_ref]

    def _get_supply_request(self, supply_request_ref: str) -> SupplyRequest:
        """
        功能说明（Description）：
            获取领用申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `supply_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SupplyRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if supply_request_ref not in self.db.supply_request:
            raise ValueError("Supply request not found")
        return self.db.supply_request[supply_request_ref]

    def _get_repair_request(self, repair_request_ref: str) -> RepairRequest:
        """
        功能说明（Description）：
            获取报修单，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `repair_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `RepairRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if repair_request_ref not in self.db.repair_request:
            raise ValueError("Repair request not found")
        return self.db.repair_request[repair_request_ref]

    def _get_complaint(self, complaint_ref: str) -> Complaint:
        """
        功能说明（Description）：
            获取投诉，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `complaint_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Complaint`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if complaint_ref not in self.db.complaint:
            raise ValueError("Complaint not found")
        return self.db.complaint[complaint_ref]

    def _get_lost_found(self, lost_found_ref: str) -> LostFound:
        """
        功能说明（Description）：
            获取失物招领记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `lost_found_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LostFound`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if lost_found_ref not in self.db.lost_found:
            raise ValueError("Lost and found record not found")
        return self.db.lost_found[lost_found_ref]

    def _get_security_incident(self, security_incident_ref: str) -> SecurityIncident:
        """
        功能说明（Description）：
            获取安全事件，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `security_incident_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SecurityIncident`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if security_incident_ref not in self.db.security_incident:
            raise ValueError("Security incident not found")
        return self.db.security_incident[security_incident_ref]

    def _get_gift(self, gift_ref: str) -> Gift:
        """
        功能说明（Description）：
            获取礼品，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `gift_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Gift`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if gift_ref not in self.db.gift:
            raise ValueError("Gift not found")
        return self.db.gift[gift_ref]

    def _get_gift_record(self, gift_record_ref: str) -> GiftRecord:
        """
        功能说明（Description）：
            获取礼品发放记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `gift_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `GiftRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if gift_record_ref not in self.db.gift_record:
            raise ValueError("Gift record not found")
        return self.db.gift_record[gift_record_ref]

    def _get_business_card(self, business_card_ref: str) -> BusinessCard:
        """
        功能说明（Description）：
            获取名片印制申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `business_card_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BusinessCard`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if business_card_ref not in self.db.business_card:
            raise ValueError("Business card not found")
        return self.db.business_card[business_card_ref]

    def _get_company_event(self, company_event_ref: str) -> CompanyEvent:
        """
        功能说明（Description）：
            获取公司活动，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `company_event_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CompanyEvent`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if company_event_ref not in self.db.company_event:
            raise ValueError("Company event not found")
        return self.db.company_event[company_event_ref]

    def _get_event_registration(self, event_registration_ref: str) -> EventRegistration:
        """
        功能说明（Description）：
            获取活动报名，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `event_registration_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EventRegistration`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if event_registration_ref not in self.db.event_registration:
            raise ValueError("Event registration not found")
        return self.db.event_registration[event_registration_ref]

    def _get_policy(self, policy_ref: str) -> Policy:
        """
        功能说明（Description）：
            获取制度/政策，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Policy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if policy_ref not in self.db.policy:
            raise ValueError("Policy not found")
        return self.db.policy[policy_ref]

    def _get_service_directory(self, service_directory_ref: str) -> ServiceDirectory:
        """
        功能说明（Description）：
            获取服务目录条目，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `service_directory_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ServiceDirectory`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if service_directory_ref not in self.db.service_directory:
            raise ValueError("Service directory entry not found")
        return self.db.service_directory[service_directory_ref]

    def _get_external_partner(self, external_partner_ref: str) -> ExternalPartner:
        """
        功能说明（Description）：
            获取外部合作方，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `external_partner_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ExternalPartner`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if external_partner_ref not in self.db.external_partner:
            raise ValueError("External partner not found")
        return self.db.external_partner[external_partner_ref]

    def _get_travel_policy(self, travel_policy_ref: str) -> TravelPolicy:
        """
        功能说明（Description）：
            获取差旅政策，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `travel_policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TravelPolicy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if travel_policy_ref not in self.db.travel_policy:
            raise ValueError("Travel policy not found")
        return self.db.travel_policy[travel_policy_ref]

    def _get_cleaning_schedule(self, cleaning_schedule_ref: str) -> CleaningSchedule:
        """
        功能说明（Description）：
            获取保洁计划，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `cleaning_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CleaningSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if cleaning_schedule_ref not in self.db.cleaning_schedule:
            raise ValueError("Cleaning schedule not found")
        return self.db.cleaning_schedule[cleaning_schedule_ref]

    def _get_cleaning_record(self, cleaning_record_ref: str) -> CleaningRecord:
        """
        功能说明（Description）：
            获取保洁执行记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `cleaning_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CleaningRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if cleaning_record_ref not in self.db.cleaning_record:
            raise ValueError("Cleaning record not found")
        return self.db.cleaning_record[cleaning_record_ref]

    # ----------------
    # 园区（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_campus_details(self, campus_ref: str) -> Campus:
        """
        功能说明（Description）：
            根据引用 ID 获取园区的详细信息。
        参数（Parameters）：
            - `campus_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Campus`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_campus(campus_ref)

    @is_tool(ToolType.READ)
    def list_campuses(
        self,
        campus_type: Optional[str] = None,
        status: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出园区/校区摘要。
        参数（Parameters）：
            - `campus_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `city` (Optional[str]) 地理信息；默认为 None 表示不按此项筛选。
            - `country` (Optional[str]) 地理信息；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的列表，每项含 campus_ref、campus_name 等字段。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for c_ref, c in self.db.campus.items():
            if campus_type is not None and c.campus_type != campus_type:
                continue
            if status is not None and c.campus_status != status:
                continue
            if city is not None and city.lower() not in c.city.lower():
                continue
            if country is not None and country.lower() not in c.country.lower():
                continue
            results.append({
                "campus_ref": c.campus_ref,
                "campus_name": c.campus_name,
                "campus_code": c.campus_code,
                "campus_type": c.campus_type,
                "campus_status": c.campus_status,
                "city": c.city,
                "country": c.country,
                "address": c.address,
            })
        return json.dumps(results)

    # ----------------
    # 楼宇（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_building_details(self, building_ref: str) -> Building:
        """
        功能说明（Description）：
            根据引用 ID 获取楼宇的详细信息。
        参数（Parameters）：
            - `building_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Building`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_building(building_ref)

    @is_tool(ToolType.READ)
    def list_buildings(
        self,
        campus_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出楼宇摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的楼宇摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for b_ref, b in self.db.building.items():
            if campus_ref is not None and b.campus_ref != campus_ref:
                continue
            if status is not None and b.building_status != status:
                continue
            results.append({
                "building_ref": b.building_ref,
                "building_name": b.building_name,
                "building_code": b.building_code,
                "campus_ref": b.campus_ref,
                "floor_count": b.floor_count,
                "building_status": b.building_status,
            })
        return json.dumps(results)

    # ----------------
    # 楼层（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_floor_details(self, floor_ref: str) -> Floor:
        """
        功能说明（Description）：
            根据引用 ID 获取楼层的详细信息。
        参数（Parameters）：
            - `floor_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Floor`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_floor(floor_ref)

    @is_tool(ToolType.READ)
    def list_floors(
        self,
        building_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出楼层摘要。
        参数（Parameters）：
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的楼层摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if building_ref is not None:
            self._get_building(building_ref)
        results = []
        for f_ref, f in self.db.floor.items():
            if building_ref is not None and f.building_ref != building_ref:
                continue
            if status is not None and f.floor_status != status:
                continue
            results.append({
                "floor_ref": f.floor_ref,
                "building_ref": f.building_ref,
                "floor_number": f.floor_number,
                "floor_name": f.floor_name,
                "floor_status": f.floor_status,
            })
        return json.dumps(results)

    # ----------------
    # 区域（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_zone_details(self, zone_ref: str) -> Zone:
        """
        功能说明（Description）：
            根据引用 ID 获取区域的详细信息。
        参数（Parameters）：
            - `zone_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Zone`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_zone(zone_ref)

    @is_tool(ToolType.READ)
    def list_zones(
        self,
        floor_ref: Optional[str] = None,
        zone_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出区域摘要。
        参数（Parameters）：
            - `floor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `zone_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的区域摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if floor_ref is not None:
            self._get_floor(floor_ref)
        results = []
        for z_ref, z in self.db.zone.items():
            if floor_ref is not None and z.floor_ref != floor_ref:
                continue
            if zone_type is not None and z.zone_type != zone_type:
                continue
            if status is not None and z.zone_status != status:
                continue
            results.append({
                "zone_ref": z.zone_ref,
                "floor_ref": z.floor_ref,
                "zone_name": z.zone_name,
                "zone_code": z.zone_code,
                "zone_type": z.zone_type,
                "zone_status": z.zone_status,
                "description": z.description,
            })
        return json.dumps(results)

    # ----------------
    # 场地/设施（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_facility_details(self, facility_ref: str) -> Facility:
        """
        功能说明（Description）：
            根据引用 ID 获取场地/设施的详细信息。
        参数（Parameters）：
            - `facility_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Facility`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_facility(facility_ref)

    @is_tool(ToolType.READ)
    def list_facilities(
        self,
        campus_ref: Optional[str] = None,
        building_ref: Optional[str] = None,
        floor_ref: Optional[str] = None,
        zone_ref: Optional[str] = None,
        facility_type: Optional[str] = None,
        status: Optional[str] = None,
        is_bookable: Optional[bool] = None,
        min_capacity: Optional[int] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出场地/设施摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `floor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `zone_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `facility_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `is_bookable` (Optional[bool])；默认为 None 表示不按此项筛选。
            - `min_capacity` (Optional[int])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的场地摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for f_ref, f in self.db.facility.items():
            if campus_ref is not None and f.campus_ref != campus_ref:
                continue
            if building_ref is not None and f.building_ref != building_ref:
                continue
            if floor_ref is not None and f.floor_ref != floor_ref:
                continue
            if zone_ref is not None and f.zone_ref != zone_ref:
                continue
            if facility_type is not None and f.facility_type != facility_type:
                continue
            if status is not None and f.facility_status != status:
                continue
            if is_bookable is not None and f.is_bookable != is_bookable:
                continue
            if min_capacity is not None and f.capacity < min_capacity:
                continue
            results.append({
                "facility_ref": f.facility_ref,
                "facility_name": f.facility_name,
                "facility_code": f.facility_code,
                "facility_type": f.facility_type,
                "campus_ref": f.campus_ref,
                "building_ref": f.building_ref,
                "floor_ref": f.floor_ref,
                "zone_ref": f.zone_ref,
                "capacity": f.capacity,
                "area_sqm": f.area_sqm,
                "facility_status": f.facility_status,
                "is_bookable": f.is_bookable,
                "amenities": f.amenities,
            })
        return json.dumps(results)

    # ----------------
    # 设施设备（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_facility_equipment_details(self, facility_equipment_ref: str) -> FacilityEquipment:
        """
        功能说明（Description）：
            根据引用 ID 获取设施设备的详细信息。
        参数（Parameters）：
            - `facility_equipment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `FacilityEquipment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_facility_equipment(facility_equipment_ref)

    @is_tool(ToolType.READ)
    def list_facility_equipment(
        self,
        facility_ref: str,
        equipment_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件列出某场地下的设备清单。
        参数（Parameters）：
            - `facility_ref` (str)；按函数语义传入。
            - `equipment_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的设备摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_facility(facility_ref)
        results = []
        for eq_ref, eq in self.db.facility_equipment.items():
            if eq.facility_ref != facility_ref:
                continue
            if equipment_type is not None and eq.equipment_type != equipment_type:
                continue
            if status is not None and eq.equipment_status != status:
                continue
            results.append({
                "facility_equipment_ref": eq.facility_equipment_ref,
                "facility_ref": eq.facility_ref,
                "equipment_name": eq.equipment_name,
                "equipment_type": eq.equipment_type,
                "quantity": eq.quantity,
                "equipment_status": eq.equipment_status,
                "notes": eq.notes,
            })
        return json.dumps(results)

    # ----------------
    # 场地预订（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_booking_details(self, booking_ref: str) -> Booking:
        """
        功能说明（Description）：
            根据引用 ID 获取场地预订的详细信息。
        参数（Parameters）：
            - `booking_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Booking`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_booking(booking_ref)

    @is_tool(ToolType.READ)
    def list_bookings(
        self,
        facility_ref: Optional[str] = None,
        booker_employee_ref: Optional[str] = None,
        booking_status: Optional[str] = None,
        booking_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出场地预订记录。
        参数（Parameters）：
            - `facility_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `booker_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `booking_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `booking_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `date_from` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
            - `date_to` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的预订摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if facility_ref is not None:
            self._get_facility(facility_ref)
        if booker_employee_ref is not None:
            self._get_employee(booker_employee_ref)
        results = []
        for b_ref, b in self.db.booking.items():
            if facility_ref is not None and b.facility_ref != facility_ref:
                continue
            if booker_employee_ref is not None and b.booker_employee_ref != booker_employee_ref:
                continue
            if booking_status is not None and b.booking_status != booking_status:
                continue
            if booking_type is not None and b.booking_type != booking_type:
                continue
            if date_from is not None and b.start_at < date_from:
                continue
            if date_to is not None and b.start_at > date_to:
                continue
            results.append({
                "booking_ref": b.booking_ref,
                "facility_ref": b.facility_ref,
                "booker_employee_ref": b.booker_employee_ref,
                "booking_title": b.booking_title,
                "booking_type": b.booking_type,
                "start_at": b.start_at,
                "end_at": b.end_at,
                "attendee_count": b.attendee_count,
                "booking_status": b.booking_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_booking(
        self,
        facility_ref: str,
        booker_employee_ref: str,
        booking_title: str,
        booking_type: str,
        start_at: str,
        end_at: str,
        attendee_count: int,
        attendee_employee_refs: List[str],
        notes: str = "",
    ) -> Booking:
        """
        功能说明（Description）：
            新建场地预订。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `facility_ref` (str)；按函数语义传入。
            - `booker_employee_ref` (str)；按函数语义传入。
            - `booking_title` (str)；按函数语义传入。
            - `booking_type` (str)；按函数语义传入。
            - `start_at` (str)；按函数语义传入。
            - `end_at` (str)；按函数语义传入。
            - `attendee_count` (int)；按函数语义传入。
            - `attendee_employee_refs` (List[str])；按函数语义传入。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `Booking`: 新建对象，`booking_status` 一般为 `pending`。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        facility = self._get_facility(facility_ref)
        self._get_employee(booker_employee_ref)

        if not facility.is_bookable:
            raise ValueError("Facility is not bookable")
        if facility.facility_status not in ("available",):
            raise ValueError(f"Facility is not available for booking (status: {facility.facility_status})")
        if start_at >= end_at:
            raise ValueError("start_at must be before end_at")
        if attendee_count > facility.capacity:
            raise ValueError(
                f"Attendee count ({attendee_count}) exceeds facility capacity ({facility.capacity})"
            )

        valid_types = {"meeting", "interview", "training", "event", "other"}
        if booking_type not in valid_types:
            raise ValueError(f"Invalid booking_type: {booking_type}. Must be one of {valid_types}")

        now = self._now_iso()
        booking_ref = self._generate_ref("BKG", self.db.booking)

        booking = Booking(
            booking_ref=booking_ref,
            facility_ref=facility_ref,
            booker_employee_ref=booker_employee_ref,
            booking_title=booking_title,
            booking_type=booking_type,
            start_at=start_at,
            end_at=end_at,
            attendee_count=attendee_count,
            attendee_employee_refs=attendee_employee_refs,
            booking_status="pending",
            cancel_reason=None,
            cancelled_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.booking[booking_ref] = booking
        return booking

    @is_tool(ToolType.WRITE)
    def confirm_booking(self, booking_ref: str) -> Booking:
        """
        功能说明（Description）：
            将待确认的场地预订确认为已确认。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `booking_ref` (str)；按函数语义传入。
        返回（Returns）：
            `Booking`: 更新后的对象，`booking_status` 为 `confirmed`。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        booking = self._get_booking(booking_ref)
        if booking.booking_status != "pending":
            raise ValueError(
                f"Booking cannot be confirmed from status '{booking.booking_status}'. Must be 'pending'."
            )
        booking.booking_status = "confirmed"
        booking.updated_at = self._now_iso()
        return booking

    @is_tool(ToolType.WRITE)
    def cancel_booking(self, booking_ref: str, cancel_reason: str) -> Booking:
        """
        功能说明（Description）：
            取消已有场地预订。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `booking_ref` (str)；按函数语义传入。
            - `cancel_reason` (str)；按函数语义传入。
        返回（Returns）：
            `Booking`: 更新后的对象，`booking_status` 为 `cancelled`。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        booking = self._get_booking(booking_ref)
        if booking.booking_status in ("cancelled", "completed"):
            raise ValueError(
                f"Booking cannot be cancelled from status '{booking.booking_status}'."
            )
        now = self._now_iso()
        booking.booking_status = "cancelled"
        booking.cancel_reason = cancel_reason
        booking.cancelled_at = now
        booking.updated_at = now
        return booking

    # ----------------
    # 工位（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_workstation_details(self, workstation_ref: str) -> Workstation:
        """
        功能说明（Description）：
            根据引用 ID 获取工位的详细信息。
        参数（Parameters）：
            - `workstation_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Workstation`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_workstation(workstation_ref)

    @is_tool(ToolType.READ)
    def list_workstations(
        self,
        campus_ref: Optional[str] = None,
        building_ref: Optional[str] = None,
        floor_ref: Optional[str] = None,
        zone_ref: Optional[str] = None,
        workstation_type: Optional[str] = None,
        status: Optional[str] = None,
        assigned_employee_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出工位摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `floor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `zone_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `workstation_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `assigned_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的工位摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for ws_ref, ws in self.db.workstation.items():
            if campus_ref is not None and ws.campus_ref != campus_ref:
                continue
            if building_ref is not None and ws.building_ref != building_ref:
                continue
            if floor_ref is not None and ws.floor_ref != floor_ref:
                continue
            if zone_ref is not None and ws.zone_ref != zone_ref:
                continue
            if workstation_type is not None and ws.workstation_type != workstation_type:
                continue
            if status is not None and ws.workstation_status != status:
                continue
            if assigned_employee_ref is not None and ws.assigned_employee_ref != assigned_employee_ref:
                continue
            results.append({
                "workstation_ref": ws.workstation_ref,
                "workstation_code": ws.workstation_code,
                "zone_ref": ws.zone_ref,
                "floor_ref": ws.floor_ref,
                "building_ref": ws.building_ref,
                "campus_ref": ws.campus_ref,
                "workstation_type": ws.workstation_type,
                "workstation_status": ws.workstation_status,
                "assigned_employee_ref": ws.assigned_employee_ref,
                "amenities": ws.amenities,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_workstation(
        self,
        workstation_ref: str,
        employee_ref: str,
    ) -> Workstation:
        """
        功能说明（Description）：
            将工位分配给某员工。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `workstation_ref` (str)；按函数语义传入。
            - `employee_ref` (str)；按函数语义传入。
        返回（Returns）：
            `Workstation`: 更新后的工位对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        workstation = self._get_workstation(workstation_ref)
        self._get_employee(employee_ref)

        if workstation.workstation_status != "available":
            raise ValueError(
                f"Workstation is not available for assignment (status: {workstation.workstation_status})"
            )
        workstation.workstation_status = "occupied"
        workstation.assigned_employee_ref = employee_ref
        workstation.updated_at = self._now_iso()
        return workstation

    @is_tool(ToolType.WRITE)
    def unassign_workstation(self, workstation_ref: str) -> Workstation:
        """
        功能说明（Description）：
            解除工位与当前占用员工的绑定。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `workstation_ref` (str)；按函数语义传入。
        返回（Returns）：
            `Workstation`: 更新后的工位对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        workstation = self._get_workstation(workstation_ref)
        if workstation.workstation_status != "occupied":
            raise ValueError(
                f"Workstation is not currently occupied (status: {workstation.workstation_status})"
            )
        workstation.workstation_status = "available"
        workstation.assigned_employee_ref = None
        workstation.updated_at = self._now_iso()
        return workstation

    # ----------------
    # 储物柜（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_locker_details(self, locker_ref: str) -> Locker:
        """
        功能说明（Description）：
            根据引用 ID 获取储物柜的详细信息。
        参数（Parameters）：
            - `locker_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Locker`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_locker(locker_ref)

    @is_tool(ToolType.READ)
    def list_lockers(
        self,
        campus_ref: Optional[str] = None,
        building_ref: Optional[str] = None,
        floor_ref: Optional[str] = None,
        zone_ref: Optional[str] = None,
        locker_size: Optional[str] = None,
        status: Optional[str] = None,
        assigned_employee_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出储物柜摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `floor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `zone_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `locker_size` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `assigned_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的储物柜摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for l_ref, l in self.db.locker.items():
            if campus_ref is not None and l.campus_ref != campus_ref:
                continue
            if building_ref is not None and l.building_ref != building_ref:
                continue
            if floor_ref is not None and l.floor_ref != floor_ref:
                continue
            if zone_ref is not None and l.zone_ref != zone_ref:
                continue
            if locker_size is not None and l.locker_size != locker_size:
                continue
            if status is not None and l.locker_status != status:
                continue
            if assigned_employee_ref is not None and l.assigned_employee_ref != assigned_employee_ref:
                continue
            results.append({
                "locker_ref": l.locker_ref,
                "locker_code": l.locker_code,
                "zone_ref": l.zone_ref,
                "floor_ref": l.floor_ref,
                "building_ref": l.building_ref,
                "campus_ref": l.campus_ref,
                "locker_size": l.locker_size,
                "locker_status": l.locker_status,
                "assigned_employee_ref": l.assigned_employee_ref,
                "assigned_at": l.assigned_at,
                "expires_at": l.expires_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_locker(
        self,
        locker_ref: str,
        employee_ref: str,
        expires_at: Optional[str] = None,
    ) -> Locker:
        """
        功能说明（Description）：
            将储物柜分配给某员工。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `locker_ref` (str)；按函数语义传入。
            - `employee_ref` (str)；按函数语义传入。
            - `expires_at` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `Locker`: 更新后的储物柜对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        locker = self._get_locker(locker_ref)
        self._get_employee(employee_ref)

        if locker.locker_status != "available":
            raise ValueError(
                f"Locker is not available for assignment (status: {locker.locker_status})"
            )
        now = self._now_iso()
        locker.locker_status = "occupied"
        locker.assigned_employee_ref = employee_ref
        locker.assigned_at = now
        locker.expires_at = expires_at
        locker.updated_at = now
        return locker

    @is_tool(ToolType.WRITE)
    def release_locker(self, locker_ref: str) -> Locker:
        """
        功能说明（Description）：
            释放储物柜占用。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `locker_ref` (str)；按函数语义传入。
        返回（Returns）：
            `Locker`: 更新后的储物柜对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        locker = self._get_locker(locker_ref)
        if locker.locker_status != "occupied":
            raise ValueError(
                f"Locker is not currently occupied (status: {locker.locker_status})"
            )
        now = self._now_iso()
        locker.locker_status = "available"
        locker.assigned_employee_ref = None
        locker.assigned_at = None
        locker.expires_at = None
        locker.updated_at = now
        return locker

    # ----------------
    # 停车位（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_parking_space_details(self, parking_space_ref: str) -> ParkingSpace:
        """
        功能说明（Description）：
            根据引用 ID 获取停车位的详细信息。
        参数（Parameters）：
            - `parking_space_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ParkingSpace`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_parking_space(parking_space_ref)

    @is_tool(ToolType.READ)
    def list_parking_spaces(
        self,
        campus_ref: Optional[str] = None,
        parking_zone: Optional[str] = None,
        space_type: Optional[str] = None,
        ev_charging: Optional[bool] = None,
        status: Optional[str] = None,
        assigned_employee_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出停车位摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `parking_zone` (Optional[str])；默认为 None 表示不按此项筛选。
            - `space_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `ev_charging` (Optional[bool])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `assigned_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的停车位摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for ps_ref, ps in self.db.parking_space.items():
            if campus_ref is not None and ps.campus_ref != campus_ref:
                continue
            if parking_zone is not None and ps.parking_zone != parking_zone:
                continue
            if space_type is not None and ps.space_type != space_type:
                continue
            if ev_charging is not None and ps.ev_charging != ev_charging:
                continue
            if status is not None and ps.space_status != status:
                continue
            if assigned_employee_ref is not None and ps.assigned_employee_ref != assigned_employee_ref:
                continue
            results.append({
                "parking_space_ref": ps.parking_space_ref,
                "space_code": ps.space_code,
                "campus_ref": ps.campus_ref,
                "parking_zone": ps.parking_zone,
                "space_type": ps.space_type,
                "ev_charging": ps.ev_charging,
                "space_status": ps.space_status,
                "assigned_employee_ref": ps.assigned_employee_ref,
                "assigned_at": ps.assigned_at,
                "expires_at": ps.expires_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_parking_space(
        self,
        parking_space_ref: str,
        employee_ref: str,
        expires_at: Optional[str] = None,
    ) -> ParkingSpace:
        """
        功能说明（Description）：
            将停车位分配给某员工。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `parking_space_ref` (str)；按函数语义传入。
            - `employee_ref` (str)；按函数语义传入。
            - `expires_at` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `ParkingSpace`: 更新后的停车位对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        parking_space = self._get_parking_space(parking_space_ref)
        self._get_employee(employee_ref)

        if parking_space.space_status != "available":
            raise ValueError(
                f"Parking space is not available for assignment (status: {parking_space.space_status})"
            )
        now = self._now_iso()
        parking_space.space_status = "reserved"
        parking_space.assigned_employee_ref = employee_ref
        parking_space.assigned_at = now
        parking_space.expires_at = expires_at
        parking_space.updated_at = now
        return parking_space

    @is_tool(ToolType.WRITE)
    def release_parking_space(self, parking_space_ref: str) -> ParkingSpace:
        """
        功能说明（Description）：
            释放停车位占用。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `parking_space_ref` (str)；按函数语义传入。
        返回（Returns）：
            `ParkingSpace`: 更新后的停车位对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        parking_space = self._get_parking_space(parking_space_ref)
        if parking_space.space_status not in ("reserved", "occupied"):
            raise ValueError(
                f"Parking space is not currently assigned (status: {parking_space.space_status})"
            )
        now = self._now_iso()
        parking_space.space_status = "available"
        parking_space.assigned_employee_ref = None
        parking_space.assigned_at = None
        parking_space.expires_at = None
        parking_space.updated_at = now
        return parking_space

    # ----------------
    # 充电桩（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_ev_charger_details(self, ev_charger_ref: str) -> EvCharger:
        """
        功能说明（Description）：
            根据引用 ID 获取充电桩的详细信息。
        参数（Parameters）：
            - `ev_charger_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EvCharger`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_ev_charger(ev_charger_ref)

    @is_tool(ToolType.READ)
    def list_ev_chargers(
        self,
        campus_ref: Optional[str] = None,
        charger_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出充电桩摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `charger_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的充电桩摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for ec_ref, ec in self.db.ev_charger.items():
            if campus_ref is not None and ec.campus_ref != campus_ref:
                continue
            if charger_type is not None and ec.charger_type != charger_type:
                continue
            if status is not None and ec.charger_status != status:
                continue
            results.append({
                "ev_charger_ref": ec.ev_charger_ref,
                "charger_code": ec.charger_code,
                "campus_ref": ec.campus_ref,
                "parking_space_ref": ec.parking_space_ref,
                "charger_type": ec.charger_type,
                "power_kw": ec.power_kw,
                "charger_status": ec.charger_status,
                "fee_per_kwh": ec.fee_per_kwh,
                "operator": ec.operator,
            })
        return json.dumps(results)

    # ----------------
    # 班车（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_shuttle_route_details(self, shuttle_route_ref: str) -> ShuttleRoute:
        """
        功能说明（Description）：
            根据引用 ID 获取班车线路的详细信息。
        参数（Parameters）：
            - `shuttle_route_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleRoute`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_shuttle_route(shuttle_route_ref)

    @is_tool(ToolType.READ)
    def list_shuttle_routes(
        self,
        campus_ref: Optional[str] = None,
        direction: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出班车线路摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `direction` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的线路摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for sr_ref, sr in self.db.shuttle_route.items():
            if campus_ref is not None and sr.campus_ref != campus_ref:
                continue
            if direction is not None and sr.direction != direction:
                continue
            if status is not None and sr.route_status != status:
                continue
            results.append({
                "shuttle_route_ref": sr.shuttle_route_ref,
                "route_name": sr.route_name,
                "route_code": sr.route_code,
                "campus_ref": sr.campus_ref,
                "direction": sr.direction,
                "route_status": sr.route_status,
                "description": sr.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_shuttle_stops(self, shuttle_route_ref: str) -> str:
        """
        功能说明（Description）：
            列出某条班车线路上的站点（按顺序）。
        参数（Parameters）：
            - `shuttle_route_ref` (str)；按函数语义传入。
        返回（Returns）：
            `str`: JSON 编码的站点列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_shuttle_route(shuttle_route_ref)
        stops = []
        for ss_ref, ss in self.db.shuttle_stop.items():
            if ss.shuttle_route_ref == shuttle_route_ref:
                stops.append({
                    "shuttle_stop_ref": ss.shuttle_stop_ref,
                    "shuttle_route_ref": ss.shuttle_route_ref,
                    "stop_name": ss.stop_name,
                    "stop_order": ss.stop_order,
                    "geo_lat": ss.geo_lat,
                    "geo_lng": ss.geo_lng,
                })
        stops.sort(key=lambda x: x["stop_order"])
        return json.dumps(stops)

    @is_tool(ToolType.READ)
    def list_shuttle_schedules(
        self,
        shuttle_route_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出班车班次。
        参数（Parameters）：
            - `shuttle_route_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的班次列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if shuttle_route_ref is not None:
            self._get_shuttle_route(shuttle_route_ref)
        results = []
        for sched_ref, sched in self.db.shuttle_schedule.items():
            if shuttle_route_ref is not None and sched.shuttle_route_ref != shuttle_route_ref:
                continue
            if status is not None and sched.schedule_status != status:
                continue
            results.append({
                "shuttle_schedule_ref": sched.shuttle_schedule_ref,
                "shuttle_route_ref": sched.shuttle_route_ref,
                "depart_time": sched.depart_time,
                "effective_days": sched.effective_days,
                "seat_capacity": sched.seat_capacity,
                "schedule_status": sched.schedule_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_shuttle_booking_details(self, shuttle_booking_ref: str) -> ShuttleBooking:
        """
        功能说明（Description）：
            根据引用 ID 获取班车预订的详细信息。
        参数（Parameters）：
            - `shuttle_booking_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ShuttleBooking`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_shuttle_booking(shuttle_booking_ref)

    @is_tool(ToolType.READ)
    def list_shuttle_bookings_for_employee(
        self,
        employee_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出某员工的班车预订记录。
        参数（Parameters）：
            - `employee_ref` (str)；按函数语义传入。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的预订列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = []
        for sb_ref, sb in self.db.shuttle_booking.items():
            if sb.employee_ref != employee_ref:
                continue
            if status is not None and sb.booking_status != status:
                continue
            results.append({
                "shuttle_booking_ref": sb.shuttle_booking_ref,
                "shuttle_schedule_ref": sb.shuttle_schedule_ref,
                "employee_ref": sb.employee_ref,
                "ride_date": sb.ride_date,
                "boarding_stop_ref": sb.boarding_stop_ref,
                "booking_status": sb.booking_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_shuttle_booking(
        self,
        shuttle_schedule_ref: str,
        employee_ref: str,
        ride_date: str,
        boarding_stop_ref: str,
    ) -> ShuttleBooking:
        """
        功能说明（Description）：
            为员工新建班车预订。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `shuttle_schedule_ref` (str)；按函数语义传入。
            - `employee_ref` (str)；按函数语义传入。
            - `ride_date` (str)；按函数语义传入。
            - `boarding_stop_ref` (str)；按函数语义传入。
        返回（Returns）：
            `ShuttleBooking`: 新建的班车预订对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        schedule = self._get_shuttle_schedule(shuttle_schedule_ref)
        self._get_employee(employee_ref)
        stop = self._get_shuttle_stop(boarding_stop_ref)

        if schedule.schedule_status != "active":
            raise ValueError(
                f"Shuttle schedule is not active (status: {schedule.schedule_status})"
            )
        if stop.shuttle_route_ref != schedule.shuttle_route_ref:
            raise ValueError("Boarding stop does not belong to the schedule's route")

        now = self._now_iso()
        sb_ref = self._generate_ref("SB", self.db.shuttle_booking)

        shuttle_booking = ShuttleBooking(
            shuttle_booking_ref=sb_ref,
            shuttle_schedule_ref=shuttle_schedule_ref,
            employee_ref=employee_ref,
            ride_date=ride_date,
            boarding_stop_ref=boarding_stop_ref,
            booking_status="confirmed",
            created_at=now,
            updated_at=now,
        )
        self.db.shuttle_booking[sb_ref] = shuttle_booking
        return shuttle_booking

    @is_tool(ToolType.WRITE)
    def cancel_shuttle_booking(self, shuttle_booking_ref: str) -> ShuttleBooking:
        """
        功能说明（Description）：
            取消已有班车预订。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `shuttle_booking_ref` (str)；按函数语义传入。
        返回（Returns）：
            `ShuttleBooking`: 更新后的班车预订对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        booking = self._get_shuttle_booking(shuttle_booking_ref)
        if booking.booking_status != "confirmed":
            raise ValueError(
                f"Shuttle booking cannot be cancelled from status '{booking.booking_status}'"
            )
        booking.booking_status = "cancelled"
        booking.updated_at = self._now_iso()
        return booking

    # ----------------
    # 食堂（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_canteen_details(self, canteen_ref: str) -> Canteen:
        """
        功能说明（Description）：
            根据引用 ID 获取食堂的详细信息。
        参数（Parameters）：
            - `canteen_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Canteen`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_canteen(canteen_ref)

    @is_tool(ToolType.READ)
    def list_canteens(
        self,
        campus_ref: Optional[str] = None,
        canteen_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出食堂摘要。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `canteen_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的食堂摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for c_ref, c in self.db.canteen.items():
            if campus_ref is not None and c.campus_ref != campus_ref:
                continue
            if canteen_type is not None and c.canteen_type != canteen_type:
                continue
            if status is not None and c.canteen_status != status:
                continue
            results.append({
                "canteen_ref": c.canteen_ref,
                "campus_ref": c.campus_ref,
                "floor_ref": c.floor_ref,
                "canteen_name": c.canteen_name,
                "canteen_type": c.canteen_type,
                "open_hours": c.open_hours,
                "seat_capacity": c.seat_capacity,
                "canteen_status": c.canteen_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_canteen_menu_details(self, canteen_menu_ref: str) -> CanteenMenu:
        """
        功能说明（Description）：
            根据引用 ID 获取食堂菜单的详细信息。
        参数（Parameters）：
            - `canteen_menu_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CanteenMenu`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_canteen_menu(canteen_menu_ref)

    @is_tool(ToolType.READ)
    def list_canteen_menus(
        self,
        canteen_ref: Optional[str] = None,
        menu_date: Optional[str] = None,
        meal_type: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出食堂菜单。
        参数（Parameters）：
            - `canteen_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `menu_date` (Optional[str])；默认为 None 表示不按此项筛选。
            - `meal_type` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的菜单列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if canteen_ref is not None:
            self._get_canteen(canteen_ref)
        results = []
        for cm_ref, cm in self.db.canteen_menu.items():
            if canteen_ref is not None and cm.canteen_ref != canteen_ref:
                continue
            if menu_date is not None and cm.menu_date != menu_date:
                continue
            if meal_type is not None and cm.meal_type != meal_type:
                continue
            results.append({
                "canteen_menu_ref": cm.canteen_menu_ref,
                "canteen_ref": cm.canteen_ref,
                "menu_date": cm.menu_date,
                "meal_type": cm.meal_type,
                "dishes": [d.model_dump() for d in cm.dishes],
            })
        return json.dumps(results)

    # ----------------
    # 访客与预约（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_visitor_details(self, visitor_ref: str) -> Visitor:
        """
        功能说明（Description）：
            根据引用 ID 获取访客的详细信息。
        参数（Parameters）：
            - `visitor_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Visitor`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_visitor(visitor_ref)

    @is_tool(ToolType.READ)
    def search_visitors(
        self,
        name: Optional[str] = None,
        company: Optional[str] = None,
        visitor_type: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按姓名、公司等条件搜索访客。
        参数（Parameters）：
            - `name` (Optional[str])；默认为 None 表示不按此项筛选。
            - `company` (Optional[str])；默认为 None 表示不按此项筛选。
            - `visitor_type` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的访客列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for v_ref, v in self.db.visitor.items():
            if name is not None and name.lower() not in v.full_name.lower():
                continue
            if company is not None and company.lower() not in v.company.lower():
                continue
            if visitor_type is not None and v.visitor_type != visitor_type:
                continue
            results.append({
                "visitor_ref": v.visitor_ref,
                "full_name": v.full_name,
                "company": v.company,
                "visitor_type": v.visitor_type,
                "phone": v.phone,
                "email": v.email,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_visitor(
        self,
        full_name: str,
        id_type: str,
        id_number: str,
        phone: str,
        email: str,
        company: str,
        visitor_type: str,
    ) -> Visitor:
        """
        功能说明（Description）：
            新建访客档案。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `full_name` (str)；按函数语义传入。
            - `id_type` (str)；按函数语义传入。
            - `id_number` (str)；按函数语义传入。
            - `phone` (str)；按函数语义传入。
            - `email` (str)；按函数语义传入。
            - `company` (str)；按函数语义传入。
            - `visitor_type` (str)；按函数语义传入。
        返回（Returns）：
            `Visitor`: 新建的访客对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_id_types = {"id_card", "passport", "driver_license", "other"}
        if id_type not in valid_id_types:
            raise ValueError(f"Invalid id_type: {id_type}. Must be one of {valid_id_types}")

        valid_visitor_types = {"business", "government", "contractor", "personal", "other"}
        if visitor_type not in valid_visitor_types:
            raise ValueError(f"Invalid visitor_type: {visitor_type}. Must be one of {valid_visitor_types}")

        now = self._now_iso()
        visitor_ref = self._generate_ref("VIS", self.db.visitor)

        visitor = Visitor(
            visitor_ref=visitor_ref,
            full_name=full_name,
            id_type=id_type,
            id_number=id_number,
            phone=phone,
            email=email,
            company=company,
            visitor_type=visitor_type,
            created_at=now,
            updated_at=now,
        )
        self.db.visitor[visitor_ref] = visitor
        return visitor

    @is_tool(ToolType.READ)
    def get_visitor_appointment_details(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            根据引用 ID 获取访客预约的详细信息。
        参数（Parameters）：
            - `visitor_appointment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `VisitorAppointment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_visitor_appointment(visitor_appointment_ref)

    @is_tool(ToolType.READ)
    def list_visitor_appointments(
        self,
        host_employee_ref: Optional[str] = None,
        visitor_ref: Optional[str] = None,
        campus_ref: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出访客预约。
        参数（Parameters）：
            - `host_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `visitor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `date_from` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
            - `date_to` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的预约列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if host_employee_ref is not None:
            self._get_employee(host_employee_ref)
        if visitor_ref is not None:
            self._get_visitor(visitor_ref)
        if campus_ref is not None:
            self._get_campus(campus_ref)

        results = []
        for va_ref, va in self.db.visitor_appointment.items():
            if host_employee_ref is not None and va.host_employee_ref != host_employee_ref:
                continue
            if visitor_ref is not None and va.visitor_ref != visitor_ref:
                continue
            if campus_ref is not None and va.campus_ref != campus_ref:
                continue
            if status is not None and va.appointment_status != status:
                continue
            if date_from is not None and va.scheduled_start_at < date_from:
                continue
            if date_to is not None and va.scheduled_start_at > date_to:
                continue
            results.append({
                "visitor_appointment_ref": va.visitor_appointment_ref,
                "visitor_ref": va.visitor_ref,
                "host_employee_ref": va.host_employee_ref,
                "campus_ref": va.campus_ref,
                "visit_purpose": va.visit_purpose,
                "visit_type": va.visit_type,
                "scheduled_start_at": va.scheduled_start_at,
                "scheduled_end_at": va.scheduled_end_at,
                "appointment_status": va.appointment_status,
                "temp_access_level": va.temp_access_level,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_visitor_appointment(
        self,
        visitor_ref: str,
        host_employee_ref: str,
        campus_ref: str,
        visit_purpose: str,
        visit_type: str,
        scheduled_start_at: str,
        scheduled_end_at: str,
        temp_access_level: str,
        facility_ref: Optional[str] = None,
        notes: str = "",
    ) -> VisitorAppointment:
        """
        功能说明（Description）：
            新建访客预约。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `visitor_ref` (str)；按函数语义传入。
            - `host_employee_ref` (str)；按函数语义传入。
            - `campus_ref` (str)；按函数语义传入。
            - `visit_purpose` (str)；按函数语义传入。
            - `visit_type` (str)；按函数语义传入。
            - `scheduled_start_at` (str)；按函数语义传入。
            - `scheduled_end_at` (str)；按函数语义传入。
            - `temp_access_level` (str)；按函数语义传入。
            - `facility_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `VisitorAppointment`: 新建的预约对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_visitor(visitor_ref)
        self._get_employee(host_employee_ref)
        self._get_campus(campus_ref)

        if facility_ref is not None:
            self._get_facility(facility_ref)

        valid_visit_types = {"business", "interview", "delivery", "maintenance", "government", "personal", "other"}
        if visit_type not in valid_visit_types:
            raise ValueError(f"Invalid visit_type: {visit_type}. Must be one of {valid_visit_types}")

        valid_access_levels = {"lobby", "floor", "zone", "full"}
        if temp_access_level not in valid_access_levels:
            raise ValueError(f"Invalid temp_access_level: {temp_access_level}. Must be one of {valid_access_levels}")

        if scheduled_start_at >= scheduled_end_at:
            raise ValueError("scheduled_start_at must be before scheduled_end_at")

        now = self._now_iso()
        va_ref = self._generate_ref("VA", self.db.visitor_appointment)

        appointment = VisitorAppointment(
            visitor_appointment_ref=va_ref,
            visitor_ref=visitor_ref,
            host_employee_ref=host_employee_ref,
            campus_ref=campus_ref,
            visit_purpose=visit_purpose,
            visit_type=visit_type,
            scheduled_start_at=scheduled_start_at,
            scheduled_end_at=scheduled_end_at,
            actual_checkin_at=None,
            actual_checkout_at=None,
            facility_ref=facility_ref,
            temp_access_level=temp_access_level,
            appointment_status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.visitor_appointment[va_ref] = appointment
        return appointment

    @is_tool(ToolType.WRITE)
    def approve_visitor_appointment(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            审批通过待处理的访客预约。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `visitor_appointment_ref` (str)；按函数语义传入。
        返回（Returns）：
            `VisitorAppointment`: 更新后的预约对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        appointment = self._get_visitor_appointment(visitor_appointment_ref)
        if appointment.appointment_status != "pending":
            raise ValueError(
                f"Appointment cannot be approved from status '{appointment.appointment_status}'"
            )
        appointment.appointment_status = "approved"
        appointment.updated_at = self._now_iso()
        return appointment

    @is_tool(ToolType.WRITE)
    def reject_visitor_appointment(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            拒绝待处理的访客预约。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `visitor_appointment_ref` (str)；按函数语义传入。
        返回（Returns）：
            `VisitorAppointment`: 更新后的预约对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        appointment = self._get_visitor_appointment(visitor_appointment_ref)
        if appointment.appointment_status != "pending":
            raise ValueError(
                f"Appointment cannot be rejected from status '{appointment.appointment_status}'"
            )
        appointment.appointment_status = "rejected"
        appointment.updated_at = self._now_iso()
        return appointment

    @is_tool(ToolType.WRITE)
    def checkin_visitor(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            为已批准预约记录访客签到。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `visitor_appointment_ref` (str)；按函数语义传入。
        返回（Returns）：
            `VisitorAppointment`: 更新后的预约对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        appointment = self._get_visitor_appointment(visitor_appointment_ref)
        if appointment.appointment_status != "approved":
            raise ValueError(
                f"Visitor cannot check in from appointment status '{appointment.appointment_status}'"
            )
        now = self._now_iso()
        appointment.appointment_status = "checked_in"
        appointment.actual_checkin_at = now
        appointment.updated_at = now
        return appointment

    @is_tool(ToolType.WRITE)
    def checkout_visitor(self, visitor_appointment_ref: str) -> VisitorAppointment:
        """
        功能说明（Description）：
            为已签到访客记录签出。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `visitor_appointment_ref` (str)；按函数语义传入。
        返回（Returns）：
            `VisitorAppointment`: 更新后的预约对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        appointment = self._get_visitor_appointment(visitor_appointment_ref)
        if appointment.appointment_status != "checked_in":
            raise ValueError(
                f"Visitor cannot check out from appointment status '{appointment.appointment_status}'"
            )
        now = self._now_iso()
        appointment.appointment_status = "checked_out"
        appointment.actual_checkout_at = now
        appointment.updated_at = now
        return appointment

    # ----------------
    # 门禁卡（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_access_card_details(self, access_card_ref: str) -> AccessCard:
        """
        功能说明（Description）：
            根据引用 ID 获取门禁卡的详细信息。
        参数（Parameters）：
            - `access_card_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `AccessCard`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_access_card(access_card_ref)

    @is_tool(ToolType.READ)
    def list_access_cards(
        self,
        holder_ref: Optional[str] = None,
        campus_ref: Optional[str] = None,
        card_type: Optional[str] = None,
        card_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出门禁卡。
        参数（Parameters）：
            - `holder_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `card_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `card_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的门禁卡列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for ac_ref, ac in self.db.access_card.items():
            if holder_ref is not None and ac.holder_ref != holder_ref:
                continue
            if campus_ref is not None and ac.campus_ref != campus_ref:
                continue
            if card_type is not None and ac.card_type != card_type:
                continue
            if card_status is not None and ac.card_status != card_status:
                continue
            results.append({
                "access_card_ref": ac.access_card_ref,
                "card_number": ac.card_number,
                "card_type": ac.card_type,
                "holder_type": ac.holder_type,
                "holder_ref": ac.holder_ref,
                "campus_ref": ac.campus_ref,
                "access_zones": ac.access_zones,
                "card_status": ac.card_status,
                "issued_at": ac.issued_at,
                "expires_at": ac.expires_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_access_logs(
        self,
        access_card_ref: Optional[str] = None,
        campus_ref: Optional[str] = None,
        building_ref: Optional[str] = None,
        access_result: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出门禁刷卡日志。
        参数（Parameters）：
            - `access_card_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `access_result` (Optional[str])；默认为 None 表示不按此项筛选。
            - `date_from` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
            - `date_to` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的日志列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for al_ref, al in self.db.access_log.items():
            if access_card_ref is not None and al.access_card_ref != access_card_ref:
                continue
            if campus_ref is not None and al.campus_ref != campus_ref:
                continue
            if building_ref is not None and al.building_ref != building_ref:
                continue
            if access_result is not None and al.access_result != access_result:
                continue
            if date_from is not None and al.occurred_at < date_from:
                continue
            if date_to is not None and al.occurred_at > date_to:
                continue
            results.append({
                "access_log_ref": al.access_log_ref,
                "access_card_ref": al.access_card_ref,
                "campus_ref": al.campus_ref,
                "building_ref": al.building_ref,
                "access_point": al.access_point,
                "access_direction": al.access_direction,
                "access_result": al.access_result,
                "occurred_at": al.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def report_access_card_lost(self, access_card_ref: str) -> AccessCard:
        """
        功能说明（Description）：
            报失门禁卡。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `access_card_ref` (str)；按函数语义传入。
        返回（Returns）：
            `AccessCard`: 更新后的门禁卡对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        card = self._get_access_card(access_card_ref)
        if card.card_status != "active":
            raise ValueError(
                f"Access card cannot be reported lost from status '{card.card_status}'"
            )
        now = self._now_iso()
        card.card_status = "lost"
        card.lost_at = now
        card.updated_at = now
        return card

    @is_tool(ToolType.WRITE)
    def deactivate_access_card(self, access_card_ref: str) -> AccessCard:
        """
        功能说明（Description）：
            停用门禁卡。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `access_card_ref` (str)；按函数语义传入。
        返回（Returns）：
            `AccessCard`: 更新后的门禁卡对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        card = self._get_access_card(access_card_ref)
        if card.card_status in ("deactivated", "returned", "expired"):
            raise ValueError(
                f"Access card cannot be deactivated from status '{card.card_status}'"
            )
        card.card_status = "deactivated"
        card.updated_at = self._now_iso()
        return card

    # ----------------
    # 工牌（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_badge_details(self, badge_ref: str) -> Badge:
        """
        功能说明（Description）：
            根据引用 ID 获取工牌的详细信息。
        参数（Parameters）：
            - `badge_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Badge`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_badge(badge_ref)

    @is_tool(ToolType.READ)
    def list_badges_for_employee(
        self,
        employee_ref: str,
        badge_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出某员工名下的工牌。
        参数（Parameters）：
            - `employee_ref` (str)；按函数语义传入。
            - `badge_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的工牌列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = []
        for b_ref, b in self.db.badge.items():
            if b.employee_ref != employee_ref:
                continue
            if badge_status is not None and b.badge_status != badge_status:
                continue
            results.append({
                "badge_ref": b.badge_ref,
                "employee_ref": b.employee_ref,
                "badge_number": b.badge_number,
                "badge_type": b.badge_type,
                "badge_status": b.badge_status,
                "issued_at": b.issued_at,
                "expires_at": b.expires_at,
                "notes": b.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def report_badge_lost(self, badge_ref: str) -> Badge:
        """
        功能说明（Description）：
            报失工牌。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `badge_ref` (str)；按函数语义传入。
        返回（Returns）：
            `Badge`: 更新后的工牌对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        badge = self._get_badge(badge_ref)
        if badge.badge_status != "active":
            raise ValueError(
                f"Badge cannot be reported lost from status '{badge.badge_status}'"
            )
        now = self._now_iso()
        badge.badge_status = "lost"
        badge.lost_at = now
        badge.updated_at = now
        return badge

    # ----------------
    # 资产（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_asset_details(self, asset_ref: str) -> Asset:
        """
        功能说明（Description）：
            根据引用 ID 获取资产的详细信息。
        参数（Parameters）：
            - `asset_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Asset`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_asset(asset_ref)

    @is_tool(ToolType.READ)
    def list_assets(
        self,
        campus_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        custodian_employee_ref: Optional[str] = None,
        asset_category: Optional[str] = None,
        asset_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出资产。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `custodian_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `asset_category` (Optional[str])；默认为 None 表示不按此项筛选。
            - `asset_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的资产摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for a_ref, a in self.db.asset.items():
            if campus_ref is not None and a.campus_ref != campus_ref:
                continue
            if department_ref is not None and a.department_ref != department_ref:
                continue
            if custodian_employee_ref is not None and a.custodian_employee_ref != custodian_employee_ref:
                continue
            if asset_category is not None and a.asset_category != asset_category:
                continue
            if asset_status is not None and a.asset_status != asset_status:
                continue
            results.append({
                "asset_ref": a.asset_ref,
                "asset_name": a.asset_name,
                "asset_code": a.asset_code,
                "asset_category": a.asset_category,
                "asset_subcategory": a.asset_subcategory,
                "brand": a.brand,
                "model": a.model,
                "serial_number": a.serial_number,
                "campus_ref": a.campus_ref,
                "department_ref": a.department_ref,
                "custodian_employee_ref": a.custodian_employee_ref,
                "asset_status": a.asset_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_asset_request_details(self, asset_request_ref: str) -> AssetRequest:
        """
        功能说明（Description）：
            根据引用 ID 获取资产申请的详细信息。
        参数（Parameters）：
            - `asset_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `AssetRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_asset_request(asset_request_ref)

    @is_tool(ToolType.READ)
    def list_asset_requests(
        self,
        requester_employee_ref: Optional[str] = None,
        request_type: Optional[str] = None,
        request_status: Optional[str] = None,
        asset_category: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出资产申请。
        参数（Parameters）：
            - `requester_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `request_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `request_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `asset_category` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的申请列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if requester_employee_ref is not None:
            self._get_employee(requester_employee_ref)
        results = []
        for ar_ref, ar in self.db.asset_request.items():
            if requester_employee_ref is not None and ar.requester_employee_ref != requester_employee_ref:
                continue
            if request_type is not None and ar.request_type != request_type:
                continue
            if request_status is not None and ar.request_status != request_status:
                continue
            if asset_category is not None and ar.asset_category != asset_category:
                continue
            results.append({
                "asset_request_ref": ar.asset_request_ref,
                "requester_employee_ref": ar.requester_employee_ref,
                "request_type": ar.request_type,
                "asset_ref": ar.asset_ref,
                "asset_category": ar.asset_category,
                "asset_subcategory": ar.asset_subcategory,
                "quantity": ar.quantity,
                "reason": ar.reason,
                "request_status": ar.request_status,
                "created_at": ar.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_asset_request(
        self,
        requester_employee_ref: str,
        request_type: str,
        asset_category: str,
        asset_subcategory: str,
        quantity: int,
        reason: str,
        asset_ref: Optional[str] = None,
        expected_return_at: Optional[str] = None,
        notes: str = "",
    ) -> AssetRequest:
        """
        功能说明（Description）：
            新建资产领用/借用等申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `requester_employee_ref` (str)；按函数语义传入。
            - `request_type` (str)；按函数语义传入。
            - `asset_category` (str)；按函数语义传入。
            - `asset_subcategory` (str)；按函数语义传入。
            - `quantity` (int)；按函数语义传入。
            - `reason` (str)；按函数语义传入。
            - `asset_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `expected_return_at` (Optional[str])；默认为 None 表示不按此项筛选。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `AssetRequest`: 新建的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(requester_employee_ref)

        valid_request_types = {"apply", "borrow", "return", "repair", "scrap", "transfer"}
        if request_type not in valid_request_types:
            raise ValueError(f"Invalid request_type: {request_type}. Must be one of {valid_request_types}")

        valid_categories = {"it_equipment", "furniture", "vehicle", "office_equipment", "lab_equipment", "other"}
        if asset_category not in valid_categories:
            raise ValueError(f"Invalid asset_category: {asset_category}. Must be one of {valid_categories}")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if asset_ref is not None:
            self._get_asset(asset_ref)

        now = self._now_iso()
        ar_ref = self._generate_ref("AR", self.db.asset_request)

        asset_request = AssetRequest(
            asset_request_ref=ar_ref,
            requester_employee_ref=requester_employee_ref,
            request_type=request_type,
            asset_ref=asset_ref,
            asset_category=asset_category,
            asset_subcategory=asset_subcategory,
            quantity=quantity,
            reason=reason,
            expected_return_at=expected_return_at,
            request_status="pending",
            approved_by_ref=None,
            approved_at=None,
            reject_reason=None,
            fulfilled_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.asset_request[ar_ref] = asset_request
        return asset_request

    @is_tool(ToolType.WRITE)
    def approve_asset_request(
        self,
        asset_request_ref: str,
        approved_by_ref: str,
    ) -> AssetRequest:
        """
        功能说明（Description）：
            审批通过待处理的资产申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `asset_request_ref` (str)；按函数语义传入。
            - `approved_by_ref` (str)；按函数语义传入。
        返回（Returns）：
            `AssetRequest`: 更新后的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        asset_request = self._get_asset_request(asset_request_ref)
        self._get_employee(approved_by_ref)

        if asset_request.request_status != "pending":
            raise ValueError(
                f"Asset request cannot be approved from status '{asset_request.request_status}'"
            )
        now = self._now_iso()
        asset_request.request_status = "approved"
        asset_request.approved_by_ref = approved_by_ref
        asset_request.approved_at = now
        asset_request.updated_at = now
        return asset_request

    @is_tool(ToolType.WRITE)
    def reject_asset_request(
        self,
        asset_request_ref: str,
        approved_by_ref: str,
        reject_reason: str,
    ) -> AssetRequest:
        """
        功能说明（Description）：
            拒绝待处理的资产申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `asset_request_ref` (str)；按函数语义传入。
            - `approved_by_ref` (str)；按函数语义传入。
            - `reject_reason` (str)；按函数语义传入。
        返回（Returns）：
            `AssetRequest`: 更新后的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        asset_request = self._get_asset_request(asset_request_ref)
        self._get_employee(approved_by_ref)

        if asset_request.request_status != "pending":
            raise ValueError(
                f"Asset request cannot be rejected from status '{asset_request.request_status}'"
            )
        now = self._now_iso()
        asset_request.request_status = "rejected"
        asset_request.approved_by_ref = approved_by_ref
        asset_request.approved_at = now
        asset_request.reject_reason = reject_reason
        asset_request.updated_at = now
        return asset_request

    @is_tool(ToolType.READ)
    def list_asset_transactions(
        self,
        asset_ref: Optional[str] = None,
        asset_request_ref: Optional[str] = None,
        transaction_type: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出资产流转记录。
        参数（Parameters）：
            - `asset_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `asset_request_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `transaction_type` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的流转记录列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if asset_ref is not None:
            self._get_asset(asset_ref)
        if asset_request_ref is not None:
            self._get_asset_request(asset_request_ref)

        results = []
        for at_ref, at in self.db.asset_transaction.items():
            if asset_ref is not None and at.asset_ref != asset_ref:
                continue
            if asset_request_ref is not None and at.asset_request_ref != asset_request_ref:
                continue
            if transaction_type is not None and at.transaction_type != transaction_type:
                continue
            results.append({
                "asset_transaction_ref": at.asset_transaction_ref,
                "asset_request_ref": at.asset_request_ref,
                "asset_ref": at.asset_ref,
                "transaction_type": at.transaction_type,
                "from_employee_ref": at.from_employee_ref,
                "to_employee_ref": at.to_employee_ref,
                "operated_by_ref": at.operated_by_ref,
                "occurred_at": at.occurred_at,
                "notes": at.notes,
            })
        return json.dumps(results)

    # ----------------
    # 库存与领用（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_inventory_item_details(self, inventory_item_ref: str) -> InventoryItem:
        """
        功能说明（Description）：
            根据引用 ID 获取库存物料的详细信息。
        参数（Parameters）：
            - `inventory_item_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `InventoryItem`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_inventory_item(inventory_item_ref)

    @is_tool(ToolType.READ)
    def list_inventory_items(
        self,
        campus_ref: Optional[str] = None,
        item_category: Optional[str] = None,
        item_status: Optional[str] = None,
        low_stock_only: bool = False,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出库存物料。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `item_category` (Optional[str])；默认为 None 表示不按此项筛选。
            - `item_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `low_stock_only` (bool)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的库存条目列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for ii_ref, ii in self.db.inventory_item.items():
            if campus_ref is not None and ii.campus_ref != campus_ref:
                continue
            if item_category is not None and ii.item_category != item_category:
                continue
            if item_status is not None and ii.item_status != item_status:
                continue
            if low_stock_only and ii.current_stock > ii.min_stock_alert:
                continue
            results.append({
                "inventory_item_ref": ii.inventory_item_ref,
                "item_name": ii.item_name,
                "item_code": ii.item_code,
                "item_category": ii.item_category,
                "item_subcategory": ii.item_subcategory,
                "unit": ii.unit,
                "campus_ref": ii.campus_ref,
                "storage_location": ii.storage_location,
                "current_stock": ii.current_stock,
                "min_stock_alert": ii.min_stock_alert,
                "unit_cost": ii.unit_cost,
                "item_status": ii.item_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_supply_request_details(self, supply_request_ref: str) -> SupplyRequest:
        """
        功能说明（Description）：
            根据引用 ID 获取领用申请的详细信息。
        参数（Parameters）：
            - `supply_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SupplyRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_supply_request(supply_request_ref)

    @is_tool(ToolType.READ)
    def list_supply_requests(
        self,
        requester_employee_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        request_type: Optional[str] = None,
        request_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出领用申请。
        参数（Parameters）：
            - `requester_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `request_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `request_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的申请列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if requester_employee_ref is not None:
            self._get_employee(requester_employee_ref)
        if department_ref is not None:
            self._get_department(department_ref)

        results = []
        for sr_ref, sr in self.db.supply_request.items():
            if requester_employee_ref is not None and sr.requester_employee_ref != requester_employee_ref:
                continue
            if department_ref is not None and sr.department_ref != department_ref:
                continue
            if request_type is not None and sr.request_type != request_type:
                continue
            if request_status is not None and sr.request_status != request_status:
                continue
            results.append({
                "supply_request_ref": sr.supply_request_ref,
                "requester_employee_ref": sr.requester_employee_ref,
                "department_ref": sr.department_ref,
                "request_type": sr.request_type,
                "items": [i.model_dump() for i in sr.items],
                "reason": sr.reason,
                "request_status": sr.request_status,
                "created_at": sr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_supply_request(
        self,
        requester_employee_ref: str,
        department_ref: str,
        request_type: str,
        items: List[Dict],
        reason: str,
        expected_return_at: Optional[str] = None,
        notes: str = "",
    ) -> SupplyRequest:
        """
        功能说明（Description）：
            新建办公用品领用申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `requester_employee_ref` (str)；按函数语义传入。
            - `department_ref` (str)；按函数语义传入。
            - `request_type` (str)；按函数语义传入。
            - `items` (List[Dict])；按函数语义传入。
            - `reason` (str)；按函数语义传入。
            - `expected_return_at` (Optional[str])；默认为 None 表示不按此项筛选。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `SupplyRequest`: 新建的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(requester_employee_ref)
        self._get_department(department_ref)

        valid_request_types = {"borrow", "consume", "return"}
        if request_type not in valid_request_types:
            raise ValueError(f"Invalid request_type: {request_type}. Must be one of {valid_request_types}")

        if not items:
            raise ValueError("Items list cannot be empty")

        supply_items = []
        for item_dict in items:
            inv_ref = item_dict.get("inventory_item_ref")
            qty = item_dict.get("quantity", 0)
            if not inv_ref:
                raise ValueError("Each item must have an 'inventory_item_ref'")
            self._get_inventory_item(inv_ref)
            if qty <= 0:
                raise ValueError(f"Quantity for item {inv_ref} must be greater than 0")
            supply_items.append(SupplyRequestItem(inventory_item_ref=inv_ref, quantity=qty))

        now = self._now_iso()
        sr_ref = self._generate_ref("SR", self.db.supply_request)

        supply_request = SupplyRequest(
            supply_request_ref=sr_ref,
            requester_employee_ref=requester_employee_ref,
            department_ref=department_ref,
            request_type=request_type,
            items=supply_items,
            reason=reason,
            expected_return_at=expected_return_at,
            request_status="pending",
            approved_by_ref=None,
            approved_at=None,
            reject_reason=None,
            fulfilled_at=None,
            returned_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.supply_request[sr_ref] = supply_request
        return supply_request

    @is_tool(ToolType.WRITE)
    def approve_supply_request(
        self,
        supply_request_ref: str,
        approved_by_ref: str,
    ) -> SupplyRequest:
        """
        功能说明（Description）：
            审批通过待处理的领用申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `supply_request_ref` (str)；按函数语义传入。
            - `approved_by_ref` (str)；按函数语义传入。
        返回（Returns）：
            `SupplyRequest`: 更新后的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        supply_request = self._get_supply_request(supply_request_ref)
        self._get_employee(approved_by_ref)

        if supply_request.request_status != "pending":
            raise ValueError(
                f"Supply request cannot be approved from status '{supply_request.request_status}'"
            )
        now = self._now_iso()
        supply_request.request_status = "approved"
        supply_request.approved_by_ref = approved_by_ref
        supply_request.approved_at = now
        supply_request.updated_at = now
        return supply_request

    @is_tool(ToolType.WRITE)
    def reject_supply_request(
        self,
        supply_request_ref: str,
        approved_by_ref: str,
        reject_reason: str,
    ) -> SupplyRequest:
        """
        功能说明（Description）：
            拒绝待处理的领用申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `supply_request_ref` (str)；按函数语义传入。
            - `approved_by_ref` (str)；按函数语义传入。
            - `reject_reason` (str)；按函数语义传入。
        返回（Returns）：
            `SupplyRequest`: 更新后的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        supply_request = self._get_supply_request(supply_request_ref)
        self._get_employee(approved_by_ref)

        if supply_request.request_status != "pending":
            raise ValueError(
                f"Supply request cannot be rejected from status '{supply_request.request_status}'"
            )
        now = self._now_iso()
        supply_request.request_status = "rejected"
        supply_request.approved_by_ref = approved_by_ref
        supply_request.approved_at = now
        supply_request.reject_reason = reject_reason
        supply_request.updated_at = now
        return supply_request

    # ----------------
    # 报修（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_repair_request_details(self, repair_request_ref: str) -> RepairRequest:
        """
        功能说明（Description）：
            根据引用 ID 获取报修单的详细信息。
        参数（Parameters）：
            - `repair_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `RepairRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_repair_request(repair_request_ref)

    @is_tool(ToolType.READ)
    def list_repair_requests(
        self,
        reporter_employee_ref: Optional[str] = None,
        campus_ref: Optional[str] = None,
        building_ref: Optional[str] = None,
        resource_type: Optional[str] = None,
        urgency: Optional[str] = None,
        repair_status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出报修单。
        参数（Parameters）：
            - `reporter_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `building_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `resource_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `urgency` (Optional[str])；默认为 None 表示不按此项筛选。
            - `repair_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `assigned_to_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的报修单列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for rr_ref, rr in self.db.repair_request.items():
            if reporter_employee_ref is not None and rr.reporter_employee_ref != reporter_employee_ref:
                continue
            if campus_ref is not None and rr.campus_ref != campus_ref:
                continue
            if building_ref is not None and rr.building_ref != building_ref:
                continue
            if resource_type is not None and rr.resource_type != resource_type:
                continue
            if urgency is not None and rr.urgency != urgency:
                continue
            if repair_status is not None and rr.repair_status != repair_status:
                continue
            if assigned_to_ref is not None and rr.assigned_to_ref != assigned_to_ref:
                continue
            results.append({
                "repair_request_ref": rr.repair_request_ref,
                "reporter_employee_ref": rr.reporter_employee_ref,
                "resource_type": rr.resource_type,
                "resource_ref": rr.resource_ref,
                "campus_ref": rr.campus_ref,
                "building_ref": rr.building_ref,
                "floor_ref": rr.floor_ref,
                "fault_description": rr.fault_description,
                "urgency": rr.urgency,
                "repair_status": rr.repair_status,
                "assigned_to_ref": rr.assigned_to_ref,
                "created_at": rr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_repair_request(
        self,
        reporter_employee_ref: str,
        resource_type: str,
        resource_ref: str,
        campus_ref: str,
        building_ref: str,
        floor_ref: str,
        fault_description: str,
        urgency: str,
        fault_images: Optional[List[str]] = None,
    ) -> RepairRequest:
        """
        功能说明（Description）：
            新建报修单。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `reporter_employee_ref` (str)；按函数语义传入。
            - `resource_type` (str)；按函数语义传入。
            - `resource_ref` (str)；按函数语义传入。
            - `campus_ref` (str)；按函数语义传入。
            - `building_ref` (str)；按函数语义传入。
            - `floor_ref` (str)；按函数语义传入。
            - `fault_description` (str)；按函数语义传入。
            - `urgency` (str)；按函数语义传入。
            - `fault_images` (Optional[List[str]])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `RepairRequest`: 新建的报修单。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(reporter_employee_ref)
        self._get_campus(campus_ref)
        self._get_building(building_ref)
        self._get_floor(floor_ref)

        valid_resource_types = {"facility", "workstation", "equipment", "building", "zone", "other"}
        if resource_type not in valid_resource_types:
            raise ValueError(f"Invalid resource_type: {resource_type}. Must be one of {valid_resource_types}")

        valid_urgencies = {"low", "normal", "high", "critical"}
        if urgency not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {urgency}. Must be one of {valid_urgencies}")

        now = self._now_iso()
        rr_ref = self._generate_ref("RR", self.db.repair_request)

        repair_request = RepairRequest(
            repair_request_ref=rr_ref,
            reporter_employee_ref=reporter_employee_ref,
            resource_type=resource_type,
            resource_ref=resource_ref,
            campus_ref=campus_ref,
            building_ref=building_ref,
            floor_ref=floor_ref,
            fault_description=fault_description,
            fault_images=fault_images or [],
            urgency=urgency,
            repair_status="pending",
            assigned_to_ref=None,
            scheduled_at=None,
            completed_at=None,
            resolution_notes="",
            created_at=now,
            updated_at=now,
        )
        self.db.repair_request[rr_ref] = repair_request
        return repair_request

    @is_tool(ToolType.WRITE)
    def assign_repair_request(
        self,
        repair_request_ref: str,
        assigned_to_ref: str,
        scheduled_at: Optional[str] = None,
    ) -> RepairRequest:
        """
        功能说明（Description）：
            将报修单指派给维修人员并约定时间。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `repair_request_ref` (str)；按函数语义传入。
            - `assigned_to_ref` (str)；按函数语义传入。
            - `scheduled_at` (Optional[str])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `RepairRequest`: 更新后的报修单。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        repair_request = self._get_repair_request(repair_request_ref)
        self._get_employee(assigned_to_ref)

        if repair_request.repair_status != "pending":
            raise ValueError(
                f"Repair request cannot be assigned from status '{repair_request.repair_status}'"
            )
        now = self._now_iso()
        repair_request.repair_status = "assigned"
        repair_request.assigned_to_ref = assigned_to_ref
        repair_request.scheduled_at = scheduled_at
        repair_request.updated_at = now
        return repair_request

    @is_tool(ToolType.WRITE)
    def complete_repair_request(
        self,
        repair_request_ref: str,
        resolution_notes: str,
    ) -> RepairRequest:
        """
        功能说明（Description）：
            将报修单标记为已完成。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `repair_request_ref` (str)；按函数语义传入。
            - `resolution_notes` (str)；按函数语义传入。
        返回（Returns）：
            `RepairRequest`: 更新后的报修单。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        repair_request = self._get_repair_request(repair_request_ref)
        if repair_request.repair_status not in ("assigned", "in_progress"):
            raise ValueError(
                f"Repair request cannot be completed from status '{repair_request.repair_status}'"
            )
        now = self._now_iso()
        repair_request.repair_status = "completed"
        repair_request.resolution_notes = resolution_notes
        repair_request.completed_at = now
        repair_request.updated_at = now
        return repair_request

    # ----------------
    # 投诉（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_complaint_details(self, complaint_ref: str) -> Complaint:
        """
        功能说明（Description）：
            根据引用 ID 获取投诉的详细信息。
        参数（Parameters）：
            - `complaint_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Complaint`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_complaint(complaint_ref)

    @is_tool(ToolType.READ)
    def list_complaints(
        self,
        complainant_employee_ref: Optional[str] = None,
        complaint_category: Optional[str] = None,
        complaint_status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出投诉。
        参数（Parameters）：
            - `complainant_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `complaint_category` (Optional[str])；默认为 None 表示不按此项筛选。
            - `complaint_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `assigned_to_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的投诉列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if complainant_employee_ref is not None:
            self._get_employee(complainant_employee_ref)

        results = []
        for c_ref, c in self.db.complaint.items():
            if complainant_employee_ref is not None and c.complainant_employee_ref != complainant_employee_ref:
                continue
            if complaint_category is not None and c.complaint_category != complaint_category:
                continue
            if complaint_status is not None and c.complaint_status != complaint_status:
                continue
            if assigned_to_ref is not None and c.assigned_to_ref != assigned_to_ref:
                continue
            results.append({
                "complaint_ref": c.complaint_ref,
                "complainant_employee_ref": c.complainant_employee_ref,
                "complaint_category": c.complaint_category,
                "title": c.title,
                "complaint_status": c.complaint_status,
                "assigned_to_ref": c.assigned_to_ref,
                "created_at": c.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_complaint(
        self,
        complainant_employee_ref: str,
        complaint_category: str,
        title: str,
        description: str,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
        attachments: Optional[List[str]] = None,
    ) -> Complaint:
        """
        功能说明（Description）：
            新建投诉。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `complainant_employee_ref` (str)；按函数语义传入。
            - `complaint_category` (str)；按函数语义传入。
            - `title` (str)；按函数语义传入。
            - `description` (str)；按函数语义传入。
            - `related_resource_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `related_resource_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `attachments` (Optional[List[str]])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `Complaint`: 新建的投诉对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(complainant_employee_ref)

        valid_categories = {"canteen", "facility", "security", "it", "hr", "admin", "other"}
        if complaint_category not in valid_categories:
            raise ValueError(f"Invalid complaint_category: {complaint_category}. Must be one of {valid_categories}")

        now = self._now_iso()
        c_ref = self._generate_ref("CMP", self.db.complaint)

        complaint = Complaint(
            complaint_ref=c_ref,
            complainant_employee_ref=complainant_employee_ref,
            complaint_category=complaint_category,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            title=title,
            description=description,
            attachments=attachments or [],
            complaint_status="open",
            assigned_to_ref=None,
            resolved_at=None,
            resolution_notes="",
            created_at=now,
            updated_at=now,
        )
        self.db.complaint[c_ref] = complaint
        return complaint

    @is_tool(ToolType.WRITE)
    def resolve_complaint(
        self,
        complaint_ref: str,
        resolution_notes: str,
    ) -> Complaint:
        """
        功能说明（Description）：
            将投诉标记为已解决。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `complaint_ref` (str)；按函数语义传入。
            - `resolution_notes` (str)；按函数语义传入。
        返回（Returns）：
            `Complaint`: 更新后的投诉对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        complaint = self._get_complaint(complaint_ref)
        if complaint.complaint_status in ("resolved", "closed", "rejected"):
            raise ValueError(
                f"Complaint cannot be resolved from status '{complaint.complaint_status}'"
            )
        now = self._now_iso()
        complaint.complaint_status = "resolved"
        complaint.resolution_notes = resolution_notes
        complaint.resolved_at = now
        complaint.updated_at = now
        return complaint

    # ----------------
    # 失物招领（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_lost_found_details(self, lost_found_ref: str) -> LostFound:
        """
        功能说明（Description）：
            根据引用 ID 获取失物招领记录的详细信息。
        参数（Parameters）：
            - `lost_found_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LostFound`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_lost_found(lost_found_ref)

    @is_tool(ToolType.READ)
    def list_lost_found_records(
        self,
        record_type: Optional[str] = None,
        campus_ref: Optional[str] = None,
        reporter_employee_ref: Optional[str] = None,
        record_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出失物招领记录。
        参数（Parameters）：
            - `record_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `reporter_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `record_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的记录列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for lf_ref, lf in self.db.lost_found.items():
            if record_type is not None and lf.record_type != record_type:
                continue
            if campus_ref is not None and lf.campus_ref != campus_ref:
                continue
            if reporter_employee_ref is not None and lf.reporter_employee_ref != reporter_employee_ref:
                continue
            if record_status is not None and lf.record_status != record_status:
                continue
            results.append({
                "lost_found_ref": lf.lost_found_ref,
                "record_type": lf.record_type,
                "reporter_employee_ref": lf.reporter_employee_ref,
                "item_name": lf.item_name,
                "item_description": lf.item_description,
                "campus_ref": lf.campus_ref,
                "location_description": lf.location_description,
                "occurred_date": lf.occurred_date,
                "record_status": lf.record_status,
                "matched_ref": lf.matched_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_lost_found_record(
        self,
        record_type: str,
        reporter_employee_ref: str,
        item_name: str,
        item_description: str,
        campus_ref: str,
        location_description: str,
        occurred_date: str,
        item_images: Optional[List[str]] = None,
        notes: str = "",
    ) -> LostFound:
        """
        功能说明（Description）：
            新建失物或招领登记。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `record_type` (str)；按函数语义传入。
            - `reporter_employee_ref` (str)；按函数语义传入。
            - `item_name` (str)；按函数语义传入。
            - `item_description` (str)；按函数语义传入。
            - `campus_ref` (str)；按函数语义传入。
            - `location_description` (str)；按函数语义传入。
            - `occurred_date` (str)；按函数语义传入。
            - `item_images` (Optional[List[str]])；默认为 None 表示不按此项筛选。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `LostFound`: 新建的记录对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(reporter_employee_ref)
        self._get_campus(campus_ref)

        valid_record_types = {"lost", "found"}
        if record_type not in valid_record_types:
            raise ValueError(f"Invalid record_type: {record_type}. Must be one of {valid_record_types}")

        now = self._now_iso()
        lf_ref = self._generate_ref("LF", self.db.lost_found)

        lost_found = LostFound(
            lost_found_ref=lf_ref,
            record_type=record_type,
            reporter_employee_ref=reporter_employee_ref,
            item_name=item_name,
            item_description=item_description,
            item_images=item_images or [],
            campus_ref=campus_ref,
            location_description=location_description,
            occurred_date=occurred_date,
            matched_ref=None,
            record_status="open",
            claimed_by_ref=None,
            claimed_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.lost_found[lf_ref] = lost_found
        return lost_found

    @is_tool(ToolType.WRITE)
    def claim_lost_found_item(
        self,
        lost_found_ref: str,
        claimed_by_ref: str,
    ) -> LostFound:
        """
        功能说明（Description）：
            将招领物品标记为已被领取。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `lost_found_ref` (str)；按函数语义传入。
            - `claimed_by_ref` (str)；按函数语义传入。
        返回（Returns）：
            `LostFound`: 更新后的记录对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        lost_found = self._get_lost_found(lost_found_ref)
        self._get_employee(claimed_by_ref)

        if lost_found.record_status not in ("open", "matched"):
            raise ValueError(
                f"Lost and found record cannot be claimed from status '{lost_found.record_status}'"
            )
        now = self._now_iso()
        lost_found.record_status = "claimed"
        lost_found.claimed_by_ref = claimed_by_ref
        lost_found.claimed_at = now
        lost_found.updated_at = now
        return lost_found

    # ----------------
    # 安全事件（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_security_incident_details(self, security_incident_ref: str) -> SecurityIncident:
        """
        功能说明（Description）：
            根据引用 ID 获取安全事件的详细信息。
        参数（Parameters）：
            - `security_incident_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SecurityIncident`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_security_incident(security_incident_ref)

    @is_tool(ToolType.READ)
    def list_security_incidents(
        self,
        campus_ref: Optional[str] = None,
        incident_type: Optional[str] = None,
        severity: Optional[str] = None,
        incident_status: Optional[str] = None,
        reporter_employee_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出安全事件。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `incident_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `severity` (Optional[str])；默认为 None 表示不按此项筛选。
            - `incident_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `reporter_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的事件列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for si_ref, si in self.db.security_incident.items():
            if campus_ref is not None and si.campus_ref != campus_ref:
                continue
            if incident_type is not None and si.incident_type != incident_type:
                continue
            if severity is not None and si.severity != severity:
                continue
            if incident_status is not None and si.incident_status != incident_status:
                continue
            if reporter_employee_ref is not None and si.reporter_employee_ref != reporter_employee_ref:
                continue
            results.append({
                "security_incident_ref": si.security_incident_ref,
                "reporter_employee_ref": si.reporter_employee_ref,
                "campus_ref": si.campus_ref,
                "incident_type": si.incident_type,
                "severity": si.severity,
                "title": si.title,
                "incident_status": si.incident_status,
                "occurred_at": si.occurred_at,
                "created_at": si.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_security_incident(
        self,
        reporter_employee_ref: str,
        campus_ref: str,
        incident_type: str,
        severity: str,
        title: str,
        description: str,
        occurred_at: str,
        location_description: str,
        involved_parties: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
    ) -> SecurityIncident:
        """
        功能说明（Description）：
            新建安全事件上报。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `reporter_employee_ref` (str)；按函数语义传入。
            - `campus_ref` (str)；按函数语义传入。
            - `incident_type` (str)；按函数语义传入。
            - `severity` (str)；按函数语义传入。
            - `title` (str)；按函数语义传入。
            - `description` (str)；按函数语义传入。
            - `occurred_at` (str)；按函数语义传入。
            - `location_description` (str)；按函数语义传入。
            - `involved_parties` (Optional[List[str]])；默认为 None 表示不按此项筛选。
            - `attachments` (Optional[List[str]])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `SecurityIncident`: 新建的事件对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(reporter_employee_ref)
        self._get_campus(campus_ref)

        valid_incident_types = {"intrusion", "theft", "vandalism", "fire", "medical", "safety_hazard", "data_breach", "other"}
        if incident_type not in valid_incident_types:
            raise ValueError(f"Invalid incident_type: {incident_type}. Must be one of {valid_incident_types}")

        valid_severities = {"low", "medium", "high", "critical"}
        if severity not in valid_severities:
            raise ValueError(f"Invalid severity: {severity}. Must be one of {valid_severities}")

        now = self._now_iso()
        si_ref = self._generate_ref("SI", self.db.security_incident)

        incident = SecurityIncident(
            security_incident_ref=si_ref,
            reporter_employee_ref=reporter_employee_ref,
            campus_ref=campus_ref,
            incident_type=incident_type,
            severity=severity,
            title=title,
            description=description,
            occurred_at=occurred_at,
            location_description=location_description,
            involved_parties=involved_parties or [],
            attachments=attachments or [],
            incident_status="open",
            assigned_to_ref=None,
            resolved_at=None,
            resolution_notes="",
            created_at=now,
            updated_at=now,
        )
        self.db.security_incident[si_ref] = incident
        return incident

    @is_tool(ToolType.WRITE)
    def resolve_security_incident(
        self,
        security_incident_ref: str,
        resolution_notes: str,
    ) -> SecurityIncident:
        """
        功能说明（Description）：
            将安全事件标记为已结案。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `security_incident_ref` (str)；按函数语义传入。
            - `resolution_notes` (str)；按函数语义传入。
        返回（Returns）：
            `SecurityIncident`: 更新后的事件对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        incident = self._get_security_incident(security_incident_ref)
        if incident.incident_status in ("resolved", "closed"):
            raise ValueError(
                f"Security incident cannot be resolved from status '{incident.incident_status}'"
            )
        now = self._now_iso()
        incident.incident_status = "resolved"
        incident.resolution_notes = resolution_notes
        incident.resolved_at = now
        incident.updated_at = now
        return incident

    # ----------------
    # 礼品（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_gift_details(self, gift_ref: str) -> Gift:
        """
        功能说明（Description）：
            根据引用 ID 获取礼品的详细信息。
        参数（Parameters）：
            - `gift_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Gift`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_gift(gift_ref)

    @is_tool(ToolType.READ)
    def list_gifts(
        self,
        campus_ref: Optional[str] = None,
        gift_status: Optional[str] = None,
        low_stock_only: bool = False,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出礼品条目。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `gift_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `low_stock_only` (bool)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的礼品列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if campus_ref is not None:
            self._get_campus(campus_ref)
        results = []
        for g_ref, g in self.db.gift.items():
            if campus_ref is not None and g.campus_ref != campus_ref:
                continue
            if gift_status is not None and g.gift_status != gift_status:
                continue
            if low_stock_only and g.current_stock > g.min_stock_alert:
                continue
            results.append({
                "gift_ref": g.gift_ref,
                "gift_name": g.gift_name,
                "gift_code": g.gift_code,
                "gift_category": g.gift_category,
                "unit_cost": g.unit_cost,
                "current_stock": g.current_stock,
                "min_stock_alert": g.min_stock_alert,
                "storage_location": g.storage_location,
                "campus_ref": g.campus_ref,
                "gift_status": g.gift_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_gift_records(
        self,
        gift_ref: Optional[str] = None,
        operated_by_ref: Optional[str] = None,
        recipient_type: Optional[str] = None,
        recipient_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出礼品领用/发放记录。
        参数（Parameters）：
            - `gift_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `operated_by_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `recipient_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `recipient_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的记录列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if gift_ref is not None:
            self._get_gift(gift_ref)

        results = []
        for gr_ref, gr in self.db.gift_record.items():
            if gift_ref is not None and gr.gift_ref != gift_ref:
                continue
            if operated_by_ref is not None and gr.operated_by_ref != operated_by_ref:
                continue
            if recipient_type is not None and gr.recipient_type != recipient_type:
                continue
            if recipient_ref is not None and gr.recipient_ref != recipient_ref:
                continue
            results.append({
                "gift_record_ref": gr.gift_record_ref,
                "gift_ref": gr.gift_ref,
                "operated_by_ref": gr.operated_by_ref,
                "recipient_type": gr.recipient_type,
                "recipient_ref": gr.recipient_ref,
                "quantity": gr.quantity,
                "occasion": gr.occasion,
                "notes": gr.notes,
                "created_at": gr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_gift_record(
        self,
        gift_ref: str,
        operated_by_ref: str,
        recipient_type: str,
        recipient_ref: str,
        quantity: int,
        occasion: str,
        notes: str = "",
    ) -> GiftRecord:
        """
        功能说明（Description）：
            登记礼品发放/领用记录。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `gift_ref` (str)；按函数语义传入。
            - `operated_by_ref` (str)；按函数语义传入。
            - `recipient_type` (str)；按函数语义传入。
            - `recipient_ref` (str)；按函数语义传入。
            - `quantity` (int)；按函数语义传入。
            - `occasion` (str)；按函数语义传入。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `GiftRecord`: 新建的发放记录。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        gift = self._get_gift(gift_ref)
        self._get_employee(operated_by_ref)

        valid_recipient_types = {"employee", "department", "team", "visitor", "external_partner"}
        if recipient_type not in valid_recipient_types:
            raise ValueError(f"Invalid recipient_type: {recipient_type}. Must be one of {valid_recipient_types}")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if gift.current_stock < quantity:
            raise ValueError(
                f"Insufficient stock. Available: {gift.current_stock}, Requested: {quantity}"
            )

        now = self._now_iso()
        gr_ref = self._generate_ref("GR", self.db.gift_record)

        gift_record = GiftRecord(
            gift_record_ref=gr_ref,
            gift_ref=gift_ref,
            operated_by_ref=operated_by_ref,
            recipient_type=recipient_type,
            recipient_ref=recipient_ref,
            quantity=quantity,
            occasion=occasion,
            notes=notes,
            created_at=now,
        )
        self.db.gift_record[gr_ref] = gift_record

        # 扣减库存
        gift.current_stock -= quantity
        gift.updated_at = now

        return gift_record

    # ----------------
    # 名片（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_business_card_details(self, business_card_ref: str) -> BusinessCard:
        """
        功能说明（Description）：
            根据引用 ID 获取名片印制申请的详细信息。
        参数（Parameters）：
            - `business_card_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BusinessCard`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_business_card(business_card_ref)

    @is_tool(ToolType.READ)
    def list_business_cards_for_employee(
        self,
        employee_ref: str,
        request_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出某员工的名片印制申请。
        参数（Parameters）：
            - `employee_ref` (str)；按函数语义传入。
            - `request_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的申请列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = []
        for bc_ref, bc in self.db.business_card.items():
            if bc.employee_ref != employee_ref:
                continue
            if request_status is not None and bc.request_status != request_status:
                continue
            results.append({
                "business_card_ref": bc.business_card_ref,
                "employee_ref": bc.employee_ref,
                "card_template": bc.card_template,
                "custom_fields": bc.custom_fields,
                "quantity": bc.quantity,
                "request_status": bc.request_status,
                "created_at": bc.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_business_card_request(
        self,
        employee_ref: str,
        card_template: str,
        quantity: int,
        custom_fields: Optional[Dict] = None,
        notes: str = "",
    ) -> BusinessCard:
        """
        功能说明（Description）：
            新建名片印制申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `employee_ref` (str)；按函数语义传入。
            - `card_template` (str)；按函数语义传入。
            - `quantity` (int)；按函数语义传入。
            - `custom_fields` (Optional[Dict])；默认为 None 表示不按此项筛选。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `BusinessCard`: 新建的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        valid_templates = {"standard", "executive", "bilingual", "custom"}
        if card_template not in valid_templates:
            raise ValueError(f"Invalid card_template: {card_template}. Must be one of {valid_templates}")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        now = self._now_iso()
        bc_ref = self._generate_ref("BC", self.db.business_card)

        business_card = BusinessCard(
            business_card_ref=bc_ref,
            employee_ref=employee_ref,
            card_template=card_template,
            custom_fields=custom_fields or {},
            quantity=quantity,
            request_status="pending",
            approved_by_ref=None,
            approved_at=None,
            delivered_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.business_card[bc_ref] = business_card
        return business_card

    @is_tool(ToolType.WRITE)
    def approve_business_card_request(
        self,
        business_card_ref: str,
        approved_by_ref: str,
    ) -> BusinessCard:
        """
        功能说明（Description）：
            审批通过待处理的名片印制申请。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `business_card_ref` (str)；按函数语义传入。
            - `approved_by_ref` (str)；按函数语义传入。
        返回（Returns）：
            `BusinessCard`: 更新后的申请对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        business_card = self._get_business_card(business_card_ref)
        self._get_employee(approved_by_ref)

        if business_card.request_status != "pending":
            raise ValueError(
                f"Business card request cannot be approved from status '{business_card.request_status}'"
            )
        now = self._now_iso()
        business_card.request_status = "approved"
        business_card.approved_by_ref = approved_by_ref
        business_card.approved_at = now
        business_card.updated_at = now
        return business_card

    # ----------------
    # 公司活动（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_company_event_details(self, company_event_ref: str) -> CompanyEvent:
        """
        功能说明（Description）：
            根据引用 ID 获取公司活动的详细信息。
        参数（Parameters）：
            - `company_event_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CompanyEvent`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_company_event(company_event_ref)

    @is_tool(ToolType.READ)
    def list_company_events(
        self,
        campus_ref: Optional[str] = None,
        event_type: Optional[str] = None,
        event_status: Optional[str] = None,
        organizer_employee_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出公司活动。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `event_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `event_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `organizer_employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `date_from` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
            - `date_to` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的活动摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for ce_ref, ce in self.db.company_event.items():
            if campus_ref is not None and ce.campus_ref != campus_ref:
                continue
            if event_type is not None and ce.event_type != event_type:
                continue
            if event_status is not None and ce.event_status != event_status:
                continue
            if organizer_employee_ref is not None and ce.organizer_employee_ref != organizer_employee_ref:
                continue
            if department_ref is not None and ce.department_ref != department_ref:
                continue
            if date_from is not None and ce.start_at < date_from:
                continue
            if date_to is not None and ce.start_at > date_to:
                continue
            results.append({
                "company_event_ref": ce.company_event_ref,
                "event_name": ce.event_name,
                "event_type": ce.event_type,
                "campus_ref": ce.campus_ref,
                "facility_ref": ce.facility_ref,
                "organizer_employee_ref": ce.organizer_employee_ref,
                "department_ref": ce.department_ref,
                "start_at": ce.start_at,
                "end_at": ce.end_at,
                "max_attendees": ce.max_attendees,
                "event_status": ce.event_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_company_event(
        self,
        event_name: str,
        event_type: str,
        campus_ref: str,
        organizer_employee_ref: str,
        start_at: str,
        end_at: str,
        description: str,
        facility_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        max_attendees: Optional[int] = None,
        attachments: Optional[List[str]] = None,
    ) -> CompanyEvent:
        """
        功能说明（Description）：
            新建公司活动。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `event_name` (str)；按函数语义传入。
            - `event_type` (str)；按函数语义传入。
            - `campus_ref` (str)；按函数语义传入。
            - `organizer_employee_ref` (str)；按函数语义传入。
            - `start_at` (str)；按函数语义传入。
            - `end_at` (str)；按函数语义传入。
            - `description` (str)；按函数语义传入。
            - `facility_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `max_attendees` (Optional[int])；默认为 None 表示不按此项筛选。
            - `attachments` (Optional[List[str]])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `CompanyEvent`: 新建的活动对象，`event_status` 一般为 `planned`。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_campus(campus_ref)
        self._get_employee(organizer_employee_ref)

        if facility_ref is not None:
            self._get_facility(facility_ref)
        if department_ref is not None:
            self._get_department(department_ref)

        valid_event_types = {"company_day", "team_building", "training", "seminar", "celebration", "sports", "charity", "other"}
        if event_type not in valid_event_types:
            raise ValueError(f"Invalid event_type: {event_type}. Must be one of {valid_event_types}")

        if start_at >= end_at:
            raise ValueError("start_at must be before end_at")

        now = self._now_iso()
        ce_ref = self._generate_ref("CE", self.db.company_event)

        company_event = CompanyEvent(
            company_event_ref=ce_ref,
            event_name=event_name,
            event_type=event_type,
            campus_ref=campus_ref,
            facility_ref=facility_ref,
            organizer_employee_ref=organizer_employee_ref,
            department_ref=department_ref,
            start_at=start_at,
            end_at=end_at,
            max_attendees=max_attendees,
            description=description,
            attachments=attachments or [],
            event_status="planned",
            created_at=now,
            updated_at=now,
        )
        self.db.company_event[ce_ref] = company_event
        return company_event

    @is_tool(ToolType.WRITE)
    def cancel_company_event(self, company_event_ref: str) -> CompanyEvent:
        """
        功能说明（Description）：
            取消计划中的公司活动。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `company_event_ref` (str)；按函数语义传入。
        返回（Returns）：
            `CompanyEvent`: 更新后的活动对象。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        event = self._get_company_event(company_event_ref)
        if event.event_status in ("completed", "cancelled"):
            raise ValueError(
                f"Company event cannot be cancelled from status '{event.event_status}'"
            )
        event.event_status = "cancelled"
        event.updated_at = self._now_iso()
        return event

    @is_tool(ToolType.READ)
    def list_event_registrations(
        self,
        company_event_ref: Optional[str] = None,
        employee_ref: Optional[str] = None,
        registration_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出活动报名。
        参数（Parameters）：
            - `company_event_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `employee_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `registration_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的报名列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if company_event_ref is not None:
            self._get_company_event(company_event_ref)
        if employee_ref is not None:
            self._get_employee(employee_ref)

        results = []
        for er_ref, er in self.db.event_registration.items():
            if company_event_ref is not None and er.company_event_ref != company_event_ref:
                continue
            if employee_ref is not None and er.employee_ref != employee_ref:
                continue
            if registration_status is not None and er.registration_status != registration_status:
                continue
            results.append({
                "event_registration_ref": er.event_registration_ref,
                "company_event_ref": er.company_event_ref,
                "employee_ref": er.employee_ref,
                "registration_status": er.registration_status,
                "checked_in_at": er.checked_in_at,
                "notes": er.notes,
                "created_at": er.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def register_for_event(
        self,
        company_event_ref: str,
        employee_ref: str,
        notes: str = "",
    ) -> EventRegistration:
        """
        功能说明（Description）：
            为员工报名参加活动。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `company_event_ref` (str)；按函数语义传入。
            - `employee_ref` (str)；按函数语义传入。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `EventRegistration`: 新建的报名记录。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        event = self._get_company_event(company_event_ref)
        self._get_employee(employee_ref)

        if event.event_status not in ("planned", "ongoing"):
            raise ValueError(
                f"Cannot register for event with status '{event.event_status}'"
            )

        # 检查是否已报名（非取消状态）
        for er in self.db.event_registration.values():
            if er.company_event_ref == company_event_ref and er.employee_ref == employee_ref:
                if er.registration_status not in ("cancelled",):
                    raise ValueError("Employee is already registered for this event")

        # 检查人数上限
        if event.max_attendees is not None:
            active_count = sum(
                1 for er in self.db.event_registration.values()
                if er.company_event_ref == company_event_ref
                and er.registration_status in ("registered", "waitlisted", "attended")
            )
            if active_count >= event.max_attendees:
                status = "waitlisted"
            else:
                status = "registered"
        else:
            status = "registered"

        now = self._now_iso()
        er_ref = self._generate_ref("ER", self.db.event_registration)

        registration = EventRegistration(
            event_registration_ref=er_ref,
            company_event_ref=company_event_ref,
            employee_ref=employee_ref,
            registration_status=status,
            checked_in_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.event_registration[er_ref] = registration
        return registration

    @is_tool(ToolType.WRITE)
    def cancel_event_registration(self, event_registration_ref: str) -> EventRegistration:
        """
        功能说明（Description）：
            取消活动报名。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `event_registration_ref` (str)；按函数语义传入。
        返回（Returns）：
            `EventRegistration`: 更新后的报名记录。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        registration = self._get_event_registration(event_registration_ref)
        if registration.registration_status in ("cancelled", "attended", "no_show"):
            raise ValueError(
                f"Event registration cannot be cancelled from status '{registration.registration_status}'"
            )
        registration.registration_status = "cancelled"
        registration.updated_at = self._now_iso()
        return registration

    # ----------------
    # 制度/政策（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_policy_details(self, policy_ref: str) -> Policy:
        """
        功能说明（Description）：
            根据引用 ID 获取制度/政策的详细信息。
        参数（Parameters）：
            - `policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Policy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_policy(policy_ref)

    @is_tool(ToolType.READ)
    def list_policies(
        self,
        policy_category: Optional[str] = None,
        policy_status: Optional[str] = None,
        owner_department_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出制度/政策。
        参数（Parameters）：
            - `policy_category` (Optional[str])；默认为 None 表示不按此项筛选。
            - `policy_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `owner_department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的政策摘要列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if owner_department_ref is not None:
            self._get_department(owner_department_ref)

        results = []
        for p_ref, p in self.db.policy.items():
            if policy_category is not None and p.policy_category != policy_category:
                continue
            if policy_status is not None and p.policy_status != policy_status:
                continue
            if owner_department_ref is not None and p.owner_department_ref != owner_department_ref:
                continue
            results.append({
                "policy_ref": p.policy_ref,
                "policy_title": p.policy_title,
                "policy_code": p.policy_code,
                "policy_category": p.policy_category,
                "effective_date": p.effective_date,
                "expiry_date": p.expiry_date,
                "policy_status": p.policy_status,
                "version": p.version,
                "owner_department_ref": p.owner_department_ref,
            })
        return json.dumps(results)

    # ----------------
    # 服务目录（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_service_directory_details(self, service_directory_ref: str) -> ServiceDirectory:
        """
        功能说明（Description）：
            根据引用 ID 获取服务目录条目的详细信息。
        参数（Parameters）：
            - `service_directory_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ServiceDirectory`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_service_directory(service_directory_ref)

    @is_tool(ToolType.READ)
    def list_service_directory(
        self,
        campus_ref: Optional[str] = None,
        service_category: Optional[str] = None,
        service_status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出服务目录。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `service_category` (Optional[str])；默认为 None 表示不按此项筛选。
            - `service_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `department_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的服务条目列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for sd_ref, sd in self.db.service_directory.items():
            if campus_ref is not None and sd.campus_ref != campus_ref:
                continue
            if service_category is not None and sd.service_category != service_category:
                continue
            if service_status is not None and sd.service_status != service_status:
                continue
            if department_ref is not None and sd.department_ref != department_ref:
                continue
            results.append({
                "service_directory_ref": sd.service_directory_ref,
                "service_name": sd.service_name,
                "service_category": sd.service_category,
                "service_description": sd.service_description,
                "contact_phone": sd.contact_phone,
                "contact_email": sd.contact_email,
                "contact_employee_ref": sd.contact_employee_ref,
                "department_ref": sd.department_ref,
                "campus_ref": sd.campus_ref,
                "service_hours": sd.service_hours,
                "location_description": sd.location_description,
                "service_status": sd.service_status,
            })
        return json.dumps(results)

    # ----------------
    # 外部合作方（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_external_partner_details(self, external_partner_ref: str) -> ExternalPartner:
        """
        功能说明（Description）：
            根据引用 ID 获取外部合作方的详细信息。
        参数（Parameters）：
            - `external_partner_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ExternalPartner`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_external_partner(external_partner_ref)

    @is_tool(ToolType.READ)
    def list_external_partners(
        self,
        partner_type: Optional[str] = None,
        partner_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出外部合作方。
        参数（Parameters）：
            - `partner_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `partner_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的合作方列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for ep_ref, ep in self.db.external_partner.items():
            if partner_type is not None and ep.partner_type != partner_type:
                continue
            if partner_status is not None and ep.partner_status != partner_status:
                continue
            results.append({
                "external_partner_ref": ep.external_partner_ref,
                "partner_name": ep.partner_name,
                "partner_type": ep.partner_type,
                "contact_person": ep.contact_person,
                "contact_phone": ep.contact_phone,
                "contact_email": ep.contact_email,
                "address": ep.address,
                "partner_status": ep.partner_status,
                "description": ep.description,
            })
        return json.dumps(results)

    # ----------------
    # 差旅政策（只读）
    # ----------------

    @is_tool(ToolType.READ)
    def get_travel_policy_details(self, travel_policy_ref: str) -> TravelPolicy:
        """
        功能说明（Description）：
            根据引用 ID 获取差旅政策的详细信息。
        参数（Parameters）：
            - `travel_policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TravelPolicy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_travel_policy(travel_policy_ref)

    @is_tool(ToolType.READ)
    def list_travel_policies(
        self,
        city_tier: Optional[str] = None,
        policy_status: Optional[str] = None,
        position_level: Optional[int] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出差旅政策。
        参数（Parameters）：
            - `city_tier` (Optional[str])；默认为 None 表示不按此项筛选。
            - `policy_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
            - `position_level` (Optional[int])；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的政策列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for tp_ref, tp in self.db.travel_policy.items():
            if city_tier is not None and tp.city_tier != city_tier:
                continue
            if policy_status is not None and tp.policy_status != policy_status:
                continue
            if position_level is not None and not (tp.position_level_min <= position_level <= tp.position_level_max):
                continue
            results.append({
                "travel_policy_ref": tp.travel_policy_ref,
                "policy_name": tp.policy_name,
                "position_level_min": tp.position_level_min,
                "position_level_max": tp.position_level_max,
                "city_tier": tp.city_tier,
                "hotel_daily_limit": tp.hotel_daily_limit,
                "meal_daily_limit": tp.meal_daily_limit,
                "transport_class": tp.transport_class,
                "effective_date": tp.effective_date,
                "expiry_date": tp.expiry_date,
                "policy_status": tp.policy_status,
                "notes": tp.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_travel_policy_for_employee(self, employee_ref: str, city_tier: str) -> str:
        """
        功能说明（Description）：
            根据员工与城市等级解析适用的差旅政策。
        参数（Parameters）：
            - `employee_ref` (str)；按函数语义传入。
            - `city_tier` (str)；按函数语义传入。
        返回（Returns）：
            `TravelPolicy | None`: 匹配到的政策；若无则可能为 None（以实际实现为准）。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)
        if not emp.position_ref:
            raise ValueError("Employee has no position assigned")

        pos = self._get_position(emp.position_ref)
        position_level = pos.position_level

        valid_tiers = {"tier1", "tier2", "tier3", "international"}
        if city_tier not in valid_tiers:
            raise ValueError(f"Invalid city_tier: {city_tier}. Must be one of {valid_tiers}")

        for tp in self.db.travel_policy.values():
            if tp.policy_status != "active":
                continue
            if tp.city_tier != city_tier:
                continue
            if tp.position_level_min <= position_level <= tp.position_level_max:
                return json.dumps({
                    "travel_policy_ref": tp.travel_policy_ref,
                    "policy_name": tp.policy_name,
                    "position_level_min": tp.position_level_min,
                    "position_level_max": tp.position_level_max,
                    "city_tier": tp.city_tier,
                    "hotel_daily_limit": tp.hotel_daily_limit,
                    "meal_daily_limit": tp.meal_daily_limit,
                    "transport_class": tp.transport_class,
                    "effective_date": tp.effective_date,
                    "expiry_date": tp.expiry_date,
                    "policy_status": tp.policy_status,
                    "notes": tp.notes,
                })

        return json.dumps({})

    # ----------------
    # 保洁计划与记录（读 + 写）
    # ----------------

    @is_tool(ToolType.READ)
    def get_cleaning_schedule_details(self, cleaning_schedule_ref: str) -> CleaningSchedule:
        """
        功能说明（Description）：
            根据引用 ID 获取保洁计划的详细信息。
        参数（Parameters）：
            - `cleaning_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CleaningSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_cleaning_schedule(cleaning_schedule_ref)

    @is_tool(ToolType.READ)
    def list_cleaning_schedules(
        self,
        campus_ref: Optional[str] = None,
        floor_ref: Optional[str] = None,
        zone_ref: Optional[str] = None,
        cleaning_type: Optional[str] = None,
        schedule_status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出保洁计划。
        参数（Parameters）：
            - `campus_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `floor_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `zone_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `cleaning_type` (Optional[str])；默认为 None 表示不按此项筛选。
            - `schedule_status` (Optional[str]) 状态；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的计划列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for cs_ref, cs in self.db.cleaning_schedule.items():
            if campus_ref is not None and cs.campus_ref != campus_ref:
                continue
            if floor_ref is not None and cs.floor_ref != floor_ref:
                continue
            if zone_ref is not None and cs.zone_ref != zone_ref:
                continue
            if cleaning_type is not None and cs.cleaning_type != cleaning_type:
                continue
            if schedule_status is not None and cs.schedule_status != schedule_status:
                continue
            results.append({
                "cleaning_schedule_ref": cs.cleaning_schedule_ref,
                "campus_ref": cs.campus_ref,
                "floor_ref": cs.floor_ref,
                "zone_ref": cs.zone_ref,
                "cleaning_type": cs.cleaning_type,
                "frequency": cs.frequency,
                "scheduled_time": cs.scheduled_time,
                "assigned_vendor_ref": cs.assigned_vendor_ref,
                "schedule_status": cs.schedule_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_cleaning_records(
        self,
        cleaning_schedule_ref: Optional[str] = None,
        result: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            按可选条件筛选并列出保洁执行记录。
        参数（Parameters）：
            - `cleaning_schedule_ref` (Optional[str]) 引用 ID；默认为 None 表示不按此项筛选。
            - `result` (Optional[str])；默认为 None 表示不按此项筛选。
            - `date_from` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
            - `date_to` (Optional[str]) ISO 8601 时间边界；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `str`: JSON 编码的记录列表。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if cleaning_schedule_ref is not None:
            self._get_cleaning_schedule(cleaning_schedule_ref)

        results = []
        for cr_ref, cr in self.db.cleaning_record.items():
            if cleaning_schedule_ref is not None and cr.cleaning_schedule_ref != cleaning_schedule_ref:
                continue
            if result is not None and cr.result != result:
                continue
            if date_from is not None and cr.executed_at < date_from:
                continue
            if date_to is not None and cr.executed_at > date_to:
                continue
            results.append({
                "cleaning_record_ref": cr.cleaning_record_ref,
                "cleaning_schedule_ref": cr.cleaning_schedule_ref,
                "executed_by": cr.executed_by,
                "executed_at": cr.executed_at,
                "result": cr.result,
                "notes": cr.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_cleaning_record(
        self,
        cleaning_schedule_ref: str,
        executed_by: str,
        executed_at: str,
        result: str,
        notes: str = "",
    ) -> CleaningRecord:
        """
        功能说明（Description）：
            登记保洁执行记录。调用本工具前，Agent 必须征得用户明确确认。
        参数（Parameters）：
            - `cleaning_schedule_ref` (str)；按函数语义传入。
            - `executed_by` (str)；按函数语义传入。
            - `executed_at` (str)；按函数语义传入。
            - `result` (str)；按函数语义传入。
            - `notes` (str)；默认为 None 表示不按此项筛选。
        返回（Returns）：
            `CleaningRecord`: 新建的执行记录。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_cleaning_schedule(cleaning_schedule_ref)

        valid_results = {"completed", "partial", "skipped", "failed"}
        if result not in valid_results:
            raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}")

        now = self._now_iso()
        cr_ref = self._generate_ref("CR", self.db.cleaning_record)

        cleaning_record = CleaningRecord(
            cleaning_record_ref=cr_ref,
            cleaning_schedule_ref=cleaning_schedule_ref,
            executed_by=executed_by,
            executed_at=executed_at,
            result=result,
            notes=notes,
            created_at=now,
        )
        self.db.cleaning_record[cr_ref] = cleaning_record
        return cleaning_record