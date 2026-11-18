"""法务域工具集：在 OfficeTools 上扩展法务协作相关能力。"""

from typing import Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.law.models import (
    LawDB,
    LawContractTemplate,
    LawContractParty,
    LawContract,
    LawContractPartyLink,
    LawContractAmendment,
    LawContractTransfer,
    LawContractMilestone,
    LawContractRisk,
    LawContractLoan,
    LawApprovalFlow,
    LawApprovalStep,
    LawSeal,
    LawSealUsageRequest,
    LawIPAsset,
    LawIPInventor,
    LawIPApplication,
    LawIPAuthorization,
    LawIPReward,
    LawIntegrityDeclaration,
    LawViolationReport,
    LawLegalCase,
    LawCaseEvent,
    LawEvidence,
    LawLegalConsultation,
    LawComplianceReview,
    LawCorporateEntity,
    LawEntityChange,
    LawQualificationCertificate,
    LawLicenseUsageRequest,
    LawRelatedParty,
    LawRelatedPartyTransaction,
    LawInnovationProposal,
    LawSupplierAssessment,
    LawHighRiskSoftware,
    LawBusinessRisk,
    LawPolicy,
    LawDomainAsset,
)


class LawTools(OfficeTools):
    """法务域工具集：在 OfficeTools 上扩展法务协作相关能力。"""

    db: LawDB

    def __init__(self, db: LawDB) -> None:
        """
        使用 LawDB 实例初始化 LawTools。

        参数：
            db：包含全部法务域数据的 LawDB 实例。

        返回：
            无
        """
        super().__init__(db)

    # -----------------------
    # 内部辅助方法
    # -----------------------

    def _get_contract_template(self, contract_template_ref: str) -> LawContractTemplate:
        """
        根据 ref 获取合同模板。

        参数：
            contract_template_ref: 合同模板的唯一标识。

        返回：
            LawContractTemplate：合同模板对象。

        异常：
            ValueError：若未找到合同模板。
        """
        if contract_template_ref not in self.db.law_contract_template:
            raise ValueError("Contract template not found")
        return self.db.law_contract_template[contract_template_ref]

    def _get_contract_party(self, contract_party_ref: str) -> LawContractParty:
        """
        根据 ref 获取合同方。

        参数：
            contract_party_ref: 合同方的唯一标识。

        返回：
            LawContractParty：合同方对象。

        异常：
            ValueError：若未找到合同方。
        """
        if contract_party_ref not in self.db.law_contract_party:
            raise ValueError("Contract party not found")
        return self.db.law_contract_party[contract_party_ref]

    def _get_contract(self, contract_ref: str) -> LawContract:
        """
        根据 ref 获取合同。

        参数：
            contract_ref: 合同的唯一标识。

        返回：
            LawContract：合同对象。

        异常：
            ValueError：若未找到合同。
        """
        if contract_ref not in self.db.law_contract:
            raise ValueError("Contract not found")
        return self.db.law_contract[contract_ref]

    def _get_contract_amendment(self, contract_amendment_ref: str) -> LawContractAmendment:
        """
        根据 ref 获取合同变更。

        参数：
            contract_amendment_ref: 合同变更的唯一标识。

        返回：
            LawContractAmendment：合同变更对象。

        异常：
            ValueError：若未找到合同变更。
        """
        if contract_amendment_ref not in self.db.law_contract_amendment:
            raise ValueError("Contract amendment not found")
        return self.db.law_contract_amendment[contract_amendment_ref]

    def _get_contract_transfer(self, contract_transfer_ref: str) -> LawContractTransfer:
        """
        根据 ref 获取合同移交。

        参数：
            contract_transfer_ref: 合同移交的唯一标识。

        返回：
            LawContractTransfer：合同移交对象。

        异常：
            ValueError：若未找到合同移交。
        """
        if contract_transfer_ref not in self.db.law_contract_transfer:
            raise ValueError("Contract transfer not found")
        return self.db.law_contract_transfer[contract_transfer_ref]

    def _get_contract_milestone(self, contract_milestone_ref: str) -> LawContractMilestone:
        """
        根据 ref 获取合同里程碑。

        参数：
            contract_milestone_ref: 合同里程碑的唯一标识。

        返回：
            LawContractMilestone：合同里程碑对象。

        异常：
            ValueError：若未找到合同里程碑。
        """
        if contract_milestone_ref not in self.db.law_contract_milestone:
            raise ValueError("Contract milestone not found")
        return self.db.law_contract_milestone[contract_milestone_ref]

    def _get_contract_risk(self, contract_risk_ref: str) -> LawContractRisk:
        """
        根据 ref 获取合同风险。

        参数：
            contract_risk_ref: 合同风险的唯一标识。

        返回：
            LawContractRisk：合同风险对象。

        异常：
            ValueError：若未找到合同风险。
        """
        if contract_risk_ref not in self.db.law_contract_risk:
            raise ValueError("Contract risk not found")
        return self.db.law_contract_risk[contract_risk_ref]

    def _get_contract_loan(self, contract_loan_ref: str) -> LawContractLoan:
        """
        根据 ref 获取合同外借。

        参数：
            contract_loan_ref: 合同外借的唯一标识。

        返回：
            LawContractLoan：合同外借对象。

        异常：
            ValueError：若未找到合同外借记录。
        """
        if contract_loan_ref not in self.db.law_contract_loan:
            raise ValueError("Contract loan not found")
        return self.db.law_contract_loan[contract_loan_ref]

    def _get_approval_flow(self, approval_flow_ref: str) -> LawApprovalFlow:
        """
        根据 ref 获取审批流。

        参数：
            approval_flow_ref: 审批流的唯一标识。

        返回：
            LawApprovalFlow：审批流对象。

        异常：
            ValueError：若未找到审批流。
        """
        if approval_flow_ref not in self.db.law_approval_flow:
            raise ValueError("Approval flow not found")
        return self.db.law_approval_flow[approval_flow_ref]

    def _get_approval_step(self, approval_step_ref: str) -> LawApprovalStep:
        """
        根据 ref 获取审批步骤。

        参数：
            approval_step_ref: 审批步骤的唯一标识。

        返回：
            LawApprovalStep：审批步骤对象。

        异常：
            ValueError：若未找到审批步骤。
        """
        if approval_step_ref not in self.db.law_approval_step:
            raise ValueError("Approval step not found")
        return self.db.law_approval_step[approval_step_ref]

    def _get_seal(self, seal_ref: str) -> LawSeal:
        """
        根据 ref 获取印章。

        参数：
            seal_ref: 印章的唯一标识。

        返回：
            LawSeal：印章对象。

        异常：
            ValueError：若未找到印章。
        """
        if seal_ref not in self.db.law_seal:
            raise ValueError("Seal not found")
        return self.db.law_seal[seal_ref]

    def _get_seal_usage_request(self, seal_usage_request_ref: str) -> LawSealUsageRequest:
        """
        根据 ref 获取用印申请。

        参数：
            seal_usage_request_ref: 用印申请的唯一标识。

        返回：
            LawSealUsageRequest：用印申请对象。

        异常：
            ValueError：若未找到用印申请。
        """
        if seal_usage_request_ref not in self.db.law_seal_usage_request:
            raise ValueError("Seal usage request not found")
        return self.db.law_seal_usage_request[seal_usage_request_ref]

    def _get_ip_asset(self, ip_asset_ref: str) -> LawIPAsset:
        """
        根据 ref 获取知识产权资产。

        参数：
            ip_asset_ref: 知识产权资产的唯一标识。

        返回：
            LawIPAsset：知识产权资产对象。

        异常：
            ValueError：若未找到知识产权资产。
        """
        if ip_asset_ref not in self.db.law_ip_asset:
            raise ValueError("IP asset not found")
        return self.db.law_ip_asset[ip_asset_ref]

    def _get_ip_application(self, ip_application_ref: str) -> LawIPApplication:
        """
        根据 ref 获取知识产权申请。

        参数：
            ip_application_ref: 知识产权申请的唯一标识。

        返回：
            LawIPApplication：知识产权申请对象。

        异常：
            ValueError：若未找到知识产权申请。
        """
        if ip_application_ref not in self.db.law_ip_application:
            raise ValueError("IP application not found")
        return self.db.law_ip_application[ip_application_ref]

    def _get_ip_authorization(self, ip_authorization_ref: str) -> LawIPAuthorization:
        """
        根据 ref 获取知识产权授权。

        参数：
            ip_authorization_ref: 知识产权授权的唯一标识。

        返回：
            LawIPAuthorization：知识产权授权对象。

        异常：
            ValueError：若未找到知识产权授权。
        """
        if ip_authorization_ref not in self.db.law_ip_authorization:
            raise ValueError("IP authorization not found")
        return self.db.law_ip_authorization[ip_authorization_ref]

    def _get_ip_reward(self, ip_reward_ref: str) -> LawIPReward:
        """
        根据 ref 获取知识产权奖励。

        参数：
            ip_reward_ref: 知识产权奖励的唯一标识。

        返回：
            LawIPReward：知识产权奖励对象。

        异常：
            ValueError：若未找到知识产权奖励。
        """
        if ip_reward_ref not in self.db.law_ip_reward:
            raise ValueError("IP reward not found")
        return self.db.law_ip_reward[ip_reward_ref]

    def _get_integrity_declaration(self, integrity_declaration_ref: str) -> LawIntegrityDeclaration:
        """
        根据 ref 获取廉洁申报。

        参数：
            integrity_declaration_ref: 廉洁申报的唯一标识。

        返回：
            LawIntegrityDeclaration：廉洁申报对象。

        异常：
            ValueError：若未找到廉洁申报。
        """
        if integrity_declaration_ref not in self.db.law_integrity_declaration:
            raise ValueError("Integrity declaration not found")
        return self.db.law_integrity_declaration[integrity_declaration_ref]

    def _get_violation_report(self, violation_report_ref: str) -> LawViolationReport:
        """
        根据 ref 获取违规举报。

        参数：
            violation_report_ref: 违规举报的唯一标识。

        返回：
            LawViolationReport：违规举报对象。

        异常：
            ValueError：若未找到违规举报。
        """
        if violation_report_ref not in self.db.law_violation_report:
            raise ValueError("Violation report not found")
        return self.db.law_violation_report[violation_report_ref]

    def _get_legal_case(self, legal_case_ref: str) -> LawLegalCase:
        """
        根据 ref 获取法务案件。

        参数：
            legal_case_ref: 法务案件的唯一标识。

        返回：
            LawLegalCase：法务案件对象。

        异常：
            ValueError：若未找到法务案件。
        """
        if legal_case_ref not in self.db.law_legal_case:
            raise ValueError("Legal case not found")
        return self.db.law_legal_case[legal_case_ref]

    def _get_case_event(self, case_event_ref: str) -> LawCaseEvent:
        """
        根据 ref 获取案件事件。

        参数：
            case_event_ref: 案件事件的唯一标识。

        返回：
            LawCaseEvent：案件事件对象。

        异常：
            ValueError：若未找到案件事件。
        """
        if case_event_ref not in self.db.law_case_event:
            raise ValueError("Case event not found")
        return self.db.law_case_event[case_event_ref]

    def _get_evidence(self, evidence_ref: str) -> LawEvidence:
        """
        根据 ref 获取证据记录。

        参数：
            evidence_ref: 证据的唯一标识。

        返回：
            LawEvidence：证据对象。

        异常：
            ValueError：若未找到证据。
        """
        if evidence_ref not in self.db.law_evidence:
            raise ValueError("Evidence not found")
        return self.db.law_evidence[evidence_ref]

    def _get_legal_consultation(self, legal_consultation_ref: str) -> LawLegalConsultation:
        """
        根据 ref 获取法律咨询。

        参数：
            legal_consultation_ref: 法律咨询的唯一标识。

        返回：
            LawLegalConsultation：法律咨询对象。

        异常：
            ValueError：若未找到法律咨询。
        """
        if legal_consultation_ref not in self.db.law_legal_consultation:
            raise ValueError("Legal consultation not found")
        return self.db.law_legal_consultation[legal_consultation_ref]

    def _get_compliance_review(self, compliance_review_ref: str) -> LawComplianceReview:
        """
        根据 ref 获取合规审查。

        参数：
            compliance_review_ref: 合规审查的唯一标识。

        返回：
            LawComplianceReview：合规审查对象。

        异常：
            ValueError：若未找到合规审查。
        """
        if compliance_review_ref not in self.db.law_compliance_review:
            raise ValueError("Compliance review not found")
        return self.db.law_compliance_review[compliance_review_ref]

    def _get_corporate_entity(self, corporate_entity_ref: str) -> LawCorporateEntity:
        """
        根据 ref 获取公司主体。

        参数：
            corporate_entity_ref: 公司主体的唯一标识。

        返回：
            LawCorporateEntity：公司主体对象。

        异常：
            ValueError：若未找到公司主体。
        """
        if corporate_entity_ref not in self.db.law_corporate_entity:
            raise ValueError("Corporate entity not found")
        return self.db.law_corporate_entity[corporate_entity_ref]

    def _get_entity_change(self, entity_change_ref: str) -> LawEntityChange:
        """
        根据 ref 获取主体变更。

        参数：
            entity_change_ref: 主体变更的唯一标识。

        返回：
            LawEntityChange：主体变更对象。

        异常：
            ValueError：若未找到主体变更。
        """
        if entity_change_ref not in self.db.law_entity_change:
            raise ValueError("Entity change not found")
        return self.db.law_entity_change[entity_change_ref]

    def _get_qualification_certificate(self, qualification_certificate_ref: str) -> LawQualificationCertificate:
        """
        根据 ref 获取资质证书。

        参数：
            qualification_certificate_ref: 资质证书的唯一标识。

        返回：
            LawQualificationCertificate：资质证书对象。

        异常：
            ValueError：若未找到资质证书。
        """
        if qualification_certificate_ref not in self.db.law_qualification_certificate:
            raise ValueError("Qualification certificate not found")
        return self.db.law_qualification_certificate[qualification_certificate_ref]

    def _get_license_usage_request(self, license_usage_request_ref: str) -> LawLicenseUsageRequest:
        """
        根据 ref 获取证照使用申请。

        参数：
            license_usage_request_ref: 证照使用申请的唯一标识。

        返回：
            LawLicenseUsageRequest：证照使用申请对象。

        异常：
            ValueError：若未找到证照使用申请。
        """
        if license_usage_request_ref not in self.db.law_license_usage_request:
            raise ValueError("License usage request not found")
        return self.db.law_license_usage_request[license_usage_request_ref]

    def _get_related_party(self, related_party_ref: str) -> LawRelatedParty:
        """
        根据 ref 获取关联方。

        参数：
            related_party_ref: 关联方的唯一标识。

        返回：
            LawRelatedParty：关联方对象。

        异常：
            ValueError：若未找到关联方。
        """
        if related_party_ref not in self.db.law_related_party:
            raise ValueError("Related party not found")
        return self.db.law_related_party[related_party_ref]

    def _get_related_party_transaction(self, related_party_transaction_ref: str) -> LawRelatedPartyTransaction:
        """
        根据 ref 获取关联方交易。

        参数：
            related_party_transaction_ref: 关联方交易的唯一标识。

        返回：
            LawRelatedPartyTransaction：关联方交易对象。

        异常：
            ValueError：若未找到关联方交易。
        """
        if related_party_transaction_ref not in self.db.law_related_party_transaction:
            raise ValueError("Related party transaction not found")
        return self.db.law_related_party_transaction[related_party_transaction_ref]

    def _get_innovation_proposal(self, innovation_proposal_ref: str) -> LawInnovationProposal:
        """
        根据 ref 获取创新提案。

        参数：
            innovation_proposal_ref: 创新提案的唯一标识。

        返回：
            LawInnovationProposal：创新提案对象。

        异常：
            ValueError：若未找到创新提案。
        """
        if innovation_proposal_ref not in self.db.law_innovation_proposal:
            raise ValueError("Innovation proposal not found")
        return self.db.law_innovation_proposal[innovation_proposal_ref]

    def _get_supplier_assessment(self, supplier_assessment_ref: str) -> LawSupplierAssessment:
        """
        根据 ref 获取供应商评估。

        参数：
            supplier_assessment_ref: 供应商评估的唯一标识。

        返回：
            LawSupplierAssessment：供应商评估对象。

        异常：
            ValueError：若未找到供应商评估。
        """
        if supplier_assessment_ref not in self.db.law_supplier_assessment:
            raise ValueError("Supplier assessment not found")
        return self.db.law_supplier_assessment[supplier_assessment_ref]

    def _get_high_risk_software(self, high_risk_software_ref: str) -> LawHighRiskSoftware:
        """
        根据 ref 获取高风险软件记录。

        参数：
            high_risk_software_ref: 高风险软件记录的唯一标识。

        返回：
            LawHighRiskSoftware：高风险软件对象。

        异常：
            ValueError：若未找到高风险软件记录。
        """
        if high_risk_software_ref not in self.db.law_high_risk_software:
            raise ValueError("High-risk software not found")
        return self.db.law_high_risk_software[high_risk_software_ref]

    def _get_business_risk(self, business_risk_ref: str) -> LawBusinessRisk:
        """
        根据 ref 获取业务风险。

        参数：
            business_risk_ref: 业务风险的唯一标识。

        返回：
            LawBusinessRisk：业务风险对象。

        异常：
            ValueError：若未找到业务风险。
        """
        if business_risk_ref not in self.db.law_business_risk:
            raise ValueError("Business risk not found")
        return self.db.law_business_risk[business_risk_ref]

    def _get_policy(self, policy_ref: str) -> LawPolicy:
        """
        根据 ref 获取制度/政策。

        参数：
            policy_ref: 制度的唯一标识。

        返回：
            LawPolicy：制度对象。

        异常：
            ValueError：若未找到制度。
        """
        if policy_ref not in self.db.law_policy:
            raise ValueError("Policy not found")
        return self.db.law_policy[policy_ref]

    def _get_domain_asset(self, domain_asset_ref: str) -> LawDomainAsset:
        """
        根据 ref 获取域名资产。

        参数：
            domain_asset_ref: 域名资产的唯一标识。

        返回：
            LawDomainAsset：域名资产对象。

        异常：
            ValueError：若未找到域名资产。
        """
        if domain_asset_ref not in self.db.law_domain_asset:
            raise ValueError("Domain asset not found")
        return self.db.law_domain_asset[domain_asset_ref]

    # ========================================
    # 合同模板（只读）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_template_details(self, contract_template_ref: str) -> LawContractTemplate:
        """
        根据 ref 获取合同模板详情。

        参数：
            contract_template_ref: 合同模板的唯一标识。

        返回：
            LawContractTemplate：合同模板对象。

        异常：
            ValueError：若未找到合同模板。
        """
        return self._get_contract_template(contract_template_ref)

    @is_tool(ToolType.READ)
    def list_contract_templates(
        self,
        contract_category: Optional[str] = None,
        template_status: Optional[str] = None,
    ) -> str:
        """
        列出合同模板（可选筛选）。

        参数：
            contract_category: 按 contract category (e.g., sales, procurement) 筛选。默认 None。
            template_status: 按 template status (active, inactive, deprecated) 筛选。默认 None。

        返回：
            str：匹配「contract templates」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, t in self.db.law_contract_template.items():
            if contract_category is not None and t.contract_category != contract_category:
                continue
            if template_status is not None and t.template_status != template_status:
                continue
            results.append({
                "contract_template_ref": t.contract_template_ref,
                "template_name": t.template_name,
                "template_code": t.template_code,
                "contract_category": t.contract_category,
                "template_version": t.template_version,
                "template_status": t.template_status,
                "created_by_ref": t.created_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_contract_template_ref_by_name(self, template_name: str) -> str:
        """
        按名称模糊查找合同模板 ref（不区分大小写）。

        参数：
            template_name: 合同模板名称（可部分匹配）。

        返回：
            str：匹配到的template 的 contract_template_ref。

        异常：
            ValueError：若未匹配到模板。
        """
        search = template_name.lower()
        for ref, t in self.db.law_contract_template.items():
            if search in t.template_name.lower():
                return ref
        raise ValueError("Contract template not found")

    # ========================================
    # 合同方（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_party_details(self, contract_party_ref: str) -> LawContractParty:
        """
        根据 ref 获取合同方详情。

        参数：
            contract_party_ref: 合同方的唯一标识。

        返回：
            LawContractParty：合同方对象。

        异常：
            ValueError：若未找到合同方。
        """
        return self._get_contract_party(contract_party_ref)

    @is_tool(ToolType.READ)
    def list_contract_parties(
        self,
        party_type: Optional[str] = None,
        party_status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> str:
        """
        列出合同方（可选筛选）。

        参数：
            party_type: 按 party type (enterprise, individual, government, ngo) 筛选。默认 None。
            party_status: 按 party status (active, inactive, blacklisted) 筛选。默认 None。
            risk_level: 按 risk level (low, medium, high, critical) 筛选。默认 None。

        返回：
            str：匹配「contract parties」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.law_contract_party.items():
            if party_type is not None and p.party_type != party_type:
                continue
            if party_status is not None and p.party_status != party_status:
                continue
            if risk_level is not None and p.risk_level != risk_level:
                continue
            results.append({
                "contract_party_ref": p.contract_party_ref,
                "party_name": p.party_name,
                "party_type": p.party_type,
                "unified_social_credit_code": p.unified_social_credit_code,
                "party_status": p.party_status,
                "risk_level": p.risk_level,
                "contact_name": p.contact_name,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_contract_party_ref_by_name(self, party_name: str) -> str:
        """
        按名称模糊查找合同方 ref（不区分大小写）。

        参数：
            party_name: 合同方名称（可部分匹配）。

        返回：
            str：匹配到的party 的 contract_party_ref。

        异常：
            ValueError：若未匹配到合同方。
        """
        search = party_name.lower()
        for ref, p in self.db.law_contract_party.items():
            if search in p.party_name.lower():
                return ref
        raise ValueError("Contract party not found")

    @is_tool(ToolType.WRITE)
    def update_contract_party_status(
        self,
        contract_party_ref: str,
        new_status: str,
    ) -> LawContractParty:
        """
        更新合同方状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_party_ref: 合同方的唯一标识。
            new_status: 要设置的新状态（active、inactive、blacklisted）。

        返回：
            LawContractParty：更新后的合同方对象。

        异常：
            ValueError：若未找到合同方或状态无效。
        """
        party = self._get_contract_party(contract_party_ref)
        valid_statuses = {"active", "inactive", "blacklisted"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        party.party_status = new_status
        party.updated_at = self._now_iso()
        return party

    # ========================================
    # 合同（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_details(self, contract_ref: str) -> LawContract:
        """
        根据 ref 获取合同详情。

        参数：
            contract_ref: 合同的唯一标识。

        返回：
            LawContract：合同对象。

        异常：
            ValueError：若未找到合同。
        """
        return self._get_contract(contract_ref)

    @is_tool(ToolType.READ)
    def search_contracts(
        self,
        contract_category: Optional[str] = None,
        contract_type: Optional[str] = None,
        contract_status: Optional[str] = None,
        risk_level: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        currency: Optional[str] = None,
        title_keyword: Optional[str] = None,
    ) -> str:
        """
        搜索合同（可选筛选）。

        参数：
            contract_category: 按 contract category 筛选。默认 None。
            contract_type: 按 contract type 筛选。默认 None。
            contract_status: 按 contract status 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            owner_employee_ref: 按 owner employee ref 筛选。默认 None。
            department_ref: 按 department ref 筛选。默认 None。
            currency: 按 currency 筛选。默认 None。
            title_keyword: 按 keyword in contract title (case-insensitive) 筛选。默认 None。

        返回：
            str：匹配「contracts」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, c in self.db.law_contract.items():
            if contract_category is not None and c.contract_category != contract_category:
                continue
            if contract_type is not None and c.contract_type != contract_type:
                continue
            if contract_status is not None and c.contract_status != contract_status:
                continue
            if risk_level is not None and c.risk_level != risk_level:
                continue
            if owner_employee_ref is not None and c.owner_employee_ref != owner_employee_ref:
                continue
            if department_ref is not None and c.department_ref != department_ref:
                continue
            if currency is not None and c.currency != currency:
                continue
            if title_keyword is not None and title_keyword.lower() not in c.contract_title.lower():
                continue
            results.append({
                "contract_ref": c.contract_ref,
                "contract_number": c.contract_number,
                "contract_title": c.contract_title,
                "contract_category": c.contract_category,
                "contract_type": c.contract_type,
                "contract_status": c.contract_status,
                "risk_level": c.risk_level,
                "total_amount": c.total_amount,
                "currency": c.currency,
                "effective_date": c.effective_date,
                "expiry_date": c.expiry_date,
                "owner_employee_ref": c.owner_employee_ref,
                "department_ref": c.department_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_contracts_by_employee(self, employee_ref: str) -> str:
        """
        列出某员工名下的全部合同。

        参数：
            employee_ref: 合同负责人的员工 ref。

        返回：
            str：contracts owned by the employee 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, c in self.db.law_contract.items():
            if c.owner_employee_ref == employee_ref:
                results.append({
                    "contract_ref": c.contract_ref,
                    "contract_number": c.contract_number,
                    "contract_title": c.contract_title,
                    "contract_category": c.contract_category,
                    "contract_status": c.contract_status,
                    "total_amount": c.total_amount,
                    "currency": c.currency,
                    "effective_date": c.effective_date,
                    "expiry_date": c.expiry_date,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_contracts_by_department(self, department_ref: str) -> str:
        """
        列出某部门的全部合同。

        参数：
            department_ref: 部门 ref。

        返回：
            str：contracts in the department 的 JSON 数组。

        异常：
            ValueError：若未找到部门。
        """
        self._get_department(department_ref)
        results = []
        for ref, c in self.db.law_contract.items():
            if c.department_ref == department_ref:
                results.append({
                    "contract_ref": c.contract_ref,
                    "contract_number": c.contract_number,
                    "contract_title": c.contract_title,
                    "contract_category": c.contract_category,
                    "contract_status": c.contract_status,
                    "total_amount": c.total_amount,
                    "currency": c.currency,
                    "effective_date": c.effective_date,
                    "expiry_date": c.expiry_date,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_contract_ref_by_number(self, contract_number: str) -> str:
        """
        按合同编号查找合同 ref。

        参数：
            contract_number: 可读合同编号。

        返回：
            str：匹配到的contract 的 contract_ref。

        异常：
            ValueError：若未匹配到合同。
        """
        for ref, c in self.db.law_contract.items():
            if c.contract_number == contract_number:
                return ref
        raise ValueError("Contract not found")

    @is_tool(ToolType.WRITE)
    def create_contract(
        self,
        contract_number: str,
        contract_title: str,
        contract_category: str,
        contract_type: str,
        currency: str,
        total_amount: float,
        effective_date: str,
        expiry_date: str,
        owner_employee_ref: str,
        department_ref: str,
        summary: str,
        special_terms: str = "",
        template_ref: Optional[str] = None,
        parent_contract_ref: Optional[str] = None,
        our_entity_ref: Optional[str] = None,
        risk_level: str = "low",
    ) -> LawContract:
        """
        新建草稿状态合同。调用前 Agent 须向用户明确确认。

        参数：
            contract_number: 可读合同编号。
            contract_title: 合同标题。
            contract_category: 合同类别（销售、采购、服务等）。
            contract_type: 合同类型（standard、framework、supplementary、renewal）。
            currency: 币种（CNY、USD、EUR、GBP、JPY、HKD）。
            total_amount: 合同总金额。
            effective_date: 生效日期（ISO 8601 日期）。
            expiry_date: 到期日期（ISO 8601 日期）。
            owner_employee_ref: 合同负责人的员工 ref。
            department_ref: 合同责任部门 ref。
            summary: 摘要描述。
            special_terms: Special terms and conditions。默认 ""
            template_ref: 引用：contract template used。默认 None。
            parent_contract_ref: 父合同引用。Defaults to None.
            our_entity_ref: Reference to our corporate entity。默认 None。
            risk_level: Risk level (low, medium, high, critical)。默认 "low"。

        返回：
            LawContract：新建的合同对象。

        异常：
            ValueError：若必填引用无效或入参格式错误。
        """
        self._get_employee(owner_employee_ref)
        self._get_department(department_ref)
        if template_ref is not None:
            self._get_contract_template(template_ref)
        if parent_contract_ref is not None:
            self._get_contract(parent_contract_ref)
        if our_entity_ref is not None:
            self._get_corporate_entity(our_entity_ref)

        valid_categories = {"sales", "procurement", "service", "lease", "employment", "nda", "partnership", "licensing", "construction", "other"}
        if contract_category not in valid_categories:
            raise ValueError(f"Invalid contract_category: {contract_category}")
        valid_types = {"standard", "framework", "supplementary", "renewal"}
        if contract_type not in valid_types:
            raise ValueError(f"Invalid contract_type: {contract_type}")
        valid_currencies = {"CNY", "USD", "EUR", "GBP", "JPY", "HKD"}
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency: {currency}")
        valid_risk_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")

        now = self._now_iso()
        ref = self._generate_ref("CON", self.db.law_contract)

        contract = LawContract(
            contract_ref=ref,
            contract_number=contract_number,
            contract_title=contract_title,
            contract_category=contract_category,
            contract_type=contract_type,
            template_ref=template_ref,
            parent_contract_ref=parent_contract_ref,
            our_entity_ref=our_entity_ref,
            currency=currency,
            total_amount=total_amount,
            effective_date=effective_date,
            expiry_date=expiry_date,
            signing_date=None,
            termination_date=None,
            contract_status="draft",
            risk_level=risk_level,
            owner_employee_ref=owner_employee_ref,
            department_ref=department_ref,
            contract_file_ref=None,
            summary=summary,
            special_terms=special_terms,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract[ref] = contract
        return contract

    @is_tool(ToolType.WRITE)
    def update_contract_status(
        self,
        contract_ref: str,
        new_status: str,
    ) -> LawContract:
        """
        更新合同状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 合同的唯一标识。
            new_status: 新状态（draft、pending_approval、approved、signed、active、suspended、expired、terminated、cancelled）。

        返回：
            LawContract：更新后的合同对象。

        异常：
            ValueError：若未找到合同或状态流转无效。
        """
        contract = self._get_contract(contract_ref)
        valid_statuses = {
            "draft", "pending_approval", "approved", "signed", "active",
            "suspended", "expired", "terminated", "cancelled"
        }
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if new_status == "signed" and contract.signing_date is None:
            contract.signing_date = now
        if new_status == "terminated" and contract.termination_date is None:
            contract.termination_date = now

        contract.contract_status = new_status
        contract.updated_at = now
        return contract

    @is_tool(ToolType.WRITE)
    def submit_contract_for_approval(self, contract_ref: str) -> LawContract:
        """
        提交草稿合同进入审批。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 合同的唯一标识。

        返回：
            LawContract：更新后的合同对象（状态为 pending_approval）。

        异常：
            ValueError：若合同非草稿状态。
        """
        contract = self._get_contract(contract_ref)
        if contract.contract_status != "draft":
            raise ValueError(f"Contract must be in 'draft' status to submit for approval, current status: {contract.contract_status}")
        contract.contract_status = "pending_approval"
        contract.updated_at = self._now_iso()
        return contract

    @is_tool(ToolType.WRITE)
    def terminate_contract(
        self,
        contract_ref: str,
        termination_date: Optional[str] = None,
    ) -> LawContract:
        """
        终止生效中或已暂停的合同。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 合同的唯一标识。
            termination_date: Date of termination (ISO 8601)。若为 None 则默认当前时间。

        返回：
            LawContract：更新后的合同对象。

        异常：
            ValueError：若当前状态不允许终止合同。
        """
        contract = self._get_contract(contract_ref)
        terminable_statuses = {"active", "suspended", "signed"}
        if contract.contract_status not in terminable_statuses:
            raise ValueError(f"Contract cannot be terminated from status '{contract.contract_status}'")
        now = self._now_iso()
        contract.contract_status = "terminated"
        contract.termination_date = termination_date if termination_date else now
        contract.updated_at = now
        return contract

    # ========================================
    # 合同—签约方关联（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_party_link_details(self, contract_party_link_ref: str) -> LawContractPartyLink:
        """
        根据 ref 获取合同—签约方关联详情。

        参数：
            contract_party_link_ref: 合同—签约方关联的唯一标识。

        返回：
            LawContractPartyLink：合同—签约方关联对象。

        异常：
            ValueError：若未找到签约方关联。
        """
        if contract_party_link_ref not in self.db.law_contract_party_link:
            raise ValueError("Contract party link not found")
        return self.db.law_contract_party_link[contract_party_link_ref]

    @is_tool(ToolType.READ)
    def list_contract_party_links(self, contract_ref: str) -> str:
        """
        列出某合同的全部签约方关联。

        参数：
            contract_ref: 合同的唯一标识。

        返回：
            str：contract-party links 的 JSON 数组。

        异常：
            ValueError：若未找到合同。
        """
        self._get_contract(contract_ref)
        results = []
        for ref, link in self.db.law_contract_party_link.items():
            if link.contract_ref == contract_ref:
                party = self._get_contract_party(link.contract_party_ref)
                results.append({
                    "contract_party_link_ref": link.contract_party_link_ref,
                    "contract_ref": link.contract_ref,
                    "contract_party_ref": link.contract_party_ref,
                    "party_name": party.party_name,
                    "party_role": link.party_role,
                    "signing_status": link.signing_status,
                    "signed_at": link.signed_at,
                    "signer_name": link.signer_name,
                })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_contract_party_signing_status(
        self,
        contract_party_link_ref: str,
        signing_status: str,
        signer_name: Optional[str] = None,
    ) -> LawContractPartyLink:
        """
        更新合同签约方的签署状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_party_link_ref: 合同—签约方关联的唯一标识。
            signing_status: 新签署状态（pending、signed、rejected）。
            signer_name: 签署人姓名；当 signing_status 为 'signed' 时必填。默认 None。

        返回：
            LawContractPartyLink：更新后的合同—签约方关联对象。

        异常：
            ValueError：若未找到关联或状态无效。
        """
        if contract_party_link_ref not in self.db.law_contract_party_link:
            raise ValueError("Contract party link not found")
        link = self.db.law_contract_party_link[contract_party_link_ref]
        valid_statuses = {"pending", "signed", "rejected"}
        if signing_status not in valid_statuses:
            raise ValueError(f"Invalid signing_status: {signing_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        link.signing_status = signing_status
        if signing_status == "signed":
            link.signed_at = now
            if signer_name:
                link.signer_name = signer_name
        link.updated_at = now
        return link

    # ========================================
    # 合同变更（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_amendment_details(self, contract_amendment_ref: str) -> LawContractAmendment:
        """
        根据 ref 获取合同变更详情。

        参数：
            contract_amendment_ref: 合同变更的唯一标识。

        返回：
            LawContractAmendment：合同变更对象。

        异常：
            ValueError：若未找到合同变更。
        """
        return self._get_contract_amendment(contract_amendment_ref)

    @is_tool(ToolType.READ)
    def list_contract_amendments(
        self,
        contract_ref: Optional[str] = None,
        amendment_type: Optional[str] = None,
        amendment_status: Optional[str] = None,
    ) -> str:
        """
        列出合同变更（可选筛选）。

        参数：
            contract_ref: 按 contract ref 筛选。默认 None。
            amendment_type: 按 amendment type (modification, supplement, renewal, termination) 筛选。默认 None。
            amendment_status: 按 amendment status 筛选。默认 None。

        返回：
            str：匹配「contract amendments」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, a in self.db.law_contract_amendment.items():
            if contract_ref is not None and a.contract_ref != contract_ref:
                continue
            if amendment_type is not None and a.amendment_type != amendment_type:
                continue
            if amendment_status is not None and a.amendment_status != amendment_status:
                continue
            results.append({
                "contract_amendment_ref": a.contract_amendment_ref,
                "contract_ref": a.contract_ref,
                "amendment_type": a.amendment_type,
                "amendment_number": a.amendment_number,
                "amendment_title": a.amendment_title,
                "amount_change": a.amount_change,
                "amendment_status": a.amendment_status,
                "initiated_by_ref": a.initiated_by_ref,
                "effective_date": a.effective_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_contract_amendment(
        self,
        contract_ref: str,
        amendment_type: str,
        amendment_number: str,
        amendment_title: str,
        reason: str,
        changes_summary: str,
        amount_change: float,
        initiated_by_ref: str,
        new_expiry_date: Optional[str] = None,
    ) -> LawContractAmendment:
        """
        新建草稿状态合同变更。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 引用：contract being amended.
            amendment_type: 变更类型（modification、supplement、renewal、termination）。
            amendment_number: 可读变更编号。
            amendment_title: 变更标题。
            reason: 变更原因。
            changes_summary: 变更摘要。
            amount_change: 合同金额变动。
            initiated_by_ref: 发起人员工 ref。
            new_expiry_date: New expiry date if applicable。默认 None。

        返回：
            LawContractAmendment：新建的变更对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_contract(contract_ref)
        self._get_employee(initiated_by_ref)
        valid_types = {"modification", "supplement", "renewal", "termination"}
        if amendment_type not in valid_types:
            raise ValueError(f"Invalid amendment_type: {amendment_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("AMEND", self.db.law_contract_amendment)

        amendment = LawContractAmendment(
            contract_amendment_ref=ref,
            contract_ref=contract_ref,
            amendment_type=amendment_type,
            amendment_number=amendment_number,
            amendment_title=amendment_title,
            reason=reason,
            changes_summary=changes_summary,
            amount_change=amount_change,
            new_expiry_date=new_expiry_date,
            amendment_status="draft",
            amendment_file_ref=None,
            initiated_by_ref=initiated_by_ref,
            effective_date=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract_amendment[ref] = amendment
        return amendment

    @is_tool(ToolType.WRITE)
    def update_contract_amendment_status(
        self,
        contract_amendment_ref: str,
        new_status: str,
    ) -> LawContractAmendment:
        """
        更新合同变更状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_amendment_ref: 合同变更的唯一标识。
            new_status: 新状态（draft、pending_approval、approved、rejected、effective）。

        返回：
            LawContractAmendment：更新后的变更对象。

        异常：
            ValueError：若未找到变更或状态无效。
        """
        amendment = self._get_contract_amendment(contract_amendment_ref)
        valid_statuses = {"draft", "pending_approval", "approved", "rejected", "effective"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "effective" and amendment.effective_date is None:
            amendment.effective_date = now
        amendment.amendment_status = new_status
        amendment.updated_at = now
        return amendment

    # ========================================
    # 合同移交（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_transfer_details(self, contract_transfer_ref: str) -> LawContractTransfer:
        """
        根据 ref 获取合同移交详情。

        参数：
            contract_transfer_ref: 合同移交的唯一标识。

        返回：
            LawContractTransfer：合同移交对象。

        异常：
            ValueError：若未找到合同移交。
        """
        return self._get_contract_transfer(contract_transfer_ref)

    @is_tool(ToolType.READ)
    def list_contract_transfers(
        self,
        contract_ref: Optional[str] = None,
        transfer_status: Optional[str] = None,
    ) -> str:
        """
        列出合同移交（可选筛选）。

        参数：
            contract_ref: 按 contract ref 筛选。默认 None。
            transfer_status: 按 transfer status 筛选。默认 None。

        返回：
            str：匹配「contract transfers」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, t in self.db.law_contract_transfer.items():
            if contract_ref is not None and t.contract_ref != contract_ref:
                continue
            if transfer_status is not None and t.transfer_status != transfer_status:
                continue
            results.append({
                "contract_transfer_ref": t.contract_transfer_ref,
                "contract_ref": t.contract_ref,
                "transfer_type": t.transfer_type,
                "from_employee_ref": t.from_employee_ref,
                "to_employee_ref": t.to_employee_ref,
                "from_department_ref": t.from_department_ref,
                "to_department_ref": t.to_department_ref,
                "transfer_status": t.transfer_status,
                "reason": t.reason,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_contract_transfer(
        self,
        contract_ref: str,
        transfer_type: str,
        from_employee_ref: str,
        to_employee_ref: str,
        reason: str,
        from_department_ref: Optional[str] = None,
        to_department_ref: Optional[str] = None,
    ) -> LawContractTransfer:
        """
        新建合同移交申请。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 引用：contract being transferred.
            transfer_type: 移交类型（owner_change、department_change、both）。
            from_employee_ref: 原负责人的员工 ref。
            to_employee_ref: 新负责人的员工 ref。
            reason: 移交原因。
            from_department_ref: Current department ref (required for department_change or both)。默认 None。
            to_department_ref: New department ref (required for department_change or both)。默认 None。

        返回：
            LawContractTransfer：新建的移交对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_contract(contract_ref)
        self._get_employee(from_employee_ref)
        self._get_employee(to_employee_ref)
        valid_types = {"owner_change", "department_change", "both"}
        if transfer_type not in valid_types:
            raise ValueError(f"Invalid transfer_type: {transfer_type}. Must be one of {valid_types}")
        if transfer_type in ("department_change", "both"):
            if from_department_ref is None or to_department_ref is None:
                raise ValueError("from_department_ref and to_department_ref are required for department transfers")
            self._get_department(from_department_ref)
            self._get_department(to_department_ref)

        now = self._now_iso()
        ref = self._generate_ref("CTRANS", self.db.law_contract_transfer)

        transfer = LawContractTransfer(
            contract_transfer_ref=ref,
            contract_ref=contract_ref,
            transfer_type=transfer_type,
            from_employee_ref=from_employee_ref,
            to_employee_ref=to_employee_ref,
            from_department_ref=from_department_ref,
            to_department_ref=to_department_ref,
            reason=reason,
            transfer_status="pending",
            transferred_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract_transfer[ref] = transfer
        return transfer

    @is_tool(ToolType.WRITE)
    def update_contract_transfer_status(
        self,
        contract_transfer_ref: str,
        new_status: str,
    ) -> LawContractTransfer:
        """
        更新合同移交状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_transfer_ref: 合同移交的唯一标识。
            new_status: 新状态（pending、approved、rejected、completed）。

        返回：
            LawContractTransfer：更新后的移交对象。

        异常：
            ValueError：若未找到移交或状态无效。
        """
        transfer = self._get_contract_transfer(contract_transfer_ref)
        valid_statuses = {"pending", "approved", "rejected", "completed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "completed":
            transfer.transferred_at = now
            # 更新合同归属
            contract = self._get_contract(transfer.contract_ref)
            contract.owner_employee_ref = transfer.to_employee_ref
            if transfer.to_department_ref:
                contract.department_ref = transfer.to_department_ref
            contract.updated_at = now
        transfer.transfer_status = new_status
        transfer.updated_at = now
        return transfer

    # ========================================
    # 合同里程碑（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_milestone_details(self, contract_milestone_ref: str) -> LawContractMilestone:
        """
        根据 ref 获取合同里程碑详情。

        参数：
            contract_milestone_ref: 合同里程碑的唯一标识。

        返回：
            LawContractMilestone：合同里程碑对象。

        异常：
            ValueError：若未找到合同里程碑。
        """
        return self._get_contract_milestone(contract_milestone_ref)

    @is_tool(ToolType.READ)
    def list_contract_milestones(
        self,
        contract_ref: Optional[str] = None,
        milestone_type: Optional[str] = None,
        milestone_status: Optional[str] = None,
        responsible_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出合同里程碑（可选筛选）。

        参数：
            contract_ref: 按 contract ref 筛选。默认 None。
            milestone_type: 按 milestone type (payment, delivery, review, acceptance, other) 筛选。默认 None。
            milestone_status: 按 milestone status 筛选。默认 None。
            responsible_employee_ref: 按 responsible employee ref 筛选。默认 None。

        返回：
            str：匹配「contract milestones」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, m in self.db.law_contract_milestone.items():
            if contract_ref is not None and m.contract_ref != contract_ref:
                continue
            if milestone_type is not None and m.milestone_type != milestone_type:
                continue
            if milestone_status is not None and m.milestone_status != milestone_status:
                continue
            if responsible_employee_ref is not None and m.responsible_employee_ref != responsible_employee_ref:
                continue
            results.append({
                "contract_milestone_ref": m.contract_milestone_ref,
                "contract_ref": m.contract_ref,
                "milestone_title": m.milestone_title,
                "milestone_type": m.milestone_type,
                "due_date": m.due_date,
                "completed_date": m.completed_date,
                "amount": m.amount,
                "milestone_status": m.milestone_status,
                "responsible_employee_ref": m.responsible_employee_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_contract_milestone(
        self,
        contract_ref: str,
        milestone_title: str,
        milestone_type: str,
        due_date: str,
        amount: float,
        responsible_employee_ref: str,
        description: str = "",
    ) -> LawContractMilestone:
        """
        新建合同里程碑。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 引用：contract.
            milestone_title: 里程碑标题。
            milestone_type: 里程碑类型（payment、delivery、review、acceptance、other）。
            due_date: 里程碑截止日期（ISO 8601 日期）。
            amount: 里程碑金额。
            responsible_employee_ref: 责任人员工 ref。
            description: Description of the milestone。默认 ""

        返回：
            LawContractMilestone：新建的里程碑对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_contract(contract_ref)
        self._get_employee(responsible_employee_ref)
        valid_types = {"payment", "delivery", "review", "acceptance", "other"}
        if milestone_type not in valid_types:
            raise ValueError(f"Invalid milestone_type: {milestone_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("CMILE", self.db.law_contract_milestone)

        milestone = LawContractMilestone(
            contract_milestone_ref=ref,
            contract_ref=contract_ref,
            milestone_title=milestone_title,
            milestone_type=milestone_type,
            due_date=due_date,
            completed_date=None,
            amount=amount,
            milestone_status="pending",
            responsible_employee_ref=responsible_employee_ref,
            description=description,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract_milestone[ref] = milestone
        return milestone

    @is_tool(ToolType.WRITE)
    def update_contract_milestone_status(
        self,
        contract_milestone_ref: str,
        new_status: str,
    ) -> LawContractMilestone:
        """
        更新合同里程碑状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_milestone_ref: 合同里程碑的唯一标识。
            new_status: 新状态（pending、in_progress、completed、overdue、cancelled）。

        返回：
            LawContractMilestone：更新后的里程碑对象。

        异常：
            ValueError：若未找到里程碑或状态无效。
        """
        milestone = self._get_contract_milestone(contract_milestone_ref)
        valid_statuses = {"pending", "in_progress", "completed", "overdue", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "completed" and milestone.completed_date is None:
            milestone.completed_date = now
        milestone.milestone_status = new_status
        milestone.updated_at = now
        return milestone

    # ========================================
    # 合同风险（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_risk_details(self, contract_risk_ref: str) -> LawContractRisk:
        """
        根据 ref 获取合同风险详情。

        参数：
            contract_risk_ref: 合同风险的唯一标识。

        返回：
            LawContractRisk：合同风险对象。

        异常：
            ValueError：若未找到合同风险。
        """
        return self._get_contract_risk(contract_risk_ref)

    @is_tool(ToolType.READ)
    def list_contract_risks(
        self,
        contract_ref: Optional[str] = None,
        risk_category: Optional[str] = None,
        risk_level: Optional[str] = None,
        risk_status: Optional[str] = None,
    ) -> str:
        """
        列出合同风险（可选筛选）。

        参数：
            contract_ref: 按 contract ref 筛选。默认 None。
            risk_category: 按 risk category (legal, financial, operational, compliance, reputational) 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            risk_status: 按 risk status 筛选。默认 None。

        返回：
            str：匹配「contract risks」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_contract_risk.items():
            if contract_ref is not None and r.contract_ref != contract_ref:
                continue
            if risk_category is not None and r.risk_category != risk_category:
                continue
            if risk_level is not None and r.risk_level != risk_level:
                continue
            if risk_status is not None and r.risk_status != risk_status:
                continue
            results.append({
                "contract_risk_ref": r.contract_risk_ref,
                "contract_ref": r.contract_ref,
                "risk_title": r.risk_title,
                "risk_category": r.risk_category,
                "risk_level": r.risk_level,
                "risk_status": r.risk_status,
                "identified_by_ref": r.identified_by_ref,
                "identified_at": r.identified_at,
                "affected_clause": r.affected_clause,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_contract_risk(
        self,
        contract_ref: str,
        risk_title: str,
        risk_category: str,
        risk_level: str,
        risk_description: str,
        affected_clause: str,
        mitigation_plan: str,
        identified_by_ref: str,
    ) -> LawContractRisk:
        """
        新建合同风险记录。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 引用：contract.
            risk_title: 风险标题。
            risk_category: 类别（legal、financial、operational、compliance、reputational）。
            risk_level: 级别（low、medium、high、critical）。
            risk_description: 风险详细描述。
            affected_clause: 受影响的合同条款。
            mitigation_plan: 风险缓释方案。
            identified_by_ref: 识别风险的员工 ref。

        返回：
            LawContractRisk：新建的合同风险对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_contract(contract_ref)
        self._get_employee(identified_by_ref)
        valid_categories = {"legal", "financial", "operational", "compliance", "reputational"}
        if risk_category not in valid_categories:
            raise ValueError(f"Invalid risk_category: {risk_category}")
        valid_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")

        now = self._now_iso()
        ref = self._generate_ref("CRISK", self.db.law_contract_risk)

        risk = LawContractRisk(
            contract_risk_ref=ref,
            contract_ref=contract_ref,
            risk_title=risk_title,
            risk_category=risk_category,
            risk_level=risk_level,
            risk_description=risk_description,
            affected_clause=affected_clause,
            mitigation_plan=mitigation_plan,
            risk_status="open",
            identified_by_ref=identified_by_ref,
            identified_at=now,
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract_risk[ref] = risk
        return risk

    @is_tool(ToolType.WRITE)
    def update_contract_risk_status(
        self,
        contract_risk_ref: str,
        new_status: str,
    ) -> LawContractRisk:
        """
        更新合同风险状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_risk_ref: 合同风险的唯一标识。
            new_status: 新状态（open、mitigating、resolved、accepted、closed）。

        返回：
            LawContractRisk：更新后的合同风险对象。

        异常：
            ValueError：若未找到风险或状态无效。
        """
        risk = self._get_contract_risk(contract_risk_ref)
        valid_statuses = {"open", "mitigating", "resolved", "accepted", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "resolved" and risk.resolved_at is None:
            risk.resolved_at = now
        risk.risk_status = new_status
        risk.updated_at = now
        return risk

    # ========================================
    # 合同外借（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_contract_loan_details(self, contract_loan_ref: str) -> LawContractLoan:
        """
        根据 ref 获取合同外借详情。

        参数：
            contract_loan_ref: 合同外借的唯一标识。

        返回：
            LawContractLoan：合同外借对象。

        异常：
            ValueError：若未找到合同外借记录。
        """
        return self._get_contract_loan(contract_loan_ref)

    @is_tool(ToolType.READ)
    def list_contract_loans(
        self,
        contract_ref: Optional[str] = None,
        borrower_employee_ref: Optional[str] = None,
        loan_status: Optional[str] = None,
    ) -> str:
        """
        列出合同外借（可选筛选）。

        参数：
            contract_ref: 按 contract ref 筛选。默认 None。
            borrower_employee_ref: 按 borrower employee ref 筛选。默认 None。
            loan_status: 按 loan status 筛选。默认 None。

        返回：
            str：匹配「contract loans」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, l in self.db.law_contract_loan.items():
            if contract_ref is not None and l.contract_ref != contract_ref:
                continue
            if borrower_employee_ref is not None and l.borrower_employee_ref != borrower_employee_ref:
                continue
            if loan_status is not None and l.loan_status != loan_status:
                continue
            results.append({
                "contract_loan_ref": l.contract_loan_ref,
                "contract_ref": l.contract_ref,
                "borrower_employee_ref": l.borrower_employee_ref,
                "loan_purpose": l.loan_purpose,
                "loan_status": l.loan_status,
                "approved_by_ref": l.approved_by_ref,
                "borrowed_at": l.borrowed_at,
                "due_return_at": l.due_return_at,
                "returned_at": l.returned_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_contract_loan(
        self,
        contract_ref: str,
        borrower_employee_ref: str,
        loan_purpose: str,
    ) -> LawContractLoan:
        """
        新建合同外借申请。调用前 Agent 须向用户明确确认。

        参数：
            contract_ref: 引用：contract being borrowed.
            borrower_employee_ref: 借用人员工的 ref。
            loan_purpose: 外借合同文本用途。

        返回：
            LawContractLoan：新建的外借对象。

        异常：
            ValueError：若引用无效。
        """
        self._get_contract(contract_ref)
        self._get_employee(borrower_employee_ref)

        now = self._now_iso()
        ref = self._generate_ref("CLOAN", self.db.law_contract_loan)

        loan = LawContractLoan(
            contract_loan_ref=ref,
            contract_ref=contract_ref,
            borrower_employee_ref=borrower_employee_ref,
            loan_purpose=loan_purpose,
            loan_status="pending",
            approved_by_ref=None,
            borrowed_at=None,
            due_return_at=None,
            returned_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_contract_loan[ref] = loan
        return loan

    @is_tool(ToolType.WRITE)
    def update_contract_loan_status(
        self,
        contract_loan_ref: str,
        new_status: str,
        approved_by_ref: Optional[str] = None,
        due_return_at: Optional[str] = None,
    ) -> LawContractLoan:
        """
        更新合同外借状态。调用前 Agent 须向用户明确确认。

        参数：
            contract_loan_ref: 合同外借的唯一标识。
            new_status: 新状态（pending、approved、borrowed、returned、overdue、rejected）。
            approved_by_ref: Employee ref of the approver (required when approving)。默认 None。
            due_return_at: Due return date (required when approving)。默认 None。

        返回：
            LawContractLoan：更新后的外借对象。

        异常：
            ValueError：若未找到外借或状态无效。
        """
        loan = self._get_contract_loan(contract_loan_ref)
        valid_statuses = {"pending", "approved", "borrowed", "returned", "overdue", "rejected"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if new_status == "approved":
            if approved_by_ref:
                self._get_employee(approved_by_ref)
                loan.approved_by_ref = approved_by_ref
            if due_return_at:
                loan.due_return_at = due_return_at
        elif new_status == "borrowed":
            loan.borrowed_at = now
        elif new_status == "returned":
            loan.returned_at = now

        loan.loan_status = new_status
        loan.updated_at = now
        return loan

    # ========================================
    # 审批流与审批步骤（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_approval_flow_details(self, approval_flow_ref: str) -> LawApprovalFlow:
        """
        根据 ref 获取审批流详情。

        参数：
            approval_flow_ref: 审批流的唯一标识。

        返回：
            LawApprovalFlow：审批流对象。

        异常：
            ValueError：若未找到审批流。
        """
        return self._get_approval_flow(approval_flow_ref)

    @is_tool(ToolType.READ)
    def list_approval_flows(
        self,
        subject_type: Optional[str] = None,
        subject_ref: Optional[str] = None,
        flow_status: Optional[str] = None,
        initiated_by_ref: Optional[str] = None,
    ) -> str:
        """
        列出审批流（可选筛选）。

        参数：
            subject_type: 按 subject type 筛选。默认 None。
            subject_ref: 按 subject ref 筛选。默认 None。
            flow_status: 按 flow status 筛选。默认 None。
            initiated_by_ref: 按 initiator employee ref 筛选。默认 None。

        返回：
            str：匹配「approval flows」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, f in self.db.law_approval_flow.items():
            if subject_type is not None and f.subject_type != subject_type:
                continue
            if subject_ref is not None and f.subject_ref != subject_ref:
                continue
            if flow_status is not None and f.flow_status != flow_status:
                continue
            if initiated_by_ref is not None and f.initiated_by_ref != initiated_by_ref:
                continue
            results.append({
                "approval_flow_ref": f.approval_flow_ref,
                "subject_type": f.subject_type,
                "subject_ref": f.subject_ref,
                "flow_title": f.flow_title,
                "flow_type": f.flow_type,
                "flow_status": f.flow_status,
                "initiated_by_ref": f.initiated_by_ref,
                "current_step": f.current_step,
                "total_steps": f.total_steps,
                "initiated_at": f.initiated_at,
                "completed_at": f.completed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_approval_step_details(self, approval_step_ref: str) -> LawApprovalStep:
        """
        根据 ref 获取审批步骤详情。

        参数：
            approval_step_ref: 审批步骤的唯一标识。

        返回：
            LawApprovalStep：审批步骤对象。

        异常：
            ValueError：若未找到审批步骤。
        """
        return self._get_approval_step(approval_step_ref)

    @is_tool(ToolType.READ)
    def list_approval_steps(self, approval_flow_ref: str) -> str:
        """
        列出审批流内全部步骤（按 step_order 排序）。

        参数：
            approval_flow_ref: 审批流的唯一标识。

        返回：
            str：approval steps in order 的 JSON 数组。

        异常：
            ValueError：若未找到审批流。
        """
        self._get_approval_flow(approval_flow_ref)
        steps = []
        for ref, s in self.db.law_approval_step.items():
            if s.approval_flow_ref == approval_flow_ref:
                steps.append(s)
        steps.sort(key=lambda x: x.step_order)
        results = []
        for s in steps:
            results.append({
                "approval_step_ref": s.approval_step_ref,
                "approval_flow_ref": s.approval_flow_ref,
                "step_order": s.step_order,
                "step_name": s.step_name,
                "approver_employee_ref": s.approver_employee_ref,
                "step_status": s.step_status,
                "decision": s.decision,
                "comments": s.comments,
                "decided_at": s.decided_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_pending_approvals_for_employee(self, employee_ref: str) -> str:
        """
        列出某员工待处理的审批步骤。

        参数：
            employee_ref: 审批人的员工 ref。

        返回：
            str：pending approval steps 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, s in self.db.law_approval_step.items():
            if s.approver_employee_ref == employee_ref and s.step_status == "pending":
                flow = self._get_approval_flow(s.approval_flow_ref)
                results.append({
                    "approval_step_ref": s.approval_step_ref,
                    "approval_flow_ref": s.approval_flow_ref,
                    "flow_title": flow.flow_title,
                    "subject_type": flow.subject_type,
                    "subject_ref": flow.subject_ref,
                    "step_order": s.step_order,
                    "step_name": s.step_name,
                    "step_status": s.step_status,
                })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_approval_flow(
        self,
        subject_type: str,
        subject_ref: str,
        flow_title: str,
        flow_type: str,
        initiated_by_ref: str,
        total_steps: int,
    ) -> LawApprovalFlow:
        """
        新建审批流。调用前 Agent 须向用户明确确认。

        参数：
            subject_type: 标的类型（contract、amendment、seal_usage、ip_application、license_usage、entity_change、other）。
            subject_ref: 引用：subject.
            flow_title: 审批流标题。
            flow_type: 审批流类型（contract_approval、amendment_approval、seal_approval、ip_approval、license_approval、entity_change_approval、general）。
            initiated_by_ref: 发起人员工 ref。
            total_steps: 步骤总数。

        返回：
            LawApprovalFlow：新建的审批流对象。

        异常：
            ValueError：若入参无效。
        """
        self._get_employee(initiated_by_ref)
        valid_subject_types = {"contract", "amendment", "seal_usage", "ip_application", "license_usage", "entity_change", "other"}
        if subject_type not in valid_subject_types:
            raise ValueError(f"Invalid subject_type: {subject_type}")
        valid_flow_types = {"contract_approval", "amendment_approval", "seal_approval", "ip_approval", "license_approval", "entity_change_approval", "general"}
        if flow_type not in valid_flow_types:
            raise ValueError(f"Invalid flow_type: {flow_type}")
        if total_steps < 1:
            raise ValueError("total_steps must be at least 1")

        now = self._now_iso()
        ref = self._generate_ref("AFLOW", self.db.law_approval_flow)

        flow = LawApprovalFlow(
            approval_flow_ref=ref,
            subject_type=subject_type,
            subject_ref=subject_ref,
            flow_title=flow_title,
            flow_type=flow_type,
            flow_status="in_progress",
            initiated_by_ref=initiated_by_ref,
            current_step=1,
            total_steps=total_steps,
            initiated_at=now,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_approval_flow[ref] = flow
        return flow

    @is_tool(ToolType.WRITE)
    def create_approval_step(
        self,
        approval_flow_ref: str,
        step_order: int,
        step_name: str,
        approver_employee_ref: str,
    ) -> LawApprovalStep:
        """
        在审批流中新建步骤。调用前 Agent 须向用户明确确认。

        参数：
            approval_flow_ref: 引用：parent approval flow.
            step_order: 本步骤序号。
            step_name: 步骤名称。
            approver_employee_ref: 审批人的员工 ref。

        返回：
            LawApprovalStep：新建的审批步骤对象。

        异常：
            ValueError：若引用无效。
        """
        self._get_approval_flow(approval_flow_ref)
        self._get_employee(approver_employee_ref)

        now = self._now_iso()
        ref = self._generate_ref("ASTEP", self.db.law_approval_step)

        step = LawApprovalStep(
            approval_step_ref=ref,
            approval_flow_ref=approval_flow_ref,
            step_order=step_order,
            step_name=step_name,
            approver_employee_ref=approver_employee_ref,
            step_status="pending",
            decision=None,
            comments="",
            decided_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_approval_step[ref] = step
        return step

    @is_tool(ToolType.WRITE)
    def decide_approval_step(
        self,
        approval_step_ref: str,
        decision: str,
        comments: str = "",
    ) -> LawApprovalStep:
        """
        对审批步骤作出审批决定。调用前 Agent 须向用户明确确认。

        参数：
            approval_step_ref: 审批步骤的唯一标识。
            decision: 决定（approve、reject、abstain）。
            comments: Comments from the approver。默认 ""

        返回：
            LawApprovalStep：更新后的审批步骤对象。

        异常：
            ValueError：若未找到步骤、非待审或决定无效。
        """
        step = self._get_approval_step(approval_step_ref)
        if step.step_status != "pending":
            raise ValueError(f"Approval step is not pending, current status: {step.step_status}")
        valid_decisions = {"approve", "reject", "abstain"}
        if decision not in valid_decisions:
            raise ValueError(f"Invalid decision: {decision}. Must be one of {valid_decisions}")

        now = self._now_iso()
        step.decision = decision
        step.comments = comments
        step.decided_at = now
        step.step_status = "approved" if decision == "approve" else ("rejected" if decision == "reject" else "skipped")
        step.updated_at = now

        # 更新审批流
        flow = self._get_approval_flow(step.approval_flow_ref)
        if decision == "reject":
            flow.flow_status = "rejected"
            flow.completed_at = now
            flow.updated_at = now
        elif decision == "approve":
            # 检查是否所有步骤均已通过
            all_steps = [s for s in self.db.law_approval_step.values() if s.approval_flow_ref == flow.approval_flow_ref]
            all_steps.sort(key=lambda x: x.step_order)
            all_decided = all(s.step_status in ("approved", "skipped") for s in all_steps)
            if all_decided:
                flow.flow_status = "approved"
                flow.completed_at = now
            else:
                flow.current_step = step.step_order + 1
            flow.updated_at = now

        return step

    @is_tool(ToolType.WRITE)
    def cancel_approval_flow(self, approval_flow_ref: str) -> LawApprovalFlow:
        """
        取消进行中的审批流。调用前 Agent 须向用户明确确认。

        参数：
            approval_flow_ref: 审批流的唯一标识。

        返回：
            LawApprovalFlow：更新后的审批流对象。

        异常：
            ValueError：若未找到审批流或不在进行中。
        """
        flow = self._get_approval_flow(approval_flow_ref)
        if flow.flow_status != "in_progress":
            raise ValueError(f"Approval flow cannot be cancelled from status '{flow.flow_status}'")
        now = self._now_iso()
        flow.flow_status = "cancelled"
        flow.completed_at = now
        flow.updated_at = now
        return flow

    # ========================================
    # 印章与用印申请（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_seal_details(self, seal_ref: str) -> LawSeal:
        """
        根据 ref 获取印章详情。

        参数：
            seal_ref: 印章的唯一标识。

        返回：
            LawSeal：印章对象。

        异常：
            ValueError：若未找到印章。
        """
        return self._get_seal(seal_ref)

    @is_tool(ToolType.READ)
    def list_seals(
        self,
        seal_type: Optional[str] = None,
        seal_status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出印章（可选筛选）。

        参数：
            seal_type: 按 seal type (corporate, contract, finance, legal, hr, custom) 筛选。默认 None。
            seal_status: 按 seal status (active, inactive, destroyed) 筛选。默认 None。
            department_ref: 按 department ref 筛选。默认 None。

        返回：
            str：匹配「seals」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, s in self.db.law_seal.items():
            if seal_type is not None and s.seal_type != seal_type:
                continue
            if seal_status is not None and s.seal_status != seal_status:
                continue
            if department_ref is not None and s.department_ref != department_ref:
                continue
            results.append({
                "seal_ref": s.seal_ref,
                "seal_name": s.seal_name,
                "seal_type": s.seal_type,
                "seal_code": s.seal_code,
                "custodian_employee_ref": s.custodian_employee_ref,
                "department_ref": s.department_ref,
                "seal_status": s.seal_status,
                "description": s.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_seal_ref_by_name(self, seal_name: str) -> str:
        """
        按名称模糊查找印章 ref（不区分大小写）。

        参数：
            seal_name: 印章名称（可部分匹配）。

        返回：
            str：匹配到的seal 的 seal_ref。

        异常：
            ValueError：若未匹配到印章。
        """
        search = seal_name.lower()
        for ref, s in self.db.law_seal.items():
            if search in s.seal_name.lower():
                return ref
        raise ValueError("Seal not found")

    @is_tool(ToolType.READ)
    def get_seal_usage_request_details(self, seal_usage_request_ref: str) -> LawSealUsageRequest:
        """
        根据 ref 获取用印申请详情。

        参数：
            seal_usage_request_ref: 用印申请的唯一标识。

        返回：
            LawSealUsageRequest：用印申请对象。

        异常：
            ValueError：若未找到用印申请。
        """
        return self._get_seal_usage_request(seal_usage_request_ref)

    @is_tool(ToolType.READ)
    def list_seal_usage_requests(
        self,
        seal_ref: Optional[str] = None,
        applicant_employee_ref: Optional[str] = None,
        usage_type: Optional[str] = None,
        request_status: Optional[str] = None,
    ) -> str:
        """
        列出用印申请（可选筛选）。

        参数：
            seal_ref: 按 seal ref 筛选。默认 None。
            applicant_employee_ref: 按 applicant employee ref 筛选。默认 None。
            usage_type: 按 usage type (contract, certificate, letter, report, other) 筛选。默认 None。
            request_status: 按 request status 筛选。默认 None。

        返回：
            str：匹配「seal usage requests」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_seal_usage_request.items():
            if seal_ref is not None and r.seal_ref != seal_ref:
                continue
            if applicant_employee_ref is not None and r.applicant_employee_ref != applicant_employee_ref:
                continue
            if usage_type is not None and r.usage_type != usage_type:
                continue
            if request_status is not None and r.request_status != request_status:
                continue
            results.append({
                "seal_usage_request_ref": r.seal_usage_request_ref,
                "seal_ref": r.seal_ref,
                "applicant_employee_ref": r.applicant_employee_ref,
                "usage_type": r.usage_type,
                "document_title": r.document_title,
                "usage_purpose": r.usage_purpose,
                "copies_count": r.copies_count,
                "request_status": r.request_status,
                "used_at": r.used_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_seal_usage_request(
        self,
        seal_ref: str,
        applicant_employee_ref: str,
        usage_type: str,
        related_resource_type: str,
        related_resource_ref: str,
        document_title: str,
        usage_purpose: str,
        copies_count: int = 1,
    ) -> LawSealUsageRequest:
        """
        新建用印申请。调用前 Agent 须向用户明确确认。

        参数：
            seal_ref: 引用：seal.
            applicant_employee_ref: 申请人的员工 ref。
            usage_type: 使用类型（contract、certificate、letter、report、other）。
            related_resource_type: 关联资源类型。
            related_resource_ref: 引用：related resource.
            document_title: 待盖章文件标题。
            usage_purpose: 用印目的。
            copies_count: Number of copies to be stamped。默认 1。

        返回：
            LawSealUsageRequest：新建的用印申请对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_seal(seal_ref)
        self._get_employee(applicant_employee_ref)
        valid_usage_types = {"contract", "certificate", "letter", "report", "other"}
        if usage_type not in valid_usage_types:
            raise ValueError(f"Invalid usage_type: {usage_type}. Must be one of {valid_usage_types}")

        now = self._now_iso()
        ref = self._generate_ref("SUREQ", self.db.law_seal_usage_request)

        request = LawSealUsageRequest(
            seal_usage_request_ref=ref,
            seal_ref=seal_ref,
            applicant_employee_ref=applicant_employee_ref,
            usage_type=usage_type,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            document_title=document_title,
            usage_purpose=usage_purpose,
            copies_count=copies_count,
            request_status="pending",
            used_at=None,
            document_file_ref=None,
            stamped_file_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_seal_usage_request[ref] = request
        return request

    @is_tool(ToolType.WRITE)
    def update_seal_usage_request_status(
        self,
        seal_usage_request_ref: str,
        new_status: str,
    ) -> LawSealUsageRequest:
        """
        更新用印申请状态。调用前 Agent 须向用户明确确认。

        参数：
            seal_usage_request_ref: 用印申请的唯一标识。
            new_status: 新状态（pending、approved、rejected、used、cancelled）。

        返回：
            LawSealUsageRequest：更新后的用印申请对象。

        异常：
            ValueError：若未找到申请或状态无效。
        """
        request = self._get_seal_usage_request(seal_usage_request_ref)
        valid_statuses = {"pending", "approved", "rejected", "used", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "used":
            request.used_at = now
        request.request_status = new_status
        request.updated_at = now
        return request

    # ========================================
    # 知识产权资产（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_ip_asset_details(self, ip_asset_ref: str) -> LawIPAsset:
        """
        根据 ref 获取知识产权资产详情。

        参数：
            ip_asset_ref: 知识产权资产的唯一标识。

        返回：
            LawIPAsset：知识产权资产对象。

        异常：
            ValueError：若未找到知识产权资产。
        """
        return self._get_ip_asset(ip_asset_ref)

    @is_tool(ToolType.READ)
    def search_ip_assets(
        self,
        ip_type: Optional[str] = None,
        ip_status: Optional[str] = None,
        owner_type: Optional[str] = None,
        department_ref: Optional[str] = None,
        responsible_employee_ref: Optional[str] = None,
        name_keyword: Optional[str] = None,
    ) -> str:
        """
        搜索知识产权资产（可选筛选）。

        参数：
            ip_type: 按 IP type (patent, trademark, copyright, trade_secret, domain, other) 筛选。默认 None。
            ip_status: 按 IP status 筛选。默认 None。
            owner_type: 按 owner type (company, employee, joint) 筛选。默认 None。
            department_ref: 按 department ref 筛选。默认 None。
            responsible_employee_ref: 按 responsible employee ref 筛选。默认 None。
            name_keyword: 按 keyword in IP name (case-insensitive) 筛选。默认 None。

        返回：
            str：匹配「IP assets」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ip in self.db.law_ip_asset.items():
            if ip_type is not None and ip.ip_type != ip_type:
                continue
            if ip_status is not None and ip.ip_status != ip_status:
                continue
            if owner_type is not None and ip.owner_type != owner_type:
                continue
            if department_ref is not None and ip.department_ref != department_ref:
                continue
            if responsible_employee_ref is not None and ip.responsible_employee_ref != responsible_employee_ref:
                continue
            if name_keyword is not None and name_keyword.lower() not in ip.ip_name.lower():
                continue
            results.append({
                "ip_asset_ref": ip.ip_asset_ref,
                "ip_type": ip.ip_type,
                "ip_name": ip.ip_name,
                "ip_number": ip.ip_number,
                "registration_number": ip.registration_number,
                "ip_status": ip.ip_status,
                "owner_type": ip.owner_type,
                "responsible_employee_ref": ip.responsible_employee_ref,
                "department_ref": ip.department_ref,
                "application_date": ip.application_date,
                "grant_date": ip.grant_date,
                "expiry_date": ip.expiry_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_ip_asset_status(
        self,
        ip_asset_ref: str,
        new_status: str,
    ) -> LawIPAsset:
        """
        更新知识产权资产状态。调用前 Agent 须向用户明确确认。

        参数：
            ip_asset_ref: 知识产权资产的唯一标识。
            new_status: 新状态（active、pending、expired、abandoned、transferred）。

        返回：
            LawIPAsset：更新后的知识产权资产对象。

        异常：
            ValueError：若未找到知识产权资产或状态无效。
        """
        ip = self._get_ip_asset(ip_asset_ref)
        valid_statuses = {"active", "pending", "expired", "abandoned", "transferred"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        ip.ip_status = new_status
        ip.updated_at = self._now_iso()
        return ip

    # ========================================
    # 知识产权发明人（只读）
    # ========================================

    @is_tool(ToolType.READ)
    def list_ip_inventors(self, ip_asset_ref: str) -> str:
        """
        列出某知识产权资产的全部发明人。

        参数：
            ip_asset_ref: 知识产权资产的唯一标识。

        返回：
            str：IP inventors 的 JSON 数组。

        异常：
            ValueError：若未找到知识产权资产。
        """
        self._get_ip_asset(ip_asset_ref)
        results = []
        for ref, inv in self.db.law_ip_inventor.items():
            if inv.ip_asset_ref == ip_asset_ref:
                emp = self._get_employee(inv.employee_ref)
                up = self._get_user_profile(emp.user_profile_ref)
                results.append({
                    "ip_inventor_ref": inv.ip_inventor_ref,
                    "ip_asset_ref": inv.ip_asset_ref,
                    "employee_ref": inv.employee_ref,
                    "display_name": up.display_name,
                    "inventor_role": inv.inventor_role,
                    "contribution_ratio": inv.contribution_ratio,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_ip_assets_by_inventor(self, employee_ref: str) -> str:
        """
        列出某员工作为发明人的知识产权资产。

        参数：
            employee_ref: 发明人的员工 ref。

        返回：
            str：IP assets with inventor details 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, inv in self.db.law_ip_inventor.items():
            if inv.employee_ref == employee_ref:
                ip = self._get_ip_asset(inv.ip_asset_ref)
                results.append({
                    "ip_asset_ref": ip.ip_asset_ref,
                    "ip_type": ip.ip_type,
                    "ip_name": ip.ip_name,
                    "ip_status": ip.ip_status,
                    "inventor_role": inv.inventor_role,
                    "contribution_ratio": inv.contribution_ratio,
                })
        return json.dumps(results)

    # ========================================
    # 知识产权申请（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_ip_application_details(self, ip_application_ref: str) -> LawIPApplication:
        """
        根据 ref 获取知识产权申请详情。

        参数：
            ip_application_ref: 知识产权申请的唯一标识。

        返回：
            LawIPApplication：知识产权申请对象。

        异常：
            ValueError：若未找到知识产权申请。
        """
        return self._get_ip_application(ip_application_ref)

    @is_tool(ToolType.READ)
    def list_ip_applications(
        self,
        ip_asset_ref: Optional[str] = None,
        application_type: Optional[str] = None,
        application_status: Optional[str] = None,
        applicant_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出知识产权申请（可选筛选）。

        参数：
            ip_asset_ref: 按 IP asset ref 筛选。默认 None。
            application_type: 按 application type 筛选。默认 None。
            application_status: 按 application status 筛选。默认 None。
            applicant_employee_ref: 按 applicant employee ref 筛选。默认 None。

        返回：
            str：匹配「IP applications」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, a in self.db.law_ip_application.items():
            if ip_asset_ref is not None and a.ip_asset_ref != ip_asset_ref:
                continue
            if application_type is not None and a.application_type != application_type:
                continue
            if application_status is not None and a.application_status != application_status:
                continue
            if applicant_employee_ref is not None and a.applicant_employee_ref != applicant_employee_ref:
                continue
            results.append({
                "ip_application_ref": a.ip_application_ref,
                "ip_asset_ref": a.ip_asset_ref,
                "application_type": a.application_type,
                "applicant_employee_ref": a.applicant_employee_ref,
                "agency_name": a.agency_name,
                "application_status": a.application_status,
                "submitted_at": a.submitted_at,
                "estimated_cost": a.estimated_cost,
                "actual_cost": a.actual_cost,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_ip_application(
        self,
        ip_asset_ref: str,
        application_type: str,
        applicant_employee_ref: str,
        agency_name: str,
        estimated_cost: float,
        notes: str = "",
    ) -> LawIPApplication:
        """
        新建知识产权申请。调用前 Agent 须向用户明确确认。

        参数：
            ip_asset_ref: 引用：IP asset.
            application_type: 申请类型（new_registration、renewal、change、transfer、opposition）。
            applicant_employee_ref: 申请人的员工 ref。
            agency_name: 知识产权代理机构名称。
            estimated_cost: 预估费用。
            notes: Additional notes。默认 ""

        返回：
            LawIPApplication：新建的知识产权申请对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_ip_asset(ip_asset_ref)
        self._get_employee(applicant_employee_ref)
        valid_types = {"new_registration", "renewal", "change", "transfer", "opposition"}
        if application_type not in valid_types:
            raise ValueError(f"Invalid application_type: {application_type}")

        now = self._now_iso()
        ref = self._generate_ref("IPAPP", self.db.law_ip_application)

        application = LawIPApplication(
            ip_application_ref=ref,
            ip_asset_ref=ip_asset_ref,
            application_type=application_type,
            applicant_employee_ref=applicant_employee_ref,
            agency_name=agency_name,
            application_status="drafting",
            submitted_at=None,
            accepted_at=None,
            granted_at=None,
            rejected_at=None,
            rejection_reason=None,
            application_file_ref=None,
            estimated_cost=estimated_cost,
            actual_cost=0.0,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.law_ip_application[ref] = application
        return application

    @is_tool(ToolType.WRITE)
    def update_ip_application_status(
        self,
        ip_application_ref: str,
        new_status: str,
        rejection_reason: Optional[str] = None,
    ) -> LawIPApplication:
        """
        更新知识产权申请状态。调用前 Agent 须向用户明确确认。

        参数：
            ip_application_ref: 知识产权申请的唯一标识。
            new_status: 新状态（drafting、internal_review、submitted、under_examination、accepted、granted、rejected、withdrawn）。
            rejection_reason: Reason for rejection (required when new_status is 'rejected')。默认 None。

        返回：
            LawIPApplication：更新后的知识产权申请对象。

        异常：
            ValueError：若未找到申请或状态无效。
        """
        application = self._get_ip_application(ip_application_ref)
        valid_statuses = {"drafting", "internal_review", "submitted", "under_examination", "accepted", "granted", "rejected", "withdrawn"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if new_status == "submitted" and application.submitted_at is None:
            application.submitted_at = now
        elif new_status == "accepted" and application.accepted_at is None:
            application.accepted_at = now
        elif new_status == "granted" and application.granted_at is None:
            application.granted_at = now
        elif new_status == "rejected":
            application.rejected_at = now
            if rejection_reason:
                application.rejection_reason = rejection_reason

        application.application_status = new_status
        application.updated_at = now
        return application

    # ========================================
    # 知识产权授权（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_ip_authorization_details(self, ip_authorization_ref: str) -> LawIPAuthorization:
        """
        根据 ref 获取知识产权授权详情。

        参数：
            ip_authorization_ref: 知识产权授权的唯一标识。

        返回：
            LawIPAuthorization：知识产权授权对象。

        异常：
            ValueError：若未找到知识产权授权。
        """
        return self._get_ip_authorization(ip_authorization_ref)

    @is_tool(ToolType.READ)
    def list_ip_authorizations(
        self,
        ip_asset_ref: Optional[str] = None,
        authorization_type: Optional[str] = None,
        authorization_status: Optional[str] = None,
    ) -> str:
        """
        列出知识产权授权（可选筛选）。

        参数：
            ip_asset_ref: 按 IP asset ref 筛选。默认 None。
            authorization_type: 按 authorization type (license, assignment, pledge, cross_license) 筛选。默认 None。
            authorization_status: 按 authorization status 筛选。默认 None。

        返回：
            str：匹配「IP authorizations」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, a in self.db.law_ip_authorization.items():
            if ip_asset_ref is not None and a.ip_asset_ref != ip_asset_ref:
                continue
            if authorization_type is not None and a.authorization_type != authorization_type:
                continue
            if authorization_status is not None and a.authorization_status != authorization_status:
                continue
            results.append({
                "ip_authorization_ref": a.ip_authorization_ref,
                "ip_asset_ref": a.ip_asset_ref,
                "authorization_type": a.authorization_type,
                "licensee_name": a.licensee_name,
                "scope": a.scope,
                "territory": a.territory,
                "exclusive": a.exclusive,
                "effective_date": a.effective_date,
                "expiry_date": a.expiry_date,
                "fee": a.fee,
                "authorization_status": a.authorization_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_ip_authorization_status(
        self,
        ip_authorization_ref: str,
        new_status: str,
    ) -> LawIPAuthorization:
        """
        更新知识产权授权状态。调用前 Agent 须向用户明确确认。

        参数：
            ip_authorization_ref: 知识产权授权的唯一标识。
            new_status: 新状态（active、expired、terminated、pending）。

        返回：
            LawIPAuthorization：更新后的知识产权授权对象。

        异常：
            ValueError：若未找到授权或状态无效。
        """
        auth = self._get_ip_authorization(ip_authorization_ref)
        valid_statuses = {"active", "expired", "terminated", "pending"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        auth.authorization_status = new_status
        auth.updated_at = self._now_iso()
        return auth

    # ========================================
    # 知识产权奖励（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_ip_reward_details(self, ip_reward_ref: str) -> LawIPReward:
        """
        根据 ref 获取知识产权奖励详情。

        参数：
            ip_reward_ref: 知识产权奖励的唯一标识。

        返回：
            LawIPReward：知识产权奖励对象。

        异常：
            ValueError：若未找到知识产权奖励。
        """
        return self._get_ip_reward(ip_reward_ref)

    @is_tool(ToolType.READ)
    def list_ip_rewards(
        self,
        ip_asset_ref: Optional[str] = None,
        employee_ref: Optional[str] = None,
        reward_type: Optional[str] = None,
        reward_status: Optional[str] = None,
    ) -> str:
        """
        列出知识产权奖励（可选筛选）。

        参数：
            ip_asset_ref: 按 IP asset ref 筛选。默认 None。
            employee_ref: 按 employee ref 筛选。默认 None。
            reward_type: 按 reward type (application_bonus, grant_bonus, commercialization_bonus, annual_award) 筛选。默认 None。
            reward_status: 按 reward status 筛选。默认 None。

        返回：
            str：匹配「IP rewards」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_ip_reward.items():
            if ip_asset_ref is not None and r.ip_asset_ref != ip_asset_ref:
                continue
            if employee_ref is not None and r.employee_ref != employee_ref:
                continue
            if reward_type is not None and r.reward_type != reward_type:
                continue
            if reward_status is not None and r.reward_status != reward_status:
                continue
            results.append({
                "ip_reward_ref": r.ip_reward_ref,
                "ip_asset_ref": r.ip_asset_ref,
                "employee_ref": r.employee_ref,
                "reward_type": r.reward_type,
                "reward_amount": r.reward_amount,
                "reward_status": r.reward_status,
                "approved_by_ref": r.approved_by_ref,
                "paid_at": r.paid_at,
                "notes": r.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_ip_reward(
        self,
        ip_asset_ref: str,
        employee_ref: str,
        reward_type: str,
        reward_amount: float,
        notes: str = "",
    ) -> LawIPReward:
        """
        新建知识产权奖励申请。调用前 Agent 须向用户明确确认。

        参数：
            ip_asset_ref: 引用：IP asset.
            employee_ref: 引用：employee receiving the reward.
            reward_type: 奖励类型（application_bonus、grant_bonus、commercialization_bonus、annual_award）。
            reward_amount: 奖励金额。
            notes: Additional notes。默认 ""

        返回：
            LawIPReward：新建的知识产权奖励对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_ip_asset(ip_asset_ref)
        self._get_employee(employee_ref)
        valid_types = {"application_bonus", "grant_bonus", "commercialization_bonus", "annual_award"}
        if reward_type not in valid_types:
            raise ValueError(f"Invalid reward_type: {reward_type}")

        now = self._now_iso()
        ref = self._generate_ref("IPRWD", self.db.law_ip_reward)

        reward = LawIPReward(
            ip_reward_ref=ref,
            ip_asset_ref=ip_asset_ref,
            employee_ref=employee_ref,
            reward_type=reward_type,
            reward_amount=reward_amount,
            reward_status="pending",
            approved_by_ref=None,
            paid_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.law_ip_reward[ref] = reward
        return reward

    @is_tool(ToolType.WRITE)
    def update_ip_reward_status(
        self,
        ip_reward_ref: str,
        new_status: str,
        approved_by_ref: Optional[str] = None,
    ) -> LawIPReward:
        """
        更新知识产权奖励状态。调用前 Agent 须向用户明确确认。

        参数：
            ip_reward_ref: 知识产权奖励的唯一标识。
            new_status: 新状态（pending、approved、paid、rejected）。
            approved_by_ref: Employee ref of the approver (when approving)。默认 None。

        返回：
            LawIPReward：更新后的知识产权奖励对象。

        异常：
            ValueError：若未找到奖励或状态无效。
        """
        reward = self._get_ip_reward(ip_reward_ref)
        valid_statuses = {"pending", "approved", "paid", "rejected"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "approved" and approved_by_ref:
            self._get_employee(approved_by_ref)
            reward.approved_by_ref = approved_by_ref
        if new_status == "paid":
            reward.paid_at = now
        reward.reward_status = new_status
        reward.updated_at = now
        return reward

    # ========================================
    # 廉洁申报（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_integrity_declaration_details(self, integrity_declaration_ref: str) -> LawIntegrityDeclaration:
        """
        根据 ref 获取廉洁申报详情。

        参数：
            integrity_declaration_ref: 廉洁申报的唯一标识。

        返回：
            LawIntegrityDeclaration：廉洁申报对象。

        异常：
            ValueError：若未找到廉洁申报。
        """
        return self._get_integrity_declaration(integrity_declaration_ref)

    @is_tool(ToolType.READ)
    def list_integrity_declarations(
        self,
        employee_ref: Optional[str] = None,
        declaration_type: Optional[str] = None,
        declaration_status: Optional[str] = None,
        declaration_period: Optional[str] = None,
    ) -> str:
        """
        列出廉洁申报（可选筛选）。

        参数：
            employee_ref: 按 employee ref 筛选。默认 None。
            declaration_type: 按 declaration type (commitment, conflict_of_interest, gift_disclosure, annual_review) 筛选。默认 None。
            declaration_status: 按 declaration status 筛选。默认 None。
            declaration_period: 按 declaration period 筛选。默认 None。

        返回：
            str：匹配「integrity declarations」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, d in self.db.law_integrity_declaration.items():
            if employee_ref is not None and d.employee_ref != employee_ref:
                continue
            if declaration_type is not None and d.declaration_type != declaration_type:
                continue
            if declaration_status is not None and d.declaration_status != declaration_status:
                continue
            if declaration_period is not None and d.declaration_period != declaration_period:
                continue
            results.append({
                "integrity_declaration_ref": d.integrity_declaration_ref,
                "employee_ref": d.employee_ref,
                "declaration_type": d.declaration_type,
                "declaration_period": d.declaration_period,
                "declaration_status": d.declaration_status,
                "submitted_at": d.submitted_at,
                "reviewed_by_ref": d.reviewed_by_ref,
                "review_result": d.review_result,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_integrity_declaration(
        self,
        employee_ref: str,
        declaration_type: str,
        declaration_period: str,
        declaration_content: dict,
    ) -> LawIntegrityDeclaration:
        """
        新建草稿状态廉洁申报。调用前 Agent 须向用户明确确认。

        参数：
            employee_ref: 引用：employee making the declaration.
            declaration_type: 申报类型（commitment、conflict_of_interest、gift_disclosure、annual_review）。
            declaration_period: 覆盖周期（如 2025、2025-Q1）。
            declaration_content: 申报结构化内容。

        返回：
            LawIntegrityDeclaration：新建的申报对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(employee_ref)
        valid_types = {"commitment", "conflict_of_interest", "gift_disclosure", "annual_review"}
        if declaration_type not in valid_types:
            raise ValueError(f"Invalid declaration_type: {declaration_type}")

        now = self._now_iso()
        ref = self._generate_ref("INTDEC", self.db.law_integrity_declaration)

        declaration = LawIntegrityDeclaration(
            integrity_declaration_ref=ref,
            employee_ref=employee_ref,
            declaration_type=declaration_type,
            declaration_period=declaration_period,
            declaration_content=declaration_content,
            declaration_status="draft",
            submitted_at=None,
            reviewed_by_ref=None,
            reviewed_at=None,
            review_result=None,
            review_comments="",
            declaration_file_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_integrity_declaration[ref] = declaration
        return declaration

    @is_tool(ToolType.WRITE)
    def submit_integrity_declaration(self, integrity_declaration_ref: str) -> LawIntegrityDeclaration:
        """
        提交廉洁申报进入审核。调用前 Agent 须向用户明确确认。

        参数：
            integrity_declaration_ref: 廉洁申报的唯一标识。

        返回：
            LawIntegrityDeclaration：更新后的申报对象。

        异常：
            ValueError：若申报非草稿状态。
        """
        declaration = self._get_integrity_declaration(integrity_declaration_ref)
        if declaration.declaration_status != "draft":
            raise ValueError(f"Declaration must be in 'draft' status to submit, current: {declaration.declaration_status}")
        now = self._now_iso()
        declaration.declaration_status = "submitted"
        declaration.submitted_at = now
        declaration.updated_at = now
        return declaration

    @is_tool(ToolType.WRITE)
    def review_integrity_declaration(
        self,
        integrity_declaration_ref: str,
        reviewed_by_ref: str,
        review_result: str,
        review_comments: str = "",
    ) -> LawIntegrityDeclaration:
        """
        审核廉洁申报。调用前 Agent 须向用户明确确认。

        参数：
            integrity_declaration_ref: 廉洁申报的唯一标识。
            reviewed_by_ref: 审核人员工 ref。
            review_result: 审查结果（pass、fail、conditional_pass）。
            review_comments: Comments from the reviewer。默认 ""

        返回：
            LawIntegrityDeclaration：更新后的申报对象。

        异常：
            ValueError：若申报非已提交/审核中或入参无效。
        """
        declaration = self._get_integrity_declaration(integrity_declaration_ref)
        if declaration.declaration_status not in ("submitted", "under_review"):
            raise ValueError(f"Declaration must be in 'submitted' or 'under_review' status to review, current: {declaration.declaration_status}")
        self._get_employee(reviewed_by_ref)
        valid_results = {"pass", "fail", "conditional_pass"}
        if review_result not in valid_results:
            raise ValueError(f"Invalid review_result: {review_result}. Must be one of {valid_results}")

        now = self._now_iso()
        declaration.reviewed_by_ref = reviewed_by_ref
        declaration.reviewed_at = now
        declaration.review_result = review_result
        declaration.review_comments = review_comments
        declaration.declaration_status = "approved" if review_result == "pass" else ("rejected" if review_result == "fail" else "approved")
        declaration.updated_at = now
        return declaration

    # ========================================
    # 违规举报（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_violation_report_details(self, violation_report_ref: str) -> LawViolationReport:
        """
        根据 ref 获取违规举报详情。

        参数：
            violation_report_ref: 违规举报的唯一标识。

        返回：
            LawViolationReport：违规举报对象。

        异常：
            ValueError：若未找到违规举报。
        """
        return self._get_violation_report(violation_report_ref)

    @is_tool(ToolType.READ)
    def list_violation_reports(
        self,
        violation_type: Optional[str] = None,
        report_status: Optional[str] = None,
        severity: Optional[str] = None,
        reported_employee_ref: Optional[str] = None,
        reported_department_ref: Optional[str] = None,
        investigator_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出违规举报（可选筛选）。

        参数：
            violation_type: 按 violation type 筛选。默认 None。
            report_status: 按 report status 筛选。默认 None。
            severity: 按 severity 筛选。默认 None。
            reported_employee_ref: 按 reported employee ref 筛选。默认 None。
            reported_department_ref: 按 reported department ref 筛选。默认 None。
            investigator_employee_ref: 按 investigator employee ref 筛选。默认 None。

        返回：
            str：匹配「violation reports」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_violation_report.items():
            if violation_type is not None and r.violation_type != violation_type:
                continue
            if report_status is not None and r.report_status != report_status:
                continue
            if severity is not None and r.severity != severity:
                continue
            if reported_employee_ref is not None and r.reported_employee_ref != reported_employee_ref:
                continue
            if reported_department_ref is not None and r.reported_department_ref != reported_department_ref:
                continue
            if investigator_employee_ref is not None and r.investigator_employee_ref != investigator_employee_ref:
                continue
            results.append({
                "violation_report_ref": r.violation_report_ref,
                "is_anonymous": r.is_anonymous,
                "violation_type": r.violation_type,
                "title": r.title,
                "report_status": r.report_status,
                "severity": r.severity,
                "reported_employee_ref": r.reported_employee_ref,
                "reported_department_ref": r.reported_department_ref,
                "investigator_employee_ref": r.investigator_employee_ref,
                "occurred_at": r.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_violation_report(
        self,
        violation_type: str,
        title: str,
        description: str,
        occurred_at: str,
        evidence_summary: str,
        severity: str,
        reporter_employee_ref: Optional[str] = None,
        is_anonymous: bool = False,
        reported_employee_ref: Optional[str] = None,
        reported_department_ref: Optional[str] = None,
    ) -> LawViolationReport:
        """
        新建违规举报。调用前 Agent 须向用户明确确认。

        参数：
            violation_type: 违规类型（bribery、conflict_of_interest、fraud、embezzlement、data_breach、policy_violation、harassment、other）。
            title: 违规举报标题。
            description: 详细描述。
            occurred_at: 违规发生时间（ISO 8601）。
            evidence_summary: 证据摘要。
            severity: 严重程度（low、medium、high、critical）。
            reporter_employee_ref: Employee ref of the reporter (null if anonymous)。默认 None。
            is_anonymous: Whether the report is anonymous。默认 False。
            reported_employee_ref: Employee ref of the person being reported。默认 None。
            reported_department_ref: Department ref being reported。默认 None。

        返回：
            LawViolationReport：新建的举报对象。

        异常：
            ValueError：若入参格式错误。
        """
        valid_types = {"bribery", "conflict_of_interest", "fraud", "embezzlement", "data_breach", "policy_violation", "harassment", "other"}
        if violation_type not in valid_types:
            raise ValueError(f"Invalid violation_type: {violation_type}")
        valid_severities = {"low", "medium", "high", "critical"}
        if severity not in valid_severities:
            raise ValueError(f"Invalid severity: {severity}")
        if reporter_employee_ref and not is_anonymous:
            self._get_employee(reporter_employee_ref)
        if reported_employee_ref:
            self._get_employee(reported_employee_ref)
        if reported_department_ref:
            self._get_department(reported_department_ref)

        now = self._now_iso()
        ref = self._generate_ref("VIORPT", self.db.law_violation_report)

        report = LawViolationReport(
            violation_report_ref=ref,
            reporter_employee_ref=reporter_employee_ref,
            is_anonymous=is_anonymous,
            violation_type=violation_type,
            reported_employee_ref=reported_employee_ref,
            reported_department_ref=reported_department_ref,
            title=title,
            description=description,
            occurred_at=occurred_at,
            evidence_summary=evidence_summary,
            report_status="submitted",
            severity=severity,
            investigator_employee_ref=None,
            investigation_result=None,
            investigation_notes="",
            closed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_violation_report[ref] = report
        return report

    @is_tool(ToolType.WRITE)
    def update_violation_report_status(
        self,
        violation_report_ref: str,
        new_status: str,
        investigator_employee_ref: Optional[str] = None,
        investigation_result: Optional[str] = None,
        investigation_notes: Optional[str] = None,
    ) -> LawViolationReport:
        """
        更新违规举报状态。调用前 Agent 须向用户明确确认。

        参数：
            violation_report_ref: 违规举报的唯一标识。
            new_status: 新状态（submitted、under_investigation、substantiated、unsubstantiated、closed、dismissed）。
            investigator_employee_ref: Employee ref of the investigator (when assigning)。默认 None。
            investigation_result: Result of the investigation。默认 None。
            investigation_notes: Notes from the investigation。默认 None。

        返回：
            LawViolationReport：更新后的举报对象。

        异常：
            ValueError：若未找到举报或状态无效。
        """
        report = self._get_violation_report(violation_report_ref)
        valid_statuses = {"submitted", "under_investigation", "substantiated", "unsubstantiated", "closed", "dismissed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if investigator_employee_ref:
            self._get_employee(investigator_employee_ref)
            report.investigator_employee_ref = investigator_employee_ref
        if investigation_result:
            report.investigation_result = investigation_result
        if investigation_notes:
            report.investigation_notes = investigation_notes
        if new_status in ("closed", "dismissed"):
            report.closed_at = now

        report.report_status = new_status
        report.updated_at = now
        return report

    # ========================================
    # 法务案件（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_legal_case_details(self, legal_case_ref: str) -> LawLegalCase:
        """
        根据 ref 获取法务案件详情。

        参数：
            legal_case_ref: 法务案件的唯一标识。

        返回：
            LawLegalCase：法务案件对象。

        异常：
            ValueError：若未找到法务案件。
        """
        return self._get_legal_case(legal_case_ref)

    @is_tool(ToolType.READ)
    def search_legal_cases(
        self,
        case_type: Optional[str] = None,
        case_category: Optional[str] = None,
        our_role: Optional[str] = None,
        case_status: Optional[str] = None,
        risk_level: Optional[str] = None,
        responsible_employee_ref: Optional[str] = None,
        title_keyword: Optional[str] = None,
    ) -> str:
        """
        搜索法务案件（可选筛选）。

        参数：
            case_type: 按 case type (litigation, arbitration, administrative, mediation) 筛选。默认 None。
            case_category: 按 case category 筛选。默认 None。
            our_role: 按 our role 筛选。默认 None。
            case_status: 按 case status 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            responsible_employee_ref: 按 responsible employee ref 筛选。默认 None。
            title_keyword: 按 keyword in case title (case-insensitive) 筛选。默认 None。

        返回：
            str：匹配「legal cases」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, c in self.db.law_legal_case.items():
            if case_type is not None and c.case_type != case_type:
                continue
            if case_category is not None and c.case_category != case_category:
                continue
            if our_role is not None and c.our_role != our_role:
                continue
            if case_status is not None and c.case_status != case_status:
                continue
            if risk_level is not None and c.risk_level != risk_level:
                continue
            if responsible_employee_ref is not None and c.responsible_employee_ref != responsible_employee_ref:
                continue
            if title_keyword is not None and title_keyword.lower() not in c.case_title.lower():
                continue
            results.append({
                "legal_case_ref": c.legal_case_ref,
                "case_number": c.case_number,
                "case_title": c.case_title,
                "case_type": c.case_type,
                "case_category": c.case_category,
                "our_role": c.our_role,
                "counterparty_name": c.counterparty_name,
                "case_status": c.case_status,
                "risk_level": c.risk_level,
                "claim_amount": c.claim_amount,
                "responsible_employee_ref": c.responsible_employee_ref,
                "filing_date": c.filing_date,
                "hearing_date": c.hearing_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_legal_case_status(
        self,
        legal_case_ref: str,
        new_status: str,
        outcome: Optional[str] = None,
        outcome_summary: Optional[str] = None,
        settlement_amount: Optional[float] = None,
    ) -> LawLegalCase:
        """
        更新法务案件状态。调用前 Agent 须向用户明确确认。

        参数：
            legal_case_ref: 法务案件的唯一标识。
            new_status: 新状态（filed、in_progress、hearing、awaiting_judgment、won、lost、settled、withdrawn、closed）。
            outcome: Outcome of the case。默认 None。
            outcome_summary: Summary of the outcome。默认 None。
            settlement_amount: Settlement amount if settled。默认 None。

        返回：
            LawLegalCase：更新后的案件对象。

        异常：
            ValueError：若未找到案件或状态无效。
        """
        case = self._get_legal_case(legal_case_ref)
        valid_statuses = {"filed", "in_progress", "hearing", "awaiting_judgment", "won", "lost", "settled", "withdrawn", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if outcome:
            case.outcome = outcome
        if outcome_summary:
            case.outcome_summary = outcome_summary
        if settlement_amount is not None:
            case.settlement_amount = settlement_amount
        if new_status in ("won", "lost", "settled", "withdrawn", "closed"):
            case.closed_at = now

        case.case_status = new_status
        case.updated_at = now
        return case

    # ========================================
    # 案件事件（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_case_event_details(self, case_event_ref: str) -> LawCaseEvent:
        """
        根据 ref 获取案件事件详情。

        参数：
            case_event_ref: 案件事件的唯一标识。

        返回：
            LawCaseEvent：案件事件对象。

        异常：
            ValueError：若未找到案件事件。
        """
        return self._get_case_event(case_event_ref)

    @is_tool(ToolType.READ)
    def list_case_events(
        self,
        legal_case_ref: str,
        event_type: Optional[str] = None,
    ) -> str:
        """
        列出某案件的全部事件。

        参数：
            legal_case_ref: 法务案件的唯一标识。
            event_type: 按 event type 筛选。默认 None。

        返回：
            str：case events 的 JSON 数组。

        异常：
            ValueError：若未找到法务案件。
        """
        self._get_legal_case(legal_case_ref)
        results = []
        for ref, e in self.db.law_case_event.items():
            if e.legal_case_ref != legal_case_ref:
                continue
            if event_type is not None and e.event_type != event_type:
                continue
            results.append({
                "case_event_ref": e.case_event_ref,
                "legal_case_ref": e.legal_case_ref,
                "event_type": e.event_type,
                "event_title": e.event_title,
                "event_date": e.event_date,
                "description": e.description,
                "outcome": e.outcome,
                "recorded_by_ref": e.recorded_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_case_event(
        self,
        legal_case_ref: str,
        event_type: str,
        event_title: str,
        event_date: str,
        description: str,
        outcome: str,
        recorded_by_ref: str,
    ) -> LawCaseEvent:
        """
        新建案件事件。调用前 Agent 须向用户明确确认。

        参数：
            legal_case_ref: 引用：legal case.
            event_type: 事件类型（hearing、filing、evidence_submission、mediation、judgment、appeal、settlement、other）。
            event_title: 事件标题。
            event_date: 事件时间（ISO 8601）。
            description: 事件描述。
            outcome: 事件结果。
            recorded_by_ref: 记录人员工 ref。

        返回：
            LawCaseEvent：新建的案件事件对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_legal_case(legal_case_ref)
        self._get_employee(recorded_by_ref)
        valid_types = {"hearing", "filing", "evidence_submission", "mediation", "judgment", "appeal", "settlement", "other"}
        if event_type not in valid_types:
            raise ValueError(f"Invalid event_type: {event_type}")

        now = self._now_iso()
        ref = self._generate_ref("CEVT", self.db.law_case_event)

        event = LawCaseEvent(
            case_event_ref=ref,
            legal_case_ref=legal_case_ref,
            event_type=event_type,
            event_title=event_title,
            event_date=event_date,
            description=description,
            outcome=outcome,
            document_file_ref=None,
            recorded_by_ref=recorded_by_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.law_case_event[ref] = event
        return event

    # ========================================
    # 证据（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_evidence_details(self, evidence_ref: str) -> LawEvidence:
        """
        根据 ref 获取证据详情。

        参数：
            evidence_ref: 证据的唯一标识。

        返回：
            LawEvidence：证据对象。

        异常：
            ValueError：若未找到证据。
        """
        return self._get_evidence(evidence_ref)

    @is_tool(ToolType.READ)
    def list_evidence(
        self,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
        evidence_type: Optional[str] = None,
        evidence_status: Optional[str] = None,
        notarization_status: Optional[str] = None,
    ) -> str:
        """
        列出证据（可选筛选）。

        参数：
            related_resource_type: 按 related resource type (legal_case, violation_report, contract, other) 筛选。默认 None。
            related_resource_ref: 按 related resource ref 筛选。默认 None。
            evidence_type: 按 evidence type 筛选。默认 None。
            evidence_status: 按 evidence status 筛选。默认 None。
            notarization_status: 按 notarization status 筛选。默认 None。

        返回：
            str：匹配「evidence records」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, e in self.db.law_evidence.items():
            if related_resource_type is not None and e.related_resource_type != related_resource_type:
                continue
            if related_resource_ref is not None and e.related_resource_ref != related_resource_ref:
                continue
            if evidence_type is not None and e.evidence_type != evidence_type:
                continue
            if evidence_status is not None and e.evidence_status != evidence_status:
                continue
            if notarization_status is not None and e.notarization_status != notarization_status:
                continue
            results.append({
                "evidence_ref": e.evidence_ref,
                "related_resource_type": e.related_resource_type,
                "related_resource_ref": e.related_resource_ref,
                "evidence_title": e.evidence_title,
                "evidence_type": e.evidence_type,
                "evidence_status": e.evidence_status,
                "notarization_status": e.notarization_status,
                "notarization_number": e.notarization_number,
                "submitted_by_ref": e.submitted_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_evidence(
        self,
        related_resource_type: str,
        related_resource_ref: str,
        evidence_title: str,
        evidence_type: str,
        evidence_description: str,
        file_attachment_ref: str,
        submitted_by_ref: str,
    ) -> LawEvidence:
        """
        新建证据记录。调用前 Agent 须向用户明确确认。

        参数：
            related_resource_type: 关联资源类型（legal_case、violation_report、contract、other）。
            related_resource_ref: 引用：related resource.
            evidence_title: 证据标题。
            evidence_type: 证据类型（document、electronic、physical、testimony、expert_opinion、other）。
            evidence_description: 证据描述。
            file_attachment_ref: 引用：file attachment.
            submitted_by_ref: 提交人员工 ref。

        返回：
            LawEvidence：新建的证据对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(submitted_by_ref)
        valid_resource_types = {"legal_case", "violation_report", "contract", "other"}
        if related_resource_type not in valid_resource_types:
            raise ValueError(f"Invalid related_resource_type: {related_resource_type}")
        valid_evidence_types = {"document", "electronic", "physical", "testimony", "expert_opinion", "other"}
        if evidence_type not in valid_evidence_types:
            raise ValueError(f"Invalid evidence_type: {evidence_type}")

        now = self._now_iso()
        ref = self._generate_ref("EVID", self.db.law_evidence)

        evidence = LawEvidence(
            evidence_ref=ref,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            evidence_title=evidence_title,
            evidence_type=evidence_type,
            evidence_description=evidence_description,
            file_attachment_ref=file_attachment_ref,
            notarization_status="none",
            notarization_number=None,
            notarization_date=None,
            notarization_institution=None,
            notarized_file_ref=None,
            submitted_by_ref=submitted_by_ref,
            evidence_status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.law_evidence[ref] = evidence
        return evidence

    @is_tool(ToolType.WRITE)
    def update_evidence_notarization(
        self,
        evidence_ref: str,
        notarization_status: str,
        notarization_number: Optional[str] = None,
        notarization_date: Optional[str] = None,
        notarization_institution: Optional[str] = None,
    ) -> LawEvidence:
        """
        更新证据的公证状态。调用前 Agent 须向用户明确确认。

        参数：
            evidence_ref: 证据的唯一标识。
            notarization_status: 新公证状态（none、pending、notarized）。
            notarization_number: Notarization certificate number。默认 None。
            notarization_date: Date of notarization (ISO 8601)。默认 None。
            notarization_institution: Name of the notarization institution。默认 None。

        返回：
            LawEvidence：更新后的证据对象。

        异常：
            ValueError：若未找到证据或状态无效。
        """
        evidence = self._get_evidence(evidence_ref)
        valid_statuses = {"none", "pending", "notarized"}
        if notarization_status not in valid_statuses:
            raise ValueError(f"Invalid notarization_status: {notarization_status}")

        evidence.notarization_status = notarization_status
        if notarization_number:
            evidence.notarization_number = notarization_number
        if notarization_date:
            evidence.notarization_date = notarization_date
        if notarization_institution:
            evidence.notarization_institution = notarization_institution
        evidence.updated_at = self._now_iso()
        return evidence

    @is_tool(ToolType.WRITE)
    def update_evidence_status(
        self,
        evidence_ref: str,
        new_status: str,
    ) -> LawEvidence:
        """
        更新证据状态。调用前 Agent 须向用户明确确认。

        参数：
            evidence_ref: 证据的唯一标识。
            new_status: 新状态（active、archived、withdrawn）。

        返回：
            LawEvidence：更新后的证据对象。

        异常：
            ValueError：若未找到证据或状态无效。
        """
        evidence = self._get_evidence(evidence_ref)
        valid_statuses = {"active", "archived", "withdrawn"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        evidence.evidence_status = new_status
        evidence.updated_at = self._now_iso()
        return evidence

    # ========================================
    # 法律咨询（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_legal_consultation_details(self, legal_consultation_ref: str) -> LawLegalConsultation:
        """
        根据 ref 获取法律咨询详情。

        参数：
            legal_consultation_ref: 法律咨询的唯一标识。

        返回：
            LawLegalConsultation：法律咨询对象。

        异常：
            ValueError：若未找到法律咨询。
        """
        return self._get_legal_consultation(legal_consultation_ref)

    @is_tool(ToolType.READ)
    def list_legal_consultations(
        self,
        requester_employee_ref: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
        consultation_type: Optional[str] = None,
        consultation_status: Optional[str] = None,
        urgency: Optional[str] = None,
        channel: Optional[str] = None,
    ) -> str:
        """
        列出法律咨询（可选筛选）。

        参数：
            requester_employee_ref: 按 requester employee ref 筛选。默认 None。
            assigned_to_ref: 按 assigned counsel employee ref 筛选。默认 None。
            consultation_type: 按 consultation type 筛选。默认 None。
            consultation_status: 按 consultation status 筛选。默认 None。
            urgency: 按 urgency 筛选。默认 None。
            channel: 按 channel 筛选。默认 None。

        返回：
            str：匹配「legal consultations」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, c in self.db.law_legal_consultation.items():
            if requester_employee_ref is not None and c.requester_employee_ref != requester_employee_ref:
                continue
            if assigned_to_ref is not None and c.assigned_to_ref != assigned_to_ref:
                continue
            if consultation_type is not None and c.consultation_type != consultation_type:
                continue
            if consultation_status is not None and c.consultation_status != consultation_status:
                continue
            if urgency is not None and c.urgency != urgency:
                continue
            if channel is not None and c.channel != channel:
                continue
            results.append({
                "legal_consultation_ref": c.legal_consultation_ref,
                "requester_employee_ref": c.requester_employee_ref,
                "consultation_type": c.consultation_type,
                "channel": c.channel,
                "title": c.title,
                "urgency": c.urgency,
                "assigned_to_ref": c.assigned_to_ref,
                "consultation_status": c.consultation_status,
                "resolved_at": c.resolved_at,
                "satisfaction_rating": c.satisfaction_rating,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_legal_consultation(
        self,
        requester_employee_ref: str,
        consultation_type: str,
        channel: str,
        title: str,
        description: str,
        urgency: str = "normal",
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
    ) -> LawLegalConsultation:
        """
        新建法律咨询申请。调用前 Agent 须向用户明确确认。

        参数：
            requester_employee_ref: 申请人员工 ref。
            consultation_type: 咨询类型（contract_review、compliance_advice、ip_consultation、labor_law、regulatory、general）。
            channel: 渠道（service_desk、email、phone、meeting、im）。
            title: 咨询申请标题。
            description: 详细描述。
            urgency: Urgency level (low, normal, high, urgent)。默认 "normal"。
            related_resource_type: Type of related resource。默认 None。
            related_resource_ref: Reference to related resource。默认 None。

        返回：
            LawLegalConsultation：新建的咨询对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(requester_employee_ref)
        valid_types = {"contract_review", "compliance_advice", "ip_consultation", "labor_law", "regulatory", "general"}
        if consultation_type not in valid_types:
            raise ValueError(f"Invalid consultation_type: {consultation_type}")
        valid_channels = {"service_desk", "email", "phone", "meeting", "im"}
        if channel not in valid_channels:
            raise ValueError(f"Invalid channel: {channel}")
        valid_urgencies = {"low", "normal", "high", "urgent"}
        if urgency not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {urgency}")

        now = self._now_iso()
        ref = self._generate_ref("LCONS", self.db.law_legal_consultation)

        consultation = LawLegalConsultation(
            legal_consultation_ref=ref,
            requester_employee_ref=requester_employee_ref,
            consultation_type=consultation_type,
            channel=channel,
            title=title,
            description=description,
            urgency=urgency,
            assigned_to_ref=None,
            consultation_status="open",
            response_summary="",
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            resolved_at=None,
            satisfaction_rating=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_legal_consultation[ref] = consultation
        return consultation

    @is_tool(ToolType.WRITE)
    def assign_legal_consultation(
        self,
        legal_consultation_ref: str,
        assigned_to_ref: str,
    ) -> LawLegalConsultation:
        """
        将法律咨询指派给法务人员。调用前 Agent 须向用户明确确认。

        参数：
            legal_consultation_ref: 法律咨询的唯一标识。
            assigned_to_ref: 被指派的法务人员员工 ref。

        返回：
            LawLegalConsultation：更新后的咨询对象。

        异常：
            ValueError：若未找到咨询或员工。
        """
        consultation = self._get_legal_consultation(legal_consultation_ref)
        self._get_employee(assigned_to_ref)
        consultation.assigned_to_ref = assigned_to_ref
        if consultation.consultation_status == "open":
            consultation.consultation_status = "assigned"
        consultation.updated_at = self._now_iso()
        return consultation

    @is_tool(ToolType.WRITE)
    def update_legal_consultation_status(
        self,
        legal_consultation_ref: str,
        new_status: str,
        response_summary: Optional[str] = None,
        satisfaction_rating: Optional[int] = None,
    ) -> LawLegalConsultation:
        """
        更新法律咨询状态。调用前 Agent 须向用户明确确认。

        参数：
            legal_consultation_ref: 法律咨询的唯一标识。
            new_status: 新状态（open、assigned、in_progress、resolved、closed）。
            response_summary: Summary of the response provided。默认 None。
            satisfaction_rating: Satisfaction rating (1-5)。默认 None。

        返回：
            LawLegalConsultation：更新后的咨询对象。

        异常：
            ValueError：若未找到咨询或状态无效。
        """
        consultation = self._get_legal_consultation(legal_consultation_ref)
        valid_statuses = {"open", "assigned", "in_progress", "resolved", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if response_summary:
            consultation.response_summary = response_summary
        if satisfaction_rating is not None:
            if satisfaction_rating < 1 or satisfaction_rating > 5:
                raise ValueError("satisfaction_rating must be between 1 and 5")
            consultation.satisfaction_rating = satisfaction_rating
        if new_status == "resolved" and consultation.resolved_at is None:
            consultation.resolved_at = now

        consultation.consultation_status = new_status
        consultation.updated_at = now
        return consultation

    # ========================================
    # 合规审查（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_compliance_review_details(self, compliance_review_ref: str) -> LawComplianceReview:
        """
        根据 ref 获取合规审查详情。

        参数：
            compliance_review_ref: 合规审查的唯一标识。

        返回：
            LawComplianceReview：合规审查对象。

        异常：
            ValueError：若未找到合规审查。
        """
        return self._get_compliance_review(compliance_review_ref)

    @is_tool(ToolType.READ)
    def list_compliance_reviews(
        self,
        review_type: Optional[str] = None,
        review_status: Optional[str] = None,
        department_ref: Optional[str] = None,
        reviewer_employee_ref: Optional[str] = None,
        risk_level: Optional[str] = None,
        review_result: Optional[str] = None,
    ) -> str:
        """
        列出合规审查（可选筛选）。

        参数：
            review_type: 按 review type 筛选。默认 None。
            review_status: 按 review status 筛选。默认 None。
            department_ref: 按 department ref 筛选。默认 None。
            reviewer_employee_ref: 按 reviewer employee ref 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            review_result: 按 review result 筛选。默认 None。

        返回：
            str：匹配「compliance reviews」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_compliance_review.items():
            if review_type is not None and r.review_type != review_type:
                continue
            if review_status is not None and r.review_status != review_status:
                continue
            if department_ref is not None and r.department_ref != department_ref:
                continue
            if reviewer_employee_ref is not None and r.reviewer_employee_ref != reviewer_employee_ref:
                continue
            if risk_level is not None and r.risk_level != risk_level:
                continue
            if review_result is not None and r.review_result != review_result:
                continue
            results.append({
                "compliance_review_ref": r.compliance_review_ref,
                "review_title": r.review_title,
                "review_type": r.review_type,
                "review_scope": r.review_scope,
                "department_ref": r.department_ref,
                "reviewer_employee_ref": r.reviewer_employee_ref,
                "review_status": r.review_status,
                "risk_level": r.risk_level,
                "review_result": r.review_result,
                "review_date": r.review_date,
                "next_review_date": r.next_review_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_compliance_review(
        self,
        review_title: str,
        review_type: str,
        review_scope: str,
        reviewer_employee_ref: str,
        review_date: str,
        risk_level: str = "low",
        department_ref: Optional[str] = None,
        target_resource_type: Optional[str] = None,
        target_resource_ref: Optional[str] = None,
    ) -> LawComplianceReview:
        """
        新建合规审查。调用前 Agent 须向用户明确确认。

        参数：
            review_title: 审查标题。
            review_type: 审查类型（business_compliance、data_privacy、export_control、anti_corruption、environmental、general）。
            review_scope: 审查范围。
            reviewer_employee_ref: 审核人员工 ref。
            review_date: 审查日期（ISO 8601 日期）。
            risk_level: Risk level (low, medium, high, critical)。默认 "low"。
            department_ref: Department ref being reviewed。默认 None。
            target_resource_type: Type of target resource。默认 None。
            target_resource_ref: Reference to target resource。默认 None。

        返回：
            LawComplianceReview：新建的审查对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(reviewer_employee_ref)
        valid_types = {"business_compliance", "data_privacy", "export_control", "anti_corruption", "environmental", "general"}
        if review_type not in valid_types:
            raise ValueError(f"Invalid review_type: {review_type}")
        valid_risk_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")
        if department_ref:
            self._get_department(department_ref)

        now = self._now_iso()
        ref = self._generate_ref("CREV", self.db.law_compliance_review)

        review = LawComplianceReview(
            compliance_review_ref=ref,
            review_title=review_title,
            review_type=review_type,
            review_scope=review_scope,
            target_resource_type=target_resource_type,
            target_resource_ref=target_resource_ref,
            department_ref=department_ref,
            reviewer_employee_ref=reviewer_employee_ref,
            review_status="planned",
            risk_level=risk_level,
            findings="",
            recommendations="",
            review_result=None,
            review_date=review_date,
            next_review_date=None,
            report_file_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_compliance_review[ref] = review
        return review

    @is_tool(ToolType.WRITE)
    def update_compliance_review(
        self,
        compliance_review_ref: str,
        review_status: Optional[str] = None,
        findings: Optional[str] = None,
        recommendations: Optional[str] = None,
        review_result: Optional[str] = None,
        risk_level: Optional[str] = None,
        next_review_date: Optional[str] = None,
    ) -> LawComplianceReview:
        """
        更新合规审查结论与结果。调用前 Agent 须向用户明确确认。

        参数：
            compliance_review_ref: 合规审查的唯一标识。
            review_status: New status (planned, in_progress, completed, cancelled)。默认 None。
            findings: Findings from the review。默认 None。
            recommendations: Recommendations。默认 None。
            review_result: Result (compliant, non_compliant, partially_compliant)。默认 None。
            risk_level: Updated risk level。默认 None。
            next_review_date: Next review date (ISO 8601 date)。默认 None。

        返回：
            LawComplianceReview：更新后的审查对象。

        异常：
            ValueError：若未找到审查或入参无效。
        """
        review = self._get_compliance_review(compliance_review_ref)

        if review_status is not None:
            valid_statuses = {"planned", "in_progress", "completed", "cancelled"}
            if review_status not in valid_statuses:
                raise ValueError(f"Invalid review_status: {review_status}")
            review.review_status = review_status

        if findings is not None:
            review.findings = findings
        if recommendations is not None:
            review.recommendations = recommendations
        if review_result is not None:
            valid_results = {"compliant", "non_compliant", "partially_compliant"}
            if review_result not in valid_results:
                raise ValueError(f"Invalid review_result: {review_result}")
            review.review_result = review_result
        if risk_level is not None:
            valid_levels = {"low", "medium", "high", "critical"}
            if risk_level not in valid_levels:
                raise ValueError(f"Invalid risk_level: {risk_level}")
            review.risk_level = risk_level
        if next_review_date is not None:
            review.next_review_date = next_review_date

        review.updated_at = self._now_iso()
        return review

    # ========================================
    # 公司主体（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_corporate_entity_details(self, corporate_entity_ref: str) -> LawCorporateEntity:
        """
        根据 ref 获取公司主体详情。

        参数：
            corporate_entity_ref: 公司主体的唯一标识。

        返回：
            LawCorporateEntity：公司主体对象。

        异常：
            ValueError：若未找到公司主体。
        """
        return self._get_corporate_entity(corporate_entity_ref)

    @is_tool(ToolType.READ)
    def list_corporate_entities(
        self,
        entity_type: Optional[str] = None,
        entity_status: Optional[str] = None,
        parent_entity_ref: Optional[str] = None,
    ) -> str:
        """
        列出公司主体（可选筛选）。

        参数：
            entity_type: 按 entity type (subsidiary, branch, joint_venture, holding, representative_office) 筛选。默认 None。
            entity_status: 按 entity status 筛选。默认 None。
            parent_entity_ref: 按 parent entity ref 筛选。默认 None。

        返回：
            str：匹配「corporate entities」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, e in self.db.law_corporate_entity.items():
            if entity_type is not None and e.entity_type != entity_type:
                continue
            if entity_status is not None and e.entity_status != entity_status:
                continue
            if parent_entity_ref is not None and e.parent_entity_ref != parent_entity_ref:
                continue
            results.append({
                "corporate_entity_ref": e.corporate_entity_ref,
                "entity_name": e.entity_name,
                "entity_type": e.entity_type,
                "unified_social_credit_code": e.unified_social_credit_code,
                "legal_representative": e.legal_representative,
                "entity_status": e.entity_status,
                "parent_entity_ref": e.parent_entity_ref,
                "responsible_employee_ref": e.responsible_employee_ref,
                "establishment_date": e.establishment_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_corporate_entity_ref_by_name(self, entity_name: str) -> str:
        """
        按名称模糊查找公司主体 ref（不区分大小写）。

        参数：
            entity_name: 公司主体名称（可部分匹配）。

        返回：
            str：匹配到的entity 的 corporate_entity_ref。

        异常：
            ValueError：若未匹配到主体。
        """
        search = entity_name.lower()
        for ref, e in self.db.law_corporate_entity.items():
            if search in e.entity_name.lower():
                return ref
        raise ValueError("Corporate entity not found")

    @is_tool(ToolType.WRITE)
    def update_corporate_entity_status(
        self,
        corporate_entity_ref: str,
        new_status: str,
    ) -> LawCorporateEntity:
        """
        Update the status of a corporate entity. 调用前 Agent 须向用户明确确认。

        参数：
            corporate_entity_ref: 公司主体的唯一标识。
            new_status: 新状态（active、inactive、dissolved、merging、liquidating）。

        返回：
            LawCorporateEntity：更新后的公司主体对象。

        异常：
            ValueError：若未找到主体或状态无效。
        """
        entity = self._get_corporate_entity(corporate_entity_ref)
        valid_statuses = {"active", "inactive", "dissolved", "merging", "liquidating"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        entity.entity_status = new_status
        entity.updated_at = self._now_iso()
        return entity

    # ========================================
    # 主体变更（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_entity_change_details(self, entity_change_ref: str) -> LawEntityChange:
        """
        根据 ref 获取主体变更详情。

        参数：
            entity_change_ref: 主体变更的唯一标识。

        返回：
            LawEntityChange：主体变更对象。

        异常：
            ValueError：若未找到主体变更。
        """
        return self._get_entity_change(entity_change_ref)

    @is_tool(ToolType.READ)
    def list_entity_changes(
        self,
        corporate_entity_ref: Optional[str] = None,
        change_type: Optional[str] = None,
        change_status: Optional[str] = None,
    ) -> str:
        """
        列出主体变更（可选筛选）。

        参数：
            corporate_entity_ref: 按 corporate entity ref 筛选。默认 None。
            change_type: 按 change type 筛选。默认 None。
            change_status: 按 change status 筛选。默认 None。

        返回：
            str：匹配「entity changes」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, c in self.db.law_entity_change.items():
            if corporate_entity_ref is not None and c.corporate_entity_ref != corporate_entity_ref:
                continue
            if change_type is not None and c.change_type != change_type:
                continue
            if change_status is not None and c.change_status != change_status:
                continue
            results.append({
                "entity_change_ref": c.entity_change_ref,
                "corporate_entity_ref": c.corporate_entity_ref,
                "change_type": c.change_type,
                "change_description": c.change_description,
                "before_value": c.before_value,
                "after_value": c.after_value,
                "change_status": c.change_status,
                "effective_date": c.effective_date,
                "applied_by_ref": c.applied_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_entity_change(
        self,
        corporate_entity_ref: str,
        change_type: str,
        change_description: str,
        before_value: str,
        after_value: str,
        applied_by_ref: str,
    ) -> LawEntityChange:
        """
        新建主体变更申请。调用前 Agent 须向用户明确确认。

        参数：
            corporate_entity_ref: 引用：corporate entity.
            change_type: 变更类型（name_change、address_change、capital_change、scope_change、representative_change、shareholder_change、other）。
            change_description: 变更说明。
            before_value: 变更前的值。
            after_value: 变更后的值。
            applied_by_ref: 申请人的员工 ref。

        返回：
            LawEntityChange：新建的变更对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_corporate_entity(corporate_entity_ref)
        self._get_employee(applied_by_ref)
        valid_types = {"name_change", "address_change", "capital_change", "scope_change", "representative_change", "shareholder_change", "other"}
        if change_type not in valid_types:
            raise ValueError(f"Invalid change_type: {change_type}")

        now = self._now_iso()
        ref = self._generate_ref("ECHG", self.db.law_entity_change)

        change = LawEntityChange(
            entity_change_ref=ref,
            corporate_entity_ref=corporate_entity_ref,
            change_type=change_type,
            change_description=change_description,
            before_value=before_value,
            after_value=after_value,
            change_status="pending",
            effective_date=None,
            applied_by_ref=applied_by_ref,
            approved_at=None,
            document_file_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_entity_change[ref] = change
        return change

    @is_tool(ToolType.WRITE)
    def update_entity_change_status(
        self,
        entity_change_ref: str,
        new_status: str,
        effective_date: Optional[str] = None,
    ) -> LawEntityChange:
        """
        更新主体变更状态。调用前 Agent 须向用户明确确认。

        参数：
            entity_change_ref: 主体变更的唯一标识。
            new_status: 新状态（pending、approved、rejected、completed、cancelled）。
            effective_date: Effective date when completing (ISO 8601 date)。默认 None。

        返回：
            LawEntityChange：更新后的变更对象。

        异常：
            ValueError：若未找到变更或状态无效。
        """
        change = self._get_entity_change(entity_change_ref)
        valid_statuses = {"pending", "approved", "rejected", "completed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "approved":
            change.approved_at = now
        if new_status == "completed" and effective_date:
            change.effective_date = effective_date
        elif new_status == "completed" and change.effective_date is None:
            change.effective_date = now
        change.change_status = new_status
        change.updated_at = now
        return change

    # ========================================
    # 资质证书（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_qualification_certificate_details(self, qualification_certificate_ref: str) -> LawQualificationCertificate:
        """
        根据 ref 获取资质证书详情。

        参数：
            qualification_certificate_ref: 资质证书的唯一标识。

        返回：
            LawQualificationCertificate：资质证书对象。

        异常：
            ValueError：若未找到资质证书。
        """
        return self._get_qualification_certificate(qualification_certificate_ref)

    @is_tool(ToolType.READ)
    def list_qualification_certificates(
        self,
        certificate_type: Optional[str] = None,
        holder_type: Optional[str] = None,
        certificate_status: Optional[str] = None,
        holder_entity_ref: Optional[str] = None,
        holder_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出资质证书（可选筛选）。

        参数：
            certificate_type: 按 certificate type 筛选。默认 None。
            holder_type: 按 holder type (company, employee) 筛选。默认 None。
            certificate_status: 按 certificate status 筛选。默认 None。
            holder_entity_ref: 按 holder entity ref 筛选。默认 None。
            holder_employee_ref: 按 holder employee ref 筛选。默认 None。

        返回：
            str：匹配「qualification certificates」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, c in self.db.law_qualification_certificate.items():
            if certificate_type is not None and c.certificate_type != certificate_type:
                continue
            if holder_type is not None and c.holder_type != holder_type:
                continue
            if certificate_status is not None and c.certificate_status != certificate_status:
                continue
            if holder_entity_ref is not None and c.holder_entity_ref != holder_entity_ref:
                continue
            if holder_employee_ref is not None and c.holder_employee_ref != holder_employee_ref:
                continue
            results.append({
                "qualification_certificate_ref": c.qualification_certificate_ref,
                "certificate_name": c.certificate_name,
                "certificate_type": c.certificate_type,
                "certificate_number": c.certificate_number,
                "issuing_authority": c.issuing_authority,
                "holder_type": c.holder_type,
                "issue_date": c.issue_date,
                "expiry_date": c.expiry_date,
                "certificate_status": c.certificate_status,
                "custodian_employee_ref": c.custodian_employee_ref,
                "storage_location": c.storage_location,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_qualification_certificate_status(
        self,
        qualification_certificate_ref: str,
        new_status: str,
    ) -> LawQualificationCertificate:
        """
        更新资质证书状态。调用前 Agent 须向用户明确确认。

        参数：
            qualification_certificate_ref: 资质证书的唯一标识。
            new_status: 新状态（active、expired、revoked、pending_renewal）。

        返回：
            LawQualificationCertificate：更新后的证书对象。

        异常：
            ValueError：若未找到证书或状态无效。
        """
        cert = self._get_qualification_certificate(qualification_certificate_ref)
        valid_statuses = {"active", "expired", "revoked", "pending_renewal"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        cert.certificate_status = new_status
        cert.updated_at = self._now_iso()
        return cert

    # ========================================
    # 证照使用申请（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_license_usage_request_details(self, license_usage_request_ref: str) -> LawLicenseUsageRequest:
        """
        根据 ref 获取证照使用申请详情。

        参数：
            license_usage_request_ref: 证照使用申请的唯一标识。

        返回：
            LawLicenseUsageRequest：证照使用申请对象。

        异常：
            ValueError：若未找到证照使用申请。
        """
        return self._get_license_usage_request(license_usage_request_ref)

    @is_tool(ToolType.READ)
    def list_license_usage_requests(
        self,
        qualification_certificate_ref: Optional[str] = None,
        applicant_employee_ref: Optional[str] = None,
        request_status: Optional[str] = None,
    ) -> str:
        """
        列出证照使用申请（可选筛选）。

        参数：
            qualification_certificate_ref: 按 certificate ref 筛选。默认 None。
            applicant_employee_ref: 按 applicant employee ref 筛选。默认 None。
            request_status: 按 request status 筛选。默认 None。

        返回：
            str：匹配「license usage requests」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_license_usage_request.items():
            if qualification_certificate_ref is not None and r.qualification_certificate_ref != qualification_certificate_ref:
                continue
            if applicant_employee_ref is not None and r.applicant_employee_ref != applicant_employee_ref:
                continue
            if request_status is not None and r.request_status != request_status:
                continue
            results.append({
                "license_usage_request_ref": r.license_usage_request_ref,
                "qualification_certificate_ref": r.qualification_certificate_ref,
                "applicant_employee_ref": r.applicant_employee_ref,
                "usage_purpose": r.usage_purpose,
                "usage_type": r.usage_type,
                "usage_start_date": r.usage_start_date,
                "usage_end_date": r.usage_end_date,
                "request_status": r.request_status,
                "approved_by_ref": r.approved_by_ref,
                "borrowed_at": r.borrowed_at,
                "returned_at": r.returned_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_license_usage_request(
        self,
        qualification_certificate_ref: str,
        applicant_employee_ref: str,
        usage_purpose: str,
        usage_type: str,
        usage_start_date: str,
        usage_end_date: str,
    ) -> LawLicenseUsageRequest:
        """
        新建证照使用申请。调用前 Agent 须向用户明确确认。

        参数：
            qualification_certificate_ref: 引用：qualification certificate.
            applicant_employee_ref: 申请人的员工 ref。
            usage_purpose: 证照使用目的。
            usage_type: 使用类型（original、copy、scan）。
            usage_start_date: 开始日期（ISO 8601 日期）。
            usage_end_date: 结束日期（ISO 8601 日期）。

        返回：
            LawLicenseUsageRequest：新建的申请对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_qualification_certificate(qualification_certificate_ref)
        self._get_employee(applicant_employee_ref)
        valid_types = {"original", "copy", "scan"}
        if usage_type not in valid_types:
            raise ValueError(f"Invalid usage_type: {usage_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("LUREQ", self.db.law_license_usage_request)

        request = LawLicenseUsageRequest(
            license_usage_request_ref=ref,
            qualification_certificate_ref=qualification_certificate_ref,
            applicant_employee_ref=applicant_employee_ref,
            usage_purpose=usage_purpose,
            usage_type=usage_type,
            usage_start_date=usage_start_date,
            usage_end_date=usage_end_date,
            request_status="pending",
            approved_by_ref=None,
            borrowed_at=None,
            returned_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_license_usage_request[ref] = request
        return request

    @is_tool(ToolType.WRITE)
    def update_license_usage_request_status(
        self,
        license_usage_request_ref: str,
        new_status: str,
        approved_by_ref: Optional[str] = None,
    ) -> LawLicenseUsageRequest:
        """
        更新证照使用申请状态。调用前 Agent 须向用户明确确认。

        参数：
            license_usage_request_ref: 证照使用申请的唯一标识。
            new_status: 新状态（pending、approved、rejected、borrowed、returned、overdue）。
            approved_by_ref: Employee ref of the approver (when approving)。默认 None。

        返回：
            LawLicenseUsageRequest：更新后的申请对象。

        异常：
            ValueError：若未找到申请或状态无效。
        """
        request = self._get_license_usage_request(license_usage_request_ref)
        valid_statuses = {"pending", "approved", "rejected", "borrowed", "returned", "overdue"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        if new_status == "approved" and approved_by_ref:
            self._get_employee(approved_by_ref)
            request.approved_by_ref = approved_by_ref
        if new_status == "borrowed":
            request.borrowed_at = now
        if new_status == "returned":
            request.returned_at = now

        request.request_status = new_status
        request.updated_at = now
        return request

    # ========================================
    # 关联方（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_related_party_details(self, related_party_ref: str) -> LawRelatedParty:
        """
        根据 ref 获取关联方详情。

        参数：
            related_party_ref: 关联方的唯一标识。

        返回：
            LawRelatedParty：关联方对象。

        异常：
            ValueError：若未找到关联方。
        """
        return self._get_related_party(related_party_ref)

    @is_tool(ToolType.READ)
    def list_related_parties(
        self,
        party_type: Optional[str] = None,
        relationship_type: Optional[str] = None,
        party_status: Optional[str] = None,
        risk_level: Optional[str] = None,
        related_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出关联方（可选筛选）。

        参数：
            party_type: 按 party type (enterprise, individual, government) 筛选。默认 None。
            relationship_type: 按 relationship type 筛选。默认 None。
            party_status: 按 party status 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            related_employee_ref: 按 related employee ref 筛选。默认 None。

        返回：
            str：匹配「related parties」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.law_related_party.items():
            if party_type is not None and p.party_type != party_type:
                continue
            if relationship_type is not None and p.relationship_type != relationship_type:
                continue
            if party_status is not None and p.party_status != party_status:
                continue
            if risk_level is not None and p.risk_level != risk_level:
                continue
            if related_employee_ref is not None and p.related_employee_ref != related_employee_ref:
                continue
            results.append({
                "related_party_ref": p.related_party_ref,
                "party_name": p.party_name,
                "party_type": p.party_type,
                "relationship_type": p.relationship_type,
                "relationship_description": p.relationship_description,
                "party_status": p.party_status,
                "risk_level": p.risk_level,
                "related_employee_ref": p.related_employee_ref,
                "identified_by_ref": p.identified_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_related_party(
        self,
        party_name: str,
        party_type: str,
        relationship_type: str,
        relationship_description: str,
        contact_info: str,
        risk_level: str,
        identified_by_ref: str,
        related_entity_ref: Optional[str] = None,
        related_employee_ref: Optional[str] = None,
        notes: str = "",
    ) -> LawRelatedParty:
        """
        新建关联方记录。调用前 Agent 须向用户明确确认。

        参数：
            party_name: 关联方名称。
            party_type: 方类型（enterprise、individual、government）。
            relationship_type: 关系类型（shareholder、subsidiary、affiliate、key_personnel、family_member、business_partner、other）。
            relationship_description: 关系说明。
            contact_info: 联系方式。
            risk_level: 风险等级（low、medium、high、critical）。
            identified_by_ref: 识别关联方的员工 ref。
            related_entity_ref: Reference to related corporate entity。默认 None。
            related_employee_ref: Reference to related employee。默认 None。
            notes: Additional notes。默认 ""

        返回：
            LawRelatedParty：新建的关联方对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(identified_by_ref)
        valid_party_types = {"enterprise", "individual", "government"}
        if party_type not in valid_party_types:
            raise ValueError(f"Invalid party_type: {party_type}")
        valid_relationship_types = {"shareholder", "subsidiary", "affiliate", "key_personnel", "family_member", "business_partner", "other"}
        if relationship_type not in valid_relationship_types:
            raise ValueError(f"Invalid relationship_type: {relationship_type}")
        valid_risk_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")
        if related_entity_ref:
            self._get_corporate_entity(related_entity_ref)
        if related_employee_ref:
            self._get_employee(related_employee_ref)

        now = self._now_iso()
        ref = self._generate_ref("RPTY", self.db.law_related_party)

        party = LawRelatedParty(
            related_party_ref=ref,
            party_name=party_name,
            party_type=party_type,
            relationship_type=relationship_type,
            relationship_description=relationship_description,
            related_entity_ref=related_entity_ref,
            related_employee_ref=related_employee_ref,
            contact_info=contact_info,
            party_status="active",
            risk_level=risk_level,
            identified_by_ref=identified_by_ref,
            identified_at=now,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.law_related_party[ref] = party
        return party

    @is_tool(ToolType.WRITE)
    def update_related_party_status(
        self,
        related_party_ref: str,
        new_status: str,
    ) -> LawRelatedParty:
        """
        更新关联方状态。调用前 Agent 须向用户明确确认。

        参数：
            related_party_ref: 关联方的唯一标识。
            new_status: 新状态（active、inactive、under_review）。

        返回：
            LawRelatedParty：更新后的关联方对象。

        异常：
            ValueError：若未找到关联方或状态无效。
        """
        party = self._get_related_party(related_party_ref)
        valid_statuses = {"active", "inactive", "under_review"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        party.party_status = new_status
        party.updated_at = self._now_iso()
        return party

    # ========================================
    # 关联方交易（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_related_party_transaction_details(self, related_party_transaction_ref: str) -> LawRelatedPartyTransaction:
        """
        根据 ref 获取关联方交易详情。

        参数：
            related_party_transaction_ref: 关联方交易的唯一标识。

        返回：
            LawRelatedPartyTransaction：关联方交易对象。

        异常：
            ValueError：若未找到关联方交易。
        """
        return self._get_related_party_transaction(related_party_transaction_ref)

    @is_tool(ToolType.READ)
    def list_related_party_transactions(
        self,
        related_party_ref: Optional[str] = None,
        transaction_type: Optional[str] = None,
        compliance_status: Optional[str] = None,
    ) -> str:
        """
        列出关联方交易（可选筛选）。

        参数：
            related_party_ref: 按 related party ref 筛选。默认 None。
            transaction_type: 按 transaction type 筛选。默认 None。
            compliance_status: 按 compliance status 筛选。默认 None。

        返回：
            str：匹配「related party transactions」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, t in self.db.law_related_party_transaction.items():
            if related_party_ref is not None and t.related_party_ref != related_party_ref:
                continue
            if transaction_type is not None and t.transaction_type != transaction_type:
                continue
            if compliance_status is not None and t.compliance_status != compliance_status:
                continue
            results.append({
                "related_party_transaction_ref": t.related_party_transaction_ref,
                "related_party_ref": t.related_party_ref,
                "transaction_type": t.transaction_type,
                "transaction_description": t.transaction_description,
                "transaction_amount": t.transaction_amount,
                "currency": t.currency,
                "transaction_date": t.transaction_date,
                "compliance_status": t.compliance_status,
                "reviewed_by_ref": t.reviewed_by_ref,
                "contract_ref": t.contract_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def review_related_party_transaction(
        self,
        related_party_transaction_ref: str,
        reviewed_by_ref: str,
        compliance_status: str,
        review_comments: str = "",
    ) -> LawRelatedPartyTransaction:
        """
        对关联方交易作合规审核。调用前 Agent 须向用户明确确认。

        参数：
            related_party_transaction_ref: transaction 的唯一标识。
            reviewed_by_ref: 审核人员工 ref。
            compliance_status: 新合规状态（pending_review、approved、rejected、flagged）。
            review_comments: Comments from the review。默认 ""

        返回：
            LawRelatedPartyTransaction：更新后的交易对象。

        异常：
            ValueError：若未找到交易或入参无效。
        """
        transaction = self._get_related_party_transaction(related_party_transaction_ref)
        self._get_employee(reviewed_by_ref)
        valid_statuses = {"pending_review", "approved", "rejected", "flagged"}
        if compliance_status not in valid_statuses:
            raise ValueError(f"Invalid compliance_status: {compliance_status}")

        now = self._now_iso()
        transaction.reviewed_by_ref = reviewed_by_ref
        transaction.reviewed_at = now
        transaction.compliance_status = compliance_status
        transaction.review_comments = review_comments
        transaction.updated_at = now
        return transaction

    # ========================================
    # 创新提案（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_innovation_proposal_details(self, innovation_proposal_ref: str) -> LawInnovationProposal:
        """
        根据 ref 获取创新提案详情。

        参数：
            innovation_proposal_ref: 创新提案的唯一标识。

        返回：
            LawInnovationProposal：创新提案对象。

        异常：
            ValueError：若未找到创新提案。
        """
        return self._get_innovation_proposal(innovation_proposal_ref)

    @is_tool(ToolType.READ)
    def list_innovation_proposals(
        self,
        proposer_employee_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        proposal_category: Optional[str] = None,
        proposal_status: Optional[str] = None,
    ) -> str:
        """
        列出创新提案（可选筛选）。

        参数：
            proposer_employee_ref: 按 proposer employee ref 筛选。默认 None。
            department_ref: 按 department ref 筛选。默认 None。
            proposal_category: 按 proposal category 筛选。默认 None。
            proposal_status: 按 proposal status 筛选。默认 None。

        返回：
            str：匹配「innovation proposals」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.law_innovation_proposal.items():
            if proposer_employee_ref is not None and p.proposer_employee_ref != proposer_employee_ref:
                continue
            if department_ref is not None and p.department_ref != department_ref:
                continue
            if proposal_category is not None and p.proposal_category != proposal_category:
                continue
            if proposal_status is not None and p.proposal_status != proposal_status:
                continue
            results.append({
                "innovation_proposal_ref": p.innovation_proposal_ref,
                "proposer_employee_ref": p.proposer_employee_ref,
                "department_ref": p.department_ref,
                "proposal_title": p.proposal_title,
                "proposal_category": p.proposal_category,
                "proposal_status": p.proposal_status,
                "reviewer_employee_ref": p.reviewer_employee_ref,
                "review_score": p.review_score,
                "ip_asset_ref": p.ip_asset_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_innovation_proposal(
        self,
        proposer_employee_ref: str,
        department_ref: str,
        proposal_title: str,
        proposal_category: str,
        description: str,
        expected_benefit: str,
        feasibility_assessment: str,
    ) -> LawInnovationProposal:
        """
        新建创新提案。调用前 Agent 须向用户明确确认。

        参数：
            proposer_employee_ref: 提案人员工 ref。
            department_ref: 部门 ref。
            proposal_title: 提案标题。
            proposal_category: 类别（product、process、technology、management、service、other）。
            description: 详细描述。
            expected_benefit: 预期收益。
            feasibility_assessment: 可行性评估。

        返回：
            LawInnovationProposal：新建的提案对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(proposer_employee_ref)
        self._get_department(department_ref)
        valid_categories = {"product", "process", "technology", "management", "service", "other"}
        if proposal_category not in valid_categories:
            raise ValueError(f"Invalid proposal_category: {proposal_category}")

        now = self._now_iso()
        ref = self._generate_ref("INNOV", self.db.law_innovation_proposal)

        proposal = LawInnovationProposal(
            innovation_proposal_ref=ref,
            proposer_employee_ref=proposer_employee_ref,
            department_ref=department_ref,
            proposal_title=proposal_title,
            proposal_category=proposal_category,
            description=description,
            expected_benefit=expected_benefit,
            feasibility_assessment=feasibility_assessment,
            proposal_status="submitted",
            reviewer_employee_ref=None,
            review_score=None,
            review_comments="",
            ip_asset_ref=None,
            proposal_file_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_innovation_proposal[ref] = proposal
        return proposal

    @is_tool(ToolType.WRITE)
    def update_innovation_proposal_status(
        self,
        innovation_proposal_ref: str,
        new_status: str,
        reviewer_employee_ref: Optional[str] = None,
        review_score: Optional[float] = None,
        review_comments: Optional[str] = None,
    ) -> LawInnovationProposal:
        """
        更新创新提案状态。调用前 Agent 须向用户明确确认。

        参数：
            innovation_proposal_ref: 创新提案的唯一标识。
            new_status: 新状态（submitted、under_review、approved、rejected、in_progress、completed、archived）。
            reviewer_employee_ref: Employee ref of the reviewer。默认 None。
            review_score: Review score。默认 None。
            review_comments: Review comments。默认 None。

        返回：
            LawInnovationProposal：更新后的提案对象。

        异常：
            ValueError：若未找到提案或状态无效。
        """
        proposal = self._get_innovation_proposal(innovation_proposal_ref)
        valid_statuses = {"submitted", "under_review", "approved", "rejected", "in_progress", "completed", "archived"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        if reviewer_employee_ref:
            self._get_employee(reviewer_employee_ref)
            proposal.reviewer_employee_ref = reviewer_employee_ref
        if review_score is not None:
            proposal.review_score = review_score
        if review_comments is not None:
            proposal.review_comments = review_comments

        proposal.proposal_status = new_status
        proposal.updated_at = self._now_iso()
        return proposal

    # ========================================
    # 供应商评估（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_supplier_assessment_details(self, supplier_assessment_ref: str) -> LawSupplierAssessment:
        """
        根据 ref 获取供应商评估详情。

        参数：
            supplier_assessment_ref: 供应商评估的唯一标识。

        返回：
            LawSupplierAssessment：供应商评估对象。

        异常：
            ValueError：若未找到供应商评估。
        """
        return self._get_supplier_assessment(supplier_assessment_ref)

    @is_tool(ToolType.READ)
    def list_supplier_assessments(
        self,
        supplier_party_ref: Optional[str] = None,
        assessment_type: Optional[str] = None,
        assessment_status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> str:
        """
        列出供应商评估（可选筛选）。

        参数：
            supplier_party_ref: 按 supplier party ref 筛选。默认 None。
            assessment_type: 按 assessment type 筛选。默认 None。
            assessment_status: 按 assessment status 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。

        返回：
            str：匹配「supplier assessments」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, a in self.db.law_supplier_assessment.items():
            if supplier_party_ref is not None and a.supplier_party_ref != supplier_party_ref:
                continue
            if assessment_type is not None and a.assessment_type != assessment_type:
                continue
            if assessment_status is not None and a.assessment_status != assessment_status:
                continue
            if risk_level is not None and a.risk_level != risk_level:
                continue
            results.append({
                "supplier_assessment_ref": a.supplier_assessment_ref,
                "supplier_name": a.supplier_name,
                "supplier_party_ref": a.supplier_party_ref,
                "assessment_type": a.assessment_type,
                "assessor_employee_ref": a.assessor_employee_ref,
                "assessment_date": a.assessment_date,
                "overall_score": a.overall_score,
                "risk_level": a.risk_level,
                "assessment_status": a.assessment_status,
                "next_assessment_date": a.next_assessment_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_supplier_assessment(
        self,
        supplier_name: str,
        assessment_type: str,
        assessor_employee_ref: str,
        assessment_date: str,
        risk_level: str = "low",
        supplier_party_ref: Optional[str] = None,
    ) -> LawSupplierAssessment:
        """
        新建供应商评估。调用前 Agent 须向用户明确确认。

        参数：
            supplier_name: 供应商名称。
            assessment_type: 评估类型（qualification、annual_review、incident_review、exit_review）。
            assessor_employee_ref: 评估人的员工 ref。
            assessment_date: 评估日期（ISO 8601 日期）。
            risk_level: Risk level (low, medium, high, critical)。默认 "low"。
            supplier_party_ref: 引用：contract party。默认 None。

        返回：
            LawSupplierAssessment：新建的评估对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(assessor_employee_ref)
        valid_types = {"qualification", "annual_review", "incident_review", "exit_review"}
        if assessment_type not in valid_types:
            raise ValueError(f"Invalid assessment_type: {assessment_type}")
        valid_risk_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")
        if supplier_party_ref:
            self._get_contract_party(supplier_party_ref)

        now = self._now_iso()
        ref = self._generate_ref("SUPASS", self.db.law_supplier_assessment)

        assessment = LawSupplierAssessment(
            supplier_assessment_ref=ref,
            supplier_name=supplier_name,
            supplier_party_ref=supplier_party_ref,
            assessment_type=assessment_type,
            assessor_employee_ref=assessor_employee_ref,
            assessment_date=assessment_date,
            financial_score=None,
            compliance_score=None,
            quality_score=None,
            overall_score=None,
            risk_level=risk_level,
            risk_findings="",
            recommendations="",
            assessment_status="planned",
            report_file_ref=None,
            next_assessment_date=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_supplier_assessment[ref] = assessment
        return assessment

    @is_tool(ToolType.WRITE)
    def update_supplier_assessment(
        self,
        supplier_assessment_ref: str,
        assessment_status: Optional[str] = None,
        financial_score: Optional[float] = None,
        compliance_score: Optional[float] = None,
        quality_score: Optional[float] = None,
        overall_score: Optional[float] = None,
        risk_level: Optional[str] = None,
        risk_findings: Optional[str] = None,
        recommendations: Optional[str] = None,
        next_assessment_date: Optional[str] = None,
    ) -> LawSupplierAssessment:
        """
        更新供应商评估分数与结论。调用前 Agent 须向用户明确确认。

        参数：
            supplier_assessment_ref: 供应商评估的唯一标识。
            assessment_status: New status (planned, in_progress, completed, cancelled)。默认 None。
            financial_score: Financial score。默认 None。
            compliance_score: Compliance score。默认 None。
            quality_score: Quality score。默认 None。
            overall_score: Overall score。默认 None。
            risk_level: Updated risk level。默认 None。
            risk_findings: Risk findings。默认 None。
            recommendations: Recommendations。默认 None。
            next_assessment_date: Next assessment date (ISO 8601 date)。默认 None。

        返回：
            LawSupplierAssessment：更新后的评估对象。

        异常：
            ValueError：若未找到评估或入参无效。
        """
        assessment = self._get_supplier_assessment(supplier_assessment_ref)

        if assessment_status is not None:
            valid_statuses = {"planned", "in_progress", "completed", "cancelled"}
            if assessment_status not in valid_statuses:
                raise ValueError(f"Invalid assessment_status: {assessment_status}")
            assessment.assessment_status = assessment_status
        if financial_score is not None:
            assessment.financial_score = financial_score
        if compliance_score is not None:
            assessment.compliance_score = compliance_score
        if quality_score is not None:
            assessment.quality_score = quality_score
        if overall_score is not None:
            assessment.overall_score = overall_score
        if risk_level is not None:
            valid_levels = {"low", "medium", "high", "critical"}
            if risk_level not in valid_levels:
                raise ValueError(f"Invalid risk_level: {risk_level}")
            assessment.risk_level = risk_level
        if risk_findings is not None:
            assessment.risk_findings = risk_findings
        if recommendations is not None:
            assessment.recommendations = recommendations
        if next_assessment_date is not None:
            assessment.next_assessment_date = next_assessment_date

        assessment.updated_at = self._now_iso()
        return assessment

    # ========================================
    # 高风险软件（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_high_risk_software_details(self, high_risk_software_ref: str) -> LawHighRiskSoftware:
        """
        根据 ref 获取高风险软件详情。

        参数：
            high_risk_software_ref: 高风险软件记录的唯一标识。

        返回：
            LawHighRiskSoftware：高风险软件对象。

        异常：
            ValueError：若未找到高风险软件记录。
        """
        return self._get_high_risk_software(high_risk_software_ref)

    @is_tool(ToolType.READ)
    def list_high_risk_software(
        self,
        risk_level: Optional[str] = None,
        risk_category: Optional[str] = None,
        usage_status: Optional[str] = None,
        compliance_status: Optional[str] = None,
    ) -> str:
        """
        列出高风险软件（可选筛选）。

        参数：
            risk_level: 按 risk level (medium, high, critical) 筛选。默认 None。
            risk_category: 按 risk category 筛选。默认 None。
            usage_status: 按 usage status 筛选。默认 None。
            compliance_status: 按 compliance status 筛选。默认 None。

        返回：
            str：匹配「high-risk software records」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, s in self.db.law_high_risk_software.items():
            if risk_level is not None and s.risk_level != risk_level:
                continue
            if risk_category is not None and s.risk_category != risk_category:
                continue
            if usage_status is not None and s.usage_status != usage_status:
                continue
            if compliance_status is not None and s.compliance_status != compliance_status:
                continue
            results.append({
                "high_risk_software_ref": s.high_risk_software_ref,
                "software_name": s.software_name,
                "software_version": s.software_version,
                "vendor": s.vendor,
                "risk_level": s.risk_level,
                "risk_category": s.risk_category,
                "usage_status": s.usage_status,
                "compliance_status": s.compliance_status,
                "affected_departments": s.affected_departments,
                "alternative_software": s.alternative_software,
                "assessed_by_ref": s.assessed_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_high_risk_software(
        self,
        high_risk_software_ref: str,
        usage_status: Optional[str] = None,
        compliance_status: Optional[str] = None,
        mitigation_measures: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> LawHighRiskSoftware:
        """
        更新高风险软件记录。调用前 Agent 须向用户明确确认。

        参数：
            high_risk_software_ref: 高风险软件记录的唯一标识。
            usage_status: New usage status (restricted, prohibited, approved_with_conditions, under_review)。默认 None。
            compliance_status: New compliance status (compliant, non_compliant, pending_review, exempted)。默认 None。
            mitigation_measures: Updated mitigation measures。默认 None。
            risk_level: Updated risk level (medium, high, critical)。默认 None。

        返回：
            LawHighRiskSoftware：更新后的高风险软件对象。

        异常：
            ValueError：若未找到记录或入参无效。
        """
        software = self._get_high_risk_software(high_risk_software_ref)

        if usage_status is not None:
            valid_statuses = {"restricted", "prohibited", "approved_with_conditions", "under_review"}
            if usage_status not in valid_statuses:
                raise ValueError(f"Invalid usage_status: {usage_status}")
            software.usage_status = usage_status
        if compliance_status is not None:
            valid_statuses = {"compliant", "non_compliant", "pending_review", "exempted"}
            if compliance_status not in valid_statuses:
                raise ValueError(f"Invalid compliance_status: {compliance_status}")
            software.compliance_status = compliance_status
        if mitigation_measures is not None:
            software.mitigation_measures = mitigation_measures
        if risk_level is not None:
            valid_levels = {"medium", "high", "critical"}
            if risk_level not in valid_levels:
                raise ValueError(f"Invalid risk_level: {risk_level}")
            software.risk_level = risk_level

        software.updated_at = self._now_iso()
        return software

    # ========================================
    # 业务风险（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_business_risk_details(self, business_risk_ref: str) -> LawBusinessRisk:
        """
        根据 ref 获取业务风险详情。

        参数：
            business_risk_ref: 业务风险的唯一标识。

        返回：
            LawBusinessRisk：业务风险对象。

        异常：
            ValueError：若未找到业务风险。
        """
        return self._get_business_risk(business_risk_ref)

    @is_tool(ToolType.READ)
    def list_business_risks(
        self,
        risk_category: Optional[str] = None,
        risk_level: Optional[str] = None,
        risk_status: Optional[str] = None,
        affected_department_ref: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出业务风险（可选筛选）。

        参数：
            risk_category: 按 risk category (market, operational, financial, legal, compliance, strategic, reputational, technology) 筛选。默认 None。
            risk_level: 按 risk level 筛选。默认 None。
            risk_status: 按 risk status 筛选。默认 None。
            affected_department_ref: 按 affected department ref 筛选。默认 None。
            owner_employee_ref: 按 owner employee ref 筛选。默认 None。

        返回：
            str：匹配「business risks」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.law_business_risk.items():
            if risk_category is not None and r.risk_category != risk_category:
                continue
            if risk_level is not None and r.risk_level != risk_level:
                continue
            if risk_status is not None and r.risk_status != risk_status:
                continue
            if affected_department_ref is not None and r.affected_department_ref != affected_department_ref:
                continue
            if owner_employee_ref is not None and r.owner_employee_ref != owner_employee_ref:
                continue
            results.append({
                "business_risk_ref": r.business_risk_ref,
                "risk_title": r.risk_title,
                "risk_category": r.risk_category,
                "risk_level": r.risk_level,
                "risk_status": r.risk_status,
                "probability": r.probability,
                "impact": r.impact,
                "affected_department_ref": r.affected_department_ref,
                "owner_employee_ref": r.owner_employee_ref,
                "identified_at": r.identified_at,
                "review_due_date": r.review_due_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_business_risk(
        self,
        risk_title: str,
        risk_category: str,
        risk_level: str,
        risk_description: str,
        risk_source: str,
        probability: str,
        impact: str,
        mitigation_plan: str,
        contingency_plan: str,
        owner_employee_ref: str,
        affected_department_ref: Optional[str] = None,
    ) -> LawBusinessRisk:
        """
        新建业务风险记录。调用前 Agent 须向用户明确确认。

        参数：
            risk_title: 风险标题。
            risk_category: 类别（market、operational、financial、legal、compliance、strategic、reputational、technology）。
            risk_level: 级别（low、medium、high、critical）。
            risk_description: 详细描述。
            risk_source: 风险来源。
            probability: 概率（low、medium、high、very_high）。
            impact: 影响程度（low、medium、high、critical）。
            mitigation_plan: 缓释计划。
            contingency_plan: 应急预案。
            owner_employee_ref: 风险责任人的员工 ref。
            affected_department_ref: Department ref affected。默认 None。

        返回：
            LawBusinessRisk：新建的业务风险对象。

        异常：
            ValueError：若引用无效或入参格式错误。
        """
        self._get_employee(owner_employee_ref)
        valid_categories = {"market", "operational", "financial", "legal", "compliance", "strategic", "reputational", "technology"}
        if risk_category not in valid_categories:
            raise ValueError(f"Invalid risk_category: {risk_category}")
        valid_levels = {"low", "medium", "high", "critical"}
        if risk_level not in valid_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}")
        valid_probabilities = {"low", "medium", "high", "very_high"}
        if probability not in valid_probabilities:
            raise ValueError(f"Invalid probability: {probability}")
        valid_impacts = {"low", "medium", "high", "critical"}
        if impact not in valid_impacts:
            raise ValueError(f"Invalid impact: {impact}")
        if affected_department_ref:
            self._get_department(affected_department_ref)

        now = self._now_iso()
        ref = self._generate_ref("BRISK", self.db.law_business_risk)

        risk = LawBusinessRisk(
            business_risk_ref=ref,
            risk_title=risk_title,
            risk_category=risk_category,
            risk_level=risk_level,
            risk_description=risk_description,
            risk_source=risk_source,
            affected_department_ref=affected_department_ref,
            probability=probability,
            impact=impact,
            mitigation_plan=mitigation_plan,
            contingency_plan=contingency_plan,
            risk_status="open",
            owner_employee_ref=owner_employee_ref,
            identified_at=now,
            review_due_date=None,
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.law_business_risk[ref] = risk
        return risk

    @is_tool(ToolType.WRITE)
    def update_business_risk_status(
        self,
        business_risk_ref: str,
        new_status: str,
    ) -> LawBusinessRisk:
        """
        更新业务风险状态。调用前 Agent 须向用户明确确认。

        参数：
            business_risk_ref: 业务风险的唯一标识。
            new_status: 新状态（open、mitigating、resolved、accepted、closed）。

        返回：
            LawBusinessRisk：更新后的业务风险对象。

        异常：
            ValueError：若未找到风险或状态无效。
        """
        risk = self._get_business_risk(business_risk_ref)
        valid_statuses = {"open", "mitigating", "resolved", "accepted", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        if new_status == "resolved" and risk.resolved_at is None:
            risk.resolved_at = now
        risk.risk_status = new_status
        risk.updated_at = now
        return risk

    # ========================================
    # 制度/政策（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_policy_details(self, policy_ref: str) -> LawPolicy:
        """
        根据 ref 获取制度详情。

        参数：
            policy_ref: 制度的唯一标识。

        返回：
            LawPolicy：制度对象。

        异常：
            ValueError：若未找到制度。
        """
        return self._get_policy(policy_ref)

    @is_tool(ToolType.READ)
    def search_policies(
        self,
        policy_category: Optional[str] = None,
        policy_scope: Optional[str] = None,
        policy_status: Optional[str] = None,
        scope_department_ref: Optional[str] = None,
        title_keyword: Optional[str] = None,
    ) -> str:
        """
        搜索制度（可选筛选）。

        参数：
            policy_category: 按 policy category (parking, travel, expense, procurement, data_privacy, information_security, hr, compliance, safety, other) 筛选。默认 None。
            policy_scope: 按 policy scope (company_wide, department, team, region) 筛选。默认 None。
            policy_status: 按 policy status (draft, active, expired, superseded, archived) 筛选。默认 None。
            scope_department_ref: 按 scope department ref 筛选。默认 None。
            title_keyword: 按 keyword in policy title (case-insensitive) 筛选。默认 None。

        返回：
            str：匹配「policies」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.law_policy.items():
            if policy_category is not None and p.policy_category != policy_category:
                continue
            if policy_scope is not None and p.policy_scope != policy_scope:
                continue
            if policy_status is not None and p.policy_status != policy_status:
                continue
            if scope_department_ref is not None and p.scope_department_ref != scope_department_ref:
                continue
            if title_keyword is not None and title_keyword.lower() not in p.policy_title.lower():
                continue
            results.append({
                "policy_ref": p.policy_ref,
                "policy_title": p.policy_title,
                "policy_code": p.policy_code,
                "policy_category": p.policy_category,
                "policy_scope": p.policy_scope,
                "policy_status": p.policy_status,
                "version": p.version,
                "effective_date": p.effective_date,
                "expiry_date": p.expiry_date,
                "issued_by_ref": p.issued_by_ref,
                "content": p.content,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_policy_ref_by_title(self, policy_title: str) -> str:
        """
        按标题模糊查找制度 ref（不区分大小写）。

        参数：
            policy_title: 制度标题（可部分匹配）。

        返回：
            str：匹配到的policy 的 policy_ref。

        异常：
            ValueError：若未匹配到制度。
        """
        search = policy_title.lower()
        for ref, p in self.db.law_policy.items():
            if search in p.policy_title.lower():
                return ref
        raise ValueError("Policy not found")

    @is_tool(ToolType.WRITE)
    def update_policy_status(
        self,
        policy_ref: str,
        new_status: str,
    ) -> LawPolicy:
        """
        更新制度状态。调用前 Agent 须向用户明确确认。

        参数：
            policy_ref: 制度的唯一标识。
            new_status: 新状态（draft、active、expired、superseded、archived）。

        返回：
            LawPolicy：更新后的制度对象。

        异常：
            ValueError：若未找到制度或状态无效。
        """
        policy = self._get_policy(policy_ref)
        valid_statuses = {"draft", "active", "expired", "superseded", "archived"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        policy.policy_status = new_status
        policy.updated_at = self._now_iso()
        return policy

    # ========================================
    # 域名资产（读/写）
    # ========================================

    @is_tool(ToolType.READ)
    def get_domain_asset_details(self, domain_asset_ref: str) -> LawDomainAsset:
        """
        根据 ref 获取域名资产详情。

        参数：
            domain_asset_ref: 域名资产的唯一标识。

        返回：
            LawDomainAsset：域名资产对象。

        异常：
            ValueError：若未找到域名资产。
        """
        return self._get_domain_asset(domain_asset_ref)

    @is_tool(ToolType.READ)
    def list_domain_assets(
        self,
        domain_status: Optional[str] = None,
        responsible_employee_ref: Optional[str] = None,
        name_keyword: Optional[str] = None,
    ) -> str:
        """
        列出域名资产（可选筛选）。

        参数：
            domain_status: 按 domain status (active, expired, transferring, suspended, reserved) 筛选。默认 None。
            responsible_employee_ref: 按 responsible employee ref 筛选。默认 None。
            name_keyword: 按 keyword in domain name (case-insensitive) 筛选。默认 None。

        返回：
            str：匹配「domain assets」的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, d in self.db.law_domain_asset.items():
            if domain_status is not None and d.domain_status != domain_status:
                continue
            if responsible_employee_ref is not None and d.responsible_employee_ref != responsible_employee_ref:
                continue
            if name_keyword is not None and name_keyword.lower() not in d.domain_name.lower():
                continue
            results.append({
                "domain_asset_ref": d.domain_asset_ref,
                "domain_name": d.domain_name,
                "registrar": d.registrar,
                "registration_date": d.registration_date,
                "expiry_date": d.expiry_date,
                "auto_renew": d.auto_renew,
                "dns_provider": d.dns_provider,
                "ssl_certificate_expiry": d.ssl_certificate_expiry,
                "domain_status": d.domain_status,
                "responsible_employee_ref": d.responsible_employee_ref,
                "usage_purpose": d.usage_purpose,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_domain_asset_status(
        self,
        domain_asset_ref: str,
        new_status: str,
    ) -> LawDomainAsset:
        """
        更新域名资产状态。调用前 Agent 须向用户明确确认。

        参数：
            domain_asset_ref: 域名资产的唯一标识。
            new_status: 新状态（active、expired、transferring、suspended、reserved）。

        返回：
            LawDomainAsset：更新后的域名资产对象。

        异常：
            ValueError：若未找到域名或状态无效。
        """
        domain = self._get_domain_asset(domain_asset_ref)
        valid_statuses = {"active", "expired", "transferring", "suspended", "reserved"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        domain.domain_status = new_status
        domain.updated_at = self._now_iso()
        return domain

    @is_tool(ToolType.WRITE)
    def update_domain_asset(
        self,
        domain_asset_ref: str,
        auto_renew: Optional[bool] = None,
        dns_provider: Optional[str] = None,
        ssl_certificate_expiry: Optional[str] = None,
        responsible_employee_ref: Optional[str] = None,
        usage_purpose: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> LawDomainAsset:
        """
        更新域名资产详情。调用前 Agent 须向用户明确确认。

        参数：
            domain_asset_ref: 域名资产的唯一标识。
            auto_renew: Whether to auto-renew。默认 None。
            dns_provider: DNS provider。默认 None。
            ssl_certificate_expiry: SSL certificate expiry date (ISO 8601 date)。默认 None。
            responsible_employee_ref: New responsible employee ref。默认 None。
            usage_purpose: Usage purpose。默认 None。
            notes: Additional notes。默认 None。

        返回：
            LawDomainAsset：更新后的域名资产对象。

        异常：
            ValueError：若未找到域名或入参无效。
        """
        domain = self._get_domain_asset(domain_asset_ref)

        if auto_renew is not None:
            domain.auto_renew = auto_renew
        if dns_provider is not None:
            domain.dns_provider = dns_provider
        if ssl_certificate_expiry is not None:
            domain.ssl_certificate_expiry = ssl_certificate_expiry
        if responsible_employee_ref is not None:
            self._get_employee(responsible_employee_ref)
            domain.responsible_employee_ref = responsible_employee_ref
        if usage_purpose is not None:
            domain.usage_purpose = usage_purpose
        if notes is not None:
            domain.notes = notes

        domain.updated_at = self._now_iso()
        return domain