"""Toolkit for the HR domain, extending OfficeTools with HR-specific operations."""

from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.hr.models import (
    ApprovalFlow,
    ApprovalStep,
    BankAccount,
    BenefitPlan,
    CertificateRequest,
    Candidate,
    CommercialInsurance,
    ComplianceReport,
    Contract,
    EmployeeBenefitEnrollment,
    EmployeeChange,
    EmployeeCommercialInsurance,
    EmployeeRecord,
    EmployeeWorkSchedule,
    EquityGrant,
    EquityVestingEvent,
    HolidayCalendar,
    HousingFund,
    HRServiceRequest,
    HRDB,
    Interview,
    JobApplication,
    JobRequisition,
    LeaveBalance,
    LeavePolicy,
    LeaveRequest,
    Offer,
    OvertimeRequest,
    PayrollLineItem,
    PayrollRecord,
    PerformanceCycle,
    PerformanceReview,
    ProbationReview,
    ProfessionalTitle,
    Referral,
    SalaryComponent,
    SalaryStructure,
    SocialInsurance,
    TalentSubsidy,
    TaxDeclaration,
    TaxSpecialDeduction,
    TrainingEnrollment,
    TrainingProgram,
    VisaRecord,
    WorkSchedule,
)


class HRTools(OfficeTools):
    """Toolkit for the HR domain, extending OfficeTools with HR-specific operations."""

    db: HRDB

    def __init__(self, db: HRDB) -> None:
        """
        功能说明（Description）：
            初始化对象并绑定所需依赖。
        参数（Parameters）：
            - `db` (HRDB): 数据库对象实例；为空时通常会走默认加载逻辑。
        返回（Returns）：
            - `None`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        super().__init__(db)

    # -----------------------
    # Internal helper methods
    # -----------------------

    def _get_salary_structure(self, salary_structure_ref: str) -> SalaryStructure:
        """
        功能说明（Description）：
            获取薪资结构，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `salary_structure_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SalaryStructure`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if salary_structure_ref not in self.db.salary_structure:
            raise ValueError("Salary structure not found")
        return self.db.salary_structure[salary_structure_ref]

    def _get_payroll_record(self, payroll_record_ref: str) -> PayrollRecord:
        """
        功能说明（Description）：
            获取薪酬发放记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `payroll_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PayrollRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if payroll_record_ref not in self.db.payroll_record:
            raise ValueError("Payroll record not found")
        return self.db.payroll_record[payroll_record_ref]

    def _get_bank_account(self, bank_account_ref: str) -> BankAccount:
        """
        功能说明（Description）：
            获取银行账户，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `bank_account_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BankAccount`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if bank_account_ref not in self.db.bank_account:
            raise ValueError("Bank account not found")
        return self.db.bank_account[bank_account_ref]

    def _get_social_insurance(self, social_insurance_ref: str) -> SocialInsurance:
        """
        功能说明（Description）：
            获取socialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `social_insurance_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SocialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if social_insurance_ref not in self.db.social_insurance:
            raise ValueError("Social insurance not found")
        return self.db.social_insurance[social_insurance_ref]

    def _get_housing_fund(self, housing_fund_ref: str) -> HousingFund:
        """
        功能说明（Description）：
            获取housingfund，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `housing_fund_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HousingFund`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if housing_fund_ref not in self.db.housing_fund:
            raise ValueError("Housing fund not found")
        return self.db.housing_fund[housing_fund_ref]

    def _get_commercial_insurance(self, commercial_insurance_ref: str) -> CommercialInsurance:
        """
        功能说明（Description）：
            获取commercialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `commercial_insurance_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CommercialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if commercial_insurance_ref not in self.db.commercial_insurance:
            raise ValueError("Commercial insurance not found")
        return self.db.commercial_insurance[commercial_insurance_ref]

    def _get_employee_commercial_insurance(self, ref: str) -> EmployeeCommercialInsurance:
        """
        功能说明（Description）：
            获取员工commercialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ref` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `EmployeeCommercialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ref not in self.db.employee_commercial_insurance:
            raise ValueError("Employee commercial insurance not found")
        return self.db.employee_commercial_insurance[ref]

    def _get_benefit_plan(self, benefit_plan_ref: str) -> BenefitPlan:
        """
        功能说明（Description）：
            获取benefitplan，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `benefit_plan_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BenefitPlan`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if benefit_plan_ref not in self.db.benefit_plan:
            raise ValueError("Benefit plan not found")
        return self.db.benefit_plan[benefit_plan_ref]

    def _get_employee_benefit_enrollment(self, ref: str) -> EmployeeBenefitEnrollment:
        """
        功能说明（Description）：
            获取员工benefitenrollment，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ref` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `EmployeeBenefitEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ref not in self.db.employee_benefit_enrollment:
            raise ValueError("Employee benefit enrollment not found")
        return self.db.employee_benefit_enrollment[ref]

    def _get_work_schedule(self, work_schedule_ref: str) -> WorkSchedule:
        """
        功能说明（Description）：
            获取workschedule，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `work_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `WorkSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if work_schedule_ref not in self.db.work_schedule:
            raise ValueError("Work schedule not found")
        return self.db.work_schedule[work_schedule_ref]

    def _get_employee_work_schedule(self, ref: str) -> EmployeeWorkSchedule:
        """
        功能说明（Description）：
            获取员工workschedule，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ref` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `EmployeeWorkSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ref not in self.db.employee_work_schedule:
            raise ValueError("Employee work schedule not found")
        return self.db.employee_work_schedule[ref]

    def _get_holiday_calendar(self, holiday_calendar_ref: str) -> HolidayCalendar:
        """
        功能说明（Description）：
            获取holidaycalendar，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `holiday_calendar_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HolidayCalendar`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if holiday_calendar_ref not in self.db.holiday_calendar:
            raise ValueError("Holiday calendar entry not found")
        return self.db.holiday_calendar[holiday_calendar_ref]

    def _get_leave_policy(self, leave_policy_ref: str) -> LeavePolicy:
        """
        功能说明（Description）：
            获取请假政策，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LeavePolicy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if leave_policy_ref not in self.db.leave_policy:
            raise ValueError("Leave policy not found")
        return self.db.leave_policy[leave_policy_ref]

    def _get_leave_request(self, leave_request_ref: str) -> LeaveRequest:
        """
        功能说明（Description）：
            获取请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if leave_request_ref not in self.db.leave_request:
            raise ValueError("Leave request not found")
        return self.db.leave_request[leave_request_ref]

    def _get_overtime_request(self, overtime_request_ref: str) -> OvertimeRequest:
        """
        功能说明（Description）：
            获取加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `overtime_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if overtime_request_ref not in self.db.overtime_request:
            raise ValueError("Overtime request not found")
        return self.db.overtime_request[overtime_request_ref]

    def _get_contract(self, contract_ref: str) -> Contract:
        """
        功能说明（Description）：
            获取合同，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `contract_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Contract`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if contract_ref not in self.db.contract:
            raise ValueError("Contract not found")
        return self.db.contract[contract_ref]

    def _get_employee_change(self, employee_change_ref: str) -> EmployeeChange:
        """
        功能说明（Description）：
            获取员工change，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_change_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if employee_change_ref not in self.db.employee_change:
            raise ValueError("Employee change not found")
        return self.db.employee_change[employee_change_ref]

    def _get_approval_flow(self, approval_flow_ref: str) -> ApprovalFlow:
        """
        功能说明（Description）：
            获取approvalflow，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `approval_flow_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ApprovalFlow`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if approval_flow_ref not in self.db.approval_flow:
            raise ValueError("Approval flow not found")
        return self.db.approval_flow[approval_flow_ref]

    def _get_job_requisition(self, job_requisition_ref: str) -> JobRequisition:
        """
        功能说明（Description）：
            获取jobrequisition，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_requisition_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `JobRequisition`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if job_requisition_ref not in self.db.job_requisition:
            raise ValueError("Job requisition not found")
        return self.db.job_requisition[job_requisition_ref]

    def _get_candidate(self, candidate_ref: str) -> Candidate:
        """
        功能说明（Description）：
            获取candidate，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `candidate_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Candidate`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if candidate_ref not in self.db.candidate:
            raise ValueError("Candidate not found")
        return self.db.candidate[candidate_ref]

    def _get_job_application(self, job_application_ref: str) -> JobApplication:
        """
        功能说明（Description）：
            获取jobapplication，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `JobApplication`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if job_application_ref not in self.db.job_application:
            raise ValueError("Job application not found")
        return self.db.job_application[job_application_ref]

    def _get_referral(self, referral_ref: str) -> Referral:
        """
        功能说明（Description）：
            获取referral，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `referral_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Referral`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if referral_ref not in self.db.referral:
            raise ValueError("Referral not found")
        return self.db.referral[referral_ref]

    def _get_interview(self, interview_ref: str) -> Interview:
        """
        功能说明（Description）：
            获取interview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `interview_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Interview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if interview_ref not in self.db.interview:
            raise ValueError("Interview not found")
        return self.db.interview[interview_ref]

    def _get_offer(self, offer_ref: str) -> Offer:
        """
        功能说明（Description）：
            获取offer，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `offer_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Offer`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if offer_ref not in self.db.offer:
            raise ValueError("Offer not found")
        return self.db.offer[offer_ref]

    def _get_training_program(self, training_program_ref: str) -> TrainingProgram:
        """
        功能说明（Description）：
            获取trainingprogram，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `training_program_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TrainingProgram`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if training_program_ref not in self.db.training_program:
            raise ValueError("Training program not found")
        return self.db.training_program[training_program_ref]

    def _get_training_enrollment(self, training_enrollment_ref: str) -> TrainingEnrollment:
        """
        功能说明（Description）：
            获取trainingenrollment，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `training_enrollment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TrainingEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if training_enrollment_ref not in self.db.training_enrollment:
            raise ValueError("Training enrollment not found")
        return self.db.training_enrollment[training_enrollment_ref]

    def _get_probation_review(self, probation_review_ref: str) -> ProbationReview:
        """
        功能说明（Description）：
            获取probationreview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `probation_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ProbationReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if probation_review_ref not in self.db.probation_review:
            raise ValueError("Probation review not found")
        return self.db.probation_review[probation_review_ref]

    def _get_performance_cycle(self, performance_cycle_ref: str) -> PerformanceCycle:
        """
        功能说明（Description）：
            获取performancecycle，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_cycle_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PerformanceCycle`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if performance_cycle_ref not in self.db.performance_cycle:
            raise ValueError("Performance cycle not found")
        return self.db.performance_cycle[performance_cycle_ref]

    def _get_performance_review(self, performance_review_ref: str) -> PerformanceReview:
        """
        功能说明（Description）：
            获取performancereview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PerformanceReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if performance_review_ref not in self.db.performance_review:
            raise ValueError("Performance review not found")
        return self.db.performance_review[performance_review_ref]

    def _get_equity_grant(self, equity_grant_ref: str) -> EquityGrant:
        """
        功能说明（Description）：
            获取equitygrant，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `equity_grant_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EquityGrant`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if equity_grant_ref not in self.db.equity_grant:
            raise ValueError("Equity grant not found")
        return self.db.equity_grant[equity_grant_ref]

    def _get_equity_vesting_event(self, ref: str) -> EquityVestingEvent:
        """
        功能说明（Description）：
            获取equityvestingevent，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ref` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `EquityVestingEvent`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ref not in self.db.equity_vesting_event:
            raise ValueError("Equity vesting event not found")
        return self.db.equity_vesting_event[ref]

    def _get_professional_title(self, professional_title_ref: str) -> ProfessionalTitle:
        """
        功能说明（Description）：
            获取professionaltitle，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `professional_title_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ProfessionalTitle`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if professional_title_ref not in self.db.professional_title:
            raise ValueError("Professional title not found")
        return self.db.professional_title[professional_title_ref]

    def _get_talent_subsidy(self, talent_subsidy_ref: str) -> TalentSubsidy:
        """
        功能说明（Description）：
            获取talentsubsidy，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `talent_subsidy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TalentSubsidy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if talent_subsidy_ref not in self.db.talent_subsidy:
            raise ValueError("Talent subsidy not found")
        return self.db.talent_subsidy[talent_subsidy_ref]

    def _get_employee_record(self, employee_record_ref: str) -> EmployeeRecord:
        """
        功能说明（Description）：
            获取员工记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if employee_record_ref not in self.db.employee_record:
            raise ValueError("Employee record not found")
        return self.db.employee_record[employee_record_ref]

    def _get_visa_record(self, visa_record_ref: str) -> VisaRecord:
        """
        功能说明（Description）：
            获取visa记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `visa_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `VisaRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if visa_record_ref not in self.db.visa_record:
            raise ValueError("Visa record not found")
        return self.db.visa_record[visa_record_ref]

    def _get_tax_declaration(self, tax_declaration_ref: str) -> TaxDeclaration:
        """
        功能说明（Description）：
            获取taxdeclaration，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `tax_declaration_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TaxDeclaration`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if tax_declaration_ref not in self.db.tax_declaration:
            raise ValueError("Tax declaration not found")
        return self.db.tax_declaration[tax_declaration_ref]

    def _get_tax_special_deduction(self, ref: str) -> TaxSpecialDeduction:
        """
        功能说明（Description）：
            获取taxspecialdeduction，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `ref` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `TaxSpecialDeduction`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if ref not in self.db.tax_special_deduction:
            raise ValueError("Tax special deduction not found")
        return self.db.tax_special_deduction[ref]

    def _get_compliance_report(self, compliance_report_ref: str) -> ComplianceReport:
        """
        功能说明（Description）：
            获取compliancereport，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `compliance_report_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ComplianceReport`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if compliance_report_ref not in self.db.compliance_report:
            raise ValueError("Compliance report not found")
        return self.db.compliance_report[compliance_report_ref]

    def _get_certificate_request(self, certificate_request_ref: str) -> CertificateRequest:
        """
        功能说明（Description）：
            获取certificate申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `certificate_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CertificateRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if certificate_request_ref not in self.db.certificate_request:
            raise ValueError("Certificate request not found")
        return self.db.certificate_request[certificate_request_ref]

    def _get_hr_service_request(self, hr_service_request_ref: str) -> HRServiceRequest:
        """
        功能说明（Description）：
            获取hrservice申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `hr_service_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HRServiceRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if hr_service_request_ref not in self.db.hr_service_request:
            raise ValueError("HR service request not found")
        return self.db.hr_service_request[hr_service_request_ref]

    # ==========================================
    # 薪酬 (Compensation)
    # ==========================================

    # ----------------
    # SalaryStructure (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_salary_structure(self, salary_structure_ref: str) -> SalaryStructure:
        """
        功能说明（Description）：
            获取薪资结构，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `salary_structure_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SalaryStructure`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_salary_structure(salary_structure_ref)

    @is_tool(ToolType.READ)
    def get_employee_salary_structures(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工薪资structures，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ss for ss in self.db.salary_structure.values()
            if ss.employee_ref == employee_ref
        ]
        results.sort(key=lambda x: x.effective_date, reverse=True)
        return json.dumps([ss.model_dump() for ss in results])

    # ----------------
    # SalaryComponent (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_salary_components(self, salary_structure_ref: str) -> str:
        """
        功能说明（Description）：
            获取薪资明细项，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `salary_structure_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_salary_structure(salary_structure_ref)
        results = [
            sc for sc in self.db.salary_component.values()
            if sc.salary_structure_ref == salary_structure_ref
        ]
        return json.dumps([sc.model_dump() for sc in results])

    # ----------------
    # PayrollRecord (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_payroll_record(self, payroll_record_ref: str) -> PayrollRecord:
        """
        功能说明（Description）：
            获取薪酬发放记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `payroll_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PayrollRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_payroll_record(payroll_record_ref)

    @is_tool(ToolType.READ)
    def get_employee_payroll_records(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工薪酬发放记录列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            pr for pr in self.db.payroll_record.values()
            if pr.employee_ref == employee_ref
        ]
        results.sort(key=lambda x: x.pay_period_start, reverse=True)
        return json.dumps([pr.model_dump() for pr in results])

    # ----------------
    # PayrollLineItem (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_payroll_line_items(self, payroll_record_ref: str) -> str:
        """
        功能说明（Description）：
            获取薪酬发放lineitems，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `payroll_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_payroll_record(payroll_record_ref)
        results = [
            pli for pli in self.db.payroll_line_item.values()
            if pli.payroll_record_ref == payroll_record_ref
        ]
        return json.dumps([pli.model_dump() for pli in results])

    # ----------------
    # BankAccount (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_bank_account(self, bank_account_ref: str) -> BankAccount:
        """
        功能说明（Description）：
            获取银行账户，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `bank_account_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BankAccount`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_bank_account(bank_account_ref)

    @is_tool(ToolType.READ)
    def get_employee_bank_accounts(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工银行账户列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ba for ba in self.db.bank_account.values()
            if ba.employee_ref == employee_ref
        ]
        return json.dumps([ba.model_dump() for ba in results])

    @is_tool(ToolType.WRITE)
    def add_bank_account(
        self,
        employee_ref: str,
        bank_name: str,
        branch_name: str,
        account_number_masked: str,
        account_holder_name: str,
        is_primary: bool,
        effective_date: str,
    ) -> BankAccount:
        """
        功能说明（Description）：
            新增银行账户，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `bank_name` (str): 业务入参，按函数语义传入。
            - `branch_name` (str): 业务入参，按函数语义传入。
            - `account_number_masked` (str): 业务入参，按函数语义传入。
            - `account_holder_name` (str): 业务入参，按函数语义传入。
            - `is_primary` (bool): 布尔开关参数，用于控制分支逻辑。
            - `effective_date` (str): 日期/时间参数，建议使用系统约定格式。
        返回（Returns）：
            - `BankAccount`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        # 若设为主账户，将其他账户取消主账户标记
        if is_primary:
            for ba in self.db.bank_account.values():
                if ba.employee_ref == employee_ref and ba.is_primary:
                    ba.is_primary = False
                    ba.updated_at = self._now_iso()

        now = self._now_iso()
        bank_ref = self._generate_ref("BANK", self.db.bank_account)

        bank_account = BankAccount(
            bank_account_ref=bank_ref,
            employee_ref=employee_ref,
            bank_name=bank_name,
            branch_name=branch_name,
            account_number_masked=account_number_masked,
            account_holder_name=account_holder_name,
            is_primary=is_primary,
            status="active",
            effective_date=effective_date,
            created_at=now,
            updated_at=now,
        )

        self.db.bank_account[bank_ref] = bank_account
        return bank_account

    @is_tool(ToolType.WRITE)
    def set_primary_bank_account(self, bank_account_ref: str) -> BankAccount:
        """
        功能说明（Description）：
            处理primary银行账户，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `bank_account_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BankAccount`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        account = self._get_bank_account(bank_account_ref)
        if account.status != "active":
            raise ValueError(
                f"Cannot set non-active bank account as primary. Account status: '{account.status}'."
            )

        now = self._now_iso()
        # 将同员工其他账户取消主账户标记
        for ba in self.db.bank_account.values():
            if ba.employee_ref == account.employee_ref and ba.bank_account_ref != bank_account_ref and ba.is_primary:
                ba.is_primary = False
                ba.updated_at = now

        account.is_primary = True
        account.updated_at = now
        return account

    # ==========================================
    # 社保/公积金/保险/福利 (Social Insurance / Housing Fund / Insurance / Benefits)
    # ==========================================

    # ----------------
    # SocialInsurance (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_social_insurance(self, social_insurance_ref: str) -> SocialInsurance:
        """
        功能说明（Description）：
            获取socialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `social_insurance_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `SocialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_social_insurance(social_insurance_ref)

    @is_tool(ToolType.READ)
    def get_employee_social_insurances(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工socialinsurances，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            si for si in self.db.social_insurance.values()
            if si.employee_ref == employee_ref
        ]
        return json.dumps([si.model_dump() for si in results])

    # ----------------
    # HousingFund (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_housing_fund(self, housing_fund_ref: str) -> HousingFund:
        """
        功能说明（Description）：
            获取housingfund，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `housing_fund_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HousingFund`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_housing_fund(housing_fund_ref)

    @is_tool(ToolType.READ)
    def get_employee_housing_funds(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工housingfunds，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            hf for hf in self.db.housing_fund.values()
            if hf.employee_ref == employee_ref
        ]
        return json.dumps([hf.model_dump() for hf in results])

    # ----------------
    # CommercialInsurance (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_commercial_insurance(self, commercial_insurance_ref: str) -> CommercialInsurance:
        """
        功能说明（Description）：
            获取commercialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `commercial_insurance_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CommercialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_commercial_insurance(commercial_insurance_ref)

    @is_tool(ToolType.READ)
    def list_commercial_insurances(self) -> str:
        """
        功能说明（Description）：
            列出commercialinsurances，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = list(self.db.commercial_insurance.values())
        return json.dumps([ci.model_dump() for ci in results])

    # ----------------
    # EmployeeCommercialInsurance (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_commercial_insurance(self, employee_commercial_insurance_ref: str) -> EmployeeCommercialInsurance:
        """
        功能说明（Description）：
            获取员工commercialinsurance，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_commercial_insurance_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeCommercialInsurance`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_employee_commercial_insurance(employee_commercial_insurance_ref)

    @is_tool(ToolType.READ)
    def get_employee_commercial_insurances(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工commercialinsurances，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            eci for eci in self.db.employee_commercial_insurance.values()
            if eci.employee_ref == employee_ref
        ]
        return json.dumps([eci.model_dump() for eci in results])

    # ----------------
    # BenefitPlan (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_benefit_plan(self, benefit_plan_ref: str) -> BenefitPlan:
        """
        功能说明（Description）：
            获取benefitplan，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `benefit_plan_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `BenefitPlan`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_benefit_plan(benefit_plan_ref)

    @is_tool(ToolType.READ)
    def list_benefit_plans(self) -> str:
        """
        功能说明（Description）：
            列出benefitplans，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = list(self.db.benefit_plan.values())
        return json.dumps([bp.model_dump() for bp in results])

    # ----------------
    # EmployeeBenefitEnrollment (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_benefit_enrollment(self, employee_benefit_enrollment_ref: str) -> EmployeeBenefitEnrollment:
        """
        功能说明（Description）：
            获取员工benefitenrollment，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_benefit_enrollment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeBenefitEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_employee_benefit_enrollment(employee_benefit_enrollment_ref)

    @is_tool(ToolType.READ)
    def get_employee_benefit_enrollments(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工benefitenrollments，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ebe for ebe in self.db.employee_benefit_enrollment.values()
            if ebe.employee_ref == employee_ref
        ]
        return json.dumps([ebe.model_dump() for ebe in results])

    # ==========================================
    # 工作日程 (Work Schedule)
    # ==========================================

    # ----------------
    # WorkSchedule (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_work_schedule(self, work_schedule_ref: str) -> WorkSchedule:
        """
        功能说明（Description）：
            获取workschedule，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `work_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `WorkSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_work_schedule(work_schedule_ref)

    @is_tool(ToolType.READ)
    def list_work_schedules(self) -> str:
        """
        功能说明（Description）：
            列出workschedules，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = list(self.db.work_schedule.values())
        return json.dumps([ws.model_dump() for ws in results])

    # ----------------
    # EmployeeWorkSchedule (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_work_schedule(self, employee_work_schedule_ref: str) -> EmployeeWorkSchedule:
        """
        功能说明（Description）：
            获取员工workschedule，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_work_schedule_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeWorkSchedule`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_employee_work_schedule(employee_work_schedule_ref)

    @is_tool(ToolType.READ)
    def get_employee_work_schedules(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工workschedules，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ews for ews in self.db.employee_work_schedule.values()
            if ews.employee_ref == employee_ref
        ]
        return json.dumps([ews.model_dump() for ews in results])

    # ----------------
    # HolidayCalendar (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_holiday_calendar(self, holiday_calendar_ref: str) -> HolidayCalendar:
        """
        功能说明（Description）：
            获取holidaycalendar，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `holiday_calendar_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HolidayCalendar`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_holiday_calendar(holiday_calendar_ref)

    @is_tool(ToolType.READ)
    def list_holiday_calendars(self, year: Optional[int] = None) -> str:
        """
        功能说明（Description）：
            列出holidaycalendars，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `year` (Optional[int]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for hc in self.db.holiday_calendar.values():
            if year is not None and hc.year != year:
                continue
            results.append(hc)
        return json.dumps([hc.model_dump() for hc in results])

    # ==========================================
    # 请假 (Leave)
    # ==========================================

    # ----------------
    # LeavePolicy (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_leave_policy(self, leave_policy_ref: str) -> LeavePolicy:
        """
        功能说明（Description）：
            获取请假政策，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LeavePolicy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_leave_policy(leave_policy_ref)

    @is_tool(ToolType.READ)
    def list_leave_policies(self) -> str:
        """
        功能说明（Description）：
            列出请假政策列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = list(self.db.leave_policy.values())
        return json.dumps([lp.model_dump() for lp in results])

    # ----------------
    # LeaveBalance (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_leave_balances(self, employee_ref: str, year: int) -> str:
        """
        功能说明（Description）：
            获取员工请假balances，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `year` (int): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            lb for lb in self.db.leave_balance.values()
            if lb.employee_ref == employee_ref and lb.year == year
        ]
        return json.dumps([lb.model_dump() for lb in results])

    # ----------------
    # LeaveRequest (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_leave_request(self, leave_request_ref: str) -> LeaveRequest:
        """
        功能说明（Description）：
            获取请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_leave_request(leave_request_ref)

    @is_tool(ToolType.READ)
    def get_employee_leave_requests(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工请假申请列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            lr for lr in self.db.leave_request.values()
            if lr.employee_ref == employee_ref
        ]
        return json.dumps([lr.model_dump() for lr in results])

    @is_tool(ToolType.READ)
    def get_pending_leave_approvals(self, approver_employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取pending请假approvals，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(approver_employee_ref)

        # Find approval steps that are pending and assigned to this approver
        pending_flow_refs = set()
        for step in self.db.approval_step.values():
            if (step.approver_employee_ref == approver_employee_ref
                    and step.status == "pending"):
                pending_flow_refs.add(step.approval_flow_ref)

        # Find leave requests that are pending and linked to those flows
        results = []
        for lr in self.db.leave_request.values():
            if lr.status == "pending" and lr.approval_flow_ref in pending_flow_refs:
                results.append(lr)

        return json.dumps([lr.model_dump() for lr in results])

    @is_tool(ToolType.WRITE)
    def submit_leave_request(
        self,
        employee_ref: str,
        leave_policy_ref: str,
        start_datetime: str,
        end_datetime: str,
        duration_days: float,
        reason: str,
        handover_employee_ref: Optional[str] = None,
    ) -> LeaveRequest:
        """
        功能说明（Description）：
            提交请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `leave_policy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `start_datetime` (str): 日期/时间参数，建议使用系统约定格式。
            - `end_datetime` (str): 日期/时间参数，建议使用系统约定格式。
            - `duration_days` (float): 业务入参，按函数语义传入。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
            - `handover_employee_ref` (Optional[str]): 目标业务对象的引用 ID，用于唯一定位记录。 默认值为 `None`。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        policy = self._get_leave_policy(leave_policy_ref)
        if handover_employee_ref is not None:
            self._get_employee(handover_employee_ref)

        # Check leave balance
        # Determine the year from start_datetime
        try:
            start_dt = datetime.fromisoformat(start_datetime)
            year = start_dt.year
        except (ValueError, TypeError):
            year = datetime.now(timezone.utc).year

        # Find matching leave balance
        matching_balance = None
        for lb in self.db.leave_balance.values():
            if (lb.employee_ref == employee_ref
                    and lb.leave_policy_ref == leave_policy_ref
                    and lb.year == year):
                matching_balance = lb
                break

        if matching_balance is not None and matching_balance.remaining_days < duration_days:
            raise ValueError(
                f"Insufficient leave balance. Remaining: {matching_balance.remaining_days} days, "
                f"requested: {duration_days} days"
            )

        now = self._now_iso()
        lr_ref = self._generate_ref("LR", self.db.leave_request)

        leave_request = LeaveRequest(
            leave_request_ref=lr_ref,
            employee_ref=employee_ref,
            leave_policy_ref=leave_policy_ref,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            duration_days=duration_days,
            reason=reason,
            handover_employee_ref=handover_employee_ref,
            approval_flow_ref=None,
            status="pending",
            created_at=now,
            updated_at=now,
        )

        self.db.leave_request[lr_ref] = leave_request
        return leave_request

    @is_tool(ToolType.WRITE)
    def cancel_leave_request(self, leave_request_ref: str, reason: str) -> LeaveRequest:
        """
        功能说明（Description）：
            取消请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        lr = self._get_leave_request(leave_request_ref)
        if lr.status not in ("pending", "draft"):
            raise ValueError(
                f"Cannot cancel leave request with status '{lr.status}'. Only 'pending' or 'draft' requests can be cancelled."
            )

        lr.status = "cancelled"
        lr.updated_at = self._now_iso()
        return lr

    @is_tool(ToolType.WRITE)
    def approve_leave_request(
        self,
        leave_request_ref: str,
        approver_employee_ref: str,
        comment: Optional[str] = None,
    ) -> LeaveRequest:
        """
        功能说明（Description）：
            审批通过请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `comment` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        lr = self._get_leave_request(leave_request_ref)
        self._get_employee(approver_employee_ref)

        if lr.status != "pending":
            raise ValueError(
                f"Cannot approve leave request with status '{lr.status}'. Only 'pending' requests can be approved."
            )

        now = self._now_iso()

        # Deduct leave balance
        try:
            start_dt = datetime.fromisoformat(lr.start_datetime)
            year = start_dt.year
        except (ValueError, TypeError):
            year = datetime.now(timezone.utc).year

        for lb in self.db.leave_balance.values():
            if (lb.employee_ref == lr.employee_ref
                    and lb.leave_policy_ref == lr.leave_policy_ref
                    and lb.year == year):
                lb.used_days += lr.duration_days
                lb.remaining_days -= lr.duration_days
                lb.updated_at = now
                break

        lr.status = "approved"
        lr.updated_at = now

        # Update approval flow/step if present
        if lr.approval_flow_ref and lr.approval_flow_ref in self.db.approval_flow:
            flow = self.db.approval_flow[lr.approval_flow_ref]
            flow.status = "approved"
            flow.completed_at = now
            flow.updated_at = now
            for step in self.db.approval_step.values():
                if (step.approval_flow_ref == lr.approval_flow_ref
                        and step.approver_employee_ref == approver_employee_ref
                        and step.status == "pending"):
                    step.action = "approved"
                    step.comment = comment
                    step.acted_at = now
                    step.status = "completed"
                    step.updated_at = now

        return lr

    @is_tool(ToolType.WRITE)
    def reject_leave_request(
        self,
        leave_request_ref: str,
        approver_employee_ref: str,
        comment: str,
    ) -> LeaveRequest:
        """
        功能说明（Description）：
            驳回请假申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `leave_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `comment` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `LeaveRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        lr = self._get_leave_request(leave_request_ref)
        self._get_employee(approver_employee_ref)

        if lr.status != "pending":
            raise ValueError(
                f"Cannot reject leave request with status '{lr.status}'. Only 'pending' requests can be rejected."
            )

        now = self._now_iso()
        lr.status = "rejected"
        lr.updated_at = now

        # Update approval flow/step if present
        if lr.approval_flow_ref and lr.approval_flow_ref in self.db.approval_flow:
            flow = self.db.approval_flow[lr.approval_flow_ref]
            flow.status = "rejected"
            flow.completed_at = now
            flow.updated_at = now
            for step in self.db.approval_step.values():
                if (step.approval_flow_ref == lr.approval_flow_ref
                        and step.approver_employee_ref == approver_employee_ref
                        and step.status == "pending"):
                    step.action = "rejected"
                    step.comment = comment
                    step.acted_at = now
                    step.status = "completed"
                    step.updated_at = now

        return lr

    # ==========================================
    # 加班 (Overtime)
    # ==========================================

    # ----------------
    # OvertimeRequest (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_overtime_request(self, overtime_request_ref: str) -> OvertimeRequest:
        """
        功能说明（Description）：
            获取加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `overtime_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_overtime_request(overtime_request_ref)

    @is_tool(ToolType.READ)
    def get_employee_overtime_requests(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工加班申请列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ot for ot in self.db.overtime_request.values()
            if ot.employee_ref == employee_ref
        ]
        return json.dumps([ot.model_dump() for ot in results])

    @is_tool(ToolType.READ)
    def get_pending_overtime_approvals(self, approver_employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取pending加班approvals，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(approver_employee_ref)

        pending_flow_refs = set()
        for step in self.db.approval_step.values():
            if (step.approver_employee_ref == approver_employee_ref
                    and step.status == "pending"):
                pending_flow_refs.add(step.approval_flow_ref)

        results = []
        for ot in self.db.overtime_request.values():
            if ot.status == "pending" and ot.approval_flow_ref in pending_flow_refs:
                results.append(ot)

        return json.dumps([ot.model_dump() for ot in results])

    @is_tool(ToolType.WRITE)
    def submit_overtime_request(
        self,
        employee_ref: str,
        overtime_date: str,
        start_time: str,
        end_time: str,
        duration_hours: float,
        overtime_type: str,
        compensation_type: str,
        reason: str,
    ) -> OvertimeRequest:
        """
        功能说明（Description）：
            提交加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `overtime_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `start_time` (str): 业务入参，按函数语义传入。
            - `end_time` (str): 业务入参，按函数语义传入。
            - `duration_hours` (float): 业务入参，按函数语义传入。
            - `overtime_type` (str): 业务入参，按函数语义传入。
            - `compensation_type` (str): 业务入参，按函数语义传入。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        valid_overtime_types = {"weekday", "weekend", "holiday"}
        if overtime_type not in valid_overtime_types:
            raise ValueError(f"Invalid overtime_type: {overtime_type}. Must be one of {valid_overtime_types}")

        valid_compensation_types = {"pay", "time_off", "mixed"}
        if compensation_type not in valid_compensation_types:
            raise ValueError(f"Invalid compensation_type: {compensation_type}. Must be one of {valid_compensation_types}")

        now = self._now_iso()
        ot_ref = self._generate_ref("OT", self.db.overtime_request)

        overtime_request = OvertimeRequest(
            overtime_request_ref=ot_ref,
            employee_ref=employee_ref,
            overtime_date=overtime_date,
            start_time=start_time,
            end_time=end_time,
            duration_hours=duration_hours,
            overtime_type=overtime_type,
            compensation_type=compensation_type,
            reason=reason,
            approval_flow_ref=None,
            status="pending",
            created_at=now,
            updated_at=now,
        )

        self.db.overtime_request[ot_ref] = overtime_request
        return overtime_request

    @is_tool(ToolType.WRITE)
    def approve_overtime_request(
        self,
        overtime_request_ref: str,
        approver_employee_ref: str,
        comment: Optional[str] = None,
    ) -> OvertimeRequest:
        """
        功能说明（Description）：
            审批通过加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `overtime_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `comment` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        ot = self._get_overtime_request(overtime_request_ref)
        self._get_employee(approver_employee_ref)

        if ot.status != "pending":
            raise ValueError(
                f"Cannot approve overtime request with status '{ot.status}'. Only 'pending' requests can be approved."
            )

        now = self._now_iso()
        ot.status = "approved"
        ot.updated_at = now

        if ot.approval_flow_ref and ot.approval_flow_ref in self.db.approval_flow:
            flow = self.db.approval_flow[ot.approval_flow_ref]
            flow.status = "approved"
            flow.completed_at = now
            flow.updated_at = now
            for step in self.db.approval_step.values():
                if (step.approval_flow_ref == ot.approval_flow_ref
                        and step.approver_employee_ref == approver_employee_ref
                        and step.status == "pending"):
                    step.action = "approved"
                    step.comment = comment
                    step.acted_at = now
                    step.status = "completed"
                    step.updated_at = now

        return ot

    @is_tool(ToolType.WRITE)
    def reject_overtime_request(
        self,
        overtime_request_ref: str,
        approver_employee_ref: str,
        comment: str,
    ) -> OvertimeRequest:
        """
        功能说明（Description）：
            驳回加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `overtime_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `approver_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `comment` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        ot = self._get_overtime_request(overtime_request_ref)
        self._get_employee(approver_employee_ref)

        if ot.status != "pending":
            raise ValueError(
                f"Cannot reject overtime request with status '{ot.status}'. Only 'pending' requests can be rejected."
            )

        now = self._now_iso()
        ot.status = "rejected"
        ot.updated_at = now

        if ot.approval_flow_ref and ot.approval_flow_ref in self.db.approval_flow:
            flow = self.db.approval_flow[ot.approval_flow_ref]
            flow.status = "rejected"
            flow.completed_at = now
            flow.updated_at = now
            for step in self.db.approval_step.values():
                if (step.approval_flow_ref == ot.approval_flow_ref
                        and step.approver_employee_ref == approver_employee_ref
                        and step.status == "pending"):
                    step.action = "rejected"
                    step.comment = comment
                    step.acted_at = now
                    step.status = "completed"
                    step.updated_at = now

        return ot

    @is_tool(ToolType.WRITE)
    def cancel_overtime_request(self, overtime_request_ref: str, reason: str) -> OvertimeRequest:
        """
        功能说明（Description）：
            取消加班申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `overtime_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `OvertimeRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        ot = self._get_overtime_request(overtime_request_ref)
        if ot.status not in ("pending", "draft"):
            raise ValueError(
                f"Cannot cancel overtime request with status '{ot.status}'. Only 'pending' or 'draft' requests can be cancelled."
            )

        ot.status = "cancelled"
        ot.updated_at = self._now_iso()
        return ot

    # ==========================================
    # 合同 (Contract)
    # ==========================================

    # ----------------
    # Contract (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_contract(self, contract_ref: str) -> Contract:
        """
        功能说明（Description）：
            获取合同，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `contract_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Contract`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_contract(contract_ref)

    @is_tool(ToolType.READ)
    def get_employee_contracts(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工合同列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            c for c in self.db.contract.values()
            if c.employee_ref == employee_ref
        ]
        return json.dumps([c.model_dump() for c in results])

    @is_tool(ToolType.READ)
    def get_expiring_contracts(self, before_date: str) -> str:
        """
        功能说明（Description）：
            获取expiring合同列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `before_date` (str): 日期/时间参数，建议使用系统约定格式。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for c in self.db.contract.values():
            if c.status == "active" and c.end_date is not None and c.end_date <= before_date:
                results.append(c)
        return json.dumps([c.model_dump() for c in results])

    @is_tool(ToolType.WRITE)
    def renew_contract(self, contract_ref: str, new_end_date: str, notes: str = "") -> Contract:
        """
        功能说明（Description）：
            续签合同，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `contract_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_end_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `Contract`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        contract = self._get_contract(contract_ref)
        if contract.status not in ("active", "expired"):
            raise ValueError(
                f"Cannot renew contract with status '{contract.status}'. "
                f"Only 'active' or 'expired' contracts can be renewed."
            )

        contract.end_date = new_end_date
        contract.renewal_count += 1
        contract.status = "active"
        if notes:
            contract.notes = f"{contract.notes}\n[续签] {notes}".strip()
        contract.updated_at = self._now_iso()
        return contract

    @is_tool(ToolType.WRITE)
    def terminate_contract(
        self,
        contract_ref: str,
        termination_date: str,
        reason: str,
        notes: str = "",
    ) -> Contract:
        """
        功能说明（Description）：
            终止合同，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `contract_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `termination_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `Contract`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        contract = self._get_contract(contract_ref)
        if contract.status != "active":
            raise ValueError(
                f"Cannot terminate contract with status '{contract.status}'. "
                f"Only 'active' contracts can be terminated."
            )

        contract.end_date = termination_date
        contract.status = "terminated"
        termination_note = f"[终止] 终止日期: {termination_date}，原因: {reason}"
        if notes:
            termination_note += f"，备注: {notes}"
        contract.notes = f"{contract.notes}\n{termination_note}".strip()
        contract.updated_at = self._now_iso()
        return contract

    # ==========================================
    # 员工变动 (Employee Changes: Onboarding / Offboarding / Promotion / Transfer)
    # ==========================================

    # ----------------
    # EmployeeChange (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_change(self, employee_change_ref: str) -> EmployeeChange:
        """
        功能说明（Description）：
            获取员工change，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_change_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_employee_change(employee_change_ref)

    @is_tool(ToolType.READ)
    def get_employee_changes(
        self,
        employee_ref: str,
        change_type: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            获取员工changes，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `change_type` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = []
        for ec in self.db.employee_change.values():
            if ec.employee_ref != employee_ref:
                continue
            if change_type is not None and ec.change_type != change_type:
                continue
            results.append(ec)
        return json.dumps([ec.model_dump() for ec in results])

    @is_tool(ToolType.READ)
    def get_onboarding_progress(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取onboardingprogress，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        onboarding_changes = [
            ec.model_dump() for ec in self.db.employee_change.values()
            if ec.employee_ref == employee_ref and ec.change_type == "onboarding"
        ]

        contracts = [
            c.model_dump() for c in self.db.contract.values()
            if c.employee_ref == employee_ref
        ]

        training_enrollments = [
            te.model_dump() for te in self.db.training_enrollment.values()
            if te.employee_ref == employee_ref
        ]

        result = {
            "onboarding_changes": onboarding_changes,
            "contracts": contracts,
            "training_enrollments": training_enrollments,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def get_offboarding_progress(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取offboardingprogress，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        offboarding_changes = [
            ec.model_dump() for ec in self.db.employee_change.values()
            if ec.employee_ref == employee_ref and ec.change_type == "offboarding"
        ]

        contracts = [
            c.model_dump() for c in self.db.contract.values()
            if c.employee_ref == employee_ref
        ]

        result = {
            "offboarding_changes": offboarding_changes,
            "contracts": contracts,
        }
        return json.dumps(result)

    @is_tool(ToolType.WRITE)
    def update_onboarding_step_status(
        self,
        employee_change_ref: str,
        new_status: str,
        notes: Optional[str] = None,
    ) -> EmployeeChange:
        """
        功能说明（Description）：
            更新onboardingstepstatus，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_change_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_status` (str): 业务入参，按函数语义传入。
            - `notes` (Optional[str]): 文本说明字段，用于补充业务上下文。 默认值为 `None`。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        ec = self._get_employee_change(employee_change_ref)
        if ec.change_type != "onboarding":
            raise ValueError(
                f"Employee change '{employee_change_ref}' is not an onboarding change (type: {ec.change_type})."
            )

        valid_statuses = {"draft", "pending", "approved", "completed", "rejected", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        ec.status = new_status
        if notes is not None:
            ec.notes = notes
        ec.updated_at = self._now_iso()
        return ec

    @is_tool(ToolType.WRITE)
    def initiate_offboarding(
        self,
        employee_ref: str,
        effective_date: str,
        reason: str,
        notes: str = "",
    ) -> EmployeeChange:
        """
        功能说明（Description）：
            发起offboarding，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `effective_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)

        now = self._now_iso()
        ec_ref = self._generate_ref("EC", self.db.employee_change)

        # Determine current department from department memberships
        from_dept_ref = None
        for dm in self.db.department_member.values():
            if dm.employee_ref == employee_ref and dm.status == "active" and dm.is_primary:
                from_dept_ref = dm.department_ref
                break

        employee_change = EmployeeChange(
            employee_change_ref=ec_ref,
            employee_ref=employee_ref,
            change_type="offboarding",
            effective_date=effective_date,
            from_department_ref=from_dept_ref,
            to_department_ref=None,
            from_position_ref=emp.position_ref,
            to_position_ref=None,
            from_manager_ref=emp.direct_manager_ref,
            to_manager_ref=None,
            from_salary_structure_ref=None,
            to_salary_structure_ref=None,
            reason=reason,
            approval_flow_ref=None,
            status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )

        self.db.employee_change[ec_ref] = employee_change
        return employee_change

    @is_tool(ToolType.WRITE)
    def update_offboarding_step_status(
        self,
        employee_change_ref: str,
        new_status: str,
        notes: Optional[str] = None,
    ) -> EmployeeChange:
        """
        功能说明（Description）：
            更新offboardingstepstatus，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_change_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_status` (str): 业务入参，按函数语义传入。
            - `notes` (Optional[str]): 文本说明字段，用于补充业务上下文。 默认值为 `None`。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        ec = self._get_employee_change(employee_change_ref)
        if ec.change_type != "offboarding":
            raise ValueError(
                f"Employee change '{employee_change_ref}' is not an offboarding change (type: {ec.change_type})."
            )

        valid_statuses = {"draft", "pending", "approved", "completed", "rejected", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        ec.status = new_status
        if notes is not None:
            ec.notes = notes
        ec.updated_at = self._now_iso()
        return ec

    @is_tool(ToolType.WRITE)
    def initiate_transfer(
        self,
        employee_ref: str,
        effective_date: str,
        to_department_ref: str,
        to_position_ref: str,
        to_manager_ref: str,
        reason: str,
        notes: str = "",
    ) -> EmployeeChange:
        """
        功能说明（Description）：
            发起transfer，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `effective_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `to_department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `to_position_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `to_manager_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)
        self._get_department(to_department_ref)
        self._get_position(to_position_ref)
        self._get_employee(to_manager_ref)

        # Determine current department
        from_dept_ref = None
        for dm in self.db.department_member.values():
            if dm.employee_ref == employee_ref and dm.status == "active" and dm.is_primary:
                from_dept_ref = dm.department_ref
                break

        now = self._now_iso()
        ec_ref = self._generate_ref("EC", self.db.employee_change)

        employee_change = EmployeeChange(
            employee_change_ref=ec_ref,
            employee_ref=employee_ref,
            change_type="transfer",
            effective_date=effective_date,
            from_department_ref=from_dept_ref,
            to_department_ref=to_department_ref,
            from_position_ref=emp.position_ref,
            to_position_ref=to_position_ref,
            from_manager_ref=emp.direct_manager_ref,
            to_manager_ref=to_manager_ref,
            from_salary_structure_ref=None,
            to_salary_structure_ref=None,
            reason=reason,
            approval_flow_ref=None,
            status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )

        self.db.employee_change[ec_ref] = employee_change
        return employee_change

    @is_tool(ToolType.WRITE)
    def initiate_promotion(
        self,
        employee_ref: str,
        effective_date: str,
        to_position_ref: str,
        to_salary_structure_ref: str,
        reason: str,
        notes: str = "",
    ) -> EmployeeChange:
        """
        功能说明（Description）：
            发起promotion，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `effective_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `to_position_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `to_salary_structure_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `EmployeeChange`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)
        self._get_position(to_position_ref)
        self._get_salary_structure(to_salary_structure_ref)

        # Find current salary structure
        from_salary_structure_ref = None
        for ss in self.db.salary_structure.values():
            if ss.employee_ref == employee_ref and ss.status == "active":
                from_salary_structure_ref = ss.salary_structure_ref
                break

        now = self._now_iso()
        ec_ref = self._generate_ref("EC", self.db.employee_change)

        employee_change = EmployeeChange(
            employee_change_ref=ec_ref,
            employee_ref=employee_ref,
            change_type="promotion",
            effective_date=effective_date,
            from_department_ref=None,
            to_department_ref=None,
            from_position_ref=emp.position_ref,
            to_position_ref=to_position_ref,
            from_manager_ref=None,
            to_manager_ref=None,
            from_salary_structure_ref=from_salary_structure_ref,
            to_salary_structure_ref=to_salary_structure_ref,
            reason=reason,
            approval_flow_ref=None,
            status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )

        self.db.employee_change[ec_ref] = employee_change
        return employee_change

    # ==========================================
    # 审批流 (Approval Flow)
    # ==========================================

    # ----------------
    # ApprovalFlow (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_approval_flow(self, approval_flow_ref: str) -> ApprovalFlow:
        """
        功能说明（Description）：
            获取approvalflow，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `approval_flow_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ApprovalFlow`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_approval_flow(approval_flow_ref)

    # ----------------
    # ApprovalStep (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_approval_steps(self, approval_flow_ref: str) -> str:
        """
        功能说明（Description）：
            获取approvalsteps，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `approval_flow_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_approval_flow(approval_flow_ref)
        results = [
            step for step in self.db.approval_step.values()
            if step.approval_flow_ref == approval_flow_ref
        ]
        results.sort(key=lambda x: x.step_order)
        return json.dumps([step.model_dump() for step in results])

    # ==========================================
    # 招聘 (Recruitment)
    # ==========================================

    # ----------------
    # JobRequisition (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_job_requisition(self, job_requisition_ref: str) -> JobRequisition:
        """
        功能说明（Description）：
            获取jobrequisition，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_requisition_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `JobRequisition`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_job_requisition(job_requisition_ref)

    @is_tool(ToolType.READ)
    def list_job_requisitions(self, status: Optional[str] = None) -> str:
        """
        功能说明（Description）：
            列出jobrequisitions，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for jr in self.db.job_requisition.values():
            if status is not None and jr.status != status:
                continue
            results.append(jr)
        return json.dumps([jr.model_dump() for jr in results])

    # ----------------
    # Candidate (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_candidate(self, candidate_ref: str) -> Candidate:
        """
        功能说明（Description）：
            获取candidate，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `candidate_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Candidate`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_candidate(candidate_ref)

    # ----------------
    # JobApplication (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_job_application(self, job_application_ref: str) -> JobApplication:
        """
        功能说明（Description）：
            获取jobapplication，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `JobApplication`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_job_application(job_application_ref)

    @is_tool(ToolType.READ)
    def get_applications_by_requisition(self, job_requisition_ref: str) -> str:
        """
        功能说明（Description）：
            获取applicationsbyrequisition，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_requisition_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_job_requisition(job_requisition_ref)
        results = [
            ja for ja in self.db.job_application.values()
            if ja.job_requisition_ref == job_requisition_ref
        ]
        return json.dumps([ja.model_dump() for ja in results])

    @is_tool(ToolType.READ)
    def get_applications_by_candidate(self, candidate_ref: str) -> str:
        """
        功能说明（Description）：
            获取applicationsbycandidate，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `candidate_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_candidate(candidate_ref)
        results = [
            ja for ja in self.db.job_application.values()
            if ja.candidate_ref == candidate_ref
        ]
        return json.dumps([ja.model_dump() for ja in results])

    # ----------------
    # Referral (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_referral(self, referral_ref: str) -> Referral:
        """
        功能说明（Description）：
            获取referral，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `referral_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Referral`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_referral(referral_ref)

    @is_tool(ToolType.READ)
    def get_employee_referrals(self, referrer_employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工referrals，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `referrer_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(referrer_employee_ref)
        results = [
            r for r in self.db.referral.values()
            if r.referrer_employee_ref == referrer_employee_ref
        ]
        return json.dumps([r.model_dump() for r in results])

    # ----------------
    # Interview (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_interview(self, interview_ref: str) -> Interview:
        """
        功能说明（Description）：
            获取interview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `interview_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Interview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_interview(interview_ref)

    @is_tool(ToolType.READ)
    def get_interviews_by_application(self, job_application_ref: str) -> str:
        """
        功能说明（Description）：
            获取interviewsbyapplication，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_job_application(job_application_ref)
        results = [
            i for i in self.db.interview.values()
            if i.job_application_ref == job_application_ref
        ]
        return json.dumps([i.model_dump() for i in results])

    # ----------------
    # Offer (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_offer(self, offer_ref: str) -> Offer:
        """
        功能说明（Description）：
            获取offer，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `offer_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Offer`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_offer(offer_ref)

    @is_tool(ToolType.READ)
    def get_offers_by_application(self, job_application_ref: str) -> str:
        """
        功能说明（Description）：
            获取offersbyapplication，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_job_application(job_application_ref)
        results = [
            o for o in self.db.offer.values()
            if o.job_application_ref == job_application_ref
        ]
        return json.dumps([o.model_dump() for o in results])

    # ----------------
    # JobApplication / Interview / Offer (WRITE)
    # ----------------

    @is_tool(ToolType.WRITE)
    def advance_application_stage(
        self,
        job_application_ref: str,
        new_stage: str,
        notes: str = "",
    ) -> JobApplication:
        """
        功能说明（Description）：
            处理applicationstage，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_stage` (str): 业务入参，按函数语义传入。
            - `notes` (str): 文本说明字段，用于补充业务上下文。 默认值为 `""`。
        返回（Returns）：
            - `JobApplication`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_stages = {
            "screening", "phone_screen", "interview", "assessment",
            "offer", "hired", "rejected", "withdrawn",
        }
        if new_stage not in valid_stages:
            raise ValueError(f"Invalid stage: {new_stage}. Must be one of {valid_stages}")

        app = self._get_job_application(job_application_ref)
        app.application_stage = new_stage
        if new_stage in ("hired", "rejected", "withdrawn"):
            app.application_status = "closed"
        if notes:
            app.notes = f"{app.notes}\n[阶段变更→{new_stage}] {notes}".strip()
        app.updated_at = self._now_iso()
        return app

    @is_tool(ToolType.WRITE)
    def schedule_interview(
        self,
        job_application_ref: str,
        interviewer_employee_ref: str,
        interview_round: int,
        interview_type: str,
        scheduled_start: str,
        scheduled_end: str,
        location: Optional[str] = None,
        meeting_link: Optional[str] = None,
    ) -> Interview:
        """
        功能说明（Description）：
            处理interview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `interviewer_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `interview_round` (int): 业务入参，按函数语义传入。
            - `interview_type` (str): 业务入参，按函数语义传入。
            - `scheduled_start` (str): 业务入参，按函数语义传入。
            - `scheduled_end` (str): 业务入参，按函数语义传入。
            - `location` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `meeting_link` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `Interview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_types = {
            "phone_screen", "technical", "behavioral", "case_study",
            "panel", "culture_fit", "hr", "final",
        }
        if interview_type not in valid_types:
            raise ValueError(f"Invalid interview_type: {interview_type}. Must be one of {valid_types}")

        self._get_job_application(job_application_ref)
        self._get_employee(interviewer_employee_ref)

        now = self._now_iso()
        intv_ref = self._generate_ref("INTV", self.db.interview)

        interview = Interview(
            interview_ref=intv_ref,
            job_application_ref=job_application_ref,
            interviewer_employee_ref=interviewer_employee_ref,
            interview_round=interview_round,
            interview_type=interview_type,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            actual_start=None,
            actual_end=None,
            location=location,
            meeting_link=meeting_link,
            rating=None,
            feedback=None,
            result=None,
            status="scheduled",
            created_at=now,
            updated_at=now,
        )

        self.db.interview[intv_ref] = interview
        return interview

    @is_tool(ToolType.WRITE)
    def submit_interview_feedback(
        self,
        interview_ref: str,
        rating: int,
        feedback: str,
        result: str,
    ) -> Interview:
        """
        功能说明（Description）：
            提交interviewfeedback，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `interview_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `rating` (int): 业务入参，按函数语义传入。
            - `feedback` (str): 业务入参，按函数语义传入。
            - `result` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `Interview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_results = {"pass", "fail", "strong_pass", "borderline", "no_show"}
        if result not in valid_results:
            raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}")
        if not (1 <= rating <= 5):
            raise ValueError(f"Invalid rating: {rating}. Must be an integer between 1 and 5.")

        interview = self._get_interview(interview_ref)
        if interview.status not in ("scheduled", "in_progress"):
            raise ValueError(
                f"Cannot submit feedback for interview with status '{interview.status}'. "
                f"Only 'scheduled' or 'in_progress' interviews can be updated."
            )

        now = self._now_iso()
        interview.rating = rating
        interview.feedback = feedback
        interview.result = result
        interview.actual_end = now
        interview.status = "completed"
        interview.updated_at = now
        return interview

    @is_tool(ToolType.WRITE)
    def extend_offer(
        self,
        job_application_ref: str,
        position_ref: str,
        department_ref: str,
        offered_salary: float,
        currency: str,
        offered_position_title: str,
        offered_worker_type: str,
        expected_hire_date: str,
        offer_valid_until: str,
        sign_on_bonus: float = 0.0,
        special_terms: Optional[str] = None,
    ) -> Offer:
        """
        功能说明（Description）：
            处理offer，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `job_application_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `position_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `offered_salary` (float): 业务入参，按函数语义传入。
            - `currency` (str): 业务入参，按函数语义传入。
            - `offered_position_title` (str): 业务入参，按函数语义传入。
            - `offered_worker_type` (str): 业务入参，按函数语义传入。
            - `expected_hire_date` (str): 日期/时间参数，建议使用系统约定格式。
            - `offer_valid_until` (str): 业务入参，按函数语义传入。
            - `sign_on_bonus` (float): 业务入参，按函数语义传入。 默认值为 `0.0`。
            - `special_terms` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `Offer`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_worker_types = {"full_time", "intern", "campus_recruit", "campus_intern", "contractor"}
        if offered_worker_type not in valid_worker_types:
            raise ValueError(f"Invalid offered_worker_type: {offered_worker_type}. Must be one of {valid_worker_types}")

        app = self._get_job_application(job_application_ref)

        now = self._now_iso()
        offr_ref = self._generate_ref("OFFR", self.db.offer)

        offer = Offer(
            offer_ref=offr_ref,
            job_application_ref=job_application_ref,
            candidate_ref=app.candidate_ref,
            position_ref=position_ref,
            department_ref=department_ref,
            offered_salary=offered_salary,
            currency=currency,
            offered_position_title=offered_position_title,
            offered_worker_type=offered_worker_type,
            expected_hire_date=expected_hire_date,
            offer_valid_until=offer_valid_until,
            sign_on_bonus=sign_on_bonus,
            special_terms=special_terms,
            status="pending",
            issued_at=None,
            responded_at=None,
            approval_flow_ref=None,
            created_at=now,
            updated_at=now,
        )

        self.db.offer[offr_ref] = offer
        return offer

    @is_tool(ToolType.WRITE)
    def update_offer_status(self, offer_ref: str, new_status: str) -> Offer:
        """
        功能说明（Description）：
            更新offerstatus，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `offer_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_status` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `Offer`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_statuses = {"issued", "approved", "accepted", "rejected", "withdrawn"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        offer = self._get_offer(offer_ref)
        now = self._now_iso()
        offer.status = new_status
        if new_status == "issued":
            offer.issued_at = now
        elif new_status in ("accepted", "rejected"):
            offer.responded_at = now
        offer.updated_at = now
        return offer

    # ==========================================
    # 培训 (Training)
    # ==========================================

    # ----------------
    # TrainingProgram (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_training_program(self, training_program_ref: str) -> TrainingProgram:
        """
        功能说明（Description）：
            获取trainingprogram，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `training_program_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TrainingProgram`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_training_program(training_program_ref)

    @is_tool(ToolType.READ)
    def list_training_programs(self, status: Optional[str] = None) -> str:
        """
        功能说明（Description）：
            列出trainingprograms，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for tp in self.db.training_program.values():
            if status is not None and tp.status != status:
                continue
            results.append(tp)
        return json.dumps([tp.model_dump() for tp in results])

    # ----------------
    # TrainingEnrollment (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_training_enrollment(self, training_enrollment_ref: str) -> TrainingEnrollment:
        """
        功能说明（Description）：
            获取trainingenrollment，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `training_enrollment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TrainingEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_training_enrollment(training_enrollment_ref)

    @is_tool(ToolType.READ)
    def get_employee_training_enrollments(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工trainingenrollments，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            te for te in self.db.training_enrollment.values()
            if te.employee_ref == employee_ref
        ]
        return json.dumps([te.model_dump() for te in results])

    @is_tool(ToolType.WRITE)
    def enroll_training(self, employee_ref: str, training_program_ref: str) -> TrainingEnrollment:
        """
        功能说明（Description）：
            处理training，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `training_program_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TrainingEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        program = self._get_training_program(training_program_ref)
        if program.status != "active":
            raise ValueError(
                f"Cannot enroll in training program with status '{program.status}'. "
                f"Only 'active' programs accept enrollments."
            )

        # 禁止重复报名同一项目（已有 enrolled/in_progress 状态的记录）
        for te in self.db.training_enrollment.values():
            if (
                te.employee_ref == employee_ref
                and te.training_program_ref == training_program_ref
                and te.status in ("enrolled", "in_progress")
            ):
                raise ValueError(
                    f"Employee {employee_ref} is already actively enrolled in training program {training_program_ref}."
                )

        now = self._now_iso()
        te_ref = self._generate_ref("TRENR", self.db.training_enrollment)

        enrollment = TrainingEnrollment(
            training_enrollment_ref=te_ref,
            training_program_ref=training_program_ref,
            employee_ref=employee_ref,
            enrolled_at=now,
            started_at=None,
            completed_at=None,
            progress_pct=0.0,
            score=None,
            result=None,
            status="enrolled",
            created_at=now,
            updated_at=now,
        )

        self.db.training_enrollment[te_ref] = enrollment
        return enrollment

    @is_tool(ToolType.WRITE)
    def update_training_enrollment_completion(
        self,
        training_enrollment_ref: str,
        progress_pct: float,
        score: Optional[float] = None,
        result: Optional[str] = None,
    ) -> TrainingEnrollment:
        """
        功能说明（Description）：
            更新trainingenrollmentcompletion，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `training_enrollment_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `progress_pct` (float): 业务入参，按函数语义传入。
            - `score` (Optional[float]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `result` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `TrainingEnrollment`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        te = self._get_training_enrollment(training_enrollment_ref)

        if progress_pct < 0.0 or progress_pct > 100.0:
            raise ValueError(f"progress_pct must be between 0.0 and 100.0, got {progress_pct}")

        if result is not None:
            valid_results = {"pass", "fail", "incomplete"}
            if result not in valid_results:
                raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}")

        now = self._now_iso()
        te.progress_pct = progress_pct
        if score is not None:
            te.score = score
        if result is not None:
            te.result = result

        # Auto-update status based on progress
        if progress_pct >= 100.0 and result is not None:
            te.status = "completed"
            te.completed_at = now
        elif progress_pct > 0.0 and te.status == "enrolled":
            te.status = "in_progress"
            if te.started_at is None:
                te.started_at = now

        te.updated_at = now
        return te

    # ==========================================
    # 试用期 (Probation)
    # ==========================================

    # ----------------
    # ProbationReview (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_probation_review(self, probation_review_ref: str) -> ProbationReview:
        """
        功能说明（Description）：
            获取probationreview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `probation_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ProbationReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_probation_review(probation_review_ref)

    @is_tool(ToolType.READ)
    def get_employee_probation_reviews(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工probationreviews，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            pr for pr in self.db.probation_review.values()
            if pr.employee_ref == employee_ref
        ]
        return json.dumps([pr.model_dump() for pr in results])

    @is_tool(ToolType.WRITE)
    def submit_probation_review(
        self,
        probation_review_ref: str,
        rating: str,
        strengths: str,
        improvements: str,
        recommendation: str,
    ) -> ProbationReview:
        """
        功能说明（Description）：
            提交probationreview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `probation_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `rating` (str): 业务入参，按函数语义传入。
            - `strengths` (str): 业务入参，按函数语义传入。
            - `improvements` (str): 业务入参，按函数语义传入。
            - `recommendation` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `ProbationReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        valid_ratings = {"exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"}
        if rating not in valid_ratings:
            raise ValueError(f"Invalid rating: {rating}. Must be one of {valid_ratings}")

        valid_recommendations = {"pass", "continue", "extend", "terminate"}
        if recommendation not in valid_recommendations:
            raise ValueError(f"Invalid recommendation: {recommendation}. Must be one of {valid_recommendations}")

        review = self._get_probation_review(probation_review_ref)
        if review.status not in ("draft", "pending"):
            raise ValueError(
                f"Cannot submit probation review with status '{review.status}'. "
                f"Only 'draft' or 'pending' reviews can be submitted."
            )

        review.rating = rating
        review.strengths = strengths
        review.improvements = improvements
        review.recommendation = recommendation
        review.status = "completed"
        review.updated_at = self._now_iso()
        return review

    # ==========================================
    # 绩效 (Performance)
    # ==========================================

    # ----------------
    # PerformanceCycle (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_performance_cycle(self, performance_cycle_ref: str) -> PerformanceCycle:
        """
        功能说明（Description）：
            获取performancecycle，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_cycle_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PerformanceCycle`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_performance_cycle(performance_cycle_ref)

    @is_tool(ToolType.READ)
    def list_performance_cycles(self) -> str:
        """
        功能说明（Description）：
            列出performancecycles，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = list(self.db.performance_cycle.values())
        return json.dumps([pc.model_dump() for pc in results])

    # ----------------
    # PerformanceReview (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_performance_review(self, performance_review_ref: str) -> PerformanceReview:
        """
        功能说明（Description）：
            获取performancereview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `PerformanceReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_performance_review(performance_review_ref)

    @is_tool(ToolType.READ)
    def get_employee_performance_reviews(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工performancereviews，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            pr for pr in self.db.performance_review.values()
            if pr.employee_ref == employee_ref
        ]
        return json.dumps([pr.model_dump() for pr in results])

    @is_tool(ToolType.WRITE)
    def submit_performance_self_review(
        self,
        performance_review_ref: str,
        self_rating: str,
        self_summary: str,
        goals_achieved: str,
    ) -> PerformanceReview:
        """
        功能说明（Description）：
            提交performanceselfreview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `self_rating` (str): 业务入参，按函数语义传入。
            - `self_summary` (str): 业务入参，按函数语义传入。
            - `goals_achieved` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `PerformanceReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        pr = self._get_performance_review(performance_review_ref)

        if pr.status not in ("draft", "self_review"):
            raise ValueError(
                f"Cannot submit self-review for performance review with status '{pr.status}'. "
                f"Status must be 'draft' or 'self_review'."
            )

        now = self._now_iso()
        pr.self_rating = self_rating
        pr.self_summary = self_summary
        pr.goals_achieved = goals_achieved
        pr.status = "manager_review"
        pr.submitted_at = now
        pr.updated_at = now
        return pr

    @is_tool(ToolType.WRITE)
    def submit_performance_manager_review(
        self,
        performance_review_ref: str,
        reviewer_employee_ref: str,
        final_rating: str,
        manager_comment: str,
        goals_for_next_period: Optional[str] = None,
    ) -> PerformanceReview:
        """
        功能说明（Description）：
            提交performancemanagerreview，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `performance_review_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reviewer_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `final_rating` (str): 业务入参，按函数语义传入。
            - `manager_comment` (str): 业务入参，按函数语义传入。
            - `goals_for_next_period` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `PerformanceReview`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        pr = self._get_performance_review(performance_review_ref)
        self._get_employee(reviewer_employee_ref)

        if pr.status != "manager_review":
            raise ValueError(
                f"Cannot submit manager review for performance review with status '{pr.status}'. "
                f"Status must be 'manager_review'."
            )

        now = self._now_iso()
        pr.reviewer_employee_ref = reviewer_employee_ref
        pr.manager_rating = final_rating
        pr.final_rating = final_rating
        pr.manager_comment = manager_comment
        if goals_for_next_period is not None:
            pr.development_plan = goals_for_next_period
        pr.status = "completed"
        pr.finalized_at = now
        pr.updated_at = now
        return pr

    # ==========================================
    # 股权 (Equity)
    # ==========================================

    # ----------------
    # EquityGrant (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_equity_grant(self, equity_grant_ref: str) -> EquityGrant:
        """
        功能说明（Description）：
            获取equitygrant，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `equity_grant_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EquityGrant`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_equity_grant(equity_grant_ref)

    @is_tool(ToolType.READ)
    def get_employee_equity_grants(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工equitygrants，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            eg for eg in self.db.equity_grant.values()
            if eg.employee_ref == employee_ref
        ]
        return json.dumps([eg.model_dump() for eg in results])

    # ----------------
    # EquityVestingEvent (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_equity_vesting_event(self, equity_vesting_event_ref: str) -> EquityVestingEvent:
        """
        功能说明（Description）：
            获取equityvestingevent，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `equity_vesting_event_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EquityVestingEvent`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_equity_vesting_event(equity_vesting_event_ref)

    @is_tool(ToolType.READ)
    def get_grant_vesting_events(self, equity_grant_ref: str) -> str:
        """
        功能说明（Description）：
            获取grantvestingevents，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `equity_grant_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_equity_grant(equity_grant_ref)
        results = [
            eve for eve in self.db.equity_vesting_event.values()
            if eve.equity_grant_ref == equity_grant_ref
        ]
        return json.dumps([eve.model_dump() for eve in results])

    # ==========================================
    # 职称/补贴/档案/签证 (Professional Title / Subsidy / Records / Visa)
    # ==========================================

    # ----------------
    # ProfessionalTitle (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_professional_title(self, professional_title_ref: str) -> ProfessionalTitle:
        """
        功能说明（Description）：
            获取professionaltitle，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `professional_title_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ProfessionalTitle`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_professional_title(professional_title_ref)

    @is_tool(ToolType.READ)
    def get_employee_professional_titles(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工professionaltitles，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            pt for pt in self.db.professional_title.values()
            if pt.employee_ref == employee_ref
        ]
        return json.dumps([pt.model_dump() for pt in results])

    # ----------------
    # TalentSubsidy (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_talent_subsidy(self, talent_subsidy_ref: str) -> TalentSubsidy:
        """
        功能说明（Description）：
            获取talentsubsidy，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `talent_subsidy_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TalentSubsidy`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_talent_subsidy(talent_subsidy_ref)

    @is_tool(ToolType.READ)
    def get_employee_talent_subsidies(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工talentsubsidies，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            ts for ts in self.db.talent_subsidy.values()
            if ts.employee_ref == employee_ref
        ]
        return json.dumps([ts.model_dump() for ts in results])

    # ----------------
    # EmployeeRecord (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_record(self, employee_record_ref: str) -> EmployeeRecord:
        """
        功能说明（Description）：
            获取员工记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_employee_record(employee_record_ref)

    @is_tool(ToolType.READ)
    def get_employee_records(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工记录列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            er for er in self.db.employee_record.values()
            if er.employee_ref == employee_ref
        ]
        return json.dumps([er.model_dump() for er in results])

    # ----------------
    # VisaRecord (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_visa_record(self, visa_record_ref: str) -> VisaRecord:
        """
        功能说明（Description）：
            获取visa记录，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `visa_record_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `VisaRecord`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_visa_record(visa_record_ref)

    @is_tool(ToolType.READ)
    def get_employee_visa_records(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工visa记录列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            vr for vr in self.db.visa_record.values()
            if vr.employee_ref == employee_ref
        ]
        return json.dumps([vr.model_dump() for vr in results])

    # ==========================================
    # 税务 (Tax)
    # ==========================================

    # ----------------
    # TaxDeclaration (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_tax_declaration(self, tax_declaration_ref: str) -> TaxDeclaration:
        """
        功能说明（Description）：
            获取taxdeclaration，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `tax_declaration_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TaxDeclaration`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_tax_declaration(tax_declaration_ref)

    @is_tool(ToolType.READ)
    def get_employee_tax_declarations(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工taxdeclarations，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            td for td in self.db.tax_declaration.values()
            if td.employee_ref == employee_ref
        ]
        return json.dumps([td.model_dump() for td in results])

    # ----------------
    # TaxSpecialDeduction (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_tax_special_deduction(self, tax_special_deduction_ref: str) -> TaxSpecialDeduction:
        """
        功能说明（Description）：
            获取taxspecialdeduction，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `tax_special_deduction_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `TaxSpecialDeduction`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_tax_special_deduction(tax_special_deduction_ref)

    @is_tool(ToolType.READ)
    def get_employee_tax_special_deductions(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工taxspecialdeductions，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            tsd for tsd in self.db.tax_special_deduction.values()
            if tsd.employee_ref == employee_ref
        ]
        return json.dumps([tsd.model_dump() for tsd in results])

    # ==========================================
    # 合规 (Compliance)
    # ==========================================

    # ----------------
    # ComplianceReport (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_compliance_report(self, compliance_report_ref: str) -> ComplianceReport:
        """
        功能说明（Description）：
            获取compliancereport，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `compliance_report_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `ComplianceReport`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_compliance_report(compliance_report_ref)

    @is_tool(ToolType.READ)
    def list_compliance_reports(self, status: Optional[str] = None) -> str:
        """
        功能说明（Description）：
            列出compliancereports，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for cr in self.db.compliance_report.values():
            if status is not None and cr.status != status:
                continue
            results.append(cr)
        return json.dumps([cr.model_dump() for cr in results])

    # ==========================================
    # 证明开具 (Certificate Request)
    # ==========================================

    # ----------------
    # CertificateRequest (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_certificate_request(self, certificate_request_ref: str) -> CertificateRequest:
        """
        功能说明（Description）：
            获取certificate申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `certificate_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `CertificateRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_certificate_request(certificate_request_ref)

    @is_tool(ToolType.READ)
    def get_employee_certificate_requests(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工certificate申请列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            cr for cr in self.db.certificate_request.values()
            if cr.employee_ref == employee_ref
        ]
        return json.dumps([cr.model_dump() for cr in results])

    @is_tool(ToolType.WRITE)
    def submit_certificate_request(
        self,
        employee_ref: str,
        certificate_type: str,
        purpose: str,
        language: str = "zh-CN",
        additional_info: Optional[str] = None,
    ) -> CertificateRequest:
        """
        功能说明（Description）：
            提交certificate申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `certificate_type` (str): 业务入参，按函数语义传入。
            - `purpose` (str): 业务入参，按函数语义传入。
            - `language` (str): 业务入参，按函数语义传入。 默认值为 `"zh-CN"`。
            - `additional_info` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `CertificateRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        valid_types = {
            "employment_proof", "income_proof", "resignation_proof",
            "social_insurance_proof", "housing_fund_proof", "reference_letter", "other"
        }
        if certificate_type not in valid_types:
            raise ValueError(f"Invalid certificate_type: {certificate_type}. Must be one of {valid_types}")

        valid_languages = {"zh-CN", "en-US"}
        if language not in valid_languages:
            raise ValueError(f"Invalid language: {language}. Must be one of {valid_languages}")

        now = self._now_iso()
        cr_ref = self._generate_ref("CERT", self.db.certificate_request)

        certificate_request = CertificateRequest(
            certificate_request_ref=cr_ref,
            employee_ref=employee_ref,
            certificate_type=certificate_type,
            purpose=purpose,
            language=language,
            additional_info=additional_info,
            generated_file_ref=None,
            approval_flow_ref=None,
            status="pending",
            requested_at=now,
            issued_at=None,
            created_at=now,
            updated_at=now,
        )

        self.db.certificate_request[cr_ref] = certificate_request
        return certificate_request

    @is_tool(ToolType.WRITE)
    def cancel_certificate_request(self, certificate_request_ref: str, reason: str) -> CertificateRequest:
        """
        功能说明（Description）：
            取消certificate申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `certificate_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `CertificateRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        cr = self._get_certificate_request(certificate_request_ref)
        if cr.status not in ("pending", "draft"):
            raise ValueError(
                f"Cannot cancel certificate request with status '{cr.status}'. "
                f"Only 'pending' or 'draft' requests can be cancelled."
            )

        cr.status = "cancelled"
        cr.updated_at = self._now_iso()
        return cr

    # ==========================================
    # HR 服务请求 (HR Service Request)
    # ==========================================

    # ----------------
    # HRServiceRequest (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def get_hr_service_request(self, hr_service_request_ref: str) -> HRServiceRequest:
        """
        功能说明（Description）：
            获取hrservice申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `hr_service_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `HRServiceRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_hr_service_request(hr_service_request_ref)

    @is_tool(ToolType.READ)
    def get_employee_hr_service_requests(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工hrservice申请列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)
        results = [
            hsr for hsr in self.db.hr_service_request.values()
            if hsr.requester_employee_ref == employee_ref
        ]
        return json.dumps([hsr.model_dump() for hsr in results])

    @is_tool(ToolType.WRITE)
    def submit_hr_service_request(
        self,
        requester_employee_ref: str,
        request_type: str,
        subject: str,
        description: str,
        priority: str = "normal",
    ) -> HRServiceRequest:
        """
        功能说明（Description）：
            提交hrservice申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `requester_employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `request_type` (str): 业务入参，按函数语义传入。
            - `subject` (str): 业务入参，按函数语义传入。
            - `description` (str): 文本说明字段，用于补充业务上下文。
            - `priority` (str): 业务入参，按函数语义传入。 默认值为 `"normal"`。
        返回（Returns）：
            - `HRServiceRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(requester_employee_ref)

        valid_types = {
            "hotline", "policy_inquiry", "document_request", "system_issue",
            "complaint", "suggestion", "onboarding_support", "offboarding_support", "other"
        }
        if request_type not in valid_types:
            raise ValueError(f"Invalid request_type: {request_type}. Must be one of {valid_types}")

        valid_priorities = {"low", "normal", "high", "urgent"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        now = self._now_iso()
        hsr_ref = self._generate_ref("HSR", self.db.hr_service_request)

        hr_service_request = HRServiceRequest(
            hr_service_request_ref=hsr_ref,
            requester_employee_ref=requester_employee_ref,
            service_category=request_type,
            priority=priority,
            subject=subject,
            description=description,
            assigned_hr_employee_ref=None,
            resolution=None,
            resolved_at=None,
            satisfaction_rating=None,
            status="open",
            created_at=now,
            updated_at=now,
        )

        self.db.hr_service_request[hsr_ref] = hr_service_request
        return hr_service_request

    @is_tool(ToolType.WRITE)
    def update_hr_service_request_status(
        self,
        hr_service_request_ref: str,
        new_status: str,
        resolution_notes: Optional[str] = None,
    ) -> HRServiceRequest:
        """
        功能说明（Description）：
            更新hrservice申请status，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `hr_service_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `new_status` (str): 业务入参，按函数语义传入。
            - `resolution_notes` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `HRServiceRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        hsr = self._get_hr_service_request(hr_service_request_ref)

        valid_statuses = {"open", "in_progress", "resolved", "closed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        hsr.status = new_status
        if resolution_notes is not None:
            hsr.resolution = resolution_notes
        if new_status == "resolved":
            hsr.resolved_at = now
        hsr.updated_at = now
        return hsr

    @is_tool(ToolType.WRITE)
    def cancel_hr_service_request(self, hr_service_request_ref: str, reason: str) -> HRServiceRequest:
        """
        功能说明（Description）：
            取消hrservice申请，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `hr_service_request_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `reason` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `HRServiceRequest`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        hsr = self._get_hr_service_request(hr_service_request_ref)
        if hsr.status not in ("open", "in_progress"):
            raise ValueError(
                f"Cannot cancel HR service request with status '{hsr.status}'. "
                f"Only 'open' or 'in_progress' requests can be cancelled."
            )

        hsr.status = "cancelled"
        hsr.resolution = reason
        hsr.updated_at = self._now_iso()
        return hsr