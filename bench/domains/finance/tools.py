"""面向财务与工作场景的工具集。"""

from typing import Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.domains.base.tools import OfficeTools
from bench.environment.toolkit import ToolType, is_tool
from bench.domains.finance.models import (
    FinanceDB,
    FinanceAccount,
    Budget,
    BudgetLine,
    ExpenseReport,
    ExpenseLine,
    Invoice,
    InvoiceHeader,
    PaymentRequest,
    PaymentExecution,
    ReceiptRecord,
    Refund,
    EmployeeLoan,
    LoanRepayment,
    Settlement,
    SettlementLine,
    FundTransfer,
    ExchangeRate,
    TaxFiling,
    EmployeeTaxRecord,
    AccrualEntry,
    ExpensePolicy,
    FinanceTicket,
    CreditApplication,
    CreditRepaymentSchedule,
    StockTradeOrder,
    FinanceApprovalFlow,
)


class FinanceTools(OfficeTools):
    """工作域工具集，基于基础能力扩展协同操作。"""

    db: FinanceDB

    def __init__(self, db: FinanceDB) -> None:
        """使用数据库实例初始化工具类。

        参数:
            db: 包含财务域全部数据的 WorkDB 数据库实例。

        返回:
            None
        """
        super().__init__(db)

    # ===========================
    # 内部辅助方法
    # ===========================

    def _get_finance_account(self, finance_account_ref: str) -> FinanceAccount:
        """根据引用编号获取财务账户。

        参数:
            finance_account_ref: 唯一标识。

        返回:
            FinanceAccount: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if finance_account_ref not in self.db.finance_account:
            raise ValueError("Finance account not found")
        return self.db.finance_account[finance_account_ref]

    def _get_budget(self, budget_ref: str) -> Budget:
        """根据引用编号获取预算。

        参数:
            budget_ref: 唯一标识。

        返回:
            Budget: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if budget_ref not in self.db.budget:
            raise ValueError("Budget not found")
        return self.db.budget[budget_ref]

    def _get_budget_line(self, budget_line_ref: str) -> BudgetLine:
        """根据引用编号获取预算明细行。

        参数:
            budget_line_ref: 唯一标识。

        返回:
            BudgetLine: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if budget_line_ref not in self.db.budget_line:
            raise ValueError("Budget line not found")
        return self.db.budget_line[budget_line_ref]

    def _get_expense_report(self, expense_report_ref: str) -> ExpenseReport:
        """根据引用编号获取报销单。

        参数:
            expense_report_ref: 唯一标识。

        返回:
            ExpenseReport: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if expense_report_ref not in self.db.expense_report:
            raise ValueError("Expense report not found")
        return self.db.expense_report[expense_report_ref]

    def _get_expense_line(self, expense_line_ref: str) -> ExpenseLine:
        """根据引用编号获取报销明细行。

        参数:
            expense_line_ref: 唯一标识。

        返回:
            ExpenseLine: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if expense_line_ref not in self.db.expense_line:
            raise ValueError("Expense line not found")
        return self.db.expense_line[expense_line_ref]

    def _get_invoice(self, invoice_ref: str) -> Invoice:
        """根据引用编号获取发票。

        参数:
            invoice_ref: 唯一标识。

        返回:
            Invoice: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if invoice_ref not in self.db.invoice:
            raise ValueError("Invoice not found")
        return self.db.invoice[invoice_ref]

    def _get_invoice_header(self, invoice_header_ref: str) -> InvoiceHeader:
        """根据引用编号获取发票抬头。

        参数:
            invoice_header_ref: 唯一标识。

        返回:
            InvoiceHeader: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if invoice_header_ref not in self.db.invoice_header:
            raise ValueError("Invoice header not found")
        return self.db.invoice_header[invoice_header_ref]

    def _get_payment_request(self, payment_request_ref: str) -> PaymentRequest:
        """根据引用编号获取付款申请。

        参数:
            payment_request_ref: 唯一标识。

        返回:
            PaymentRequest: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if payment_request_ref not in self.db.payment_request:
            raise ValueError("Payment request not found")
        return self.db.payment_request[payment_request_ref]

    def _get_payment_execution(self, payment_execution_ref: str) -> PaymentExecution:
        """根据引用编号获取付款执行记录。

        参数:
            payment_execution_ref: 唯一标识。

        返回:
            PaymentExecution: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if payment_execution_ref not in self.db.payment_execution:
            raise ValueError("Payment execution not found")
        return self.db.payment_execution[payment_execution_ref]

    def _get_receipt_record(self, receipt_record_ref: str) -> ReceiptRecord:
        """根据引用编号获取收款记录。

        参数:
            receipt_record_ref: 唯一标识。

        返回:
            ReceiptRecord: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if receipt_record_ref not in self.db.receipt_record:
            raise ValueError("Receipt record not found")
        return self.db.receipt_record[receipt_record_ref]

    def _get_refund(self, refund_ref: str) -> Refund:
        """根据引用编号获取退款单。

        参数:
            refund_ref: 唯一标识。

        返回:
            Refund: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if refund_ref not in self.db.refund:
            raise ValueError("Refund not found")
        return self.db.refund[refund_ref]

    def _get_employee_loan(self, employee_loan_ref: str) -> EmployeeLoan:
        """根据引用编号获取员工借款。

        参数:
            employee_loan_ref: 唯一标识。

        返回:
            EmployeeLoan: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if employee_loan_ref not in self.db.employee_loan:
            raise ValueError("Employee loan not found")
        return self.db.employee_loan[employee_loan_ref]

    def _get_loan_repayment(self, loan_repayment_ref: str) -> LoanRepayment:
        """根据引用编号获取借款还款记录。

        参数:
            loan_repayment_ref: 唯一标识。

        返回:
            LoanRepayment: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if loan_repayment_ref not in self.db.loan_repayment:
            raise ValueError("Loan repayment not found")
        return self.db.loan_repayment[loan_repayment_ref]

    def _get_settlement(self, settlement_ref: str) -> Settlement:
        """根据引用编号获取结算单。

        参数:
            settlement_ref: 唯一标识。

        返回:
            Settlement: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if settlement_ref not in self.db.settlement:
            raise ValueError("Settlement not found")
        return self.db.settlement[settlement_ref]

    def _get_settlement_line(self, settlement_line_ref: str) -> SettlementLine:
        """根据引用编号获取结算明细行。

        参数:
            settlement_line_ref: 唯一标识。

        返回:
            SettlementLine: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if settlement_line_ref not in self.db.settlement_line:
            raise ValueError("Settlement line not found")
        return self.db.settlement_line[settlement_line_ref]

    def _get_fund_transfer(self, fund_transfer_ref: str) -> FundTransfer:
        """根据引用编号获取资金调拨单。

        参数:
            fund_transfer_ref: 唯一标识。

        返回:
            FundTransfer: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if fund_transfer_ref not in self.db.fund_transfer:
            raise ValueError("Fund transfer not found")
        return self.db.fund_transfer[fund_transfer_ref]

    def _get_exchange_rate(self, exchange_rate_ref: str) -> ExchangeRate:
        """根据引用编号获取汇率记录。

        参数:
            exchange_rate_ref: 唯一标识。

        返回:
            ExchangeRate: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if exchange_rate_ref not in self.db.exchange_rate:
            raise ValueError("Exchange rate not found")
        return self.db.exchange_rate[exchange_rate_ref]

    def _get_tax_filing(self, tax_filing_ref: str) -> TaxFiling:
        """根据引用编号获取税务申报单。

        参数:
            tax_filing_ref: 唯一标识。

        返回:
            TaxFiling: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if tax_filing_ref not in self.db.tax_filing:
            raise ValueError("Tax filing not found")
        return self.db.tax_filing[tax_filing_ref]

    def _get_employee_tax_record(self, employee_tax_record_ref: str) -> EmployeeTaxRecord:
        """根据引用编号获取员工个税记录。

        参数:
            employee_tax_record_ref: 唯一标识。

        返回:
            EmployeeTaxRecord: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if employee_tax_record_ref not in self.db.employee_tax_record:
            raise ValueError("Employee tax record not found")
        return self.db.employee_tax_record[employee_tax_record_ref]

    def _get_accrual_entry(self, accrual_entry_ref: str) -> AccrualEntry:
        """根据引用编号获取计提分录。

        参数:
            accrual_entry_ref: 唯一标识。

        返回:
            AccrualEntry: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if accrual_entry_ref not in self.db.accrual_entry:
            raise ValueError("Accrual entry not found")
        return self.db.accrual_entry[accrual_entry_ref]

    def _get_expense_policy(self, expense_policy_ref: str) -> ExpensePolicy:
        """根据引用编号获取报销政策。

        参数:
            expense_policy_ref: 唯一标识。

        返回:
            ExpensePolicy: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if expense_policy_ref not in self.db.expense_policy:
            raise ValueError("Expense policy not found")
        return self.db.expense_policy[expense_policy_ref]

    def _get_finance_ticket(self, finance_ticket_ref: str) -> FinanceTicket:
        """根据引用编号获取财务工单。

        参数:
            finance_ticket_ref: 唯一标识。

        返回:
            FinanceTicket: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if finance_ticket_ref not in self.db.finance_ticket:
            raise ValueError("Finance ticket not found")
        return self.db.finance_ticket[finance_ticket_ref]

    def _get_credit_application(self, credit_application_ref: str) -> CreditApplication:
        """根据引用编号获取信贷申请。

        参数:
            credit_application_ref: 唯一标识。

        返回:
            CreditApplication: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if credit_application_ref not in self.db.credit_application:
            raise ValueError("Credit application not found")
        return self.db.credit_application[credit_application_ref]

    def _get_credit_repayment_schedule(self, credit_repayment_schedule_ref: str) -> CreditRepaymentSchedule:
        """根据引用编号获取信贷还款计划。

        参数:
            credit_repayment_schedule_ref: 唯一标识。

        返回:
            CreditRepaymentSchedule: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if credit_repayment_schedule_ref not in self.db.credit_repayment_schedule:
            raise ValueError("Credit repayment schedule not found")
        return self.db.credit_repayment_schedule[credit_repayment_schedule_ref]

    def _get_stock_trade_order(self, stock_trade_order_ref: str) -> StockTradeOrder:
        """根据引用编号获取股票交易订单。

        参数:
            stock_trade_order_ref: 唯一标识。

        返回:
            StockTradeOrder: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if stock_trade_order_ref not in self.db.stock_trade_order:
            raise ValueError("Stock trade order not found")
        return self.db.stock_trade_order[stock_trade_order_ref]

    def _get_finance_approval_flow(self, finance_approval_flow_ref: str) -> FinanceApprovalFlow:
        """根据引用编号获取财务审批流步骤。

        参数:
            finance_approval_flow_ref: 唯一标识。

        返回:
            FinanceApprovalFlow: 对象实例。

        异常:
            ValueError: 如果未找到对应记录。
        """
        if finance_approval_flow_ref not in self.db.finance_approval_flow:
            raise ValueError("Finance approval flow step not found")
        return self.db.finance_approval_flow[finance_approval_flow_ref]

    # ===================================================================
    # 财务账户 — 收款账户管理 / 资金查询
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_finance_account_details(self, finance_account_ref: str) -> str:
        """获取指定财务账户的详细信息。

        参数:
            finance_account_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        acct = self._get_finance_account(finance_account_ref)
        result = {
            "finance_account_ref": acct.finance_account_ref,
            "account_name": acct.account_name,
            "account_number": acct.account_number,
            "bank_name": acct.bank_name,
            "bank_branch": acct.bank_branch,
            "swift_code": acct.swift_code,
            "currency": acct.currency,
            "account_type": acct.account_type,
            "account_purpose": acct.account_purpose,
            "account_status": acct.account_status,
            "balance": acct.balance,
            "balance_updated_at": acct.balance_updated_at,
            "department_ref": acct.department_ref,
            "managed_by_ref": acct.managed_by_ref,
            "created_at": acct.created_at,
            "updated_at": acct.updated_at,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def list_finance_accounts(
        self,
        account_type: Optional[str] = None,
        account_status: Optional[str] = None,
        currency: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出财务账户。

        参数:
            account_type: Filter by account type (settlement, payroll, petty_cash, escrow, investment, tax). Defaults to None.
            account_status: Filter by account status (active, frozen, closed). Defaults to None.
            currency: Filter by currency code (CNY, USD, EUR, etc.). Defaults to None.
            department_ref: Filter by the owning department ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, acct in self.db.finance_account.items():
            if account_type is not None and acct.account_type != account_type:
                continue
            if account_status is not None and acct.account_status != account_status:
                continue
            if currency is not None and acct.currency != currency:
                continue
            if department_ref is not None and acct.department_ref != department_ref:
                continue
            results.append({
                "finance_account_ref": acct.finance_account_ref,
                "account_name": acct.account_name,
                "account_number": acct.account_number,
                "bank_name": acct.bank_name,
                "currency": acct.currency,
                "account_type": acct.account_type,
                "account_purpose": acct.account_purpose,
                "account_status": acct.account_status,
                "balance": acct.balance,
                "department_ref": acct.department_ref,
                "managed_by_ref": acct.managed_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_finance_account_status(
        self,
        finance_account_ref: str,
        new_status: str,
    ) -> str:
        """更新财务账户状态（如冻结或关闭）。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            finance_account_ref: 唯一标识。
            new_status: The new status to set (active, frozen, closed).

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the account is not found or the status transition is invalid.
        """
        acct = self._get_finance_account(finance_account_ref)
        valid_statuses = {"active", "frozen", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        if acct.account_status == "closed" and new_status != "closed":
            raise ValueError("Cannot change status of a closed account")
        acct.account_status = new_status
        acct.updated_at = self._now_iso()
        return json.dumps({
            "finance_account_ref": acct.finance_account_ref,
            "account_name": acct.account_name,
            "account_status": acct.account_status,
            "updated_at": acct.updated_at,
        })

    # ===================================================================
    # 预算 — 财务预算管理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_budget_details(self, budget_ref: str) -> str:
        """获取指定预算的详细信息。

        参数:
            budget_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        b = self._get_budget(budget_ref)
        result = {
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "budget_code": b.budget_code,
            "fiscal_year": b.fiscal_year,
            "fiscal_period": b.fiscal_period,
            "budget_type": b.budget_type,
            "scope_type": b.scope_type,
            "scope_ref": b.scope_ref,
            "parent_budget_ref": b.parent_budget_ref,
            "currency": b.currency,
            "total_amount": b.total_amount,
            "allocated_amount": b.allocated_amount,
            "spent_amount": b.spent_amount,
            "frozen_amount": b.frozen_amount,
            "budget_status": b.budget_status,
            "approved_by_ref": b.approved_by_ref,
            "approved_at": b.approved_at,
            "notes": b.notes,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def list_budgets(
        self,
        fiscal_year: Optional[int] = None,
        fiscal_period: Optional[str] = None,
        budget_type: Optional[str] = None,
        scope_type: Optional[str] = None,
        scope_ref: Optional[str] = None,
        budget_status: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出预算。

        参数:
            fiscal_year: Filter by fiscal year. Defaults to None.
            fiscal_period: Filter by fiscal period (Q1, Q2, Q3, Q4, H1, H2, annual). Defaults to None.
            budget_type: Filter by budget type (department, project, company, special). Defaults to None.
            scope_type: Filter by scope type (department, team, company, project). Defaults to None.
            scope_ref: Filter by scope ref. Defaults to None.
            budget_status: Filter by budget status (draft, submitted, approved, rejected, closed, frozen). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, b in self.db.budget.items():
            if fiscal_year is not None and b.fiscal_year != fiscal_year:
                continue
            if fiscal_period is not None and b.fiscal_period != fiscal_period:
                continue
            if budget_type is not None and b.budget_type != budget_type:
                continue
            if scope_type is not None and b.scope_type != scope_type:
                continue
            if scope_ref is not None and b.scope_ref != scope_ref:
                continue
            if budget_status is not None and b.budget_status != budget_status:
                continue
            results.append({
                "budget_ref": b.budget_ref,
                "budget_name": b.budget_name,
                "budget_code": b.budget_code,
                "fiscal_year": b.fiscal_year,
                "fiscal_period": b.fiscal_period,
                "budget_type": b.budget_type,
                "scope_type": b.scope_type,
                "scope_ref": b.scope_ref,
                "currency": b.currency,
                "total_amount": b.total_amount,
                "allocated_amount": b.allocated_amount,
                "spent_amount": b.spent_amount,
                "frozen_amount": b.frozen_amount,
                "budget_status": b.budget_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_budget_utilization(self, budget_ref: str) -> str:
        """获取预算使用概览，包含剩余额度与使用率。

        参数:
            budget_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        b = self._get_budget(budget_ref)
        remaining = b.total_amount - b.spent_amount - b.frozen_amount
        utilization_rate = round(b.spent_amount / b.total_amount * 100, 2) if b.total_amount > 0 else 0.0
        # 获取预算明细行
        lines = []
        for bl in self.db.budget_line.values():
            if bl.budget_ref == budget_ref:
                line_remaining = bl.planned_amount - bl.spent_amount - bl.frozen_amount
                lines.append({
                    "budget_line_ref": bl.budget_line_ref,
                    "expense_category": bl.expense_category,
                    "line_label": bl.line_label,
                    "planned_amount": bl.planned_amount,
                    "spent_amount": bl.spent_amount,
                    "frozen_amount": bl.frozen_amount,
                    "remaining_amount": round(line_remaining, 2),
                })
        return json.dumps({
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "total_amount": b.total_amount,
            "allocated_amount": b.allocated_amount,
            "spent_amount": b.spent_amount,
            "frozen_amount": b.frozen_amount,
            "remaining_amount": round(remaining, 2),
            "utilization_rate_pct": utilization_rate,
            "budget_status": b.budget_status,
            "lines": lines,
        })

    @is_tool(ToolType.WRITE)
    def create_budget(
        self,
        budget_name: str,
        budget_code: str,
        fiscal_year: int,
        fiscal_period: str,
        budget_type: str,
        scope_type: str,
        scope_ref: Optional[str],
        currency: str,
        total_amount: float,
        notes: str = "",
        parent_budget_ref: Optional[str] = None,
    ) -> str:
        """创建新的预算记录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            budget_name: Name of the budget.
            budget_code: Short code for the budget.
            fiscal_year: Fiscal year the budget applies to.
            fiscal_period: Fiscal period (Q1, Q2, Q3, Q4, H1, H2, annual).
            budget_type: Type of budget (department, project, company, special).
            scope_type: Scope type (department, team, company, project).
            scope_ref: Reference to the scoped entity, None if company-level.
            currency: Currency code (CNY, USD, EUR, etc.).
            total_amount: Total budgeted amount.
            notes: Additional notes. Defaults to "".
            parent_budget_ref: Reference to parent budget, None if top-level. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        valid_periods = {"Q1", "Q2", "Q3", "Q4", "H1", "H2", "annual"}
        if fiscal_period not in valid_periods:
            raise ValueError(f"Invalid fiscal_period: {fiscal_period}. Must be one of {valid_periods}")
        valid_types = {"department", "project", "company", "special"}
        if budget_type not in valid_types:
            raise ValueError(f"Invalid budget_type: {budget_type}. Must be one of {valid_types}")
        valid_scopes = {"department", "team", "company", "project"}
        if scope_type not in valid_scopes:
            raise ValueError(f"Invalid scope_type: {scope_type}. Must be one of {valid_scopes}")
        if total_amount <= 0:
            raise ValueError("total_amount must be positive")
        if scope_type == "department" and scope_ref is not None:
            self._get_department(scope_ref)
        if scope_type == "team" and scope_ref is not None:
            self._get_team(scope_ref)
        if parent_budget_ref is not None:
            self._get_budget(parent_budget_ref)

        now = self._now_iso()
        ref = self._generate_ref("BUD", self.db.budget)
        budget = Budget(
            budget_ref=ref,
            budget_name=budget_name,
            budget_code=budget_code,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period,
            budget_type=budget_type,
            scope_type=scope_type,
            scope_ref=scope_ref,
            parent_budget_ref=parent_budget_ref,
            currency=currency,
            total_amount=total_amount,
            allocated_amount=0.0,
            spent_amount=0.0,
            frozen_amount=0.0,
            budget_status="draft",
            approved_by_ref=None,
            approved_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.budget[ref] = budget
        return json.dumps({
            "budget_ref": ref,
            "budget_name": budget_name,
            "budget_status": "draft",
            "total_amount": total_amount,
        })

    @is_tool(ToolType.WRITE)
    def submit_budget(self, budget_ref: str) -> str:
        """提交草稿预算进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            budget_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the budget is not found or not in draft status.
        """
        b = self._get_budget(budget_ref)
        if b.budget_status != "draft":
            raise ValueError(f"Budget cannot be submitted from status '{b.budget_status}'. Must be 'draft'.")
        b.budget_status = "submitted"
        b.updated_at = self._now_iso()
        return json.dumps({
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "budget_status": b.budget_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_budget(self, budget_ref: str, approver_ref: str) -> str:
        """审批通过已提交的预算。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            budget_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the budget is not found or not in submitted status.
        """
        b = self._get_budget(budget_ref)
        self._get_employee(approver_ref)
        if b.budget_status != "submitted":
            raise ValueError(f"Budget cannot be approved from status '{b.budget_status}'. Must be 'submitted'.")
        now = self._now_iso()
        b.budget_status = "approved"
        b.approved_by_ref = approver_ref
        b.approved_at = now
        b.updated_at = now
        return json.dumps({
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "budget_status": b.budget_status,
            "approved_by_ref": approver_ref,
        })

    @is_tool(ToolType.WRITE)
    def reject_budget(self, budget_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交的预算。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            budget_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the budget is not found or not in submitted status.
        """
        b = self._get_budget(budget_ref)
        self._get_employee(approver_ref)
        if b.budget_status != "submitted":
            raise ValueError(f"Budget cannot be rejected from status '{b.budget_status}'. Must be 'submitted'.")
        now = self._now_iso()
        b.budget_status = "rejected"
        b.approved_by_ref = approver_ref
        b.approved_at = now
        b.notes = f"{b.notes}\nRejection reason: {reason}" if b.notes else f"Rejection reason: {reason}"
        b.updated_at = now
        return json.dumps({
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "budget_status": b.budget_status,
        })

    @is_tool(ToolType.WRITE)
    def close_budget(self, budget_ref: str) -> str:
        """关闭已审批通过的预算。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            budget_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the budget is not found or not in approved status.
        """
        b = self._get_budget(budget_ref)
        if b.budget_status != "approved":
            raise ValueError(f"Budget cannot be closed from status '{b.budget_status}'. Must be 'approved'.")
        b.budget_status = "closed"
        b.updated_at = self._now_iso()
        return json.dumps({
            "budget_ref": b.budget_ref,
            "budget_name": b.budget_name,
            "budget_status": b.budget_status,
        })

    # ===================================================================
    # 预算明细行 — 预算明细
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_budget_lines(self, budget_ref: str) -> str:
        """列出指定预算下的全部预算明细行。

        参数:
            budget_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_budget(budget_ref)
        results = []
        for bl in self.db.budget_line.values():
            if bl.budget_ref == budget_ref:
                results.append({
                    "budget_line_ref": bl.budget_line_ref,
                    "budget_ref": bl.budget_ref,
                    "expense_category": bl.expense_category,
                    "line_label": bl.line_label,
                    "planned_amount": bl.planned_amount,
                    "spent_amount": bl.spent_amount,
                    "frozen_amount": bl.frozen_amount,
                    "created_at": bl.created_at,
                    "updated_at": bl.updated_at,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_budget_line_details(self, budget_line_ref: str) -> str:
        """获取指定预算明细行的详细信息。

        参数:
            budget_line_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        bl = self._get_budget_line(budget_line_ref)
        return json.dumps({
            "budget_line_ref": bl.budget_line_ref,
            "budget_ref": bl.budget_ref,
            "expense_category": bl.expense_category,
            "line_label": bl.line_label,
            "planned_amount": bl.planned_amount,
            "spent_amount": bl.spent_amount,
            "frozen_amount": bl.frozen_amount,
            "created_at": bl.created_at,
            "updated_at": bl.updated_at,
        })

    # ===================================================================
    # 报销单 — 报销单据管理 / 报销流程指引 / 财务报账管理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_expense_report_details(self, expense_report_ref: str) -> str:
        """获取指定报销单的详细信息。

        参数:
            expense_report_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        er = self._get_expense_report(expense_report_ref)
        result = {
            "expense_report_ref": er.expense_report_ref,
            "report_number": er.report_number,
            "applicant_ref": er.applicant_ref,
            "department_ref": er.department_ref,
            "expense_type": er.expense_type,
            "title": er.title,
            "currency": er.currency,
            "total_amount": er.total_amount,
            "approved_amount": er.approved_amount,
            "trip_ref": er.trip_ref,
            "budget_ref": er.budget_ref,
            "report_status": er.report_status,
            "current_approver_ref": er.current_approver_ref,
            "submitted_at": er.submitted_at,
            "approved_at": er.approved_at,
            "paid_at": er.paid_at,
            "rejected_reason": er.rejected_reason,
            "notes": er.notes,
            "created_at": er.created_at,
            "updated_at": er.updated_at,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def list_expense_reports(
        self,
        applicant_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        expense_type: Optional[str] = None,
        report_status: Optional[str] = None,
        current_approver_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出报销单。

        参数:
            applicant_ref: Filter by the applicant employee ref. Defaults to None.
            department_ref: Filter by department ref. Defaults to None.
            expense_type: Filter by expense type (travel, daily, project, entertainment, training, other). Defaults to None.
            report_status: Filter by report status. Defaults to None.
            current_approver_ref: Filter by the current approver employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, er in self.db.expense_report.items():
            if applicant_ref is not None and er.applicant_ref != applicant_ref:
                continue
            if department_ref is not None and er.department_ref != department_ref:
                continue
            if expense_type is not None and er.expense_type != expense_type:
                continue
            if report_status is not None and er.report_status != report_status:
                continue
            if current_approver_ref is not None and er.current_approver_ref != current_approver_ref:
                continue
            results.append({
                "expense_report_ref": er.expense_report_ref,
                "report_number": er.report_number,
                "applicant_ref": er.applicant_ref,
                "expense_type": er.expense_type,
                "title": er.title,
                "currency": er.currency,
                "total_amount": er.total_amount,
                "approved_amount": er.approved_amount,
                "report_status": er.report_status,
                "submitted_at": er.submitted_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_expense_report(
        self,
        applicant_ref: str,
        department_ref: str,
        expense_type: str,
        title: str,
        currency: str,
        budget_ref: Optional[str] = None,
        trip_ref: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态报销单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            applicant_ref: Employee ref of the applicant.
            department_ref: Department ref of the applicant.
            expense_type: Type of expense (travel, daily, project, entertainment, training, other).
            title: Title or summary of the expense report.
            currency: Currency code (CNY, USD, EUR, etc.).
            budget_ref: Reference to the budget to charge against. Defaults to None.
            trip_ref: Reference to the associated trip. Defaults to None.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(applicant_ref)
        self._get_department(department_ref)
        valid_types = {"travel", "daily", "project", "entertainment", "training", "other"}
        if expense_type not in valid_types:
            raise ValueError(f"Invalid expense_type: {expense_type}. Must be one of {valid_types}")
        if budget_ref is not None:
            self._get_budget(budget_ref)

        now = self._now_iso()
        ref = self._generate_ref("EXPR", self.db.expense_report)
        idx = len(self.db.expense_report) + 1
        report_number = f"ER-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        er = ExpenseReport(
            expense_report_ref=ref,
            report_number=report_number,
            applicant_ref=applicant_ref,
            department_ref=department_ref,
            expense_type=expense_type,
            title=title,
            currency=currency,
            total_amount=0.0,
            approved_amount=0.0,
            trip_ref=trip_ref,
            budget_ref=budget_ref,
            report_status="draft",
            current_approver_ref=None,
            submitted_at=None,
            approved_at=None,
            paid_at=None,
            rejected_reason=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.expense_report[ref] = er
        return json.dumps({
            "expense_report_ref": ref,
            "report_number": report_number,
            "report_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_expense_report(self, expense_report_ref: str) -> str:
        """提交草稿报销单进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            expense_report_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the expense report is not found or not in draft status.
        """
        er = self._get_expense_report(expense_report_ref)
        if er.report_status != "draft":
            raise ValueError(f"Expense report cannot be submitted from status '{er.report_status}'. Must be 'draft'.")
        now = self._now_iso()
        er.report_status = "submitted"
        er.submitted_at = now
        er.updated_at = now
        return json.dumps({
            "expense_report_ref": er.expense_report_ref,
            "report_number": er.report_number,
            "report_status": er.report_status,
            "submitted_at": er.submitted_at,
        })

    @is_tool(ToolType.WRITE)
    def approve_expense_report(
        self,
        expense_report_ref: str,
        approver_ref: str,
        approved_amount: Optional[float] = None,
    ) -> str:
        """审批通过处于已提交或审核中的报销单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            expense_report_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            approved_amount: The approved amount. If None, uses total_amount. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the expense report is not found or not in a valid status for approval.
        """
        er = self._get_expense_report(expense_report_ref)
        self._get_employee(approver_ref)
        if er.report_status not in ("submitted", "under_review"):
            raise ValueError(f"Expense report cannot be approved from status '{er.report_status}'.")
        now = self._now_iso()
        er.report_status = "approved"
        er.approved_amount = approved_amount if approved_amount is not None else er.total_amount
        er.approved_at = now
        er.current_approver_ref = None
        er.updated_at = now
        return json.dumps({
            "expense_report_ref": er.expense_report_ref,
            "report_status": er.report_status,
            "approved_amount": er.approved_amount,
        })

    @is_tool(ToolType.WRITE)
    def reject_expense_report(
        self,
        expense_report_ref: str,
        approver_ref: str,
        reason: str,
    ) -> str:
        """驳回处于已提交或审核中的报销单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            expense_report_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the expense report is not found or not in a valid status for rejection.
        """
        er = self._get_expense_report(expense_report_ref)
        self._get_employee(approver_ref)
        if er.report_status not in ("submitted", "under_review"):
            raise ValueError(f"Expense report cannot be rejected from status '{er.report_status}'.")
        now = self._now_iso()
        er.report_status = "rejected"
        er.rejected_reason = reason
        er.current_approver_ref = None
        er.updated_at = now
        return json.dumps({
            "expense_report_ref": er.expense_report_ref,
            "report_status": er.report_status,
            "rejected_reason": reason,
        })

    @is_tool(ToolType.WRITE)
    def cancel_expense_report(self, expense_report_ref: str) -> str:
        """取消处于草稿或已提交状态的报销单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            expense_report_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the expense report is not found or not in a cancellable status.
        """
        er = self._get_expense_report(expense_report_ref)
        if er.report_status not in ("draft", "submitted"):
            raise ValueError(f"Expense report cannot be cancelled from status '{er.report_status}'.")
        er.report_status = "cancelled"
        er.updated_at = self._now_iso()
        return json.dumps({
            "expense_report_ref": er.expense_report_ref,
            "report_status": er.report_status,
        })

    # ===================================================================
    # 报销明细行 — 报销明细行 (交通费/住宿费/餐饮费/招待费/其他差旅费用)
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_expense_lines(self, expense_report_ref: str) -> str:
        """列出指定报销单下的全部明细行。

        参数:
            expense_report_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_expense_report(expense_report_ref)
        results = []
        for el in self.db.expense_line.values():
            if el.expense_report_ref == expense_report_ref:
                results.append({
                    "expense_line_ref": el.expense_line_ref,
                    "expense_report_ref": el.expense_report_ref,
                    "expense_category": el.expense_category,
                    "expense_subcategory": el.expense_subcategory,
                    "description": el.description,
                    "currency": el.currency,
                    "amount": el.amount,
                    "approved_amount": el.approved_amount,
                    "expense_date": el.expense_date,
                    "invoice_ref": el.invoice_ref,
                    "line_status": el.line_status,
                    "rejection_reason": el.rejection_reason,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_expense_line_details(self, expense_line_ref: str) -> str:
        """获取指定报销明细行的详细信息。

        参数:
            expense_line_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        el = self._get_expense_line(expense_line_ref)
        return json.dumps({
            "expense_line_ref": el.expense_line_ref,
            "expense_report_ref": el.expense_report_ref,
            "expense_category": el.expense_category,
            "expense_subcategory": el.expense_subcategory,
            "description": el.description,
            "currency": el.currency,
            "amount": el.amount,
            "approved_amount": el.approved_amount,
            "expense_date": el.expense_date,
            "invoice_ref": el.invoice_ref,
            "receipt_file_ref": el.receipt_file_ref,
            "line_status": el.line_status,
            "rejection_reason": el.rejection_reason,
            "created_at": el.created_at,
            "updated_at": el.updated_at,
        })

    @is_tool(ToolType.WRITE)
    def add_expense_line(
        self,
        expense_report_ref: str,
        expense_category: str,
        expense_subcategory: str,
        description: str,
        currency: str,
        amount: float,
        expense_date: str,
        invoice_ref: Optional[str] = None,
        receipt_file_ref: Optional[str] = None,
    ) -> str:
        """向草稿报销单新增一条报销明细行。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            expense_report_ref: Reference to the parent expense report.
            expense_category: Expense category (travel, accommodation, meals, transportation, etc.).
            expense_subcategory: Subcategory (e.g., taxi, flight, hotel).
            description: Description of the expense item.
            currency: Currency code.
            amount: Claimed amount.
            expense_date: Date the expense was incurred (ISO 8601 date).
            invoice_ref: Reference to the associated invoice. Defaults to None.
            receipt_file_ref: Reference to the receipt file. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the expense report is not found, not in draft status, or inputs are invalid.
        """
        er = self._get_expense_report(expense_report_ref)
        if er.report_status != "draft":
            raise ValueError("Expense lines can only be added to draft expense reports.")
        valid_categories = {
            "travel", "accommodation", "meals", "transportation", "office_supplies",
            "software", "hardware", "training", "entertainment", "communication",
            "marketing", "consulting", "other"
        }
        if expense_category not in valid_categories:
            raise ValueError(f"Invalid expense_category: {expense_category}. Must be one of {valid_categories}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if invoice_ref is not None:
            self._get_invoice(invoice_ref)

        now = self._now_iso()
        ref = self._generate_ref("EL", self.db.expense_line)
        el = ExpenseLine(
            expense_line_ref=ref,
            expense_report_ref=expense_report_ref,
            expense_category=expense_category,
            expense_subcategory=expense_subcategory,
            description=description,
            currency=currency,
            amount=amount,
            approved_amount=0.0,
            expense_date=expense_date,
            invoice_ref=invoice_ref,
            receipt_file_ref=receipt_file_ref,
            line_status="pending",
            rejection_reason=None,
            created_at=now,
            updated_at=now,
        )
        self.db.expense_line[ref] = el

        # 更新报销单的总金额字段
        er.total_amount = round(er.total_amount + amount, 2)
        er.updated_at = now

        return json.dumps({
            "expense_line_ref": ref,
            "expense_report_ref": expense_report_ref,
            "expense_category": expense_category,
            "amount": amount,
            "line_status": "pending",
        })

    # ===================================================================
    # 发票 — 发票处理 / 采购发票管理 / 发票类型选择 / 发票税务处理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_invoice_details(self, invoice_ref: str) -> str:
        """获取指定发票的详细信息。

        参数:
            invoice_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        inv = self._get_invoice(invoice_ref)
        result = {
            "invoice_ref": inv.invoice_ref,
            "invoice_number": inv.invoice_number,
            "invoice_code": inv.invoice_code,
            "invoice_type": inv.invoice_type,
            "invoice_direction": inv.invoice_direction,
            "invoice_date": inv.invoice_date,
            "currency": inv.currency,
            "amount_without_tax": inv.amount_without_tax,
            "tax_amount": inv.tax_amount,
            "total_amount": inv.total_amount,
            "tax_rate": inv.tax_rate,
            "seller_name": inv.seller_name,
            "seller_tax_id": inv.seller_tax_id,
            "buyer_name": inv.buyer_name,
            "buyer_tax_id": inv.buyer_tax_id,
            "items_summary": inv.items_summary,
            "verification_status": inv.verification_status,
            "verification_code": inv.verification_code,
            "associated_resource_type": inv.associated_resource_type,
            "associated_resource_ref": inv.associated_resource_ref,
            "invoice_status": inv.invoice_status,
            "recorded_by_ref": inv.recorded_by_ref,
            "created_at": inv.created_at,
            "updated_at": inv.updated_at,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def list_invoices(
        self,
        invoice_type: Optional[str] = None,
        invoice_direction: Optional[str] = None,
        invoice_status: Optional[str] = None,
        verification_status: Optional[str] = None,
        seller_name: Optional[str] = None,
        buyer_name: Optional[str] = None,
        associated_resource_type: Optional[str] = None,
        associated_resource_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出发票。

        参数:
            invoice_type: Filter by invoice type. Defaults to None.
            invoice_direction: Filter by direction (inbound, outbound). Defaults to None.
            invoice_status: Filter by invoice status (active, voided, lost, archived). Defaults to None.
            verification_status: Filter by verification status. Defaults to None.
            seller_name: Filter by seller name (partial match). Defaults to None.
            buyer_name: Filter by buyer name (partial match). Defaults to None.
            associated_resource_type: Filter by associated resource type. Defaults to None.
            associated_resource_ref: Filter by associated resource ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, inv in self.db.invoice.items():
            if invoice_type is not None and inv.invoice_type != invoice_type:
                continue
            if invoice_direction is not None and inv.invoice_direction != invoice_direction:
                continue
            if invoice_status is not None and inv.invoice_status != invoice_status:
                continue
            if verification_status is not None and inv.verification_status != verification_status:
                continue
            if seller_name is not None and seller_name.lower() not in inv.seller_name.lower():
                continue
            if buyer_name is not None and buyer_name.lower() not in inv.buyer_name.lower():
                continue
            if associated_resource_type is not None and inv.associated_resource_type != associated_resource_type:
                continue
            if associated_resource_ref is not None and inv.associated_resource_ref != associated_resource_ref:
                continue
            results.append({
                "invoice_ref": inv.invoice_ref,
                "invoice_number": inv.invoice_number,
                "invoice_type": inv.invoice_type,
                "invoice_direction": inv.invoice_direction,
                "invoice_date": inv.invoice_date,
                "currency": inv.currency,
                "total_amount": inv.total_amount,
                "tax_amount": inv.tax_amount,
                "verification_status": inv.verification_status,
                "invoice_status": inv.invoice_status,
                "seller_name": inv.seller_name,
                "buyer_name": inv.buyer_name,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_invoice(
        self,
        invoice_number: str,
        invoice_code: str,
        invoice_type: str,
        invoice_direction: str,
        invoice_date: str,
        currency: str,
        amount_without_tax: float,
        tax_amount: float,
        total_amount: float,
        tax_rate: float,
        seller_name: str,
        seller_tax_id: str,
        buyer_name: str,
        buyer_tax_id: str,
        items_summary: str,
        recorded_by_ref: str,
        associated_resource_type: Optional[str] = None,
        associated_resource_ref: Optional[str] = None,
    ) -> str:
        """创建新的发票记录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            invoice_number: Invoice number printed on the invoice.
            invoice_code: Invoice code for tax verification.
            invoice_type: Type of invoice (vat_special, vat_general, electronic, receipt, etc.).
            invoice_direction: Direction (inbound, outbound).
            invoice_date: Date the invoice was issued (ISO 8601 date).
            currency: Currency code.
            amount_without_tax: Amount excluding tax.
            tax_amount: Tax amount.
            total_amount: Total amount including tax.
            tax_rate: Tax rate (e.g., 0.13 for 13%).
            seller_name: Name of the seller.
            seller_tax_id: Tax ID of the seller.
            buyer_name: Name of the buyer.
            buyer_tax_id: Tax ID of the buyer.
            items_summary: Summary of items on the invoice.
            recorded_by_ref: Employee ref of the person recording the invoice.
            associated_resource_type: Type of associated resource. Defaults to None.
            associated_resource_ref: Ref of associated resource. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(recorded_by_ref)
        valid_types = {"vat_special", "vat_general", "electronic", "receipt", "train_ticket", "air_ticket", "toll", "other"}
        if invoice_type not in valid_types:
            raise ValueError(f"Invalid invoice_type: {invoice_type}. Must be one of {valid_types}")
        valid_directions = {"inbound", "outbound"}
        if invoice_direction not in valid_directions:
            raise ValueError(f"Invalid invoice_direction: {invoice_direction}. Must be one of {valid_directions}")

        now = self._now_iso()
        ref = self._generate_ref("INV", self.db.invoice)
        inv = Invoice(
            invoice_ref=ref,
            invoice_number=invoice_number,
            invoice_code=invoice_code,
            invoice_type=invoice_type,
            invoice_direction=invoice_direction,
            invoice_date=invoice_date,
            currency=currency,
            amount_without_tax=amount_without_tax,
            tax_amount=tax_amount,
            total_amount=total_amount,
            tax_rate=tax_rate,
            seller_name=seller_name,
            seller_tax_id=seller_tax_id,
            buyer_name=buyer_name,
            buyer_tax_id=buyer_tax_id,
            items_summary=items_summary,
            verification_status="unverified",
            verification_code=None,
            associated_resource_type=associated_resource_type,
            associated_resource_ref=associated_resource_ref,
            invoice_file_ref=None,
            invoice_status="active",
            recorded_by_ref=recorded_by_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.invoice[ref] = inv
        return json.dumps({
            "invoice_ref": ref,
            "invoice_number": invoice_number,
            "invoice_type": invoice_type,
            "invoice_status": "active",
        })

    @is_tool(ToolType.WRITE)
    def verify_invoice(self, invoice_ref: str, verification_code: Optional[str] = None) -> str:
        """核验发票（标记为通过或失败）。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            invoice_ref: 唯一标识。
            verification_code: Verification code from tax authority. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the invoice is not found or already verified.
        """
        inv = self._get_invoice(invoice_ref)
        if inv.verification_status == "verified":
            raise ValueError("Invoice is already verified")
        if inv.invoice_status != "active":
            raise ValueError(f"Cannot verify invoice with status '{inv.invoice_status}'")
        inv.verification_status = "verified"
        inv.verification_code = verification_code
        inv.updated_at = self._now_iso()
        return json.dumps({
            "invoice_ref": inv.invoice_ref,
            "verification_status": inv.verification_status,
        })

    @is_tool(ToolType.WRITE)
    def void_invoice(self, invoice_ref: str) -> str:
        """作废有效状态的发票。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            invoice_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the invoice is not found or not in active status.
        """
        inv = self._get_invoice(invoice_ref)
        if inv.invoice_status != "active":
            raise ValueError(f"Cannot void invoice with status '{inv.invoice_status}'")
        inv.invoice_status = "voided"
        inv.updated_at = self._now_iso()
        return json.dumps({
            "invoice_ref": inv.invoice_ref,
            "invoice_status": inv.invoice_status,
        })

    # ===================================================================
    # 发票抬头 — 发票抬头信息
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_invoice_header_details(self, invoice_header_ref: str) -> str:
        """获取指定发票抬头的详细信息。

        参数:
            invoice_header_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ih = self._get_invoice_header(invoice_header_ref)
        return json.dumps({
            "invoice_header_ref": ih.invoice_header_ref,
            "header_type": ih.header_type,
            "company_name": ih.company_name,
            "tax_id": ih.tax_id,
            "registered_address": ih.registered_address,
            "registered_phone": ih.registered_phone,
            "bank_name": ih.bank_name,
            "bank_account": ih.bank_account,
            "is_default": ih.is_default,
            "header_status": ih.header_status,
            "created_at": ih.created_at,
            "updated_at": ih.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_invoice_headers(
        self,
        header_type: Optional[str] = None,
        header_status: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出发票抬头。

        参数:
            header_type: Filter by header type (company, individual). Defaults to None.
            header_status: Filter by header status (active, inactive). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ih in self.db.invoice_header.items():
            if header_type is not None and ih.header_type != header_type:
                continue
            if header_status is not None and ih.header_status != header_status:
                continue
            results.append({
                "invoice_header_ref": ih.invoice_header_ref,
                "header_type": ih.header_type,
                "company_name": ih.company_name,
                "tax_id": ih.tax_id,
                "is_default": ih.is_default,
                "header_status": ih.header_status,
            })
        return json.dumps(results)

    # ===================================================================
    # 付款申请 — 支付管理 / 企业付款流程管理 / 采购付款管理 / 特付管理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_payment_request_details(self, payment_request_ref: str) -> str:
        """获取指定付款申请的详细信息。

        参数:
            payment_request_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        pr = self._get_payment_request(payment_request_ref)
        result = {
            "payment_request_ref": pr.payment_request_ref,
            "request_number": pr.request_number,
            "applicant_ref": pr.applicant_ref,
            "department_ref": pr.department_ref,
            "payment_type": pr.payment_type,
            "payment_method": pr.payment_method,
            "currency": pr.currency,
            "amount": pr.amount,
            "payee_name": pr.payee_name,
            "payee_account": pr.payee_account,
            "payee_bank": pr.payee_bank,
            "source_account_ref": pr.source_account_ref,
            "associated_resource_type": pr.associated_resource_type,
            "associated_resource_ref": pr.associated_resource_ref,
            "budget_ref": pr.budget_ref,
            "purpose": pr.purpose,
            "planned_payment_date": pr.planned_payment_date,
            "request_status": pr.request_status,
            "current_approver_ref": pr.current_approver_ref,
            "submitted_at": pr.submitted_at,
            "approved_at": pr.approved_at,
            "rejected_reason": pr.rejected_reason,
            "urgency": pr.urgency,
            "notes": pr.notes,
            "created_at": pr.created_at,
            "updated_at": pr.updated_at,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def list_payment_requests(
        self,
        applicant_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        payment_type: Optional[str] = None,
        request_status: Optional[str] = None,
        urgency: Optional[str] = None,
        current_approver_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出付款申请。

        参数:
            applicant_ref: Filter by applicant employee ref. Defaults to None.
            department_ref: Filter by department ref. Defaults to None.
            payment_type: Filter by payment type. Defaults to None.
            request_status: Filter by request status. Defaults to None.
            urgency: Filter by urgency (normal, urgent, critical). Defaults to None.
            current_approver_ref: Filter by current approver employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, pr in self.db.payment_request.items():
            if applicant_ref is not None and pr.applicant_ref != applicant_ref:
                continue
            if department_ref is not None and pr.department_ref != department_ref:
                continue
            if payment_type is not None and pr.payment_type != payment_type:
                continue
            if request_status is not None and pr.request_status != request_status:
                continue
            if urgency is not None and pr.urgency != urgency:
                continue
            if current_approver_ref is not None and pr.current_approver_ref != current_approver_ref:
                continue
            results.append({
                "payment_request_ref": pr.payment_request_ref,
                "request_number": pr.request_number,
                "applicant_ref": pr.applicant_ref,
                "payment_type": pr.payment_type,
                "currency": pr.currency,
                "amount": pr.amount,
                "payee_name": pr.payee_name,
                "request_status": pr.request_status,
                "urgency": pr.urgency,
                "planned_payment_date": pr.planned_payment_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_payment_request(
        self,
        applicant_ref: str,
        department_ref: str,
        payment_type: str,
        payment_method: str,
        currency: str,
        amount: float,
        payee_name: str,
        payee_account: str,
        payee_bank: str,
        purpose: str,
        planned_payment_date: str,
        urgency: str = "normal",
        source_account_ref: Optional[str] = None,
        associated_resource_type: Optional[str] = None,
        associated_resource_ref: Optional[str] = None,
        budget_ref: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态付款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            applicant_ref: Employee ref of the applicant.
            department_ref: Department ref of the applicant.
            payment_type: Type of payment (procurement, service, reimbursement, salary, bonus, refund, loan_disbursement, other).
            payment_method: Payment method (bank_transfer, check, cash, alipay, wechat_pay, internal_transfer).
            currency: Currency code.
            amount: Payment amount.
            payee_name: Name of the payee.
            payee_account: Account of the payee.
            payee_bank: Bank of the payee.
            purpose: Purpose of the payment.
            planned_payment_date: Planned payment date (ISO 8601 date).
            urgency: Urgency level (normal, urgent, critical). Defaults to "normal".
            source_account_ref: Source finance account ref. Defaults to None.
            associated_resource_type: Associated resource type. Defaults to None.
            associated_resource_ref: Associated resource ref. Defaults to None.
            budget_ref: Budget ref to charge against. Defaults to None.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(applicant_ref)
        self._get_department(department_ref)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if source_account_ref is not None:
            self._get_finance_account(source_account_ref)
        if budget_ref is not None:
            self._get_budget(budget_ref)

        valid_payment_types = {"procurement", "service", "reimbursement", "salary", "bonus", "refund", "loan_disbursement", "other"}
        if payment_type not in valid_payment_types:
            raise ValueError(f"Invalid payment_type: {payment_type}. Must be one of {valid_payment_types}")
        valid_methods = {"bank_transfer", "check", "cash", "alipay", "wechat_pay", "internal_transfer"}
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment_method: {payment_method}. Must be one of {valid_methods}")
        valid_urgencies = {"normal", "urgent", "critical"}
        if urgency not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {urgency}. Must be one of {valid_urgencies}")

        now = self._now_iso()
        ref = self._generate_ref("PR", self.db.payment_request)
        idx = len(self.db.payment_request) + 1
        request_number = f"PR-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        pr = PaymentRequest(
            payment_request_ref=ref,
            request_number=request_number,
            applicant_ref=applicant_ref,
            department_ref=department_ref,
            payment_type=payment_type,
            payment_method=payment_method,
            currency=currency,
            amount=amount,
            payee_name=payee_name,
            payee_account=payee_account,
            payee_bank=payee_bank,
            source_account_ref=source_account_ref,
            associated_resource_type=associated_resource_type,
            associated_resource_ref=associated_resource_ref,
            budget_ref=budget_ref,
            purpose=purpose,
            planned_payment_date=planned_payment_date,
            request_status="draft",
            current_approver_ref=None,
            submitted_at=None,
            approved_at=None,
            rejected_reason=None,
            urgency=urgency,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.payment_request[ref] = pr
        return json.dumps({
            "payment_request_ref": ref,
            "request_number": request_number,
            "request_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_payment_request(self, payment_request_ref: str) -> str:
        """提交草稿付款申请进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            payment_request_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the payment request is not found or not in draft status.
        """
        pr = self._get_payment_request(payment_request_ref)
        if pr.request_status != "draft":
            raise ValueError(f"Payment request cannot be submitted from status '{pr.request_status}'.")
        now = self._now_iso()
        pr.request_status = "submitted"
        pr.submitted_at = now
        pr.updated_at = now
        return json.dumps({
            "payment_request_ref": pr.payment_request_ref,
            "request_status": pr.request_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_payment_request(self, payment_request_ref: str, approver_ref: str) -> str:
        """审批通过已提交或审核中的付款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            payment_request_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the payment request is not found or not in a valid status.
        """
        pr = self._get_payment_request(payment_request_ref)
        self._get_employee(approver_ref)
        if pr.request_status not in ("submitted", "under_review"):
            raise ValueError(f"Payment request cannot be approved from status '{pr.request_status}'.")
        now = self._now_iso()
        pr.request_status = "approved"
        pr.approved_at = now
        pr.current_approver_ref = None
        pr.updated_at = now
        return json.dumps({
            "payment_request_ref": pr.payment_request_ref,
            "request_status": pr.request_status,
        })

    @is_tool(ToolType.WRITE)
    def reject_payment_request(self, payment_request_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交或审核中的付款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            payment_request_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the payment request is not found or not in a valid status.
        """
        pr = self._get_payment_request(payment_request_ref)
        self._get_employee(approver_ref)
        if pr.request_status not in ("submitted", "under_review"):
            raise ValueError(f"Payment request cannot be rejected from status '{pr.request_status}'.")
        now = self._now_iso()
        pr.request_status = "rejected"
        pr.rejected_reason = reason
        pr.current_approver_ref = None
        pr.updated_at = now
        return json.dumps({
            "payment_request_ref": pr.payment_request_ref,
            "request_status": pr.request_status,
            "rejected_reason": reason,
        })

    @is_tool(ToolType.WRITE)
    def cancel_payment_request(self, payment_request_ref: str) -> str:
        """取消处于草稿或已提交状态的付款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            payment_request_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the payment request is not found or not in a cancellable status.
        """
        pr = self._get_payment_request(payment_request_ref)
        if pr.request_status not in ("draft", "submitted"):
            raise ValueError(f"Payment request cannot be cancelled from status '{pr.request_status}'.")
        pr.request_status = "cancelled"
        pr.updated_at = self._now_iso()
        return json.dumps({
            "payment_request_ref": pr.payment_request_ref,
            "request_status": pr.request_status,
        })

    # ===================================================================
    # 付款执行 — 支付执行
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_payment_execution_details(self, payment_execution_ref: str) -> str:
        """获取指定付款执行记录的详细信息。

        参数:
            payment_execution_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        pe = self._get_payment_execution(payment_execution_ref)
        return json.dumps({
            "payment_execution_ref": pe.payment_execution_ref,
            "payment_request_ref": pe.payment_request_ref,
            "source_account_ref": pe.source_account_ref,
            "transaction_number": pe.transaction_number,
            "currency": pe.currency,
            "amount": pe.amount,
            "exchange_rate": pe.exchange_rate,
            "settlement_currency": pe.settlement_currency,
            "settlement_amount": pe.settlement_amount,
            "payee_name": pe.payee_name,
            "payee_account": pe.payee_account,
            "payee_bank": pe.payee_bank,
            "payment_channel": pe.payment_channel,
            "execution_status": pe.execution_status,
            "executed_at": pe.executed_at,
            "executed_by_ref": pe.executed_by_ref,
            "failure_reason": pe.failure_reason,
            "bank_reference": pe.bank_reference,
            "created_at": pe.created_at,
            "updated_at": pe.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_payment_executions(
        self,
        payment_request_ref: Optional[str] = None,
        execution_status: Optional[str] = None,
        payment_channel: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出付款执行记录。

        参数:
            payment_request_ref: Filter by payment request ref. Defaults to None.
            execution_status: Filter by execution status. Defaults to None.
            payment_channel: Filter by payment channel. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, pe in self.db.payment_execution.items():
            if payment_request_ref is not None and pe.payment_request_ref != payment_request_ref:
                continue
            if execution_status is not None and pe.execution_status != execution_status:
                continue
            if payment_channel is not None and pe.payment_channel != payment_channel:
                continue
            results.append({
                "payment_execution_ref": pe.payment_execution_ref,
                "payment_request_ref": pe.payment_request_ref,
                "transaction_number": pe.transaction_number,
                "currency": pe.currency,
                "amount": pe.amount,
                "payee_name": pe.payee_name,
                "payment_channel": pe.payment_channel,
                "execution_status": pe.execution_status,
                "executed_at": pe.executed_at,
            })
        return json.dumps(results)

    # ===================================================================
    # 收款记录 — 收款流水处理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_receipt_record_details(self, receipt_record_ref: str) -> str:
        """获取指定收款记录的详细信息。

        参数:
            receipt_record_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        rr = self._get_receipt_record(receipt_record_ref)
        return json.dumps({
            "receipt_record_ref": rr.receipt_record_ref,
            "receipt_number": rr.receipt_number,
            "finance_account_ref": rr.finance_account_ref,
            "payer_name": rr.payer_name,
            "payer_account": rr.payer_account,
            "currency": rr.currency,
            "amount": rr.amount,
            "receipt_date": rr.receipt_date,
            "receipt_channel": rr.receipt_channel,
            "receipt_type": rr.receipt_type,
            "reconciliation_status": rr.reconciliation_status,
            "matched_resource_type": rr.matched_resource_type,
            "matched_resource_ref": rr.matched_resource_ref,
            "bank_reference": rr.bank_reference,
            "notes": rr.notes,
            "recorded_by_ref": rr.recorded_by_ref,
            "created_at": rr.created_at,
            "updated_at": rr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_receipt_records(
        self,
        finance_account_ref: Optional[str] = None,
        receipt_type: Optional[str] = None,
        reconciliation_status: Optional[str] = None,
        receipt_channel: Optional[str] = None,
        payer_name: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出收款记录。

        参数:
            finance_account_ref: Filter by finance account ref. Defaults to None.
            receipt_type: Filter by receipt type. Defaults to None.
            reconciliation_status: Filter by reconciliation status. Defaults to None.
            receipt_channel: Filter by receipt channel. Defaults to None.
            payer_name: Filter by payer name (partial match). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, rr in self.db.receipt_record.items():
            if finance_account_ref is not None and rr.finance_account_ref != finance_account_ref:
                continue
            if receipt_type is not None and rr.receipt_type != receipt_type:
                continue
            if reconciliation_status is not None and rr.reconciliation_status != reconciliation_status:
                continue
            if receipt_channel is not None and rr.receipt_channel != receipt_channel:
                continue
            if payer_name is not None and payer_name.lower() not in rr.payer_name.lower():
                continue
            results.append({
                "receipt_record_ref": rr.receipt_record_ref,
                "receipt_number": rr.receipt_number,
                "finance_account_ref": rr.finance_account_ref,
                "payer_name": rr.payer_name,
                "currency": rr.currency,
                "amount": rr.amount,
                "receipt_date": rr.receipt_date,
                "receipt_type": rr.receipt_type,
                "reconciliation_status": rr.reconciliation_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_receipt_reconciliation_status(
        self,
        receipt_record_ref: str,
        reconciliation_status: str,
        matched_resource_type: Optional[str] = None,
        matched_resource_ref: Optional[str] = None,
    ) -> str:
        """更新收款记录的对账状态。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            receipt_record_ref: 唯一标识。
            reconciliation_status: New reconciliation status (unmatched, matched, partial_matched, disputed).
            matched_resource_type: Type of matched resource. Defaults to None.
            matched_resource_ref: Ref of matched resource. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the receipt record is not found or the status is invalid.
        """
        rr = self._get_receipt_record(receipt_record_ref)
        valid_statuses = {"unmatched", "matched", "partial_matched", "disputed"}
        if reconciliation_status not in valid_statuses:
            raise ValueError(f"Invalid reconciliation_status: {reconciliation_status}. Must be one of {valid_statuses}")
        rr.reconciliation_status = reconciliation_status
        rr.matched_resource_type = matched_resource_type
        rr.matched_resource_ref = matched_resource_ref
        rr.updated_at = self._now_iso()
        return json.dumps({
            "receipt_record_ref": rr.receipt_record_ref,
            "reconciliation_status": rr.reconciliation_status,
        })

    # ===================================================================
    # 退款 — 退货退款 / 退款处理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_refund_details(self, refund_ref: str) -> str:
        """获取指定退款单的详细信息。

        参数:
            refund_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        r = self._get_refund(refund_ref)
        return json.dumps({
            "refund_ref": r.refund_ref,
            "refund_number": r.refund_number,
            "applicant_ref": r.applicant_ref,
            "refund_type": r.refund_type,
            "customer_name": r.customer_name,
            "original_payment_ref": r.original_payment_ref,
            "original_receipt_ref": r.original_receipt_ref,
            "currency": r.currency,
            "refund_amount": r.refund_amount,
            "reason_category": r.reason_category,
            "reason_detail": r.reason_detail,
            "refund_method": r.refund_method,
            "target_account": r.target_account,
            "refund_status": r.refund_status,
            "current_approver_ref": r.current_approver_ref,
            "submitted_at": r.submitted_at,
            "approved_at": r.approved_at,
            "executed_at": r.executed_at,
            "rejected_reason": r.rejected_reason,
            "notes": r.notes,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_refunds(
        self,
        applicant_ref: Optional[str] = None,
        refund_type: Optional[str] = None,
        refund_status: Optional[str] = None,
        customer_name: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出退款单。

        参数:
            applicant_ref: Filter by applicant employee ref. Defaults to None.
            refund_type: Filter by refund type. Defaults to None.
            refund_status: Filter by refund status. Defaults to None.
            customer_name: Filter by customer name (partial match). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, r in self.db.refund.items():
            if applicant_ref is not None and r.applicant_ref != applicant_ref:
                continue
            if refund_type is not None and r.refund_type != refund_type:
                continue
            if refund_status is not None and r.refund_status != refund_status:
                continue
            if customer_name is not None and customer_name.lower() not in r.customer_name.lower():
                continue
            results.append({
                "refund_ref": r.refund_ref,
                "refund_number": r.refund_number,
                "applicant_ref": r.applicant_ref,
                "refund_type": r.refund_type,
                "customer_name": r.customer_name,
                "currency": r.currency,
                "refund_amount": r.refund_amount,
                "refund_status": r.refund_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_refund(
        self,
        applicant_ref: str,
        refund_type: str,
        customer_name: str,
        currency: str,
        refund_amount: float,
        reason_category: str,
        reason_detail: str,
        refund_method: str,
        original_payment_ref: Optional[str] = None,
        original_receipt_ref: Optional[str] = None,
        target_account: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态退款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            applicant_ref: Employee ref of the applicant.
            refund_type: Type of refund (customer_return, service_cancellation, overcharge, duplicate_payment, other).
            customer_name: Name of the customer receiving the refund.
            currency: Currency code.
            refund_amount: Amount to be refunded.
            reason_category: Category of reason (product_defect, service_issue, customer_request, billing_error, policy_compliance, other).
            reason_detail: Detailed description of the refund reason.
            refund_method: Method of refund (original_channel, bank_transfer, cash, credit_note).
            original_payment_ref: Reference to original payment execution. Defaults to None.
            original_receipt_ref: Reference to original receipt record. Defaults to None.
            target_account: Target account for refund. Defaults to None.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(applicant_ref)
        if refund_amount <= 0:
            raise ValueError("refund_amount must be positive")
        valid_types = {"customer_return", "service_cancellation", "overcharge", "duplicate_payment", "other"}
        if refund_type not in valid_types:
            raise ValueError(f"Invalid refund_type: {refund_type}. Must be one of {valid_types}")
        valid_reasons = {"product_defect", "service_issue", "customer_request", "billing_error", "policy_compliance", "other"}
        if reason_category not in valid_reasons:
            raise ValueError(f"Invalid reason_category: {reason_category}. Must be one of {valid_reasons}")
        valid_methods = {"original_channel", "bank_transfer", "cash", "credit_note"}
        if refund_method not in valid_methods:
            raise ValueError(f"Invalid refund_method: {refund_method}. Must be one of {valid_methods}")

        now = self._now_iso()
        ref = self._generate_ref("RF", self.db.refund)
        idx = len(self.db.refund) + 1
        refund_number = f"RF-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        refund = Refund(
            refund_ref=ref,
            refund_number=refund_number,
            applicant_ref=applicant_ref,
            refund_type=refund_type,
            customer_name=customer_name,
            original_payment_ref=original_payment_ref,
            original_receipt_ref=original_receipt_ref,
            currency=currency,
            refund_amount=refund_amount,
            reason_category=reason_category,
            reason_detail=reason_detail,
            refund_method=refund_method,
            target_account=target_account,
            refund_status="draft",
            current_approver_ref=None,
            submitted_at=None,
            approved_at=None,
            executed_at=None,
            rejected_reason=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.refund[ref] = refund
        return json.dumps({
            "refund_ref": ref,
            "refund_number": refund_number,
            "refund_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_refund(self, refund_ref: str) -> str:
        """提交草稿退款申请进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            refund_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the refund is not found or not in draft status.
        """
        r = self._get_refund(refund_ref)
        if r.refund_status != "draft":
            raise ValueError(f"Refund cannot be submitted from status '{r.refund_status}'.")
        now = self._now_iso()
        r.refund_status = "submitted"
        r.submitted_at = now
        r.updated_at = now
        return json.dumps({
            "refund_ref": r.refund_ref,
            "refund_status": r.refund_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_refund(self, refund_ref: str, approver_ref: str) -> str:
        """审批通过已提交或审核中的退款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            refund_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the refund is not found or not in a valid status.
        """
        r = self._get_refund(refund_ref)
        self._get_employee(approver_ref)
        if r.refund_status not in ("submitted", "under_review"):
            raise ValueError(f"Refund cannot be approved from status '{r.refund_status}'.")
        now = self._now_iso()
        r.refund_status = "approved"
        r.approved_at = now
        r.current_approver_ref = None
        r.updated_at = now
        return json.dumps({
            "refund_ref": r.refund_ref,
            "refund_status": r.refund_status,
        })

    @is_tool(ToolType.WRITE)
    def reject_refund(self, refund_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交或审核中的退款申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            refund_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the refund is not found or not in a valid status.
        """
        r = self._get_refund(refund_ref)
        self._get_employee(approver_ref)
        if r.refund_status not in ("submitted", "under_review"):
            raise ValueError(f"Refund cannot be rejected from status '{r.refund_status}'.")
        now = self._now_iso()
        r.refund_status = "rejected"
        r.rejected_reason = reason
        r.current_approver_ref = None
        r.updated_at = now
        return json.dumps({
            "refund_ref": r.refund_ref,
            "refund_status": r.refund_status,
            "rejected_reason": reason,
        })

    # ===================================================================
    # 员工借款 — 员工借款
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_employee_loan_details(self, employee_loan_ref: str) -> str:
        """获取指定员工借款的详细信息。

        参数:
            employee_loan_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        el = self._get_employee_loan(employee_loan_ref)
        return json.dumps({
            "employee_loan_ref": el.employee_loan_ref,
            "loan_number": el.loan_number,
            "borrower_ref": el.borrower_ref,
            "department_ref": el.department_ref,
            "loan_purpose": el.loan_purpose,
            "currency": el.currency,
            "loan_amount": el.loan_amount,
            "repaid_amount": el.repaid_amount,
            "outstanding_amount": el.outstanding_amount,
            "loan_date": el.loan_date,
            "due_date": el.due_date,
            "loan_status": el.loan_status,
            "current_approver_ref": el.current_approver_ref,
            "approved_at": el.approved_at,
            "disbursed_at": el.disbursed_at,
            "settled_at": el.settled_at,
            "offset_expense_report_ref": el.offset_expense_report_ref,
            "notes": el.notes,
            "created_at": el.created_at,
            "updated_at": el.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_employee_loans(
        self,
        borrower_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        loan_status: Optional[str] = None,
        loan_purpose: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出员工借款。

        参数:
            borrower_ref: Filter by borrower employee ref. Defaults to None.
            department_ref: Filter by department ref. Defaults to None.
            loan_status: Filter by loan status. Defaults to None.
            loan_purpose: Filter by loan purpose. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, el in self.db.employee_loan.items():
            if borrower_ref is not None and el.borrower_ref != borrower_ref:
                continue
            if department_ref is not None and el.department_ref != department_ref:
                continue
            if loan_status is not None and el.loan_status != loan_status:
                continue
            if loan_purpose is not None and el.loan_purpose != loan_purpose:
                continue
            results.append({
                "employee_loan_ref": el.employee_loan_ref,
                "loan_number": el.loan_number,
                "borrower_ref": el.borrower_ref,
                "loan_purpose": el.loan_purpose,
                "currency": el.currency,
                "loan_amount": el.loan_amount,
                "outstanding_amount": el.outstanding_amount,
                "loan_status": el.loan_status,
                "due_date": el.due_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_employee_loan(
        self,
        borrower_ref: str,
        department_ref: str,
        loan_purpose: str,
        currency: str,
        loan_amount: float,
        loan_date: str,
        due_date: str,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态员工借款。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            borrower_ref: Employee ref of the borrower.
            department_ref: Department ref of the borrower.
            loan_purpose: Purpose of the loan (travel_advance, project_advance, emergency, other).
            currency: Currency code.
            loan_amount: Total loan amount.
            loan_date: Date the loan is issued (ISO 8601 date).
            due_date: Due date for repayment (ISO 8601 date).
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(borrower_ref)
        self._get_department(department_ref)
        if loan_amount <= 0:
            raise ValueError("loan_amount must be positive")
        valid_purposes = {"travel_advance", "project_advance", "emergency", "other"}
        if loan_purpose not in valid_purposes:
            raise ValueError(f"Invalid loan_purpose: {loan_purpose}. Must be one of {valid_purposes}")

        now = self._now_iso()
        ref = self._generate_ref("EL", self.db.employee_loan)
        idx = len(self.db.employee_loan) + 1
        loan_number = f"EL-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        loan = EmployeeLoan(
            employee_loan_ref=ref,
            loan_number=loan_number,
            borrower_ref=borrower_ref,
            department_ref=department_ref,
            loan_purpose=loan_purpose,
            currency=currency,
            loan_amount=loan_amount,
            repaid_amount=0.0,
            outstanding_amount=loan_amount,
            loan_date=loan_date,
            due_date=due_date,
            loan_status="draft",
            current_approver_ref=None,
            approved_at=None,
            disbursed_at=None,
            settled_at=None,
            offset_expense_report_ref=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.employee_loan[ref] = loan
        return json.dumps({
            "employee_loan_ref": ref,
            "loan_number": loan_number,
            "loan_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_employee_loan(self, employee_loan_ref: str) -> str:
        """提交草稿员工借款进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            employee_loan_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the loan is not found or not in draft status.
        """
        el = self._get_employee_loan(employee_loan_ref)
        if el.loan_status != "draft":
            raise ValueError(f"Employee loan cannot be submitted from status '{el.loan_status}'.")
        el.loan_status = "submitted"
        el.updated_at = self._now_iso()
        return json.dumps({
            "employee_loan_ref": el.employee_loan_ref,
            "loan_status": el.loan_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_employee_loan(self, employee_loan_ref: str, approver_ref: str) -> str:
        """审批通过已提交的员工借款。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            employee_loan_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the loan is not found or not in submitted status.
        """
        el = self._get_employee_loan(employee_loan_ref)
        self._get_employee(approver_ref)
        if el.loan_status != "submitted":
            raise ValueError(f"Employee loan cannot be approved from status '{el.loan_status}'.")
        now = self._now_iso()
        el.loan_status = "approved"
        el.approved_at = now
        el.current_approver_ref = None
        el.updated_at = now
        return json.dumps({
            "employee_loan_ref": el.employee_loan_ref,
            "loan_status": el.loan_status,
        })

    @is_tool(ToolType.WRITE)
    def reject_employee_loan(self, employee_loan_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交的员工借款。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            employee_loan_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the loan is not found or not in submitted status.
        """
        el = self._get_employee_loan(employee_loan_ref)
        self._get_employee(approver_ref)
        if el.loan_status != "submitted":
            raise ValueError(f"Employee loan cannot be rejected from status '{el.loan_status}'.")
        now = self._now_iso()
        el.loan_status = "rejected"
        el.notes = f"{el.notes}\nRejection reason: {reason}" if el.notes else f"Rejection reason: {reason}"
        el.current_approver_ref = None
        el.updated_at = now
        return json.dumps({
            "employee_loan_ref": el.employee_loan_ref,
            "loan_status": el.loan_status,
        })

    # ===================================================================
    # 借款还款 — 员工借款还款
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_loan_repayments(self, employee_loan_ref: str) -> str:
        """列出指定员工借款下的全部还款记录。

        参数:
            employee_loan_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_employee_loan(employee_loan_ref)
        results = []
        for lr in self.db.loan_repayment.values():
            if lr.employee_loan_ref == employee_loan_ref:
                results.append({
                    "loan_repayment_ref": lr.loan_repayment_ref,
                    "employee_loan_ref": lr.employee_loan_ref,
                    "repayment_amount": lr.repayment_amount,
                    "repayment_method": lr.repayment_method,
                    "repayment_date": lr.repayment_date,
                    "notes": lr.notes,
                    "created_at": lr.created_at,
                })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_loan_repayment(
        self,
        employee_loan_ref: str,
        repayment_amount: float,
        repayment_method: str,
        repayment_date: str,
        notes: str = "",
    ) -> str:
        """登记一笔员工借款还款记录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            employee_loan_ref: Reference to the employee loan.
            repayment_amount: Amount being repaid.
            repayment_method: Method of repayment (salary_deduction, bank_transfer, cash, expense_offset).
            repayment_date: Date of repayment (ISO 8601 date).
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the loan is not found, not in active/overdue status, or amount exceeds outstanding.
        """
        el = self._get_employee_loan(employee_loan_ref)
        if el.loan_status not in ("active", "overdue"):
            raise ValueError(f"Repayments can only be made on active or overdue loans. Current status: '{el.loan_status}'.")
        if repayment_amount <= 0:
            raise ValueError("repayment_amount must be positive")
        if repayment_amount > el.outstanding_amount:
            raise ValueError(f"Repayment amount ({repayment_amount}) exceeds outstanding amount ({el.outstanding_amount})")
        valid_methods = {"salary_deduction", "bank_transfer", "cash", "expense_offset"}
        if repayment_method not in valid_methods:
            raise ValueError(f"Invalid repayment_method: {repayment_method}. Must be one of {valid_methods}")

        now = self._now_iso()
        ref = self._generate_ref("LR", self.db.loan_repayment)
        lr = LoanRepayment(
            loan_repayment_ref=ref,
            employee_loan_ref=employee_loan_ref,
            repayment_amount=repayment_amount,
            repayment_method=repayment_method,
            repayment_date=repayment_date,
            notes=notes,
            created_at=now,
        )
        self.db.loan_repayment[ref] = lr

        # 更新借款状态
        el.repaid_amount = round(el.repaid_amount + repayment_amount, 2)
        el.outstanding_amount = round(el.outstanding_amount - repayment_amount, 2)
        if el.outstanding_amount <= 0:
            el.loan_status = "settled"
            el.settled_at = now
        el.updated_at = now

        return json.dumps({
            "loan_repayment_ref": ref,
            "employee_loan_ref": employee_loan_ref,
            "repayment_amount": repayment_amount,
            "outstanding_amount": el.outstanding_amount,
            "loan_status": el.loan_status,
        })

    # ===================================================================
    # 结算单 — 结算单管理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_settlement_details(self, settlement_ref: str) -> str:
        """获取指定结算单的详细信息。

        参数:
            settlement_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        s = self._get_settlement(settlement_ref)
        return json.dumps({
            "settlement_ref": s.settlement_ref,
            "settlement_number": s.settlement_number,
            "counterparty_type": s.counterparty_type,
            "counterparty_name": s.counterparty_name,
            "counterparty_id": s.counterparty_id,
            "settlement_period_start": s.settlement_period_start,
            "settlement_period_end": s.settlement_period_end,
            "currency": s.currency,
            "gross_amount": s.gross_amount,
            "adjustment_amount": s.adjustment_amount,
            "net_amount": s.net_amount,
            "settlement_status": s.settlement_status,
            "current_approver_ref": s.current_approver_ref,
            "submitted_at": s.submitted_at,
            "approved_at": s.approved_at,
            "settled_at": s.settled_at,
            "payment_request_ref": s.payment_request_ref,
            "notes": s.notes,
            "prepared_by_ref": s.prepared_by_ref,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_settlements(
        self,
        counterparty_type: Optional[str] = None,
        counterparty_name: Optional[str] = None,
        settlement_status: Optional[str] = None,
        prepared_by_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出结算单。

        参数:
            counterparty_type: Filter by counterparty type (supplier, customer, partner, employee). Defaults to None.
            counterparty_name: Filter by counterparty name (partial match). Defaults to None.
            settlement_status: Filter by settlement status. Defaults to None.
            prepared_by_ref: Filter by the preparer employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, s in self.db.settlement.items():
            if counterparty_type is not None and s.counterparty_type != counterparty_type:
                continue
            if counterparty_name is not None and counterparty_name.lower() not in s.counterparty_name.lower():
                continue
            if settlement_status is not None and s.settlement_status != settlement_status:
                continue
            if prepared_by_ref is not None and s.prepared_by_ref != prepared_by_ref:
                continue
            results.append({
                "settlement_ref": s.settlement_ref,
                "settlement_number": s.settlement_number,
                "counterparty_type": s.counterparty_type,
                "counterparty_name": s.counterparty_name,
                "currency": s.currency,
                "net_amount": s.net_amount,
                "settlement_status": s.settlement_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_settlement_lines(self, settlement_ref: str) -> str:
        """列出指定结算单下的全部明细行。

        参数:
            settlement_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_settlement(settlement_ref)
        results = []
        for sl in self.db.settlement_line.values():
            if sl.settlement_ref == settlement_ref:
                results.append({
                    "settlement_line_ref": sl.settlement_line_ref,
                    "settlement_ref": sl.settlement_ref,
                    "description": sl.description,
                    "quantity": sl.quantity,
                    "unit_price": sl.unit_price,
                    "amount": sl.amount,
                    "tax_rate": sl.tax_rate,
                    "tax_amount": sl.tax_amount,
                    "invoice_ref": sl.invoice_ref,
                })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def submit_settlement(self, settlement_ref: str) -> str:
        """提交草稿结算单进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            settlement_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the settlement is not found or not in draft status.
        """
        s = self._get_settlement(settlement_ref)
        if s.settlement_status != "draft":
            raise ValueError(f"Settlement cannot be submitted from status '{s.settlement_status}'.")
        now = self._now_iso()
        s.settlement_status = "submitted"
        s.submitted_at = now
        s.updated_at = now
        return json.dumps({
            "settlement_ref": s.settlement_ref,
            "settlement_status": s.settlement_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_settlement(self, settlement_ref: str, approver_ref: str) -> str:
        """审批通过已提交的结算单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            settlement_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the settlement is not found or not in submitted status.
        """
        s = self._get_settlement(settlement_ref)
        self._get_employee(approver_ref)
        if s.settlement_status != "submitted":
            raise ValueError(f"Settlement cannot be approved from status '{s.settlement_status}'.")
        now = self._now_iso()
        s.settlement_status = "approved"
        s.approved_at = now
        s.current_approver_ref = None
        s.updated_at = now
        return json.dumps({
            "settlement_ref": s.settlement_ref,
            "settlement_status": s.settlement_status,
        })

    @is_tool(ToolType.WRITE)
    def reject_settlement(self, settlement_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交的结算单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            settlement_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the settlement is not found or not in submitted status.
        """
        s = self._get_settlement(settlement_ref)
        self._get_employee(approver_ref)
        if s.settlement_status != "submitted":
            raise ValueError(f"Settlement cannot be rejected from status '{s.settlement_status}'.")
        now = self._now_iso()
        s.settlement_status = "rejected"
        s.notes = f"{s.notes}\nRejection reason: {reason}" if s.notes else f"Rejection reason: {reason}"
        s.current_approver_ref = None
        s.updated_at = now
        return json.dumps({
            "settlement_ref": s.settlement_ref,
            "settlement_status": s.settlement_status,
        })

    # ===================================================================
    # 资金调拨 — 资金调拨
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_fund_transfer_details(self, fund_transfer_ref: str) -> str:
        """获取指定资金调拨单的详细信息。

        参数:
            fund_transfer_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ft = self._get_fund_transfer(fund_transfer_ref)
        return json.dumps({
            "fund_transfer_ref": ft.fund_transfer_ref,
            "transfer_number": ft.transfer_number,
            "applicant_ref": ft.applicant_ref,
            "source_account_ref": ft.source_account_ref,
            "target_account_ref": ft.target_account_ref,
            "currency": ft.currency,
            "amount": ft.amount,
            "exchange_rate": ft.exchange_rate,
            "target_currency": ft.target_currency,
            "target_amount": ft.target_amount,
            "transfer_reason": ft.transfer_reason,
            "transfer_status": ft.transfer_status,
            "current_approver_ref": ft.current_approver_ref,
            "approved_at": ft.approved_at,
            "executed_at": ft.executed_at,
            "notes": ft.notes,
            "created_at": ft.created_at,
            "updated_at": ft.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_fund_transfers(
        self,
        applicant_ref: Optional[str] = None,
        transfer_status: Optional[str] = None,
        source_account_ref: Optional[str] = None,
        target_account_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出资金调拨单。

        参数:
            applicant_ref: Filter by applicant employee ref. Defaults to None.
            transfer_status: Filter by transfer status. Defaults to None.
            source_account_ref: Filter by source account ref. Defaults to None.
            target_account_ref: Filter by target account ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ft in self.db.fund_transfer.items():
            if applicant_ref is not None and ft.applicant_ref != applicant_ref:
                continue
            if transfer_status is not None and ft.transfer_status != transfer_status:
                continue
            if source_account_ref is not None and ft.source_account_ref != source_account_ref:
                continue
            if target_account_ref is not None and ft.target_account_ref != target_account_ref:
                continue
            results.append({
                "fund_transfer_ref": ft.fund_transfer_ref,
                "transfer_number": ft.transfer_number,
                "applicant_ref": ft.applicant_ref,
                "source_account_ref": ft.source_account_ref,
                "target_account_ref": ft.target_account_ref,
                "currency": ft.currency,
                "amount": ft.amount,
                "transfer_status": ft.transfer_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_fund_transfer(
        self,
        applicant_ref: str,
        source_account_ref: str,
        target_account_ref: str,
        currency: str,
        amount: float,
        transfer_reason: str,
        exchange_rate: Optional[float] = None,
        target_currency: Optional[str] = None,
        target_amount: Optional[float] = None,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态资金调拨申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            applicant_ref: Employee ref of the applicant.
            source_account_ref: Source finance account ref.
            target_account_ref: Target finance account ref.
            currency: Currency code of the source.
            amount: Transfer amount in source currency.
            transfer_reason: Reason for the transfer.
            exchange_rate: Exchange rate for cross-currency transfers. Defaults to None.
            target_currency: Target currency if different. Defaults to None.
            target_amount: Amount in target currency. Defaults to None.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(applicant_ref)
        self._get_finance_account(source_account_ref)
        self._get_finance_account(target_account_ref)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if source_account_ref == target_account_ref:
            raise ValueError("Source and target accounts must be different")

        now = self._now_iso()
        ref = self._generate_ref("FT", self.db.fund_transfer)
        idx = len(self.db.fund_transfer) + 1
        transfer_number = f"FT-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        ft = FundTransfer(
            fund_transfer_ref=ref,
            transfer_number=transfer_number,
            applicant_ref=applicant_ref,
            source_account_ref=source_account_ref,
            target_account_ref=target_account_ref,
            currency=currency,
            amount=amount,
            exchange_rate=exchange_rate,
            target_currency=target_currency,
            target_amount=target_amount,
            transfer_reason=transfer_reason,
            transfer_status="draft",
            current_approver_ref=None,
            approved_at=None,
            executed_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.fund_transfer[ref] = ft
        return json.dumps({
            "fund_transfer_ref": ref,
            "transfer_number": transfer_number,
            "transfer_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_fund_transfer(self, fund_transfer_ref: str) -> str:
        """提交草稿资金调拨申请进入审批。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            fund_transfer_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the fund transfer is not found or not in draft status.
        """
        ft = self._get_fund_transfer(fund_transfer_ref)
        if ft.transfer_status != "draft":
            raise ValueError(f"Fund transfer cannot be submitted from status '{ft.transfer_status}'.")
        ft.transfer_status = "submitted"
        ft.updated_at = self._now_iso()
        return json.dumps({
            "fund_transfer_ref": ft.fund_transfer_ref,
            "transfer_status": ft.transfer_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_fund_transfer(self, fund_transfer_ref: str, approver_ref: str) -> str:
        """审批通过已提交的资金调拨申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            fund_transfer_ref: 唯一标识。
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the fund transfer is not found or not in submitted status.
        """
        ft = self._get_fund_transfer(fund_transfer_ref)
        self._get_employee(approver_ref)
        if ft.transfer_status != "submitted":
            raise ValueError(f"Fund transfer cannot be approved from status '{ft.transfer_status}'.")
        now = self._now_iso()
        ft.transfer_status = "approved"
        ft.approved_at = now
        ft.current_approver_ref = None
        ft.updated_at = now
        return json.dumps({
            "fund_transfer_ref": ft.fund_transfer_ref,
            "transfer_status": ft.transfer_status,
        })

    @is_tool(ToolType.WRITE)
    def reject_fund_transfer(self, fund_transfer_ref: str, approver_ref: str, reason: str) -> str:
        """驳回已提交的资金调拨申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            fund_transfer_ref: 唯一标识。
            approver_ref: Employee ref of the approver.
            reason: Reason for rejection.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the fund transfer is not found or not in submitted status.
        """
        ft = self._get_fund_transfer(fund_transfer_ref)
        self._get_employee(approver_ref)
        if ft.transfer_status != "submitted":
            raise ValueError(f"Fund transfer cannot be rejected from status '{ft.transfer_status}'.")
        now = self._now_iso()
        ft.transfer_status = "rejected"
        ft.notes = f"{ft.notes}\nRejection reason: {reason}" if ft.notes else f"Rejection reason: {reason}"
        ft.current_approver_ref = None
        ft.updated_at = now
        return json.dumps({
            "fund_transfer_ref": ft.fund_transfer_ref,
            "transfer_status": ft.transfer_status,
        })

    # ===================================================================
    # 汇率 — 汇率与外汇
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_exchange_rate_details(self, exchange_rate_ref: str) -> str:
        """获取指定汇率记录的详细信息。

        参数:
            exchange_rate_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        er = self._get_exchange_rate(exchange_rate_ref)
        return json.dumps({
            "exchange_rate_ref": er.exchange_rate_ref,
            "source_currency": er.source_currency,
            "target_currency": er.target_currency,
            "rate": er.rate,
            "rate_type": er.rate_type,
            "effective_date": er.effective_date,
            "created_at": er.created_at,
        })

    @is_tool(ToolType.READ)
    def list_exchange_rates(
        self,
        source_currency: Optional[str] = None,
        target_currency: Optional[str] = None,
        rate_type: Optional[str] = None,
        effective_date: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出汇率记录。

        参数:
            source_currency: Filter by source currency. Defaults to None.
            target_currency: Filter by target currency. Defaults to None.
            rate_type: Filter by rate type (central_bank, commercial, internal). Defaults to None.
            effective_date: Filter by effective date (ISO 8601 date). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, er in self.db.exchange_rate.items():
            if source_currency is not None and er.source_currency != source_currency:
                continue
            if target_currency is not None and er.target_currency != target_currency:
                continue
            if rate_type is not None and er.rate_type != rate_type:
                continue
            if effective_date is not None and er.effective_date != effective_date:
                continue
            results.append({
                "exchange_rate_ref": er.exchange_rate_ref,
                "source_currency": er.source_currency,
                "target_currency": er.target_currency,
                "rate": er.rate,
                "rate_type": er.rate_type,
                "effective_date": er.effective_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def convert_currency(
        self,
        source_currency: str,
        target_currency: str,
        amount: float,
        rate_type: str = "commercial",
    ) -> str:
        """使用最新可用汇率将金额从一种货币换算为另一种货币。

        参数:
            source_currency: Source currency code.
            target_currency: Target currency code.
            amount: Amount in source currency.
            rate_type: Type of exchange rate to use (central_bank, commercial, internal). Defaults to "commercial".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果no exchange rate is found for the given currency pair.
        """
        if source_currency == target_currency:
            return json.dumps({
                "source_currency": source_currency,
                "target_currency": target_currency,
                "source_amount": amount,
                "target_amount": amount,
                "exchange_rate": 1.0,
            })

        # 查找该货币对的最新汇率
        best_rate = None
        best_date = None
        for er in self.db.exchange_rate.values():
            if er.source_currency == source_currency and er.target_currency == target_currency and er.rate_type == rate_type:
                if best_date is None or er.effective_date > best_date:
                    best_rate = er.rate
                    best_date = er.effective_date

        if best_rate is None:
            raise ValueError(f"No exchange rate found for {source_currency} -> {target_currency} with rate_type '{rate_type}'")

        target_amount = round(amount * best_rate, 2)
        return json.dumps({
            "source_currency": source_currency,
            "target_currency": target_currency,
            "source_amount": amount,
            "target_amount": target_amount,
            "exchange_rate": best_rate,
            "effective_date": best_date,
        })

    # ===================================================================
    # 税务申报 — 税务申报 / 税务信息查询 / 发票税务处理
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_tax_filing_details(self, tax_filing_ref: str) -> str:
        """获取指定税务申报单的详细信息。

        参数:
            tax_filing_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        tf = self._get_tax_filing(tax_filing_ref)
        return json.dumps({
            "tax_filing_ref": tf.tax_filing_ref,
            "filing_number": tf.filing_number,
            "tax_type": tf.tax_type,
            "filing_period_start": tf.filing_period_start,
            "filing_period_end": tf.filing_period_end,
            "filing_deadline": tf.filing_deadline,
            "currency": tf.currency,
            "taxable_amount": tf.taxable_amount,
            "tax_rate": tf.tax_rate,
            "tax_amount": tf.tax_amount,
            "deductions_amount": tf.deductions_amount,
            "payable_amount": tf.payable_amount,
            "filing_status": tf.filing_status,
            "filed_at": tf.filed_at,
            "filed_by_ref": tf.filed_by_ref,
            "confirmation_number": tf.confirmation_number,
            "notes": tf.notes,
            "created_at": tf.created_at,
            "updated_at": tf.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_tax_filings(
        self,
        tax_type: Optional[str] = None,
        filing_status: Optional[str] = None,
        filed_by_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出税务申报单。

        参数:
            tax_type: Filter by tax type. Defaults to None.
            filing_status: Filter by filing status. Defaults to None.
            filed_by_ref: Filter by the filer employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, tf in self.db.tax_filing.items():
            if tax_type is not None and tf.tax_type != tax_type:
                continue
            if filing_status is not None and tf.filing_status != filing_status:
                continue
            if filed_by_ref is not None and tf.filed_by_ref != filed_by_ref:
                continue
            results.append({
                "tax_filing_ref": tf.tax_filing_ref,
                "filing_number": tf.filing_number,
                "tax_type": tf.tax_type,
                "filing_period_start": tf.filing_period_start,
                "filing_period_end": tf.filing_period_end,
                "filing_deadline": tf.filing_deadline,
                "payable_amount": tf.payable_amount,
                "filing_status": tf.filing_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_tax_filing_status(
        self,
        tax_filing_ref: str,
        new_status: str,
        confirmation_number: Optional[str] = None,
    ) -> str:
        """更新税务申报单状态。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            tax_filing_ref: 唯一标识。
            new_status: New filing status (draft, prepared, filed, accepted, rejected, amended).
            confirmation_number: Confirmation number from tax authority. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the tax filing is not found or the status transition is invalid.
        """
        tf = self._get_tax_filing(tax_filing_ref)
        valid_statuses = {"draft", "prepared", "filed", "accepted", "rejected", "amended"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid filing_status: {new_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        tf.filing_status = new_status
        if new_status == "filed":
            tf.filed_at = now
        if confirmation_number is not None:
            tf.confirmation_number = confirmation_number
        tf.updated_at = now
        return json.dumps({
            "tax_filing_ref": tf.tax_filing_ref,
            "filing_status": tf.filing_status,
            "confirmation_number": tf.confirmation_number,
        })

    # ===================================================================
    # 员工个税记录 — 个税申报 / 个税测算
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_employee_tax_record_details(self, employee_tax_record_ref: str) -> str:
        """获取指定员工个税记录的详细信息。

        参数:
            employee_tax_record_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        etr = self._get_employee_tax_record(employee_tax_record_ref)
        return json.dumps({
            "employee_tax_record_ref": etr.employee_tax_record_ref,
            "employee_ref": etr.employee_ref,
            "tax_period": etr.tax_period,
            "gross_income": etr.gross_income,
            "income_type": etr.income_type,
            "taxable_income": etr.taxable_income,
            "tax_exempt_amount": etr.tax_exempt_amount,
            "social_insurance_deduction": etr.social_insurance_deduction,
            "housing_fund_deduction": etr.housing_fund_deduction,
            "special_additional_deductions": etr.special_additional_deductions,
            "other_deductions": etr.other_deductions,
            "cumulative_income_ytd": etr.cumulative_income_ytd,
            "cumulative_tax_ytd": etr.cumulative_tax_ytd,
            "tax_rate_applied": etr.tax_rate_applied,
            "quick_deduction": etr.quick_deduction,
            "tax_withheld": etr.tax_withheld,
            "tax_paid": etr.tax_paid,
            "filing_status": etr.filing_status,
            "notes": etr.notes,
            "created_at": etr.created_at,
            "updated_at": etr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_employee_tax_records(
        self,
        employee_ref: Optional[str] = None,
        tax_period: Optional[str] = None,
        income_type: Optional[str] = None,
        filing_status: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出员工个税记录。

        参数:
            employee_ref: Filter by employee ref. Defaults to None.
            tax_period: Filter by tax period (YYYY-MM). Defaults to None.
            income_type: Filter by income type. Defaults to None.
            filing_status: Filter by filing status. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, etr in self.db.employee_tax_record.items():
            if employee_ref is not None and etr.employee_ref != employee_ref:
                continue
            if tax_period is not None and etr.tax_period != tax_period:
                continue
            if income_type is not None and etr.income_type != income_type:
                continue
            if filing_status is not None and etr.filing_status != filing_status:
                continue
            results.append({
                "employee_tax_record_ref": etr.employee_tax_record_ref,
                "employee_ref": etr.employee_ref,
                "tax_period": etr.tax_period,
                "gross_income": etr.gross_income,
                "income_type": etr.income_type,
                "taxable_income": etr.taxable_income,
                "tax_withheld": etr.tax_withheld,
                "filing_status": etr.filing_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def calculate_individual_income_tax(
        self,
        gross_income: float,
        tax_exempt_amount: float = 5000.0,
        social_insurance_deduction: float = 0.0,
        housing_fund_deduction: float = 0.0,
        special_additional_deductions: float = 0.0,
        other_deductions: float = 0.0,
    ) -> str:
        """按中国累进税率计算个人所得税。

        参数:
            gross_income: Monthly gross income.
            tax_exempt_amount: Tax-exempt threshold (default 5000 CNY). Defaults to 5000.0.
            social_insurance_deduction: Social insurance deduction. Defaults to 0.0.
            housing_fund_deduction: Housing provident fund deduction. Defaults to 0.0.
            special_additional_deductions: Total special additional deductions. Defaults to 0.0.
            other_deductions: Other deductions. Defaults to 0.0.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果gross_income is negative.
        """
        if gross_income < 0:
            raise ValueError("gross_income cannot be negative")

        total_deductions = tax_exempt_amount + social_insurance_deduction + housing_fund_deduction + special_additional_deductions + other_deductions
        taxable_income = max(0, gross_income - total_deductions)

        # 中国个人所得税月度累进税率表
        brackets = [
            (3000, 0.03, 0),
            (12000, 0.10, 210),
            (25000, 0.20, 1410),
            (35000, 0.25, 2660),
            (55000, 0.30, 4410),
            (80000, 0.35, 7160),
            (float('inf'), 0.45, 15160),
        ]

        tax_amount = 0.0
        tax_rate = 0.0
        quick_deduction = 0.0
        for upper, rate, qd in brackets:
            if taxable_income <= upper:
                tax_amount = round(taxable_income * rate - qd, 2)
                tax_rate = rate
                quick_deduction = qd
                break

        return json.dumps({
            "gross_income": gross_income,
            "total_deductions": round(total_deductions, 2),
            "taxable_income": round(taxable_income, 2),
            "tax_rate": tax_rate,
            "quick_deduction": quick_deduction,
            "tax_amount": max(0, tax_amount),
        })

    # ===================================================================
    # 计提分录 — 预提与计提
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_accrual_entry_details(self, accrual_entry_ref: str) -> str:
        """获取指定计提分录的详细信息。

        参数:
            accrual_entry_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ae = self._get_accrual_entry(accrual_entry_ref)
        return json.dumps({
            "accrual_entry_ref": ae.accrual_entry_ref,
            "entry_number": ae.entry_number,
            "accrual_type": ae.accrual_type,
            "accounting_period": ae.accounting_period,
            "department_ref": ae.department_ref,
            "expense_category": ae.expense_category,
            "description": ae.description,
            "currency": ae.currency,
            "amount": ae.amount,
            "reversal_period": ae.reversal_period,
            "is_reversed": ae.is_reversed,
            "reversed_at": ae.reversed_at,
            "entry_status": ae.entry_status,
            "prepared_by_ref": ae.prepared_by_ref,
            "approved_by_ref": ae.approved_by_ref,
            "created_at": ae.created_at,
            "updated_at": ae.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_accrual_entries(
        self,
        accrual_type: Optional[str] = None,
        accounting_period: Optional[str] = None,
        department_ref: Optional[str] = None,
        entry_status: Optional[str] = None,
        prepared_by_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出计提分录。

        参数:
            accrual_type: Filter by accrual type. Defaults to None.
            accounting_period: Filter by accounting period (YYYY-MM). Defaults to None.
            department_ref: Filter by department ref. Defaults to None.
            entry_status: Filter by entry status. Defaults to None.
            prepared_by_ref: Filter by preparer employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ae in self.db.accrual_entry.items():
            if accrual_type is not None and ae.accrual_type != accrual_type:
                continue
            if accounting_period is not None and ae.accounting_period != accounting_period:
                continue
            if department_ref is not None and ae.department_ref != department_ref:
                continue
            if entry_status is not None and ae.entry_status != entry_status:
                continue
            if prepared_by_ref is not None and ae.prepared_by_ref != prepared_by_ref:
                continue
            results.append({
                "accrual_entry_ref": ae.accrual_entry_ref,
                "entry_number": ae.entry_number,
                "accrual_type": ae.accrual_type,
                "accounting_period": ae.accounting_period,
                "expense_category": ae.expense_category,
                "currency": ae.currency,
                "amount": ae.amount,
                "entry_status": ae.entry_status,
                "is_reversed": ae.is_reversed,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_accrual_entry(
        self,
        accrual_type: str,
        accounting_period: str,
        expense_category: str,
        description: str,
        currency: str,
        amount: float,
        prepared_by_ref: str,
        department_ref: Optional[str] = None,
        reversal_period: Optional[str] = None,
    ) -> str:
        """创建新的草稿状态计提分录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            accrual_type: Type of accrual (expense_accrual, revenue_accrual, provision, prepaid_amortization).
            accounting_period: Accounting period in YYYY-MM format.
            expense_category: Expense or revenue category.
            description: Description of the accrual.
            currency: Currency code.
            amount: Accrual amount.
            prepared_by_ref: Employee ref of the preparer.
            department_ref: Department ref. Defaults to None.
            reversal_period: Period for reversal in YYYY-MM format. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(prepared_by_ref)
        valid_types = {"expense_accrual", "revenue_accrual", "provision", "prepaid_amortization"}
        if accrual_type not in valid_types:
            raise ValueError(f"Invalid accrual_type: {accrual_type}. Must be one of {valid_types}")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if department_ref is not None:
            self._get_department(department_ref)

        now = self._now_iso()
        ref = self._generate_ref("AC", self.db.accrual_entry)
        idx = len(self.db.accrual_entry) + 1
        entry_number = f"AC-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        ae = AccrualEntry(
            accrual_entry_ref=ref,
            entry_number=entry_number,
            accrual_type=accrual_type,
            accounting_period=accounting_period,
            department_ref=department_ref,
            expense_category=expense_category,
            description=description,
            currency=currency,
            amount=amount,
            reversal_period=reversal_period,
            is_reversed=False,
            reversed_at=None,
            entry_status="draft",
            prepared_by_ref=prepared_by_ref,
            approved_by_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.accrual_entry[ref] = ae
        return json.dumps({
            "accrual_entry_ref": ref,
            "entry_number": entry_number,
            "entry_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def post_accrual_entry(self, accrual_entry_ref: str, approved_by_ref: str) -> str:
        """过账草稿计提分录（审批并最终确认）。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            accrual_entry_ref: 唯一标识。
            approved_by_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the accrual entry is not found or not in draft status.
        """
        ae = self._get_accrual_entry(accrual_entry_ref)
        self._get_employee(approved_by_ref)
        if ae.entry_status != "draft":
            raise ValueError(f"Accrual entry cannot be posted from status '{ae.entry_status}'.")
        now = self._now_iso()
        ae.entry_status = "posted"
        ae.approved_by_ref = approved_by_ref
        ae.updated_at = now
        return json.dumps({
            "accrual_entry_ref": ae.accrual_entry_ref,
            "entry_status": ae.entry_status,
        })

    @is_tool(ToolType.WRITE)
    def reverse_accrual_entry(self, accrual_entry_ref: str) -> str:
        """冲销已过账的计提分录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            accrual_entry_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the accrual entry is not found, not posted, or already reversed.
        """
        ae = self._get_accrual_entry(accrual_entry_ref)
        if ae.entry_status != "posted":
            raise ValueError(f"Accrual entry cannot be reversed from status '{ae.entry_status}'.")
        if ae.is_reversed:
            raise ValueError("Accrual entry is already reversed")
        now = self._now_iso()
        ae.entry_status = "reversed"
        ae.is_reversed = True
        ae.reversed_at = now
        ae.updated_at = now
        return json.dumps({
            "accrual_entry_ref": ae.accrual_entry_ref,
            "entry_status": ae.entry_status,
            "is_reversed": ae.is_reversed,
        })

    # ===================================================================
    # 报销政策 — 报销政策咨询 / 财务制度咨询
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_expense_policy_details(self, expense_policy_ref: str) -> str:
        """获取指定报销政策的详细信息。

        参数:
            expense_policy_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ep = self._get_expense_policy(expense_policy_ref)
        return json.dumps({
            "expense_policy_ref": ep.expense_policy_ref,
            "policy_name": ep.policy_name,
            "policy_code": ep.policy_code,
            "expense_category": ep.expense_category,
            "applicable_position_levels": ep.applicable_position_levels,
            "applicable_worker_types": ep.applicable_worker_types,
            "city_tier": ep.city_tier,
            "currency": ep.currency,
            "daily_limit": ep.daily_limit,
            "per_occurrence_limit": ep.per_occurrence_limit,
            "monthly_limit": ep.monthly_limit,
            "requires_invoice": ep.requires_invoice,
            "requires_pre_approval": ep.requires_pre_approval,
            "policy_detail": ep.policy_detail,
            "effective_from": ep.effective_from,
            "effective_to": ep.effective_to,
            "policy_status": ep.policy_status,
            "created_at": ep.created_at,
            "updated_at": ep.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_expense_policies(
        self,
        expense_category: Optional[str] = None,
        city_tier: Optional[str] = None,
        policy_status: Optional[str] = None,
        position_level: Optional[int] = None,
        worker_type: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出报销政策。

        参数:
            expense_category: Filter by expense category. Defaults to None.
            city_tier: Filter by city tier. Defaults to None.
            policy_status: Filter by policy status (active, inactive, deprecated). Defaults to None.
            position_level: Filter by applicable position level. Defaults to None.
            worker_type: Filter by applicable worker type. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ep in self.db.expense_policy.items():
            if expense_category is not None and ep.expense_category != expense_category:
                continue
            if city_tier is not None and ep.city_tier != city_tier:
                continue
            if policy_status is not None and ep.policy_status != policy_status:
                continue
            if position_level is not None and position_level not in ep.applicable_position_levels:
                continue
            if worker_type is not None and worker_type not in ep.applicable_worker_types:
                continue
            results.append({
                "expense_policy_ref": ep.expense_policy_ref,
                "policy_name": ep.policy_name,
                "policy_code": ep.policy_code,
                "expense_category": ep.expense_category,
                "city_tier": ep.city_tier,
                "currency": ep.currency,
                "daily_limit": ep.daily_limit,
                "per_occurrence_limit": ep.per_occurrence_limit,
                "monthly_limit": ep.monthly_limit,
                "requires_invoice": ep.requires_invoice,
                "requires_pre_approval": ep.requires_pre_approval,
                "policy_status": ep.policy_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def check_expense_against_policy(
        self,
        expense_category: str,
        amount: float,
        city_tier: str,
        position_level: int,
        worker_type: str,
    ) -> str:
        """检查报销金额是否符合适用政策。

        参数:
            expense_category: Expense category to check.
            amount: Expense amount to check.
            city_tier: City tier for the expense.
            position_level: Position level of the employee.
            worker_type: Worker type of the employee.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid.
        """
        applicable_policies = []
        for ep in self.db.expense_policy.values():
            if ep.policy_status != "active":
                continue
            if ep.expense_category != expense_category:
                continue
            if ep.city_tier != city_tier:
                continue
            if position_level not in ep.applicable_position_levels:
                continue
            if worker_type not in ep.applicable_worker_types:
                continue
            applicable_policies.append(ep)

        if not applicable_policies:
            return json.dumps({
                "compliant": True,
                "message": "No applicable policy found for the given criteria",
                "applicable_policies": [],
            })

        violations = []
        for ep in applicable_policies:
            if ep.per_occurrence_limit is not None and amount > ep.per_occurrence_limit:
                violations.append({
                    "policy_ref": ep.expense_policy_ref,
                    "policy_name": ep.policy_name,
                    "limit_type": "per_occurrence",
                    "limit_amount": ep.per_occurrence_limit,
                    "exceeded_by": round(amount - ep.per_occurrence_limit, 2),
                })
            if ep.daily_limit is not None and amount > ep.daily_limit:
                violations.append({
                    "policy_ref": ep.expense_policy_ref,
                    "policy_name": ep.policy_name,
                    "limit_type": "daily",
                    "limit_amount": ep.daily_limit,
                    "exceeded_by": round(amount - ep.daily_limit, 2),
                })

        return json.dumps({
            "compliant": len(violations) == 0,
            "violations": violations,
            "applicable_policies": [
                {
                    "expense_policy_ref": ep.expense_policy_ref,
                    "policy_name": ep.policy_name,
                    "daily_limit": ep.daily_limit,
                    "per_occurrence_limit": ep.per_occurrence_limit,
                    "monthly_limit": ep.monthly_limit,
                    "requires_invoice": ep.requires_invoice,
                    "requires_pre_approval": ep.requires_pre_approval,
                }
                for ep in applicable_policies
            ],
        })

    # ===================================================================
    # 财务工单 — 财务服务台查询 / 财务热线查询
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_finance_ticket_details(self, finance_ticket_ref: str) -> str:
        """获取指定财务工单的详细信息。

        参数:
            finance_ticket_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ft = self._get_finance_ticket(finance_ticket_ref)
        return json.dumps({
            "finance_ticket_ref": ft.finance_ticket_ref,
            "ticket_number": ft.ticket_number,
            "requester_ref": ft.requester_ref,
            "ticket_category": ft.ticket_category,
            "ticket_subcategory": ft.ticket_subcategory,
            "subject": ft.subject,
            "description": ft.description,
            "priority": ft.priority,
            "ticket_status": ft.ticket_status,
            "assigned_to_ref": ft.assigned_to_ref,
            "related_resource_type": ft.related_resource_type,
            "related_resource_ref": ft.related_resource_ref,
            "resolution": ft.resolution,
            "resolved_at": ft.resolved_at,
            "created_at": ft.created_at,
            "updated_at": ft.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_finance_tickets(
        self,
        requester_ref: Optional[str] = None,
        ticket_category: Optional[str] = None,
        ticket_subcategory: Optional[str] = None,
        ticket_status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出财务工单。

        参数:
            requester_ref: Filter by requester employee ref. Defaults to None.
            ticket_category: Filter by ticket category. Defaults to None.
            ticket_subcategory: Filter by ticket subcategory. Defaults to None.
            ticket_status: Filter by ticket status. Defaults to None.
            priority: Filter by priority. Defaults to None.
            assigned_to_ref: Filter by assigned handler employee ref. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ft in self.db.finance_ticket.items():
            if requester_ref is not None and ft.requester_ref != requester_ref:
                continue
            if ticket_category is not None and ft.ticket_category != ticket_category:
                continue
            if ticket_subcategory is not None and ft.ticket_subcategory != ticket_subcategory:
                continue
            if ticket_status is not None and ft.ticket_status != ticket_status:
                continue
            if priority is not None and ft.priority != priority:
                continue
            if assigned_to_ref is not None and ft.assigned_to_ref != assigned_to_ref:
                continue
            results.append({
                "finance_ticket_ref": ft.finance_ticket_ref,
                "ticket_number": ft.ticket_number,
                "requester_ref": ft.requester_ref,
                "ticket_category": ft.ticket_category,
                "ticket_subcategory": ft.ticket_subcategory,
                "subject": ft.subject,
                "priority": ft.priority,
                "ticket_status": ft.ticket_status,
                "assigned_to_ref": ft.assigned_to_ref,
                "created_at": ft.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_finance_ticket(
        self,
        requester_ref: str,
        ticket_category: str,
        ticket_subcategory: str,
        subject: str,
        description: str,
        priority: str = "normal",
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
    ) -> str:
        """创建新的财务工单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            requester_ref: Employee ref of the requester.
            ticket_category: Category of the ticket (reimbursement, payment, invoice, budget, tax, loan, settlement, account, other).
            ticket_subcategory: Subcategory (policy_inquiry, status_inquiry, correction, dispute, system_issue, approval_escalation, other).
            subject: Subject line of the ticket.
            description: Detailed description of the issue.
            priority: Priority level (low, normal, high, critical). Defaults to "normal".
            related_resource_type: Type of related resource. Defaults to None.
            related_resource_ref: Ref of related resource. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(requester_ref)
        valid_categories = {"reimbursement", "payment", "invoice", "budget", "tax", "loan", "settlement", "account", "other"}
        if ticket_category not in valid_categories:
            raise ValueError(f"Invalid ticket_category: {ticket_category}. Must be one of {valid_categories}")
        valid_subcategories = {"policy_inquiry", "status_inquiry", "correction", "dispute", "system_issue", "approval_escalation", "other"}
        if ticket_subcategory not in valid_subcategories:
            raise ValueError(f"Invalid ticket_subcategory: {ticket_subcategory}. Must be one of {valid_subcategories}")
        valid_priorities = {"low", "normal", "high", "critical"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        now = self._now_iso()
        ref = self._generate_ref("FTK", self.db.finance_ticket)
        idx = len(self.db.finance_ticket) + 1
        ticket_number = f"FT-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        ft = FinanceTicket(
            finance_ticket_ref=ref,
            ticket_number=ticket_number,
            requester_ref=requester_ref,
            ticket_category=ticket_category,
            ticket_subcategory=ticket_subcategory,
            subject=subject,
            description=description,
            priority=priority,
            ticket_status="open",
            assigned_to_ref=None,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            resolution=None,
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.finance_ticket[ref] = ft
        return json.dumps({
            "finance_ticket_ref": ref,
            "ticket_number": ticket_number,
            "ticket_status": "open",
        })

    @is_tool(ToolType.WRITE)
    def update_finance_ticket_status(
        self,
        finance_ticket_ref: str,
        new_status: str,
        resolution: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
    ) -> str:
        """更新财务工单状态。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            finance_ticket_ref: 唯一标识。
            new_status: New ticket status (open, in_progress, pending_info, resolved, closed, cancelled).
            resolution: Resolution description (required when resolving). Defaults to None.
            assigned_to_ref: Employee ref to assign the ticket to. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the ticket is not found or the status transition is invalid.
        """
        ft = self._get_finance_ticket(finance_ticket_ref)
        valid_statuses = {"open", "in_progress", "pending_info", "resolved", "closed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid ticket_status: {new_status}. Must be one of {valid_statuses}")
        if ft.ticket_status in ("closed", "cancelled"):
            raise ValueError(f"Cannot update ticket from status '{ft.ticket_status}'")
        if new_status == "resolved" and resolution is None:
            raise ValueError("Resolution is required when resolving a ticket")

        now = self._now_iso()
        ft.ticket_status = new_status
        if resolution is not None:
            ft.resolution = resolution
        if new_status == "resolved":
            ft.resolved_at = now
        if assigned_to_ref is not None:
            self._get_employee(assigned_to_ref)
            ft.assigned_to_ref = assigned_to_ref
        ft.updated_at = now
        return json.dumps({
            "finance_ticket_ref": ft.finance_ticket_ref,
            "ticket_status": ft.ticket_status,
            "assigned_to_ref": ft.assigned_to_ref,
        })

    # ===================================================================
    # 信贷申请 — 金融信贷服务
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_credit_application_details(self, credit_application_ref: str) -> str:
        """获取指定信贷申请的详细信息。

        参数:
            credit_application_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        ca = self._get_credit_application(credit_application_ref)
        return json.dumps({
            "credit_application_ref": ca.credit_application_ref,
            "application_number": ca.application_number,
            "applicant_ref": ca.applicant_ref,
            "product_type": ca.product_type,
            "currency": ca.currency,
            "requested_amount": ca.requested_amount,
            "approved_amount": ca.approved_amount,
            "interest_rate": ca.interest_rate,
            "loan_term_months": ca.loan_term_months,
            "repayment_method": ca.repayment_method,
            "purpose": ca.purpose,
            "credit_score": ca.credit_score,
            "risk_level": ca.risk_level,
            "application_status": ca.application_status,
            "reviewed_by_ref": ca.reviewed_by_ref,
            "approved_at": ca.approved_at,
            "disbursed_at": ca.disbursed_at,
            "maturity_date": ca.maturity_date,
            "outstanding_balance": ca.outstanding_balance,
            "next_payment_date": ca.next_payment_date,
            "next_payment_amount": ca.next_payment_amount,
            "notes": ca.notes,
            "created_at": ca.created_at,
            "updated_at": ca.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_credit_applications(
        self,
        applicant_ref: Optional[str] = None,
        product_type: Optional[str] = None,
        application_status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出信贷申请。

        参数:
            applicant_ref: Filter by applicant employee ref. Defaults to None.
            product_type: Filter by product type. Defaults to None.
            application_status: Filter by application status. Defaults to None.
            risk_level: Filter by risk level. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, ca in self.db.credit_application.items():
            if applicant_ref is not None and ca.applicant_ref != applicant_ref:
                continue
            if product_type is not None and ca.product_type != product_type:
                continue
            if application_status is not None and ca.application_status != application_status:
                continue
            if risk_level is not None and ca.risk_level != risk_level:
                continue
            results.append({
                "credit_application_ref": ca.credit_application_ref,
                "application_number": ca.application_number,
                "applicant_ref": ca.applicant_ref,
                "product_type": ca.product_type,
                "currency": ca.currency,
                "requested_amount": ca.requested_amount,
                "approved_amount": ca.approved_amount,
                "application_status": ca.application_status,
                "risk_level": ca.risk_level,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_credit_application(
        self,
        applicant_ref: str,
        product_type: str,
        currency: str,
        requested_amount: float,
        loan_term_months: int,
        repayment_method: str,
        purpose: str,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态信贷申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            applicant_ref: Employee ref of the applicant.
            product_type: Type of credit product (personal_loan, housing_loan, education_loan, emergency_loan, other).
            currency: Currency code.
            requested_amount: Amount requested.
            loan_term_months: Loan term in months.
            repayment_method: Repayment method (equal_installment, equal_principal, bullet, custom).
            purpose: Purpose of the credit application.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(applicant_ref)
        if requested_amount <= 0:
            raise ValueError("requested_amount must be positive")
        if loan_term_months <= 0:
            raise ValueError("loan_term_months must be positive")
        valid_product_types = {"personal_loan", "housing_loan", "education_loan", "emergency_loan", "other"}
        if product_type not in valid_product_types:
            raise ValueError(f"Invalid product_type: {product_type}. Must be one of {valid_product_types}")
        valid_repayment_methods = {"equal_installment", "equal_principal", "bullet", "custom"}
        if repayment_method not in valid_repayment_methods:
            raise ValueError(f"Invalid repayment_method: {repayment_method}. Must be one of {valid_repayment_methods}")

        now = self._now_iso()
        ref = self._generate_ref("CA", self.db.credit_application)
        idx = len(self.db.credit_application) + 1
        application_number = f"CA-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        ca = CreditApplication(
            credit_application_ref=ref,
            application_number=application_number,
            applicant_ref=applicant_ref,
            product_type=product_type,
            currency=currency,
            requested_amount=requested_amount,
            approved_amount=None,
            interest_rate=None,
            loan_term_months=loan_term_months,
            repayment_method=repayment_method,
            purpose=purpose,
            credit_score=None,
            risk_level=None,
            application_status="draft",
            reviewed_by_ref=None,
            approved_at=None,
            disbursed_at=None,
            maturity_date=None,
            outstanding_balance=None,
            next_payment_date=None,
            next_payment_amount=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.credit_application[ref] = ca
        return json.dumps({
            "credit_application_ref": ref,
            "application_number": application_number,
            "application_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_credit_application(self, credit_application_ref: str) -> str:
        """提交草稿信贷申请进入审核。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            credit_application_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the application is not found or not in draft status.
        """
        ca = self._get_credit_application(credit_application_ref)
        if ca.application_status != "draft":
            raise ValueError(f"Credit application cannot be submitted from status '{ca.application_status}'.")
        ca.application_status = "submitted"
        ca.updated_at = self._now_iso()
        return json.dumps({
            "credit_application_ref": ca.credit_application_ref,
            "application_status": ca.application_status,
        })

    @is_tool(ToolType.WRITE)
    def approve_credit_application(
        self,
        credit_application_ref: str,
        reviewer_ref: str,
        approved_amount: float,
        interest_rate: float,
        risk_level: str,
        credit_score: Optional[int] = None,
    ) -> str:
        """审核后审批通过信贷申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            credit_application_ref: 唯一标识。
            reviewer_ref: Employee ref of the reviewer.
            approved_amount: Approved loan amount.
            interest_rate: Annual interest rate.
            risk_level: Risk level assessment (low, medium, high, very_high).
            credit_score: Applicant's credit score. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the application is not found or not in a valid status.
        """
        ca = self._get_credit_application(credit_application_ref)
        self._get_employee(reviewer_ref)
        if ca.application_status not in ("submitted", "under_review"):
            raise ValueError(f"Credit application cannot be approved from status '{ca.application_status}'.")
        valid_risk_levels = {"low", "medium", "high", "very_high"}
        if risk_level not in valid_risk_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_risk_levels}")

        now = self._now_iso()
        ca.application_status = "approved"
        ca.approved_amount = approved_amount
        ca.interest_rate = interest_rate
        ca.risk_level = risk_level
        ca.credit_score = credit_score
        ca.reviewed_by_ref = reviewer_ref
        ca.approved_at = now
        ca.updated_at = now
        return json.dumps({
            "credit_application_ref": ca.credit_application_ref,
            "application_status": ca.application_status,
            "approved_amount": approved_amount,
        })

    @is_tool(ToolType.WRITE)
    def reject_credit_application(
        self,
        credit_application_ref: str,
        reviewer_ref: str,
        reason: str,
        risk_level: Optional[str] = None,
    ) -> str:
        """驳回信贷申请。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            credit_application_ref: 唯一标识。
            reviewer_ref: Employee ref of the reviewer.
            reason: Reason for rejection.
            risk_level: Risk level assessment. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the application is not found or not in a valid status.
        """
        ca = self._get_credit_application(credit_application_ref)
        self._get_employee(reviewer_ref)
        if ca.application_status not in ("submitted", "under_review"):
            raise ValueError(f"Credit application cannot be rejected from status '{ca.application_status}'.")
        now = self._now_iso()
        ca.application_status = "rejected"
        ca.reviewed_by_ref = reviewer_ref
        if risk_level is not None:
            ca.risk_level = risk_level
        ca.notes = f"{ca.notes}\nRejection reason: {reason}" if ca.notes else f"Rejection reason: {reason}"
        ca.updated_at = now
        return json.dumps({
            "credit_application_ref": ca.credit_application_ref,
            "application_status": ca.application_status,
        })

    # ===================================================================
    # 信贷还款计划 — 信贷还款计划
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_credit_repayment_schedules(
        self,
        credit_application_ref: str,
        schedule_status: Optional[str] = None,
    ) -> str:
        """列出指定信贷申请下的还款计划。

        参数:
            credit_application_ref: 唯一标识。
            schedule_status: Filter by schedule status (pending, paid, overdue, partial_paid, waived). Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_credit_application(credit_application_ref)
        results = []
        for crs in self.db.credit_repayment_schedule.values():
            if crs.credit_application_ref != credit_application_ref:
                continue
            if schedule_status is not None and crs.schedule_status != schedule_status:
                continue
            results.append({
                "credit_repayment_schedule_ref": crs.credit_repayment_schedule_ref,
                "credit_application_ref": crs.credit_application_ref,
                "installment_number": crs.installment_number,
                "due_date": crs.due_date,
                "principal_amount": crs.principal_amount,
                "interest_amount": crs.interest_amount,
                "total_amount": crs.total_amount,
                "paid_amount": crs.paid_amount,
                "paid_at": crs.paid_at,
                "schedule_status": crs.schedule_status,
            })
        # 按分期序号排序
        results.sort(key=lambda x: x["installment_number"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_credit_repayment_schedule_details(self, credit_repayment_schedule_ref: str) -> str:
        """获取指定信贷还款计划条目的详细信息。

        参数:
            credit_repayment_schedule_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        crs = self._get_credit_repayment_schedule(credit_repayment_schedule_ref)
        return json.dumps({
            "credit_repayment_schedule_ref": crs.credit_repayment_schedule_ref,
            "credit_application_ref": crs.credit_application_ref,
            "installment_number": crs.installment_number,
            "due_date": crs.due_date,
            "principal_amount": crs.principal_amount,
            "interest_amount": crs.interest_amount,
            "total_amount": crs.total_amount,
            "paid_amount": crs.paid_amount,
            "paid_at": crs.paid_at,
            "schedule_status": crs.schedule_status,
            "created_at": crs.created_at,
        })

    @is_tool(ToolType.WRITE)
    def make_credit_repayment(
        self,
        credit_repayment_schedule_ref: str,
        payment_amount: float,
    ) -> str:
        """登记信贷还款计划条目的实付记录。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            credit_repayment_schedule_ref: 唯一标识。
            payment_amount: Amount being paid.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the schedule entry is not found, already paid, or amount is invalid.
        """
        crs = self._get_credit_repayment_schedule(credit_repayment_schedule_ref)
        if crs.schedule_status in ("paid", "waived"):
            raise ValueError(f"Repayment schedule is already {crs.schedule_status}")
        if payment_amount <= 0:
            raise ValueError("payment_amount must be positive")

        now = self._now_iso()
        crs.paid_amount = round(crs.paid_amount + payment_amount, 2)
        if crs.paid_amount >= crs.total_amount:
            crs.schedule_status = "paid"
            crs.paid_at = now
        else:
            crs.schedule_status = "partial_paid"

        # 更新信贷申请的未偿还余额
        ca = self._get_credit_application(crs.credit_application_ref)
        if ca.outstanding_balance is not None:
            ca.outstanding_balance = round(ca.outstanding_balance - payment_amount, 2)
            ca.updated_at = now

        return json.dumps({
            "credit_repayment_schedule_ref": crs.credit_repayment_schedule_ref,
            "paid_amount": crs.paid_amount,
            "total_amount": crs.total_amount,
            "schedule_status": crs.schedule_status,
        })

    # ===================================================================
    # 股票交易订单 — 中银国际股票交易
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_stock_trade_order_details(self, stock_trade_order_ref: str) -> str:
        """获取指定股票交易订单的详细信息。

        参数:
            stock_trade_order_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        sto = self._get_stock_trade_order(stock_trade_order_ref)
        return json.dumps({
            "stock_trade_order_ref": sto.stock_trade_order_ref,
            "order_number": sto.order_number,
            "employee_ref": sto.employee_ref,
            "brokerage": sto.brokerage,
            "stock_code": sto.stock_code,
            "stock_name": sto.stock_name,
            "market": sto.market,
            "trade_direction": sto.trade_direction,
            "order_type": sto.order_type,
            "currency": sto.currency,
            "quantity": sto.quantity,
            "price": sto.price,
            "filled_quantity": sto.filled_quantity,
            "filled_avg_price": sto.filled_avg_price,
            "total_amount": sto.total_amount,
            "commission": sto.commission,
            "stamp_duty": sto.stamp_duty,
            "order_status": sto.order_status,
            "submitted_at": sto.submitted_at,
            "filled_at": sto.filled_at,
            "cancelled_at": sto.cancelled_at,
            "notes": sto.notes,
            "created_at": sto.created_at,
            "updated_at": sto.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_stock_trade_orders(
        self,
        employee_ref: Optional[str] = None,
        stock_code: Optional[str] = None,
        trade_direction: Optional[str] = None,
        order_status: Optional[str] = None,
        brokerage: Optional[str] = None,
        market: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出股票交易订单。

        参数:
            employee_ref: Filter by employee ref. Defaults to None.
            stock_code: Filter by stock code. Defaults to None.
            trade_direction: Filter by trade direction (buy, sell). Defaults to None.
            order_status: Filter by order status. Defaults to None.
            brokerage: Filter by brokerage. Defaults to None.
            market: Filter by market. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, sto in self.db.stock_trade_order.items():
            if employee_ref is not None and sto.employee_ref != employee_ref:
                continue
            if stock_code is not None and sto.stock_code != stock_code:
                continue
            if trade_direction is not None and sto.trade_direction != trade_direction:
                continue
            if order_status is not None and sto.order_status != order_status:
                continue
            if brokerage is not None and sto.brokerage != brokerage:
                continue
            if market is not None and sto.market != market:
                continue
            results.append({
                "stock_trade_order_ref": sto.stock_trade_order_ref,
                "order_number": sto.order_number,
                "employee_ref": sto.employee_ref,
                "stock_code": sto.stock_code,
                "stock_name": sto.stock_name,
                "market": sto.market,
                "trade_direction": sto.trade_direction,
                "order_type": sto.order_type,
                "currency": sto.currency,
                "quantity": sto.quantity,
                "price": sto.price,
                "filled_quantity": sto.filled_quantity,
                "order_status": sto.order_status,
                "total_amount": sto.total_amount,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_stock_trade_order(
        self,
        employee_ref: str,
        brokerage: str,
        stock_code: str,
        stock_name: str,
        market: str,
        trade_direction: str,
        order_type: str,
        currency: str,
        quantity: int,
        price: float,
        notes: str = "",
    ) -> str:
        """创建新的草稿状态股票交易订单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            employee_ref: Employee ref of the trader.
            brokerage: Brokerage firm (boci, cicc, citic, huatai, guotai, other).
            stock_code: Stock ticker code (e.g., 00700.HK).
            stock_name: Name of the stock.
            market: Stock market (SSE, SZSE, HKEX, NYSE, NASDAQ, other).
            trade_direction: Trade direction (buy, sell).
            order_type: Order type (limit, market, stop, stop_limit).
            currency: Currency code.
            quantity: Number of shares.
            price: Order price per share.
            notes: Additional notes. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果inputs are invalid or referenced entities are not found.
        """
        self._get_employee(employee_ref)
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if price < 0:
            raise ValueError("price cannot be negative")
        valid_brokerages = {"boci", "cicc", "citic", "huatai", "guotai", "other"}
        if brokerage not in valid_brokerages:
            raise ValueError(f"Invalid brokerage: {brokerage}. Must be one of {valid_brokerages}")
        valid_markets = {"SSE", "SZSE", "HKEX", "NYSE", "NASDAQ", "other"}
        if market not in valid_markets:
            raise ValueError(f"Invalid market: {market}. Must be one of {valid_markets}")
        valid_directions = {"buy", "sell"}
        if trade_direction not in valid_directions:
            raise ValueError(f"Invalid trade_direction: {trade_direction}. Must be one of {valid_directions}")
        valid_order_types = {"limit", "market", "stop", "stop_limit"}
        if order_type not in valid_order_types:
            raise ValueError(f"Invalid order_type: {order_type}. Must be one of {valid_order_types}")

        now = self._now_iso()
        ref = self._generate_ref("STO", self.db.stock_trade_order)
        idx = len(self.db.stock_trade_order) + 1
        order_number = f"SO-{datetime.now(timezone.utc).strftime('%Y')}-{idx:06d}"

        sto = StockTradeOrder(
            stock_trade_order_ref=ref,
            order_number=order_number,
            employee_ref=employee_ref,
            brokerage=brokerage,
            stock_code=stock_code,
            stock_name=stock_name,
            market=market,
            trade_direction=trade_direction,
            order_type=order_type,
            currency=currency,
            quantity=quantity,
            price=price,
            filled_quantity=0,
            filled_avg_price=0.0,
            total_amount=0.0,
            commission=0.0,
            stamp_duty=0.0,
            order_status="draft",
            submitted_at=None,
            filled_at=None,
            cancelled_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.stock_trade_order[ref] = sto
        return json.dumps({
            "stock_trade_order_ref": ref,
            "order_number": order_number,
            "order_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_stock_trade_order(self, stock_trade_order_ref: str) -> str:
        """提交草稿股票交易订单进入执行。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            stock_trade_order_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the order is not found or not in draft status.
        """
        sto = self._get_stock_trade_order(stock_trade_order_ref)
        if sto.order_status != "draft":
            raise ValueError(f"Stock trade order cannot be submitted from status '{sto.order_status}'.")
        now = self._now_iso()
        sto.order_status = "submitted"
        sto.submitted_at = now
        sto.updated_at = now
        return json.dumps({
            "stock_trade_order_ref": sto.stock_trade_order_ref,
            "order_status": sto.order_status,
        })

    @is_tool(ToolType.WRITE)
    def cancel_stock_trade_order(self, stock_trade_order_ref: str) -> str:
        """取消处于草稿或已提交状态的股票交易订单。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            stock_trade_order_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the order is not found or not in a cancellable status.
        """
        sto = self._get_stock_trade_order(stock_trade_order_ref)
        if sto.order_status not in ("draft", "submitted", "partial_filled"):
            raise ValueError(f"Stock trade order cannot be cancelled from status '{sto.order_status}'.")
        now = self._now_iso()
        sto.order_status = "cancelled"
        sto.cancelled_at = now
        sto.updated_at = now
        return json.dumps({
            "stock_trade_order_ref": sto.stock_trade_order_ref,
            "order_status": sto.order_status,
        })

    # ===================================================================
    # 财务审批流 — 财务审批流程
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_finance_approval_flow_details(self, finance_approval_flow_ref: str) -> str:
        """获取指定财务审批流步骤的详细信息。

        参数:
            finance_approval_flow_ref: 唯一标识。

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        faf = self._get_finance_approval_flow(finance_approval_flow_ref)
        return json.dumps({
            "finance_approval_flow_ref": faf.finance_approval_flow_ref,
            "source_type": faf.source_type,
            "source_ref": faf.source_ref,
            "step_order": faf.step_order,
            "approver_ref": faf.approver_ref,
            "approver_role": faf.approver_role,
            "approval_action": faf.approval_action,
            "comments": faf.comments,
            "acted_at": faf.acted_at,
            "created_at": faf.created_at,
            "updated_at": faf.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_finance_approval_flows(
        self,
        source_type: Optional[str] = None,
        source_ref: Optional[str] = None,
        approver_ref: Optional[str] = None,
        approval_action: Optional[str] = None,
    ) -> str:
        """按可选过滤条件列出财务审批流步骤。

        参数:
            source_type: Filter by source document type. Defaults to None.
            source_ref: Filter by source document ref. Defaults to None.
            approver_ref: Filter by approver employee ref. Defaults to None.
            approval_action: Filter by approval action. Defaults to None.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果any referenced entity 未找到。
        """
        results = []
        for ref, faf in self.db.finance_approval_flow.items():
            if source_type is not None and faf.source_type != source_type:
                continue
            if source_ref is not None and faf.source_ref != source_ref:
                continue
            if approver_ref is not None and faf.approver_ref != approver_ref:
                continue
            if approval_action is not None and faf.approval_action != approval_action:
                continue
            results.append({
                "finance_approval_flow_ref": faf.finance_approval_flow_ref,
                "source_type": faf.source_type,
                "source_ref": faf.source_ref,
                "step_order": faf.step_order,
                "approver_ref": faf.approver_ref,
                "approver_role": faf.approver_role,
                "approval_action": faf.approval_action,
                "acted_at": faf.acted_at,
            })
        # 按来源引用与审批步骤顺序排序
        results.sort(key=lambda x: (x["source_ref"], x["step_order"]))
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_pending_approvals_for_employee(self, approver_ref: str) -> str:
        """列出指定员工在全部财务单据上的待审批步骤。

        参数:
            approver_ref: Employee ref of the approver.

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果未找到对应记录。
        """
        self._get_employee(approver_ref)
        results = []
        for faf in self.db.finance_approval_flow.values():
            if faf.approver_ref == approver_ref and faf.approval_action == "pending":
                results.append({
                    "finance_approval_flow_ref": faf.finance_approval_flow_ref,
                    "source_type": faf.source_type,
                    "source_ref": faf.source_ref,
                    "step_order": faf.step_order,
                    "approver_role": faf.approver_role,
                    "created_at": faf.created_at,
                })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def act_on_finance_approval(
        self,
        finance_approval_flow_ref: str,
        action: str,
        comments: str = "",
    ) -> str:
        """对待处理的财务审批流步骤执行审批动作。

        调用该工具前，智能体必须先征得用户明确确认。

        参数:
            finance_approval_flow_ref: 唯一标识。
            action: Action to take (approved, rejected, returned, delegated, skipped).
            comments: Comments or remarks from the approver. Defaults to "".

        返回:
            str: JSON 字符串。

        异常:
            ValueError: 如果the approval step is not found, not pending, or action is invalid.
        """
        faf = self._get_finance_approval_flow(finance_approval_flow_ref)
        if faf.approval_action != "pending":
            raise ValueError(f"Approval step is not pending. Current action: '{faf.approval_action}'")
        valid_actions = {"approved", "rejected", "returned", "delegated", "skipped"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}")

        now = self._now_iso()
        faf.approval_action = action
        faf.comments = comments
        faf.acted_at = now
        faf.updated_at = now
        return json.dumps({
            "finance_approval_flow_ref": faf.finance_approval_flow_ref,
            "source_type": faf.source_type,
            "source_ref": faf.source_ref,
            "approval_action": faf.approval_action,
            "acted_at": faf.acted_at,
        })