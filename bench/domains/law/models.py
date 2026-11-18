from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

ContractCategory = Literal[
    "sales", "procurement", "service", "lease", "employment",
    "nda", "partnership", "licensing", "construction", "other"
]
ContractTemplateStatus = Literal["active", "inactive", "deprecated"]
ContractPartyType = Literal["enterprise", "individual", "government", "ngo"]
ContractPartyStatus = Literal["active", "inactive", "blacklisted"]
ContractPartyRiskLevel = Literal["low", "medium", "high", "critical"]
ContractType = Literal["standard", "framework", "supplementary", "renewal"]
ContractStatus = Literal[
    "draft", "pending_approval", "approved", "signed", "active",
    "suspended", "expired", "terminated", "cancelled"
]
ContractRiskLevel = Literal["low", "medium", "high", "critical"]
Currency = Literal["CNY", "USD", "EUR", "GBP", "JPY", "HKD"]
PartyRole = Literal["party_a", "party_b", "party_c", "guarantor", "witness"]
SigningStatus = Literal["pending", "signed", "rejected"]
AmendmentType = Literal["modification", "supplement", "renewal", "termination"]
AmendmentStatus = Literal["draft", "pending_approval", "approved", "rejected", "effective"]
TransferType = Literal["owner_change", "department_change", "both"]
TransferStatus = Literal["pending", "approved", "rejected", "completed"]
MilestoneType = Literal["payment", "delivery", "review", "acceptance", "other"]
MilestoneStatus = Literal["pending", "in_progress", "completed", "overdue", "cancelled"]
ContractRiskCategory = Literal["legal", "financial", "operational", "compliance", "reputational"]
ContractRiskStatus = Literal["open", "mitigating", "resolved", "accepted", "closed"]
ContractLoanStatus = Literal["pending", "approved", "borrowed", "returned", "overdue", "rejected"]
ApprovalFlowSubjectType = Literal[
    "contract", "amendment", "seal_usage", "ip_application",
    "license_usage", "entity_change", "other"
]
ApprovalFlowType = Literal[
    "contract_approval", "amendment_approval", "seal_approval",
    "ip_approval", "license_approval", "entity_change_approval", "general"
]
ApprovalFlowStatus = Literal["in_progress", "approved", "rejected", "cancelled", "withdrawn"]
ApprovalStepStatus = Literal["pending", "approved", "rejected", "skipped"]
ApprovalDecision = Literal["approve", "reject", "abstain"]
SealType = Literal["corporate", "contract", "finance", "legal", "hr", "custom"]
SealStatus = Literal["active", "inactive", "destroyed"]
SealUsageType = Literal["contract", "certificate", "letter", "report", "other"]
SealUsageRequestStatus = Literal["pending", "approved", "rejected", "used", "cancelled"]
IPType = Literal["patent", "trademark", "copyright", "trade_secret", "domain", "other"]
IPStatus = Literal["active", "pending", "expired", "abandoned", "transferred"]
IPOwnerType = Literal["company", "employee", "joint"]
IPInventorRole = Literal["primary", "co_inventor", "contributor"]
IPApplicationType = Literal["new_registration", "renewal", "change", "transfer", "opposition"]
IPApplicationStatus = Literal[
    "drafting", "internal_review", "submitted", "under_examination",
    "accepted", "granted", "rejected", "withdrawn"
]
IPAuthorizationType = Literal["license", "assignment", "pledge", "cross_license"]
IPAuthorizationStatus = Literal["active", "expired", "terminated", "pending"]
IPRewardType = Literal["application_bonus", "grant_bonus", "commercialization_bonus", "annual_award"]
IPRewardStatus = Literal["pending", "approved", "paid", "rejected"]
IntegrityDeclarationType = Literal["commitment", "conflict_of_interest", "gift_disclosure", "annual_review"]
IntegrityDeclarationStatus = Literal["draft", "submitted", "under_review", "approved", "rejected", "returned"]
IntegrityReviewResult = Literal["pass", "fail", "conditional_pass"]
ViolationType = Literal[
    "bribery", "conflict_of_interest", "fraud", "embezzlement",
    "data_breach", "policy_violation", "harassment", "other"
]
ViolationReportStatus = Literal[
    "submitted", "under_investigation", "substantiated",
    "unsubstantiated", "closed", "dismissed"
]
ViolationSeverity = Literal["low", "medium", "high", "critical"]
LegalCaseType = Literal["litigation", "arbitration", "administrative", "mediation"]
LegalCaseCategory = Literal[
    "contract_dispute", "ip_infringement", "labor_dispute",
    "tort", "regulatory", "other"
]
OurRole = Literal["plaintiff", "defendant", "applicant", "respondent", "third_party"]
LegalCaseStatus = Literal[
    "filed", "in_progress", "hearing", "awaiting_judgment",
    "won", "lost", "settled", "withdrawn", "closed"
]
CaseEventType = Literal[
    "hearing", "filing", "evidence_submission", "mediation",
    "judgment", "appeal", "settlement", "other"
]
EvidenceType = Literal["document", "electronic", "physical", "testimony", "expert_opinion", "other"]
EvidenceNotarizationStatus = Literal["none", "pending", "notarized"]
EvidenceStatus = Literal["active", "archived", "withdrawn"]
EvidenceRelatedResourceType = Literal["legal_case", "violation_report", "contract", "other"]
ConsultationType = Literal[
    "contract_review", "compliance_advice", "ip_consultation",
    "labor_law", "regulatory", "general"
]
ConsultationChannel = Literal["service_desk", "email", "phone", "meeting", "im"]
ConsultationUrgency = Literal["low", "normal", "high", "urgent"]
ConsultationStatus = Literal["open", "assigned", "in_progress", "resolved", "closed"]
ComplianceReviewType = Literal[
    "business_compliance", "data_privacy", "export_control",
    "anti_corruption", "environmental", "general"
]
ComplianceReviewStatus = Literal["planned", "in_progress", "completed", "cancelled"]
ComplianceReviewResult = Literal["compliant", "non_compliant", "partially_compliant"]
CorporateEntityType = Literal["subsidiary", "branch", "joint_venture", "holding", "representative_office"]
CorporateEntityStatus = Literal["active", "inactive", "dissolved", "merging", "liquidating"]
EntityChangeType = Literal[
    "name_change", "address_change", "capital_change", "scope_change",
    "representative_change", "shareholder_change", "other"
]
EntityChangeStatus = Literal["pending", "approved", "rejected", "completed", "cancelled"]
QualificationCertificateType = Literal[
    "business_license", "tax_registration", "safety_permit",
    "quality_certification", "industry_license", "professional_license", "other"
]
CertificateHolderType = Literal["company", "employee"]
CertificateStatus = Literal["active", "expired", "revoked", "pending_renewal"]
LicenseUsageType = Literal["original", "copy", "scan"]
LicenseUsageRequestStatus = Literal["pending", "approved", "rejected", "borrowed", "returned", "overdue"]
RelatedPartyType = Literal["enterprise", "individual", "government"]
RelationshipType = Literal[
    "shareholder", "subsidiary", "affiliate", "key_personnel",
    "family_member", "business_partner", "other"
]
RelatedPartyStatus = Literal["active", "inactive", "under_review"]
RelatedPartyRiskLevel = Literal["low", "medium", "high", "critical"]
RelatedPartyTransactionType = Literal[
    "procurement", "sales", "service", "lease", "loan",
    "guarantee", "asset_transfer", "other"
]
RelatedPartyComplianceStatus = Literal["pending_review", "approved", "rejected", "flagged"]
InnovationProposalCategory = Literal[
    "product", "process", "technology", "management", "service", "other"
]
InnovationProposalStatus = Literal[
    "submitted", "under_review", "approved", "rejected",
    "in_progress", "completed", "archived"
]
SupplierAssessmentType = Literal["qualification", "annual_review", "incident_review", "exit_review"]
SupplierAssessmentStatus = Literal["planned", "in_progress", "completed", "cancelled"]
SupplierRiskLevel = Literal["low", "medium", "high", "critical"]
HighRiskSoftwareRiskLevel = Literal["medium", "high", "critical"]
HighRiskSoftwareRiskCategory = Literal[
    "security_vulnerability", "license_violation", "data_leakage",
    "compliance_issue", "supply_chain_risk", "other"
]
HighRiskSoftwareUsageStatus = Literal["restricted", "prohibited", "approved_with_conditions", "under_review"]
HighRiskSoftwareComplianceStatus = Literal["compliant", "non_compliant", "pending_review", "exempted"]
BusinessRiskCategory = Literal[
    "market", "operational", "financial", "legal",
    "compliance", "strategic", "reputational", "technology"
]
BusinessRiskLevel = Literal["low", "medium", "high", "critical"]
BusinessRiskProbability = Literal["low", "medium", "high", "very_high"]
BusinessRiskImpact = Literal["low", "medium", "high", "critical"]
BusinessRiskStatus = Literal["open", "mitigating", "resolved", "accepted", "closed"]
PolicyCategory = Literal[
    "parking", "travel", "expense", "procurement", "data_privacy",
    "information_security", "hr", "compliance", "safety", "other"
]
PolicyScope = Literal["company_wide", "department", "team", "region"]
PolicyStatus = Literal["draft", "active", "expired", "superseded", "archived"]
DomainStatus = Literal["active", "expired", "transferring", "suspended", "reserved"]


# --- Models ---


class LawContractTemplate(BaseModel):
    """Represents a contract template used for generating standardized contracts"""

    contract_template_ref: str = Field(description="Unique identifier for the contract template")
    template_name: str = Field(description="Name of the contract template")
    template_code: str = Field(description="Short code for the contract template")
    contract_category: ContractCategory = Field(
        description="Category of contracts this template applies to (sales, procurement, service, lease, employment, nda, partnership, licensing, construction, other)"
    )
    template_version: str = Field(description="Version string of the template (e.g., 1.0, 2.1)")
    template_content: str = Field(description="Content or body of the contract template")
    template_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the template document, null if not uploaded",
        default=None,
    )
    template_status: ContractTemplateStatus = Field(
        description="Current status of the template (active, inactive, deprecated)"
    )
    created_by_ref: str = Field(description="Employee reference of the template creator")
    created_at: str = Field(description="Timestamp when the template was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the template was last updated (ISO 8601)")


class LawContractParty(BaseModel):
    """Represents an external party that can be involved in contracts"""

    contract_party_ref: str = Field(description="Unique identifier for the contract party")
    party_name: str = Field(description="Name of the contract party")
    party_type: ContractPartyType = Field(
        description="Type of party (enterprise, individual, government, ngo)"
    )
    unified_social_credit_code: str = Field(
        description="Unified social credit code for enterprise parties"
    )
    legal_representative: str = Field(description="Name of the legal representative")
    registered_address: str = Field(description="Registered address of the party")
    contact_name: str = Field(description="Name of the primary contact person")
    contact_phone: str = Field(description="Phone number of the primary contact person")
    contact_email: str = Field(description="Email address of the primary contact person")
    bank_name: str = Field(description="Name of the party's bank")
    bank_account: str = Field(description="Bank account number of the party")
    party_status: ContractPartyStatus = Field(
        description="Current status of the party (active, inactive, blacklisted)"
    )
    risk_level: ContractPartyRiskLevel = Field(
        description="Risk level assessment of the party (low, medium, high, critical)"
    )
    notes: str = Field(description="Additional notes about the contract party")
    created_at: str = Field(description="Timestamp when the party record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the party record was last updated (ISO 8601)")


class LawContract(BaseModel):
    """Represents a legal contract with financial details, lifecycle status and ownership"""

    contract_ref: str = Field(description="Unique identifier for the contract")
    contract_number: str = Field(description="Human-readable contract number")
    contract_title: str = Field(description="Title of the contract")
    contract_category: ContractCategory = Field(
        description="Category of the contract (sales, procurement, service, lease, employment, nda, partnership, licensing, construction, other)"
    )
    contract_type: ContractType = Field(
        description="Type of contract (standard, framework, supplementary, renewal)"
    )
    template_ref: Optional[str] = Field(
        description="Reference to the contract template used, null if not based on a template",
        default=None,
    )
    parent_contract_ref: Optional[str] = Field(
        description="Reference to the parent contract, null if this is a standalone contract",
        default=None,
    )
    our_entity_ref: Optional[str] = Field(
        description="Reference to our corporate entity that is party to this contract, null if not specified",
        default=None,
    )
    currency: Currency = Field(
        description="Currency of the contract amount (CNY, USD, EUR, GBP, JPY, HKD)"
    )
    total_amount: float = Field(description="Total monetary amount of the contract")
    effective_date: str = Field(description="Date when the contract becomes effective (ISO 8601 date)")
    expiry_date: str = Field(description="Date when the contract expires (ISO 8601 date)")
    signing_date: Optional[str] = Field(
        description="Date when the contract was signed, null if not yet signed (ISO 8601 date)",
        default=None,
    )
    termination_date: Optional[str] = Field(
        description="Date when the contract was terminated, null if not terminated (ISO 8601 date)",
        default=None,
    )
    contract_status: ContractStatus = Field(
        description="Current status of the contract (draft, pending_approval, approved, signed, active, suspended, expired, terminated, cancelled)"
    )
    risk_level: ContractRiskLevel = Field(
        description="Risk level of the contract (low, medium, high, critical)"
    )
    owner_employee_ref: str = Field(
        description="Employee reference of the contract owner"
    )
    department_ref: str = Field(
        description="Reference to the department responsible for the contract"
    )
    contract_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the contract document, null if not uploaded",
        default=None,
    )
    summary: str = Field(description="Summary description of the contract")
    special_terms: str = Field(description="Special terms and conditions of the contract")
    created_at: str = Field(description="Timestamp when the contract was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the contract was last updated (ISO 8601)")


class LawContractPartyLink(BaseModel):
    """Represents the link between a contract and a contract party with role and signing status"""

    contract_party_link_ref: str = Field(description="Unique identifier for the contract-party link")
    contract_ref: str = Field(description="Reference to the contract")
    contract_party_ref: str = Field(description="Reference to the contract party")
    party_role: PartyRole = Field(
        description="Role of the party in the contract (party_a, party_b, party_c, guarantor, witness)"
    )
    signing_status: SigningStatus = Field(
        description="Signing status of the party (pending, signed, rejected)"
    )
    signed_at: Optional[str] = Field(
        description="Timestamp when the party signed, null if not yet signed (ISO 8601)",
        default=None,
    )
    signer_name: str = Field(description="Name of the person who signed on behalf of the party")
    created_at: str = Field(description="Timestamp when the link was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the link was last updated (ISO 8601)")


class LawContractAmendment(BaseModel):
    """Represents an amendment or modification to an existing contract"""

    contract_amendment_ref: str = Field(description="Unique identifier for the contract amendment")
    contract_ref: str = Field(description="Reference to the contract being amended")
    amendment_type: AmendmentType = Field(
        description="Type of amendment (modification, supplement, renewal, termination)"
    )
    amendment_number: str = Field(description="Human-readable amendment number")
    amendment_title: str = Field(description="Title of the amendment")
    reason: str = Field(description="Reason for the amendment")
    changes_summary: str = Field(description="Summary of the changes made by this amendment")
    amount_change: float = Field(description="Change in contract amount, positive for increase, negative for decrease")
    new_expiry_date: Optional[str] = Field(
        description="New expiry date if the amendment changes the contract duration, null otherwise (ISO 8601 date)",
        default=None,
    )
    amendment_status: AmendmentStatus = Field(
        description="Current status of the amendment (draft, pending_approval, approved, rejected, effective)"
    )
    amendment_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the amendment document, null if not uploaded",
        default=None,
    )
    initiated_by_ref: str = Field(description="Employee reference of the person who initiated the amendment")
    effective_date: Optional[str] = Field(
        description="Date when the amendment becomes effective, null if not yet effective (ISO 8601 date)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the amendment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the amendment was last updated (ISO 8601)")


class LawContractTransfer(BaseModel):
    """Represents a transfer of contract ownership or departmental responsibility"""

    contract_transfer_ref: str = Field(description="Unique identifier for the contract transfer")
    contract_ref: str = Field(description="Reference to the contract being transferred")
    transfer_type: TransferType = Field(
        description="Type of transfer (owner_change, department_change, both)"
    )
    from_employee_ref: str = Field(description="Employee reference of the current owner")
    to_employee_ref: str = Field(description="Employee reference of the new owner")
    from_department_ref: Optional[str] = Field(
        description="Reference to the current department, null if not a department transfer",
        default=None,
    )
    to_department_ref: Optional[str] = Field(
        description="Reference to the new department, null if not a department transfer",
        default=None,
    )
    reason: str = Field(description="Reason for the transfer")
    transfer_status: TransferStatus = Field(
        description="Current status of the transfer (pending, approved, rejected, completed)"
    )
    transferred_at: Optional[str] = Field(
        description="Timestamp when the transfer was completed, null if not yet completed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the transfer was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the transfer was last updated (ISO 8601)")


class LawContractMilestone(BaseModel):
    """Represents a milestone or key deliverable within a contract"""

    contract_milestone_ref: str = Field(description="Unique identifier for the contract milestone")
    contract_ref: str = Field(description="Reference to the contract")
    milestone_title: str = Field(description="Title of the milestone")
    milestone_type: MilestoneType = Field(
        description="Type of milestone (payment, delivery, review, acceptance, other)"
    )
    due_date: str = Field(description="Due date for the milestone (ISO 8601 date)")
    completed_date: Optional[str] = Field(
        description="Date when the milestone was completed, null if not yet completed (ISO 8601 date)",
        default=None,
    )
    amount: float = Field(description="Monetary amount associated with the milestone")
    milestone_status: MilestoneStatus = Field(
        description="Current status of the milestone (pending, in_progress, completed, overdue, cancelled)"
    )
    responsible_employee_ref: str = Field(
        description="Employee reference of the person responsible for the milestone"
    )
    description: str = Field(description="Description of the milestone")
    created_at: str = Field(description="Timestamp when the milestone was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the milestone was last updated (ISO 8601)")


class LawContractRisk(BaseModel):
    """Represents an identified risk associated with a contract"""

    contract_risk_ref: str = Field(description="Unique identifier for the contract risk")
    contract_ref: str = Field(description="Reference to the contract")
    risk_title: str = Field(description="Title of the risk")
    risk_category: ContractRiskCategory = Field(
        description="Category of the risk (legal, financial, operational, compliance, reputational)"
    )
    risk_level: ContractRiskLevel = Field(
        description="Level of the risk (low, medium, high, critical)"
    )
    risk_description: str = Field(description="Detailed description of the risk")
    affected_clause: str = Field(description="Contract clause affected by the risk")
    mitigation_plan: str = Field(description="Plan to mitigate the risk")
    risk_status: ContractRiskStatus = Field(
        description="Current status of the risk (open, mitigating, resolved, accepted, closed)"
    )
    identified_by_ref: str = Field(description="Employee reference of the person who identified the risk")
    identified_at: str = Field(description="Timestamp when the risk was identified (ISO 8601)")
    resolved_at: Optional[str] = Field(
        description="Timestamp when the risk was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the risk record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the risk record was last updated (ISO 8601)")


class LawContractLoan(BaseModel):
    """Represents a loan or borrowing record for a physical contract document"""

    contract_loan_ref: str = Field(description="Unique identifier for the contract loan")
    contract_ref: str = Field(description="Reference to the contract being borrowed")
    borrower_employee_ref: str = Field(description="Employee reference of the borrower")
    loan_purpose: str = Field(description="Purpose of borrowing the contract document")
    loan_status: ContractLoanStatus = Field(
        description="Current status of the loan (pending, approved, borrowed, returned, overdue, rejected)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who approved the loan, null if not yet approved",
        default=None,
    )
    borrowed_at: Optional[str] = Field(
        description="Timestamp when the contract was borrowed, null if not yet borrowed (ISO 8601)",
        default=None,
    )
    due_return_at: Optional[str] = Field(
        description="Timestamp when the contract is due to be returned, null if not yet set (ISO 8601)",
        default=None,
    )
    returned_at: Optional[str] = Field(
        description="Timestamp when the contract was returned, null if not yet returned (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the loan record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the loan record was last updated (ISO 8601)")


class LawApprovalFlow(BaseModel):
    """Represents an approval workflow for legal-related subjects"""

    approval_flow_ref: str = Field(description="Unique identifier for the approval flow")
    subject_type: ApprovalFlowSubjectType = Field(
        description="Type of subject being approved (contract, amendment, seal_usage, ip_application, license_usage, entity_change, other)"
    )
    subject_ref: str = Field(description="Reference to the subject being approved")
    flow_title: str = Field(description="Title of the approval flow")
    flow_type: ApprovalFlowType = Field(
        description="Type of approval flow (contract_approval, amendment_approval, seal_approval, ip_approval, license_approval, entity_change_approval, general)"
    )
    flow_status: ApprovalFlowStatus = Field(
        description="Current status of the approval flow (in_progress, approved, rejected, cancelled, withdrawn)"
    )
    initiated_by_ref: str = Field(description="Employee reference of the person who initiated the flow")
    current_step: int = Field(description="Current step number in the approval flow")
    total_steps: int = Field(description="Total number of steps in the approval flow")
    initiated_at: str = Field(description="Timestamp when the approval flow was initiated (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the approval flow was completed, null if still in progress (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the approval flow was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the approval flow was last updated (ISO 8601)")


class LawApprovalStep(BaseModel):
    """Represents a single step within an approval flow"""

    approval_step_ref: str = Field(description="Unique identifier for the approval step")
    approval_flow_ref: str = Field(description="Reference to the parent approval flow")
    step_order: int = Field(description="Order of this step within the approval flow")
    step_name: str = Field(description="Name of the approval step")
    approver_employee_ref: str = Field(description="Employee reference of the approver for this step")
    step_status: ApprovalStepStatus = Field(
        description="Current status of the step (pending, approved, rejected, skipped)"
    )
    decision: Optional[ApprovalDecision] = Field(
        description="Decision made by the approver (approve, reject, abstain), null if not yet decided",
        default=None,
    )
    comments: str = Field(description="Comments provided by the approver")
    decided_at: Optional[str] = Field(
        description="Timestamp when the decision was made, null if not yet decided (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the step was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the step was last updated (ISO 8601)")


class LawSeal(BaseModel):
    """Represents a corporate seal managed by the legal department"""

    seal_ref: str = Field(description="Unique identifier for the seal")
    seal_name: str = Field(description="Name of the seal")
    seal_type: SealType = Field(
        description="Type of seal (corporate, contract, finance, legal, hr, custom)"
    )
    seal_code: str = Field(description="Short code for the seal")
    custodian_employee_ref: str = Field(description="Employee reference of the seal custodian")
    department_ref: str = Field(description="Reference to the department that owns the seal")
    seal_status: SealStatus = Field(
        description="Current status of the seal (active, inactive, destroyed)"
    )
    description: str = Field(description="Description of the seal and its usage")
    created_at: str = Field(description="Timestamp when the seal record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the seal record was last updated (ISO 8601)")


class LawSealUsageRequest(BaseModel):
    """Represents a request to use a corporate seal on a document"""

    seal_usage_request_ref: str = Field(description="Unique identifier for the seal usage request")
    seal_ref: str = Field(description="Reference to the seal being requested")
    applicant_employee_ref: str = Field(description="Employee reference of the applicant")
    usage_type: SealUsageType = Field(
        description="Type of usage (contract, certificate, letter, report, other)"
    )
    related_resource_type: str = Field(
        description="Type of the related resource (e.g., contract, certificate, letter)"
    )
    related_resource_ref: str = Field(description="Reference to the related resource")
    document_title: str = Field(description="Title of the document to be stamped")
    usage_purpose: str = Field(description="Purpose of using the seal")
    copies_count: int = Field(description="Number of copies to be stamped")
    request_status: SealUsageRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, used, cancelled)"
    )
    used_at: Optional[str] = Field(
        description="Timestamp when the seal was used, null if not yet used (ISO 8601)",
        default=None,
    )
    document_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the document to be stamped, null if not uploaded",
        default=None,
    )
    stamped_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the stamped document, null if not yet stamped",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the request was last updated (ISO 8601)")


class LawIPAsset(BaseModel):
    """Represents an intellectual property asset owned or managed by the organization"""

    ip_asset_ref: str = Field(description="Unique identifier for the IP asset")
    ip_type: IPType = Field(
        description="Type of intellectual property (patent, trademark, copyright, trade_secret, domain, other)"
    )
    ip_name: str = Field(description="Name of the IP asset")
    ip_number: str = Field(description="Internal IP number or identifier")
    registration_number: str = Field(description="Official registration number")
    ip_status: IPStatus = Field(
        description="Current status of the IP asset (active, pending, expired, abandoned, transferred)"
    )
    application_date: Optional[str] = Field(
        description="Date when the IP application was filed, null if not applicable (ISO 8601 date)",
        default=None,
    )
    grant_date: Optional[str] = Field(
        description="Date when the IP was granted, null if not yet granted (ISO 8601 date)",
        default=None,
    )
    expiry_date: Optional[str] = Field(
        description="Date when the IP expires, null if no expiry (ISO 8601 date)",
        default=None,
    )
    owner_type: IPOwnerType = Field(
        description="Type of IP owner (company, employee, joint)"
    )
    owner_entity_ref: Optional[str] = Field(
        description="Reference to the corporate entity that owns the IP, null if not applicable",
        default=None,
    )
    responsible_employee_ref: str = Field(
        description="Employee reference of the person responsible for managing the IP"
    )
    department_ref: str = Field(description="Reference to the department associated with the IP")
    ip_class: str = Field(description="Classification of the IP (e.g., IPC class for patents)")
    description: str = Field(description="Description of the IP asset")
    certificate_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the IP certificate, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the IP asset record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the IP asset record was last updated (ISO 8601)")


class LawIPInventor(BaseModel):
    """Represents an inventor or contributor associated with an IP asset"""

    ip_inventor_ref: str = Field(description="Unique identifier for the IP inventor record")
    ip_asset_ref: str = Field(description="Reference to the IP asset")
    employee_ref: str = Field(description="Reference to the employee who is the inventor")
    inventor_role: IPInventorRole = Field(
        description="Role of the inventor (primary, co_inventor, contributor)"
    )
    contribution_ratio: float = Field(description="Contribution ratio as a percentage (e.g., 50.00)")
    created_at: str = Field(description="Timestamp when the inventor record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the inventor record was last updated (ISO 8601)")


class LawIPApplication(BaseModel):
    """Represents an application process for an IP asset"""

    ip_application_ref: str = Field(description="Unique identifier for the IP application")
    ip_asset_ref: str = Field(description="Reference to the IP asset being applied for")
    application_type: IPApplicationType = Field(
        description="Type of application (new_registration, renewal, change, transfer, opposition)"
    )
    applicant_employee_ref: str = Field(description="Employee reference of the applicant")
    agency_name: str = Field(description="Name of the IP agency handling the application")
    application_status: IPApplicationStatus = Field(
        description="Current status of the application (drafting, internal_review, submitted, under_examination, accepted, granted, rejected, withdrawn)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the application was submitted, null if not yet submitted (ISO 8601)",
        default=None,
    )
    accepted_at: Optional[str] = Field(
        description="Timestamp when the application was accepted, null if not yet accepted (ISO 8601)",
        default=None,
    )
    granted_at: Optional[str] = Field(
        description="Timestamp when the IP was granted, null if not yet granted (ISO 8601)",
        default=None,
    )
    rejected_at: Optional[str] = Field(
        description="Timestamp when the application was rejected, null if not rejected (ISO 8601)",
        default=None,
    )
    rejection_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    application_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the application document, null if not uploaded",
        default=None,
    )
    estimated_cost: float = Field(description="Estimated cost of the application")
    actual_cost: float = Field(description="Actual cost incurred for the application")
    notes: str = Field(description="Additional notes about the application")
    created_at: str = Field(description="Timestamp when the application record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the application record was last updated (ISO 8601)")


class LawIPAuthorization(BaseModel):
    """Represents an authorization or license granted for an IP asset"""

    ip_authorization_ref: str = Field(description="Unique identifier for the IP authorization")
    ip_asset_ref: str = Field(description="Reference to the IP asset being authorized")
    authorization_type: IPAuthorizationType = Field(
        description="Type of authorization (license, assignment, pledge, cross_license)"
    )
    licensee_name: str = Field(description="Name of the licensee or authorized party")
    licensee_party_ref: Optional[str] = Field(
        description="Reference to the contract party who is the licensee, null if not linked",
        default=None,
    )
    scope: str = Field(description="Scope of the authorization")
    territory: str = Field(description="Geographic territory covered by the authorization")
    exclusive: bool = Field(description="Whether the authorization is exclusive")
    effective_date: str = Field(description="Date when the authorization becomes effective (ISO 8601 date)")
    expiry_date: str = Field(description="Date when the authorization expires (ISO 8601 date)")
    fee: float = Field(description="Fee or royalty amount for the authorization")
    authorization_status: IPAuthorizationStatus = Field(
        description="Current status of the authorization (active, expired, terminated, pending)"
    )
    contract_ref: Optional[str] = Field(
        description="Reference to the related contract, null if not linked to a contract",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the authorization was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the authorization was last updated (ISO 8601)")


class LawIPReward(BaseModel):
    """Represents a reward or bonus granted to an employee for IP contributions"""

    ip_reward_ref: str = Field(description="Unique identifier for the IP reward")
    ip_asset_ref: str = Field(description="Reference to the IP asset")
    employee_ref: str = Field(description="Reference to the employee receiving the reward")
    reward_type: IPRewardType = Field(
        description="Type of reward (application_bonus, grant_bonus, commercialization_bonus, annual_award)"
    )
    reward_amount: float = Field(description="Monetary amount of the reward")
    reward_status: IPRewardStatus = Field(
        description="Current status of the reward (pending, approved, paid, rejected)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who approved the reward, null if not yet approved",
        default=None,
    )
    paid_at: Optional[str] = Field(
        description="Timestamp when the reward was paid, null if not yet paid (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the reward")
    created_at: str = Field(description="Timestamp when the reward record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the reward record was last updated (ISO 8601)")


class LawIntegrityDeclaration(BaseModel):
    """Represents an integrity or compliance declaration submitted by an employee"""

    integrity_declaration_ref: str = Field(description="Unique identifier for the integrity declaration")
    employee_ref: str = Field(description="Reference to the employee making the declaration")
    declaration_type: IntegrityDeclarationType = Field(
        description="Type of declaration (commitment, conflict_of_interest, gift_disclosure, annual_review)"
    )
    declaration_period: str = Field(description="Period covered by the declaration (e.g., 2025, 2025-Q1)")
    declaration_content: Dict[str, Any] = Field(
        description="Structured content of the declaration as key-value pairs"
    )
    declaration_status: IntegrityDeclarationStatus = Field(
        description="Current status of the declaration (draft, submitted, under_review, approved, rejected, returned)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the declaration was submitted, null if not yet submitted (ISO 8601)",
        default=None,
    )
    reviewed_by_ref: Optional[str] = Field(
        description="Employee reference of the reviewer, null if not yet reviewed",
        default=None,
    )
    reviewed_at: Optional[str] = Field(
        description="Timestamp when the declaration was reviewed, null if not yet reviewed (ISO 8601)",
        default=None,
    )
    review_result: Optional[IntegrityReviewResult] = Field(
        description="Result of the review (pass, fail, conditional_pass), null if not yet reviewed",
        default=None,
    )
    review_comments: str = Field(description="Comments from the reviewer")
    declaration_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the declaration document, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the declaration was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the declaration was last updated (ISO 8601)")


class LawViolationReport(BaseModel):
    """Represents a report of a compliance or integrity violation"""

    violation_report_ref: str = Field(description="Unique identifier for the violation report")
    reporter_employee_ref: Optional[str] = Field(
        description="Employee reference of the reporter, null if anonymous",
        default=None,
    )
    is_anonymous: bool = Field(description="Whether the report was submitted anonymously")
    violation_type: ViolationType = Field(
        description="Type of violation (bribery, conflict_of_interest, fraud, embezzlement, data_breach, policy_violation, harassment, other)"
    )
    reported_employee_ref: Optional[str] = Field(
        description="Employee reference of the person being reported, null if not specific",
        default=None,
    )
    reported_department_ref: Optional[str] = Field(
        description="Department reference of the department being reported, null if not specific",
        default=None,
    )
    title: str = Field(description="Title of the violation report")
    description: str = Field(description="Detailed description of the violation")
    occurred_at: str = Field(description="Timestamp when the violation occurred (ISO 8601)")
    evidence_summary: str = Field(description="Summary of evidence supporting the report")
    report_status: ViolationReportStatus = Field(
        description="Current status of the report (submitted, under_investigation, substantiated, unsubstantiated, closed, dismissed)"
    )
    severity: ViolationSeverity = Field(
        description="Severity of the violation (low, medium, high, critical)"
    )
    investigator_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned investigator, null if not yet assigned",
        default=None,
    )
    investigation_result: Optional[str] = Field(
        description="Result of the investigation, null if not yet concluded",
        default=None,
    )
    investigation_notes: str = Field(description="Notes from the investigation")
    closed_at: Optional[str] = Field(
        description="Timestamp when the report was closed, null if still open (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the report was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the report was last updated (ISO 8601)")


class LawLegalCase(BaseModel):
    """Represents a legal case or dispute involving the organization"""

    legal_case_ref: str = Field(description="Unique identifier for the legal case")
    case_number: str = Field(description="Official case number assigned by the court or institution")
    case_title: str = Field(description="Title of the legal case")
    case_type: LegalCaseType = Field(
        description="Type of case (litigation, arbitration, administrative, mediation)"
    )
    case_category: LegalCaseCategory = Field(
        description="Category of the case (contract_dispute, ip_infringement, labor_dispute, tort, regulatory, other)"
    )
    our_role: OurRole = Field(
        description="Our role in the case (plaintiff, defendant, applicant, respondent, third_party)"
    )
    counterparty_name: str = Field(description="Name of the counterparty in the case")
    counterparty_party_ref: Optional[str] = Field(
        description="Reference to the contract party representing the counterparty, null if not linked",
        default=None,
    )
    court_or_institution: str = Field(description="Name of the court or arbitration institution")
    jurisdiction: str = Field(description="Jurisdiction of the case")
    filing_date: Optional[str] = Field(
        description="Date when the case was filed, null if not yet filed (ISO 8601 date)",
        default=None,
    )
    hearing_date: Optional[str] = Field(
        description="Date of the next hearing, null if not scheduled (ISO 8601 date)",
        default=None,
    )
    claim_amount: float = Field(description="Amount claimed in the case")
    case_status: LegalCaseStatus = Field(
        description="Current status of the case (filed, in_progress, hearing, awaiting_judgment, won, lost, settled, withdrawn, closed)"
    )
    risk_level: ContractRiskLevel = Field(
        description="Risk level of the case (low, medium, high, critical)"
    )
    responsible_employee_ref: str = Field(
        description="Employee reference of the person responsible for the case"
    )
    external_counsel: str = Field(description="Name or firm of the external legal counsel")
    related_contract_ref: Optional[str] = Field(
        description="Reference to a related contract, null if not linked",
        default=None,
    )
    outcome: Optional[str] = Field(
        description="Outcome of the case, null if not yet concluded",
        default=None,
    )
    outcome_summary: str = Field(description="Summary of the case outcome")
    settlement_amount: Optional[float] = Field(
        description="Settlement amount if the case was settled, null otherwise",
        default=None,
    )
    closed_at: Optional[str] = Field(
        description="Timestamp when the case was closed, null if still open (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the case")
    created_at: str = Field(description="Timestamp when the case record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the case record was last updated (ISO 8601)")


class LawCaseEvent(BaseModel):
    """Represents an event or proceeding within a legal case"""

    case_event_ref: str = Field(description="Unique identifier for the case event")
    legal_case_ref: str = Field(description="Reference to the legal case")
    event_type: CaseEventType = Field(
        description="Type of event (hearing, filing, evidence_submission, mediation, judgment, appeal, settlement, other)"
    )
    event_title: str = Field(description="Title of the event")
    event_date: str = Field(description="Date and time of the event (ISO 8601)")
    description: str = Field(description="Description of the event")
    outcome: str = Field(description="Outcome of the event")
    document_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for event documents, null if not uploaded",
        default=None,
    )
    recorded_by_ref: str = Field(description="Employee reference of the person who recorded the event")
    created_at: str = Field(description="Timestamp when the event record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the event record was last updated (ISO 8601)")


class LawEvidence(BaseModel):
    """Represents a piece of evidence associated with a legal case or investigation"""

    evidence_ref: str = Field(description="Unique identifier for the evidence")
    related_resource_type: EvidenceRelatedResourceType = Field(
        description="Type of the related resource (legal_case, violation_report, contract, other)"
    )
    related_resource_ref: str = Field(description="Reference to the related resource")
    evidence_title: str = Field(description="Title of the evidence")
    evidence_type: EvidenceType = Field(
        description="Type of evidence (document, electronic, physical, testimony, expert_opinion, other)"
    )
    evidence_description: str = Field(description="Description of the evidence")
    file_attachment_ref: str = Field(description="Reference to the file attachment for the evidence")
    notarization_status: EvidenceNotarizationStatus = Field(
        description="Notarization status of the evidence (none, pending, notarized)"
    )
    notarization_number: Optional[str] = Field(
        description="Notarization certificate number, null if not notarized",
        default=None,
    )
    notarization_date: Optional[str] = Field(
        description="Date of notarization, null if not notarized (ISO 8601 date)",
        default=None,
    )
    notarization_institution: Optional[str] = Field(
        description="Name of the notarization institution, null if not notarized",
        default=None,
    )
    notarized_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the notarized document, null if not notarized",
        default=None,
    )
    submitted_by_ref: str = Field(description="Employee reference of the person who submitted the evidence")
    evidence_status: EvidenceStatus = Field(
        description="Current status of the evidence (active, archived, withdrawn)"
    )
    created_at: str = Field(description="Timestamp when the evidence record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the evidence record was last updated (ISO 8601)")


class LawLegalConsultation(BaseModel):
    """Represents a legal consultation request from an employee"""

    legal_consultation_ref: str = Field(description="Unique identifier for the legal consultation")
    requester_employee_ref: str = Field(description="Employee reference of the person requesting consultation")
    consultation_type: ConsultationType = Field(
        description="Type of consultation (contract_review, compliance_advice, ip_consultation, labor_law, regulatory, general)"
    )
    channel: ConsultationChannel = Field(
        description="Channel through which the consultation was requested (service_desk, email, phone, meeting, im)"
    )
    title: str = Field(description="Title of the consultation request")
    description: str = Field(description="Detailed description of the consultation request")
    urgency: ConsultationUrgency = Field(
        description="Urgency level of the consultation (low, normal, high, urgent)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the legal counsel assigned, null if not yet assigned",
        default=None,
    )
    consultation_status: ConsultationStatus = Field(
        description="Current status of the consultation (open, assigned, in_progress, resolved, closed)"
    )
    response_summary: str = Field(description="Summary of the response provided")
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource, null if not linked",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference to the related resource, null if not linked",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the consultation was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    satisfaction_rating: Optional[int] = Field(
        description="Satisfaction rating from the requester (1-5), null if not rated",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the consultation was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the consultation was last updated (ISO 8601)")


class LawComplianceReview(BaseModel):
    """Represents a compliance review conducted on a business area or resource"""

    compliance_review_ref: str = Field(description="Unique identifier for the compliance review")
    review_title: str = Field(description="Title of the compliance review")
    review_type: ComplianceReviewType = Field(
        description="Type of review (business_compliance, data_privacy, export_control, anti_corruption, environmental, general)"
    )
    review_scope: str = Field(description="Scope of the compliance review")
    target_resource_type: Optional[str] = Field(
        description="Type of the target resource being reviewed, null if general review",
        default=None,
    )
    target_resource_ref: Optional[str] = Field(
        description="Reference to the target resource being reviewed, null if general review",
        default=None,
    )
    department_ref: Optional[str] = Field(
        description="Reference to the department being reviewed, null if not department-specific",
        default=None,
    )
    reviewer_employee_ref: str = Field(description="Employee reference of the reviewer")
    review_status: ComplianceReviewStatus = Field(
        description="Current status of the review (planned, in_progress, completed, cancelled)"
    )
    risk_level: ContractRiskLevel = Field(
        description="Risk level identified in the review (low, medium, high, critical)"
    )
    findings: str = Field(description="Findings from the compliance review")
    recommendations: str = Field(description="Recommendations based on the review findings")
    review_result: Optional[ComplianceReviewResult] = Field(
        description="Result of the review (compliant, non_compliant, partially_compliant), null if not yet concluded",
        default=None,
    )
    review_date: str = Field(description="Date of the review (ISO 8601 date)")
    next_review_date: Optional[str] = Field(
        description="Date of the next scheduled review, null if not scheduled (ISO 8601 date)",
        default=None,
    )
    report_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the review report, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the review record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the review record was last updated (ISO 8601)")


class LawCorporateEntity(BaseModel):
    """Represents a corporate entity or subsidiary managed by the organization"""

    corporate_entity_ref: str = Field(description="Unique identifier for the corporate entity")
    entity_name: str = Field(description="Name of the corporate entity")
    entity_type: CorporateEntityType = Field(
        description="Type of entity (subsidiary, branch, joint_venture, holding, representative_office)"
    )
    unified_social_credit_code: str = Field(description="Unified social credit code of the entity")
    legal_representative: str = Field(description="Name of the legal representative")
    registered_capital: str = Field(description="Registered capital of the entity")
    registered_address: str = Field(description="Registered address of the entity")
    business_scope: str = Field(description="Business scope of the entity")
    establishment_date: str = Field(description="Date when the entity was established (ISO 8601 date)")
    entity_status: CorporateEntityStatus = Field(
        description="Current status of the entity (active, inactive, dissolved, merging, liquidating)"
    )
    parent_entity_ref: Optional[str] = Field(
        description="Reference to the parent corporate entity, null if top-level",
        default=None,
    )
    responsible_employee_ref: str = Field(
        description="Employee reference of the person responsible for the entity"
    )
    notes: str = Field(description="Additional notes about the corporate entity")
    created_at: str = Field(description="Timestamp when the entity record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the entity record was last updated (ISO 8601)")


class LawEntityChange(BaseModel):
    """Represents a change or modification to a corporate entity's registration details"""

    entity_change_ref: str = Field(description="Unique identifier for the entity change")
    corporate_entity_ref: str = Field(description="Reference to the corporate entity being changed")
    change_type: EntityChangeType = Field(
        description="Type of change (name_change, address_change, capital_change, scope_change, representative_change, shareholder_change, other)"
    )
    change_description: str = Field(description="Description of the change")
    before_value: str = Field(description="Value before the change")
    after_value: str = Field(description="Value after the change")
    change_status: EntityChangeStatus = Field(
        description="Current status of the change (pending, approved, rejected, completed, cancelled)"
    )
    effective_date: Optional[str] = Field(
        description="Date when the change becomes effective, null if not yet effective (ISO 8601 date)",
        default=None,
    )
    applied_by_ref: str = Field(description="Employee reference of the person who applied the change")
    approved_at: Optional[str] = Field(
        description="Timestamp when the change was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    document_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the change document, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the change record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the change record was last updated (ISO 8601)")


class LawQualificationCertificate(BaseModel):
    """Represents a qualification certificate or license held by the organization or an employee"""

    qualification_certificate_ref: str = Field(description="Unique identifier for the qualification certificate")
    certificate_name: str = Field(description="Name of the certificate")
    certificate_type: QualificationCertificateType = Field(
        description="Type of certificate (business_license, tax_registration, safety_permit, quality_certification, industry_license, professional_license, other)"
    )
    certificate_number: str = Field(description="Certificate number")
    issuing_authority: str = Field(description="Name of the issuing authority")
    holder_type: CertificateHolderType = Field(
        description="Type of holder (company, employee)"
    )
    holder_entity_ref: Optional[str] = Field(
        description="Reference to the corporate entity holding the certificate, null if held by an employee",
        default=None,
    )
    holder_employee_ref: Optional[str] = Field(
        description="Reference to the employee holding the certificate, null if held by a company",
        default=None,
    )
    issue_date: str = Field(description="Date when the certificate was issued (ISO 8601 date)")
    expiry_date: str = Field(description="Date when the certificate expires (ISO 8601 date)")
    renewal_reminder_days: int = Field(description="Number of days before expiry to send a renewal reminder")
    certificate_status: CertificateStatus = Field(
        description="Current status of the certificate (active, expired, revoked, pending_renewal)"
    )
    certificate_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the certificate, null if not uploaded",
        default=None,
    )
    custodian_employee_ref: str = Field(
        description="Employee reference of the certificate custodian"
    )
    storage_location: str = Field(description="Physical storage location of the certificate")
    notes: str = Field(description="Additional notes about the certificate")
    created_at: str = Field(description="Timestamp when the certificate record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the certificate record was last updated (ISO 8601)")


class LawLicenseUsageRequest(BaseModel):
    """Represents a request to borrow or use a qualification certificate"""

    license_usage_request_ref: str = Field(description="Unique identifier for the license usage request")
    qualification_certificate_ref: str = Field(description="Reference to the qualification certificate")
    applicant_employee_ref: str = Field(description="Employee reference of the applicant")
    usage_purpose: str = Field(description="Purpose of using the certificate")
    usage_type: LicenseUsageType = Field(
        description="Type of usage (original, copy, scan)"
    )
    usage_start_date: str = Field(description="Start date of the usage period (ISO 8601 date)")
    usage_end_date: str = Field(description="End date of the usage period (ISO 8601 date)")
    request_status: LicenseUsageRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, borrowed, returned, overdue)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who approved the request, null if not yet approved",
        default=None,
    )
    borrowed_at: Optional[str] = Field(
        description="Timestamp when the certificate was borrowed, null if not yet borrowed (ISO 8601)",
        default=None,
    )
    returned_at: Optional[str] = Field(
        description="Timestamp when the certificate was returned, null if not yet returned (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the request was last updated (ISO 8601)")


class LawRelatedParty(BaseModel):
    """Represents a related party with potential conflicts of interest"""

    related_party_ref: str = Field(description="Unique identifier for the related party")
    party_name: str = Field(description="Name of the related party")
    party_type: RelatedPartyType = Field(
        description="Type of party (enterprise, individual, government)"
    )
    relationship_type: RelationshipType = Field(
        description="Type of relationship (shareholder, subsidiary, affiliate, key_personnel, family_member, business_partner, other)"
    )
    relationship_description: str = Field(description="Description of the relationship")
    related_entity_ref: Optional[str] = Field(
        description="Reference to the related corporate entity, null if not applicable",
        default=None,
    )
    related_employee_ref: Optional[str] = Field(
        description="Reference to the related employee, null if not applicable",
        default=None,
    )
    contact_info: str = Field(description="Contact information for the related party")
    party_status: RelatedPartyStatus = Field(
        description="Current status of the related party (active, inactive, under_review)"
    )
    risk_level: RelatedPartyRiskLevel = Field(
        description="Risk level of the related party (low, medium, high, critical)"
    )
    identified_by_ref: str = Field(description="Employee reference of the person who identified the related party")
    identified_at: str = Field(description="Timestamp when the related party was identified (ISO 8601)")
    notes: str = Field(description="Additional notes about the related party")
    created_at: str = Field(description="Timestamp when the related party record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the related party record was last updated (ISO 8601)")


class LawRelatedPartyTransaction(BaseModel):
    """Represents a transaction with a related party requiring compliance review"""

    related_party_transaction_ref: str = Field(description="Unique identifier for the related party transaction")
    related_party_ref: str = Field(description="Reference to the related party")
    transaction_type: RelatedPartyTransactionType = Field(
        description="Type of transaction (procurement, sales, service, lease, loan, guarantee, asset_transfer, other)"
    )
    transaction_description: str = Field(description="Description of the transaction")
    transaction_amount: float = Field(description="Monetary amount of the transaction")
    currency: Currency = Field(
        description="Currency of the transaction amount (CNY, USD, EUR, GBP, JPY, HKD)"
    )
    transaction_date: str = Field(description="Date of the transaction (ISO 8601 date)")
    contract_ref: Optional[str] = Field(
        description="Reference to the related contract, null if not linked",
        default=None,
    )
    compliance_status: RelatedPartyComplianceStatus = Field(
        description="Compliance review status (pending_review, approved, rejected, flagged)"
    )
    reviewed_by_ref: Optional[str] = Field(
        description="Employee reference of the reviewer, null if not yet reviewed",
        default=None,
    )
    reviewed_at: Optional[str] = Field(
        description="Timestamp when the transaction was reviewed, null if not yet reviewed (ISO 8601)",
        default=None,
    )
    review_comments: str = Field(description="Comments from the compliance review")
    created_at: str = Field(description="Timestamp when the transaction record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the transaction record was last updated (ISO 8601)")


class LawInnovationProposal(BaseModel):
    """Represents an innovation proposal submitted by an employee"""

    innovation_proposal_ref: str = Field(description="Unique identifier for the innovation proposal")
    proposer_employee_ref: str = Field(description="Employee reference of the proposer")
    department_ref: str = Field(description="Reference to the department associated with the proposal")
    proposal_title: str = Field(description="Title of the innovation proposal")
    proposal_category: InnovationProposalCategory = Field(
        description="Category of the proposal (product, process, technology, management, service, other)"
    )
    description: str = Field(description="Detailed description of the innovation proposal")
    expected_benefit: str = Field(description="Expected benefit of the proposed innovation")
    feasibility_assessment: str = Field(description="Feasibility assessment of the proposal")
    proposal_status: InnovationProposalStatus = Field(
        description="Current status of the proposal (submitted, under_review, approved, rejected, in_progress, completed, archived)"
    )
    reviewer_employee_ref: Optional[str] = Field(
        description="Employee reference of the reviewer, null if not yet assigned",
        default=None,
    )
    review_score: Optional[float] = Field(
        description="Review score assigned to the proposal, null if not yet reviewed",
        default=None,
    )
    review_comments: str = Field(description="Comments from the reviewer")
    ip_asset_ref: Optional[str] = Field(
        description="Reference to the IP asset created from this proposal, null if not applicable",
        default=None,
    )
    proposal_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the proposal document, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the proposal was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the proposal was last updated (ISO 8601)")


class LawSupplierAssessment(BaseModel):
    """Represents an assessment of a supplier's qualifications and risk profile"""

    supplier_assessment_ref: str = Field(description="Unique identifier for the supplier assessment")
    supplier_name: str = Field(description="Name of the supplier being assessed")
    supplier_party_ref: Optional[str] = Field(
        description="Reference to the contract party representing the supplier, null if not linked",
        default=None,
    )
    assessment_type: SupplierAssessmentType = Field(
        description="Type of assessment (qualification, annual_review, incident_review, exit_review)"
    )
    assessor_employee_ref: str = Field(description="Employee reference of the assessor")
    assessment_date: str = Field(description="Date of the assessment (ISO 8601 date)")
    financial_score: Optional[float] = Field(
        description="Financial assessment score, null if not scored",
        default=None,
    )
    compliance_score: Optional[float] = Field(
        description="Compliance assessment score, null if not scored",
        default=None,
    )
    quality_score: Optional[float] = Field(
        description="Quality assessment score, null if not scored",
        default=None,
    )
    overall_score: Optional[float] = Field(
        description="Overall assessment score, null if not scored",
        default=None,
    )
    risk_level: SupplierRiskLevel = Field(
        description="Risk level of the supplier (low, medium, high, critical)"
    )
    risk_findings: str = Field(description="Risk findings from the assessment")
    recommendations: str = Field(description="Recommendations based on the assessment")
    assessment_status: SupplierAssessmentStatus = Field(
        description="Current status of the assessment (planned, in_progress, completed, cancelled)"
    )
    report_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the assessment report, null if not uploaded",
        default=None,
    )
    next_assessment_date: Optional[str] = Field(
        description="Date of the next scheduled assessment, null if not scheduled (ISO 8601 date)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the assessment record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the assessment record was last updated (ISO 8601)")


class LawHighRiskSoftware(BaseModel):
    """Represents a high-risk software identified for compliance and security review"""

    high_risk_software_ref: str = Field(description="Unique identifier for the high-risk software record")
    software_name: str = Field(description="Name of the software")
    software_version: str = Field(description="Version of the software")
    vendor: str = Field(description="Vendor or publisher of the software")
    risk_level: HighRiskSoftwareRiskLevel = Field(
        description="Risk level of the software (medium, high, critical)"
    )
    risk_category: HighRiskSoftwareRiskCategory = Field(
        description="Category of risk (security_vulnerability, license_violation, data_leakage, compliance_issue, supply_chain_risk, other)"
    )
    risk_description: str = Field(description="Description of the identified risk")
    affected_departments: List[str] = Field(
        description="List of department references affected by this software"
    )
    usage_status: HighRiskSoftwareUsageStatus = Field(
        description="Current usage status (restricted, prohibited, approved_with_conditions, under_review)"
    )
    mitigation_measures: str = Field(description="Measures taken to mitigate the risk")
    alternative_software: str = Field(description="Recommended alternative software")
    compliance_status: HighRiskSoftwareComplianceStatus = Field(
        description="Compliance status (compliant, non_compliant, pending_review, exempted)"
    )
    assessed_by_ref: str = Field(description="Employee reference of the person who assessed the software")
    assessed_at: str = Field(description="Timestamp when the assessment was performed (ISO 8601)")
    review_due_date: Optional[str] = Field(
        description="Date when the next review is due, null if not scheduled (ISO 8601 date)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class LawBusinessRisk(BaseModel):
    """Represents a business risk identified and tracked by the organization"""

    business_risk_ref: str = Field(description="Unique identifier for the business risk")
    risk_title: str = Field(description="Title of the business risk")
    risk_category: BusinessRiskCategory = Field(
        description="Category of the risk (market, operational, financial, legal, compliance, strategic, reputational, technology)"
    )
    risk_level: BusinessRiskLevel = Field(
        description="Level of the risk (low, medium, high, critical)"
    )
    risk_description: str = Field(description="Detailed description of the risk")
    risk_source: str = Field(description="Source or origin of the risk")
    affected_department_ref: Optional[str] = Field(
        description="Reference to the department affected by the risk, null if organization-wide",
        default=None,
    )
    probability: BusinessRiskProbability = Field(
        description="Probability of the risk occurring (low, medium, high, very_high)"
    )
    impact: BusinessRiskImpact = Field(
        description="Impact level if the risk materializes (low, medium, high, critical)"
    )
    mitigation_plan: str = Field(description="Plan to mitigate the risk")
    contingency_plan: str = Field(description="Contingency plan if the risk materializes")
    risk_status: BusinessRiskStatus = Field(
        description="Current status of the risk (open, mitigating, resolved, accepted, closed)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the risk owner")
    identified_at: str = Field(description="Timestamp when the risk was identified (ISO 8601)")
    review_due_date: Optional[str] = Field(
        description="Date when the next review is due, null if not scheduled (ISO 8601 date)",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the risk was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the risk record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the risk record was last updated (ISO 8601)")


class LawPolicy(BaseModel):
    """Represents an organizational policy or regulation"""

    policy_ref: str = Field(description="Unique identifier for the policy")
    policy_title: str = Field(description="Title of the policy")
    policy_code: str = Field(description="Short code for the policy")
    policy_category: PolicyCategory = Field(
        description="Category of the policy (parking, travel, expense, procurement, data_privacy, information_security, hr, compliance, safety, other)"
    )
    policy_scope: PolicyScope = Field(
        description="Scope of the policy (company_wide, department, team, region)"
    )
    scope_department_ref: Optional[str] = Field(
        description="Reference to the department if policy scope is department, null otherwise",
        default=None,
    )
    content: str = Field(description="Content of the policy")
    version: str = Field(description="Version string of the policy (e.g., 1.0, 2.1)")
    effective_date: str = Field(description="Date when the policy becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the policy expires, null if no expiry (ISO 8601 date)",
        default=None,
    )
    policy_status: PolicyStatus = Field(
        description="Current status of the policy (draft, active, expired, superseded, archived)"
    )
    issued_by_ref: str = Field(description="Employee reference of the person who issued the policy")
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who approved the policy, null if not yet approved",
        default=None,
    )
    policy_file_ref: Optional[str] = Field(
        description="Reference to the file attachment for the policy document, null if not uploaded",
        default=None,
    )
    supersedes_ref: Optional[str] = Field(
        description="Reference to the policy that this policy supersedes, null if not applicable",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the policy was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the policy was last updated (ISO 8601)")


class LawDomainAsset(BaseModel):
    """Represents a domain name asset managed by the organization"""

    domain_asset_ref: str = Field(description="Unique identifier for the domain asset")
    domain_name: str = Field(description="Domain name (e.g., example.com)")
    registrar: str = Field(description="Domain registrar name")
    registration_date: str = Field(description="Date when the domain was registered (ISO 8601 date)")
    expiry_date: str = Field(description="Date when the domain registration expires (ISO 8601 date)")
    auto_renew: bool = Field(description="Whether the domain is set to auto-renew")
    dns_provider: str = Field(description="DNS service provider")
    ssl_certificate_expiry: Optional[str] = Field(
        description="Expiry date of the SSL certificate, null if no SSL certificate (ISO 8601 date)",
        default=None,
    )
    owner_entity_ref: Optional[str] = Field(
        description="Reference to the corporate entity that owns the domain, null if not specified",
        default=None,
    )
    responsible_employee_ref: str = Field(
        description="Employee reference of the person responsible for the domain"
    )
    domain_status: DomainStatus = Field(
        description="Current status of the domain (active, expired, transferring, suspended, reserved)"
    )
    usage_purpose: str = Field(description="Purpose or usage of the domain")
    notes: str = Field(description="Additional notes about the domain")
    created_at: str = Field(description="Timestamp when the domain record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the domain record was last updated (ISO 8601)")


class LawDB(OfficeDB):
    """Database containing legal affairs module data including contracts, IP assets, compliance, corporate entities and more, inheriting all base office tables"""

    law_contract_template: Dict[str, LawContractTemplate] = Field(
        description="Dictionary of all contract templates indexed by contract_template_ref"
    )
    law_contract_party: Dict[str, LawContractParty] = Field(
        description="Dictionary of all contract parties indexed by contract_party_ref"
    )
    law_contract: Dict[str, LawContract] = Field(
        description="Dictionary of all contracts indexed by contract_ref"
    )
    law_contract_party_link: Dict[str, LawContractPartyLink] = Field(
        description="Dictionary of all contract-party links indexed by contract_party_link_ref"
    )
    law_contract_amendment: Dict[str, LawContractAmendment] = Field(
        description="Dictionary of all contract amendments indexed by contract_amendment_ref"
    )
    law_contract_transfer: Dict[str, LawContractTransfer] = Field(
        description="Dictionary of all contract transfers indexed by contract_transfer_ref"
    )
    law_contract_milestone: Dict[str, LawContractMilestone] = Field(
        description="Dictionary of all contract milestones indexed by contract_milestone_ref"
    )
    law_contract_risk: Dict[str, LawContractRisk] = Field(
        description="Dictionary of all contract risks indexed by contract_risk_ref"
    )
    law_contract_loan: Dict[str, LawContractLoan] = Field(
        description="Dictionary of all contract loans indexed by contract_loan_ref"
    )
    law_approval_flow: Dict[str, LawApprovalFlow] = Field(
        description="Dictionary of all approval flows indexed by approval_flow_ref"
    )
    law_approval_step: Dict[str, LawApprovalStep] = Field(
        description="Dictionary of all approval steps indexed by approval_step_ref"
    )
    law_seal: Dict[str, LawSeal] = Field(
        description="Dictionary of all seals indexed by seal_ref"
    )
    law_seal_usage_request: Dict[str, LawSealUsageRequest] = Field(
        description="Dictionary of all seal usage requests indexed by seal_usage_request_ref"
    )
    law_ip_asset: Dict[str, LawIPAsset] = Field(
        description="Dictionary of all IP assets indexed by ip_asset_ref"
    )
    law_ip_inventor: Dict[str, LawIPInventor] = Field(
        description="Dictionary of all IP inventors indexed by ip_inventor_ref"
    )
    law_ip_application: Dict[str, LawIPApplication] = Field(
        description="Dictionary of all IP applications indexed by ip_application_ref"
    )
    law_ip_authorization: Dict[str, LawIPAuthorization] = Field(
        description="Dictionary of all IP authorizations indexed by ip_authorization_ref"
    )
    law_ip_reward: Dict[str, LawIPReward] = Field(
        description="Dictionary of all IP rewards indexed by ip_reward_ref"
    )
    law_integrity_declaration: Dict[str, LawIntegrityDeclaration] = Field(
        description="Dictionary of all integrity declarations indexed by integrity_declaration_ref"
    )
    law_violation_report: Dict[str, LawViolationReport] = Field(
        description="Dictionary of all violation reports indexed by violation_report_ref"
    )
    law_legal_case: Dict[str, LawLegalCase] = Field(
        description="Dictionary of all legal cases indexed by legal_case_ref"
    )
    law_case_event: Dict[str, LawCaseEvent] = Field(
        description="Dictionary of all case events indexed by case_event_ref"
    )
    law_evidence: Dict[str, LawEvidence] = Field(
        description="Dictionary of all evidence records indexed by evidence_ref"
    )
    law_legal_consultation: Dict[str, LawLegalConsultation] = Field(
        description="Dictionary of all legal consultations indexed by legal_consultation_ref"
    )
    law_compliance_review: Dict[str, LawComplianceReview] = Field(
        description="Dictionary of all compliance reviews indexed by compliance_review_ref"
    )
    law_corporate_entity: Dict[str, LawCorporateEntity] = Field(
        description="Dictionary of all corporate entities indexed by corporate_entity_ref"
    )
    law_entity_change: Dict[str, LawEntityChange] = Field(
        description="Dictionary of all entity changes indexed by entity_change_ref"
    )
    law_qualification_certificate: Dict[str, LawQualificationCertificate] = Field(
        description="Dictionary of all qualification certificates indexed by qualification_certificate_ref"
    )
    law_license_usage_request: Dict[str, LawLicenseUsageRequest] = Field(
        description="Dictionary of all license usage requests indexed by license_usage_request_ref"
    )
    law_related_party: Dict[str, LawRelatedParty] = Field(
        description="Dictionary of all related parties indexed by related_party_ref"
    )
    law_related_party_transaction: Dict[str, LawRelatedPartyTransaction] = Field(
        description="Dictionary of all related party transactions indexed by related_party_transaction_ref"
    )
    law_innovation_proposal: Dict[str, LawInnovationProposal] = Field(
        description="Dictionary of all innovation proposals indexed by innovation_proposal_ref"
    )
    law_supplier_assessment: Dict[str, LawSupplierAssessment] = Field(
        description="Dictionary of all supplier assessments indexed by supplier_assessment_ref"
    )
    law_high_risk_software: Dict[str, LawHighRiskSoftware] = Field(
        description="Dictionary of all high-risk software records indexed by high_risk_software_ref"
    )
    law_business_risk: Dict[str, LawBusinessRisk] = Field(
        description="Dictionary of all business risks indexed by business_risk_ref"
    )
    law_policy: Dict[str, LawPolicy] = Field(
        description="Dictionary of all policies indexed by policy_ref"
    )
    law_domain_asset: Dict[str, LawDomainAsset] = Field(
        description="Dictionary of all domain assets indexed by domain_asset_ref"
    )

    def get_statistics(self) -> Dict[str, Any]:
        """
        功能说明（Description）：
            获取统计信息，并返回可供后续流程使用的结果。包含基础办公模块和法务模块的统计数据。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `Dict[str, Any]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        base_stats = super().get_statistics()
        law_stats = {
            "num_law_contract_templates": len(self.law_contract_template),
            "num_law_contract_parties": len(self.law_contract_party),
            "num_law_contracts": len(self.law_contract),
            "num_law_contract_party_links": len(self.law_contract_party_link),
            "num_law_contract_amendments": len(self.law_contract_amendment),
            "num_law_contract_transfers": len(self.law_contract_transfer),
            "num_law_contract_milestones": len(self.law_contract_milestone),
            "num_law_contract_risks": len(self.law_contract_risk),
            "num_law_contract_loans": len(self.law_contract_loan),
            "num_law_approval_flows": len(self.law_approval_flow),
            "num_law_approval_steps": len(self.law_approval_step),
            "num_law_seals": len(self.law_seal),
            "num_law_seal_usage_requests": len(self.law_seal_usage_request),
            "num_law_ip_assets": len(self.law_ip_asset),
            "num_law_ip_inventors": len(self.law_ip_inventor),
            "num_law_ip_applications": len(self.law_ip_application),
            "num_law_ip_authorizations": len(self.law_ip_authorization),
            "num_law_ip_rewards": len(self.law_ip_reward),
            "num_law_integrity_declarations": len(self.law_integrity_declaration),
            "num_law_violation_reports": len(self.law_violation_report),
            "num_law_legal_cases": len(self.law_legal_case),
            "num_law_case_events": len(self.law_case_event),
            "num_law_evidence": len(self.law_evidence),
            "num_law_legal_consultations": len(self.law_legal_consultation),
            "num_law_compliance_reviews": len(self.law_compliance_review),
            "num_law_corporate_entities": len(self.law_corporate_entity),
            "num_law_entity_changes": len(self.law_entity_change),
            "num_law_qualification_certificates": len(self.law_qualification_certificate),
            "num_law_license_usage_requests": len(self.law_license_usage_request),
            "num_law_related_parties": len(self.law_related_party),
            "num_law_related_party_transactions": len(self.law_related_party_transaction),
            "num_law_innovation_proposals": len(self.law_innovation_proposal),
            "num_law_supplier_assessments": len(self.law_supplier_assessment),
            "num_law_high_risk_software": len(self.law_high_risk_software),
            "num_law_business_risks": len(self.law_business_risk),
            "num_law_policies": len(self.law_policy),
            "num_law_domain_assets": len(self.law_domain_asset),
        }
        return {**base_stats, **law_stats}