from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

ProcurementCategoryStatus = Literal["active", "inactive"]

SupplierType = Literal["standard", "strategic", "occasional"]
CooperationStatus = Literal["pending", "approved", "suspended", "blacklisted"]
RiskLevel = Literal["low", "medium", "high", "critical"]

SupplierContactStatus = Literal["active", "inactive"]

QualificationType = Literal[
    "business_license", "tax_registration", "iso_certification",
    "industry_permit", "safety_certification", "environmental_certification", "other"
]
VerificationStatus = Literal["pending", "verified", "rejected", "expired"]

SupplierCategoryStatus = Literal["active", "removed"]

EvaluationRating = Literal["A", "B", "C", "D", "E"]
EvaluationStatus = Literal["draft", "submitted", "approved", "rejected"]

SourcingType = Literal["competitive_bid", "negotiation", "sole_source", "framework_agreement", "reverse_auction"]
ProcurementMethod = Literal["centralized", "decentralized", "hybrid"]
SourcingProjectStatus = Literal["draft", "open", "evaluation", "awarded", "cancelled", "closed"]

InvitationStatus = Literal["invited", "accepted", "declined", "no_response"]
QualificationCheck = Literal["pending", "passed", "failed"]
SourcingSupplierStatus = Literal["active", "disqualified", "withdrawn"]

QuotationStatus = Literal["draft", "submitted", "under_review", "accepted", "rejected", "expired", "withdrawn"]

RequisitionType = Literal["standard", "urgent", "blanket", "service"]
RequisitionStatus = Literal["draft", "submitted", "under_review", "approved", "rejected", "cancelled", "fulfilled"]

ContractType = Literal["fixed_price", "cost_plus", "time_and_materials", "framework", "blanket"]
ContractStatus = Literal["draft", "pending_approval", "active", "suspended", "expired", "terminated", "completed"]

OrderType = Literal["standard", "blanket_release", "emergency", "service"]
OrderPriority = Literal["low", "normal", "high", "urgent"]
OrderStatus = Literal[
    "draft", "submitted", "approved", "rejected", "sent_to_supplier",
    "confirmed", "partially_received", "completed", "cancelled"
]

PurchaseOrderItemStatus = Literal["pending", "partially_received", "received", "accepted", "rejected", "cancelled"]

ChangeTargetType = Literal["purchase_order", "purchase_contract"]
ChangeType = Literal["quantity_adjustment", "price_adjustment", "delivery_date_change", "item_addition", "item_removal", "cancellation", "other"]
ChangeStatus = Literal["pending", "approved", "rejected", "executed", "cancelled"]

ReceiptStatus = Literal["pending_inspection", "inspected", "accepted", "partially_accepted", "rejected", "completed"]

ItemCondition = Literal["good", "damaged", "defective", "wrong_item"]

InspectionType = Literal["full", "sampling", "visual", "functional", "skip"]
OverallResult = Literal["accepted", "partially_accepted", "rejected", "conditional"]
AcceptanceItemResult = Literal["accepted", "rejected", "conditional"]
AcceptanceStatus = Literal["pending", "in_progress", "completed", "cancelled"]

ApplicableType = Literal[
    "purchase_requisition", "purchase_order", "purchase_contract",
    "purchase_change_request", "supplier_onboarding"
]
ApprovalFlowTemplateStatus = Literal["active", "inactive", "deprecated"]

ApproverType = Literal["employee", "role", "department_head", "direct_manager"]

ApprovalStatus = Literal["in_progress", "approved", "rejected", "cancelled", "withdrawn"]

ApprovalActionType = Literal["approve", "reject", "return", "delegate", "comment"]

ProcurementPermissionOperation = Literal[
    "create_requisition", "create_order", "approve", "create_contract",
    "manage_supplier", "view_reports", "export_data"
]
ProcurementPermissionRuleStatus = Literal["active", "inactive", "expired"]

CourseType = Literal["process_training", "system_training", "compliance", "skill_development"]
CourseStatus = Literal["active", "archived", "draft"]

TrainingRecordStatus = Literal["enrolled", "in_progress", "completed", "failed", "cancelled"]

IssueType = Literal["system_error", "process_issue", "supplier_complaint", "delivery_issue", "quality_issue", "other"]
IssueSeverity = Literal["low", "medium", "high", "critical"]
TicketStatus = Literal["open", "in_progress", "resolved", "closed", "cancelled"]


# --- Models ---


class ProcurementCategory(BaseModel):
    """Represents a hierarchical procurement category for classifying purchases"""

    procurement_category_ref: str = Field(description="Unique identifier for the procurement category")
    category_name: str = Field(description="Name of the procurement category")
    category_code: str = Field(description="Short code for the procurement category")
    parent_category_ref: Optional[str] = Field(
        description="Reference to the parent category, null if root category",
        default=None,
    )
    category_level: int = Field(description="Depth in the category tree, root = 1")
    category_status: ProcurementCategoryStatus = Field(
        description="Current status of the category (active, inactive)"
    )
    description: str = Field(description="Description of the procurement category")
    display_order: int = Field(description="Order for display/sorting purposes")
    created_at: str = Field(description="Timestamp when the category was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the category was last updated (ISO 8601)")


class Supplier(BaseModel):
    """Represents a supplier with registration details, banking information and cooperation status"""

    supplier_ref: str = Field(description="Unique identifier for the supplier")
    supplier_name: str = Field(description="Name of the supplier")
    supplier_code: str = Field(description="Short code for the supplier")
    supplier_type: SupplierType = Field(
        description="Type of supplier (standard, strategic, occasional)"
    )
    unified_social_credit_code: str = Field(
        description="Unified social credit code for the supplier (business registration number)"
    )
    legal_representative: str = Field(description="Name of the legal representative of the supplier")
    registered_address: str = Field(description="Registered address of the supplier")
    business_address: str = Field(description="Business/operating address of the supplier")
    country: str = Field(description="Country code of the supplier (e.g., CN, US)")
    bank_name: str = Field(description="Name of the supplier's bank")
    bank_account: str = Field(description="Bank account number of the supplier")
    tax_id: str = Field(description="Tax identification number of the supplier")
    cooperation_status: CooperationStatus = Field(
        description="Current cooperation status (pending, approved, suspended, blacklisted)"
    )
    risk_level: RiskLevel = Field(
        description="Risk level assessment of the supplier (low, medium, high, critical)"
    )
    onboarding_date: Optional[str] = Field(
        description="Date the supplier was onboarded, null if not yet onboarded (ISO 8601 date)",
        default=None,
    )
    blacklist_reason: Optional[str] = Field(
        description="Reason for blacklisting the supplier, null if not blacklisted",
        default=None,
    )
    notes: str = Field(description="Additional notes about the supplier")
    registered_by_ref: str = Field(description="Employee reference of the person who registered the supplier")
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who approved the supplier, null if not yet approved",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the supplier was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the supplier was last updated (ISO 8601)")


class SupplierContact(BaseModel):
    """Represents a contact person associated with a supplier"""

    supplier_contact_ref: str = Field(description="Unique identifier for the supplier contact")
    supplier_ref: str = Field(description="Reference to the associated supplier")
    contact_name: str = Field(description="Name of the contact person")
    contact_title: str = Field(description="Job title of the contact person")
    phone: str = Field(description="Phone number of the contact person")
    email: str = Field(description="Email address of the contact person")
    is_primary: bool = Field(description="Whether this is the primary contact for the supplier")
    status: SupplierContactStatus = Field(
        description="Current status of the contact (active, inactive)"
    )
    created_at: str = Field(description="Timestamp when the contact was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the contact was last updated (ISO 8601)")


class SupplierQualification(BaseModel):
    """Represents a qualification or certification held by a supplier"""

    supplier_qualification_ref: str = Field(description="Unique identifier for the supplier qualification")
    supplier_ref: str = Field(description="Reference to the associated supplier")
    qualification_type: QualificationType = Field(
        description="Type of qualification (business_license, tax_registration, iso_certification, industry_permit, safety_certification, environmental_certification, other)"
    )
    qualification_name: str = Field(description="Name of the qualification or certification")
    certificate_number: str = Field(description="Certificate or license number")
    issuing_authority: str = Field(description="Authority that issued the qualification")
    issue_date: str = Field(description="Date the qualification was issued (ISO 8601 date)")
    expiry_date: str = Field(description="Date the qualification expires (ISO 8601 date)")
    file_attachment_ref: Optional[str] = Field(
        description="Reference to the file attachment of the certificate, null if not uploaded",
        default=None,
    )
    verification_status: VerificationStatus = Field(
        description="Current verification status (pending, verified, rejected, expired)"
    )
    verified_by_ref: Optional[str] = Field(
        description="Employee reference of the person who verified the qualification, null if not verified",
        default=None,
    )
    verified_at: Optional[str] = Field(
        description="Timestamp when the qualification was verified, null if not verified (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the qualification was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the qualification was last updated (ISO 8601)")


class SupplierCategory(BaseModel):
    """Represents the association between a supplier and a procurement category"""

    supplier_category_ref: str = Field(description="Unique identifier for the supplier-category association")
    supplier_ref: str = Field(description="Reference to the associated supplier")
    procurement_category_ref: str = Field(description="Reference to the associated procurement category")
    is_preferred: bool = Field(description="Whether the supplier is preferred for this category")
    status: SupplierCategoryStatus = Field(
        description="Current status of the association (active, removed)"
    )
    created_at: str = Field(description="Timestamp when the association was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the association was last updated (ISO 8601)")


class SupplierEvaluation(BaseModel):
    """Represents a periodic evaluation of a supplier's performance"""

    supplier_evaluation_ref: str = Field(description="Unique identifier for the supplier evaluation")
    supplier_ref: str = Field(description="Reference to the evaluated supplier")
    evaluation_period: str = Field(description="Evaluation period identifier (e.g., 2025-Q1)")
    quality_score: float = Field(description="Quality score for the evaluation period")
    delivery_score: float = Field(description="Delivery performance score for the evaluation period")
    price_score: float = Field(description="Price competitiveness score for the evaluation period")
    service_score: float = Field(description="Service quality score for the evaluation period")
    overall_score: float = Field(description="Overall composite score for the evaluation period")
    rating: EvaluationRating = Field(
        description="Overall rating grade (A, B, C, D, E)"
    )
    evaluator_ref: str = Field(description="Employee reference of the evaluator")
    comments: str = Field(description="Evaluator's comments and observations")
    status: EvaluationStatus = Field(
        description="Current status of the evaluation (draft, submitted, approved, rejected)"
    )
    created_at: str = Field(description="Timestamp when the evaluation was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the evaluation was last updated (ISO 8601)")


class SourcingProject(BaseModel):
    """Represents a sourcing project for procurement with bidding and evaluation details"""

    sourcing_project_ref: str = Field(description="Unique identifier for the sourcing project")
    project_title: str = Field(description="Title of the sourcing project")
    project_code: str = Field(description="Short code for the sourcing project")
    sourcing_type: SourcingType = Field(
        description="Type of sourcing (competitive_bid, negotiation, sole_source, framework_agreement, reverse_auction)"
    )
    procurement_category_ref: str = Field(description="Reference to the procurement category")
    procurement_method: ProcurementMethod = Field(
        description="Procurement method (centralized, decentralized, hybrid)"
    )
    budget_amount: float = Field(description="Budget amount for the sourcing project")
    currency: str = Field(description="Currency code (e.g., CNY, USD)")
    description: str = Field(description="Description of the sourcing project")
    requirements: str = Field(description="Detailed requirements for the sourcing project")
    bid_document_file_ref: Optional[str] = Field(
        description="Reference to the bid document file attachment, null if not uploaded",
        default=None,
    )
    submission_deadline: str = Field(description="Deadline for supplier submissions (ISO 8601)")
    evaluation_criteria: Dict[str, Any] = Field(
        description="Dictionary of evaluation criteria and their weights"
    )
    owner_employee_ref: str = Field(description="Employee reference of the project owner")
    project_status: SourcingProjectStatus = Field(
        description="Current status of the sourcing project (draft, open, evaluation, awarded, cancelled, closed)"
    )
    awarded_supplier_ref: Optional[str] = Field(
        description="Reference to the awarded supplier, null if not yet awarded",
        default=None,
    )
    award_date: Optional[str] = Field(
        description="Date the project was awarded, null if not yet awarded (ISO 8601 date)",
        default=None,
    )
    cancel_reason: Optional[str] = Field(
        description="Reason for cancellation, null if not cancelled",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the sourcing project was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the sourcing project was last updated (ISO 8601)")


class SourcingSupplier(BaseModel):
    """Represents a supplier's participation in a sourcing project"""

    sourcing_supplier_ref: str = Field(description="Unique identifier for the sourcing supplier record")
    sourcing_project_ref: str = Field(description="Reference to the sourcing project")
    supplier_ref: str = Field(description="Reference to the supplier")
    invitation_status: InvitationStatus = Field(
        description="Current invitation status (invited, accepted, declined, no_response)"
    )
    qualification_check: QualificationCheck = Field(
        description="Qualification check result (pending, passed, failed)"
    )
    evaluation_score: Optional[float] = Field(
        description="Evaluation score assigned to the supplier, null if not yet evaluated",
        default=None,
    )
    evaluation_rank: Optional[int] = Field(
        description="Rank of the supplier in the evaluation, null if not yet ranked",
        default=None,
    )
    evaluation_comments: str = Field(description="Comments from the evaluation of the supplier")
    status: SourcingSupplierStatus = Field(
        description="Current status of the sourcing supplier (active, disqualified, withdrawn)"
    )
    invited_at: str = Field(description="Timestamp when the supplier was invited (ISO 8601)")
    responded_at: Optional[str] = Field(
        description="Timestamp when the supplier responded, null if no response (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class Quotation(BaseModel):
    """Represents a price quotation submitted by a supplier"""

    quotation_ref: str = Field(description="Unique identifier for the quotation")
    quotation_code: str = Field(description="Short code for the quotation")
    sourcing_project_ref: Optional[str] = Field(
        description="Reference to the associated sourcing project, null if standalone quotation",
        default=None,
    )
    supplier_ref: str = Field(description="Reference to the supplier who submitted the quotation")
    procurement_category_ref: str = Field(description="Reference to the procurement category")
    currency: str = Field(description="Currency code (e.g., CNY, USD)")
    total_amount: float = Field(description="Total amount of the quotation")
    tax_rate: float = Field(description="Applicable tax rate as a decimal")
    tax_amount: float = Field(description="Calculated tax amount")
    validity_date: str = Field(description="Date until which the quotation is valid (ISO 8601 date)")
    payment_terms: str = Field(description="Payment terms offered by the supplier")
    delivery_terms: str = Field(description="Delivery terms offered by the supplier")
    quotation_file_ref: Optional[str] = Field(
        description="Reference to the quotation file attachment, null if not uploaded",
        default=None,
    )
    submitted_by_ref: str = Field(description="Employee reference of the person who submitted the quotation")
    quotation_status: QuotationStatus = Field(
        description="Current status of the quotation (draft, submitted, under_review, accepted, rejected, expired, withdrawn)"
    )
    notes: str = Field(description="Additional notes about the quotation")
    created_at: str = Field(description="Timestamp when the quotation was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the quotation was last updated (ISO 8601)")


class QuotationItem(BaseModel):
    """Represents a line item within a quotation"""

    quotation_item_ref: str = Field(description="Unique identifier for the quotation item")
    quotation_ref: str = Field(description="Reference to the parent quotation")
    item_name: str = Field(description="Name of the quoted item")
    item_description: str = Field(description="Description of the quoted item")
    specification: str = Field(description="Technical specification of the item")
    unit: str = Field(description="Unit of measure (e.g., piece, kg, set)")
    quantity: int = Field(description="Quoted quantity")
    unit_price: float = Field(description="Unit price for the item")
    line_amount: float = Field(description="Total line amount (quantity × unit_price)")
    delivery_days: int = Field(description="Estimated delivery days for the item")
    notes: str = Field(description="Additional notes about the item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class PurchaseRequisition(BaseModel):
    """Represents a purchase requisition submitted by an employee for procurement"""

    purchase_requisition_ref: str = Field(description="Unique identifier for the purchase requisition")
    requisition_code: str = Field(description="Short code for the requisition")
    requisition_type: RequisitionType = Field(
        description="Type of requisition (standard, urgent, blanket, service)"
    )
    procurement_category_ref: str = Field(description="Reference to the procurement category")
    department_ref: str = Field(description="Reference to the requesting department")
    requestor_ref: str = Field(description="Employee reference of the requestor")
    procurement_method: ProcurementMethod = Field(
        description="Procurement method (centralized, decentralized, hybrid)"
    )
    currency: str = Field(description="Currency code (e.g., CNY, USD)")
    estimated_amount: float = Field(description="Estimated total amount for the requisition")
    required_date: str = Field(description="Date by which the items are required (ISO 8601 date)")
    business_justification: str = Field(description="Business justification for the purchase")
    special_requirements: str = Field(description="Any special requirements for the purchase")
    suggested_supplier_ref: Optional[str] = Field(
        description="Reference to a suggested supplier, null if no preference",
        default=None,
    )
    requisition_status: RequisitionStatus = Field(
        description="Current status of the requisition (draft, submitted, under_review, approved, rejected, cancelled, fulfilled)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the requisition was submitted, null if not submitted (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the requisition was approved, null if not approved (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the requisition was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the requisition was last updated (ISO 8601)")


class RequisitionItem(BaseModel):
    """Represents a line item within a purchase requisition"""

    requisition_item_ref: str = Field(description="Unique identifier for the requisition item")
    purchase_requisition_ref: str = Field(description="Reference to the parent purchase requisition")
    item_name: str = Field(description="Name of the requested item")
    item_description: str = Field(description="Description of the requested item")
    specification: str = Field(description="Technical specification of the item")
    unit: str = Field(description="Unit of measure (e.g., piece, kg, set)")
    quantity: int = Field(description="Requested quantity")
    estimated_unit_price: float = Field(description="Estimated unit price for the item")
    estimated_line_amount: float = Field(description="Estimated total line amount (quantity × estimated_unit_price)")
    required_date: str = Field(description="Date by which the item is required (ISO 8601 date)")
    notes: str = Field(description="Additional notes about the item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class PurchaseContract(BaseModel):
    """Represents a purchase contract with a supplier"""

    purchase_contract_ref: str = Field(description="Unique identifier for the purchase contract")
    contract_code: str = Field(description="Short code for the contract")
    contract_title: str = Field(description="Title of the contract")
    contract_type: ContractType = Field(
        description="Type of contract (fixed_price, cost_plus, time_and_materials, framework, blanket)"
    )
    supplier_ref: str = Field(description="Reference to the supplier")
    procurement_category_ref: str = Field(description="Reference to the procurement category")
    sourcing_project_ref: Optional[str] = Field(
        description="Reference to the associated sourcing project, null if not from a sourcing project",
        default=None,
    )
    currency: str = Field(description="Currency code (e.g., CNY, USD)")
    total_amount: float = Field(description="Total contract amount")
    tax_rate: float = Field(description="Applicable tax rate as a decimal")
    payment_terms: str = Field(description="Payment terms of the contract")
    delivery_terms: str = Field(description="Delivery terms of the contract")
    effective_date: str = Field(description="Date the contract becomes effective (ISO 8601 date)")
    expiry_date: str = Field(description="Date the contract expires (ISO 8601 date)")
    auto_renew: bool = Field(description="Whether the contract auto-renews upon expiry")
    contract_file_ref: Optional[str] = Field(
        description="Reference to the contract file attachment, null if not uploaded",
        default=None,
    )
    owner_employee_ref: str = Field(description="Employee reference of the contract owner")
    signer_employee_ref: str = Field(description="Employee reference of the contract signer")
    signed_at: Optional[str] = Field(
        description="Timestamp when the contract was signed, null if not signed (ISO 8601)",
        default=None,
    )
    contract_status: ContractStatus = Field(
        description="Current status of the contract (draft, pending_approval, active, suspended, expired, terminated, completed)"
    )
    consumed_amount: float = Field(description="Amount consumed/utilized against the contract so far")
    termination_reason: Optional[str] = Field(
        description="Reason for termination, null if not terminated",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the contract was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the contract was last updated (ISO 8601)")


class ContractItem(BaseModel):
    """Represents a line item within a purchase contract"""

    contract_item_ref: str = Field(description="Unique identifier for the contract item")
    purchase_contract_ref: str = Field(description="Reference to the parent purchase contract")
    item_name: str = Field(description="Name of the contracted item")
    item_description: str = Field(description="Description of the contracted item")
    specification: str = Field(description="Technical specification of the item")
    unit: str = Field(description="Unit of measure (e.g., piece, kg, set)")
    contracted_quantity: int = Field(description="Total contracted quantity")
    unit_price: float = Field(description="Unit price for the item")
    line_amount: float = Field(description="Total line amount (contracted_quantity × unit_price)")
    ordered_quantity: int = Field(description="Quantity already ordered against this contract item")
    received_quantity: int = Field(description="Quantity already received against this contract item")
    notes: str = Field(description="Additional notes about the item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class PurchaseOrder(BaseModel):
    """Represents a purchase order sent to a supplier for procurement of goods or services"""

    purchase_order_ref: str = Field(description="Unique identifier for the purchase order")
    order_code: str = Field(description="Short code for the purchase order")
    order_type: OrderType = Field(
        description="Type of order (standard, blanket_release, emergency, service)"
    )
    purchase_requisition_ref: Optional[str] = Field(
        description="Reference to the originating purchase requisition, null if not from a requisition",
        default=None,
    )
    purchase_contract_ref: Optional[str] = Field(
        description="Reference to the associated purchase contract, null if not contract-based",
        default=None,
    )
    supplier_ref: str = Field(description="Reference to the supplier")
    procurement_category_ref: str = Field(description="Reference to the procurement category")
    department_ref: str = Field(description="Reference to the requesting department")
    requestor_ref: str = Field(description="Employee reference of the requestor")
    buyer_ref: str = Field(description="Employee reference of the buyer handling the order")
    currency: str = Field(description="Currency code (e.g., CNY, USD)")
    total_amount: float = Field(description="Total amount of the purchase order")
    tax_rate: float = Field(description="Applicable tax rate as a decimal")
    tax_amount: float = Field(description="Calculated tax amount")
    payment_terms: str = Field(description="Payment terms for the order")
    delivery_address: str = Field(description="Delivery address for the order")
    expected_delivery_date: str = Field(description="Expected delivery date (ISO 8601 date)")
    priority: OrderPriority = Field(
        description="Priority level of the order (low, normal, high, urgent)"
    )
    order_status: OrderStatus = Field(
        description="Current status of the order (draft, submitted, approved, rejected, sent_to_supplier, confirmed, partially_received, completed, cancelled)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the order was submitted, null if not submitted (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the order was approved, null if not approved (ISO 8601)",
        default=None,
    )
    sent_to_supplier_at: Optional[str] = Field(
        description="Timestamp when the order was sent to the supplier, null if not sent (ISO 8601)",
        default=None,
    )
    supplier_confirmed_at: Optional[str] = Field(
        description="Timestamp when the supplier confirmed the order, null if not confirmed (ISO 8601)",
        default=None,
    )
    completed_at: Optional[str] = Field(
        description="Timestamp when the order was completed, null if not completed (ISO 8601)",
        default=None,
    )
    cancelled_at: Optional[str] = Field(
        description="Timestamp when the order was cancelled, null if not cancelled (ISO 8601)",
        default=None,
    )
    cancel_reason: Optional[str] = Field(
        description="Reason for cancellation, null if not cancelled",
        default=None,
    )
    notes: str = Field(description="Additional notes about the purchase order")
    created_at: str = Field(description="Timestamp when the order was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the order was last updated (ISO 8601)")


class PurchaseOrderItem(BaseModel):
    """Represents a line item within a purchase order"""

    purchase_order_item_ref: str = Field(description="Unique identifier for the purchase order item")
    purchase_order_ref: str = Field(description="Reference to the parent purchase order")
    contract_item_ref: Optional[str] = Field(
        description="Reference to the associated contract item, null if not contract-based",
        default=None,
    )
    requisition_item_ref: Optional[str] = Field(
        description="Reference to the associated requisition item, null if not from a requisition",
        default=None,
    )
    item_name: str = Field(description="Name of the ordered item")
    item_description: str = Field(description="Description of the ordered item")
    specification: str = Field(description="Technical specification of the item")
    unit: str = Field(description="Unit of measure (e.g., piece, kg, set)")
    quantity: int = Field(description="Ordered quantity")
    unit_price: float = Field(description="Unit price for the item")
    line_amount: float = Field(description="Total line amount (quantity × unit_price)")
    received_quantity: int = Field(description="Quantity received so far")
    accepted_quantity: int = Field(description="Quantity accepted after inspection")
    expected_delivery_date: str = Field(description="Expected delivery date for the item (ISO 8601 date)")
    item_status: PurchaseOrderItemStatus = Field(
        description="Current status of the item (pending, partially_received, received, accepted, rejected, cancelled)"
    )
    notes: str = Field(description="Additional notes about the item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class PurchaseChangeRequest(BaseModel):
    """Represents a change request for a purchase order or contract"""

    purchase_change_request_ref: str = Field(description="Unique identifier for the purchase change request")
    change_code: str = Field(description="Short code for the change request")
    change_target_type: ChangeTargetType = Field(
        description="Type of target being changed (purchase_order, purchase_contract)"
    )
    change_target_ref: str = Field(description="Reference to the target being changed")
    change_type: ChangeType = Field(
        description="Type of change (quantity_adjustment, price_adjustment, delivery_date_change, item_addition, item_removal, cancellation, other)"
    )
    change_reason: str = Field(description="Reason for the change request")
    change_details: Dict[str, Any] = Field(
        description="Dictionary of field changes with before/after values keyed by field name"
    )
    impact_amount: float = Field(description="Financial impact amount of the change")
    requestor_ref: str = Field(description="Employee reference of the person requesting the change")
    change_status: ChangeStatus = Field(
        description="Current status of the change request (pending, approved, rejected, executed, cancelled)"
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the change was approved, null if not approved (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    executed_at: Optional[str] = Field(
        description="Timestamp when the change was executed, null if not executed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the change request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the change request was last updated (ISO 8601)")


class GoodsReceipt(BaseModel):
    """Represents a goods receipt record for items delivered against a purchase order"""

    goods_receipt_ref: str = Field(description="Unique identifier for the goods receipt")
    receipt_code: str = Field(description="Short code for the goods receipt")
    purchase_order_ref: str = Field(description="Reference to the associated purchase order")
    supplier_ref: str = Field(description="Reference to the supplier who delivered the goods")
    receiver_ref: str = Field(description="Employee reference of the person who received the goods")
    receipt_date: str = Field(description="Date the goods were received (ISO 8601 date)")
    delivery_note_number: str = Field(description="Delivery note or shipping document number")
    warehouse_location: str = Field(description="Warehouse or storage location where goods were received")
    receipt_status: ReceiptStatus = Field(
        description="Current status of the receipt (pending_inspection, inspected, accepted, partially_accepted, rejected, completed)"
    )
    notes: str = Field(description="Additional notes about the goods receipt")
    created_at: str = Field(description="Timestamp when the receipt was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the receipt was last updated (ISO 8601)")


class GoodsReceiptItem(BaseModel):
    """Represents a line item within a goods receipt"""

    goods_receipt_item_ref: str = Field(description="Unique identifier for the goods receipt item")
    goods_receipt_ref: str = Field(description="Reference to the parent goods receipt")
    purchase_order_item_ref: str = Field(description="Reference to the associated purchase order item")
    item_name: str = Field(description="Name of the received item")
    received_quantity: int = Field(description="Quantity received")
    rejected_quantity: int = Field(description="Quantity rejected upon receipt")
    unit: str = Field(description="Unit of measure (e.g., piece, kg, set)")
    item_condition: ItemCondition = Field(
        description="Condition of the received item (good, damaged, defective, wrong_item)"
    )
    notes: str = Field(description="Additional notes about the received item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class AcceptanceRecord(BaseModel):
    """Represents an acceptance/inspection record for received goods"""

    acceptance_record_ref: str = Field(description="Unique identifier for the acceptance record")
    acceptance_code: str = Field(description="Short code for the acceptance record")
    goods_receipt_ref: str = Field(description="Reference to the associated goods receipt")
    purchase_order_ref: str = Field(description="Reference to the associated purchase order")
    inspector_ref: str = Field(description="Employee reference of the inspector")
    inspection_date: str = Field(description="Date the inspection was performed (ISO 8601 date)")
    inspection_type: InspectionType = Field(
        description="Type of inspection (full, sampling, visual, functional, skip)"
    )
    overall_result: OverallResult = Field(
        description="Overall inspection result (accepted, partially_accepted, rejected, conditional)"
    )
    accepted_quantity: int = Field(description="Total quantity accepted across all items")
    rejected_quantity: int = Field(description="Total quantity rejected across all items")
    defect_description: Optional[str] = Field(
        description="Description of defects found, null if no defects",
        default=None,
    )
    corrective_action: Optional[str] = Field(
        description="Corrective action required, null if not applicable",
        default=None,
    )
    acceptance_report_file_ref: Optional[str] = Field(
        description="Reference to the acceptance report file attachment, null if not uploaded",
        default=None,
    )
    acceptance_status: AcceptanceStatus = Field(
        description="Current status of the acceptance record (pending, in_progress, completed, cancelled)"
    )
    notes: str = Field(description="Additional notes about the acceptance")
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class AcceptanceItem(BaseModel):
    """Represents a line item within an acceptance record"""

    acceptance_item_ref: str = Field(description="Unique identifier for the acceptance item")
    acceptance_record_ref: str = Field(description="Reference to the parent acceptance record")
    goods_receipt_item_ref: str = Field(description="Reference to the associated goods receipt item")
    item_name: str = Field(description="Name of the inspected item")
    inspected_quantity: int = Field(description="Quantity inspected")
    accepted_quantity: int = Field(description="Quantity accepted after inspection")
    rejected_quantity: int = Field(description="Quantity rejected after inspection")
    result: AcceptanceItemResult = Field(
        description="Inspection result for the item (accepted, rejected, conditional)"
    )
    defect_description: Optional[str] = Field(
        description="Description of defects found, null if no defects",
        default=None,
    )
    notes: str = Field(description="Additional notes about the inspected item")
    created_at: str = Field(description="Timestamp when the item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the item was last updated (ISO 8601)")


class ApprovalFlowTemplate(BaseModel):
    """Represents a template defining the approval workflow for procurement processes"""

    approval_flow_template_ref: str = Field(description="Unique identifier for the approval flow template")
    template_name: str = Field(description="Name of the approval flow template")
    template_code: str = Field(description="Short code for the template")
    applicable_type: ApplicableType = Field(
        description="Type of entity this template applies to (purchase_requisition, purchase_order, purchase_contract, purchase_change_request, supplier_onboarding)"
    )
    condition_rules: Dict[str, Any] = Field(
        description="Dictionary of condition rules for template matching (e.g., amount_threshold, department_ref, procurement_category_ref)"
    )
    priority: int = Field(description="Priority for template selection when multiple templates match")
    template_status: ApprovalFlowTemplateStatus = Field(
        description="Current status of the template (active, inactive, deprecated)"
    )
    description: str = Field(description="Description of the approval flow template")
    created_by_ref: str = Field(description="Employee reference of the template creator")
    created_at: str = Field(description="Timestamp when the template was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the template was last updated (ISO 8601)")


class ApprovalFlowNode(BaseModel):
    """Represents a node (step) within an approval flow template"""

    approval_flow_node_ref: str = Field(description="Unique identifier for the approval flow node")
    approval_flow_template_ref: str = Field(description="Reference to the parent approval flow template")
    node_sequence: int = Field(description="Sequence number of the node within the flow")
    node_name: str = Field(description="Name of the approval node")
    approver_type: ApproverType = Field(
        description="Type of approver (employee, role, department_head, direct_manager)"
    )
    approver_ref: Optional[str] = Field(
        description="Reference to the specific approver (employee_ref or role_ref), null for dynamic resolution",
        default=None,
    )
    fallback_approver_ref: Optional[str] = Field(
        description="Reference to the fallback approver if primary is unavailable, null if no fallback",
        default=None,
    )
    auto_approve_hours: Optional[int] = Field(
        description="Hours after which the node auto-approves, null if no auto-approval",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the node was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the node was last updated (ISO 8601)")


class ApprovalInstance(BaseModel):
    """Represents an active instance of an approval flow for a specific target"""

    approval_instance_ref: str = Field(description="Unique identifier for the approval instance")
    approval_flow_template_ref: str = Field(description="Reference to the approval flow template used")
    target_type: str = Field(description="Type of entity being approved (e.g., purchase_requisition, purchase_order)")
    target_ref: str = Field(description="Reference to the entity being approved")
    initiator_ref: str = Field(description="Employee reference of the person who initiated the approval")
    current_node_sequence: int = Field(description="Current node sequence in the approval flow")
    approval_status: ApprovalStatus = Field(
        description="Current status of the approval (in_progress, approved, rejected, cancelled, withdrawn)"
    )
    submitted_at: str = Field(description="Timestamp when the approval was submitted (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the approval was completed, null if still in progress (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the instance was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the instance was last updated (ISO 8601)")


class ApprovalAction(BaseModel):
    """Represents an action taken by an approver within an approval instance"""

    approval_action_ref: str = Field(description="Unique identifier for the approval action")
    approval_instance_ref: str = Field(description="Reference to the parent approval instance")
    node_sequence: int = Field(description="Node sequence at which the action was taken")
    approver_ref: str = Field(description="Employee reference of the approver who took the action")
    action: ApprovalActionType = Field(
        description="Action taken (approve, reject, return, delegate, comment)"
    )
    comments: str = Field(description="Comments provided by the approver")
    acted_at: str = Field(description="Timestamp when the action was taken (ISO 8601)")
    created_at: str = Field(description="Timestamp when the action record was created (ISO 8601)")


class ProcurementPermissionRule(BaseModel):
    """Represents a permission rule governing procurement operations"""

    procurement_permission_rule_ref: str = Field(description="Unique identifier for the procurement permission rule")
    rule_name: str = Field(description="Name of the permission rule")
    rule_code: str = Field(description="Short code for the permission rule")
    employee_ref: Optional[str] = Field(
        description="Reference to a specific employee, null if rule applies broadly",
        default=None,
    )
    role_ref: Optional[str] = Field(
        description="Reference to a role, null if not role-based",
        default=None,
    )
    department_ref: Optional[str] = Field(
        description="Reference to a department, null if not department-scoped",
        default=None,
    )
    procurement_category_ref: Optional[str] = Field(
        description="Reference to a procurement category, null if not category-scoped",
        default=None,
    )
    max_single_amount: Optional[float] = Field(
        description="Maximum amount for a single transaction, null if no limit",
        default=None,
    )
    max_monthly_amount: Optional[float] = Field(
        description="Maximum monthly cumulative amount, null if no limit",
        default=None,
    )
    currency: str = Field(description="Currency code for the amount limits (e.g., CNY, USD)")
    allowed_operations: List[ProcurementPermissionOperation] = Field(
        description="List of allowed procurement operations (create_requisition, create_order, approve, create_contract, manage_supplier, view_reports, export_data)"
    )
    rule_status: ProcurementPermissionRuleStatus = Field(
        description="Current status of the rule (active, inactive, expired)"
    )
    created_by_ref: str = Field(description="Employee reference of the person who created the rule")
    created_at: str = Field(description="Timestamp when the rule was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the rule was last updated (ISO 8601)")


class ProcurementTrainingCourse(BaseModel):
    """Represents a training course related to procurement processes"""

    procurement_training_course_ref: str = Field(description="Unique identifier for the training course")
    course_title: str = Field(description="Title of the training course")
    course_code: str = Field(description="Short code for the course")
    course_type: CourseType = Field(
        description="Type of course (process_training, system_training, compliance, skill_development)"
    )
    content_summary: str = Field(description="Summary of the course content")
    duration_hours: int = Field(description="Duration of the course in hours")
    is_certification_required: bool = Field(
        description="Whether certification is required upon completion"
    )
    certification_validity_months: Optional[int] = Field(
        description="Number of months the certification is valid, null if no certification",
        default=None,
    )
    material_file_ref: Optional[str] = Field(
        description="Reference to the course material file attachment, null if not uploaded",
        default=None,
    )
    course_status: CourseStatus = Field(
        description="Current status of the course (active, archived, draft)"
    )
    created_by_ref: str = Field(description="Employee reference of the course creator")
    created_at: str = Field(description="Timestamp when the course was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the course was last updated (ISO 8601)")


class ProcurementTrainingRecord(BaseModel):
    """Represents an employee's enrollment and completion record for a procurement training course"""

    procurement_training_record_ref: str = Field(description="Unique identifier for the training record")
    procurement_training_course_ref: str = Field(description="Reference to the associated training course")
    employee_ref: str = Field(description="Reference to the employee enrolled in the course")
    enrollment_date: str = Field(description="Date the employee enrolled in the course (ISO 8601 date)")
    completion_date: Optional[str] = Field(
        description="Date the employee completed the course, null if not completed (ISO 8601 date)",
        default=None,
    )
    score: Optional[float] = Field(
        description="Score achieved by the employee, null if not yet assessed",
        default=None,
    )
    certification_number: Optional[str] = Field(
        description="Certification number issued upon completion, null if not certified",
        default=None,
    )
    certification_expiry_date: Optional[str] = Field(
        description="Expiry date of the certification, null if not certified (ISO 8601 date)",
        default=None,
    )
    certificate_file_ref: Optional[str] = Field(
        description="Reference to the certificate file attachment, null if not uploaded",
        default=None,
    )
    record_status: TrainingRecordStatus = Field(
        description="Current status of the training record (enrolled, in_progress, completed, failed, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class ProcurementIssueTicket(BaseModel):
    """Represents an issue ticket related to procurement processes"""

    procurement_issue_ticket_ref: str = Field(description="Unique identifier for the issue ticket")
    ticket_code: str = Field(description="Short code for the issue ticket")
    issue_type: IssueType = Field(
        description="Type of issue (system_error, process_issue, supplier_complaint, delivery_issue, quality_issue, other)"
    )
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource (e.g., purchase_order, supplier, goods_receipt), null if general",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference to the related resource, null if general",
        default=None,
    )
    title: str = Field(description="Title of the issue ticket")
    description: str = Field(description="Detailed description of the issue")
    severity: IssueSeverity = Field(
        description="Severity level of the issue (low, medium, high, critical)"
    )
    reporter_ref: str = Field(description="Employee reference of the person who reported the issue")
    assignee_ref: Optional[str] = Field(
        description="Employee reference of the person assigned to resolve the issue, null if unassigned",
        default=None,
    )
    resolution: Optional[str] = Field(
        description="Description of the resolution, null if not resolved",
        default=None,
    )
    ticket_status: TicketStatus = Field(
        description="Current status of the ticket (open, in_progress, resolved, closed, cancelled)"
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the issue was resolved, null if not resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the ticket was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the ticket was last updated (ISO 8601)")


class PurchaseDB(OfficeDB):
    """Database containing procurement/purchase module data in addition to all base office collaboration tables"""

    procurement_category: Dict[str, ProcurementCategory] = Field(
        description="Dictionary of all procurement categories indexed by procurement_category_ref"
    )
    supplier: Dict[str, Supplier] = Field(
        description="Dictionary of all suppliers indexed by supplier_ref"
    )
    supplier_contact: Dict[str, SupplierContact] = Field(
        description="Dictionary of all supplier contacts indexed by supplier_contact_ref"
    )
    supplier_qualification: Dict[str, SupplierQualification] = Field(
        description="Dictionary of all supplier qualifications indexed by supplier_qualification_ref"
    )
    supplier_category: Dict[str, SupplierCategory] = Field(
        description="Dictionary of all supplier-category associations indexed by supplier_category_ref"
    )
    supplier_evaluation: Dict[str, SupplierEvaluation] = Field(
        description="Dictionary of all supplier evaluations indexed by supplier_evaluation_ref"
    )
    sourcing_project: Dict[str, SourcingProject] = Field(
        description="Dictionary of all sourcing projects indexed by sourcing_project_ref"
    )
    sourcing_supplier: Dict[str, SourcingSupplier] = Field(
        description="Dictionary of all sourcing supplier records indexed by sourcing_supplier_ref"
    )
    quotation: Dict[str, Quotation] = Field(
        description="Dictionary of all quotations indexed by quotation_ref"
    )
    quotation_item: Dict[str, QuotationItem] = Field(
        description="Dictionary of all quotation items indexed by quotation_item_ref"
    )
    purchase_requisition: Dict[str, PurchaseRequisition] = Field(
        description="Dictionary of all purchase requisitions indexed by purchase_requisition_ref"
    )
    requisition_item: Dict[str, RequisitionItem] = Field(
        description="Dictionary of all requisition items indexed by requisition_item_ref"
    )
    purchase_contract: Dict[str, PurchaseContract] = Field(
        description="Dictionary of all purchase contracts indexed by purchase_contract_ref"
    )
    contract_item: Dict[str, ContractItem] = Field(
        description="Dictionary of all contract items indexed by contract_item_ref"
    )
    purchase_order: Dict[str, PurchaseOrder] = Field(
        description="Dictionary of all purchase orders indexed by purchase_order_ref"
    )
    purchase_order_item: Dict[str, PurchaseOrderItem] = Field(
        description="Dictionary of all purchase order items indexed by purchase_order_item_ref"
    )
    purchase_change_request: Dict[str, PurchaseChangeRequest] = Field(
        description="Dictionary of all purchase change requests indexed by purchase_change_request_ref"
    )
    goods_receipt: Dict[str, GoodsReceipt] = Field(
        description="Dictionary of all goods receipts indexed by goods_receipt_ref"
    )
    goods_receipt_item: Dict[str, GoodsReceiptItem] = Field(
        description="Dictionary of all goods receipt items indexed by goods_receipt_item_ref"
    )
    acceptance_record: Dict[str, AcceptanceRecord] = Field(
        description="Dictionary of all acceptance records indexed by acceptance_record_ref"
    )
    acceptance_item: Dict[str, AcceptanceItem] = Field(
        description="Dictionary of all acceptance items indexed by acceptance_item_ref"
    )
    approval_flow_template: Dict[str, ApprovalFlowTemplate] = Field(
        description="Dictionary of all approval flow templates indexed by approval_flow_template_ref"
    )
    approval_flow_node: Dict[str, ApprovalFlowNode] = Field(
        description="Dictionary of all approval flow nodes indexed by approval_flow_node_ref"
    )
    approval_instance: Dict[str, ApprovalInstance] = Field(
        description="Dictionary of all approval instances indexed by approval_instance_ref"
    )
    approval_action: Dict[str, ApprovalAction] = Field(
        description="Dictionary of all approval actions indexed by approval_action_ref"
    )
    procurement_permission_rule: Dict[str, ProcurementPermissionRule] = Field(
        description="Dictionary of all procurement permission rules indexed by procurement_permission_rule_ref"
    )
    procurement_training_course: Dict[str, ProcurementTrainingCourse] = Field(
        description="Dictionary of all procurement training courses indexed by procurement_training_course_ref"
    )
    procurement_training_record: Dict[str, ProcurementTrainingRecord] = Field(
        description="Dictionary of all procurement training records indexed by procurement_training_record_ref"
    )
    procurement_issue_ticket: Dict[str, ProcurementIssueTicket] = Field(
        description="Dictionary of all procurement issue tickets indexed by procurement_issue_ticket_ref"
    )

    def get_statistics(self) -> Dict[str, Any]:
        """
        功能说明（Description）：
            获取采购模块的统计信息，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `Dict[str, Any]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        base_stats = super().get_statistics()
        work_stats = {
            "num_procurement_categories": len(self.procurement_category),
            "num_suppliers": len(self.supplier),
            "num_supplier_contacts": len(self.supplier_contact),
            "num_supplier_qualifications": len(self.supplier_qualification),
            "num_supplier_categories": len(self.supplier_category),
            "num_supplier_evaluations": len(self.supplier_evaluation),
            "num_sourcing_projects": len(self.sourcing_project),
            "num_sourcing_suppliers": len(self.sourcing_supplier),
            "num_quotations": len(self.quotation),
            "num_quotation_items": len(self.quotation_item),
            "num_purchase_requisitions": len(self.purchase_requisition),
            "num_requisition_items": len(self.requisition_item),
            "num_purchase_contracts": len(self.purchase_contract),
            "num_contract_items": len(self.contract_item),
            "num_purchase_orders": len(self.purchase_order),
            "num_purchase_order_items": len(self.purchase_order_item),
            "num_purchase_change_requests": len(self.purchase_change_request),
            "num_goods_receipts": len(self.goods_receipt),
            "num_goods_receipt_items": len(self.goods_receipt_item),
            "num_acceptance_records": len(self.acceptance_record),
            "num_acceptance_items": len(self.acceptance_item),
            "num_approval_flow_templates": len(self.approval_flow_template),
            "num_approval_flow_nodes": len(self.approval_flow_node),
            "num_approval_instances": len(self.approval_instance),
            "num_approval_actions": len(self.approval_action),
            "num_procurement_permission_rules": len(self.procurement_permission_rule),
            "num_procurement_training_courses": len(self.procurement_training_course),
            "num_procurement_training_records": len(self.procurement_training_record),
            "num_procurement_issue_tickets": len(self.procurement_issue_ticket),
        }
        return {**base_stats, **work_stats}