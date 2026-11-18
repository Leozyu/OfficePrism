# PURCHASE 业务规则

## 一、采购分类

- 采购类别（procurement_category）按公司采购目录统一维护，包含类别编码、名称和上级类别。
- 采购类别决定后续的审批层级、供应商准入要求和采购方式建议。

## 二、供应商管理

### 供应商准入
- 供应商（supplier）须指定供应商类型（supplier_type）和风险等级（risk_level），均须为合法枚举值。
- 供应商编码（supplier_code）在系统内全局唯一，重复编码拒绝创建。
- 新供应商默认状态为 pending，须经审批后方可合作。

### 供应商状态流转
- 审批通过（approve）仅允许从 pending 状态发起，状态变为 approved。
- 暂停合作（suspend）仅允许从 approved 状态发起，状态变为 suspended。
- 列入黑名单（blacklist）仅允许对非 blacklisted 状态的供应商操作。
- 被黑名单的供应商不可参与新的采购项目。

### 供应商联系人与资质
- 供应商联系人（supplier_contact）关联具体供应商，维护联系方式和职务。
- 供应商资质（supplier_qualification）记录营业执照、资质证书等资料，需定期更新。
- 资质审核（verify）/ 拒绝（reject）仅允许从 pending 状态操作。

### 供应商分类与评估
- 供应商类别关联（supplier_category）记录供应商与采购类别的对应关系。
- 同一供应商不可在同一类别下重复添加 active 关联，移除（remove）仅允许对非 removed 状态操作。
- 供应商评估（supplier_evaluation）包含评分（rating）、评估维度，须为合法枚举值。
- 评估状态流转：draft → submitted → approved / rejected。

## 三、寻源与报价

### 寻源项目
- 寻源项目（sourcing_project）管理从需求发布到供应商选定的全过程。
- 寻源项目状态流转有严格校验：非法状态转换直接报错（"Cannot transition from 'A' to 'B'"）。
- 取消寻源项目须填写取消原因（cancel_reason）。
- 定标时须指定中标供应商（awarded_supplier_ref）。

### 寻源邀请
- 邀请供应商参与寻源须校验供应商是否已被邀请，不可重复邀请。
- 仅 approved 状态的供应商可被邀请参与寻源。

### 报价管理
- 报价（quotation）由供应商提交，包含报价明细行（quotation_item）。
- 报价比价（compare）须至少提供 2 份报价进行对比，少于 2 份拒绝执行。
- 报价状态流转有前置条件校验。

## 四、采购申请

### 请购
- 采购申请（purchase_requisition）由需求部门发起，包含申请明细行（requisition_item）。
- 仅在允许的状态下可添加明细行。
- 提交（submit）/ 审批（approve）/ 拒绝（reject）/ 取消（cancel）操作均有状态前置条件。
- 取消时须填写取消原因。

### 审批控制
- 采购申请按金额层级审批，超过权限金额须逐级上报。
- 不得绕过审批直接创建采购订单。

## 五、采购合同

### 合同管理
- 采购合同（purchase_contract）关联供应商和采购项目，包含合同明细行（contract_item）。
- 合同状态流转有前置条件校验，非法转换直接报错。
- 终止合同须填写终止原因（termination_reason）。
- 合同剩余金额（contract_remaining_amount）= 合同总金额 - 已消耗金额（consumed_amount）。

### 合同执行
- 采购订单须关联采购合同，订单金额不得超过合同剩余金额。

## 六、采购订单

### 订单管理
- 采购订单（purchase_order）关联采购合同和供应商，包含订单明细行（purchase_order_item）。
- 仅在允许的状态下可添加明细行。
- 订单状态流转有前置条件校验。

### 变更管理
- 采购变更申请（purchase_change_request）用于修改已提交的订单。
- 变更须说明变更原因和影响范围。

## 七、收货与验收

### 收货
- 收货记录（goods_receipt）关联采购订单，包含收货明细行（goods_receipt_item）。
- 收货状态流转有前置条件校验，非法转换直接报错。
- 收货数量须与订单数量核对，超收需说明原因。

### 验收
- 验收记录（acceptance_record）关联收货记录，包含验收明细行（acceptance_item）。
- 验收状态流转有前置条件校验。
- 验收不合格须记录问题描述和补救措施。
- 异常交付（短缺、损坏、规格不符）必须记录问题与补救动作。

## 八、审批流程

### 审批模板
- 审批流程模板（approval_flow_template）定义各类采购业务的审批路径。
- 审批节点（approval_flow_node）按顺序排列，可配置条件规则（condition_rules），如金额阈值。

### 审批实例
- 审批实例（approval_instance）关联具体采购业务。
- 审批动作（approval_action）仅允许对 in_progress 状态的审批实例执行。
- 审批须按节点顺序执行，不可跳步。

## 九、权限管理

### 采购权限
- 采购权限规则（procurement_permission_rule）定义员工的采购操作权限。
- 权限包含最大单笔金额（max_single_amount）和允许的操作类型（allowed_operations）。
- 提交采购前须校验操作人权限（check_employee_procurement_permissions），无权限时拒绝操作。

## 十、培训与工单

### 采购培训
- 采购培训课程（procurement_training_course）须为 active 状态方可报名。
- 同一员工不可重复报名同一培训课程（重复报名拒绝）。
- 培训记录（procurement_training_record）状态流转有前置条件校验。

### 问题工单
- 采购问题工单（procurement_issue_ticket）用于处理采购过程中的异常和咨询。
- 工单状态流转有前置条件校验，非法转换直接报错。

## 十一、辅助功能

- 采购流程指引（get_procurement_process_guide）提供各阶段操作指导。
- 采购方式建议（get_procurement_method_recommendation）根据金额和类别推荐采购方式。
- 合同剩余金额查询（get_contract_remaining_amount）用于下单前的额度校验。

## 十二、数据完整性与合规
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 采购全流程须保持请购 → 寻源 → 下单 → 收货 → 验收的闭环推进，不可跳过环节。
- 所有金额须为正数，币种须显式标注。
- 采购操作须保留完整审计轨迹，满足内控和审计要求。
