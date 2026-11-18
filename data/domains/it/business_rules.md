# IT 业务规则

## 一、账号与权限管理

### 系统账号生命周期
- 新建系统账号（it_system_account）必须绑定真实员工（employee_ref）和目标 IT 系统（it_system_ref）。
- 同一 IT 系统内不允许存在重复用户名（username），创建时自动校验唯一性。
- 账号类型（account_type）和系统角色（role_in_system）须为系统定义的合法枚举值。
- 账号状态流转规则：
  - **禁用（disable）**：仅 active 或 locked 状态可禁用；已 disabled / deprovisioned 的账号不可重复禁用。
  - **启用（enable）**：仅 disabled 或 locked 状态可启用，恢复为 active。
  - **锁定（lock）**：仅 active 状态可锁定；已 locked / deprovisioned 的不可再锁。
  - **解锁（unlock）**：仅 locked 状态可解锁，恢复为 active。
  - **注销（deprovision）**：任何非 deprovisioned 状态均可注销，注销后不可恢复。
- 密码重置（reset_password）不可对已 deprovisioned 的账号执行；若账号处于 locked 状态，重置密码时自动解锁。
- 离职员工的关键系统账号必须在离职当天完成注销或禁用。

### 权限管理
- 系统权限（it_system_account_permission）包含权限级别（permission_level），须为合法枚举值。
- 权限撤销（revoke）仅允许从 active 状态发起；已 revoked 或 expired 的权限不可重复撤销。
- 高权限变更（如 admin / super_admin 级别）需保留审批链并记录审计日志。
- 权限变更应遵循最小权限原则，授权范围不得超出岗位职责所需。

### 访问异常
- 访问异常（access_anomaly）记录系统自动生成或人工上报。
- 异常状态合法值：open / investigating / resolved / dismissed。
- 关闭异常（resolve / dismiss）仅允许从 open 或 investigating 状态发起；已 resolved / dismissed 的不可重复操作。
- 高风险异常（如暴力破解、权限提升）应在 4 小时内响应处理。

### 账号迁移
- 账号迁移（account_migration）需指定迁移类型（migration_type）和目标系统。
- 迁移状态（migration_status）须为合法枚举值。
- 迁移完成时自动设置 completed_at 时间戳，并可关联执行人（executed_by_ref）。

## 二、邮箱与通讯

### 邮箱账号
- 邮箱账号（email_account）状态合法值：active / suspended / deactivated / archived。
- 垃圾邮件过滤级别（spam_filter_level）须为系统定义的合法值。
- 邮箱状态变更需关联人事变动（如离职 → deactivated / archived）。

### 邮件组
- 邮件分发列表（email_distribution_list）成员管理须校验角色（role）枚举值。
- 同一分发列表中不允许添加重复的 active 成员（同一员工 + 同一列表）。
- 移除成员时，已 removed 状态的成员不可重复移除。
- 移除成员后，列表的 member_count 自动减 1（最小为 0）。

### 邮件安全事件
- 邮件安全事件（email_security_event）处置规则与访问异常一致：resolve / dismiss 仅从 open / investigating 状态发起。

## 三、代码仓库与 DevOps

### 代码仓库
- 代码仓库（code_repository）成员管理需指定访问级别（access_level），须为合法枚举值。
- 同一仓库不允许添加重复的 active 成员。
- 已 revoked 的成员权限不可再更新，需重新添加。

### 分支管理
- 受保护分支（protected branch）不可直接删除。
- 分支删除前需确认无关联的 open 状态合并请求（merge_request）。
- 分支合并须通过合并请求流程，不可直接推送到受保护分支。

### 合并请求（MR）
- 合并请求状态流转：open → merged / closed；closed 可 reopen。
- 合并操作须满足：无冲突（conflicts）、非 draft 状态、通过必要的代码评审。
- MR 合并后自动关联代码分支变更记录。
- MR 评审人（merge_request_reviewer）须为仓库成员。

### CI/CD 与部署
- CI/CD 流水线（ci_cd_pipeline）触发须满足流水线状态为可执行状态。
- 流水线执行（pipeline_execution）可取消，但仅限运行中状态。
- 部署（deployment）策略（strategy）和状态须为合法枚举值。
- 回滚（rollback）仅允许从特定有效状态发起。
- 部署环境（deploy_environment）隔离管理，生产环境部署需额外审批。

## 四、IT 资源管理

### 开发环境
- 开发环境（dev_environment）资源由 IT 统一分配和回收。

### IT 资源申请
- IT 资源申请（it_resource_request）走完整的申请-审批-交付-关闭流程。
- 审批 / 拒绝 / 交付 / 取消操作均有状态前置条件校验。
- 已完成或已取消的申请不可再变更状态。

## 五、数据管理

### 数据源与权限
- 数据源（data_source）注册须包含连接信息和责任人。
- 数据访问授权（data_access_grant）撤销仅允许从非 revoked 状态发起。
- 数据资产（data_asset）需关联所属数据源和数据分类。

### 数据传输
- 数据传输任务（data_transfer_job）可取消，但仅限特定运行状态。
- 跨系统数据传输需经数据安全审批。

## 六、网络管理

### 网络区域与 VPN
- 网络区域（network_zone）划分遵循安全域隔离原则。
- VPN 连接（vpn_connection）凭证有有效期限制，到期自动失效。
- VPN 凭证状态变更需校验前置状态。

### 访客 WiFi
- 访客 WiFi 凭证（guest_wifi_credential）有时效限制，过期自动回收。
- 凭证发放需关联访客登记信息。

### 网络规则与事件
- 网络访问规则（network_access_rule）支持激活 / 停用操作。
- 网络安全事件（network_incident）需指定事件类型（incident_type）和严重等级（severity），均须为合法枚举值。
- 生产网络故障优先保障业务恢复，再补充根因分析记录。

## 七、软件与许可

### 软件目录
- 软件目录（software_catalog）维护公司批准使用的软件清单。
- 未在目录中的软件需先完成合规备案（software_filing）方可安装使用。

### 许可证管理
- 软件许可证（software_license）有席位数限制。
- 许可证分配（software_license_assignment）须满足：许可证可分配、剩余席位 > 0、同一员工未持有该许可证的 active 分配。
- 许可证回收（revoke）后席位数归还。

### 软件备案
- 软件备案（software_filing）状态流转有前置条件：审批 / 拒绝仅从待审核状态；撤回须在终态之前。

## 八、办公设备

### 打印机
- 打印机（printer）管理包含耗材（printer_supply）监控和故障报修（printer_incident）。
- 耗材低于阈值时应自动触发补充提醒。

### 文件传输
- 文件传输（file_transfer）需遵循文件安全策略（file_security_policy）。
- 涉密文件传输须额外审批。

## 九、IT 服务台

### 工单管理
- IT 服务工单（it_service_ticket）须指定类别（category）、子类别（subcategory）、紧急度（urgency）、影响度（impact）和优先级（priority），均须为合法枚举值。
- 搜索工单时关键词不可为空。
- 工单关闭时可填写满意度评分（satisfaction），取值范围 1~5。
- 工单评论（it_service_ticket_comment）支持追踪处理过程。

### 知识库
- IT 知识库文章（it_knowledge_article）用于沉淀常见问题解决方案，支持搜索和引用。

## 十、数据完整性与审计
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 关键操作（账号创建 / 禁用 / 权限变更 / 数据访问授权）须记录操作人、操作时间和操作内容。
- 变更类操作需先评估影响范围，再执行变更。
