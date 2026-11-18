# FINANCE 业务规则

## 一、财务账户

### 账户管理
- 财务账户（finance_account）状态合法值：active / frozen / closed。
- 账户一旦进入 closed 状态，不可再变更为其他状态（封闭不可逆）。
- 账户冻结（frozen）期间不可发起付款、转账等出款操作。

## 二、预算管理

### 预算编制
- 预算（budget）创建须指定会计期间（fiscal_period）、预算类型（budget_type）和范围类型（scope_type），均须为合法枚举值。
- 预算总金额（total_amount）必须为正数。
- 预算包含多个预算明细行（budget_line），按科目或项目拆分。

### 预算审批流程
- 预算状态流转：draft → submitted → approved / rejected → closed。
- 提交（submit）仅允许从 draft 状态发起。
- 审批（approve）/ 拒绝（reject）仅允许从 submitted 状态操作。
- 关闭（close）仅允许从 approved 状态操作。
- 预算审批通过后方可被费用报销、采购等流程引用。

### 预算控制
- 费用发生时须校验对应预算的剩余额度（utilization），超预算需升级审批。
- 预算使用率达到 80% 时应触发预警。

## 三、费用报销

### 报销申请
- 费用报告（expense_report）状态流转：draft → submitted → under_review → approved / rejected；cancel 仅从 draft 或 submitted 状态。
- 提交（submit）仅允许从 draft 状态发起。
- 审批（approve）/ 拒绝（reject）仅允许从 submitted 或 under_review 状态操作。

### 报销明细
- 报销明细（expense_line）只能添加到 draft 状态的费用报告中。
- 费用科目（expense_category）须为合法枚举值。
- 报销金额（amount）必须为正数。
- 每笔报销明细必须关联真实发票或凭证。

### 费用政策
- 费用政策（expense_policy）按费用类别、职级层级和限额定义报销标准。
- 超出费用政策限额的报销需走特殊审批流程。
- 费用报销不得拆单规避审批限额。

## 四、发票管理

### 发票登记
- 发票（invoice）创建须指定发票类型、金额、开票方等信息，须为合法枚举值。
- 发票头（invoice_header）关联发票基本信息。

### 发票验证
- 发票验证（verify）仅允许对未验证且 invoice_status = active 的发票执行。
- 已验证的发票不可重复验证。
- 发票作废（void）仅允许从 active 状态操作。
- 发票金额与报销金额不一致时应标记异常。

## 五、付款管理

### 付款申请
- 付款申请（payment_request）须指定付款金额（正数）、付款类型（payment_type）、付款方式（method）和紧急度（urgency），均须为合法枚举值。
- 付款前须完成金额、收款方与合同信息核对。

### 付款审批
- 付款申请状态流转与费用报销一致：draft → submitted → approved / rejected；cancel 从 draft / submitted。
- 大额付款（超过审批权限）需逐级上报。

### 付款执行
- 付款执行（payment_execution）关联已审批的付款申请。
- 付款完成后更新对应应付账款状态。

## 六、收款与对账

### 收款管理
- 收款记录（receipt_record）关联客户和应收账款。
- 收款金额须与实际到账金额一致。

### 对账
- 对账（reconciliation）须比对系统记录与银行流水，差异须人工核实。

## 七、退款管理

- 退款（refund）金额必须为正数。
- 退款走独立的审批流程，状态流转有前置条件校验。
- 退款须关联原始付款记录或发票。
- 退款金额不得超过原始付款金额。

## 八、员工借款

### 借款管理
- 员工借款（employee_loan）金额须为正数。
- 借款走审批流程，审批通过后方可放款。

### 还款管理
- 借款还款（loan_repayment）仅允许对 active 或 overdue 状态的借款执行。
- 单次还款金额不得超过剩余未还金额（outstanding amount）。
- 借款到期未还自动转为 overdue 状态。

## 九、结算管理

- 结算（settlement）包含结算明细行（settlement_line）。
- 结算走审批流程，状态流转有前置条件校验。
- 结算金额须为正数。

## 十、资金调拨

- 资金调拨（fund_transfer）须指定源账户和目标账户，源账户和目标账户不得相同。
- 调拨金额须为正数。
- 调拨走审批流程，大额调拨需升级审批。

## 十一、汇率与外币

- 汇率（exchange_rate）按币种对和汇率类型（rate_type）维护。
- 币种转换（convert_currency）时须使用系统登记的汇率，无对应汇率记录时报错。
- 外币交易须统一折算为本位币记账。

## 十二、税务管理

### 企业税务
- 税务申报（tax_filing）需按申报周期和税种分别填报。
- 申报走审批流程，状态流转有前置条件校验。

### 个人所得税
- 员工个税记录（employee_tax_record）关联员工和纳税期间。
- 个税计算（calculate_individual_income_tax）要求 gross_income 不得为负数。
- 专项附加扣除（tax_special_deduction）须关联真实员工和扣除项目。

## 十三、计提与核销

- 计提分录（accrual_entry）按会计期间和科目生成。
- 计提走审批流程，状态流转有前置条件校验。

## 十四、信用管理

### 信用申请
- 信用申请（credit_application）走审批流程。
- 还款计划（credit_repayment_schedule）关联信用申请自动生成。

### 信用还款
- 还款须按还款计划执行，提前还款需额外审批。

## 十五、证券交易

- 股票交易指令（stock_trade_order）须指定交易方向、数量和价格。
- 数量和价格须为正数。
- 交易走审批流程，状态流转有前置条件校验。

## 十六、财务审批

### 审批链
- 财务审批流程（finance_approval_flow）关联具体业务实体。
- 审批步骤须为 pending 状态方可操作（approve / reject）。
- 审批动作（action）须为合法枚举值。
- 所有涉及金额的操作不得跳过审批直接修改结算状态。

### 审批权限
- 审批权限按金额层级划分：一般金额由部门负责人审批，大额由财务总监或 CFO 审批。
- 不得自审自批（申请人不可同时是审批人）。

## 十七、财务工单

- 财务工单（finance_ticket）用于处理财务咨询和异常事项。
- 工单有优先级和分类，走标准工单处理流程。

## 十八、数据完整性与合规
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 所有金额口径需与币种和税务规则一致。
- 金额字段统一使用正数，负数需通过退款或冲销流程处理。
- 财务数据修改须保留完整审计轨迹，不可直接修改已入账数据。
