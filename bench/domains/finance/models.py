from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

FinanceAccountType = Literal["settlement", "payroll", "petty_cash", "escrow", "investment", "tax"]
FinanceAccountPurpose = Literal["general", "operating", "capital", "reserve"]
FinanceAccountStatus = Literal["active", "frozen", "closed"]
Currency = Literal["CNY", "USD", "EUR", "GBP", "JPY", "HKD", "SGD", "KRW", "TWD"]

BudgetType = Literal["department", "project", "company", "special"]
BudgetScopeType = Literal["department", "team", "company", "project"]
BudgetStatus = Literal["draft", "submitted", "approved", "rejected", "closed", "frozen"]
FiscalPeriod = Literal["Q1", "Q2", "Q3", "Q4", "H1", "H2", "annual"]

ExpenseCategory = Literal[
    "travel", "accommodation", "meals", "transportation", "office_supplies",
    "software", "hardware", "training", "entertainment", "communication",
    "marketing", "consulting", "other"
]

ExpenseType = Literal["travel", "daily", "project", "entertainment", "training", "other"]
ExpenseReportStatus = Literal[
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "paid", "cancelled"
]

ExpenseLineStatus = Literal["pending", "approved", "rejected", "partial_approved"]

InvoiceType = Literal[
    "vat_special", "vat_general", "electronic", "receipt",
    "train_ticket", "air_ticket", "toll", "other"
]
InvoiceDirection = Literal["inbound", "outbound"]
InvoiceVerificationStatus = Literal["unverified", "verified", "failed", "expired"]
InvoiceStatus = Literal["active", "voided", "lost", "archived"]

InvoiceHeaderType = Literal["company", "individual"]
InvoiceHeaderStatus = Literal["active", "inactive"]

PaymentType = Literal[
    "procurement", "service", "reimbursement", "salary",
    "bonus", "refund", "loan_disbursement", "other"
]
PaymentMethod = Literal["bank_transfer", "check", "cash", "alipay", "wechat_pay", "internal_transfer"]
PaymentRequestStatus = Literal[
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "completed", "cancelled"
]
PaymentUrgency = Literal["normal", "urgent", "critical"]

PaymentChannel = Literal["bank_transfer", "check", "cash", "alipay", "wechat_pay", "internal_transfer"]
PaymentExecutionStatus = Literal["pending", "processing", "completed", "failed", "reversed"]

ReceiptChannel = Literal["bank_transfer", "check", "cash", "alipay", "wechat_pay", "pos", "other"]
ReceiptType = Literal["sales", "service", "refund_return", "investment", "loan_repayment", "other"]
ReconciliationStatus = Literal["unmatched", "matched", "partial_matched", "disputed"]

RefundType = Literal["customer_return", "service_cancellation", "overcharge", "duplicate_payment", "other"]
RefundReasonCategory = Literal[
    "product_defect", "service_issue", "customer_request",
    "billing_error", "policy_compliance", "other"
]
RefundMethod = Literal["original_channel", "bank_transfer", "cash", "credit_note"]
RefundStatus = Literal[
    "draft", "submitted", "under_review", "approved", "rejected",
    "processing", "completed", "cancelled"
]

LoanPurpose = Literal["travel_advance", "project_advance", "emergency", "other"]
EmployeeLoanStatus = Literal["draft", "submitted", "approved", "rejected", "active", "settled", "overdue", "written_off"]

RepaymentMethod = Literal["salary_deduction", "bank_transfer", "cash", "expense_offset"]

SettlementCounterpartyType = Literal["supplier", "customer", "partner", "employee"]
SettlementStatus = Literal["draft", "submitted", "approved", "rejected", "settled", "cancelled"]

FundTransferStatus = Literal["draft", "submitted", "approved", "rejected", "executed", "failed", "cancelled"]

ExchangeRateType = Literal["central_bank", "commercial", "internal"]

TaxType = Literal[
    "corporate_income", "vat", "individual_income", "stamp_duty",
    "urban_maintenance", "education_surcharge", "other"
]
TaxFilingStatus = Literal["draft", "prepared", "filed", "accepted", "rejected", "amended"]

IncomeType = Literal["salary", "bonus", "equity", "allowance", "severance", "other"]
EmployeeTaxFilingStatus = Literal["withheld", "filed", "adjusted", "finalized"]

AccrualType = Literal["expense_accrual", "revenue_accrual", "provision", "prepaid_amortization"]
AccrualEntryStatus = Literal["draft", "posted", "reversed", "cancelled"]

CityTier = Literal["tier_1", "new_tier_1", "tier_2", "tier_3", "other"]
ExpensePolicyStatus = Literal["active", "inactive", "deprecated"]

FinanceTicketCategory = Literal[
    "reimbursement", "payment", "invoice", "budget", "tax",
    "loan", "settlement", "account", "other"
]
FinanceTicketSubcategory = Literal[
    "policy_inquiry", "status_inquiry", "correction", "dispute",
    "system_issue", "approval_escalation", "other"
]
FinanceTicketPriority = Literal["low", "normal", "high", "critical"]
FinanceTicketStatus = Literal["open", "in_progress", "pending_info", "resolved", "closed", "cancelled"]

CreditProductType = Literal["personal_loan", "housing_loan", "education_loan", "emergency_loan", "other"]
CreditRepaymentMethod = Literal["equal_installment", "equal_principal", "bullet", "custom"]
CreditApplicationStatus = Literal[
    "draft", "submitted", "under_review", "approved", "rejected",
    "disbursed", "repaying", "settled", "overdue", "defaulted", "cancelled"
]
CreditRiskLevel = Literal["low", "medium", "high", "very_high"]
CreditScheduleStatus = Literal["pending", "paid", "overdue", "partial_paid", "waived"]

StockBrokerage = Literal["boci", "cicc", "citic", "huatai", "guotai", "other"]
StockMarket = Literal["SSE", "SZSE", "HKEX", "NYSE", "NASDAQ", "other"]
TradeDirection = Literal["buy", "sell"]
OrderType = Literal["limit", "market", "stop", "stop_limit"]
StockOrderStatus = Literal["draft", "submitted", "partial_filled", "filled", "cancelled", "rejected", "expired"]

FinanceApprovalSourceType = Literal[
    "expense_report", "payment_request", "refund", "employee_loan",
    "settlement", "fund_transfer", "budget", "credit_application", "tax_filing"
]
FinanceApproverRole = Literal[
    "direct_manager", "department_head", "finance_manager",
    "finance_director", "cfo", "ceo", "custom"
]
FinanceApprovalAction = Literal["pending", "approved", "rejected", "returned", "delegated", "skipped"]


# --- Models ---


class FinanceAccount(BaseModel):
    """Represents a financial account used for payments, receipts and fund management"""

    finance_account_ref: str = Field(description="Unique identifier for the finance account")
    account_name: str = Field(description="Display name of the finance account")
    account_number: str = Field(description="Bank account number")
    bank_name: str = Field(description="Name of the bank")
    bank_branch: str = Field(description="Branch name of the bank")
    swift_code: Optional[str] = Field(
        description="SWIFT/BIC code for international transfers, null if not applicable",
        default=None,
    )
    currency: Currency = Field(description="Primary currency of the account (CNY, USD, EUR, etc.)")
    account_type: FinanceAccountType = Field(
        description="Type of finance account (settlement, payroll, petty_cash, escrow, investment, tax)"
    )
    account_purpose: FinanceAccountPurpose = Field(
        description="Purpose of the account (general, operating, capital, reserve)"
    )
    account_status: FinanceAccountStatus = Field(
        description="Current status of the account (active, frozen, closed)"
    )
    balance: float = Field(description="Current balance of the account")
    balance_updated_at: str = Field(description="Timestamp when the balance was last updated (ISO 8601)")
    department_ref: Optional[str] = Field(
        description="Reference to the department owning this account, null if company-level",
        default=None,
    )
    managed_by_ref: str = Field(description="Employee reference of the account manager")
    created_at: str = Field(description="Timestamp when the account was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the account was last updated (ISO 8601)")


class Budget(BaseModel):
    """Represents a budget allocation for a fiscal period with spending tracking"""

    budget_ref: str = Field(description="Unique identifier for the budget")
    budget_name: str = Field(description="Name of the budget")
    budget_code: str = Field(description="Short code for the budget")
    fiscal_year: int = Field(description="Fiscal year the budget applies to")
    fiscal_period: FiscalPeriod = Field(
        description="Fiscal period within the year (Q1, Q2, Q3, Q4, H1, H2, annual)"
    )
    budget_type: BudgetType = Field(
        description="Type of budget (department, project, company, special)"
    )
    scope_type: BudgetScopeType = Field(
        description="Scope type of the budget (department, team, company, project)"
    )
    scope_ref: Optional[str] = Field(
        description="Reference to the scoped entity (department_ref, team_ref, etc.), null if company-level",
        default=None,
    )
    parent_budget_ref: Optional[str] = Field(
        description="Reference to the parent budget, null if top-level budget",
        default=None,
    )
    currency: Currency = Field(description="Currency of the budget (CNY, USD, EUR, etc.)")
    total_amount: float = Field(description="Total budgeted amount")
    allocated_amount: float = Field(description="Amount allocated to sub-budgets or budget lines")
    spent_amount: float = Field(description="Amount already spent against this budget")
    frozen_amount: float = Field(description="Amount frozen/reserved pending approval")
    budget_status: BudgetStatus = Field(
        description="Current status of the budget (draft, submitted, approved, rejected, closed, frozen)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the budget was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the budget")
    created_at: str = Field(description="Timestamp when the budget was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the budget was last updated (ISO 8601)")


class BudgetLine(BaseModel):
    """Represents a line item within a budget for a specific expense category"""

    budget_line_ref: str = Field(description="Unique identifier for the budget line")
    budget_ref: str = Field(description="Reference to the parent budget")
    expense_category: ExpenseCategory = Field(
        description="Expense category for this budget line (travel, accommodation, meals, etc.)"
    )
    line_label: str = Field(description="Human-readable label for the budget line")
    planned_amount: float = Field(description="Planned amount for this budget line")
    spent_amount: float = Field(description="Amount already spent against this budget line")
    frozen_amount: float = Field(description="Amount frozen/reserved pending approval")
    created_at: str = Field(description="Timestamp when the budget line was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the budget line was last updated (ISO 8601)")


class ExpenseReport(BaseModel):
    """Represents an expense report submitted by an employee for reimbursement"""

    expense_report_ref: str = Field(description="Unique identifier for the expense report")
    report_number: str = Field(description="Human-readable report number (e.g., ER-2025-000001)")
    applicant_ref: str = Field(description="Employee reference of the applicant")
    department_ref: str = Field(description="Reference to the applicant's department")
    expense_type: ExpenseType = Field(
        description="Type of expense (travel, daily, project, entertainment, training, other)"
    )
    title: str = Field(description="Title or summary of the expense report")
    currency: Currency = Field(description="Currency of the expense report (CNY, USD, EUR, etc.)")
    total_amount: float = Field(description="Total amount claimed in the expense report")
    approved_amount: float = Field(description="Total approved amount after review")
    trip_ref: Optional[str] = Field(
        description="Reference to the associated trip, null if not trip-related",
        default=None,
    )
    budget_ref: Optional[str] = Field(
        description="Reference to the budget this expense is charged against, null if unlinked",
        default=None,
    )
    report_status: ExpenseReportStatus = Field(
        description="Current status of the expense report (draft, submitted, under_review, approved, rejected, processing, paid, cancelled)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the report was submitted, null if draft (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the report was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    paid_at: Optional[str] = Field(
        description="Timestamp when the reimbursement was paid, null if not yet paid (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    notes: str = Field(description="Additional notes about the expense report")
    created_at: str = Field(description="Timestamp when the expense report was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the expense report was last updated (ISO 8601)")


class ExpenseLine(BaseModel):
    """Represents a single line item within an expense report"""

    expense_line_ref: str = Field(description="Unique identifier for the expense line")
    expense_report_ref: str = Field(description="Reference to the parent expense report")
    expense_category: ExpenseCategory = Field(
        description="Expense category (travel, accommodation, meals, transportation, etc.)"
    )
    expense_subcategory: str = Field(description="Subcategory or specific type (e.g., taxi, flight, hotel)")
    description: str = Field(description="Description of the expense item")
    currency: Currency = Field(description="Currency of the expense line (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Claimed amount for this expense line")
    approved_amount: float = Field(description="Approved amount after review")
    expense_date: str = Field(description="Date the expense was incurred (ISO 8601 date)")
    invoice_ref: Optional[str] = Field(
        description="Reference to the associated invoice, null if no invoice",
        default=None,
    )
    receipt_file_ref: Optional[str] = Field(
        description="Reference to the receipt file attachment, null if no receipt uploaded",
        default=None,
    )
    line_status: ExpenseLineStatus = Field(
        description="Current status of the expense line (pending, approved, rejected, partial_approved)"
    )
    rejection_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the expense line was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the expense line was last updated (ISO 8601)")


class Invoice(BaseModel):
    """Represents an invoice record for tax and accounting purposes"""

    invoice_ref: str = Field(description="Unique identifier for the invoice")
    invoice_number: str = Field(description="Invoice number printed on the invoice")
    invoice_code: str = Field(description="Invoice code for tax verification")
    invoice_type: InvoiceType = Field(
        description="Type of invoice (vat_special, vat_general, electronic, receipt, train_ticket, air_ticket, toll, other)"
    )
    invoice_direction: InvoiceDirection = Field(
        description="Direction of the invoice (inbound for received, outbound for issued)"
    )
    invoice_date: str = Field(description="Date the invoice was issued (ISO 8601 date)")
    currency: Currency = Field(description="Currency of the invoice (CNY, USD, EUR, etc.)")
    amount_without_tax: float = Field(description="Invoice amount excluding tax")
    tax_amount: float = Field(description="Tax amount on the invoice")
    total_amount: float = Field(description="Total invoice amount including tax")
    tax_rate: float = Field(description="Tax rate applied (e.g., 0.13 for 13%)")
    seller_name: str = Field(description="Name of the seller/issuer")
    seller_tax_id: str = Field(description="Tax identification number of the seller")
    buyer_name: str = Field(description="Name of the buyer/recipient")
    buyer_tax_id: str = Field(description="Tax identification number of the buyer")
    items_summary: str = Field(description="Summary of items or services on the invoice")
    verification_status: InvoiceVerificationStatus = Field(
        description="Verification status of the invoice (unverified, verified, failed, expired)"
    )
    verification_code: Optional[str] = Field(
        description="Verification code used for tax authority validation, null if not applicable",
        default=None,
    )
    associated_resource_type: Optional[str] = Field(
        description="Type of the associated resource (e.g., expense_report, payment_request), null if unlinked",
        default=None,
    )
    associated_resource_ref: Optional[str] = Field(
        description="Reference ID of the associated resource, null if unlinked",
        default=None,
    )
    invoice_file_ref: Optional[str] = Field(
        description="Reference to the invoice file attachment, null if not uploaded",
        default=None,
    )
    invoice_status: InvoiceStatus = Field(
        description="Current status of the invoice (active, voided, lost, archived)"
    )
    recorded_by_ref: str = Field(description="Employee reference of the person who recorded the invoice")
    created_at: str = Field(description="Timestamp when the invoice was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the invoice was last updated (ISO 8601)")


class InvoiceHeader(BaseModel):
    """Represents an invoice header template for issuing or receiving invoices"""

    invoice_header_ref: str = Field(description="Unique identifier for the invoice header")
    header_type: InvoiceHeaderType = Field(
        description="Type of invoice header (company, individual)"
    )
    company_name: str = Field(description="Company or individual name on the invoice header")
    tax_id: str = Field(description="Tax identification number")
    registered_address: str = Field(description="Registered address for the invoice header")
    registered_phone: str = Field(description="Registered phone number for the invoice header")
    bank_name: str = Field(description="Bank name for the invoice header")
    bank_account: str = Field(description="Bank account number for the invoice header")
    is_default: bool = Field(description="Whether this is the default invoice header")
    header_status: InvoiceHeaderStatus = Field(
        description="Current status of the invoice header (active, inactive)"
    )
    created_at: str = Field(description="Timestamp when the invoice header was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the invoice header was last updated (ISO 8601)")


class PaymentRequest(BaseModel):
    """Represents a payment request submitted for approval and execution"""

    payment_request_ref: str = Field(description="Unique identifier for the payment request")
    request_number: str = Field(description="Human-readable request number (e.g., PR-2025-000001)")
    applicant_ref: str = Field(description="Employee reference of the applicant")
    department_ref: str = Field(description="Reference to the applicant's department")
    payment_type: PaymentType = Field(
        description="Type of payment (procurement, service, reimbursement, salary, bonus, refund, loan_disbursement, other)"
    )
    payment_method: PaymentMethod = Field(
        description="Preferred payment method (bank_transfer, check, cash, alipay, wechat_pay, internal_transfer)"
    )
    currency: Currency = Field(description="Currency of the payment (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Payment amount requested")
    payee_name: str = Field(description="Name of the payee")
    payee_account: str = Field(description="Account number or identifier of the payee")
    payee_bank: str = Field(description="Bank name of the payee")
    source_account_ref: Optional[str] = Field(
        description="Reference to the source finance account, null if not specified",
        default=None,
    )
    associated_resource_type: Optional[str] = Field(
        description="Type of the associated resource (e.g., expense_report, settlement), null if standalone",
        default=None,
    )
    associated_resource_ref: Optional[str] = Field(
        description="Reference ID of the associated resource, null if standalone",
        default=None,
    )
    budget_ref: Optional[str] = Field(
        description="Reference to the budget this payment is charged against, null if unlinked",
        default=None,
    )
    purpose: str = Field(description="Purpose or description of the payment")
    planned_payment_date: str = Field(description="Planned date for the payment (ISO 8601 date)")
    request_status: PaymentRequestStatus = Field(
        description="Current status of the payment request (draft, submitted, under_review, approved, rejected, processing, completed, cancelled)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the request was submitted, null if draft (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the request was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    urgency: PaymentUrgency = Field(
        description="Urgency level of the payment request (normal, urgent, critical)"
    )
    notes: str = Field(description="Additional notes about the payment request")
    created_at: str = Field(description="Timestamp when the payment request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the payment request was last updated (ISO 8601)")


class PaymentExecution(BaseModel):
    """Represents the execution record of a payment request"""

    payment_execution_ref: str = Field(description="Unique identifier for the payment execution")
    payment_request_ref: str = Field(description="Reference to the associated payment request")
    source_account_ref: str = Field(description="Reference to the source finance account")
    transaction_number: str = Field(description="Transaction number from the payment system")
    currency: Currency = Field(description="Currency of the payment (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Amount paid in the execution")
    exchange_rate: Optional[float] = Field(
        description="Exchange rate applied for cross-currency payments, null if same currency",
        default=None,
    )
    settlement_currency: Optional[str] = Field(
        description="Settlement currency if different from payment currency, null if same currency",
        default=None,
    )
    settlement_amount: Optional[float] = Field(
        description="Settlement amount in settlement currency, null if same currency",
        default=None,
    )
    payee_name: str = Field(description="Name of the payee")
    payee_account: str = Field(description="Account number or identifier of the payee")
    payee_bank: str = Field(description="Bank name of the payee")
    payment_channel: PaymentChannel = Field(
        description="Payment channel used (bank_transfer, check, cash, alipay, wechat_pay, internal_transfer)"
    )
    execution_status: PaymentExecutionStatus = Field(
        description="Current status of the execution (pending, processing, completed, failed, reversed)"
    )
    executed_at: Optional[str] = Field(
        description="Timestamp when the payment was executed, null if not yet executed (ISO 8601)",
        default=None,
    )
    executed_by_ref: str = Field(description="Employee reference of the person who executed the payment")
    failure_reason: Optional[str] = Field(
        description="Reason for failure, null if not failed",
        default=None,
    )
    bank_reference: Optional[str] = Field(
        description="Bank reference number for the transaction, null if not available",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the execution record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the execution record was last updated (ISO 8601)")


class ReceiptRecord(BaseModel):
    """Represents a record of money received into a finance account"""

    receipt_record_ref: str = Field(description="Unique identifier for the receipt record")
    receipt_number: str = Field(description="Receipt number for tracking")
    finance_account_ref: str = Field(description="Reference to the finance account that received the funds")
    payer_name: str = Field(description="Name of the payer")
    payer_account: str = Field(description="Account number or identifier of the payer")
    currency: Currency = Field(description="Currency of the receipt (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Amount received")
    receipt_date: str = Field(description="Date the receipt was recorded (ISO 8601 date)")
    receipt_channel: ReceiptChannel = Field(
        description="Channel through which the payment was received (bank_transfer, check, cash, alipay, wechat_pay, pos, other)"
    )
    receipt_type: ReceiptType = Field(
        description="Type of receipt (sales, service, refund_return, investment, loan_repayment, other)"
    )
    reconciliation_status: ReconciliationStatus = Field(
        description="Reconciliation status (unmatched, matched, partial_matched, disputed)"
    )
    matched_resource_type: Optional[str] = Field(
        description="Type of the matched resource (e.g., invoice, settlement), null if unmatched",
        default=None,
    )
    matched_resource_ref: Optional[str] = Field(
        description="Reference ID of the matched resource, null if unmatched",
        default=None,
    )
    bank_reference: Optional[str] = Field(
        description="Bank reference number for the transaction, null if not available",
        default=None,
    )
    notes: str = Field(description="Additional notes about the receipt")
    recorded_by_ref: str = Field(description="Employee reference of the person who recorded the receipt")
    created_at: str = Field(description="Timestamp when the receipt record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the receipt record was last updated (ISO 8601)")


class Refund(BaseModel):
    """Represents a refund request for returning money to a customer or counterparty"""

    refund_ref: str = Field(description="Unique identifier for the refund")
    refund_number: str = Field(description="Human-readable refund number (e.g., RF-2025-000001)")
    applicant_ref: str = Field(description="Employee reference of the refund applicant")
    refund_type: RefundType = Field(
        description="Type of refund (customer_return, service_cancellation, overcharge, duplicate_payment, other)"
    )
    customer_name: str = Field(description="Name of the customer or counterparty receiving the refund")
    original_payment_ref: Optional[str] = Field(
        description="Reference to the original payment execution, null if not applicable",
        default=None,
    )
    original_receipt_ref: Optional[str] = Field(
        description="Reference to the original receipt record, null if not applicable",
        default=None,
    )
    currency: Currency = Field(description="Currency of the refund (CNY, USD, EUR, etc.)")
    refund_amount: float = Field(description="Amount to be refunded")
    reason_category: RefundReasonCategory = Field(
        description="Category of the refund reason (product_defect, service_issue, customer_request, billing_error, policy_compliance, other)"
    )
    reason_detail: str = Field(description="Detailed description of the refund reason")
    refund_method: RefundMethod = Field(
        description="Method of refund (original_channel, bank_transfer, cash, credit_note)"
    )
    target_account: Optional[str] = Field(
        description="Target account for the refund, null if using original channel",
        default=None,
    )
    refund_status: RefundStatus = Field(
        description="Current status of the refund (draft, submitted, under_review, approved, rejected, processing, completed, cancelled)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the refund was submitted, null if draft (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the refund was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    executed_at: Optional[str] = Field(
        description="Timestamp when the refund was executed, null if not yet executed (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    notes: str = Field(description="Additional notes about the refund")
    created_at: str = Field(description="Timestamp when the refund was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the refund was last updated (ISO 8601)")


class EmployeeLoan(BaseModel):
    """Represents a loan or advance given to an employee"""

    employee_loan_ref: str = Field(description="Unique identifier for the employee loan")
    loan_number: str = Field(description="Human-readable loan number (e.g., EL-2025-000001)")
    borrower_ref: str = Field(description="Employee reference of the borrower")
    department_ref: str = Field(description="Reference to the borrower's department")
    loan_purpose: LoanPurpose = Field(
        description="Purpose of the loan (travel_advance, project_advance, emergency, other)"
    )
    currency: Currency = Field(description="Currency of the loan (CNY, USD, EUR, etc.)")
    loan_amount: float = Field(description="Total loan amount")
    repaid_amount: float = Field(description="Amount already repaid")
    outstanding_amount: float = Field(description="Outstanding amount remaining")
    loan_date: str = Field(description="Date the loan was issued (ISO 8601 date)")
    due_date: str = Field(description="Due date for loan repayment (ISO 8601 date)")
    loan_status: EmployeeLoanStatus = Field(
        description="Current status of the loan (draft, submitted, approved, rejected, active, settled, overdue, written_off)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the loan was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    disbursed_at: Optional[str] = Field(
        description="Timestamp when the loan was disbursed, null if not yet disbursed (ISO 8601)",
        default=None,
    )
    settled_at: Optional[str] = Field(
        description="Timestamp when the loan was fully settled, null if not yet settled (ISO 8601)",
        default=None,
    )
    offset_expense_report_ref: Optional[str] = Field(
        description="Reference to the expense report used to offset this loan, null if not offset",
        default=None,
    )
    notes: str = Field(description="Additional notes about the loan")
    created_at: str = Field(description="Timestamp when the loan record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the loan record was last updated (ISO 8601)")


class LoanRepayment(BaseModel):
    """Represents a repayment record against an employee loan"""

    loan_repayment_ref: str = Field(description="Unique identifier for the loan repayment")
    employee_loan_ref: str = Field(description="Reference to the associated employee loan")
    repayment_amount: float = Field(description="Amount repaid in this transaction")
    repayment_method: RepaymentMethod = Field(
        description="Method of repayment (salary_deduction, bank_transfer, cash, expense_offset)"
    )
    repayment_date: str = Field(description="Date the repayment was made (ISO 8601 date)")
    notes: str = Field(description="Additional notes about the repayment")
    created_at: str = Field(description="Timestamp when the repayment record was created (ISO 8601)")


class Settlement(BaseModel):
    """Represents a settlement with an external counterparty for a given period"""

    settlement_ref: str = Field(description="Unique identifier for the settlement")
    settlement_number: str = Field(description="Human-readable settlement number (e.g., ST-2025-000001)")
    counterparty_type: SettlementCounterpartyType = Field(
        description="Type of counterparty (supplier, customer, partner, employee)"
    )
    counterparty_name: str = Field(description="Name of the counterparty")
    counterparty_id: str = Field(description="Identifier of the counterparty (e.g., tax ID or vendor code)")
    settlement_period_start: str = Field(description="Start date of the settlement period (ISO 8601 date)")
    settlement_period_end: str = Field(description="End date of the settlement period (ISO 8601 date)")
    currency: Currency = Field(description="Currency of the settlement (CNY, USD, EUR, etc.)")
    gross_amount: float = Field(description="Gross amount before adjustments")
    adjustment_amount: float = Field(description="Adjustment amount (discounts, penalties, etc.)")
    net_amount: float = Field(description="Net amount after adjustments")
    settlement_status: SettlementStatus = Field(
        description="Current status of the settlement (draft, submitted, approved, rejected, settled, cancelled)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the settlement was submitted, null if draft (ISO 8601)",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the settlement was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    settled_at: Optional[str] = Field(
        description="Timestamp when the settlement was completed, null if not yet settled (ISO 8601)",
        default=None,
    )
    payment_request_ref: Optional[str] = Field(
        description="Reference to the associated payment request, null if not yet created",
        default=None,
    )
    notes: str = Field(description="Additional notes about the settlement")
    prepared_by_ref: str = Field(description="Employee reference of the person who prepared the settlement")
    created_at: str = Field(description="Timestamp when the settlement was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the settlement was last updated (ISO 8601)")


class SettlementLine(BaseModel):
    """Represents a line item within a settlement"""

    settlement_line_ref: str = Field(description="Unique identifier for the settlement line")
    settlement_ref: str = Field(description="Reference to the parent settlement")
    description: str = Field(description="Description of the settlement line item")
    quantity: int = Field(description="Quantity of items or units")
    unit_price: float = Field(description="Unit price of the item")
    amount: float = Field(description="Total amount for this line (quantity × unit_price)")
    tax_rate: float = Field(description="Tax rate applied to this line (e.g., 0.13 for 13%)")
    tax_amount: float = Field(description="Tax amount for this line")
    invoice_ref: Optional[str] = Field(
        description="Reference to the associated invoice, null if no invoice",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the settlement line was created (ISO 8601)")


class FundTransfer(BaseModel):
    """Represents an internal fund transfer between finance accounts"""

    fund_transfer_ref: str = Field(description="Unique identifier for the fund transfer")
    transfer_number: str = Field(description="Human-readable transfer number (e.g., FT-2025-000001)")
    applicant_ref: str = Field(description="Employee reference of the transfer applicant")
    source_account_ref: str = Field(description="Reference to the source finance account")
    target_account_ref: str = Field(description="Reference to the target finance account")
    currency: Currency = Field(description="Currency of the transfer (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Transfer amount in source currency")
    exchange_rate: Optional[float] = Field(
        description="Exchange rate applied for cross-currency transfers, null if same currency",
        default=None,
    )
    target_currency: Optional[str] = Field(
        description="Target currency if different from source, null if same currency",
        default=None,
    )
    target_amount: Optional[float] = Field(
        description="Amount in target currency, null if same currency",
        default=None,
    )
    transfer_reason: str = Field(description="Reason or purpose for the fund transfer")
    transfer_status: FundTransferStatus = Field(
        description="Current status of the transfer (draft, submitted, approved, rejected, executed, failed, cancelled)"
    )
    current_approver_ref: Optional[str] = Field(
        description="Employee reference of the current approver, null if not in approval",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the transfer was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    executed_at: Optional[str] = Field(
        description="Timestamp when the transfer was executed, null if not yet executed (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the fund transfer")
    created_at: str = Field(description="Timestamp when the fund transfer was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the fund transfer was last updated (ISO 8601)")


class ExchangeRate(BaseModel):
    """Represents an exchange rate between two currencies for a given date"""

    exchange_rate_ref: str = Field(description="Unique identifier for the exchange rate entry")
    source_currency: Currency = Field(description="Source currency code (e.g., USD)")
    target_currency: Currency = Field(description="Target currency code (e.g., CNY)")
    rate: float = Field(description="Exchange rate (1 unit of source = rate units of target)")
    rate_type: ExchangeRateType = Field(
        description="Type of exchange rate (central_bank, commercial, internal)"
    )
    effective_date: str = Field(description="Date the exchange rate is effective (ISO 8601 date)")
    created_at: str = Field(description="Timestamp when the exchange rate was created (ISO 8601)")


class TaxFiling(BaseModel):
    """Represents a tax filing record for a specific tax type and period"""

    tax_filing_ref: str = Field(description="Unique identifier for the tax filing")
    filing_number: str = Field(description="Human-readable filing number (e.g., TF-2025-000001)")
    tax_type: TaxType = Field(
        description="Type of tax (corporate_income, vat, individual_income, stamp_duty, urban_maintenance, education_surcharge, other)"
    )
    filing_period_start: str = Field(description="Start date of the filing period (ISO 8601 date)")
    filing_period_end: str = Field(description="End date of the filing period (ISO 8601 date)")
    filing_deadline: str = Field(description="Deadline for filing (ISO 8601 date)")
    currency: Currency = Field(description="Currency of the tax filing (CNY, USD, EUR, etc.)")
    taxable_amount: float = Field(description="Taxable amount before deductions")
    tax_rate: float = Field(description="Tax rate applied (e.g., 0.25 for 25%)")
    tax_amount: float = Field(description="Calculated tax amount before deductions")
    deductions_amount: float = Field(description="Total deductions applied")
    payable_amount: float = Field(description="Final payable tax amount after deductions")
    filing_status: TaxFilingStatus = Field(
        description="Current status of the filing (draft, prepared, filed, accepted, rejected, amended)"
    )
    filed_at: Optional[str] = Field(
        description="Timestamp when the filing was submitted, null if not yet filed (ISO 8601)",
        default=None,
    )
    filed_by_ref: str = Field(description="Employee reference of the person responsible for filing")
    confirmation_number: Optional[str] = Field(
        description="Confirmation number from the tax authority, null if not yet filed",
        default=None,
    )
    attachment_file_ref: Optional[str] = Field(
        description="Reference to the filing attachment file, null if not uploaded",
        default=None,
    )
    notes: str = Field(description="Additional notes about the tax filing")
    created_at: str = Field(description="Timestamp when the tax filing was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the tax filing was last updated (ISO 8601)")


class EmployeeTaxRecord(BaseModel):
    """Represents an individual employee's tax withholding record for a given period"""

    employee_tax_record_ref: str = Field(description="Unique identifier for the employee tax record")
    employee_ref: str = Field(description="Reference to the employee")
    tax_period: str = Field(description="Tax period in YYYY-MM format (e.g., 2025-01)")
    gross_income: float = Field(description="Gross income for the period")
    income_type: IncomeType = Field(
        description="Type of income (salary, bonus, equity, allowance, severance, other)"
    )
    taxable_income: float = Field(description="Taxable income after exemptions and deductions")
    tax_exempt_amount: float = Field(description="Tax-exempt threshold amount (e.g., 5000.00 for China)")
    social_insurance_deduction: float = Field(description="Social insurance deduction amount")
    housing_fund_deduction: float = Field(description="Housing provident fund deduction amount")
    special_additional_deductions: Dict[str, float] = Field(
        description="Dictionary of special additional deductions (children_education, continuing_education, housing_loan_interest, housing_rent, elderly_care, infant_care, serious_illness)"
    )
    other_deductions: float = Field(description="Other miscellaneous deductions")
    cumulative_income_ytd: float = Field(description="Cumulative gross income year-to-date")
    cumulative_tax_ytd: float = Field(description="Cumulative tax withheld year-to-date")
    tax_rate_applied: float = Field(description="Tax rate applied for this period (e.g., 0.10 for 10%)")
    quick_deduction: float = Field(description="Quick deduction amount based on the tax bracket")
    tax_withheld: float = Field(description="Tax amount withheld for this period")
    tax_paid: float = Field(description="Tax amount actually paid/remitted for this period")
    filing_status: EmployeeTaxFilingStatus = Field(
        description="Filing status of the employee tax record (withheld, filed, adjusted, finalized)"
    )
    notes: str = Field(description="Additional notes about the employee tax record")
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class AccrualEntry(BaseModel):
    """Represents an accrual or prepaid amortization entry for accounting purposes"""

    accrual_entry_ref: str = Field(description="Unique identifier for the accrual entry")
    entry_number: str = Field(description="Human-readable entry number (e.g., AC-2025-000001)")
    accrual_type: AccrualType = Field(
        description="Type of accrual (expense_accrual, revenue_accrual, provision, prepaid_amortization)"
    )
    accounting_period: str = Field(description="Accounting period in YYYY-MM format (e.g., 2025-01)")
    department_ref: Optional[str] = Field(
        description="Reference to the department, null if company-level",
        default=None,
    )
    expense_category: str = Field(description="Expense or revenue category for the accrual")
    description: str = Field(description="Description of the accrual entry")
    currency: Currency = Field(description="Currency of the accrual (CNY, USD, EUR, etc.)")
    amount: float = Field(description="Accrual amount")
    reversal_period: Optional[str] = Field(
        description="Period in which the accrual will be reversed (YYYY-MM), null if not applicable",
        default=None,
    )
    is_reversed: bool = Field(description="Whether the accrual has been reversed")
    reversed_at: Optional[str] = Field(
        description="Timestamp when the accrual was reversed, null if not reversed (ISO 8601)",
        default=None,
    )
    entry_status: AccrualEntryStatus = Field(
        description="Current status of the accrual entry (draft, posted, reversed, cancelled)"
    )
    prepared_by_ref: str = Field(description="Employee reference of the person who prepared the entry")
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the accrual entry was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the accrual entry was last updated (ISO 8601)")


class ExpensePolicy(BaseModel):
    """Represents an expense policy defining limits and rules for a specific expense category"""

    expense_policy_ref: str = Field(description="Unique identifier for the expense policy")
    policy_name: str = Field(description="Name of the expense policy")
    policy_code: str = Field(description="Short code for the expense policy")
    expense_category: ExpenseCategory = Field(
        description="Expense category this policy applies to (travel, accommodation, meals, etc.)"
    )
    applicable_position_levels: List[int] = Field(
        description="List of position levels this policy applies to"
    )
    applicable_worker_types: List[str] = Field(
        description="List of worker types this policy applies to (e.g., full_time, intern)"
    )
    city_tier: CityTier = Field(
        description="City tier this policy applies to (tier_1, new_tier_1, tier_2, tier_3, other)"
    )
    currency: Currency = Field(description="Currency of the policy limits (CNY, USD, EUR, etc.)")
    daily_limit: Optional[float] = Field(
        description="Daily spending limit, null if not applicable",
        default=None,
    )
    per_occurrence_limit: Optional[float] = Field(
        description="Per-occurrence spending limit, null if not applicable",
        default=None,
    )
    monthly_limit: Optional[float] = Field(
        description="Monthly spending limit, null if not applicable",
        default=None,
    )
    requires_invoice: bool = Field(description="Whether an invoice is required for this expense category")
    requires_pre_approval: bool = Field(description="Whether pre-approval is required before incurring the expense")
    policy_detail: str = Field(description="Detailed description of the policy rules and conditions")
    effective_from: str = Field(description="Date from which the policy is effective (ISO 8601 date)")
    effective_to: Optional[str] = Field(
        description="Date until which the policy is effective, null if no end date (ISO 8601 date)",
        default=None,
    )
    policy_status: ExpensePolicyStatus = Field(
        description="Current status of the expense policy (active, inactive, deprecated)"
    )
    created_at: str = Field(description="Timestamp when the policy was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the policy was last updated (ISO 8601)")


class FinanceTicket(BaseModel):
    """Represents a finance-related support ticket or inquiry"""

    finance_ticket_ref: str = Field(description="Unique identifier for the finance ticket")
    ticket_number: str = Field(description="Human-readable ticket number (e.g., FT-2025-000001)")
    requester_ref: str = Field(description="Employee reference of the ticket requester")
    ticket_category: FinanceTicketCategory = Field(
        description="Category of the ticket (reimbursement, payment, invoice, budget, tax, loan, settlement, account, other)"
    )
    ticket_subcategory: FinanceTicketSubcategory = Field(
        description="Subcategory of the ticket (policy_inquiry, status_inquiry, correction, dispute, system_issue, approval_escalation, other)"
    )
    subject: str = Field(description="Subject line of the ticket")
    description: str = Field(description="Detailed description of the issue or inquiry")
    priority: FinanceTicketPriority = Field(
        description="Priority level of the ticket (low, normal, high, critical)"
    )
    ticket_status: FinanceTicketStatus = Field(
        description="Current status of the ticket (open, in_progress, pending_info, resolved, closed, cancelled)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the assigned handler, null if unassigned",
        default=None,
    )
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource (e.g., expense_report, payment_request), null if general inquiry",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference ID of the related resource, null if general inquiry",
        default=None,
    )
    resolution: Optional[str] = Field(
        description="Resolution description, null if not yet resolved",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the ticket was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the ticket was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the ticket was last updated (ISO 8601)")


class CreditApplication(BaseModel):
    """Represents a credit or loan application submitted by an employee"""

    credit_application_ref: str = Field(description="Unique identifier for the credit application")
    application_number: str = Field(description="Human-readable application number (e.g., CA-2025-000001)")
    applicant_ref: str = Field(description="Employee reference of the applicant")
    product_type: CreditProductType = Field(
        description="Type of credit product (personal_loan, housing_loan, education_loan, emergency_loan, other)"
    )
    currency: Currency = Field(description="Currency of the credit application (CNY, USD, EUR, etc.)")
    requested_amount: float = Field(description="Amount requested by the applicant")
    approved_amount: Optional[float] = Field(
        description="Amount approved after review, null if not yet approved",
        default=None,
    )
    interest_rate: Optional[float] = Field(
        description="Annual interest rate applied, null if not yet determined",
        default=None,
    )
    loan_term_months: int = Field(description="Loan term in months")
    repayment_method: CreditRepaymentMethod = Field(
        description="Repayment method (equal_installment, equal_principal, bullet, custom)"
    )
    purpose: str = Field(description="Purpose or reason for the credit application")
    credit_score: Optional[int] = Field(
        description="Applicant's credit score, null if not yet assessed",
        default=None,
    )
    risk_level: Optional[CreditRiskLevel] = Field(
        description="Risk level assessment (low, medium, high, very_high), null if not yet assessed",
        default=None,
    )
    application_status: CreditApplicationStatus = Field(
        description="Current status of the application (draft, submitted, under_review, approved, rejected, disbursed, repaying, settled, overdue, defaulted, cancelled)"
    )
    reviewed_by_ref: Optional[str] = Field(
        description="Employee reference of the reviewer, null if not yet reviewed",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the application was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    disbursed_at: Optional[str] = Field(
        description="Timestamp when the funds were disbursed, null if not yet disbursed (ISO 8601)",
        default=None,
    )
    maturity_date: Optional[str] = Field(
        description="Maturity date of the loan, null if not yet determined (ISO 8601 date)",
        default=None,
    )
    outstanding_balance: Optional[float] = Field(
        description="Current outstanding balance, null if not yet disbursed",
        default=None,
    )
    next_payment_date: Optional[str] = Field(
        description="Date of the next scheduled payment, null if not applicable (ISO 8601 date)",
        default=None,
    )
    next_payment_amount: Optional[float] = Field(
        description="Amount of the next scheduled payment, null if not applicable",
        default=None,
    )
    notes: str = Field(description="Additional notes about the credit application")
    created_at: str = Field(description="Timestamp when the application was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the application was last updated (ISO 8601)")


class CreditRepaymentSchedule(BaseModel):
    """Represents a scheduled repayment installment for a credit application"""

    credit_repayment_schedule_ref: str = Field(description="Unique identifier for the repayment schedule entry")
    credit_application_ref: str = Field(description="Reference to the associated credit application")
    installment_number: int = Field(description="Installment sequence number (starting from 1)")
    due_date: str = Field(description="Due date for this installment (ISO 8601 date)")
    principal_amount: float = Field(description="Principal portion of the installment")
    interest_amount: float = Field(description="Interest portion of the installment")
    total_amount: float = Field(description="Total amount due for this installment")
    paid_amount: float = Field(description="Amount actually paid for this installment")
    paid_at: Optional[str] = Field(
        description="Timestamp when the installment was paid, null if not yet paid (ISO 8601)",
        default=None,
    )
    schedule_status: CreditScheduleStatus = Field(
        description="Current status of the installment (pending, paid, overdue, partial_paid, waived)"
    )
    created_at: str = Field(description="Timestamp when the schedule entry was created (ISO 8601)")


class StockTradeOrder(BaseModel):
    """Represents a stock trade order placed by an employee"""

    stock_trade_order_ref: str = Field(description="Unique identifier for the stock trade order")
    order_number: str = Field(description="Human-readable order number (e.g., SO-2025-000001)")
    employee_ref: str = Field(description="Reference to the employee placing the order")
    brokerage: StockBrokerage = Field(
        description="Brokerage firm handling the order (boci, cicc, citic, huatai, guotai, other)"
    )
    stock_code: str = Field(description="Stock ticker code (e.g., 00700.HK)")
    stock_name: str = Field(description="Name of the stock")
    market: StockMarket = Field(
        description="Stock market (SSE, SZSE, HKEX, NYSE, NASDAQ, other)"
    )
    trade_direction: TradeDirection = Field(
        description="Trade direction (buy, sell)"
    )
    order_type: OrderType = Field(
        description="Order type (limit, market, stop, stop_limit)"
    )
    currency: Currency = Field(description="Currency of the order (CNY, USD, HKD, etc.)")
    quantity: int = Field(description="Number of shares ordered")
    price: float = Field(description="Order price per share (for limit orders)")
    filled_quantity: int = Field(description="Number of shares filled")
    filled_avg_price: float = Field(description="Average fill price per share")
    total_amount: float = Field(description="Total transaction amount")
    commission: float = Field(description="Commission charged by the brokerage")
    stamp_duty: float = Field(description="Stamp duty charged on the transaction")
    order_status: StockOrderStatus = Field(
        description="Current status of the order (draft, submitted, partial_filled, filled, cancelled, rejected, expired)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the order was submitted, null if draft (ISO 8601)",
        default=None,
    )
    filled_at: Optional[str] = Field(
        description="Timestamp when the order was fully filled, null if not yet filled (ISO 8601)",
        default=None,
    )
    cancelled_at: Optional[str] = Field(
        description="Timestamp when the order was cancelled, null if not cancelled (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the trade order")
    created_at: str = Field(description="Timestamp when the order was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the order was last updated (ISO 8601)")


class FinanceApprovalFlow(BaseModel):
    """Represents a step in a finance approval workflow"""

    finance_approval_flow_ref: str = Field(description="Unique identifier for the approval flow step")
    source_type: FinanceApprovalSourceType = Field(
        description="Type of the source document (expense_report, payment_request, refund, employee_loan, settlement, fund_transfer, budget, credit_application, tax_filing)"
    )
    source_ref: str = Field(description="Reference ID of the source document")
    step_order: int = Field(description="Order of this step in the approval flow (starting from 1)")
    approver_ref: str = Field(description="Employee reference of the approver for this step")
    approver_role: FinanceApproverRole = Field(
        description="Role of the approver (direct_manager, department_head, finance_manager, finance_director, cfo, ceo, custom)"
    )
    approval_action: FinanceApprovalAction = Field(
        description="Action taken by the approver (pending, approved, rejected, returned, delegated, skipped)"
    )
    comments: str = Field(description="Comments or remarks from the approver")
    acted_at: Optional[str] = Field(
        description="Timestamp when the approver acted, null if pending (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the approval flow step was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the approval flow step was last updated (ISO 8601)")


class FinanceDB(OfficeDB):
    """Database containing finance module data including accounts, budgets, expenses, invoices, payments, loans, settlements, tax records and more"""

    finance_account: Dict[str, FinanceAccount] = Field(
        description="Dictionary of all finance accounts indexed by finance_account_ref"
    )
    budget: Dict[str, Budget] = Field(
        description="Dictionary of all budgets indexed by budget_ref"
    )
    budget_line: Dict[str, BudgetLine] = Field(
        description="Dictionary of all budget lines indexed by budget_line_ref"
    )
    expense_report: Dict[str, ExpenseReport] = Field(
        description="Dictionary of all expense reports indexed by expense_report_ref"
    )
    expense_line: Dict[str, ExpenseLine] = Field(
        description="Dictionary of all expense lines indexed by expense_line_ref"
    )
    invoice: Dict[str, Invoice] = Field(
        description="Dictionary of all invoices indexed by invoice_ref"
    )
    invoice_header: Dict[str, InvoiceHeader] = Field(
        description="Dictionary of all invoice headers indexed by invoice_header_ref"
    )
    payment_request: Dict[str, PaymentRequest] = Field(
        description="Dictionary of all payment requests indexed by payment_request_ref"
    )
    payment_execution: Dict[str, PaymentExecution] = Field(
        description="Dictionary of all payment executions indexed by payment_execution_ref"
    )
    receipt_record: Dict[str, ReceiptRecord] = Field(
        description="Dictionary of all receipt records indexed by receipt_record_ref"
    )
    refund: Dict[str, Refund] = Field(
        description="Dictionary of all refunds indexed by refund_ref"
    )
    employee_loan: Dict[str, EmployeeLoan] = Field(
        description="Dictionary of all employee loans indexed by employee_loan_ref"
    )
    loan_repayment: Dict[str, LoanRepayment] = Field(
        description="Dictionary of all loan repayments indexed by loan_repayment_ref"
    )
    settlement: Dict[str, Settlement] = Field(
        description="Dictionary of all settlements indexed by settlement_ref"
    )
    settlement_line: Dict[str, SettlementLine] = Field(
        description="Dictionary of all settlement lines indexed by settlement_line_ref"
    )
    fund_transfer: Dict[str, FundTransfer] = Field(
        description="Dictionary of all fund transfers indexed by fund_transfer_ref"
    )
    exchange_rate: Dict[str, ExchangeRate] = Field(
        description="Dictionary of all exchange rates indexed by exchange_rate_ref"
    )
    tax_filing: Dict[str, TaxFiling] = Field(
        description="Dictionary of all tax filings indexed by tax_filing_ref"
    )
    employee_tax_record: Dict[str, EmployeeTaxRecord] = Field(
        description="Dictionary of all employee tax records indexed by employee_tax_record_ref"
    )
    accrual_entry: Dict[str, AccrualEntry] = Field(
        description="Dictionary of all accrual entries indexed by accrual_entry_ref"
    )
    expense_policy: Dict[str, ExpensePolicy] = Field(
        description="Dictionary of all expense policies indexed by expense_policy_ref"
    )
    finance_ticket: Dict[str, FinanceTicket] = Field(
        description="Dictionary of all finance tickets indexed by finance_ticket_ref"
    )
    credit_application: Dict[str, CreditApplication] = Field(
        description="Dictionary of all credit applications indexed by credit_application_ref"
    )
    credit_repayment_schedule: Dict[str, CreditRepaymentSchedule] = Field(
        description="Dictionary of all credit repayment schedules indexed by credit_repayment_schedule_ref"
    )
    stock_trade_order: Dict[str, StockTradeOrder] = Field(
        description="Dictionary of all stock trade orders indexed by stock_trade_order_ref"
    )
    finance_approval_flow: Dict[str, FinanceApprovalFlow] = Field(
        description="Dictionary of all finance approval flow steps indexed by finance_approval_flow_ref"
    )

    def get_statistics(self) -> Dict[str, Any]:
        """
        功能说明（Description）：
            获取财务模块统计信息，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `Dict[str, Any]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        base_stats = super().get_statistics()
        finance_stats = {
            "num_finance_accounts": len(self.finance_account),
            "num_budgets": len(self.budget),
            "num_budget_lines": len(self.budget_line),
            "num_expense_reports": len(self.expense_report),
            "num_expense_lines": len(self.expense_line),
            "num_invoices": len(self.invoice),
            "num_invoice_headers": len(self.invoice_header),
            "num_payment_requests": len(self.payment_request),
            "num_payment_executions": len(self.payment_execution),
            "num_receipt_records": len(self.receipt_record),
            "num_refunds": len(self.refund),
            "num_employee_loans": len(self.employee_loan),
            "num_loan_repayments": len(self.loan_repayment),
            "num_settlements": len(self.settlement),
            "num_settlement_lines": len(self.settlement_line),
            "num_fund_transfers": len(self.fund_transfer),
            "num_exchange_rates": len(self.exchange_rate),
            "num_tax_filings": len(self.tax_filing),
            "num_employee_tax_records": len(self.employee_tax_record),
            "num_accrual_entries": len(self.accrual_entry),
            "num_expense_policies": len(self.expense_policy),
            "num_finance_tickets": len(self.finance_ticket),
            "num_credit_applications": len(self.credit_application),
            "num_credit_repayment_schedules": len(self.credit_repayment_schedule),
            "num_stock_trade_orders": len(self.stock_trade_order),
            "num_finance_approval_flows": len(self.finance_approval_flow),
        }
        return {**base_stats, **finance_stats}