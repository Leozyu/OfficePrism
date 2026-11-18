# HR 业务规则

## 一、薪酬与发薪

### 薪资结构
- 每位员工必须关联一个有效的薪资结构（salary_structure），薪资结构包含多个薪资组成项（salary_component）。
- 薪资组成项分为固定（fixed）和浮动（variable）两类，浮动部分需绑定计算规则或绩效系数。
- 薪资币种默认为 CNY，涉及外币需在薪资结构中显式标注。

### 发薪流程
- 每月发薪记录（payroll_record）按发薪周期生成，包含多个发薪明细行（payroll_line_item）。
- 发薪记录状态流转：draft → submitted → approved → paid；rejected 可从 submitted 退回。
- 发薪金额必须与薪资结构、社保公积金扣缴、个税计算结果一致，不得手动覆盖系统计算值。

### 银行账户
- 员工可绑定多个银行账户（bank_account），但同一时间只能有一个主账户（is_primary）。
- 设为主账户时，该账户状态必须为 active；非 active 账户不可设为主账户。
- 发薪默认打款至主账户，无主账户时发薪流程应中止并提示。

## 二、社保与福利

### 社会保险
- 社保（social_insurance）记录需关联员工和参保城市，包含养老、医疗、失业、工伤、生育五险。
- 缴费基数应在当地社保局公布的上下限范围内，超出需说明原因。
- 社保状态为 active 的记录不可重复创建（同一员工同一险种同一参保地）。

### 住房公积金
- 住房公积金（housing_fund）缴存比例一般为 5%~12%，企业和个人比例须一致。
- 公积金账户状态变更（如封存、转移）需关联离职或调岗流程。

### 商业保险与福利
- 商业保险（commercial_insurance）方案由公司统一采购，员工通过 employee_commercial_insurance 关联。
- 福利计划（benefit_plan）有生效/失效日期，员工报名（employee_benefit_enrollment）须在有效期内。
- 同一福利计划不可重复报名（同一员工同一计划且状态为 active）。

## 三、考勤与排班

### 工作日历
- 公司统一维护节假日日历（holiday_calendar），标注法定节假日、调休工作日。
- 排班表（work_schedule）按部门或岗位设定，员工通过 employee_work_schedule 关联。
- 排班冲突（同一员工同一天多个班次）系统应拒绝。

### 请假制度
- 请假最小申请单位为半天（0.5 天），不支持按小时请假。
- 年假需至少提前 3 个工作日提交申请；病假超过 3 天需补充医疗证明。
- 请假申请（leave_request）状态流转：draft → pending → approved / rejected；已 approved 的假单不可直接取消，需走撤销审批。
- 取消请假仅允许从 pending 或 draft 状态发起，已 approved / rejected / cancelled 的不可再取消。
- 审批请假仅允许从 pending 状态操作（approve / reject）。
- 提交请假时系统自动校验假期余额（leave_balance）：若 remaining_days < 请假天数，拒绝提交并提示余额不足。
- 假期余额按自然年度（start_datetime 所在年份）扣减，跨年假期分段计算。
- 连续请假超过 5 天需部门总监复核（审批链 approval_flow 增加一级）。

### 加班制度
- 加班申请（overtime_request）必须先申请后执行，事后补报须在 3 个工作日内完成。
- 加班类型（overtime_type）须为系统定义的合法值（如 weekday / weekend / holiday）。
- 补偿方式（compensation_type）须为合法值（如 overtime_pay / comp_off）。
- 月度加班上限为 36 小时，超出需升级审批。
- 法定节假日加班按 3 倍工资计算，休息日加班按 2 倍或调休，工作日延长按 1.5 倍。
- 加班审批 / 取消规则与请假一致：approve / reject 仅从 pending 状态；cancel 仅从 pending / draft。

## 四、劳动合同

### 合同管理
- 劳动合同（contract）包含合同类型、起止日期、签约主体等信息。
- 合同续签（renew）仅允许从 active 或 expired 状态发起；terminated / cancelled 合同不可续签。
- 合同终止（terminate）仅允许从 active 状态发起，需填写终止日期和终止原因。
- 合同到期预警：通过 get_expiring_contracts 查询 end_date 早于指定日期的 active 合同。

### 合同合规
- 试用期不得超过法定上限（合同期 1 年以下试用期不超过 1 个月，1~3 年不超过 2 个月，3 年以上不超过 6 个月）。
- 同一员工不得同时拥有两份 active 状态的劳动合同。

## 五、人事变动

### 入职 / 离职 / 调岗 / 晋升
- 所有人事变动通过 employee_change 记录，change_type 区分 onboarding / offboarding / transfer / promotion。
- 入职流程（onboarding）更新时，change_type 必须为 onboarding，否则报错。
- 离职流程（offboarding）同理，change_type 必须为 offboarding。
- 人事变动状态合法值：draft / pending / approved / completed / rejected / cancelled。
- 状态流转由审批链（approval_flow + approval_step）驱动，每一步审批有独立的审批人和结果。

### 审批链
- 审批链（approval_flow）关联具体业务实体（如请假、加班、人事变动）。
- 审批步骤（approval_step）按顺序执行，前一步未完成不可跳步审批。
- 审批结果为 approve 时自动流转到下一步；reject 时整个流程置为 rejected。

## 六、招聘

### 职位与候选人
- 招聘需求（job_requisition）由用人部门发起，需包含岗位、人数、要求等信息。
- 候选人（candidate）信息独立于职位，一个候选人可投递多个岗位（通过 job_application 关联）。
- 内部推荐（referral）需关联推荐人（员工）和被推荐候选人。

### 招聘流程
- 应聘记录（job_application）阶段流转：screening → interview → offer → hired / rejected / withdrawn。
- 面试（interview）类型须为合法值（如 phone / onsite / video）。
- 面试反馈评分为 1~5 整数，仅允许对 scheduled 或 in_progress 状态的面试提交反馈。
- 录用通知（offer）状态合法值：issued / approved / accepted / rejected / withdrawn。
- 录用通知中 offered_worker_type 须为合法值。

## 七、培训

- 培训项目（training_program）状态为 active 时方可报名。
- 同一员工不可重复报名同一培训（已有 enrolled 或 in_progress 状态的报名记录时拒绝）。
- 培训进度（progress_pct）取值范围 0.0~100.0，超出报错。
- 培训完成时须填写结果（result）：pass / fail / incomplete。

## 八、试用期与绩效

### 试用期
- 试用期评审（probation_review）状态流转：draft → pending → submitted → completed。
- 提交评审仅允许从 draft 或 pending 状态发起。
- 评审包含评分（rating）和建议（recommendation），须为合法枚举值。

### 绩效考核
- 绩效周期（performance_cycle）定义考核时间窗口。
- 绩效评审（performance_review）流程：draft → self_review → manager_review → completed。
- 员工自评仅允许从 draft 或 self_review 状态提交。
- 主管评审仅允许从 manager_review 状态提交。

## 九、股权与激励

- 股权授予（equity_grant）需关联员工与授予方案。
- 归属事件（equity_vesting_event）按归属日程表自动或手动触发。
- 职称（professional_title）与人才补贴（talent_subsidy）需关联真实员工信息。

## 十、员工服务

### 证明开具
- 证明类型（certificate_type）须为合法值（如 employment_proof / income_proof 等）。
- 语言（language）须为合法值。
- 取消证明申请仅允许从 pending 或 draft 状态发起。

### HR 服务工单
- 服务类型（request_type）须为合法值（如 hotline / policy_inquiry 等）。
- 优先级（priority）须为合法值：low / normal / high / urgent。
- 工单状态合法值：open / in_progress / resolved / closed / cancelled。
- 取消工单仅允许从 open 或 in_progress 状态发起。

## 十一、角色与权限
- 员工只能提交本人申请（请假、加班、报名等），不能代他人提交或审批本人记录。
- 主管可审批直属下属的常规假勤和人事申请。
- 涉及薪资、合同、社保等敏感变更必须由 HR 角色处理，普通员工和主管无权操作。
- 所有写操作需校验操作人角色和权限，无权限时返回明确错误。

## 十二、数据完整性
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 日期字段统一使用 ISO 8601 格式（YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS）。
- 金额字段必须为正数，币种须显式标注。
