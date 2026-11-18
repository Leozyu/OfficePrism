# LAW 业务规则

## 一、合同管理

### 合同模板与签约方
- 合同模板（law_contract_template）按业务类别维护标准条款，新建合同可引用模板快速生成。
- 签约方（law_contract_party）独立管理，状态合法值：active / inactive / blacklisted。
- 被列入黑名单（blacklisted）的签约方不得作为新合同的当事人。

### 合同创建与基本信息
- 创建合同（law_contract）须指定合同类别（contract_category）、合同类型（contract_type）、币种（currency）和风险等级（risk_level），均须为系统定义的合法枚举值，非法值直接拒绝。
- 合同金额须为正数，币种须与实际结算币种一致。

### 合同状态流转
- 合同状态合法值：draft / pending_approval / approved / signed / active / suspended / expired / terminated / cancelled。
- 提交审批（submit_contract_for_approval）仅允许从 draft 状态发起，状态变为 pending_approval。
- 签署（signed）时若未填写签署日期（signing_date），系统自动设置为当前时间。
- 终止合同（terminate_contract）仅允许从 active / suspended / signed 状态发起；terminated / cancelled / expired 合同不可终止。
- 终止时若未填写终止日期（termination_date），系统自动设置为当前时间。
- 状态可在合法值范围内自由更新（update_contract_status），但须符合业务合理性。

### 合同签约关联
- 合同与签约方通过 law_contract_party_link 关联，记录各方签约状态（signing_status）。
- 签约状态更新时，若状态为 signed，可记录签署人姓名（signer_name）。

### 合同变更（Amendment）
- 合同变更（law_contract_amendment）记录条款修改内容和原因。
- 变更生效（effective）时若未填写生效日期（effective_date），系统自动设置为当前时间。
- 变更须关联原合同，不可对已终止 / 已取消的合同创建变更。

### 合同移交（Transfer）
- 合同移交（law_contract_transfer）用于合同管理权在部门间转移。
- 部门移交须同时指定移出部门（from_department_ref）和接收部门（to_department_ref），缺失任一则报错。

### 合同里程碑
- 合同里程碑（law_contract_milestone）标记合同执行的关键节点。
- 里程碑完成（completed）时若未填写完成日期（completed_date），系统自动设置为当前时间。

### 合同风险
- 合同风险（law_contract_risk）记录合同执行中识别的风险点。
- 风险解决（resolved）时若未填写解决时间（resolved_at），系统自动设置为当前时间。
- 高风险合同须升级到法务负责人或法律顾问处理。

### 合同借款
- 合同借款（law_contract_loan）记录合同相关的借贷信息，须关联具体合同。

## 二、审批流程

### 审批链
- 法务审批流程（law_approval_flow）关联具体法务业务实体（合同、用章等）。
- 审批步骤总数（total_steps）必须 >= 1。
- 审批步骤（law_approval_step）按顺序执行，每步有独立的审批人和决定（decision），决定须为合法枚举值。

### 审批规则
- 合同审批必须覆盖法务审阅环节，不可跳过法务直接进入签署。
- 取消审批流程须校验当前状态，已完成的流程不可取消。
- 审批拒绝时须填写拒绝理由。

## 三、印章管理

### 印章台账
- 印章（law_seal）按类型分类管理（如公章、合同章、财务章、法人章等）。
- 每枚印章有唯一编号、保管人和使用权限范围。

### 用章申请
- 用章申请（law_seal_usage_request）须指定用章事由、用章文件和申请印章。
- 用章须在授权范围内，超出授权范围的用章需额外审批。
- 用章申请走审批流程，审批通过后方可使用。
- 外带用章须额外登记外带原因和预计归还时间。

## 四、知识产权

### IP 资产管理
- 知识产权资产（law_ip_asset）包含专利、商标、著作权、商业秘密等。
- IP 发明人（law_ip_inventor）关联员工信息，记录贡献比例。

### IP 申请与授权
- IP 申请（law_ip_application）记录知识产权注册 / 申请的全流程。
- IP 授权（law_ip_authorization）记录对外许可使用的授权信息。
- IP 奖励（law_ip_reward）关联发明人和奖励金额。

## 五、合规与廉洁

### 廉洁申报
- 廉洁声明（law_integrity_declaration）由员工定期提交。
- 提交（submit）/ 审核（review）操作有状态前置条件。
- 满意度评分（satisfaction_rating）取值范围 1~5。

### 违规举报
- 违规举报（law_violation_report）支持匿名和实名举报。
- 举报状态流转有前置条件，处理中的举报不可直接关闭。

## 六、法律案件

### 案件管理
- 法律案件（law_legal_case）记录诉讼、仲裁、行政处罚等法律事务。
- 案件事件（law_case_event）记录案件推进的每个节点。

### 证据管理
- 证据（law_evidence）须关联具体案件，记录证据类型、来源和保管链。
- 未完备证据的法务结论必须标记为"待补充"，不可作为最终结论。
- 证据管理需确保完整的保管链记录，防止证据灭失或污染。

### 法律咨询
- 法律咨询（law_legal_consultation）记录内部法律咨询的问题和答复。
- 法务结论必须基于已登记的条款与证据，不可凭空推断。

### 合规审查
- 合规审查（law_compliance_review）对业务活动进行法律合规性评估。
- 审查结论须关联具体审查依据和发现的问题。

## 七、公司治理

### 法人实体
- 法人实体（law_corporate_entity）管理公司及子公司的法律主体信息。
- 实体变更（law_entity_change）记录工商变更（如法人变更、地址变更、经营范围变更等）。

### 资质证照
- 资质证书（law_qualification_certificate）有有效期管理，到期前需及时续期。
- 证照借用（law_license_usage_request）须登记借用人、用途和预计归还时间。

### 关联交易
- 关联方（law_related_party）须事先登记。
- 关联交易（law_related_party_transaction）须进行合规审查（compliance_status），确保交易公允。
- 关联交易金额超过阈值需报董事会审批。

## 八、创新与供应商

### 创新提案
- 创新提案（law_innovation_proposal）记录员工的创新建议和知识产权预评估。

### 供应商法务评估
- 供应商评估（law_supplier_assessment）从法律风险角度评估供应商资质。

### 高风险软件
- 高风险软件（law_high_risk_software）登记涉及开源协议合规、数据安全等法律风险的软件。

## 九、风险管理

### 业务风险
- 业务风险（law_business_risk）记录和跟踪各类法律及合规风险。
- 高风险事项须升级到对应负责人，不可自行降级处理。

### 法务制度
- 法务制度（law_policy）按类别（policy_category）管理，有版本控制。
- 制度变更需经法务审批后发布。

## 十、法务资产与数据完整性

### 法务资产
- 法务域资产（law_domain_asset）统一管理法务相关的文档、模板等资源。

### 数据完整性
- 所有引用字段（*_ref）必须指向已存在的实体，不存在时返回 "not found" 错误。
- 合同、印章、证据等关键法务记录不可物理删除，仅支持状态变更（如归档、作废）。
- 所有法务操作须保留完整审计轨迹，满足监管和诉讼举证要求。
