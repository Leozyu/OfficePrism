# ADMIN 业务规则

## 一、空间与设施管理

### 空间层级
- 公司空间按 campus → building → floor → zone 四级层级管理。
- 每个设施（facility）关联到具体楼层或区域，包含容量（capacity）、可预订标志（is_bookable）和状态（facility_status）。
- 设施设备（facility_equipment）关联到具体设施，记录设备型号、数量和维护状态。

### 设施预订
- 仅 is_bookable = true 且 facility_status = available 的设施可预订。
- 预订时间必须满足 start_at < end_at，不可创建结束时间早于开始时间的预订。
- 预订人数（attendee_count）不得超过设施容量（capacity），超出时拒绝预订。
- 预订类型（booking_type）须为合法枚举值。
- 预订状态流转：pending → confirmed → completed；取消（cancel）不可从 cancelled 或 completed 状态发起。
- 确认预订（confirm）仅允许从 pending 状态操作。
- 预订时间段不可与同一设施已确认的预订冲突。
- 设施可配置提前预订天数限制（booking_advance_days）。

### 工位与储物柜
- 工位（workstation）分配仅允许将 available 状态的工位分配给员工，分配后状态变为 occupied。
- 释放工位后状态恢复为 available。
- 储物柜（locker）分配逻辑与工位一致：available → occupied → available。
- 同一员工不得同时占用多个同类型工位（同一楼层内）。

### 停车与充电
- 停车位（parking_space）管理支持分配和释放。
- 电动车充电桩（ev_charger）状态管理独立于停车位，需关注充电桩可用状态。

## 二、通勤与餐饮

### 班车服务
- 班车路线（shuttle_route）包含多个站点（shuttle_stop），站点有顺序编号。
- 班车时刻表（shuttle_schedule）需关联路线且状态为 active 方可预订。
- 班车预订（shuttle_booking）的上车站点必须属于该路线的站点列表。
- 取消班车预订仅允许从 confirmed 状态发起。

### 食堂
- 食堂（canteen）按园区管理，每个食堂有营业时间和容量限制。
- 食堂菜单（canteen_menu）按日期更新，包含菜品、价格和营养信息。

## 三、访客与门禁

### 访客管理
- 访客（visitor）登记须填写证件类型（id_type）、访客类型（visitor_type），均须为合法枚举值。
- 访客预约（visitor_appointment）须指定来访类型（visit_type）和临时门禁级别（temp_access_level），均须为合法枚举值。
- 预约时间必须满足 scheduled_start_at < scheduled_end_at。
- 访客到访当天需完成签到（check-in），离开时签退（check-out）。
- 访客预约支持审批流程：approve / reject 操作。

### 门禁管理
- 门禁卡（access_card）关联员工或访客，有有效期限制。
- 门禁日志（access_log）记录所有刷卡进出记录，不可篡改。
- 工牌（badge）管理独立于门禁卡，记录工牌类型和状态。
- 访客临时门禁权限必须在预约有效期内，过期自动失效。

## 四、资产管理

### 资产台账
- 固定资产（asset）包含资产编号、类别、状态、责任人等信息。
- 资产申请（asset_request）须指定申请类型（request_type）和资产类别（asset_category），均须为合法枚举值。
- 申请数量（quantity）必须大于 0。

### 资产流转
- 资产交易（asset_transaction）记录资产的领用、归还、调拨、报废等操作。
- 资产领用需校验资产库存状态：仅 available 状态的资产可领用。
- 资产归还后需检验资产状态，损坏资产需走报修流程。

## 五、库存与耗材

### 库存管理
- 库存物品（inventory_item）包含当前库存量、安全库存量和存放位置。
- 库存低于安全库存时应触发补货提醒。

### 领用申请
- 耗材领用申请（supply_request）须包含非空的物品明细列表。
- 每个明细项须关联库存物品（inventory_item_ref）且数量（quantity）大于 0。
- 领用审批通过后自动扣减库存。

## 六、报修与投诉

### 报修管理
- 报修申请（repair_request）关联到具体设施或资产，需描述故障现象。
- 报修走派单 → 处理 → 验收流程。

### 投诉管理
- 投诉（complaint）需指定投诉类别，包含投诉描述和期望解决方案。
- 投诉处理有时效要求，需在规定时间内响应。

## 七、安全与应急

### 安全事件
- 安全事件（security_incident）需记录事件类型、发生时间、地点和严重等级。
- 事件处置需保留完整的处理记录和后续整改措施。

### 失物招领
- 失物招领（lost_found）记录包含物品描述、发现地点和认领状态。
- 认领须核实物品所有人身份。

## 八、礼品与商务

### 礼品管理
- 礼品（gift）包含库存管理和发放记录（gift_record）。
- 礼品发放须关联具体事由和接收人。

### 名片管理
- 名片（business_card）申请须提供职位、部门等信息，按公司统一模板制作。

## 九、活动与差旅

### 公司活动
- 公司活动（company_event）须指定开始和结束时间，满足 start_at < end_at。
- 活动报名（event_registration）不允许同一员工重复报名同一活动。
- 活动有容量限制时，报满后不再接受报名。

### 差旅政策
- 差旅标准（travel_policy）按员工职级和城市等级（city_tier）确定住宿、交通标准。
- 城市等级（city_tier）须为合法枚举值。
- 查询差旅标准时需校验员工是否已分配职位，无职位员工无法匹配差旅标准。

## 十、行政制度与服务

### 制度管理
- 行政制度（policy）按类别（policy_category）管理，如 meal_allowance 等。
- 制度文档有版本控制，以最新版本为准。

### 服务目录
- 行政服务目录（service_directory）列出所有可用行政服务及联系方式。
- 外部合作伙伴（external_partner）信息统一维护。

### 保洁管理
- 保洁排班（cleaning_schedule）按区域和时段安排。
- 保洁记录（cleaning_record）用于追踪保洁执行情况和质量。

## 十一、数据完整性
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 行政变更应保留可追踪的操作记录，包含操作人、时间和变更内容。
- 涉及费用的行政请求需按审批层级流转，不得跳过审批直接执行。
