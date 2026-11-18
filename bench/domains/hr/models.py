from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.environment.db import DB
from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

SalaryStructureStatus = Literal["active", "inactive", "expired"]
PayFrequency = Literal["monthly", "bi_weekly", "weekly"]
SalaryCurrency = Literal["CNY", "USD", "EUR", "GBP", "JPY", "KRW", "HKD"]

SalaryComponentType = Literal[
    "base_salary", "housing_allowance", "meal_allowance", "transport_allowance",
    "communication_allowance", "performance_bonus", "year_end_bonus",
    "overtime_pay", "equity_compensation", "sign_on_bonus", "other"
]

PayrollRecordStatus = Literal["draft", "calculated", "approved", "paid", "cancelled"]

PayrollLineItemCategory = Literal["earning", "deduction", "employer_contribution"]
PayrollLineItemType = Literal[
    "base_salary", "bonus", "allowance", "overtime_pay", "commission",
    "pension", "medical", "unemployment", "work_injury", "maternity",
    "housing_fund", "supplementary_housing_fund", "income_tax",
    "commercial_insurance", "other_deduction", "other_earning"
]

BankAccountStatus = Literal["active", "inactive", "closed"]

InsuranceType = Literal["pension", "medical", "unemployment", "work_injury", "maternity"]
SocialInsuranceStatus = Literal["active", "suspended", "terminated"]

HousingFundStatus = Literal["active", "suspended", "terminated"]

CommercialInsuranceCategory = Literal[
    "supplemental_medical", "accident", "life", "critical_illness",
    "dental", "vision", "travel", "other"
]
CommercialInsurancePlanStatus = Literal["active", "inactive", "expired"]

EmployeeCommercialInsuranceStatus = Literal["active", "cancelled", "expired"]

BenefitPlanType = Literal[
    "relocation", "education", "wellness", "meal", "transport",
    "communication", "childcare", "elderly_care", "other"
]
BenefitPlanFrequency = Literal["one_time", "monthly", "quarterly", "yearly"]
BenefitPlanStatus = Literal["active", "inactive", "expired"]

EmployeeBenefitEnrollmentStatus = Literal["active", "cancelled", "expired"]

WorkScheduleType = Literal["standard", "flexible", "shift", "compressed"]
WorkScheduleStatus = Literal["active", "inactive"]

EmployeeWorkScheduleStatus = Literal["active", "inactive"]

HolidayType = Literal["statutory", "company", "regional"]

LeaveType = Literal[
    "annual", "sick", "personal", "marriage", "maternity", "paternity",
    "bereavement", "work_injury", "prenatal_checkup", "nursing",
    "compassionate", "unpaid", "other"
]
LeaveAccrualRule = Literal["yearly", "monthly", "upon_hire", "manual"]
LeavePolicyStatus = Literal["active", "inactive"]

LeaveRequestStatus = Literal["draft", "pending", "approved", "rejected", "cancelled", "withdrawn"]

OvertimeType = Literal["weekday", "weekend", "holiday"]
OvertimeCompensationType = Literal["pay", "time_off", "mixed"]
OvertimeRequestStatus = Literal["draft", "pending", "approved", "rejected", "cancelled"]

ContractType = Literal["fixed_term", "open_ended", "internship", "labor_dispatch", "part_time"]
ProbationStatus = Literal["not_applicable", "in_progress", "passed", "failed", "extended"]
SigningStatus = Literal["draft", "pending_signature", "signed", "expired", "terminated"]
ContractStatus = Literal["active", "expired", "terminated", "renewed"]

EmployeeChangeType = Literal[
    "onboarding", "transfer", "promotion", "demotion", "lateral_move",
    "salary_adjustment", "manager_change", "offboarding", "reinstatement"
]
EmployeeChangeStatus = Literal["draft", "pending", "approved", "completed", "rejected", "cancelled"]

ApprovalFlowStatus = Literal["draft", "pending", "approved", "rejected", "cancelled", "withdrawn"]

ApprovalStepAction = Literal["approved", "rejected", "forwarded", "returned"]
ApprovalStepStatus = Literal["pending", "completed", "skipped", "cancelled"]

RequisitionType = Literal["social", "campus", "internal", "headhunter"]
RequisitionUrgency = Literal["low", "normal", "high", "urgent"]
JobRequisitionStatus = Literal["draft", "open", "on_hold", "filled", "cancelled", "closed"]

CandidateSource = Literal[
    "social_recruitment", "campus_recruitment", "internal_referral",
    "headhunter", "job_board", "company_website", "social_media", "other"
]
CandidateStatus = Literal["active", "inactive", "hired", "blacklisted"]

ApplicationStage = Literal[
    "screening", "phone_screen", "interview", "assessment",
    "offer", "hired", "rejected", "withdrawn"
]
ApplicationStatus = Literal["in_progress", "on_hold", "closed"]

ReferralBonusStatus = Literal["pending", "approved", "paid", "cancelled"]
ReferralRelationship = Literal[
    "former_colleague", "classmate", "friend", "family", "professional_network", "other"
]
ReferralStatus = Literal["active", "inactive", "cancelled"]

InterviewType = Literal[
    "phone_screen", "technical", "behavioral", "case_study",
    "panel", "culture_fit", "hr", "final"
]
InterviewResult = Literal["pass", "fail", "strong_pass", "borderline", "no_show"]
InterviewStatus = Literal["scheduled", "in_progress", "completed", "cancelled", "no_show"]

OfferWorkerType = Literal["full_time", "intern", "campus_recruit", "campus_intern", "contractor"]
OfferStatus = Literal["draft", "pending", "approved", "issued", "accepted", "rejected", "withdrawn", "expired"]

TrainingProgramType = Literal[
    "onboarding", "technical", "leadership", "compliance",
    "soft_skills", "certification", "other"
]
TrainingDeliveryMethod = Literal["online", "in_person", "blended", "self_paced"]
TrainingTargetAudience = Literal["new_hire", "all_employees", "managers", "engineers", "specific_team", "other"]
TrainingProgramStatus = Literal["draft", "active", "completed", "cancelled", "archived"]

TrainingEnrollmentResult = Literal["pass", "fail", "incomplete"]
TrainingEnrollmentStatus = Literal["enrolled", "in_progress", "completed", "dropped", "cancelled"]

ProbationReviewRating = Literal[
    "exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"
]
ProbationReviewRecommendation = Literal["pass", "continue", "extend", "terminate"]
ProbationReviewStatus = Literal["draft", "pending", "completed", "cancelled"]

PerformanceCycleType = Literal["monthly", "quarterly", "semi_annual", "annual"]
PerformanceCycleStatus = Literal["draft", "active", "review", "calibration", "completed", "cancelled"]

PerformanceReviewStatus = Literal[
    "draft", "self_review", "manager_review", "calibration",
    "completed", "acknowledged", "appealed"
]

EquityGrantType = Literal["rsu", "stock_option", "espp", "sar", "phantom"]
EquityVestingSchedule = Literal[
    "4_year_1_year_cliff", "4_year_no_cliff", "3_year_1_year_cliff",
    "immediate", "custom"
]
EquityGrantStatus = Literal["active", "fully_vested", "cancelled", "forfeited", "expired"]

EquityVestingEventStatus = Literal["scheduled", "vested", "cancelled", "forfeited"]

ProfessionalTitleLevel = Literal["junior", "intermediate", "senior", "principal", "fellow"]
ProfessionalTitleStatus = Literal["active", "expired", "revoked"]

TalentSubsidyType = Literal["housing", "education", "relocation", "settlement", "talent_award", "other"]
TalentSubsidyFrequency = Literal["one_time", "monthly", "quarterly", "yearly"]
TalentSubsidyStatus = Literal["active", "suspended", "expired", "cancelled"]

EmployeeRecordType = Literal[
    "hukou", "education", "work_history", "emergency_contact",
    "id_document", "health_check", "background_check", "other"
]
EmployeeRecordStatus = Literal["active", "archived", "expired"]

VisaType = Literal[
    "work_permit", "residence_permit", "business_visa", "tourist_visa",
    "student_visa", "dependent_visa", "permanent_residence", "other"
]
VisaEntryCount = Literal["single", "double", "multiple"]
VisaRecordStatus = Literal["active", "expired", "revoked", "pending_renewal"]

TaxDeclarationStatus = Literal["draft", "filed", "amended", "cancelled"]

TaxSpecialDeductionType = Literal[
    "children_education", "continuing_education", "housing_loan_interest",
    "housing_rent", "elderly_care", "infant_care", "serious_illness"
]
TaxSpecialDeductionStatus = Literal["active", "inactive", "expired"]

ComplianceReportType = Literal["violation", "ethics", "safety", "harassment", "fraud", "other"]
ComplianceReportChannel = Literal["anonymous_hotline", "email", "in_person", "online_form", "manager_report"]
ComplianceReportSeverity = Literal["low", "medium", "high", "critical"]
ComplianceInvestigationStatus = Literal["pending", "investigating", "resolved", "dismissed"]
ComplianceReportStatus = Literal["open", "in_progress", "closed", "dismissed"]

CertificateType = Literal[
    "employment_proof", "income_proof", "resignation_proof",
    "social_insurance_proof", "housing_fund_proof", "reference_letter", "other"
]
CertificateRequestLanguage = Literal["zh-CN", "en-US"]
CertificateRequestStatus = Literal["draft", "pending", "approved", "issued", "rejected", "cancelled"]

HRServiceCategory = Literal[
    "hotline", "policy_inquiry", "document_request", "system_issue",
    "complaint", "suggestion", "onboarding_support", "offboarding_support", "other"
]
HRServicePriority = Literal["low", "normal", "high", "urgent"]
HRServiceRequestStatus = Literal["open", "in_progress", "resolved", "closed", "cancelled"]


# --- Models ---


class SalaryStructure(BaseModel):
    """Represents an employee's salary structure with base salary and pay configuration"""

    salary_structure_ref: str = Field(description="Unique identifier for the salary structure")
    employee_ref: str = Field(description="Reference to the employee")
    effective_date: str = Field(description="Date when the salary structure becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the salary structure expires, null if currently active (ISO 8601 date)",
        default=None,
    )
    base_salary: float = Field(description="Base salary amount")
    currency: SalaryCurrency = Field(description="Currency of the salary (CNY, USD, EUR, GBP, JPY, KRW, HKD)")
    pay_frequency: PayFrequency = Field(description="Pay frequency (monthly, bi_weekly, weekly)")
    status: SalaryStructureStatus = Field(description="Current status of the salary structure (active, inactive, expired)")
    approved_by_ref: str = Field(description="Employee reference of the person who approved the salary structure")
    created_at: str = Field(description="Timestamp when the salary structure was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the salary structure was last updated (ISO 8601)")


class SalaryComponent(BaseModel):
    """Represents a component of a salary structure such as base salary, allowance or bonus"""

    salary_component_ref: str = Field(description="Unique identifier for the salary component")
    salary_structure_ref: str = Field(description="Reference to the parent salary structure")
    component_type: SalaryComponentType = Field(
        description="Type of salary component (base_salary, housing_allowance, meal_allowance, transport_allowance, communication_allowance, performance_bonus, year_end_bonus, overtime_pay, equity_compensation, sign_on_bonus, other)"
    )
    component_name: str = Field(description="Display name of the salary component")
    amount: float = Field(description="Amount of the salary component")
    currency: SalaryCurrency = Field(description="Currency of the component amount")
    is_taxable: bool = Field(description="Whether this component is subject to taxation")
    is_recurring: bool = Field(description="Whether this component recurs each pay period")
    effective_date: str = Field(description="Date when the component becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the component expires, null if no expiry (ISO 8601 date)",
        default=None,
    )
    description: str = Field(description="Description of the salary component")
    created_at: str = Field(description="Timestamp when the salary component was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the salary component was last updated (ISO 8601)")


class PayrollRecord(BaseModel):
    """Represents a payroll record for an employee for a specific pay period"""

    payroll_record_ref: str = Field(description="Unique identifier for the payroll record")
    employee_ref: str = Field(description="Reference to the employee")
    pay_period_start: str = Field(description="Start date of the pay period (ISO 8601 date)")
    pay_period_end: str = Field(description="End date of the pay period (ISO 8601 date)")
    gross_amount: float = Field(description="Total gross amount before deductions")
    net_amount: float = Field(description="Net amount after all deductions")
    total_deductions: float = Field(description="Total amount of deductions")
    currency: SalaryCurrency = Field(description="Currency of the payroll amounts")
    pay_date: str = Field(description="Date when the payment was or will be made (ISO 8601 date)")
    bank_account_ref: str = Field(description="Reference to the bank account for payment")
    status: PayrollRecordStatus = Field(description="Current status of the payroll record (draft, calculated, approved, paid, cancelled)")
    created_at: str = Field(description="Timestamp when the payroll record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the payroll record was last updated (ISO 8601)")


class PayrollLineItem(BaseModel):
    """Represents a single line item in a payroll record such as an earning or deduction"""

    payroll_line_item_ref: str = Field(description="Unique identifier for the payroll line item")
    payroll_record_ref: str = Field(description="Reference to the parent payroll record")
    item_category: PayrollLineItemCategory = Field(
        description="Category of the line item (earning, deduction, employer_contribution)"
    )
    item_type: PayrollLineItemType = Field(
        description="Type of the line item (base_salary, bonus, allowance, overtime_pay, commission, pension, medical, unemployment, work_injury, maternity, housing_fund, supplementary_housing_fund, income_tax, commercial_insurance, other_deduction, other_earning)"
    )
    item_name: str = Field(description="Display name of the line item")
    amount: float = Field(description="Amount of the line item")
    description: str = Field(description="Description of the line item")
    created_at: str = Field(description="Timestamp when the line item was created (ISO 8601)")


class BankAccount(BaseModel):
    """Represents an employee's bank account for salary payment"""

    bank_account_ref: str = Field(description="Unique identifier for the bank account")
    employee_ref: str = Field(description="Reference to the employee")
    bank_name: str = Field(description="Name of the bank")
    branch_name: str = Field(description="Name of the bank branch")
    account_number_masked: str = Field(description="Masked bank account number (e.g., ****1234)")
    account_holder_name: str = Field(description="Name of the account holder")
    is_primary: bool = Field(description="Whether this is the employee's primary bank account for salary payment")
    status: BankAccountStatus = Field(description="Current status of the bank account (active, inactive, closed)")
    effective_date: str = Field(description="Date when the bank account becomes effective (ISO 8601 date)")
    created_at: str = Field(description="Timestamp when the bank account record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the bank account record was last updated (ISO 8601)")


class SocialInsurance(BaseModel):
    """Represents an employee's social insurance enrollment with contribution details"""

    social_insurance_ref: str = Field(description="Unique identifier for the social insurance record")
    employee_ref: str = Field(description="Reference to the employee")
    insurance_city: str = Field(description="City where the social insurance is registered")
    insurance_type: InsuranceType = Field(
        description="Type of social insurance (pension, medical, unemployment, work_injury, maternity)"
    )
    base_amount: float = Field(description="Base amount for calculating contributions")
    employee_rate: float = Field(description="Employee contribution rate as a decimal (e.g., 0.08 for 8%)")
    employer_rate: float = Field(description="Employer contribution rate as a decimal (e.g., 0.16 for 16%)")
    employee_amount: float = Field(description="Employee contribution amount per period")
    employer_amount: float = Field(description="Employer contribution amount per period")
    effective_date: str = Field(description="Date when the insurance becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the insurance expires, null if currently active (ISO 8601 date)",
        default=None,
    )
    status: SocialInsuranceStatus = Field(description="Current status of the social insurance (active, suspended, terminated)")
    created_at: str = Field(description="Timestamp when the social insurance record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the social insurance record was last updated (ISO 8601)")


class HousingFund(BaseModel):
    """Represents an employee's housing provident fund enrollment with contribution details"""

    housing_fund_ref: str = Field(description="Unique identifier for the housing fund record")
    employee_ref: str = Field(description="Reference to the employee")
    fund_city: str = Field(description="City where the housing fund is registered")
    fund_account_number: str = Field(description="Housing fund account number")
    base_amount: float = Field(description="Base amount for calculating contributions")
    employee_rate: float = Field(description="Employee contribution rate as a decimal (e.g., 0.12 for 12%)")
    employer_rate: float = Field(description="Employer contribution rate as a decimal (e.g., 0.12 for 12%)")
    employee_amount: float = Field(description="Employee contribution amount per period")
    employer_amount: float = Field(description="Employer contribution amount per period")
    is_supplementary: bool = Field(description="Whether this is a supplementary housing fund")
    effective_date: str = Field(description="Date when the housing fund becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the housing fund expires, null if currently active (ISO 8601 date)",
        default=None,
    )
    status: HousingFundStatus = Field(description="Current status of the housing fund (active, suspended, terminated)")
    created_at: str = Field(description="Timestamp when the housing fund record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the housing fund record was last updated (ISO 8601)")


class CommercialInsurance(BaseModel):
    """Represents a commercial insurance plan offered by the organization"""

    commercial_insurance_ref: str = Field(description="Unique identifier for the commercial insurance plan")
    plan_name: str = Field(description="Name of the insurance plan")
    insurance_provider: str = Field(description="Name of the insurance provider")
    insurance_category: CommercialInsuranceCategory = Field(
        description="Category of commercial insurance (supplemental_medical, accident, life, critical_illness, dental, vision, travel, other)"
    )
    coverage_description: str = Field(description="Description of the insurance coverage")
    employer_paid: bool = Field(description="Whether the premium is fully paid by the employer")
    premium_amount: float = Field(description="Premium amount per period")
    currency: SalaryCurrency = Field(description="Currency of the premium amount")
    plan_status: CommercialInsurancePlanStatus = Field(
        description="Current status of the insurance plan (active, inactive, expired)"
    )
    created_at: str = Field(description="Timestamp when the insurance plan was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the insurance plan was last updated (ISO 8601)")


class EmployeeCommercialInsurance(BaseModel):
    """Represents the enrollment of an employee in a commercial insurance plan"""

    employee_commercial_insurance_ref: str = Field(description="Unique identifier for the employee commercial insurance enrollment")
    employee_ref: str = Field(description="Reference to the employee")
    commercial_insurance_ref: str = Field(description="Reference to the commercial insurance plan")
    coverage_start_date: str = Field(description="Start date of the coverage (ISO 8601 date)")
    coverage_end_date: Optional[str] = Field(
        description="End date of the coverage, null if ongoing (ISO 8601 date)",
        default=None,
    )
    status: EmployeeCommercialInsuranceStatus = Field(
        description="Current status of the enrollment (active, cancelled, expired)"
    )
    created_at: str = Field(description="Timestamp when the enrollment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the enrollment was last updated (ISO 8601)")


class BenefitPlan(BaseModel):
    """Represents a benefit plan offered by the organization"""

    benefit_plan_ref: str = Field(description="Unique identifier for the benefit plan")
    plan_name: str = Field(description="Name of the benefit plan")
    plan_type: BenefitPlanType = Field(
        description="Type of benefit plan (relocation, education, wellness, meal, transport, communication, childcare, elderly_care, other)"
    )
    description: str = Field(description="Description of the benefit plan")
    eligibility_criteria: str = Field(description="Eligibility criteria for the benefit plan")
    amount: float = Field(description="Benefit amount per period")
    currency: SalaryCurrency = Field(description="Currency of the benefit amount")
    frequency: BenefitPlanFrequency = Field(description="Frequency of the benefit (one_time, monthly, quarterly, yearly)")
    status: BenefitPlanStatus = Field(description="Current status of the benefit plan (active, inactive, expired)")
    created_at: str = Field(description="Timestamp when the benefit plan was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the benefit plan was last updated (ISO 8601)")


class EmployeeBenefitEnrollment(BaseModel):
    """Represents the enrollment of an employee in a benefit plan"""

    employee_benefit_enrollment_ref: str = Field(description="Unique identifier for the employee benefit enrollment")
    employee_ref: str = Field(description="Reference to the employee")
    benefit_plan_ref: str = Field(description="Reference to the benefit plan")
    enrollment_date: str = Field(description="Date when the employee enrolled in the benefit plan (ISO 8601 date)")
    end_date: Optional[str] = Field(
        description="Date when the enrollment ends, null if ongoing (ISO 8601 date)",
        default=None,
    )
    status: EmployeeBenefitEnrollmentStatus = Field(
        description="Current status of the enrollment (active, cancelled, expired)"
    )
    created_at: str = Field(description="Timestamp when the enrollment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the enrollment was last updated (ISO 8601)")


class WorkSchedule(BaseModel):
    """Represents a work schedule template defining working hours and days"""

    work_schedule_ref: str = Field(description="Unique identifier for the work schedule")
    schedule_name: str = Field(description="Name of the work schedule")
    schedule_code: str = Field(description="Short code for the work schedule")
    schedule_type: WorkScheduleType = Field(
        description="Type of work schedule (standard, flexible, shift, compressed)"
    )
    work_start_time: str = Field(description="Daily work start time (HH:MM format)")
    work_end_time: str = Field(description="Daily work end time (HH:MM format)")
    break_start_time: Optional[str] = Field(
        description="Break start time, null if no designated break (HH:MM format)",
        default=None,
    )
    break_end_time: Optional[str] = Field(
        description="Break end time, null if no designated break (HH:MM format)",
        default=None,
    )
    work_days_per_week: str = Field(
        description="Comma-separated list of working days (1=Monday, 7=Sunday, e.g., '1,2,3,4,5')"
    )
    hours_per_day: float = Field(description="Standard working hours per day")
    flexible_minutes: int = Field(description="Flexible minutes allowed for clock-in/out, 0 if not flexible")
    description: str = Field(description="Description of the work schedule")
    status: WorkScheduleStatus = Field(description="Current status of the work schedule (active, inactive)")
    created_at: str = Field(description="Timestamp when the work schedule was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the work schedule was last updated (ISO 8601)")


class EmployeeWorkSchedule(BaseModel):
    """Represents the assignment of a work schedule to an employee"""

    employee_work_schedule_ref: str = Field(description="Unique identifier for the employee work schedule assignment")
    employee_ref: str = Field(description="Reference to the employee")
    work_schedule_ref: str = Field(description="Reference to the work schedule")
    effective_date: str = Field(description="Date when the schedule assignment becomes effective (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Date when the schedule assignment expires, null if currently active (ISO 8601 date)",
        default=None,
    )
    status: EmployeeWorkScheduleStatus = Field(
        description="Current status of the schedule assignment (active, inactive)"
    )
    created_at: str = Field(description="Timestamp when the assignment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the assignment was last updated (ISO 8601)")


class HolidayCalendar(BaseModel):
    """Represents a holiday entry in the organization's holiday calendar"""

    holiday_calendar_ref: str = Field(description="Unique identifier for the holiday calendar entry")
    holiday_name: str = Field(description="Name of the holiday")
    holiday_type: HolidayType = Field(description="Type of holiday (statutory, company, regional)")
    holiday_date: str = Field(description="Date of the holiday (ISO 8601 date)")
    is_workday_swap: bool = Field(description="Whether this holiday involves a workday swap")
    swap_workday_date: Optional[str] = Field(
        description="Date of the swapped workday, null if no swap (ISO 8601 date)",
        default=None,
    )
    year: int = Field(description="Year of the holiday")
    region: str = Field(description="Region code where the holiday applies (e.g., CN, CN-BJ)")
    description: str = Field(description="Description of the holiday")
    created_at: str = Field(description="Timestamp when the holiday entry was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the holiday entry was last updated (ISO 8601)")


class LeavePolicy(BaseModel):
    """Represents a leave policy defining leave type rules and entitlements"""

    leave_policy_ref: str = Field(description="Unique identifier for the leave policy")
    leave_type: LeaveType = Field(
        description="Type of leave (annual, sick, personal, marriage, maternity, paternity, bereavement, work_injury, prenatal_checkup, nursing, compassionate, unpaid, other)"
    )
    leave_name: str = Field(description="Display name of the leave type")
    default_days_per_year: float = Field(description="Default number of leave days entitled per year")
    accrual_rule: LeaveAccrualRule = Field(description="Rule for accruing leave days (yearly, monthly, upon_hire, manual)")
    carry_over_allowed: bool = Field(description="Whether unused leave days can be carried over to the next year")
    max_carry_over_days: float = Field(description="Maximum number of days that can be carried over")
    min_leave_unit: str = Field(
        description="Minimum leave unit allowed by policy (half_day/day/hour)",
        default="half_day",
    )
    max_consecutive_days: Optional[int] = Field(
        description="Maximum consecutive days allowed per request, null means no strict limit",
        default=None,
    )
    advance_notice_days: int = Field(
        description="Required advance notice days before leave starts",
        default=0,
    )
    min_service_months: int = Field(description="Minimum months of service required to be eligible for this leave")
    is_paid: bool = Field(description="Whether this leave type is paid")
    requires_approval: bool = Field(description="Whether leave requests of this type require approval")
    description: str = Field(description="Description of the leave policy")
    status: LeavePolicyStatus = Field(description="Current status of the leave policy (active, inactive)")
    created_at: str = Field(description="Timestamp when the leave policy was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the leave policy was last updated (ISO 8601)")


class LeaveBalance(BaseModel):
    """Represents an employee's leave balance for a specific leave type and year"""

    leave_balance_ref: str = Field(description="Unique identifier for the leave balance record")
    employee_ref: str = Field(description="Reference to the employee")
    leave_policy_ref: str = Field(description="Reference to the leave policy")
    year: int = Field(description="Year for which the leave balance applies")
    entitled_days: float = Field(description="Total number of entitled leave days for the year")
    used_days: float = Field(description="Number of leave days used")
    remaining_days: float = Field(description="Number of remaining leave days")
    carried_over_days: float = Field(description="Number of days carried over from the previous year")
    created_at: str = Field(description="Timestamp when the leave balance was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the leave balance was last updated (ISO 8601)")


class LeaveRequest(BaseModel):
    """Represents a leave request submitted by an employee"""

    leave_request_ref: str = Field(description="Unique identifier for the leave request")
    employee_ref: str = Field(description="Reference to the employee requesting leave")
    leave_policy_ref: str = Field(description="Reference to the leave policy")
    start_datetime: str = Field(description="Start date and time of the leave (ISO 8601)")
    end_datetime: str = Field(description="End date and time of the leave (ISO 8601)")
    duration_days: float = Field(description="Duration of the leave in days")
    reason: str = Field(description="Reason for the leave request")
    handover_employee_ref: Optional[str] = Field(
        description="Employee reference of the person handling work during leave, null if not specified",
        default=None,
    )
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if not yet submitted",
        default=None,
    )
    status: LeaveRequestStatus = Field(
        description="Current status of the leave request (draft, pending, approved, rejected, cancelled, withdrawn)"
    )
    created_at: str = Field(description="Timestamp when the leave request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the leave request was last updated (ISO 8601)")


class OvertimeRequest(BaseModel):
    """Represents an overtime request submitted by an employee"""

    overtime_request_ref: str = Field(description="Unique identifier for the overtime request")
    employee_ref: str = Field(description="Reference to the employee requesting overtime")
    overtime_date: str = Field(description="Date of the overtime work (ISO 8601 date)")
    start_time: str = Field(description="Start time of the overtime (ISO 8601)")
    end_time: str = Field(description="End time of the overtime (ISO 8601)")
    duration_hours: float = Field(description="Duration of the overtime in hours")
    overtime_type: OvertimeType = Field(description="Type of overtime (weekday, weekend, holiday)")
    compensation_type: OvertimeCompensationType = Field(
        description="Type of compensation for overtime (pay, time_off, mixed)"
    )
    reason: str = Field(description="Reason for the overtime request")
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if not yet submitted",
        default=None,
    )
    status: OvertimeRequestStatus = Field(
        description="Current status of the overtime request (draft, pending, approved, rejected, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the overtime request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the overtime request was last updated (ISO 8601)")


class Contract(BaseModel):
    """Represents an employment contract between an employee and the organization"""

    contract_ref: str = Field(description="Unique identifier for the contract")
    employee_ref: str = Field(description="Reference to the employee")
    contract_type: ContractType = Field(
        description="Type of contract (fixed_term, open_ended, internship, labor_dispatch, part_time)"
    )
    contract_number: str = Field(description="Human-readable contract number (e.g., LC-2025-0001)")
    start_date: str = Field(description="Start date of the contract (ISO 8601 date)")
    end_date: Optional[str] = Field(
        description="End date of the contract, null for open-ended contracts (ISO 8601 date)",
        default=None,
    )
    probation_start_date: Optional[str] = Field(
        description="Start date of the probation period, null if not applicable (ISO 8601 date)",
        default=None,
    )
    probation_end_date: Optional[str] = Field(
        description="End date of the probation period, null if not applicable (ISO 8601 date)",
        default=None,
    )
    probation_status: ProbationStatus = Field(
        description="Current probation status (not_applicable, in_progress, passed, failed, extended)"
    )
    renewal_count: int = Field(description="Number of times the contract has been renewed")
    signing_date: str = Field(description="Date when the contract was signed (ISO 8601 date)")
    signing_status: SigningStatus = Field(
        description="Current signing status (draft, pending_signature, signed, expired, terminated)"
    )
    contract_entity: str = Field(description="Legal entity name of the contracting employer")
    work_location: str = Field(description="Primary work location specified in the contract")
    file_attachment_ref: Optional[str] = Field(
        description="Reference to the contract file attachment, null if not uploaded",
        default=None,
    )
    status: ContractStatus = Field(description="Current status of the contract (active, expired, terminated, renewed)")
    notes: str = Field(description="Additional notes about the contract")
    created_at: str = Field(description="Timestamp when the contract was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the contract was last updated (ISO 8601)")


class EmployeeChange(BaseModel):
    """Represents an employee change event such as onboarding, transfer, promotion or offboarding"""

    employee_change_ref: str = Field(description="Unique identifier for the employee change record")
    employee_ref: str = Field(description="Reference to the employee")
    change_type: EmployeeChangeType = Field(
        description="Type of change (onboarding, transfer, promotion, demotion, lateral_move, salary_adjustment, manager_change, offboarding, reinstatement)"
    )
    effective_date: str = Field(description="Effective date of the change (ISO 8601 date)")
    from_department_ref: Optional[str] = Field(
        description="Reference to the previous department, null if not applicable",
        default=None,
    )
    to_department_ref: Optional[str] = Field(
        description="Reference to the new department, null if not applicable",
        default=None,
    )
    from_position_ref: Optional[str] = Field(
        description="Reference to the previous position, null if not applicable",
        default=None,
    )
    to_position_ref: Optional[str] = Field(
        description="Reference to the new position, null if not applicable",
        default=None,
    )
    from_manager_ref: Optional[str] = Field(
        description="Reference to the previous manager, null if not applicable",
        default=None,
    )
    to_manager_ref: Optional[str] = Field(
        description="Reference to the new manager, null if not applicable",
        default=None,
    )
    from_salary_structure_ref: Optional[str] = Field(
        description="Reference to the previous salary structure, null if not applicable",
        default=None,
    )
    to_salary_structure_ref: Optional[str] = Field(
        description="Reference to the new salary structure, null if not applicable",
        default=None,
    )
    reason: str = Field(description="Reason for the change")
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if no approval required",
        default=None,
    )
    status: EmployeeChangeStatus = Field(
        description="Current status of the change (draft, pending, approved, completed, rejected, cancelled)"
    )
    notes: str = Field(description="Additional notes about the change")
    created_at: str = Field(description="Timestamp when the change record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the change record was last updated (ISO 8601)")


class ApprovalFlow(BaseModel):
    """Represents an approval workflow instance associated with a resource"""

    approval_flow_ref: str = Field(description="Unique identifier for the approval flow")
    flow_title: str = Field(description="Title of the approval flow")
    related_resource_type: str = Field(
        description="Type of the related resource (e.g., leave_request, overtime_request, employee_change, offer, certificate_request)"
    )
    related_resource_ref: str = Field(description="Reference ID of the related resource")
    initiator_employee_ref: str = Field(description="Employee reference of the person who initiated the flow")
    current_step_order: int = Field(description="Current step order in the approval flow")
    total_steps: int = Field(description="Total number of steps in the approval flow")
    status: ApprovalFlowStatus = Field(
        description="Current status of the approval flow (draft, pending, approved, rejected, cancelled, withdrawn)"
    )
    initiated_at: str = Field(description="Timestamp when the approval flow was initiated (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the approval flow was completed, null if still in progress (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the approval flow was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the approval flow was last updated (ISO 8601)")


class ApprovalStep(BaseModel):
    """Represents a single step in an approval flow"""

    approval_step_ref: str = Field(description="Unique identifier for the approval step")
    approval_flow_ref: str = Field(description="Reference to the parent approval flow")
    step_order: int = Field(description="Order of this step in the approval flow")
    approver_employee_ref: str = Field(description="Employee reference of the approver for this step")
    action: Optional[ApprovalStepAction] = Field(
        description="Action taken by the approver (approved, rejected, forwarded, returned), null if pending",
        default=None,
    )
    comment: Optional[str] = Field(
        description="Comment left by the approver, null if no comment",
        default=None,
    )
    acted_at: Optional[str] = Field(
        description="Timestamp when the approver acted, null if pending (ISO 8601)",
        default=None,
    )
    status: ApprovalStepStatus = Field(
        description="Current status of the step (pending, completed, skipped, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the step was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the step was last updated (ISO 8601)")


class JobRequisition(BaseModel):
    """Represents a job requisition for hiring new employees"""

    job_requisition_ref: str = Field(description="Unique identifier for the job requisition")
    position_ref: str = Field(description="Reference to the position being hired for")
    department_ref: str = Field(description="Reference to the department requesting the hire")
    hiring_manager_ref: str = Field(description="Employee reference of the hiring manager")
    recruiter_ref: Optional[str] = Field(
        description="Employee reference of the assigned recruiter, null if not assigned",
        default=None,
    )
    requisition_type: RequisitionType = Field(
        description="Type of requisition (social, campus, internal, headhunter)"
    )
    headcount: int = Field(description="Number of positions to be filled")
    filled_count: int = Field(description="Number of positions already filled")
    urgency: RequisitionUrgency = Field(description="Urgency level of the requisition (low, normal, high, urgent)")
    job_description: str = Field(description="Job description for the position")
    requirements: str = Field(description="Requirements for the position")
    salary_range_min: Optional[float] = Field(
        description="Minimum salary range, null if not specified",
        default=None,
    )
    salary_range_max: Optional[float] = Field(
        description="Maximum salary range, null if not specified",
        default=None,
    )
    currency: SalaryCurrency = Field(description="Currency of the salary range")
    status: JobRequisitionStatus = Field(
        description="Current status of the requisition (draft, open, on_hold, filled, cancelled, closed)"
    )
    opened_at: Optional[str] = Field(
        description="Timestamp when the requisition was opened, null if not yet opened (ISO 8601)",
        default=None,
    )
    closed_at: Optional[str] = Field(
        description="Timestamp when the requisition was closed, null if still open (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the requisition was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the requisition was last updated (ISO 8601)")


class Candidate(BaseModel):
    """Represents a candidate in the recruitment pipeline"""

    candidate_ref: str = Field(description="Unique identifier for the candidate")
    given_name: str = Field(description="Candidate's given (first) name")
    family_name: str = Field(description="Candidate's family (last) name")
    email: str = Field(description="Candidate's email address")
    phone: str = Field(description="Candidate's phone number")
    resume_file_ref: Optional[str] = Field(
        description="Reference to the resume file attachment, null if not uploaded",
        default=None,
    )
    source: CandidateSource = Field(
        description="Source of the candidate (social_recruitment, campus_recruitment, internal_referral, headhunter, job_board, company_website, social_media, other)"
    )
    status: CandidateStatus = Field(description="Current status of the candidate (active, inactive, hired, blacklisted)")
    notes: str = Field(description="Additional notes about the candidate")
    created_at: str = Field(description="Timestamp when the candidate record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the candidate record was last updated (ISO 8601)")


class JobApplication(BaseModel):
    """Represents a candidate's application for a specific job requisition"""

    job_application_ref: str = Field(description="Unique identifier for the job application")
    job_requisition_ref: str = Field(description="Reference to the job requisition")
    candidate_ref: str = Field(description="Reference to the candidate")
    referral_ref: Optional[str] = Field(
        description="Reference to the referral, null if not a referral",
        default=None,
    )
    application_stage: ApplicationStage = Field(
        description="Current stage of the application (screening, phone_screen, interview, assessment, offer, hired, rejected, withdrawn)"
    )
    application_status: ApplicationStatus = Field(
        description="Current status of the application (in_progress, on_hold, closed)"
    )
    applied_at: str = Field(description="Timestamp when the candidate applied (ISO 8601)")
    notes: str = Field(description="Additional notes about the application")
    created_at: str = Field(description="Timestamp when the application was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the application was last updated (ISO 8601)")


class Referral(BaseModel):
    """Represents an employee referral for a candidate"""

    referral_ref: str = Field(description="Unique identifier for the referral")
    referrer_employee_ref: str = Field(description="Employee reference of the person making the referral")
    candidate_ref: str = Field(description="Reference to the referred candidate")
    job_requisition_ref: str = Field(description="Reference to the job requisition")
    referral_bonus_amount: Optional[float] = Field(
        description="Referral bonus amount, null if no bonus",
        default=None,
    )
    currency: SalaryCurrency = Field(description="Currency of the referral bonus")
    bonus_status: ReferralBonusStatus = Field(
        description="Status of the referral bonus (pending, approved, paid, cancelled)"
    )
    bonus_paid_at: Optional[str] = Field(
        description="Timestamp when the bonus was paid, null if not yet paid (ISO 8601)",
        default=None,
    )
    relationship: ReferralRelationship = Field(
        description="Relationship between the referrer and the candidate (former_colleague, classmate, friend, family, professional_network, other)"
    )
    recommendation: str = Field(description="Referrer's recommendation for the candidate")
    status: ReferralStatus = Field(description="Current status of the referral (active, inactive, cancelled)")
    created_at: str = Field(description="Timestamp when the referral was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the referral was last updated (ISO 8601)")


class Interview(BaseModel):
    """Represents an interview session for a job application"""

    interview_ref: str = Field(description="Unique identifier for the interview")
    job_application_ref: str = Field(description="Reference to the job application")
    interviewer_employee_ref: str = Field(description="Employee reference of the interviewer")
    interview_round: int = Field(description="Round number of the interview")
    interview_type: InterviewType = Field(
        description="Type of interview (phone_screen, technical, behavioral, case_study, panel, culture_fit, hr, final)"
    )
    scheduled_start: str = Field(description="Scheduled start time of the interview (ISO 8601)")
    scheduled_end: str = Field(description="Scheduled end time of the interview (ISO 8601)")
    actual_start: Optional[str] = Field(
        description="Actual start time of the interview, null if not started (ISO 8601)",
        default=None,
    )
    actual_end: Optional[str] = Field(
        description="Actual end time of the interview, null if not ended (ISO 8601)",
        default=None,
    )
    location: Optional[str] = Field(
        description="Physical location of the interview, null if remote",
        default=None,
    )
    meeting_link: Optional[str] = Field(
        description="Online meeting link, null if in-person",
        default=None,
    )
    rating: Optional[int] = Field(
        description="Interview rating (1-5 scale), null if not yet rated",
        default=None,
    )
    feedback: Optional[str] = Field(
        description="Interviewer's feedback, null if not yet provided",
        default=None,
    )
    result: Optional[InterviewResult] = Field(
        description="Result of the interview (pass, fail, strong_pass, borderline, no_show), null if not yet decided",
        default=None,
    )
    status: InterviewStatus = Field(
        description="Current status of the interview (scheduled, in_progress, completed, cancelled, no_show)"
    )
    created_at: str = Field(description="Timestamp when the interview was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the interview was last updated (ISO 8601)")


class Offer(BaseModel):
    """Represents a job offer extended to a candidate"""

    offer_ref: str = Field(description="Unique identifier for the offer")
    job_application_ref: str = Field(description="Reference to the job application")
    candidate_ref: str = Field(description="Reference to the candidate")
    position_ref: str = Field(description="Reference to the offered position")
    department_ref: str = Field(description="Reference to the department")
    offered_salary: float = Field(description="Offered salary amount")
    currency: SalaryCurrency = Field(description="Currency of the offered salary")
    offered_position_title: str = Field(description="Title of the offered position")
    offered_worker_type: OfferWorkerType = Field(
        description="Worker type for the offer (full_time, intern, campus_recruit, campus_intern, contractor)"
    )
    expected_hire_date: str = Field(description="Expected hire date (ISO 8601 date)")
    offer_valid_until: str = Field(description="Date until which the offer is valid (ISO 8601 date)")
    sign_on_bonus: float = Field(description="Sign-on bonus amount, 0 if none")
    special_terms: Optional[str] = Field(
        description="Special terms or conditions of the offer, null if none",
        default=None,
    )
    status: OfferStatus = Field(
        description="Current status of the offer (draft, pending, approved, issued, accepted, rejected, withdrawn, expired)"
    )
    issued_at: Optional[str] = Field(
        description="Timestamp when the offer was issued, null if not yet issued (ISO 8601)",
        default=None,
    )
    responded_at: Optional[str] = Field(
        description="Timestamp when the candidate responded, null if no response yet (ISO 8601)",
        default=None,
    )
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if no approval required",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the offer was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the offer was last updated (ISO 8601)")


class TrainingProgram(BaseModel):
    """Represents a training program offered by the organization"""

    training_program_ref: str = Field(description="Unique identifier for the training program")
    program_name: str = Field(description="Name of the training program")
    program_type: TrainingProgramType = Field(
        description="Type of training program (onboarding, technical, leadership, compliance, soft_skills, certification, other)"
    )
    description: str = Field(description="Description of the training program")
    duration_hours: float = Field(description="Total duration of the training program in hours")
    delivery_method: TrainingDeliveryMethod = Field(
        description="Delivery method of the training (online, in_person, blended, self_paced)"
    )
    target_audience: TrainingTargetAudience = Field(
        description="Target audience for the training (new_hire, all_employees, managers, engineers, specific_team, other)"
    )
    status: TrainingProgramStatus = Field(
        description="Current status of the training program (draft, active, completed, cancelled, archived)"
    )
    created_at: str = Field(description="Timestamp when the training program was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the training program was last updated (ISO 8601)")


class TrainingEnrollment(BaseModel):
    """Represents an employee's enrollment in a training program"""

    training_enrollment_ref: str = Field(description="Unique identifier for the training enrollment")
    training_program_ref: str = Field(description="Reference to the training program")
    employee_ref: str = Field(description="Reference to the employee")
    enrolled_at: str = Field(description="Timestamp when the employee enrolled (ISO 8601)")
    started_at: Optional[str] = Field(
        description="Timestamp when the employee started the training, null if not started (ISO 8601)",
        default=None,
    )
    completed_at: Optional[str] = Field(
        description="Timestamp when the employee completed the training, null if not completed (ISO 8601)",
        default=None,
    )
    progress_pct: float = Field(description="Progress percentage of the training (0.0 to 100.0)")
    score: Optional[float] = Field(
        description="Score achieved in the training, null if not scored",
        default=None,
    )
    result: Optional[TrainingEnrollmentResult] = Field(
        description="Result of the training (pass, fail, incomplete), null if not yet determined",
        default=None,
    )
    status: TrainingEnrollmentStatus = Field(
        description="Current status of the enrollment (enrolled, in_progress, completed, dropped, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the enrollment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the enrollment was last updated (ISO 8601)")


class ProbationReview(BaseModel):
    """Represents a probation review for an employee during their probation period"""

    probation_review_ref: str = Field(description="Unique identifier for the probation review")
    employee_ref: str = Field(description="Reference to the employee being reviewed")
    contract_ref: str = Field(description="Reference to the associated contract")
    reviewer_employee_ref: str = Field(description="Employee reference of the reviewer")
    review_date: str = Field(description="Date of the probation review (ISO 8601 date)")
    review_round: int = Field(description="Round number of the probation review")
    rating: ProbationReviewRating = Field(
        description="Rating of the probation review (exceeds_expectations, meets_expectations, below_expectations, unsatisfactory)"
    )
    strengths: str = Field(description="Strengths identified during the review")
    improvements: str = Field(description="Areas for improvement identified during the review")
    recommendation: ProbationReviewRecommendation = Field(
        description="Recommendation from the review (pass, continue, extend, terminate)"
    )
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if no approval required",
        default=None,
    )
    status: ProbationReviewStatus = Field(
        description="Current status of the probation review (draft, pending, completed, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the probation review was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the probation review was last updated (ISO 8601)")


class PerformanceCycle(BaseModel):
    """Represents a performance review cycle"""

    performance_cycle_ref: str = Field(description="Unique identifier for the performance cycle")
    cycle_name: str = Field(description="Name of the performance cycle")
    cycle_type: PerformanceCycleType = Field(
        description="Type of performance cycle (monthly, quarterly, semi_annual, annual)"
    )
    start_date: str = Field(description="Start date of the performance cycle (ISO 8601 date)")
    end_date: str = Field(description="End date of the performance cycle (ISO 8601 date)")
    review_deadline: str = Field(description="Deadline for submitting reviews (ISO 8601 date)")
    status: PerformanceCycleStatus = Field(
        description="Current status of the cycle (draft, active, review, calibration, completed, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the performance cycle was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the performance cycle was last updated (ISO 8601)")


class PerformanceReview(BaseModel):
    """Represents a performance review for an employee within a performance cycle"""

    performance_review_ref: str = Field(description="Unique identifier for the performance review")
    performance_cycle_ref: str = Field(description="Reference to the performance cycle")
    employee_ref: str = Field(description="Reference to the employee being reviewed")
    reviewer_employee_ref: str = Field(description="Employee reference of the reviewer")
    self_rating: Optional[str] = Field(
        description="Employee's self-rating, null if not yet submitted",
        default=None,
    )
    manager_rating: Optional[str] = Field(
        description="Manager's rating, null if not yet submitted",
        default=None,
    )
    final_rating: Optional[str] = Field(
        description="Final calibrated rating, null if not yet finalized",
        default=None,
    )
    self_summary: Optional[str] = Field(
        description="Employee's self-assessment summary, null if not yet submitted",
        default=None,
    )
    manager_comment: Optional[str] = Field(
        description="Manager's comment, null if not yet submitted",
        default=None,
    )
    goals_achieved: Optional[str] = Field(
        description="Summary of goals achieved, null if not yet submitted",
        default=None,
    )
    development_plan: Optional[str] = Field(
        description="Development plan for the employee, null if not yet submitted",
        default=None,
    )
    status: PerformanceReviewStatus = Field(
        description="Current status of the review (draft, self_review, manager_review, calibration, completed, acknowledged, appealed)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the review was submitted, null if not yet submitted (ISO 8601)",
        default=None,
    )
    finalized_at: Optional[str] = Field(
        description="Timestamp when the review was finalized, null if not yet finalized (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the performance review was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the performance review was last updated (ISO 8601)")


class EquityGrant(BaseModel):
    """Represents an equity grant awarded to an employee"""

    equity_grant_ref: str = Field(description="Unique identifier for the equity grant")
    employee_ref: str = Field(description="Reference to the employee")
    grant_type: EquityGrantType = Field(
        description="Type of equity grant (rsu, stock_option, espp, sar, phantom)"
    )
    grant_date: str = Field(description="Date when the equity was granted (ISO 8601 date)")
    total_units: int = Field(description="Total number of equity units granted")
    vested_units: int = Field(description="Number of equity units that have vested")
    grant_price: float = Field(description="Price per unit at the time of grant")
    currency: SalaryCurrency = Field(description="Currency of the grant price")
    vesting_schedule: EquityVestingSchedule = Field(
        description="Vesting schedule type (4_year_1_year_cliff, 4_year_no_cliff, 3_year_1_year_cliff, immediate, custom)"
    )
    vesting_start_date: str = Field(description="Start date of the vesting schedule (ISO 8601 date)")
    cliff_date: Optional[str] = Field(
        description="Cliff date for the vesting schedule, null if no cliff (ISO 8601 date)",
        default=None,
    )
    expiry_date: Optional[str] = Field(
        description="Expiry date of the equity grant, null if no expiry (ISO 8601 date)",
        default=None,
    )
    status: EquityGrantStatus = Field(
        description="Current status of the equity grant (active, fully_vested, cancelled, forfeited, expired)"
    )
    notes: str = Field(description="Additional notes about the equity grant")
    created_at: str = Field(description="Timestamp when the equity grant was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the equity grant was last updated (ISO 8601)")


class EquityVestingEvent(BaseModel):
    """Represents a single vesting event within an equity grant"""

    equity_vesting_event_ref: str = Field(description="Unique identifier for the equity vesting event")
    equity_grant_ref: str = Field(description="Reference to the parent equity grant")
    vesting_date: str = Field(description="Date when the vesting occurs (ISO 8601 date)")
    units_vested: int = Field(description="Number of units vesting in this event")
    vesting_price: Optional[float] = Field(
        description="Price per unit at the time of vesting, null if not yet vested",
        default=None,
    )
    status: EquityVestingEventStatus = Field(
        description="Current status of the vesting event (scheduled, vested, cancelled, forfeited)"
    )
    created_at: str = Field(description="Timestamp when the vesting event was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the vesting event was last updated (ISO 8601)")


class ProfessionalTitle(BaseModel):
    """Represents a professional title or certification held by an employee"""

    professional_title_ref: str = Field(description="Unique identifier for the professional title")
    employee_ref: str = Field(description="Reference to the employee")
    title_name: str = Field(description="Name of the professional title")
    title_level: ProfessionalTitleLevel = Field(
        description="Level of the professional title (junior, intermediate, senior, principal, fellow)"
    )
    issuing_authority: str = Field(description="Authority that issued the professional title")
    certificate_number: str = Field(description="Certificate number of the professional title")
    issue_date: str = Field(description="Date when the title was issued (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Expiry date of the title, null if no expiry (ISO 8601 date)",
        default=None,
    )
    file_attachment_ref: Optional[str] = Field(
        description="Reference to the certificate file attachment, null if not uploaded",
        default=None,
    )
    status: ProfessionalTitleStatus = Field(
        description="Current status of the professional title (active, expired, revoked)"
    )
    created_at: str = Field(description="Timestamp when the professional title was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the professional title was last updated (ISO 8601)")


class TalentSubsidy(BaseModel):
    """Represents a talent subsidy or allowance granted to an employee"""

    talent_subsidy_ref: str = Field(description="Unique identifier for the talent subsidy")
    employee_ref: str = Field(description="Reference to the employee")
    subsidy_type: TalentSubsidyType = Field(
        description="Type of subsidy (housing, education, relocation, settlement, talent_award, other)"
    )
    subsidy_name: str = Field(description="Name of the subsidy")
    amount: float = Field(description="Subsidy amount per period")
    currency: SalaryCurrency = Field(description="Currency of the subsidy amount")
    frequency: TalentSubsidyFrequency = Field(
        description="Frequency of the subsidy (one_time, monthly, quarterly, yearly)"
    )
    start_date: str = Field(description="Start date of the subsidy (ISO 8601 date)")
    end_date: Optional[str] = Field(
        description="End date of the subsidy, null if ongoing (ISO 8601 date)",
        default=None,
    )
    status: TalentSubsidyStatus = Field(
        description="Current status of the subsidy (active, suspended, expired, cancelled)"
    )
    notes: str = Field(description="Additional notes about the subsidy")
    created_at: str = Field(description="Timestamp when the subsidy was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the subsidy was last updated (ISO 8601)")


class EmployeeRecord(BaseModel):
    """Represents a supplementary record associated with an employee such as hukou, education or emergency contact"""

    employee_record_ref: str = Field(description="Unique identifier for the employee record")
    employee_ref: str = Field(description="Reference to the employee")
    record_type: EmployeeRecordType = Field(
        description="Type of record (hukou, education, work_history, emergency_contact, id_document, health_check, background_check, other)"
    )
    record_data: Dict[str, Any] = Field(
        description="Dictionary containing the record data, structure varies by record_type"
    )
    effective_date: str = Field(description="Effective date of the record (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Expiry date of the record, null if no expiry (ISO 8601 date)",
        default=None,
    )
    file_attachment_ref: Optional[str] = Field(
        description="Reference to an associated file attachment, null if none",
        default=None,
    )
    status: EmployeeRecordStatus = Field(
        description="Current status of the record (active, archived, expired)"
    )
    created_at: str = Field(description="Timestamp when the record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the record was last updated (ISO 8601)")


class VisaRecord(BaseModel):
    """Represents a visa or work permit record for an employee"""

    visa_record_ref: str = Field(description="Unique identifier for the visa record")
    employee_ref: str = Field(description="Reference to the employee")
    visa_type: VisaType = Field(
        description="Type of visa (work_permit, residence_permit, business_visa, tourist_visa, student_visa, dependent_visa, permanent_residence, other)"
    )
    document_number: str = Field(description="Document number of the visa")
    issuing_country: str = Field(description="Country code that issued the visa (e.g., CN)")
    nationality: str = Field(description="Nationality of the employee (country code, e.g., US)")
    issue_date: str = Field(description="Date when the visa was issued (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Expiry date of the visa, null if no expiry (ISO 8601 date)",
        default=None,
    )
    entry_count: VisaEntryCount = Field(description="Number of entries allowed (single, double, multiple)")
    sponsoring_entity: Optional[str] = Field(
        description="Name of the sponsoring entity, null if not applicable",
        default=None,
    )
    file_attachment_ref: Optional[str] = Field(
        description="Reference to the visa document file attachment, null if not uploaded",
        default=None,
    )
    renewal_reminder_date: Optional[str] = Field(
        description="Date to send a renewal reminder, null if not set (ISO 8601 date)",
        default=None,
    )
    status: VisaRecordStatus = Field(
        description="Current status of the visa record (active, expired, revoked, pending_renewal)"
    )
    notes: str = Field(description="Additional notes about the visa record")
    created_at: str = Field(description="Timestamp when the visa record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the visa record was last updated (ISO 8601)")


class TaxDeclaration(BaseModel):
    """Represents a monthly tax declaration for an employee"""

    tax_declaration_ref: str = Field(description="Unique identifier for the tax declaration")
    employee_ref: str = Field(description="Reference to the employee")
    tax_year: int = Field(description="Tax year")
    tax_month: int = Field(description="Tax month (1-12)")
    taxable_income: float = Field(description="Taxable income for the period")
    tax_deductions: float = Field(description="Standard tax deductions applied")
    special_deductions: float = Field(description="Special additional deductions applied")
    tax_amount: float = Field(description="Tax amount calculated for the period")
    cumulative_tax_paid: float = Field(description="Cumulative tax paid year-to-date")
    currency: SalaryCurrency = Field(description="Currency of the tax amounts")
    declaration_status: TaxDeclarationStatus = Field(
        description="Current status of the declaration (draft, filed, amended, cancelled)"
    )
    filed_at: Optional[str] = Field(
        description="Timestamp when the declaration was filed, null if not yet filed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the tax declaration was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the tax declaration was last updated (ISO 8601)")


class TaxSpecialDeduction(BaseModel):
    """Represents a special tax deduction claimed by an employee"""

    tax_special_deduction_ref: str = Field(description="Unique identifier for the tax special deduction")
    employee_ref: str = Field(description="Reference to the employee")
    deduction_type: TaxSpecialDeductionType = Field(
        description="Type of special deduction (children_education, continuing_education, housing_loan_interest, housing_rent, elderly_care, infant_care, serious_illness)"
    )
    deduction_amount: float = Field(description="Monthly deduction amount")
    tax_year: int = Field(description="Tax year for the deduction")
    effective_start_month: int = Field(description="Start month of the deduction (1-12)")
    effective_end_month: int = Field(description="End month of the deduction (1-12)")
    supporting_info: str = Field(description="Supporting information for the deduction claim")
    status: TaxSpecialDeductionStatus = Field(
        description="Current status of the deduction (active, inactive, expired)"
    )
    created_at: str = Field(description="Timestamp when the deduction was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the deduction was last updated (ISO 8601)")


class ComplianceReport(BaseModel):
    """Represents a compliance report or whistleblower submission"""

    compliance_report_ref: str = Field(description="Unique identifier for the compliance report")
    reporter_employee_ref: Optional[str] = Field(
        description="Employee reference of the reporter, null if anonymous",
        default=None,
    )
    report_type: ComplianceReportType = Field(
        description="Type of compliance report (violation, ethics, safety, harassment, fraud, other)"
    )
    report_channel: ComplianceReportChannel = Field(
        description="Channel through which the report was submitted (anonymous_hotline, email, in_person, online_form, manager_report)"
    )
    is_anonymous: bool = Field(description="Whether the report was submitted anonymously")
    subject: str = Field(description="Subject of the compliance report")
    description: str = Field(description="Detailed description of the compliance issue")
    involved_employee_refs: List[str] = Field(
        description="List of employee references involved in the reported issue"
    )
    severity: ComplianceReportSeverity = Field(
        description="Severity level of the report (low, medium, high, critical)"
    )
    investigator_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned investigator, null if not assigned",
        default=None,
    )
    investigation_status: ComplianceInvestigationStatus = Field(
        description="Current investigation status (pending, investigating, resolved, dismissed)"
    )
    resolution: Optional[str] = Field(
        description="Resolution description, null if not yet resolved",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the report was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    file_attachment_refs: List[str] = Field(
        description="List of file attachment references supporting the report"
    )
    status: ComplianceReportStatus = Field(
        description="Current status of the report (open, in_progress, closed, dismissed)"
    )
    created_at: str = Field(description="Timestamp when the compliance report was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the compliance report was last updated (ISO 8601)")


class CertificateRequest(BaseModel):
    """Represents a request for an official certificate or proof document"""

    certificate_request_ref: str = Field(description="Unique identifier for the certificate request")
    employee_ref: str = Field(description="Reference to the employee requesting the certificate")
    certificate_type: CertificateType = Field(
        description="Type of certificate (employment_proof, income_proof, resignation_proof, social_insurance_proof, housing_fund_proof, reference_letter, other)"
    )
    purpose: str = Field(description="Purpose for requesting the certificate")
    language: CertificateRequestLanguage = Field(description="Language of the certificate (zh-CN, en-US)")
    additional_info: Optional[str] = Field(
        description="Additional information for the certificate, null if none",
        default=None,
    )
    generated_file_ref: Optional[str] = Field(
        description="Reference to the generated certificate file, null if not yet generated",
        default=None,
    )
    approval_flow_ref: Optional[str] = Field(
        description="Reference to the approval flow, null if no approval required",
        default=None,
    )
    status: CertificateRequestStatus = Field(
        description="Current status of the request (draft, pending, approved, issued, rejected, cancelled)"
    )
    requested_at: str = Field(description="Timestamp when the certificate was requested (ISO 8601)")
    issued_at: Optional[str] = Field(
        description="Timestamp when the certificate was issued, null if not yet issued (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the request was last updated (ISO 8601)")


class HRServiceRequest(BaseModel):
    """Represents an HR service request submitted by an employee"""

    hr_service_request_ref: str = Field(description="Unique identifier for the HR service request")
    requester_employee_ref: str = Field(description="Employee reference of the person making the request")
    service_category: HRServiceCategory = Field(
        description="Category of the HR service (hotline, policy_inquiry, document_request, system_issue, complaint, suggestion, onboarding_support, offboarding_support, other)"
    )
    priority: HRServicePriority = Field(description="Priority level of the request (low, normal, high, urgent)")
    subject: str = Field(description="Subject of the service request")
    description: str = Field(description="Detailed description of the service request")
    assigned_hr_employee_ref: Optional[str] = Field(
        description="Employee reference of the assigned HR representative, null if not assigned",
        default=None,
    )
    resolution: Optional[str] = Field(
        description="Resolution description, null if not yet resolved",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the request was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    satisfaction_rating: Optional[int] = Field(
        description="Satisfaction rating from the requester (1-5 scale), null if not rated",
        default=None,
    )
    status: HRServiceRequestStatus = Field(
        description="Current status of the request (open, in_progress, resolved, closed, cancelled)"
    )
    created_at: str = Field(description="Timestamp when the service request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the service request was last updated (ISO 8601)")


class HRDB(OfficeDB):
    """Database containing HR module data including salary, payroll, benefits, attendance, recruitment, performance and more, inheriting all base office collaboration tables"""

    salary_structure: Dict[str, SalaryStructure] = Field(
        description="Dictionary of all salary structures indexed by salary_structure_ref"
    )
    salary_component: Dict[str, SalaryComponent] = Field(
        description="Dictionary of all salary components indexed by salary_component_ref"
    )
    payroll_record: Dict[str, PayrollRecord] = Field(
        description="Dictionary of all payroll records indexed by payroll_record_ref"
    )
    payroll_line_item: Dict[str, PayrollLineItem] = Field(
        description="Dictionary of all payroll line items indexed by payroll_line_item_ref"
    )
    bank_account: Dict[str, BankAccount] = Field(
        description="Dictionary of all bank accounts indexed by bank_account_ref"
    )
    social_insurance: Dict[str, SocialInsurance] = Field(
        description="Dictionary of all social insurance records indexed by social_insurance_ref"
    )
    housing_fund: Dict[str, HousingFund] = Field(
        description="Dictionary of all housing fund records indexed by housing_fund_ref"
    )
    commercial_insurance: Dict[str, CommercialInsurance] = Field(
        description="Dictionary of all commercial insurance plans indexed by commercial_insurance_ref"
    )
    employee_commercial_insurance: Dict[str, EmployeeCommercialInsurance] = Field(
        description="Dictionary of all employee commercial insurance enrollments indexed by employee_commercial_insurance_ref"
    )
    benefit_plan: Dict[str, BenefitPlan] = Field(
        description="Dictionary of all benefit plans indexed by benefit_plan_ref"
    )
    employee_benefit_enrollment: Dict[str, EmployeeBenefitEnrollment] = Field(
        description="Dictionary of all employee benefit enrollments indexed by employee_benefit_enrollment_ref"
    )
    work_schedule: Dict[str, WorkSchedule] = Field(
        description="Dictionary of all work schedules indexed by work_schedule_ref"
    )
    employee_work_schedule: Dict[str, EmployeeWorkSchedule] = Field(
        description="Dictionary of all employee work schedule assignments indexed by employee_work_schedule_ref"
    )
    holiday_calendar: Dict[str, HolidayCalendar] = Field(
        description="Dictionary of all holiday calendar entries indexed by holiday_calendar_ref"
    )
    leave_policy: Dict[str, LeavePolicy] = Field(
        description="Dictionary of all leave policies indexed by leave_policy_ref"
    )
    leave_balance: Dict[str, LeaveBalance] = Field(
        description="Dictionary of all leave balances indexed by leave_balance_ref"
    )
    leave_request: Dict[str, LeaveRequest] = Field(
        description="Dictionary of all leave requests indexed by leave_request_ref"
    )
    overtime_request: Dict[str, OvertimeRequest] = Field(
        description="Dictionary of all overtime requests indexed by overtime_request_ref"
    )
    contract: Dict[str, Contract] = Field(
        description="Dictionary of all contracts indexed by contract_ref"
    )
    employee_change: Dict[str, EmployeeChange] = Field(
        description="Dictionary of all employee change records indexed by employee_change_ref"
    )
    approval_flow: Dict[str, ApprovalFlow] = Field(
        description="Dictionary of all approval flows indexed by approval_flow_ref"
    )
    approval_step: Dict[str, ApprovalStep] = Field(
        description="Dictionary of all approval steps indexed by approval_step_ref"
    )
    job_requisition: Dict[str, JobRequisition] = Field(
        description="Dictionary of all job requisitions indexed by job_requisition_ref"
    )
    candidate: Dict[str, Candidate] = Field(
        description="Dictionary of all candidates indexed by candidate_ref"
    )
    job_application: Dict[str, JobApplication] = Field(
        description="Dictionary of all job applications indexed by job_application_ref"
    )
    referral: Dict[str, Referral] = Field(
        description="Dictionary of all referrals indexed by referral_ref"
    )
    interview: Dict[str, Interview] = Field(
        description="Dictionary of all interviews indexed by interview_ref"
    )
    offer: Dict[str, Offer] = Field(
        description="Dictionary of all offers indexed by offer_ref"
    )
    training_program: Dict[str, TrainingProgram] = Field(
        description="Dictionary of all training programs indexed by training_program_ref"
    )
    training_enrollment: Dict[str, TrainingEnrollment] = Field(
        description="Dictionary of all training enrollments indexed by training_enrollment_ref"
    )
    probation_review: Dict[str, ProbationReview] = Field(
        description="Dictionary of all probation reviews indexed by probation_review_ref"
    )
    performance_cycle: Dict[str, PerformanceCycle] = Field(
        description="Dictionary of all performance cycles indexed by performance_cycle_ref"
    )
    performance_review: Dict[str, PerformanceReview] = Field(
        description="Dictionary of all performance reviews indexed by performance_review_ref"
    )
    equity_grant: Dict[str, EquityGrant] = Field(
        description="Dictionary of all equity grants indexed by equity_grant_ref"
    )
    equity_vesting_event: Dict[str, EquityVestingEvent] = Field(
        description="Dictionary of all equity vesting events indexed by equity_vesting_event_ref"
    )
    professional_title: Dict[str, ProfessionalTitle] = Field(
        description="Dictionary of all professional titles indexed by professional_title_ref"
    )
    talent_subsidy: Dict[str, TalentSubsidy] = Field(
        description="Dictionary of all talent subsidies indexed by talent_subsidy_ref"
    )
    employee_record: Dict[str, EmployeeRecord] = Field(
        description="Dictionary of all employee records indexed by employee_record_ref"
    )
    visa_record: Dict[str, VisaRecord] = Field(
        description="Dictionary of all visa records indexed by visa_record_ref"
    )
    tax_declaration: Dict[str, TaxDeclaration] = Field(
        description="Dictionary of all tax declarations indexed by tax_declaration_ref"
    )
    tax_special_deduction: Dict[str, TaxSpecialDeduction] = Field(
        description="Dictionary of all tax special deductions indexed by tax_special_deduction_ref"
    )
    compliance_report: Dict[str, ComplianceReport] = Field(
        description="Dictionary of all compliance reports indexed by compliance_report_ref"
    )
    certificate_request: Dict[str, CertificateRequest] = Field(
        description="Dictionary of all certificate requests indexed by certificate_request_ref"
    )
    hr_service_request: Dict[str, HRServiceRequest] = Field(
        description="Dictionary of all HR service requests indexed by hr_service_request_ref"
    )

    def get_statistics(self) -> Dict[str, Any]:
        """
        功能说明（Description）：
            获取统计信息，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `Dict[str, Any]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        base_stats = super().get_statistics()
        hr_stats = {
            "num_salary_structures": len(self.salary_structure),
            "num_salary_components": len(self.salary_component),
            "num_payroll_records": len(self.payroll_record),
            "num_payroll_line_items": len(self.payroll_line_item),
            "num_bank_accounts": len(self.bank_account),
            "num_social_insurances": len(self.social_insurance),
            "num_housing_funds": len(self.housing_fund),
            "num_commercial_insurances": len(self.commercial_insurance),
            "num_employee_commercial_insurances": len(self.employee_commercial_insurance),
            "num_benefit_plans": len(self.benefit_plan),
            "num_employee_benefit_enrollments": len(self.employee_benefit_enrollment),
            "num_work_schedules": len(self.work_schedule),
            "num_employee_work_schedules": len(self.employee_work_schedule),
            "num_holiday_calendars": len(self.holiday_calendar),
            "num_leave_policies": len(self.leave_policy),
            "num_leave_balances": len(self.leave_balance),
            "num_leave_requests": len(self.leave_request),
            "num_overtime_requests": len(self.overtime_request),
            "num_contracts": len(self.contract),
            "num_employee_changes": len(self.employee_change),
            "num_approval_flows": len(self.approval_flow),
            "num_approval_steps": len(self.approval_step),
            "num_job_requisitions": len(self.job_requisition),
            "num_candidates": len(self.candidate),
            "num_job_applications": len(self.job_application),
            "num_referrals": len(self.referral),
            "num_interviews": len(self.interview),
            "num_offers": len(self.offer),
            "num_training_programs": len(self.training_program),
            "num_training_enrollments": len(self.training_enrollment),
            "num_probation_reviews": len(self.probation_review),
            "num_performance_cycles": len(self.performance_cycle),
            "num_performance_reviews": len(self.performance_review),
            "num_equity_grants": len(self.equity_grant),
            "num_equity_vesting_events": len(self.equity_vesting_event),
            "num_professional_titles": len(self.professional_title),
            "num_talent_subsidies": len(self.talent_subsidy),
            "num_employee_records": len(self.employee_record),
            "num_visa_records": len(self.visa_record),
            "num_tax_declarations": len(self.tax_declaration),
            "num_tax_special_deductions": len(self.tax_special_deduction),
            "num_compliance_reports": len(self.compliance_report),
            "num_certificate_requests": len(self.certificate_request),
            "num_hr_service_requests": len(self.hr_service_request),
        }
        return {**base_stats, **hr_stats}