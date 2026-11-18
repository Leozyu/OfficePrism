"""Toolkit for the purchase/procurement domain, extending OfficeTools."""
from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.purchase.models import (
    AcceptanceItem,
    AcceptanceRecord,
    ApprovalAction,
    ApprovalFlowNode,
    ApprovalFlowTemplate,
    ApprovalInstance,
    ContractItem,
    GoodsReceipt,
    GoodsReceiptItem,
    ProcurementCategory,
    ProcurementIssueTicket,
    ProcurementPermissionRule,
    ProcurementTrainingCourse,
    ProcurementTrainingRecord,
    PurchaseChangeRequest,
    PurchaseContract,
    PurchaseDB,
    PurchaseOrder,
    PurchaseOrderItem,
    PurchaseRequisition,
    Quotation,
    QuotationItem,
    RequisitionItem,
    SourcingProject,
    SourcingSupplier,
    Supplier,
    SupplierCategory,
    SupplierContact,
    SupplierEvaluation,
    SupplierQualification,
)


class PurchaseTools(OfficeTools):
    """Toolkit for the purchase/procurement domain, extending OfficeTools with procurement operations."""

    db: PurchaseDB

    def __init__(self, db: PurchaseDB) -> None:
        """
        Initialize PurchaseTools with a PurchaseDB instance.

        Args:
            db: The purchase database instance.

        Returns:
            None
        """
        super().__init__(db)

    # -----------------------
    # Internal helper methods
    # -----------------------

    def _get_procurement_category(self, procurement_category_ref: str) -> ProcurementCategory:
        """
        Retrieve a procurement category by ref.

        Args:
            procurement_category_ref: The unique identifier of the procurement category.

        Returns:
            ProcurementCategory: The procurement category object.

        Raises:
            ValueError: If the procurement category is not found.
        """
        if procurement_category_ref not in self.db.procurement_category:
            raise ValueError("Procurement category not found")
        return self.db.procurement_category[procurement_category_ref]

    def _get_supplier(self, supplier_ref: str) -> Supplier:
        """
        Retrieve a supplier by ref.

        Args:
            supplier_ref: The unique identifier of the supplier.

        Returns:
            Supplier: The supplier object.

        Raises:
            ValueError: If the supplier is not found.
        """
        if supplier_ref not in self.db.supplier:
            raise ValueError("Supplier not found")
        return self.db.supplier[supplier_ref]

    def _get_supplier_contact(self, supplier_contact_ref: str) -> SupplierContact:
        """
        Retrieve a supplier contact by ref.

        Args:
            supplier_contact_ref: The unique identifier of the supplier contact.

        Returns:
            SupplierContact: The supplier contact object.

        Raises:
            ValueError: If the supplier contact is not found.
        """
        if supplier_contact_ref not in self.db.supplier_contact:
            raise ValueError("Supplier contact not found")
        return self.db.supplier_contact[supplier_contact_ref]

    def _get_supplier_qualification(self, supplier_qualification_ref: str) -> SupplierQualification:
        """
        Retrieve a supplier qualification by ref.

        Args:
            supplier_qualification_ref: The unique identifier of the supplier qualification.

        Returns:
            SupplierQualification: The supplier qualification object.

        Raises:
            ValueError: If the supplier qualification is not found.
        """
        if supplier_qualification_ref not in self.db.supplier_qualification:
            raise ValueError("Supplier qualification not found")
        return self.db.supplier_qualification[supplier_qualification_ref]

    def _get_supplier_evaluation(self, supplier_evaluation_ref: str) -> SupplierEvaluation:
        """
        Retrieve a supplier evaluation by ref.

        Args:
            supplier_evaluation_ref: The unique identifier of the supplier evaluation.

        Returns:
            SupplierEvaluation: The supplier evaluation object.

        Raises:
            ValueError: If the supplier evaluation is not found.
        """
        if supplier_evaluation_ref not in self.db.supplier_evaluation:
            raise ValueError("Supplier evaluation not found")
        return self.db.supplier_evaluation[supplier_evaluation_ref]

    def _get_sourcing_project(self, sourcing_project_ref: str) -> SourcingProject:
        """
        Retrieve a sourcing project by ref.

        Args:
            sourcing_project_ref: The unique identifier of the sourcing project.

        Returns:
            SourcingProject: The sourcing project object.

        Raises:
            ValueError: If the sourcing project is not found.
        """
        if sourcing_project_ref not in self.db.sourcing_project:
            raise ValueError("Sourcing project not found")
        return self.db.sourcing_project[sourcing_project_ref]

    def _get_sourcing_supplier(self, sourcing_supplier_ref: str) -> SourcingSupplier:
        """
        Retrieve a sourcing supplier record by ref.

        Args:
            sourcing_supplier_ref: The unique identifier of the sourcing supplier record.

        Returns:
            SourcingSupplier: The sourcing supplier object.

        Raises:
            ValueError: If the sourcing supplier record is not found.
        """
        if sourcing_supplier_ref not in self.db.sourcing_supplier:
            raise ValueError("Sourcing supplier not found")
        return self.db.sourcing_supplier[sourcing_supplier_ref]

    def _get_quotation(self, quotation_ref: str) -> Quotation:
        """
        Retrieve a quotation by ref.

        Args:
            quotation_ref: The unique identifier of the quotation.

        Returns:
            Quotation: The quotation object.

        Raises:
            ValueError: If the quotation is not found.
        """
        if quotation_ref not in self.db.quotation:
            raise ValueError("Quotation not found")
        return self.db.quotation[quotation_ref]

    def _get_purchase_requisition(self, purchase_requisition_ref: str) -> PurchaseRequisition:
        """
        Retrieve a purchase requisition by ref.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            PurchaseRequisition: The purchase requisition object.

        Raises:
            ValueError: If the purchase requisition is not found.
        """
        if purchase_requisition_ref not in self.db.purchase_requisition:
            raise ValueError("Purchase requisition not found")
        return self.db.purchase_requisition[purchase_requisition_ref]

    def _get_purchase_contract(self, purchase_contract_ref: str) -> PurchaseContract:
        """
        Retrieve a purchase contract by ref.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.

        Returns:
            PurchaseContract: The purchase contract object.

        Raises:
            ValueError: If the purchase contract is not found.
        """
        if purchase_contract_ref not in self.db.purchase_contract:
            raise ValueError("Purchase contract not found")
        return self.db.purchase_contract[purchase_contract_ref]

    def _get_purchase_order(self, purchase_order_ref: str) -> PurchaseOrder:
        """
        Retrieve a purchase order by ref.

        Args:
            purchase_order_ref: The unique identifier of the purchase order.

        Returns:
            PurchaseOrder: The purchase order object.

        Raises:
            ValueError: If the purchase order is not found.
        """
        if purchase_order_ref not in self.db.purchase_order:
            raise ValueError("Purchase order not found")
        return self.db.purchase_order[purchase_order_ref]

    def _get_purchase_change_request(self, purchase_change_request_ref: str) -> PurchaseChangeRequest:
        """
        Retrieve a purchase change request by ref.

        Args:
            purchase_change_request_ref: The unique identifier of the purchase change request.

        Returns:
            PurchaseChangeRequest: The purchase change request object.

        Raises:
            ValueError: If the purchase change request is not found.
        """
        if purchase_change_request_ref not in self.db.purchase_change_request:
            raise ValueError("Purchase change request not found")
        return self.db.purchase_change_request[purchase_change_request_ref]

    def _get_goods_receipt(self, goods_receipt_ref: str) -> GoodsReceipt:
        """
        Retrieve a goods receipt by ref.

        Args:
            goods_receipt_ref: The unique identifier of the goods receipt.

        Returns:
            GoodsReceipt: The goods receipt object.

        Raises:
            ValueError: If the goods receipt is not found.
        """
        if goods_receipt_ref not in self.db.goods_receipt:
            raise ValueError("Goods receipt not found")
        return self.db.goods_receipt[goods_receipt_ref]

    def _get_acceptance_record(self, acceptance_record_ref: str) -> AcceptanceRecord:
        """
        Retrieve an acceptance record by ref.

        Args:
            acceptance_record_ref: The unique identifier of the acceptance record.

        Returns:
            AcceptanceRecord: The acceptance record object.

        Raises:
            ValueError: If the acceptance record is not found.
        """
        if acceptance_record_ref not in self.db.acceptance_record:
            raise ValueError("Acceptance record not found")
        return self.db.acceptance_record[acceptance_record_ref]

    def _get_approval_flow_template(self, approval_flow_template_ref: str) -> ApprovalFlowTemplate:
        """
        Retrieve an approval flow template by ref.

        Args:
            approval_flow_template_ref: The unique identifier of the approval flow template.

        Returns:
            ApprovalFlowTemplate: The approval flow template object.

        Raises:
            ValueError: If the approval flow template is not found.
        """
        if approval_flow_template_ref not in self.db.approval_flow_template:
            raise ValueError("Approval flow template not found")
        return self.db.approval_flow_template[approval_flow_template_ref]

    def _get_approval_instance(self, approval_instance_ref: str) -> ApprovalInstance:
        """
        Retrieve an approval instance by ref.

        Args:
            approval_instance_ref: The unique identifier of the approval instance.

        Returns:
            ApprovalInstance: The approval instance object.

        Raises:
            ValueError: If the approval instance is not found.
        """
        if approval_instance_ref not in self.db.approval_instance:
            raise ValueError("Approval instance not found")
        return self.db.approval_instance[approval_instance_ref]

    def _get_procurement_permission_rule(self, procurement_permission_rule_ref: str) -> ProcurementPermissionRule:
        """
        Retrieve a procurement permission rule by ref.

        Args:
            procurement_permission_rule_ref: The unique identifier of the procurement permission rule.

        Returns:
            ProcurementPermissionRule: The procurement permission rule object.

        Raises:
            ValueError: If the procurement permission rule is not found.
        """
        if procurement_permission_rule_ref not in self.db.procurement_permission_rule:
            raise ValueError("Procurement permission rule not found")
        return self.db.procurement_permission_rule[procurement_permission_rule_ref]

    def _get_procurement_training_course(self, procurement_training_course_ref: str) -> ProcurementTrainingCourse:
        """
        Retrieve a procurement training course by ref.

        Args:
            procurement_training_course_ref: The unique identifier of the procurement training course.

        Returns:
            ProcurementTrainingCourse: The procurement training course object.

        Raises:
            ValueError: If the procurement training course is not found.
        """
        if procurement_training_course_ref not in self.db.procurement_training_course:
            raise ValueError("Procurement training course not found")
        return self.db.procurement_training_course[procurement_training_course_ref]

    def _get_procurement_training_record(self, procurement_training_record_ref: str) -> ProcurementTrainingRecord:
        """
        Retrieve a procurement training record by ref.

        Args:
            procurement_training_record_ref: The unique identifier of the procurement training record.

        Returns:
            ProcurementTrainingRecord: The procurement training record object.

        Raises:
            ValueError: If the procurement training record is not found.
        """
        if procurement_training_record_ref not in self.db.procurement_training_record:
            raise ValueError("Procurement training record not found")
        return self.db.procurement_training_record[procurement_training_record_ref]

    def _get_procurement_issue_ticket(self, procurement_issue_ticket_ref: str) -> ProcurementIssueTicket:
        """
        Retrieve a procurement issue ticket by ref.

        Args:
            procurement_issue_ticket_ref: The unique identifier of the procurement issue ticket.

        Returns:
            ProcurementIssueTicket: The procurement issue ticket object.

        Raises:
            ValueError: If the procurement issue ticket is not found.
        """
        if procurement_issue_ticket_ref not in self.db.procurement_issue_ticket:
            raise ValueError("Procurement issue ticket not found")
        return self.db.procurement_issue_ticket[procurement_issue_ticket_ref]

    # =========================================================================
    # Procurement Category (采购类目选择)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_category_details(self, procurement_category_ref: str) -> str:
        """
        Get detailed information about a specific procurement category.

        Args:
            procurement_category_ref: The unique identifier of the procurement category.

        Returns:
            str: JSON string containing the procurement category details.

        Raises:
            ValueError: If the procurement category is not found.
        """
        cat = self._get_procurement_category(procurement_category_ref)
        return json.dumps({
            "procurement_category_ref": cat.procurement_category_ref,
            "category_name": cat.category_name,
            "category_code": cat.category_code,
            "parent_category_ref": cat.parent_category_ref,
            "category_level": cat.category_level,
            "category_status": cat.category_status,
            "description": cat.description,
            "display_order": cat.display_order,
            "created_at": cat.created_at,
            "updated_at": cat.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_procurement_categories(
        self,
        parent_category_ref: Optional[str] = None,
        category_status: Optional[str] = None,
        category_level: Optional[int] = None,
    ) -> str:
        """
        List procurement categories with optional filters.

        Args:
            parent_category_ref: Filter by parent category ref. None returns all.
            category_status: Filter by status (active, inactive). None returns all.
            category_level: Filter by category level. None returns all.

        Returns:
            str: JSON string containing a list of matching procurement categories.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, cat in self.db.procurement_category.items():
            if parent_category_ref is not None and cat.parent_category_ref != parent_category_ref:
                continue
            if category_status is not None and cat.category_status != category_status:
                continue
            if category_level is not None and cat.category_level != category_level:
                continue
            results.append({
                "procurement_category_ref": cat.procurement_category_ref,
                "category_name": cat.category_name,
                "category_code": cat.category_code,
                "parent_category_ref": cat.parent_category_ref,
                "category_level": cat.category_level,
                "category_status": cat.category_status,
                "description": cat.description,
                "display_order": cat.display_order,
            })
        results.sort(key=lambda x: x["display_order"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_procurement_category_ref_by_name(self, category_name: str) -> str:
        """
        Find a procurement category ref by name (case-insensitive partial match).

        Args:
            category_name: The name (or partial name) of the procurement category to search for.

        Returns:
            str: The procurement_category_ref of the first matching category.

        Raises:
            ValueError: If no matching procurement category is found.
        """
        search = category_name.lower()
        for ref, cat in self.db.procurement_category.items():
            if search in cat.category_name.lower():
                return ref
        raise ValueError("Procurement category not found")

    @is_tool(ToolType.READ)
    def list_procurement_category_children(self, procurement_category_ref: str) -> str:
        """
        List all direct child categories of a given procurement category.

        Args:
            procurement_category_ref: The unique identifier of the parent procurement category.

        Returns:
            str: JSON string containing a list of child procurement categories.

        Raises:
            ValueError: If the parent procurement category is not found.
        """
        self._get_procurement_category(procurement_category_ref)
        results = []
        for ref, cat in self.db.procurement_category.items():
            if cat.parent_category_ref == procurement_category_ref:
                results.append({
                    "procurement_category_ref": cat.procurement_category_ref,
                    "category_name": cat.category_name,
                    "category_code": cat.category_code,
                    "category_level": cat.category_level,
                    "category_status": cat.category_status,
                    "description": cat.description,
                })
        results.sort(key=lambda x: x.get("procurement_category_ref", ""))
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_suppliers_for_category(self, procurement_category_ref: str, preferred_only: bool = False) -> str:
        """
        List all suppliers associated with a given procurement category.

        Args:
            procurement_category_ref: The unique identifier of the procurement category.
            preferred_only: If True, only return preferred suppliers for the category.

        Returns:
            str: JSON string containing a list of suppliers for the category.

        Raises:
            ValueError: If the procurement category is not found.
        """
        self._get_procurement_category(procurement_category_ref)
        results = []
        for sc in self.db.supplier_category.values():
            if sc.procurement_category_ref != procurement_category_ref:
                continue
            if sc.status != "active":
                continue
            if preferred_only and not sc.is_preferred:
                continue
            if sc.supplier_ref in self.db.supplier:
                sup = self.db.supplier[sc.supplier_ref]
                results.append({
                    "supplier_ref": sup.supplier_ref,
                    "supplier_name": sup.supplier_name,
                    "supplier_code": sup.supplier_code,
                    "supplier_type": sup.supplier_type,
                    "cooperation_status": sup.cooperation_status,
                    "risk_level": sup.risk_level,
                    "is_preferred": sc.is_preferred,
                })
        return json.dumps(results)

    # =========================================================================
    # Supplier Management (供应商入库 / 供应商信息管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_supplier_details(self, supplier_ref: str) -> str:
        """
        Get detailed information about a specific supplier.

        Args:
            supplier_ref: The unique identifier of the supplier.

        Returns:
            str: JSON string containing the supplier details.

        Raises:
            ValueError: If the supplier is not found.
        """
        sup = self._get_supplier(supplier_ref)
        return json.dumps({
            "supplier_ref": sup.supplier_ref,
            "supplier_name": sup.supplier_name,
            "supplier_code": sup.supplier_code,
            "supplier_type": sup.supplier_type,
            "unified_social_credit_code": sup.unified_social_credit_code,
            "legal_representative": sup.legal_representative,
            "registered_address": sup.registered_address,
            "business_address": sup.business_address,
            "country": sup.country,
            "bank_name": sup.bank_name,
            "bank_account": sup.bank_account,
            "tax_id": sup.tax_id,
            "cooperation_status": sup.cooperation_status,
            "risk_level": sup.risk_level,
            "onboarding_date": sup.onboarding_date,
            "blacklist_reason": sup.blacklist_reason,
            "notes": sup.notes,
            "registered_by_ref": sup.registered_by_ref,
            "approved_by_ref": sup.approved_by_ref,
            "created_at": sup.created_at,
            "updated_at": sup.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_suppliers(
        self,
        supplier_type: Optional[str] = None,
        cooperation_status: Optional[str] = None,
        risk_level: Optional[str] = None,
        country: Optional[str] = None,
    ) -> str:
        """
        List suppliers with optional filters.

        Args:
            supplier_type: Filter by supplier type (standard, strategic, occasional). None returns all.
            cooperation_status: Filter by cooperation status (pending, approved, suspended, blacklisted). None returns all.
            risk_level: Filter by risk level (low, medium, high, critical). None returns all.
            country: Filter by country code. None returns all.

        Returns:
            str: JSON string containing a list of matching suppliers.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, sup in self.db.supplier.items():
            if supplier_type is not None and sup.supplier_type != supplier_type:
                continue
            if cooperation_status is not None and sup.cooperation_status != cooperation_status:
                continue
            if risk_level is not None and sup.risk_level != risk_level:
                continue
            if country is not None and sup.country != country:
                continue
            results.append({
                "supplier_ref": sup.supplier_ref,
                "supplier_name": sup.supplier_name,
                "supplier_code": sup.supplier_code,
                "supplier_type": sup.supplier_type,
                "cooperation_status": sup.cooperation_status,
                "risk_level": sup.risk_level,
                "country": sup.country,
                "onboarding_date": sup.onboarding_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_supplier_ref_by_name(self, supplier_name: str) -> str:
        """
        Find a supplier ref by name (case-insensitive partial match).

        Args:
            supplier_name: The name (or partial name) of the supplier to search for.

        Returns:
            str: The supplier_ref of the first matching supplier.

        Raises:
            ValueError: If no matching supplier is found.
        """
        search = supplier_name.lower()
        for ref, sup in self.db.supplier.items():
            if search in sup.supplier_name.lower():
                return ref
        raise ValueError("Supplier not found")

    @is_tool(ToolType.READ)
    def search_suppliers(
        self,
        name: Optional[str] = None,
        supplier_type: Optional[str] = None,
        cooperation_status: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
    ) -> str:
        """
        Search suppliers with combined filters including category association.

        Args:
            name: Partial name match (case-insensitive). None skips this filter.
            supplier_type: Filter by supplier type. None returns all.
            cooperation_status: Filter by cooperation status. None returns all.
            procurement_category_ref: Filter by associated procurement category. None returns all.

        Returns:
            str: JSON string containing a list of matching suppliers.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        # If category filter, get supplier refs in that category
        category_supplier_refs = None
        if procurement_category_ref is not None:
            category_supplier_refs = set()
            for sc in self.db.supplier_category.values():
                if sc.procurement_category_ref == procurement_category_ref and sc.status == "active":
                    category_supplier_refs.add(sc.supplier_ref)

        results = []
        for ref, sup in self.db.supplier.items():
            if name is not None and name.lower() not in sup.supplier_name.lower():
                continue
            if supplier_type is not None and sup.supplier_type != supplier_type:
                continue
            if cooperation_status is not None and sup.cooperation_status != cooperation_status:
                continue
            if category_supplier_refs is not None and ref not in category_supplier_refs:
                continue
            results.append({
                "supplier_ref": sup.supplier_ref,
                "supplier_name": sup.supplier_name,
                "supplier_code": sup.supplier_code,
                "supplier_type": sup.supplier_type,
                "cooperation_status": sup.cooperation_status,
                "risk_level": sup.risk_level,
                "country": sup.country,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_supplier(
        self,
        supplier_name: str,
        supplier_code: str,
        supplier_type: str,
        unified_social_credit_code: str,
        legal_representative: str,
        registered_address: str,
        business_address: str,
        country: str,
        bank_name: str,
        bank_account: str,
        tax_id: str,
        registered_by_ref: str,
        notes: str = "",
    ) -> str:
        """
        Create a new supplier record (supplier onboarding). The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_name: Name of the supplier.
            supplier_code: Short code for the supplier.
            supplier_type: Type of supplier (standard, strategic, occasional).
            unified_social_credit_code: Business registration number.
            legal_representative: Name of the legal representative.
            registered_address: Registered address of the supplier.
            business_address: Business/operating address.
            country: Country code (e.g., CN, US).
            bank_name: Name of the supplier's bank.
            bank_account: Bank account number.
            tax_id: Tax identification number.
            registered_by_ref: Employee ref of the person registering the supplier.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created supplier details.

        Raises:
            ValueError: If required fields are invalid or the registering employee is not found.
        """
        valid_types = {"standard", "strategic", "occasional"}
        if supplier_type not in valid_types:
            raise ValueError(f"Invalid supplier_type: {supplier_type}. Must be one of {valid_types}")
        self._get_employee(registered_by_ref)

        # Check for duplicate supplier code
        for sup in self.db.supplier.values():
            if sup.supplier_code == supplier_code:
                raise ValueError(f"Supplier code '{supplier_code}' already exists")

        now = self._now_iso()
        ref = self._generate_ref("SUP", self.db.supplier)

        supplier = Supplier(
            supplier_ref=ref,
            supplier_name=supplier_name,
            supplier_code=supplier_code,
            supplier_type=supplier_type,
            unified_social_credit_code=unified_social_credit_code,
            legal_representative=legal_representative,
            registered_address=registered_address,
            business_address=business_address,
            country=country,
            bank_name=bank_name,
            bank_account=bank_account,
            tax_id=tax_id,
            cooperation_status="pending",
            risk_level="medium",
            onboarding_date=None,
            blacklist_reason=None,
            notes=notes,
            registered_by_ref=registered_by_ref,
            approved_by_ref=None,
            created_at=now,
            updated_at=now,
        )
        self.db.supplier[ref] = supplier
        return json.dumps({
            "supplier_ref": ref,
            "supplier_name": supplier_name,
            "supplier_code": supplier_code,
            "cooperation_status": "pending",
        })

    @is_tool(ToolType.WRITE)
    def update_supplier(
        self,
        supplier_ref: str,
        supplier_name: Optional[str] = None,
        supplier_type: Optional[str] = None,
        business_address: Optional[str] = None,
        bank_name: Optional[str] = None,
        bank_account: Optional[str] = None,
        risk_level: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """
        Update supplier information. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier to update.
            supplier_name: New supplier name. None to keep unchanged.
            supplier_type: New supplier type (standard, strategic, occasional). None to keep unchanged.
            business_address: New business address. None to keep unchanged.
            bank_name: New bank name. None to keep unchanged.
            bank_account: New bank account. None to keep unchanged.
            risk_level: New risk level (low, medium, high, critical). None to keep unchanged.
            notes: New notes. None to keep unchanged.

        Returns:
            str: JSON string containing the updated supplier details.

        Raises:
            ValueError: If the supplier is not found or invalid values are provided.
        """
        sup = self._get_supplier(supplier_ref)

        if supplier_type is not None:
            valid_types = {"standard", "strategic", "occasional"}
            if supplier_type not in valid_types:
                raise ValueError(f"Invalid supplier_type: {supplier_type}. Must be one of {valid_types}")
            sup.supplier_type = supplier_type

        if risk_level is not None:
            valid_levels = {"low", "medium", "high", "critical"}
            if risk_level not in valid_levels:
                raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_levels}")
            sup.risk_level = risk_level

        if supplier_name is not None:
            sup.supplier_name = supplier_name
        if business_address is not None:
            sup.business_address = business_address
        if bank_name is not None:
            sup.bank_name = bank_name
        if bank_account is not None:
            sup.bank_account = bank_account
        if notes is not None:
            sup.notes = notes

        sup.updated_at = self._now_iso()
        return json.dumps({
            "supplier_ref": sup.supplier_ref,
            "supplier_name": sup.supplier_name,
            "cooperation_status": sup.cooperation_status,
            "updated_at": sup.updated_at,
        })

    @is_tool(ToolType.WRITE)
    def approve_supplier(self, supplier_ref: str, approved_by_ref: str) -> str:
        """
        Approve a pending supplier for cooperation. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier to approve.
            approved_by_ref: Employee ref of the person approving the supplier.

        Returns:
            str: JSON string containing the updated supplier status.

        Raises:
            ValueError: If the supplier is not found, not in pending status, or the approver is not found.
        """
        sup = self._get_supplier(supplier_ref)
        self._get_employee(approved_by_ref)

        if sup.cooperation_status != "pending":
            raise ValueError(f"Supplier cooperation status is '{sup.cooperation_status}', expected 'pending'")

        now = self._now_iso()
        sup.cooperation_status = "approved"
        sup.approved_by_ref = approved_by_ref
        sup.onboarding_date = now[:10]
        sup.updated_at = now
        return json.dumps({
            "supplier_ref": sup.supplier_ref,
            "supplier_name": sup.supplier_name,
            "cooperation_status": sup.cooperation_status,
            "onboarding_date": sup.onboarding_date,
        })

    @is_tool(ToolType.WRITE)
    def suspend_supplier(self, supplier_ref: str, reason: str) -> str:
        """
        Suspend a supplier's cooperation status. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier to suspend.
            reason: Reason for suspending the supplier.

        Returns:
            str: JSON string containing the updated supplier status.

        Raises:
            ValueError: If the supplier is not found or not in approved status.
        """
        sup = self._get_supplier(supplier_ref)
        if sup.cooperation_status != "approved":
            raise ValueError(f"Supplier cooperation status is '{sup.cooperation_status}', can only suspend approved suppliers")

        sup.cooperation_status = "suspended"
        sup.notes = f"{sup.notes}\nSuspended: {reason}" if sup.notes else f"Suspended: {reason}"
        sup.updated_at = self._now_iso()
        return json.dumps({
            "supplier_ref": sup.supplier_ref,
            "supplier_name": sup.supplier_name,
            "cooperation_status": sup.cooperation_status,
        })

    @is_tool(ToolType.WRITE)
    def blacklist_supplier(self, supplier_ref: str, reason: str) -> str:
        """
        Blacklist a supplier. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier to blacklist.
            reason: Reason for blacklisting the supplier.

        Returns:
            str: JSON string containing the updated supplier status.

        Raises:
            ValueError: If the supplier is not found or already blacklisted.
        """
        sup = self._get_supplier(supplier_ref)
        if sup.cooperation_status == "blacklisted":
            raise ValueError("Supplier is already blacklisted")

        sup.cooperation_status = "blacklisted"
        sup.blacklist_reason = reason
        sup.updated_at = self._now_iso()
        return json.dumps({
            "supplier_ref": sup.supplier_ref,
            "supplier_name": sup.supplier_name,
            "cooperation_status": sup.cooperation_status,
            "blacklist_reason": sup.blacklist_reason,
        })

    # =========================================================================
    # Supplier Contact
    # =========================================================================

    @is_tool(ToolType.READ)
    def list_supplier_contacts(self, supplier_ref: str, status: Optional[str] = None) -> str:
        """
        List contacts for a specific supplier.

        Args:
            supplier_ref: The unique identifier of the supplier.
            status: Filter by contact status (active, inactive). None returns all.

        Returns:
            str: JSON string containing a list of supplier contacts.

        Raises:
            ValueError: If the supplier is not found.
        """
        self._get_supplier(supplier_ref)
        results = []
        for sc in self.db.supplier_contact.values():
            if sc.supplier_ref != supplier_ref:
                continue
            if status is not None and sc.status != status:
                continue
            results.append({
                "supplier_contact_ref": sc.supplier_contact_ref,
                "contact_name": sc.contact_name,
                "contact_title": sc.contact_title,
                "phone": sc.phone,
                "email": sc.email,
                "is_primary": sc.is_primary,
                "status": sc.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_supplier_contact(
        self,
        supplier_ref: str,
        contact_name: str,
        contact_title: str,
        phone: str,
        email: str,
        is_primary: bool = False,
    ) -> str:
        """
        Create a new contact for a supplier. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier.
            contact_name: Name of the contact person.
            contact_title: Job title of the contact person.
            phone: Phone number.
            email: Email address.
            is_primary: Whether this is the primary contact. Defaults to False.

        Returns:
            str: JSON string containing the created supplier contact details.

        Raises:
            ValueError: If the supplier is not found.
        """
        self._get_supplier(supplier_ref)
        now = self._now_iso()
        ref = self._generate_ref("SC", self.db.supplier_contact)

        contact = SupplierContact(
            supplier_contact_ref=ref,
            supplier_ref=supplier_ref,
            contact_name=contact_name,
            contact_title=contact_title,
            phone=phone,
            email=email,
            is_primary=is_primary,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.supplier_contact[ref] = contact
        return json.dumps({
            "supplier_contact_ref": ref,
            "contact_name": contact_name,
            "is_primary": is_primary,
            "status": "active",
        })

    @is_tool(ToolType.WRITE)
    def update_supplier_contact(
        self,
        supplier_contact_ref: str,
        contact_name: Optional[str] = None,
        contact_title: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        is_primary: Optional[bool] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Update a supplier contact. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_contact_ref: The unique identifier of the supplier contact.
            contact_name: New contact name. None to keep unchanged.
            contact_title: New contact title. None to keep unchanged.
            phone: New phone number. None to keep unchanged.
            email: New email. None to keep unchanged.
            is_primary: New primary flag. None to keep unchanged.
            status: New status (active, inactive). None to keep unchanged.

        Returns:
            str: JSON string containing the updated supplier contact details.

        Raises:
            ValueError: If the supplier contact is not found or invalid values are provided.
        """
        sc = self._get_supplier_contact(supplier_contact_ref)

        if status is not None:
            valid_statuses = {"active", "inactive"}
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
            sc.status = status

        if contact_name is not None:
            sc.contact_name = contact_name
        if contact_title is not None:
            sc.contact_title = contact_title
        if phone is not None:
            sc.phone = phone
        if email is not None:
            sc.email = email
        if is_primary is not None:
            sc.is_primary = is_primary

        sc.updated_at = self._now_iso()
        return json.dumps({
            "supplier_contact_ref": sc.supplier_contact_ref,
            "contact_name": sc.contact_name,
            "status": sc.status,
            "updated_at": sc.updated_at,
        })

    # =========================================================================
    # Supplier Qualification
    # =========================================================================

    @is_tool(ToolType.READ)
    def list_supplier_qualifications(
        self,
        supplier_ref: str,
        qualification_type: Optional[str] = None,
        verification_status: Optional[str] = None,
    ) -> str:
        """
        List qualifications for a specific supplier.

        Args:
            supplier_ref: The unique identifier of the supplier.
            qualification_type: Filter by qualification type. None returns all.
            verification_status: Filter by verification status. None returns all.

        Returns:
            str: JSON string containing a list of supplier qualifications.

        Raises:
            ValueError: If the supplier is not found.
        """
        self._get_supplier(supplier_ref)
        results = []
        for sq in self.db.supplier_qualification.values():
            if sq.supplier_ref != supplier_ref:
                continue
            if qualification_type is not None and sq.qualification_type != qualification_type:
                continue
            if verification_status is not None and sq.verification_status != verification_status:
                continue
            results.append({
                "supplier_qualification_ref": sq.supplier_qualification_ref,
                "qualification_type": sq.qualification_type,
                "qualification_name": sq.qualification_name,
                "certificate_number": sq.certificate_number,
                "issuing_authority": sq.issuing_authority,
                "issue_date": sq.issue_date,
                "expiry_date": sq.expiry_date,
                "verification_status": sq.verification_status,
                "verified_by_ref": sq.verified_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_supplier_qualification_details(self, supplier_qualification_ref: str) -> str:
        """
        Get detailed information about a specific supplier qualification.

        Args:
            supplier_qualification_ref: The unique identifier of the supplier qualification.

        Returns:
            str: JSON string containing the supplier qualification details.

        Raises:
            ValueError: If the supplier qualification is not found.
        """
        sq = self._get_supplier_qualification(supplier_qualification_ref)
        return json.dumps({
            "supplier_qualification_ref": sq.supplier_qualification_ref,
            "supplier_ref": sq.supplier_ref,
            "qualification_type": sq.qualification_type,
            "qualification_name": sq.qualification_name,
            "certificate_number": sq.certificate_number,
            "issuing_authority": sq.issuing_authority,
            "issue_date": sq.issue_date,
            "expiry_date": sq.expiry_date,
            "file_attachment_ref": sq.file_attachment_ref,
            "verification_status": sq.verification_status,
            "verified_by_ref": sq.verified_by_ref,
            "verified_at": sq.verified_at,
            "created_at": sq.created_at,
            "updated_at": sq.updated_at,
        })

    @is_tool(ToolType.WRITE)
    def verify_supplier_qualification(
        self,
        supplier_qualification_ref: str,
        verified_by_ref: str,
        verification_status: str,
    ) -> str:
        """
        Verify or reject a supplier qualification. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_qualification_ref: The unique identifier of the supplier qualification.
            verified_by_ref: Employee ref of the person verifying the qualification.
            verification_status: New verification status (verified, rejected).

        Returns:
            str: JSON string containing the updated qualification status.

        Raises:
            ValueError: If the qualification is not found, verifier is not found, or invalid status.
        """
        sq = self._get_supplier_qualification(supplier_qualification_ref)
        self._get_employee(verified_by_ref)

        valid_statuses = {"verified", "rejected"}
        if verification_status not in valid_statuses:
            raise ValueError(f"Invalid verification_status: {verification_status}. Must be one of {valid_statuses}")

        if sq.verification_status not in ("pending",):
            raise ValueError(f"Qualification verification status is '{sq.verification_status}', expected 'pending'")

        now = self._now_iso()
        sq.verification_status = verification_status
        sq.verified_by_ref = verified_by_ref
        sq.verified_at = now
        sq.updated_at = now
        return json.dumps({
            "supplier_qualification_ref": sq.supplier_qualification_ref,
            "verification_status": sq.verification_status,
            "verified_by_ref": sq.verified_by_ref,
            "verified_at": sq.verified_at,
        })

    # =========================================================================
    # Supplier Category Association
    # =========================================================================

    @is_tool(ToolType.READ)
    def list_supplier_categories(self, supplier_ref: str) -> str:
        """
        List procurement categories associated with a supplier.

        Args:
            supplier_ref: The unique identifier of the supplier.

        Returns:
            str: JSON string containing a list of category associations for the supplier.

        Raises:
            ValueError: If the supplier is not found.
        """
        self._get_supplier(supplier_ref)
        results = []
        for sc in self.db.supplier_category.values():
            if sc.supplier_ref != supplier_ref and sc.status == "active":
                continue
            if sc.supplier_ref != supplier_ref:
                continue
            if sc.status != "active":
                continue
            cat_name = ""
            if sc.procurement_category_ref in self.db.procurement_category:
                cat_name = self.db.procurement_category[sc.procurement_category_ref].category_name
            results.append({
                "supplier_category_ref": sc.supplier_category_ref,
                "procurement_category_ref": sc.procurement_category_ref,
                "category_name": cat_name,
                "is_preferred": sc.is_preferred,
                "status": sc.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_supplier_to_category(
        self,
        supplier_ref: str,
        procurement_category_ref: str,
        is_preferred: bool = False,
    ) -> str:
        """
        Associate a supplier with a procurement category. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier.
            procurement_category_ref: The unique identifier of the procurement category.
            is_preferred: Whether the supplier is preferred for this category. Defaults to False.

        Returns:
            str: JSON string containing the created association details.

        Raises:
            ValueError: If the supplier or category is not found, or association already exists.
        """
        self._get_supplier(supplier_ref)
        self._get_procurement_category(procurement_category_ref)

        # Check for existing active association
        for sc in self.db.supplier_category.values():
            if (sc.supplier_ref == supplier_ref
                    and sc.procurement_category_ref == procurement_category_ref
                    and sc.status == "active"):
                raise ValueError("Supplier is already associated with this category")

        now = self._now_iso()
        ref = self._generate_ref("SCAT", self.db.supplier_category)
        sc = SupplierCategory(
            supplier_category_ref=ref,
            supplier_ref=supplier_ref,
            procurement_category_ref=procurement_category_ref,
            is_preferred=is_preferred,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.supplier_category[ref] = sc
        return json.dumps({
            "supplier_category_ref": ref,
            "supplier_ref": supplier_ref,
            "procurement_category_ref": procurement_category_ref,
            "is_preferred": is_preferred,
            "status": "active",
        })

    @is_tool(ToolType.WRITE)
    def remove_supplier_from_category(self, supplier_category_ref: str) -> str:
        """
        Remove a supplier from a procurement category. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_category_ref: The unique identifier of the supplier-category association.

        Returns:
            str: JSON string confirming the removal.

        Raises:
            ValueError: If the association is not found or already removed.
        """
        if supplier_category_ref not in self.db.supplier_category:
            raise ValueError("Supplier category association not found")
        sc = self.db.supplier_category[supplier_category_ref]
        if sc.status == "removed":
            raise ValueError("Supplier category association is already removed")
        sc.status = "removed"
        sc.updated_at = self._now_iso()
        return json.dumps({
            "supplier_category_ref": sc.supplier_category_ref,
            "status": sc.status,
        })

    # =========================================================================
    # Supplier Evaluation (供应商信息管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def list_supplier_evaluations(
        self,
        supplier_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        List evaluations for a specific supplier.

        Args:
            supplier_ref: The unique identifier of the supplier.
            status: Filter by evaluation status (draft, submitted, approved, rejected). None returns all.

        Returns:
            str: JSON string containing a list of supplier evaluations.

        Raises:
            ValueError: If the supplier is not found.
        """
        self._get_supplier(supplier_ref)
        results = []
        for se in self.db.supplier_evaluation.values():
            if se.supplier_ref != supplier_ref:
                continue
            if status is not None and se.status != status:
                continue
            results.append({
                "supplier_evaluation_ref": se.supplier_evaluation_ref,
                "evaluation_period": se.evaluation_period,
                "quality_score": se.quality_score,
                "delivery_score": se.delivery_score,
                "price_score": se.price_score,
                "service_score": se.service_score,
                "overall_score": se.overall_score,
                "rating": se.rating,
                "evaluator_ref": se.evaluator_ref,
                "status": se.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_supplier_evaluation_details(self, supplier_evaluation_ref: str) -> str:
        """
        Get detailed information about a specific supplier evaluation.

        Args:
            supplier_evaluation_ref: The unique identifier of the supplier evaluation.

        Returns:
            str: JSON string containing the supplier evaluation details.

        Raises:
            ValueError: If the supplier evaluation is not found.
        """
        se = self._get_supplier_evaluation(supplier_evaluation_ref)
        return json.dumps({
            "supplier_evaluation_ref": se.supplier_evaluation_ref,
            "supplier_ref": se.supplier_ref,
            "evaluation_period": se.evaluation_period,
            "quality_score": se.quality_score,
            "delivery_score": se.delivery_score,
            "price_score": se.price_score,
            "service_score": se.service_score,
            "overall_score": se.overall_score,
            "rating": se.rating,
            "evaluator_ref": se.evaluator_ref,
            "comments": se.comments,
            "status": se.status,
            "created_at": se.created_at,
            "updated_at": se.updated_at,
        })

    @is_tool(ToolType.WRITE)
    def create_supplier_evaluation(
        self,
        supplier_ref: str,
        evaluation_period: str,
        quality_score: float,
        delivery_score: float,
        price_score: float,
        service_score: float,
        overall_score: float,
        rating: str,
        evaluator_ref: str,
        comments: str = "",
    ) -> str:
        """
        Create a new supplier evaluation. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_ref: The unique identifier of the supplier being evaluated.
            evaluation_period: Evaluation period identifier (e.g., 2025-Q1).
            quality_score: Quality score.
            delivery_score: Delivery performance score.
            price_score: Price competitiveness score.
            service_score: Service quality score.
            overall_score: Overall composite score.
            rating: Rating grade (A, B, C, D, E).
            evaluator_ref: Employee ref of the evaluator.
            comments: Evaluator's comments. Defaults to empty string.

        Returns:
            str: JSON string containing the created evaluation details.

        Raises:
            ValueError: If the supplier or evaluator is not found, or invalid rating.
        """
        self._get_supplier(supplier_ref)
        self._get_employee(evaluator_ref)

        valid_ratings = {"A", "B", "C", "D", "E"}
        if rating not in valid_ratings:
            raise ValueError(f"Invalid rating: {rating}. Must be one of {valid_ratings}")

        now = self._now_iso()
        ref = self._generate_ref("SEVAL", self.db.supplier_evaluation)
        se = SupplierEvaluation(
            supplier_evaluation_ref=ref,
            supplier_ref=supplier_ref,
            evaluation_period=evaluation_period,
            quality_score=quality_score,
            delivery_score=delivery_score,
            price_score=price_score,
            service_score=service_score,
            overall_score=overall_score,
            rating=rating,
            evaluator_ref=evaluator_ref,
            comments=comments,
            status="draft",
            created_at=now,
            updated_at=now,
        )
        self.db.supplier_evaluation[ref] = se
        return json.dumps({
            "supplier_evaluation_ref": ref,
            "supplier_ref": supplier_ref,
            "evaluation_period": evaluation_period,
            "rating": rating,
            "status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def submit_supplier_evaluation(self, supplier_evaluation_ref: str) -> str:
        """
        Submit a draft supplier evaluation for approval. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_evaluation_ref: The unique identifier of the supplier evaluation.

        Returns:
            str: JSON string containing the updated evaluation status.

        Raises:
            ValueError: If the evaluation is not found or not in draft status.
        """
        se = self._get_supplier_evaluation(supplier_evaluation_ref)
        if se.status != "draft":
            raise ValueError(f"Evaluation status is '{se.status}', expected 'draft'")
        se.status = "submitted"
        se.updated_at = self._now_iso()
        return json.dumps({
            "supplier_evaluation_ref": se.supplier_evaluation_ref,
            "status": se.status,
        })

    @is_tool(ToolType.WRITE)
    def approve_supplier_evaluation(self, supplier_evaluation_ref: str) -> str:
        """
        Approve a submitted supplier evaluation. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_evaluation_ref: The unique identifier of the supplier evaluation.

        Returns:
            str: JSON string containing the updated evaluation status.

        Raises:
            ValueError: If the evaluation is not found or not in submitted status.
        """
        se = self._get_supplier_evaluation(supplier_evaluation_ref)
        if se.status != "submitted":
            raise ValueError(f"Evaluation status is '{se.status}', expected 'submitted'")
        se.status = "approved"
        se.updated_at = self._now_iso()
        return json.dumps({
            "supplier_evaluation_ref": se.supplier_evaluation_ref,
            "status": se.status,
        })

    @is_tool(ToolType.WRITE)
    def reject_supplier_evaluation(self, supplier_evaluation_ref: str, reason: str) -> str:
        """
        Reject a submitted supplier evaluation. The agent must ask for explicit user confirmation before calling.

        Args:
            supplier_evaluation_ref: The unique identifier of the supplier evaluation.
            reason: Reason for rejecting the evaluation.

        Returns:
            str: JSON string containing the updated evaluation status.

        Raises:
            ValueError: If the evaluation is not found or not in submitted status.
        """
        se = self._get_supplier_evaluation(supplier_evaluation_ref)
        if se.status != "submitted":
            raise ValueError(f"Evaluation status is '{se.status}', expected 'submitted'")
        se.status = "rejected"
        se.comments = f"{se.comments}\nRejected: {reason}" if se.comments else f"Rejected: {reason}"
        se.updated_at = self._now_iso()
        return json.dumps({
            "supplier_evaluation_ref": se.supplier_evaluation_ref,
            "status": se.status,
        })

    # =========================================================================
    # Sourcing Project (采购招投标管理 / 智能寻源管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_sourcing_project_details(self, sourcing_project_ref: str) -> str:
        """
        Get detailed information about a specific sourcing project.

        Args:
            sourcing_project_ref: The unique identifier of the sourcing project.

        Returns:
            str: JSON string containing the sourcing project details.

        Raises:
            ValueError: If the sourcing project is not found.
        """
        sp = self._get_sourcing_project(sourcing_project_ref)
        return json.dumps({
            "sourcing_project_ref": sp.sourcing_project_ref,
            "project_title": sp.project_title,
            "project_code": sp.project_code,
            "sourcing_type": sp.sourcing_type,
            "procurement_category_ref": sp.procurement_category_ref,
            "procurement_method": sp.procurement_method,
            "budget_amount": sp.budget_amount,
            "currency": sp.currency,
            "description": sp.description,
            "requirements": sp.requirements,
            "submission_deadline": sp.submission_deadline,
            "evaluation_criteria": sp.evaluation_criteria,
            "owner_employee_ref": sp.owner_employee_ref,
            "project_status": sp.project_status,
            "awarded_supplier_ref": sp.awarded_supplier_ref,
            "award_date": sp.award_date,
            "cancel_reason": sp.cancel_reason,
            "created_at": sp.created_at,
            "updated_at": sp.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_sourcing_projects(
        self,
        sourcing_type: Optional[str] = None,
        project_status: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> str:
        """
        List sourcing projects with optional filters.

        Args:
            sourcing_type: Filter by sourcing type. None returns all.
            project_status: Filter by project status. None returns all.
            procurement_category_ref: Filter by procurement category. None returns all.
            owner_employee_ref: Filter by project owner. None returns all.

        Returns:
            str: JSON string containing a list of matching sourcing projects.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, sp in self.db.sourcing_project.items():
            if sourcing_type is not None and sp.sourcing_type != sourcing_type:
                continue
            if project_status is not None and sp.project_status != project_status:
                continue
            if procurement_category_ref is not None and sp.procurement_category_ref != procurement_category_ref:
                continue
            if owner_employee_ref is not None and sp.owner_employee_ref != owner_employee_ref:
                continue
            results.append({
                "sourcing_project_ref": sp.sourcing_project_ref,
                "project_title": sp.project_title,
                "project_code": sp.project_code,
                "sourcing_type": sp.sourcing_type,
                "procurement_method": sp.procurement_method,
                "budget_amount": sp.budget_amount,
                "currency": sp.currency,
                "project_status": sp.project_status,
                "submission_deadline": sp.submission_deadline,
                "awarded_supplier_ref": sp.awarded_supplier_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_sourcing_project(
        self,
        project_title: str,
        project_code: str,
        sourcing_type: str,
        procurement_category_ref: str,
        procurement_method: str,
        budget_amount: float,
        currency: str,
        description: str,
        requirements: str,
        submission_deadline: str,
        evaluation_criteria: Dict[str, Any],
        owner_employee_ref: str,
    ) -> str:
        """
        Create a new sourcing project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_title: Title of the sourcing project.
            project_code: Short code for the project.
            sourcing_type: Type of sourcing (competitive_bid, negotiation, sole_source, framework_agreement, reverse_auction).
            procurement_category_ref: Reference to the procurement category.
            procurement_method: Procurement method (centralized, decentralized, hybrid).
            budget_amount: Budget amount for the project.
            currency: Currency code (e.g., CNY, USD).
            description: Description of the project.
            requirements: Detailed requirements.
            submission_deadline: Deadline for supplier submissions (ISO 8601).
            evaluation_criteria: Dictionary of evaluation criteria and their weights.
            owner_employee_ref: Employee ref of the project owner.

        Returns:
            str: JSON string containing the created sourcing project details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_sourcing_types = {"competitive_bid", "negotiation", "sole_source", "framework_agreement", "reverse_auction"}
        if sourcing_type not in valid_sourcing_types:
            raise ValueError(f"Invalid sourcing_type: {sourcing_type}. Must be one of {valid_sourcing_types}")

        valid_methods = {"centralized", "decentralized", "hybrid"}
        if procurement_method not in valid_methods:
            raise ValueError(f"Invalid procurement_method: {procurement_method}. Must be one of {valid_methods}")

        self._get_procurement_category(procurement_category_ref)
        self._get_employee(owner_employee_ref)

        now = self._now_iso()
        ref = self._generate_ref("SP", self.db.sourcing_project)
        sp = SourcingProject(
            sourcing_project_ref=ref,
            project_title=project_title,
            project_code=project_code,
            sourcing_type=sourcing_type,
            procurement_category_ref=procurement_category_ref,
            procurement_method=procurement_method,
            budget_amount=budget_amount,
            currency=currency,
            description=description,
            requirements=requirements,
            bid_document_file_ref=None,
            submission_deadline=submission_deadline,
            evaluation_criteria=evaluation_criteria,
            owner_employee_ref=owner_employee_ref,
            project_status="draft",
            awarded_supplier_ref=None,
            award_date=None,
            cancel_reason=None,
            created_at=now,
            updated_at=now,
        )
        self.db.sourcing_project[ref] = sp
        return json.dumps({
            "sourcing_project_ref": ref,
            "project_title": project_title,
            "project_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def update_sourcing_project_status(
        self,
        sourcing_project_ref: str,
        new_status: str,
        cancel_reason: Optional[str] = None,
        awarded_supplier_ref: Optional[str] = None,
    ) -> str:
        """
        Update the status of a sourcing project. The agent must ask for explicit user confirmation before calling.

        Args:
            sourcing_project_ref: The unique identifier of the sourcing project.
            new_status: New project status (open, evaluation, awarded, cancelled, closed).
            cancel_reason: Reason for cancellation (required if new_status is cancelled).
            awarded_supplier_ref: Supplier ref to award (required if new_status is awarded).

        Returns:
            str: JSON string containing the updated sourcing project status.

        Raises:
            ValueError: If the project is not found, invalid status transition, or missing required fields.
        """
        sp = self._get_sourcing_project(sourcing_project_ref)

        valid_statuses = {"draft", "open", "evaluation", "awarded", "cancelled", "closed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        # Validate transitions
        valid_transitions = {
            "draft": {"open", "cancelled"},
            "open": {"evaluation", "cancelled"},
            "evaluation": {"awarded", "cancelled"},
            "awarded": {"closed"},
            "cancelled": set(),
            "closed": set(),
        }
        if new_status not in valid_transitions.get(sp.project_status, set()):
            raise ValueError(f"Cannot transition from '{sp.project_status}' to '{new_status}'")

        if new_status == "cancelled" and not cancel_reason:
            raise ValueError("cancel_reason is required when cancelling a sourcing project")

        if new_status == "awarded":
            if not awarded_supplier_ref:
                raise ValueError("awarded_supplier_ref is required when awarding a sourcing project")
            self._get_supplier(awarded_supplier_ref)
            sp.awarded_supplier_ref = awarded_supplier_ref
            sp.award_date = self._now_iso()[:10]

        if new_status == "cancelled":
            sp.cancel_reason = cancel_reason

        sp.project_status = new_status
        sp.updated_at = self._now_iso()
        return json.dumps({
            "sourcing_project_ref": sp.sourcing_project_ref,
            "project_status": sp.project_status,
            "awarded_supplier_ref": sp.awarded_supplier_ref,
        })

    # =========================================================================
    # Sourcing Supplier (采购招投标管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def list_sourcing_suppliers(
        self,
        sourcing_project_ref: str,
        status: Optional[str] = None,
        invitation_status: Optional[str] = None,
    ) -> str:
        """
        List suppliers participating in a sourcing project.

        Args:
            sourcing_project_ref: The unique identifier of the sourcing project.
            status: Filter by sourcing supplier status (active, disqualified, withdrawn). None returns all.
            invitation_status: Filter by invitation status. None returns all.

        Returns:
            str: JSON string containing a list of sourcing suppliers.

        Raises:
            ValueError: If the sourcing project is not found.
        """
        self._get_sourcing_project(sourcing_project_ref)
        results = []
        for ss in self.db.sourcing_supplier.values():
            if ss.sourcing_project_ref != sourcing_project_ref:
                continue
            if status is not None and ss.status != status:
                continue
            if invitation_status is not None and ss.invitation_status != invitation_status:
                continue
            supplier_name = ""
            if ss.supplier_ref in self.db.supplier:
                supplier_name = self.db.supplier[ss.supplier_ref].supplier_name
            results.append({
                "sourcing_supplier_ref": ss.sourcing_supplier_ref,
                "supplier_ref": ss.supplier_ref,
                "supplier_name": supplier_name,
                "invitation_status": ss.invitation_status,
                "qualification_check": ss.qualification_check,
                "evaluation_score": ss.evaluation_score,
                "evaluation_rank": ss.evaluation_rank,
                "status": ss.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_sourcing_supplier_details(self, sourcing_supplier_ref: str) -> str:
        """
        Get detailed information about a sourcing supplier record.

        Args:
            sourcing_supplier_ref: The unique identifier of the sourcing supplier record.

        Returns:
            str: JSON string containing the sourcing supplier details.

        Raises:
            ValueError: If the sourcing supplier record is not found.
        """
        ss = self._get_sourcing_supplier(sourcing_supplier_ref)
        return json.dumps({
            "sourcing_supplier_ref": ss.sourcing_supplier_ref,
            "sourcing_project_ref": ss.sourcing_project_ref,
            "supplier_ref": ss.supplier_ref,
            "invitation_status": ss.invitation_status,
            "qualification_check": ss.qualification_check,
            "evaluation_score": ss.evaluation_score,
            "evaluation_rank": ss.evaluation_rank,
            "evaluation_comments": ss.evaluation_comments,
            "status": ss.status,
            "invited_at": ss.invited_at,
            "responded_at": ss.responded_at,
            "created_at": ss.created_at,
            "updated_at": ss.updated_at,
        })

    @is_tool(ToolType.WRITE)
    def invite_supplier_to_sourcing(
        self,
        sourcing_project_ref: str,
        supplier_ref: str,
    ) -> str:
        """
        Invite a supplier to participate in a sourcing project. The agent must ask for explicit user confirmation before calling.

        Args:
            sourcing_project_ref: The unique identifier of the sourcing project.
            supplier_ref: The unique identifier of the supplier to invite.

        Returns:
            str: JSON string containing the created sourcing supplier record.

        Raises:
            ValueError: If the project or supplier is not found, or supplier already invited.
        """
        sp = self._get_sourcing_project(sourcing_project_ref)
        self._get_supplier(supplier_ref)

        if sp.project_status not in ("draft", "open"):
            raise ValueError(f"Cannot invite suppliers when project status is '{sp.project_status}'")

        # Check for existing invitation
        for ss in self.db.sourcing_supplier.values():
            if ss.sourcing_project_ref == sourcing_project_ref and ss.supplier_ref == supplier_ref:
                raise ValueError("Supplier is already invited to this sourcing project")

        now = self._now_iso()
        ref = self._generate_ref("SS", self.db.sourcing_supplier)
        ss = SourcingSupplier(
            sourcing_supplier_ref=ref,
            sourcing_project_ref=sourcing_project_ref,
            supplier_ref=supplier_ref,
            invitation_status="invited",
            qualification_check="pending",
            evaluation_score=None,
            evaluation_rank=None,
            evaluation_comments="",
            status="active",
            invited_at=now,
            responded_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.sourcing_supplier[ref] = ss
        return json.dumps({
            "sourcing_supplier_ref": ref,
            "sourcing_project_ref": sourcing_project_ref,
            "supplier_ref": supplier_ref,
            "invitation_status": "invited",
            "status": "active",
        })

    @is_tool(ToolType.WRITE)
    def update_sourcing_supplier(
        self,
        sourcing_supplier_ref: str,
        invitation_status: Optional[str] = None,
        qualification_check: Optional[str] = None,
        evaluation_score: Optional[float] = None,
        evaluation_rank: Optional[int] = None,
        evaluation_comments: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Update a sourcing supplier record. The agent must ask for explicit user confirmation before calling.

        Args:
            sourcing_supplier_ref: The unique identifier of the sourcing supplier record.
            invitation_status: New invitation status (invited, accepted, declined, no_response). None to keep unchanged.
            qualification_check: New qualification check result (pending, passed, failed). None to keep unchanged.
            evaluation_score: New evaluation score. None to keep unchanged.
            evaluation_rank: New evaluation rank. None to keep unchanged.
            evaluation_comments: New evaluation comments. None to keep unchanged.
            status: New status (active, disqualified, withdrawn). None to keep unchanged.

        Returns:
            str: JSON string containing the updated sourcing supplier record.

        Raises:
            ValueError: If the record is not found or invalid values are provided.
        """
        ss = self._get_sourcing_supplier(sourcing_supplier_ref)

        if invitation_status is not None:
            valid = {"invited", "accepted", "declined", "no_response"}
            if invitation_status not in valid:
                raise ValueError(f"Invalid invitation_status: {invitation_status}. Must be one of {valid}")
            ss.invitation_status = invitation_status
            if invitation_status in ("accepted", "declined", "no_response"):
                ss.responded_at = self._now_iso()

        if qualification_check is not None:
            valid = {"pending", "passed", "failed"}
            if qualification_check not in valid:
                raise ValueError(f"Invalid qualification_check: {qualification_check}. Must be one of {valid}")
            ss.qualification_check = qualification_check

        if evaluation_score is not None:
            ss.evaluation_score = evaluation_score
        if evaluation_rank is not None:
            ss.evaluation_rank = evaluation_rank
        if evaluation_comments is not None:
            ss.evaluation_comments = evaluation_comments

        if status is not None:
            valid = {"active", "disqualified", "withdrawn"}
            if status not in valid:
                raise ValueError(f"Invalid status: {status}. Must be one of {valid}")
            ss.status = status

        ss.updated_at = self._now_iso()
        return json.dumps({
            "sourcing_supplier_ref": ss.sourcing_supplier_ref,
            "invitation_status": ss.invitation_status,
            "qualification_check": ss.qualification_check,
            "evaluation_score": ss.evaluation_score,
            "evaluation_rank": ss.evaluation_rank,
            "status": ss.status,
        })

    # =========================================================================
    # Quotation (报价处理与审批)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_quotation_details(self, quotation_ref: str) -> str:
        """
        Get detailed information about a specific quotation.

        Args:
            quotation_ref: The unique identifier of the quotation.

        Returns:
            str: JSON string containing the quotation details.

        Raises:
            ValueError: If the quotation is not found.
        """
        q = self._get_quotation(quotation_ref)
        return json.dumps({
            "quotation_ref": q.quotation_ref,
            "quotation_code": q.quotation_code,
            "sourcing_project_ref": q.sourcing_project_ref,
            "supplier_ref": q.supplier_ref,
            "procurement_category_ref": q.procurement_category_ref,
            "currency": q.currency,
            "total_amount": q.total_amount,
            "tax_rate": q.tax_rate,
            "tax_amount": q.tax_amount,
            "validity_date": q.validity_date,
            "payment_terms": q.payment_terms,
            "delivery_terms": q.delivery_terms,
            "submitted_by_ref": q.submitted_by_ref,
            "quotation_status": q.quotation_status,
            "notes": q.notes,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_quotations(
        self,
        supplier_ref: Optional[str] = None,
        sourcing_project_ref: Optional[str] = None,
        quotation_status: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
    ) -> str:
        """
        List quotations with optional filters.

        Args:
            supplier_ref: Filter by supplier. None returns all.
            sourcing_project_ref: Filter by sourcing project. None returns all.
            quotation_status: Filter by quotation status. None returns all.
            procurement_category_ref: Filter by procurement category. None returns all.

        Returns:
            str: JSON string containing a list of matching quotations.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, q in self.db.quotation.items():
            if supplier_ref is not None and q.supplier_ref != supplier_ref:
                continue
            if sourcing_project_ref is not None and q.sourcing_project_ref != sourcing_project_ref:
                continue
            if quotation_status is not None and q.quotation_status != quotation_status:
                continue
            if procurement_category_ref is not None and q.procurement_category_ref != procurement_category_ref:
                continue
            supplier_name = ""
            if q.supplier_ref in self.db.supplier:
                supplier_name = self.db.supplier[q.supplier_ref].supplier_name
            results.append({
                "quotation_ref": q.quotation_ref,
                "quotation_code": q.quotation_code,
                "supplier_ref": q.supplier_ref,
                "supplier_name": supplier_name,
                "total_amount": q.total_amount,
                "currency": q.currency,
                "quotation_status": q.quotation_status,
                "validity_date": q.validity_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_quotation_items(self, quotation_ref: str) -> str:
        """
        List line items for a specific quotation.

        Args:
            quotation_ref: The unique identifier of the quotation.

        Returns:
            str: JSON string containing a list of quotation items.

        Raises:
            ValueError: If the quotation is not found.
        """
        self._get_quotation(quotation_ref)
        results = []
        for qi in self.db.quotation_item.values():
            if qi.quotation_ref != quotation_ref:
                continue
            results.append({
                "quotation_item_ref": qi.quotation_item_ref,
                "item_name": qi.item_name,
                "item_description": qi.item_description,
                "specification": qi.specification,
                "unit": qi.unit,
                "quantity": qi.quantity,
                "unit_price": qi.unit_price,
                "line_amount": qi.line_amount,
                "delivery_days": qi.delivery_days,
                "notes": qi.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def compare_quotations(self, quotation_refs: List[str]) -> str:
        """
        Compare multiple quotations side by side.

        Args:
            quotation_refs: List of quotation refs to compare.

        Returns:
            str: JSON string containing comparison data for the quotations.

        Raises:
            ValueError: If any quotation is not found or fewer than 2 quotations provided.
        """
        if len(quotation_refs) < 2:
            raise ValueError("At least 2 quotation refs are required for comparison")

        comparisons = []
        for qref in quotation_refs:
            q = self._get_quotation(qref)
            supplier_name = ""
            if q.supplier_ref in self.db.supplier:
                supplier_name = self.db.supplier[q.supplier_ref].supplier_name

            items = []
            for qi in self.db.quotation_item.values():
                if qi.quotation_ref == qref:
                    items.append({
                        "item_name": qi.item_name,
                        "quantity": qi.quantity,
                        "unit_price": qi.unit_price,
                        "line_amount": qi.line_amount,
                        "delivery_days": qi.delivery_days,
                    })

            comparisons.append({
                "quotation_ref": q.quotation_ref,
                "quotation_code": q.quotation_code,
                "supplier_ref": q.supplier_ref,
                "supplier_name": supplier_name,
                "total_amount": q.total_amount,
                "currency": q.currency,
                "tax_rate": q.tax_rate,
                "tax_amount": q.tax_amount,
                "payment_terms": q.payment_terms,
                "delivery_terms": q.delivery_terms,
                "validity_date": q.validity_date,
                "quotation_status": q.quotation_status,
                "items": items,
            })
        return json.dumps(comparisons)

    @is_tool(ToolType.WRITE)
    def update_quotation_status(
        self,
        quotation_ref: str,
        new_status: str,
    ) -> str:
        """
        Update the status of a quotation (accept, reject, withdraw, etc.). The agent must ask for explicit user confirmation before calling.

        Args:
            quotation_ref: The unique identifier of the quotation.
            new_status: New quotation status (submitted, under_review, accepted, rejected, withdrawn).

        Returns:
            str: JSON string containing the updated quotation status.

        Raises:
            ValueError: If the quotation is not found or invalid status transition.
        """
        q = self._get_quotation(quotation_ref)

        valid_statuses = {"draft", "submitted", "under_review", "accepted", "rejected", "expired", "withdrawn"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "draft": {"submitted", "withdrawn"},
            "submitted": {"under_review", "withdrawn"},
            "under_review": {"accepted", "rejected"},
            "accepted": set(),
            "rejected": set(),
            "expired": set(),
            "withdrawn": set(),
        }
        if new_status not in valid_transitions.get(q.quotation_status, set()):
            raise ValueError(f"Cannot transition from '{q.quotation_status}' to '{new_status}'")

        q.quotation_status = new_status
        q.updated_at = self._now_iso()
        return json.dumps({
            "quotation_ref": q.quotation_ref,
            "quotation_status": q.quotation_status,
        })

    # =========================================================================
    # Purchase Requisition (特殊采购申请 / 采购审批流程管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_purchase_requisition_details(self, purchase_requisition_ref: str) -> str:
        """
        Get detailed information about a specific purchase requisition.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            str: JSON string containing the purchase requisition details.

        Raises:
            ValueError: If the purchase requisition is not found.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        return json.dumps({
            "purchase_requisition_ref": pr.purchase_requisition_ref,
            "requisition_code": pr.requisition_code,
            "requisition_type": pr.requisition_type,
            "procurement_category_ref": pr.procurement_category_ref,
            "department_ref": pr.department_ref,
            "requestor_ref": pr.requestor_ref,
            "procurement_method": pr.procurement_method,
            "currency": pr.currency,
            "estimated_amount": pr.estimated_amount,
            "required_date": pr.required_date,
            "business_justification": pr.business_justification,
            "special_requirements": pr.special_requirements,
            "suggested_supplier_ref": pr.suggested_supplier_ref,
            "requisition_status": pr.requisition_status,
            "submitted_at": pr.submitted_at,
            "approved_at": pr.approved_at,
            "rejected_reason": pr.rejected_reason,
            "created_at": pr.created_at,
            "updated_at": pr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_purchase_requisitions(
        self,
        requestor_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        requisition_status: Optional[str] = None,
        requisition_type: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
    ) -> str:
        """
        List purchase requisitions with optional filters.

        Args:
            requestor_ref: Filter by requestor employee ref. None returns all.
            department_ref: Filter by department ref. None returns all.
            requisition_status: Filter by requisition status. None returns all.
            requisition_type: Filter by requisition type. None returns all.
            procurement_category_ref: Filter by procurement category. None returns all.

        Returns:
            str: JSON string containing a list of matching purchase requisitions.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, pr in self.db.purchase_requisition.items():
            if requestor_ref is not None and pr.requestor_ref != requestor_ref:
                continue
            if department_ref is not None and pr.department_ref != department_ref:
                continue
            if requisition_status is not None and pr.requisition_status != requisition_status:
                continue
            if requisition_type is not None and pr.requisition_type != requisition_type:
                continue
            if procurement_category_ref is not None and pr.procurement_category_ref != procurement_category_ref:
                continue
            results.append({
                "purchase_requisition_ref": pr.purchase_requisition_ref,
                "requisition_code": pr.requisition_code,
                "requisition_type": pr.requisition_type,
                "requestor_ref": pr.requestor_ref,
                "department_ref": pr.department_ref,
                "estimated_amount": pr.estimated_amount,
                "currency": pr.currency,
                "requisition_status": pr.requisition_status,
                "required_date": pr.required_date,
                "submitted_at": pr.submitted_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_requisition_items(self, purchase_requisition_ref: str) -> str:
        """
        List line items for a specific purchase requisition.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            str: JSON string containing a list of requisition items.

        Raises:
            ValueError: If the purchase requisition is not found.
        """
        self._get_purchase_requisition(purchase_requisition_ref)
        results = []
        for ri in self.db.requisition_item.values():
            if ri.purchase_requisition_ref != purchase_requisition_ref:
                continue
            results.append({
                "requisition_item_ref": ri.requisition_item_ref,
                "item_name": ri.item_name,
                "item_description": ri.item_description,
                "specification": ri.specification,
                "unit": ri.unit,
                "quantity": ri.quantity,
                "estimated_unit_price": ri.estimated_unit_price,
                "estimated_line_amount": ri.estimated_line_amount,
                "required_date": ri.required_date,
                "notes": ri.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_purchase_requisition(
        self,
        requisition_code: str,
        requisition_type: str,
        procurement_category_ref: str,
        department_ref: str,
        requestor_ref: str,
        procurement_method: str,
        currency: str,
        estimated_amount: float,
        required_date: str,
        business_justification: str,
        special_requirements: str = "",
        suggested_supplier_ref: Optional[str] = None,
    ) -> str:
        """
        Create a new purchase requisition. The agent must ask for explicit user confirmation before calling.

        Args:
            requisition_code: Short code for the requisition.
            requisition_type: 类型（requisition （standard, urgent, blanket, service).
            procurement_category_ref: Reference to the procurement category.
            department_ref: Reference to the requesting department.
            requestor_ref: Employee ref of the requestor.
            procurement_method: Procurement method (centralized, decentralized, hybrid).
            currency: Currency code (e.g., CNY, USD).
            estimated_amount: Estimated total amount.
            required_date: Date by which items are required (ISO 8601 date).
            business_justification: Business justification for the purchase.
            special_requirements: Any special requirements. Defaults to empty string.
            suggested_supplier_ref: Reference to a suggested supplier. Defaults to None.

        Returns:
            str: JSON string containing the created purchase requisition details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_types = {"standard", "urgent", "blanket", "service"}
        if requisition_type not in valid_types:
            raise ValueError(f"Invalid requisition_type: {requisition_type}. Must be one of {valid_types}")

        valid_methods = {"centralized", "decentralized", "hybrid"}
        if procurement_method not in valid_methods:
            raise ValueError(f"Invalid procurement_method: {procurement_method}. Must be one of {valid_methods}")

        self._get_procurement_category(procurement_category_ref)
        self._get_department(department_ref)
        self._get_employee(requestor_ref)
        if suggested_supplier_ref is not None:
            self._get_supplier(suggested_supplier_ref)

        now = self._now_iso()
        ref = self._generate_ref("PR", self.db.purchase_requisition)
        pr = PurchaseRequisition(
            purchase_requisition_ref=ref,
            requisition_code=requisition_code,
            requisition_type=requisition_type,
            procurement_category_ref=procurement_category_ref,
            department_ref=department_ref,
            requestor_ref=requestor_ref,
            procurement_method=procurement_method,
            currency=currency,
            estimated_amount=estimated_amount,
            required_date=required_date,
            business_justification=business_justification,
            special_requirements=special_requirements,
            suggested_supplier_ref=suggested_supplier_ref,
            requisition_status="draft",
            submitted_at=None,
            approved_at=None,
            rejected_reason=None,
            created_at=now,
            updated_at=now,
        )
        self.db.purchase_requisition[ref] = pr
        return json.dumps({
            "purchase_requisition_ref": ref,
            "requisition_code": requisition_code,
            "requisition_type": requisition_type,
            "requisition_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def add_requisition_item(
        self,
        purchase_requisition_ref: str,
        item_name: str,
        item_description: str,
        specification: str,
        unit: str,
        quantity: int,
        estimated_unit_price: float,
        required_date: str,
        notes: str = "",
    ) -> str:
        """
        Add a line item to a purchase requisition. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.
            item_name: Name of the requested item.
            item_description: Description of the item.
            specification: Technical specification.
            unit: Unit of measure.
            quantity: Requested quantity.
            estimated_unit_price: Estimated unit price.
            required_date: Date by which the item is required (ISO 8601 date).
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created requisition item details.

        Raises:
            ValueError: If the purchase requisition is not found or not in draft status.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        if pr.requisition_status != "draft":
            raise ValueError(f"Cannot add items when requisition status is '{pr.requisition_status}'")

        now = self._now_iso()
        ref = self._generate_ref("RI", self.db.requisition_item)
        estimated_line_amount = round(quantity * estimated_unit_price, 2)
        ri = RequisitionItem(
            requisition_item_ref=ref,
            purchase_requisition_ref=purchase_requisition_ref,
            item_name=item_name,
            item_description=item_description,
            specification=specification,
            unit=unit,
            quantity=quantity,
            estimated_unit_price=estimated_unit_price,
            estimated_line_amount=estimated_line_amount,
            required_date=required_date,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.requisition_item[ref] = ri
        return json.dumps({
            "requisition_item_ref": ref,
            "item_name": item_name,
            "quantity": quantity,
            "estimated_line_amount": estimated_line_amount,
        })

    @is_tool(ToolType.WRITE)
    def submit_purchase_requisition(self, purchase_requisition_ref: str) -> str:
        """
        Submit a draft purchase requisition for approval. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            str: JSON string containing the updated requisition status.

        Raises:
            ValueError: If the requisition is not found or not in draft status.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        if pr.requisition_status != "draft":
            raise ValueError(f"Requisition status is '{pr.requisition_status}', expected 'draft'")

        now = self._now_iso()
        pr.requisition_status = "submitted"
        pr.submitted_at = now
        pr.updated_at = now
        return json.dumps({
            "purchase_requisition_ref": pr.purchase_requisition_ref,
            "requisition_status": pr.requisition_status,
            "submitted_at": pr.submitted_at,
        })

    @is_tool(ToolType.WRITE)
    def approve_purchase_requisition(self, purchase_requisition_ref: str) -> str:
        """
        Approve a submitted purchase requisition. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            str: JSON string containing the updated requisition status.

        Raises:
            ValueError: If the requisition is not found or not in submitted/under_review status.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        if pr.requisition_status not in ("submitted", "under_review"):
            raise ValueError(f"Requisition status is '{pr.requisition_status}', expected 'submitted' or 'under_review'")

        now = self._now_iso()
        pr.requisition_status = "approved"
        pr.approved_at = now
        pr.updated_at = now
        return json.dumps({
            "purchase_requisition_ref": pr.purchase_requisition_ref,
            "requisition_status": pr.requisition_status,
            "approved_at": pr.approved_at,
        })

    @is_tool(ToolType.WRITE)
    def reject_purchase_requisition(self, purchase_requisition_ref: str, reason: str) -> str:
        """
        Reject a submitted purchase requisition. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.
            reason: Reason for rejection.

        Returns:
            str: JSON string containing the updated requisition status.

        Raises:
            ValueError: If the requisition is not found or not in submitted/under_review status.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        if pr.requisition_status not in ("submitted", "under_review"):
            raise ValueError(f"Requisition status is '{pr.requisition_status}', expected 'submitted' or 'under_review'")

        pr.requisition_status = "rejected"
        pr.rejected_reason = reason
        pr.updated_at = self._now_iso()
        return json.dumps({
            "purchase_requisition_ref": pr.purchase_requisition_ref,
            "requisition_status": pr.requisition_status,
            "rejected_reason": pr.rejected_reason,
        })

    @is_tool(ToolType.WRITE)
    def cancel_purchase_requisition(self, purchase_requisition_ref: str) -> str:
        """
        Cancel a purchase requisition. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_requisition_ref: The unique identifier of the purchase requisition.

        Returns:
            str: JSON string containing the updated requisition status.

        Raises:
            ValueError: If the requisition is not found or already in a terminal status.
        """
        pr = self._get_purchase_requisition(purchase_requisition_ref)
        if pr.requisition_status in ("cancelled", "fulfilled"):
            raise ValueError(f"Requisition status is '{pr.requisition_status}', cannot cancel")

        pr.requisition_status = "cancelled"
        pr.updated_at = self._now_iso()
        return json.dumps({
            "purchase_requisition_ref": pr.purchase_requisition_ref,
            "requisition_status": pr.requisition_status,
        })

    # =========================================================================
    # Purchase Contract (采购合同关联下单)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_purchase_contract_details(self, purchase_contract_ref: str) -> str:
        """
        Get detailed information about a specific purchase contract.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.

        Returns:
            str: JSON string containing the purchase contract details.

        Raises:
            ValueError: 若the purchase contract is not found。
        """
        pc = self._get_purchase_contract(purchase_contract_ref)
        return json.dumps({
            "purchase_contract_ref": pc.purchase_contract_ref,
            "contract_code": pc.contract_code,
            "contract_title": pc.contract_title,
            "contract_type": pc.contract_type,
            "supplier_ref": pc.supplier_ref,
            "procurement_category_ref": pc.procurement_category_ref,
            "sourcing_project_ref": pc.sourcing_project_ref,
            "currency": pc.currency,
            "total_amount": pc.total_amount,
            "tax_rate": pc.tax_rate,
            "payment_terms": pc.payment_terms,
            "delivery_terms": pc.delivery_terms,
            "effective_date": pc.effective_date,
            "expiry_date": pc.expiry_date,
            "auto_renew": pc.auto_renew,
            "owner_employee_ref": pc.owner_employee_ref,
            "signer_employee_ref": pc.signer_employee_ref,
            "signed_at": pc.signed_at,
            "contract_status": pc.contract_status,
            "consumed_amount": pc.consumed_amount,
            "termination_reason": pc.termination_reason,
            "created_at": pc.created_at,
            "updated_at": pc.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_purchase_contracts(
        self,
        supplier_ref: Optional[str] = None,
        contract_status: Optional[str] = None,
        contract_type: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> str:
        """
        List purchase contracts with optional filters.

        Args:
            supplier_ref: Filter by supplier. None returns all.
            contract_status: Filter by contract status. None returns all.
            contract_type: Filter by contract type. None returns all.
            procurement_category_ref: Filter by procurement category. None returns all.
            owner_employee_ref: Filter by contract owner. None returns all.

        Returns:
            str: JSON string containing a list of matching purchase contracts.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, pc in self.db.purchase_contract.items():
            if supplier_ref is not None and pc.supplier_ref != supplier_ref:
                continue
            if contract_status is not None and pc.contract_status != contract_status:
                continue
            if contract_type is not None and pc.contract_type != contract_type:
                continue
            if procurement_category_ref is not None and pc.procurement_category_ref != procurement_category_ref:
                continue
            if owner_employee_ref is not None and pc.owner_employee_ref != owner_employee_ref:
                continue
            supplier_name = ""
            if pc.supplier_ref in self.db.supplier:
                supplier_name = self.db.supplier[pc.supplier_ref].supplier_name
            results.append({
                "purchase_contract_ref": pc.purchase_contract_ref,
                "contract_code": pc.contract_code,
                "contract_title": pc.contract_title,
                "contract_type": pc.contract_type,
                "supplier_ref": pc.supplier_ref,
                "supplier_name": supplier_name,
                "total_amount": pc.total_amount,
                "currency": pc.currency,
                "contract_status": pc.contract_status,
                "effective_date": pc.effective_date,
                "expiry_date": pc.expiry_date,
                "consumed_amount": pc.consumed_amount,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_contract_items(self, purchase_contract_ref: str) -> str:
        """
        List line items for a specific purchase contract.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.

        Returns:
            str: JSON string containing a list of contract items.

        Raises:
            ValueError: If the purchase contract is not found.
        """
        self._get_purchase_contract(purchase_contract_ref)
        results = []
        for ci in self.db.contract_item.values():
            if ci.purchase_contract_ref != purchase_contract_ref:
                continue
            results.append({
                "contract_item_ref": ci.contract_item_ref,
                "item_name": ci.item_name,
                "item_description": ci.item_description,
                "specification": ci.specification,
                "unit": ci.unit,
                "contracted_quantity": ci.contracted_quantity,
                "unit_price": ci.unit_price,
                "line_amount": ci.line_amount,
                "ordered_quantity": ci.ordered_quantity,
                "received_quantity": ci.received_quantity,
                "notes": ci.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_purchase_contract(
        self,
        contract_code: str,
        contract_title: str,
        contract_type: str,
        supplier_ref: str,
        procurement_category_ref: str,
        currency: str,
        total_amount: float,
        tax_rate: float,
        payment_terms: str,
        delivery_terms: str,
        effective_date: str,
        expiry_date: str,
        owner_employee_ref: str,
        signer_employee_ref: str,
        auto_renew: bool = False,
        sourcing_project_ref: Optional[str] = None,
    ) -> str:
        """
        Create a new purchase contract. The agent must ask for explicit user confirmation before calling.

        Args:
            contract_code: Short code for the contract.
            contract_title: Title of the contract.
            contract_type: Type of contract (fixed_price, cost_plus, time_and_materials, framework, blanket).
            supplier_ref: Reference to the supplier.
            procurement_category_ref: Reference to the procurement category.
            currency: Currency code.
            total_amount: Total contract amount.
            tax_rate: Applicable tax rate as a decimal.
            payment_terms: Payment terms.
            delivery_terms: Delivery terms.
            effective_date: Contract effective date (ISO 8601 date).
            expiry_date: Contract expiry date (ISO 8601 date).
            owner_employee_ref: Employee ref of the contract owner.
            signer_employee_ref: Employee ref of the contract signer.
            auto_renew: Whether the contract auto-renews. Defaults to False.
            sourcing_project_ref: Reference to the associated sourcing project. Defaults to None.

        Returns:
            str: JSON string containing the created purchase contract details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_types = {"fixed_price", "cost_plus", "time_and_materials", "framework", "blanket"}
        if contract_type not in valid_types:
            raise ValueError(f"Invalid contract_type: {contract_type}. Must be one of {valid_types}")

        self._get_supplier(supplier_ref)
        self._get_procurement_category(procurement_category_ref)
        self._get_employee(owner_employee_ref)
        self._get_employee(signer_employee_ref)
        if sourcing_project_ref is not None:
            self._get_sourcing_project(sourcing_project_ref)

        now = self._now_iso()
        ref = self._generate_ref("PC", self.db.purchase_contract)
        pc = PurchaseContract(
            purchase_contract_ref=ref,
            contract_code=contract_code,
            contract_title=contract_title,
            contract_type=contract_type,
            supplier_ref=supplier_ref,
            procurement_category_ref=procurement_category_ref,
            sourcing_project_ref=sourcing_project_ref,
            currency=currency,
            total_amount=total_amount,
            tax_rate=tax_rate,
            payment_terms=payment_terms,
            delivery_terms=delivery_terms,
            effective_date=effective_date,
            expiry_date=expiry_date,
            auto_renew=auto_renew,
            contract_file_ref=None,
            owner_employee_ref=owner_employee_ref,
            signer_employee_ref=signer_employee_ref,
            signed_at=None,
            contract_status="draft",
            consumed_amount=0.0,
            termination_reason=None,
            created_at=now,
            updated_at=now,
        )
        self.db.purchase_contract[ref] = pc
        return json.dumps({
            "purchase_contract_ref": ref,
            "contract_code": contract_code,
            "contract_title": contract_title,
            "contract_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def update_purchase_contract_status(
        self,
        purchase_contract_ref: str,
        new_status: str,
        termination_reason: Optional[str] = None,
    ) -> str:
        """
        Update the status of a purchase contract. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.
            new_status: New contract status (pending_approval, active, suspended, expired, terminated, completed).
            termination_reason: Reason for termination (required if new_status is terminated).

        Returns:
            str: JSON string containing the updated contract status.

        Raises:
            ValueError: If the contract is not found, invalid status transition, or missing required fields.
        """
        pc = self._get_purchase_contract(purchase_contract_ref)

        valid_statuses = {"draft", "pending_approval", "active", "suspended", "expired", "terminated", "completed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "draft": {"pending_approval", "cancelled"},
            "pending_approval": {"active", "draft"},
            "active": {"suspended", "expired", "terminated", "completed"},
            "suspended": {"active", "terminated"},
            "expired": set(),
            "terminated": set(),
            "completed": set(),
        }
        if new_status not in valid_transitions.get(pc.contract_status, set()):
            raise ValueError(f"Cannot transition from '{pc.contract_status}' to '{new_status}'")

        if new_status == "terminated" and not termination_reason:
            raise ValueError("termination_reason is required when terminating a contract")

        if new_status == "terminated":
            pc.termination_reason = termination_reason

        if new_status == "active" and pc.signed_at is None:
            pc.signed_at = self._now_iso()

        pc.contract_status = new_status
        pc.updated_at = self._now_iso()
        return json.dumps({
            "purchase_contract_ref": pc.purchase_contract_ref,
            "contract_status": pc.contract_status,
        })

    # =========================================================================
    # Purchase Order (采购合同关联下单 / 特殊下单场景)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_purchase_order_details(self, purchase_order_ref: str) -> str:
        """
        Get detailed information about a specific purchase order.

        Args:
            purchase_order_ref: The unique identifier of the purchase order.

        Returns:
            str: JSON string containing the purchase order details.

        Raises:
            ValueError: If the purchase order is not found.
        """
        po = self._get_purchase_order(purchase_order_ref)
        supplier_name = ""
        if po.supplier_ref in self.db.supplier:
            supplier_name = self.db.supplier[po.supplier_ref].supplier_name
        return json.dumps({
            "purchase_order_ref": po.purchase_order_ref,
            "order_code": po.order_code,
            "order_type": po.order_type,
            "purchase_requisition_ref": po.purchase_requisition_ref,
            "purchase_contract_ref": po.purchase_contract_ref,
            "supplier_ref": po.supplier_ref,
            "supplier_name": supplier_name,
            "procurement_category_ref": po.procurement_category_ref,
            "department_ref": po.department_ref,
            "requestor_ref": po.requestor_ref,
            "buyer_ref": po.buyer_ref,
            "currency": po.currency,
            "total_amount": po.total_amount,
            "tax_rate": po.tax_rate,
            "tax_amount": po.tax_amount,
            "payment_terms": po.payment_terms,
            "delivery_address": po.delivery_address,
            "expected_delivery_date": po.expected_delivery_date,
            "priority": po.priority,
            "order_status": po.order_status,
            "submitted_at": po.submitted_at,
            "approved_at": po.approved_at,
            "sent_to_supplier_at": po.sent_to_supplier_at,
            "supplier_confirmed_at": po.supplier_confirmed_at,
            "completed_at": po.completed_at,
            "cancelled_at": po.cancelled_at,
            "cancel_reason": po.cancel_reason,
            "notes": po.notes,
            "created_at": po.created_at,
            "updated_at": po.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_purchase_orders(
        self,
        supplier_ref: Optional[str] = None,
        order_status: Optional[str] = None,
        order_type: Optional[str] = None,
        department_ref: Optional[str] = None,
        requestor_ref: Optional[str] = None,
        buyer_ref: Optional[str] = None,
        purchase_contract_ref: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> str:
        """
        List purchase orders with optional filters.

        Args:
            supplier_ref: Filter by supplier. None returns all.
            order_status: Filter by order status. None returns all.
            order_type: Filter by order type. None returns all.
            department_ref: Filter by department. None returns all.
            requestor_ref: Filter by requestor. None returns all.
            buyer_ref: Filter by buyer. None returns all.
            purchase_contract_ref: Filter by associated contract. None returns all.
            priority: Filter by priority. None returns all.

        Returns:
            str: JSON string containing a list of matching purchase orders.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, po in self.db.purchase_order.items():
            if supplier_ref is not None and po.supplier_ref != supplier_ref:
                continue
            if order_status is not None and po.order_status != order_status:
                continue
            if order_type is not None and po.order_type != order_type:
                continue
            if department_ref is not None and po.department_ref != department_ref:
                continue
            if requestor_ref is not None and po.requestor_ref != requestor_ref:
                continue
            if buyer_ref is not None and po.buyer_ref != buyer_ref:
                continue
            if purchase_contract_ref is not None and po.purchase_contract_ref != purchase_contract_ref:
                continue
            if priority is not None and po.priority != priority:
                continue
            supplier_name = ""
            if po.supplier_ref in self.db.supplier:
                supplier_name = self.db.supplier[po.supplier_ref].supplier_name
            results.append({
                "purchase_order_ref": po.purchase_order_ref,
                "order_code": po.order_code,
                "order_type": po.order_type,
                "supplier_ref": po.supplier_ref,
                "supplier_name": supplier_name,
                "total_amount": po.total_amount,
                "currency": po.currency,
                "priority": po.priority,
                "order_status": po.order_status,
                "expected_delivery_date": po.expected_delivery_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_purchase_order_items(self, purchase_order_ref: str) -> str:
        """
        List line items for a specific purchase order.

        Args:
            purchase_order_ref: The unique identifier of the purchase order.

        Returns:
            str: JSON string containing a list of purchase order items.

        Raises:
            ValueError: If the purchase order is not found.
        """
        self._get_purchase_order(purchase_order_ref)
        results = []
        for poi in self.db.purchase_order_item.values():
            if poi.purchase_order_ref != purchase_order_ref:
                continue
            results.append({
                "purchase_order_item_ref": poi.purchase_order_item_ref,
                "contract_item_ref": poi.contract_item_ref,
                "requisition_item_ref": poi.requisition_item_ref,
                "item_name": poi.item_name,
                "item_description": poi.item_description,
                "specification": poi.specification,
                "unit": poi.unit,
                "quantity": poi.quantity,
                "unit_price": poi.unit_price,
                "line_amount": poi.line_amount,
                "received_quantity": poi.received_quantity,
                "accepted_quantity": poi.accepted_quantity,
                "expected_delivery_date": poi.expected_delivery_date,
                "item_status": poi.item_status,
                "notes": poi.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_purchase_order(
        self,
        order_code: str,
        order_type: str,
        supplier_ref: str,
        procurement_category_ref: str,
        department_ref: str,
        requestor_ref: str,
        buyer_ref: str,
        currency: str,
        total_amount: float,
        tax_rate: float,
        tax_amount: float,
        payment_terms: str,
        delivery_address: str,
        expected_delivery_date: str,
        priority: str = "normal",
        purchase_requisition_ref: Optional[str] = None,
        purchase_contract_ref: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """
        Create a new purchase order. The agent must ask for explicit user confirmation before calling.

        Args:
            order_code: Short code for the purchase order.
            order_type: Type of order (standard, blanket_release, emergency, service).
            supplier_ref: Reference to the supplier.
            procurement_category_ref: Reference to the procurement category.
            department_ref: Reference to the requesting department.
            requestor_ref: Employee ref of the requestor.
            buyer_ref: Employee ref of the buyer.
            currency: Currency code.
            total_amount: Total amount.
            tax_rate: Tax rate as a decimal.
            tax_amount: Calculated tax amount.
            payment_terms: Payment terms.
            delivery_address: Delivery address.
            expected_delivery_date: Expected delivery date (ISO 8601 date).
            priority: Priority level (low, normal, high, urgent). Defaults to normal.
            purchase_requisition_ref: Reference to originating requisition. Defaults to None.
            purchase_contract_ref: Reference to associated contract. Defaults to None.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created purchase order details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_types = {"standard", "blanket_release", "emergency", "service"}
        if order_type not in valid_types:
            raise ValueError(f"Invalid order_type: {order_type}. Must be one of {valid_types}")

        valid_priorities = {"low", "normal", "high", "urgent"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        self._get_supplier(supplier_ref)
        self._get_procurement_category(procurement_category_ref)
        self._get_department(department_ref)
        self._get_employee(requestor_ref)
        self._get_employee(buyer_ref)
        if purchase_requisition_ref is not None:
            self._get_purchase_requisition(purchase_requisition_ref)
        if purchase_contract_ref is not None:
            self._get_purchase_contract(purchase_contract_ref)

        now = self._now_iso()
        ref = self._generate_ref("PO", self.db.purchase_order)
        po = PurchaseOrder(
            purchase_order_ref=ref,
            order_code=order_code,
            order_type=order_type,
            purchase_requisition_ref=purchase_requisition_ref,
            purchase_contract_ref=purchase_contract_ref,
            supplier_ref=supplier_ref,
            procurement_category_ref=procurement_category_ref,
            department_ref=department_ref,
            requestor_ref=requestor_ref,
            buyer_ref=buyer_ref,
            currency=currency,
            total_amount=total_amount,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            payment_terms=payment_terms,
            delivery_address=delivery_address,
            expected_delivery_date=expected_delivery_date,
            priority=priority,
            order_status="draft",
            submitted_at=None,
            approved_at=None,
            sent_to_supplier_at=None,
            supplier_confirmed_at=None,
            completed_at=None,
            cancelled_at=None,
            cancel_reason=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.purchase_order[ref] = po
        return json.dumps({
            "purchase_order_ref": ref,
            "order_code": order_code,
            "order_type": order_type,
            "order_status": "draft",
        })

    @is_tool(ToolType.WRITE)
    def add_purchase_order_item(
        self,
        purchase_order_ref: str,
        item_name: str,
        item_description: str,
        specification: str,
        unit: str,
        quantity: int,
        unit_price: float,
        expected_delivery_date: str,
        contract_item_ref: Optional[str] = None,
        requisition_item_ref: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """
        Add a line item to a purchase order. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_order_ref: The unique identifier of the purchase order.
            item_name: Name of the ordered item.
            item_description: Description of the item.
            specification: Technical specification.
            unit: Unit of measure.
            quantity: Ordered quantity.
            unit_price: Unit price.
            expected_delivery_date: Expected delivery date (ISO 8601 date).
            contract_item_ref: Reference to associated contract item. Defaults to None.
            requisition_item_ref: Reference to associated requisition item. Defaults to None.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created purchase order item details.

        Raises:
            ValueError: If the purchase order is not found or not in draft status.
        """
        po = self._get_purchase_order(purchase_order_ref)
        if po.order_status != "draft":
            raise ValueError(f"Cannot add items when order status is '{po.order_status}'")

        now = self._now_iso()
        ref = self._generate_ref("POI", self.db.purchase_order_item)
        line_amount = round(quantity * unit_price, 2)
        poi = PurchaseOrderItem(
            purchase_order_item_ref=ref,
            purchase_order_ref=purchase_order_ref,
            contract_item_ref=contract_item_ref,
            requisition_item_ref=requisition_item_ref,
            item_name=item_name,
            item_description=item_description,
            specification=specification,
            unit=unit,
            quantity=quantity,
            unit_price=unit_price,
            line_amount=line_amount,
            received_quantity=0,
            accepted_quantity=0,
            expected_delivery_date=expected_delivery_date,
            item_status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.purchase_order_item[ref] = poi
        return json.dumps({
            "purchase_order_item_ref": ref,
            "item_name": item_name,
            "quantity": quantity,
            "line_amount": line_amount,
        })

    @is_tool(ToolType.WRITE)
    def update_purchase_order_status(
        self,
        purchase_order_ref: str,
        new_status: str,
        cancel_reason: Optional[str] = None,
    ) -> str:
        """
        Update the status of a purchase order. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_order_ref: The unique identifier of the purchase order.
            new_status: New order status (submitted, approved, rejected, sent_to_supplier, confirmed, partially_received, completed, cancelled).
            cancel_reason: Reason for cancellation (required if new_status is cancelled).

        Returns:
            str: JSON string containing the updated order status.

        Raises:
            ValueError: If the order is not found, invalid status transition, or missing required fields.
        """
        po = self._get_purchase_order(purchase_order_ref)

        valid_statuses = {
            "draft", "submitted", "approved", "rejected", "sent_to_supplier",
            "confirmed", "partially_received", "completed", "cancelled"
        }
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "draft": {"submitted", "cancelled"},
            "submitted": {"approved", "rejected", "cancelled"},
            "approved": {"sent_to_supplier", "cancelled"},
            "rejected": {"draft"},
            "sent_to_supplier": {"confirmed", "cancelled"},
            "confirmed": {"partially_received", "completed", "cancelled"},
            "partially_received": {"completed", "cancelled"},
            "completed": set(),
            "cancelled": set(),
        }
        if new_status not in valid_transitions.get(po.order_status, set()):
            raise ValueError(f"Cannot transition from '{po.order_status}' to '{new_status}'")

        now = self._now_iso()

        if new_status == "cancelled":
            if not cancel_reason:
                raise ValueError("cancel_reason is required when cancelling an order")
            po.cancel_reason = cancel_reason
            po.cancelled_at = now
        elif new_status == "submitted":
            po.submitted_at = now
        elif new_status == "approved":
            po.approved_at = now
        elif new_status == "sent_to_supplier":
            po.sent_to_supplier_at = now
        elif new_status == "confirmed":
            po.supplier_confirmed_at = now
        elif new_status == "completed":
            po.completed_at = now

        po.order_status = new_status
        po.updated_at = now
        return json.dumps({
            "purchase_order_ref": po.purchase_order_ref,
            "order_status": po.order_status,
        })

    # =========================================================================
    # Purchase Change Request (采购变更管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_purchase_change_request_details(self, purchase_change_request_ref: str) -> str:
        """
        Get detailed information about a specific purchase change request.

        Args:
            purchase_change_request_ref: The unique identifier of the purchase change request.

        Returns:
            str: JSON string containing the purchase change request details.

        Raises:
            ValueError: If the purchase change request is not found.
        """
        cr = self._get_purchase_change_request(purchase_change_request_ref)
        return json.dumps({
            "purchase_change_request_ref": cr.purchase_change_request_ref,
            "change_code": cr.change_code,
            "change_target_type": cr.change_target_type,
            "change_target_ref": cr.change_target_ref,
            "change_type": cr.change_type,
            "change_reason": cr.change_reason,
            "change_details": cr.change_details,
            "impact_amount": cr.impact_amount,
            "requestor_ref": cr.requestor_ref,
            "change_status": cr.change_status,
            "approved_at": cr.approved_at,
            "rejected_reason": cr.rejected_reason,
            "executed_at": cr.executed_at,
            "created_at": cr.created_at,
            "updated_at": cr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_purchase_change_requests(
        self,
        change_target_type: Optional[str] = None,
        change_target_ref: Optional[str] = None,
        change_status: Optional[str] = None,
        requestor_ref: Optional[str] = None,
        change_type: Optional[str] = None,
    ) -> str:
        """
        List purchase change requests with optional filters.

        Args:
            change_target_type: Filter by target type (purchase_order, purchase_contract). None returns all.
            change_target_ref: Filter by target ref. None returns all.
            change_status: Filter by change status. None returns all.
            requestor_ref: Filter by requestor. None returns all.
            change_type: Filter by change type. None returns all.

        Returns:
            str: JSON string containing a list of matching purchase change requests.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, cr in self.db.purchase_change_request.items():
            if change_target_type is not None and cr.change_target_type != change_target_type:
                continue
            if change_target_ref is not None and cr.change_target_ref != change_target_ref:
                continue
            if change_status is not None and cr.change_status != change_status:
                continue
            if requestor_ref is not None and cr.requestor_ref != requestor_ref:
                continue
            if change_type is not None and cr.change_type != change_type:
                continue
            results.append({
                "purchase_change_request_ref": cr.purchase_change_request_ref,
                "change_code": cr.change_code,
                "change_target_type": cr.change_target_type,
                "change_target_ref": cr.change_target_ref,
                "change_type": cr.change_type,
                "impact_amount": cr.impact_amount,
                "change_status": cr.change_status,
                "requestor_ref": cr.requestor_ref,
                "created_at": cr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_purchase_change_request(
        self,
        change_code: str,
        change_target_type: str,
        change_target_ref: str,
        change_type: str,
        change_reason: str,
        change_details: Dict[str, Any],
        impact_amount: float,
        requestor_ref: str,
    ) -> str:
        """
        Create a new purchase change request. The agent must ask for explicit user confirmation before calling.

        Args:
            change_code: Short code for the change request.
            change_target_type: Type of target (purchase_order, purchase_contract).
            change_target_ref: Reference to the target being changed.
            change_type: Type of change (quantity_adjustment, price_adjustment, delivery_date_change, item_addition, item_removal, cancellation, other).
            change_reason: Reason for the change.
            change_details: Dictionary of field changes with before/after values.
            impact_amount: Financial impact amount.
            requestor_ref: Employee ref of the requestor.

        Returns:
            str: JSON string containing the created change request details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_target_types = {"purchase_order", "purchase_contract"}
        if change_target_type not in valid_target_types:
            raise ValueError(f"Invalid change_target_type: {change_target_type}. Must be one of {valid_target_types}")

        valid_change_types = {"quantity_adjustment", "price_adjustment", "delivery_date_change", "item_addition", "item_removal", "cancellation", "other"}
        if change_type not in valid_change_types:
            raise ValueError(f"Invalid change_type: {change_type}. Must be one of {valid_change_types}")

        # Validate target exists
        if change_target_type == "purchase_order":
            self._get_purchase_order(change_target_ref)
        elif change_target_type == "purchase_contract":
            self._get_purchase_contract(change_target_ref)

        self._get_employee(requestor_ref)

        now = self._now_iso()
        ref = self._generate_ref("PCR", self.db.purchase_change_request)
        cr = PurchaseChangeRequest(
            purchase_change_request_ref=ref,
            change_code=change_code,
            change_target_type=change_target_type,
            change_target_ref=change_target_ref,
            change_type=change_type,
            change_reason=change_reason,
            change_details=change_details,
            impact_amount=impact_amount,
            requestor_ref=requestor_ref,
            change_status="pending",
            approved_at=None,
            rejected_reason=None,
            executed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.purchase_change_request[ref] = cr
        return json.dumps({
            "purchase_change_request_ref": ref,
            "change_code": change_code,
            "change_type": change_type,
            "change_status": "pending",
        })

    @is_tool(ToolType.WRITE)
    def approve_purchase_change_request(self, purchase_change_request_ref: str) -> str:
        """
        Approve a pending purchase change request. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_change_request_ref: The unique identifier of the purchase change request.

        Returns:
            str: JSON string containing the updated change request status.

        Raises:
            ValueError: If the change request is not found or not in pending status.
        """
        cr = self._get_purchase_change_request(purchase_change_request_ref)
        if cr.change_status != "pending":
            raise ValueError(f"Change request status is '{cr.change_status}', expected 'pending'")

        now = self._now_iso()
        cr.change_status = "approved"
        cr.approved_at = now
        cr.updated_at = now
        return json.dumps({
            "purchase_change_request_ref": cr.purchase_change_request_ref,
            "change_status": cr.change_status,
            "approved_at": cr.approved_at,
        })

    @is_tool(ToolType.WRITE)
    def reject_purchase_change_request(self, purchase_change_request_ref: str, reason: str) -> str:
        """
        Reject a pending purchase change request. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_change_request_ref: The unique identifier of the purchase change request.
            reason: Reason for rejection.

        Returns:
            str: JSON string containing the updated change request status.

        Raises:
            ValueError: If the change request is not found or not in pending status.
        """
        cr = self._get_purchase_change_request(purchase_change_request_ref)
        if cr.change_status != "pending":
            raise ValueError(f"Change request status is '{cr.change_status}', expected 'pending'")

        cr.change_status = "rejected"
        cr.rejected_reason = reason
        cr.updated_at = self._now_iso()
        return json.dumps({
            "purchase_change_request_ref": cr.purchase_change_request_ref,
            "change_status": cr.change_status,
            "rejected_reason": cr.rejected_reason,
        })

    @is_tool(ToolType.WRITE)
    def execute_purchase_change_request(self, purchase_change_request_ref: str) -> str:
        """
        Execute an approved purchase change request. The agent must ask for explicit user confirmation before calling.

        Args:
            purchase_change_request_ref: The unique identifier of the purchase change request.

        Returns:
            str: JSON string containing the updated change request status.

        Raises:
            ValueError: If the change request is not found or not in approved status.
        """
        cr = self._get_purchase_change_request(purchase_change_request_ref)
        if cr.change_status != "approved":
            raise ValueError(f"Change request status is '{cr.change_status}', expected 'approved'")

        now = self._now_iso()
        cr.change_status = "executed"
        cr.executed_at = now
        cr.updated_at = now
        return json.dumps({
            "purchase_change_request_ref": cr.purchase_change_request_ref,
            "change_status": cr.change_status,
            "executed_at": cr.executed_at,
        })

    # =========================================================================
    # Goods Receipt (收货与验收)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_goods_receipt_details(self, goods_receipt_ref: str) -> str:
        """
        Get detailed information about a specific goods receipt.

        Args:
            goods_receipt_ref: The unique identifier of the goods receipt.

        Returns:
            str: JSON string containing the goods receipt details.

        Raises:
            ValueError: If the goods receipt is not found.
        """
        gr = self._get_goods_receipt(goods_receipt_ref)
        return json.dumps({
            "goods_receipt_ref": gr.goods_receipt_ref,
            "receipt_code": gr.receipt_code,
            "purchase_order_ref": gr.purchase_order_ref,
            "supplier_ref": gr.supplier_ref,
            "receiver_ref": gr.receiver_ref,
            "receipt_date": gr.receipt_date,
            "delivery_note_number": gr.delivery_note_number,
            "warehouse_location": gr.warehouse_location,
            "receipt_status": gr.receipt_status,
            "notes": gr.notes,
            "created_at": gr.created_at,
            "updated_at": gr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_goods_receipts(
        self,
        purchase_order_ref: Optional[str] = None,
        supplier_ref: Optional[str] = None,
        receipt_status: Optional[str] = None,
        receiver_ref: Optional[str] = None,
    ) -> str:
        """
        List goods receipts with optional filters.

        Args:
            purchase_order_ref: Filter by purchase order. None returns all.
            supplier_ref: Filter by supplier. None returns all.
            receipt_status: Filter by receipt status. None returns all.
            receiver_ref: Filter by receiver employee. None returns all.

        Returns:
            str: JSON string containing a list of matching goods receipts.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, gr in self.db.goods_receipt.items():
            if purchase_order_ref is not None and gr.purchase_order_ref != purchase_order_ref:
                continue
            if supplier_ref is not None and gr.supplier_ref != supplier_ref:
                continue
            if receipt_status is not None and gr.receipt_status != receipt_status:
                continue
            if receiver_ref is not None and gr.receiver_ref != receiver_ref:
                continue
            results.append({
                "goods_receipt_ref": gr.goods_receipt_ref,
                "receipt_code": gr.receipt_code,
                "purchase_order_ref": gr.purchase_order_ref,
                "supplier_ref": gr.supplier_ref,
                "receipt_date": gr.receipt_date,
                "receipt_status": gr.receipt_status,
                "warehouse_location": gr.warehouse_location,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_goods_receipt_items(self, goods_receipt_ref: str) -> str:
        """
        List line items for a specific goods receipt.

        Args:
            goods_receipt_ref: The unique identifier of the goods receipt.

        Returns:
            str: JSON string containing a list of goods receipt items.

        Raises:
            ValueError: If the goods receipt is not found.
        """
        self._get_goods_receipt(goods_receipt_ref)
        results = []
        for gri in self.db.goods_receipt_item.values():
            if gri.goods_receipt_ref != goods_receipt_ref:
                continue
            results.append({
                "goods_receipt_item_ref": gri.goods_receipt_item_ref,
                "purchase_order_item_ref": gri.purchase_order_item_ref,
                "item_name": gri.item_name,
                "received_quantity": gri.received_quantity,
                "rejected_quantity": gri.rejected_quantity,
                "unit": gri.unit,
                "item_condition": gri.item_condition,
                "notes": gri.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_goods_receipt(
        self,
        receipt_code: str,
        purchase_order_ref: str,
        supplier_ref: str,
        receiver_ref: str,
        receipt_date: str,
        delivery_note_number: str,
        warehouse_location: str,
        notes: str = "",
    ) -> str:
        """
        Create a new goods receipt. The agent must ask for explicit user confirmation before calling.

        Args:
            receipt_code: Short code for the goods receipt.
            purchase_order_ref: Reference to the associated purchase order.
            supplier_ref: Reference to the supplier.
            receiver_ref: Employee ref of the receiver.
            receipt_date: Date goods were received (ISO 8601 date).
            delivery_note_number: Delivery note number.
            warehouse_location: Warehouse location.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created goods receipt details.

        Raises:
            ValueError: If required references are not found.
        """
        self._get_purchase_order(purchase_order_ref)
        self._get_supplier(supplier_ref)
        self._get_employee(receiver_ref)

        now = self._now_iso()
        ref = self._generate_ref("GR", self.db.goods_receipt)
        gr = GoodsReceipt(
            goods_receipt_ref=ref,
            receipt_code=receipt_code,
            purchase_order_ref=purchase_order_ref,
            supplier_ref=supplier_ref,
            receiver_ref=receiver_ref,
            receipt_date=receipt_date,
            delivery_note_number=delivery_note_number,
            warehouse_location=warehouse_location,
            receipt_status="pending_inspection",
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.goods_receipt[ref] = gr
        return json.dumps({
            "goods_receipt_ref": ref,
            "receipt_code": receipt_code,
            "receipt_status": "pending_inspection",
        })

    @is_tool(ToolType.WRITE)
    def add_goods_receipt_item(
        self,
        goods_receipt_ref: str,
        purchase_order_item_ref: str,
        item_name: str,
        received_quantity: int,
        rejected_quantity: int,
        unit: str,
        item_condition: str,
        notes: str = "",
    ) -> str:
        """
        Add a line item to a goods receipt. The agent must ask for explicit user confirmation before calling.

        Args:
            goods_receipt_ref: The unique identifier of the goods receipt.
            purchase_order_item_ref: Reference to the associated purchase order item.
            item_name: Name of the received item.
            received_quantity: Quantity received.
            rejected_quantity: Quantity rejected.
            unit: Unit of measure.
            item_condition: Condition of the item (good, damaged, defective, wrong_item).
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created goods receipt item details.

        Raises:
            ValueError: If the goods receipt is not found or invalid item condition.
        """
        self._get_goods_receipt(goods_receipt_ref)

        valid_conditions = {"good", "damaged", "defective", "wrong_item"}
        if item_condition not in valid_conditions:
            raise ValueError(f"Invalid item_condition: {item_condition}. Must be one of {valid_conditions}")

        now = self._now_iso()
        ref = self._generate_ref("GRI", self.db.goods_receipt_item)
        gri = GoodsReceiptItem(
            goods_receipt_item_ref=ref,
            goods_receipt_ref=goods_receipt_ref,
            purchase_order_item_ref=purchase_order_item_ref,
            item_name=item_name,
            received_quantity=received_quantity,
            rejected_quantity=rejected_quantity,
            unit=unit,
            item_condition=item_condition,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.goods_receipt_item[ref] = gri
        return json.dumps({
            "goods_receipt_item_ref": ref,
            "item_name": item_name,
            "received_quantity": received_quantity,
            "item_condition": item_condition,
        })

    @is_tool(ToolType.WRITE)
    def update_goods_receipt_status(
        self,
        goods_receipt_ref: str,
        new_status: str,
    ) -> str:
        """
        Update the status of a goods receipt. The agent must ask for explicit user confirmation before calling.

        Args:
            goods_receipt_ref: The unique identifier of the goods receipt.
            new_status: New receipt status (inspected, accepted, partially_accepted, rejected, completed).

        Returns:
            str: JSON string containing the updated goods receipt status.

        Raises:
            ValueError: If the goods receipt is not found or invalid status transition.
        """
        gr = self._get_goods_receipt(goods_receipt_ref)

        valid_statuses = {"pending_inspection", "inspected", "accepted", "partially_accepted", "rejected", "completed"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "pending_inspection": {"inspected"},
            "inspected": {"accepted", "partially_accepted", "rejected"},
            "accepted": {"completed"},
            "partially_accepted": {"completed"},
            "rejected": set(),
            "completed": set(),
        }
        if new_status not in valid_transitions.get(gr.receipt_status, set()):
            raise ValueError(f"Cannot transition from '{gr.receipt_status}' to '{new_status}'")

        gr.receipt_status = new_status
        gr.updated_at = self._now_iso()
        return json.dumps({
            "goods_receipt_ref": gr.goods_receipt_ref,
            "receipt_status": gr.receipt_status,
        })

    # =========================================================================
    # Acceptance Record (收货与验收)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_acceptance_record_details(self, acceptance_record_ref: str) -> str:
        """
        Get detailed information about a specific acceptance record.

        Args:
            acceptance_record_ref: The unique identifier of the acceptance record.

        Returns:
            str: JSON string containing the acceptance record details.

        Raises:
            ValueError: If the acceptance record is not found.
        """
        ar = self._get_acceptance_record(acceptance_record_ref)
        return json.dumps({
            "acceptance_record_ref": ar.acceptance_record_ref,
            "acceptance_code": ar.acceptance_code,
            "goods_receipt_ref": ar.goods_receipt_ref,
            "purchase_order_ref": ar.purchase_order_ref,
            "inspector_ref": ar.inspector_ref,
            "inspection_date": ar.inspection_date,
            "inspection_type": ar.inspection_type,
            "overall_result": ar.overall_result,
            "accepted_quantity": ar.accepted_quantity,
            "rejected_quantity": ar.rejected_quantity,
            "defect_description": ar.defect_description,
            "corrective_action": ar.corrective_action,
            "acceptance_status": ar.acceptance_status,
            "notes": ar.notes,
            "created_at": ar.created_at,
            "updated_at": ar.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_acceptance_records(
        self,
        goods_receipt_ref: Optional[str] = None,
        purchase_order_ref: Optional[str] = None,
        acceptance_status: Optional[str] = None,
        overall_result: Optional[str] = None,
        inspector_ref: Optional[str] = None,
    ) -> str:
        """
        List acceptance records with optional filters.

        Args:
            goods_receipt_ref: Filter by goods receipt. None returns all.
            purchase_order_ref: Filter by purchase order. None returns all.
            acceptance_status: Filter by acceptance status. None returns all.
            overall_result: Filter by overall result. None returns all.
            inspector_ref: Filter by inspector employee. None returns all.

        Returns:
            str: JSON string containing a list of matching acceptance records.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, ar in self.db.acceptance_record.items():
            if goods_receipt_ref is not None and ar.goods_receipt_ref != goods_receipt_ref:
                continue
            if purchase_order_ref is not None and ar.purchase_order_ref != purchase_order_ref:
                continue
            if acceptance_status is not None and ar.acceptance_status != acceptance_status:
                continue
            if overall_result is not None and ar.overall_result != overall_result:
                continue
            if inspector_ref is not None and ar.inspector_ref != inspector_ref:
                continue
            results.append({
                "acceptance_record_ref": ar.acceptance_record_ref,
                "acceptance_code": ar.acceptance_code,
                "goods_receipt_ref": ar.goods_receipt_ref,
                "purchase_order_ref": ar.purchase_order_ref,
                "inspection_type": ar.inspection_type,
                "overall_result": ar.overall_result,
                "accepted_quantity": ar.accepted_quantity,
                "rejected_quantity": ar.rejected_quantity,
                "acceptance_status": ar.acceptance_status,
                "inspection_date": ar.inspection_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_acceptance_items(self, acceptance_record_ref: str) -> str:
        """
        List line items for a specific acceptance record.

        Args:
            acceptance_record_ref: The unique identifier of the acceptance record.

        Returns:
            str: JSON string containing a list of acceptance items.

        Raises:
            ValueError: If the acceptance record is not found.
        """
        self._get_acceptance_record(acceptance_record_ref)
        results = []
        for ai in self.db.acceptance_item.values():
            if ai.acceptance_record_ref != acceptance_record_ref:
                continue
            results.append({
                "acceptance_item_ref": ai.acceptance_item_ref,
                "goods_receipt_item_ref": ai.goods_receipt_item_ref,
                "item_name": ai.item_name,
                "inspected_quantity": ai.inspected_quantity,
                "accepted_quantity": ai.accepted_quantity,
                "rejected_quantity": ai.rejected_quantity,
                "result": ai.result,
                "defect_description": ai.defect_description,
                "notes": ai.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_acceptance_record(
        self,
        acceptance_code: str,
        goods_receipt_ref: str,
        purchase_order_ref: str,
        inspector_ref: str,
        inspection_date: str,
        inspection_type: str,
        overall_result: str,
        accepted_quantity: int,
        rejected_quantity: int,
        defect_description: Optional[str] = None,
        corrective_action: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """
        Create a new acceptance record. The agent must ask for explicit user confirmation before calling.

        Args:
            acceptance_code: Short code for the acceptance record.
            goods_receipt_ref: Reference to the associated goods receipt.
            purchase_order_ref: Reference to the associated purchase order.
            inspector_ref: Employee ref of the inspector.
            inspection_date: Date of inspection (ISO 8601 date).
            inspection_type: Type of inspection (full, sampling, visual, functional, skip).
            overall_result: Overall result (accepted, partially_accepted, rejected, conditional).
            accepted_quantity: Total quantity accepted.
            rejected_quantity: Total quantity rejected.
            defect_description: Description of defects. Defaults to None.
            corrective_action: Corrective action required. Defaults to None.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created acceptance record details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        self._get_goods_receipt(goods_receipt_ref)
        self._get_purchase_order(purchase_order_ref)
        self._get_employee(inspector_ref)

        valid_inspection_types = {"full", "sampling", "visual", "functional", "skip"}
        if inspection_type not in valid_inspection_types:
            raise ValueError(f"Invalid inspection_type: {inspection_type}. Must be one of {valid_inspection_types}")

        valid_results = {"accepted", "partially_accepted", "rejected", "conditional"}
        if overall_result not in valid_results:
            raise ValueError(f"Invalid overall_result: {overall_result}. Must be one of {valid_results}")

        now = self._now_iso()
        ref = self._generate_ref("AR", self.db.acceptance_record)
        ar = AcceptanceRecord(
            acceptance_record_ref=ref,
            acceptance_code=acceptance_code,
            goods_receipt_ref=goods_receipt_ref,
            purchase_order_ref=purchase_order_ref,
            inspector_ref=inspector_ref,
            inspection_date=inspection_date,
            inspection_type=inspection_type,
            overall_result=overall_result,
            accepted_quantity=accepted_quantity,
            rejected_quantity=rejected_quantity,
            defect_description=defect_description,
            corrective_action=corrective_action,
            acceptance_report_file_ref=None,
            acceptance_status="pending",
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.acceptance_record[ref] = ar
        return json.dumps({
            "acceptance_record_ref": ref,
            "acceptance_code": acceptance_code,
            "overall_result": overall_result,
            "acceptance_status": "pending",
        })

    @is_tool(ToolType.WRITE)
    def add_acceptance_item(
        self,
        acceptance_record_ref: str,
        goods_receipt_item_ref: str,
        item_name: str,
        inspected_quantity: int,
        accepted_quantity: int,
        rejected_quantity: int,
        result: str,
        defect_description: Optional[str] = None,
        notes: str = "",
    ) -> str:
        """
        Add a line item to an acceptance record. The agent must ask for explicit user confirmation before calling.

        Args:
            acceptance_record_ref: The unique identifier of the acceptance record.
            goods_receipt_item_ref: Reference to the associated goods receipt item.
            item_name: Name of the inspected item.
            inspected_quantity: Quantity inspected.
            accepted_quantity: Quantity accepted.
            rejected_quantity: Quantity rejected.
            result: Inspection result (accepted, rejected, conditional).
            defect_description: Description of defects. Defaults to None.
            notes: Additional notes. Defaults to empty string.

        Returns:
            str: JSON string containing the created acceptance item details.

        Raises:
            ValueError: If the acceptance record is not found or invalid result.
        """
        self._get_acceptance_record(acceptance_record_ref)

        valid_results = {"accepted", "rejected", "conditional"}
        if result not in valid_results:
            raise ValueError(f"Invalid result: {result}. Must be one of {valid_results}")

        now = self._now_iso()
        ref = self._generate_ref("AI", self.db.acceptance_item)
        ai = AcceptanceItem(
            acceptance_item_ref=ref,
            acceptance_record_ref=acceptance_record_ref,
            goods_receipt_item_ref=goods_receipt_item_ref,
            item_name=item_name,
            inspected_quantity=inspected_quantity,
            accepted_quantity=accepted_quantity,
            rejected_quantity=rejected_quantity,
            result=result,
            defect_description=defect_description,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.acceptance_item[ref] = ai
        return json.dumps({
            "acceptance_item_ref": ref,
            "item_name": item_name,
            "result": result,
            "accepted_quantity": accepted_quantity,
        })

    @is_tool(ToolType.WRITE)
    def update_acceptance_record_status(
        self,
        acceptance_record_ref: str,
        new_status: str,
    ) -> str:
        """
        Update the status of an acceptance record. The agent must ask for explicit user confirmation before calling.

        Args:
            acceptance_record_ref: The unique identifier of the acceptance record.
            new_status: New acceptance status (in_progress, completed, cancelled).

        Returns:
            str: JSON string containing the updated acceptance record status.

        Raises:
            ValueError: If the acceptance record is not found or invalid status transition.
        """
        ar = self._get_acceptance_record(acceptance_record_ref)

        valid_statuses = {"pending", "in_progress", "completed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "pending": {"in_progress", "cancelled"},
            "in_progress": {"completed", "cancelled"},
            "completed": set(),
            "cancelled": set(),
        }
        if new_status not in valid_transitions.get(ar.acceptance_status, set()):
            raise ValueError(f"Cannot transition from '{ar.acceptance_status}' to '{new_status}'")

        ar.acceptance_status = new_status
        ar.updated_at = self._now_iso()
        return json.dumps({
            "acceptance_record_ref": ar.acceptance_record_ref,
            "acceptance_status": ar.acceptance_status,
        })

    # =========================================================================
    # Approval Flow (采购审批流程管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_approval_flow_template_details(self, approval_flow_template_ref: str) -> str:
        """
        Get detailed information about a specific approval flow template.

        Args:
            approval_flow_template_ref: The unique identifier of the approval flow template.

        Returns:
            str: JSON string containing the approval flow template details.

        Raises:
            ValueError: If the approval flow template is not found.
        """
        aft = self._get_approval_flow_template(approval_flow_template_ref)
        return json.dumps({
            "approval_flow_template_ref": aft.approval_flow_template_ref,
            "template_name": aft.template_name,
            "template_code": aft.template_code,
            "applicable_type": aft.applicable_type,
            "condition_rules": aft.condition_rules,
            "priority": aft.priority,
            "template_status": aft.template_status,
            "description": aft.description,
            "created_by_ref": aft.created_by_ref,
            "created_at": aft.created_at,
            "updated_at": aft.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_approval_flow_templates(
        self,
        applicable_type: Optional[str] = None,
        template_status: Optional[str] = None,
    ) -> str:
        """
        List approval flow templates with optional filters.

        Args:
            applicable_type: Filter by applicable type. None returns all.
            template_status: Filter by template status (active, inactive, deprecated). None returns all.

        Returns:
            str: JSON string containing a list of matching approval flow templates.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, aft in self.db.approval_flow_template.items():
            if applicable_type is not None and aft.applicable_type != applicable_type:
                continue
            if template_status is not None and aft.template_status != template_status:
                continue
            results.append({
                "approval_flow_template_ref": aft.approval_flow_template_ref,
                "template_name": aft.template_name,
                "template_code": aft.template_code,
                "applicable_type": aft.applicable_type,
                "priority": aft.priority,
                "template_status": aft.template_status,
                "description": aft.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_approval_flow_nodes(self, approval_flow_template_ref: str) -> str:
        """
        List nodes (steps) for a specific approval flow template, ordered by sequence.

        Args:
            approval_flow_template_ref: The unique identifier of the approval flow template.

        Returns:
            str: JSON string containing a list of approval flow nodes.

        Raises:
            ValueError: If the approval flow template is not found.
        """
        self._get_approval_flow_template(approval_flow_template_ref)
        results = []
        for afn in self.db.approval_flow_node.values():
            if afn.approval_flow_template_ref != approval_flow_template_ref:
                continue
            results.append({
                "approval_flow_node_ref": afn.approval_flow_node_ref,
                "node_sequence": afn.node_sequence,
                "node_name": afn.node_name,
                "approver_type": afn.approver_type,
                "approver_ref": afn.approver_ref,
                "fallback_approver_ref": afn.fallback_approver_ref,
                "auto_approve_hours": afn.auto_approve_hours,
            })
        results.sort(key=lambda x: x["node_sequence"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_approval_instance_details(self, approval_instance_ref: str) -> str:
        """
        Get detailed information about a specific approval instance.

        Args:
            approval_instance_ref: The unique identifier of the approval instance.

        Returns:
            str: JSON string containing the approval instance details.

        Raises:
            ValueError: If the approval instance is not found.
        """
        ai = self._get_approval_instance(approval_instance_ref)
        return json.dumps({
            "approval_instance_ref": ai.approval_instance_ref,
            "approval_flow_template_ref": ai.approval_flow_template_ref,
            "target_type": ai.target_type,
            "target_ref": ai.target_ref,
            "initiator_ref": ai.initiator_ref,
            "current_node_sequence": ai.current_node_sequence,
            "approval_status": ai.approval_status,
            "submitted_at": ai.submitted_at,
            "completed_at": ai.completed_at,
            "created_at": ai.created_at,
            "updated_at": ai.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_approval_instances(
        self,
        target_type: Optional[str] = None,
        target_ref: Optional[str] = None,
        approval_status: Optional[str] = None,
        initiator_ref: Optional[str] = None,
    ) -> str:
        """
        List approval instances with optional filters.

        Args:
            target_type: Filter by target type. None returns all.
            target_ref: Filter by target ref. None returns all.
            approval_status: Filter by approval status. None returns all.
            initiator_ref: Filter by initiator employee. None returns all.

        Returns:
            str: JSON string containing a list of matching approval instances.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, ai in self.db.approval_instance.items():
            if target_type is not None and ai.target_type != target_type:
                continue
            if target_ref is not None and ai.target_ref != target_ref:
                continue
            if approval_status is not None and ai.approval_status != approval_status:
                continue
            if initiator_ref is not None and ai.initiator_ref != initiator_ref:
                continue
            results.append({
                "approval_instance_ref": ai.approval_instance_ref,
                "approval_flow_template_ref": ai.approval_flow_template_ref,
                "target_type": ai.target_type,
                "target_ref": ai.target_ref,
                "initiator_ref": ai.initiator_ref,
                "current_node_sequence": ai.current_node_sequence,
                "approval_status": ai.approval_status,
                "submitted_at": ai.submitted_at,
                "completed_at": ai.completed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_approval_actions(self, approval_instance_ref: str) -> str:
        """
        List actions taken within a specific approval instance, ordered by acted_at.

        Args:
            approval_instance_ref: The unique identifier of the approval instance.

        Returns:
            str: JSON string containing a list of approval actions.

        Raises:
            ValueError: If the approval instance is not found.
        """
        self._get_approval_instance(approval_instance_ref)
        results = []
        for aa in self.db.approval_action.values():
            if aa.approval_instance_ref != approval_instance_ref:
                continue
            results.append({
                "approval_action_ref": aa.approval_action_ref,
                "node_sequence": aa.node_sequence,
                "approver_ref": aa.approver_ref,
                "action": aa.action,
                "comments": aa.comments,
                "acted_at": aa.acted_at,
            })
        results.sort(key=lambda x: x["acted_at"])
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_approval_instance(
        self,
        approval_flow_template_ref: str,
        target_type: str,
        target_ref: str,
        initiator_ref: str,
    ) -> str:
        """
        Create a new approval instance to start an approval flow. The agent must ask for explicit user confirmation before calling.

        Args:
            approval_flow_template_ref: Reference to the approval flow template.
            target_type: Type of entity being approved (e.g., purchase_requisition, purchase_order).
            target_ref: Reference to the entity being approved.
            initiator_ref: Employee ref of the person initiating the approval.

        Returns:
            str: JSON string containing the created approval instance details.

        Raises:
            ValueError: If required references are not found.
        """
        self._get_approval_flow_template(approval_flow_template_ref)
        self._get_employee(initiator_ref)

        now = self._now_iso()
        ref = self._generate_ref("APRI", self.db.approval_instance)
        ai = ApprovalInstance(
            approval_instance_ref=ref,
            approval_flow_template_ref=approval_flow_template_ref,
            target_type=target_type,
            target_ref=target_ref,
            initiator_ref=initiator_ref,
            current_node_sequence=1,
            approval_status="in_progress",
            submitted_at=now,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.approval_instance[ref] = ai
        return json.dumps({
            "approval_instance_ref": ref,
            "target_type": target_type,
            "target_ref": target_ref,
            "approval_status": "in_progress",
        })

    @is_tool(ToolType.WRITE)
    def take_approval_action(
        self,
        approval_instance_ref: str,
        approver_ref: str,
        action: str,
        comments: str = "",
    ) -> str:
        """
        Take an action on an approval instance (approve, reject, return, delegate, comment). The agent must ask for explicit user confirmation before calling.

        Args:
            approval_instance_ref: The unique identifier of the approval instance.
            approver_ref: Employee ref of the approver taking the action.
            action: Action to take (approve, reject, return, delegate, comment).
            comments: Comments from the approver. Defaults to empty string.

        Returns:
            str: JSON string containing the result of the approval action.

        Raises:
            ValueError: If the instance is not found, not in progress, or invalid action.
        """
        ai = self._get_approval_instance(approval_instance_ref)
        self._get_employee(approver_ref)

        if ai.approval_status != "in_progress":
            raise ValueError(f"Approval instance status is '{ai.approval_status}', expected 'in_progress'")

        valid_actions = {"approve", "reject", "return", "delegate", "comment"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}")

        now = self._now_iso()
        action_ref = self._generate_ref("AA", self.db.approval_action)
        aa = ApprovalAction(
            approval_action_ref=action_ref,
            approval_instance_ref=approval_instance_ref,
            node_sequence=ai.current_node_sequence,
            approver_ref=approver_ref,
            action=action,
            comments=comments,
            acted_at=now,
            created_at=now,
        )
        self.db.approval_action[action_ref] = aa

        # Update instance based on action
        if action == "approve":
            # Check if there are more nodes
            max_sequence = 0
            for afn in self.db.approval_flow_node.values():
                if afn.approval_flow_template_ref == ai.approval_flow_template_ref:
                    max_sequence = max(max_sequence, afn.node_sequence)

            if ai.current_node_sequence >= max_sequence:
                ai.approval_status = "approved"
                ai.completed_at = now
            else:
                ai.current_node_sequence += 1
        elif action == "reject":
            ai.approval_status = "rejected"
            ai.completed_at = now
        elif action == "return":
            if ai.current_node_sequence > 1:
                ai.current_node_sequence -= 1

        ai.updated_at = now
        return json.dumps({
            "approval_action_ref": action_ref,
            "approval_instance_ref": approval_instance_ref,
            "action": action,
            "approval_status": ai.approval_status,
            "current_node_sequence": ai.current_node_sequence,
        })

    @is_tool(ToolType.WRITE)
    def cancel_approval_instance(self, approval_instance_ref: str) -> str:
        """
        Cancel an in-progress approval instance. The agent must ask for explicit user confirmation before calling.

        Args:
            approval_instance_ref: The unique identifier of the approval instance.

        Returns:
            str: JSON string containing the updated approval instance status.

        Raises:
            ValueError: If the instance is not found or not in progress.
        """
        ai = self._get_approval_instance(approval_instance_ref)
        if ai.approval_status != "in_progress":
            raise ValueError(f"Approval instance status is '{ai.approval_status}', expected 'in_progress'")

        now = self._now_iso()
        ai.approval_status = "cancelled"
        ai.completed_at = now
        ai.updated_at = now
        return json.dumps({
            "approval_instance_ref": ai.approval_instance_ref,
            "approval_status": ai.approval_status,
        })

    # =========================================================================
    # Procurement Permission Rules (采购权限管理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_permission_rule_details(self, procurement_permission_rule_ref: str) -> str:
        """
        Get detailed information about a specific procurement permission rule.

        Args:
            procurement_permission_rule_ref: The unique identifier of the procurement permission rule.

        Returns:
            str: JSON string containing the procurement permission rule details.

        Raises:
            ValueError: If the procurement permission rule is not found.
        """
        ppr = self._get_procurement_permission_rule(procurement_permission_rule_ref)
        return json.dumps({
            "procurement_permission_rule_ref": ppr.procurement_permission_rule_ref,
            "rule_name": ppr.rule_name,
            "rule_code": ppr.rule_code,
            "employee_ref": ppr.employee_ref,
            "role_ref": ppr.role_ref,
            "department_ref": ppr.department_ref,
            "procurement_category_ref": ppr.procurement_category_ref,
            "max_single_amount": ppr.max_single_amount,
            "max_monthly_amount": ppr.max_monthly_amount,
            "currency": ppr.currency,
            "allowed_operations": ppr.allowed_operations,
            "rule_status": ppr.rule_status,
            "created_by_ref": ppr.created_by_ref,
            "created_at": ppr.created_at,
            "updated_at": ppr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_procurement_permission_rules(
        self,
        employee_ref: Optional[str] = None,
        role_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        rule_status: Optional[str] = None,
    ) -> str:
        """
        List procurement permission rules with optional filters.

        Args:
            employee_ref: Filter by employee. None returns all.
            role_ref: Filter by role. None returns all.
            department_ref: Filter by department. None returns all.
            rule_status: Filter by rule status (active, inactive, expired). None returns all.

        Returns:
            str: JSON string containing a list of matching procurement permission rules.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, ppr in self.db.procurement_permission_rule.items():
            if employee_ref is not None and ppr.employee_ref != employee_ref:
                continue
            if role_ref is not None and ppr.role_ref != role_ref:
                continue
            if department_ref is not None and ppr.department_ref != department_ref:
                continue
            if rule_status is not None and ppr.rule_status != rule_status:
                continue
            results.append({
                "procurement_permission_rule_ref": ppr.procurement_permission_rule_ref,
                "rule_name": ppr.rule_name,
                "rule_code": ppr.rule_code,
                "employee_ref": ppr.employee_ref,
                "role_ref": ppr.role_ref,
                "department_ref": ppr.department_ref,
                "max_single_amount": ppr.max_single_amount,
                "max_monthly_amount": ppr.max_monthly_amount,
                "currency": ppr.currency,
                "allowed_operations": ppr.allowed_operations,
                "rule_status": ppr.rule_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_procurement_permission_rule(
        self,
        rule_name: str,
        rule_code: str,
        currency: str,
        allowed_operations: List[str],
        created_by_ref: str,
        employee_ref: Optional[str] = None,
        role_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        procurement_category_ref: Optional[str] = None,
        max_single_amount: Optional[float] = None,
        max_monthly_amount: Optional[float] = None,
    ) -> str:
        """
        Create a new procurement permission rule. The agent must ask for explicit user confirmation before calling.

        Args:
            rule_name: Name of the permission rule.
            rule_code: Short code for the rule.
            currency: Currency code for amount limits.
            allowed_operations: List of allowed operations.
            created_by_ref: Employee ref of the rule creator.
            employee_ref: Reference to a specific employee. Defaults to None.
            role_ref: Reference to a role. Defaults to None.
            department_ref: Reference to a department. Defaults to None.
            procurement_category_ref: Reference to a procurement category. Defaults to None.
            max_single_amount: Maximum single transaction amount. Defaults to None.
            max_monthly_amount: Maximum monthly amount. Defaults to None.

        Returns:
            str: JSON string containing the created permission rule details.

        Raises:
            ValueError: If required references are not found or invalid operations.
        """
        valid_operations = {
            "create_requisition", "create_order", "approve", "create_contract",
            "manage_supplier", "view_reports", "export_data"
        }
        for op in allowed_operations:
            if op not in valid_operations:
                raise ValueError(f"Invalid operation: {op}. Must be one of {valid_operations}")

        self._get_employee(created_by_ref)
        if employee_ref is not None:
            self._get_employee(employee_ref)
        if role_ref is not None:
            self._get_role(role_ref)
        if department_ref is not None:
            self._get_department(department_ref)
        if procurement_category_ref is not None:
            self._get_procurement_category(procurement_category_ref)

        now = self._now_iso()
        ref = self._generate_ref("PPR", self.db.procurement_permission_rule)
        ppr = ProcurementPermissionRule(
            procurement_permission_rule_ref=ref,
            rule_name=rule_name,
            rule_code=rule_code,
            employee_ref=employee_ref,
            role_ref=role_ref,
            department_ref=department_ref,
            procurement_category_ref=procurement_category_ref,
            max_single_amount=max_single_amount,
            max_monthly_amount=max_monthly_amount,
            currency=currency,
            allowed_operations=allowed_operations,
            rule_status="active",
            created_by_ref=created_by_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.procurement_permission_rule[ref] = ppr
        return json.dumps({
            "procurement_permission_rule_ref": ref,
            "rule_name": rule_name,
            "rule_status": "active",
        })

    @is_tool(ToolType.WRITE)
    def update_procurement_permission_rule_status(
        self,
        procurement_permission_rule_ref: str,
        new_status: str,
    ) -> str:
        """
        Update the status of a procurement permission rule. The agent must ask for explicit user confirmation before calling.

        Args:
            procurement_permission_rule_ref: The unique identifier of the procurement permission rule.
            new_status: New rule status (active, inactive, expired).

        Returns:
            str: JSON string containing the updated permission rule status.

        Raises:
            ValueError: If the rule is not found or invalid status.
        """
        ppr = self._get_procurement_permission_rule(procurement_permission_rule_ref)

        valid_statuses = {"active", "inactive", "expired"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        ppr.rule_status = new_status
        ppr.updated_at = self._now_iso()
        return json.dumps({
            "procurement_permission_rule_ref": ppr.procurement_permission_rule_ref,
            "rule_status": ppr.rule_status,
        })

    @is_tool(ToolType.READ)
    def check_employee_procurement_permissions(self, employee_ref: str) -> str:
        """
        Check all procurement permission rules applicable to a specific employee.

        Args:
            employee_ref: The unique identifier of the employee.

        Returns:
            str: JSON string containing all applicable permission rules and their details.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        # Get employee's roles
        employee_role_refs = set()
        for er in self.db.employee_role.values():
            if er.employee_ref == employee_ref and er.status == "active":
                employee_role_refs.add(er.role_ref)

        # Get employee's departments
        employee_dept_refs = set()
        for dm in self.db.department_member.values():
            if dm.employee_ref == employee_ref and dm.status == "active":
                employee_dept_refs.add(dm.department_ref)

        results = []
        for ppr in self.db.procurement_permission_rule.values():
            if ppr.rule_status != "active":
                continue

            applicable = False
            # Direct employee match
            if ppr.employee_ref == employee_ref:
                applicable = True
            # Role match
            elif ppr.role_ref is not None and ppr.role_ref in employee_role_refs:
                applicable = True
            # Department match
            elif ppr.department_ref is not None and ppr.department_ref in employee_dept_refs:
                applicable = True
            # Global rule (no specific employee, role, or department)
            elif ppr.employee_ref is None and ppr.role_ref is None and ppr.department_ref is None:
                applicable = True

            if applicable:
                results.append({
                    "procurement_permission_rule_ref": ppr.procurement_permission_rule_ref,
                    "rule_name": ppr.rule_name,
                    "max_single_amount": ppr.max_single_amount,
                    "max_monthly_amount": ppr.max_monthly_amount,
                    "currency": ppr.currency,
                    "allowed_operations": ppr.allowed_operations,
                    "procurement_category_ref": ppr.procurement_category_ref,
                })
        return json.dumps(results)

    # =========================================================================
    # Procurement Training (采购培训与认证)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_training_course_details(self, procurement_training_course_ref: str) -> str:
        """
        Get detailed information about a specific procurement training course.

        Args:
            procurement_training_course_ref: The unique identifier of the training course.

        Returns:
            str: JSON string containing the training course details.

        Raises:
            ValueError: If the training course is not found.
        """
        ptc = self._get_procurement_training_course(procurement_training_course_ref)
        return json.dumps({
            "procurement_training_course_ref": ptc.procurement_training_course_ref,
            "course_title": ptc.course_title,
            "course_code": ptc.course_code,
            "course_type": ptc.course_type,
            "content_summary": ptc.content_summary,
            "duration_hours": ptc.duration_hours,
            "is_certification_required": ptc.is_certification_required,
            "certification_validity_months": ptc.certification_validity_months,
            "course_status": ptc.course_status,
            "created_by_ref": ptc.created_by_ref,
            "created_at": ptc.created_at,
            "updated_at": ptc.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_procurement_training_courses(
        self,
        course_type: Optional[str] = None,
        course_status: Optional[str] = None,
    ) -> str:
        """
        List procurement training courses with optional filters.

        Args:
            course_type: Filter by course type (process_training, system_training, compliance, skill_development). None returns all.
            course_status: Filter by course status (active, archived, draft). None returns all.

        Returns:
            str: JSON string containing a list of matching training courses.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, ptc in self.db.procurement_training_course.items():
            if course_type is not None and ptc.course_type != course_type:
                continue
            if course_status is not None and ptc.course_status != course_status:
                continue
            results.append({
                "procurement_training_course_ref": ptc.procurement_training_course_ref,
                "course_title": ptc.course_title,
                "course_code": ptc.course_code,
                "course_type": ptc.course_type,
                "duration_hours": ptc.duration_hours,
                "is_certification_required": ptc.is_certification_required,
                "course_status": ptc.course_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_procurement_training_record_details(self, procurement_training_record_ref: str) -> str:
        """
        Get detailed information about a specific procurement training record.

        Args:
            procurement_training_record_ref: The unique identifier of the training record.

        Returns:
            str: JSON string containing the training record details.

        Raises:
            ValueError: If the training record is not found.
        """
        ptr = self._get_procurement_training_record(procurement_training_record_ref)
        return json.dumps({
            "procurement_training_record_ref": ptr.procurement_training_record_ref,
            "procurement_training_course_ref": ptr.procurement_training_course_ref,
            "employee_ref": ptr.employee_ref,
            "enrollment_date": ptr.enrollment_date,
            "completion_date": ptr.completion_date,
            "score": ptr.score,
            "certification_number": ptr.certification_number,
            "certification_expiry_date": ptr.certification_expiry_date,
            "record_status": ptr.record_status,
            "created_at": ptr.created_at,
            "updated_at": ptr.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_procurement_training_records(
        self,
        employee_ref: Optional[str] = None,
        procurement_training_course_ref: Optional[str] = None,
        record_status: Optional[str] = None,
    ) -> str:
        """
        List procurement training records with optional filters.

        Args:
            employee_ref: Filter by employee. None returns all.
            procurement_training_course_ref: Filter by training course. None returns all.
            record_status: Filter by record status (enrolled, in_progress, completed, failed, cancelled). None returns all.

        Returns:
            str: JSON string containing a list of matching training records.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, ptr in self.db.procurement_training_record.items():
            if employee_ref is not None and ptr.employee_ref != employee_ref:
                continue
            if procurement_training_course_ref is not None and ptr.procurement_training_course_ref != procurement_training_course_ref:
                continue
            if record_status is not None and ptr.record_status != record_status:
                continue

            course_title = ""
            if ptr.procurement_training_course_ref in self.db.procurement_training_course:
                course_title = self.db.procurement_training_course[ptr.procurement_training_course_ref].course_title

            results.append({
                "procurement_training_record_ref": ptr.procurement_training_record_ref,
                "procurement_training_course_ref": ptr.procurement_training_course_ref,
                "course_title": course_title,
                "employee_ref": ptr.employee_ref,
                "enrollment_date": ptr.enrollment_date,
                "completion_date": ptr.completion_date,
                "score": ptr.score,
                "record_status": ptr.record_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def enroll_employee_in_training(
        self,
        procurement_training_course_ref: str,
        employee_ref: str,
    ) -> str:
        """
        Enroll an employee in a procurement training course. The agent must ask for explicit user confirmation before calling.

        Args:
            procurement_training_course_ref: Reference to the training course.
            employee_ref: Reference to the employee.

        Returns:
            str: JSON string containing the created training record details.

        Raises:
            ValueError: If the course or employee is not found, or employee already enrolled.
        """
        ptc = self._get_procurement_training_course(procurement_training_course_ref)
        self._get_employee(employee_ref)

        if ptc.course_status != "active":
            raise ValueError(f"Course status is '{ptc.course_status}', expected 'active'")

        # Check for existing active enrollment
        for ptr in self.db.procurement_training_record.values():
            if (ptr.procurement_training_course_ref == procurement_training_course_ref
                    and ptr.employee_ref == employee_ref
                    and ptr.record_status in ("enrolled", "in_progress")):
                raise ValueError("Employee is already enrolled in this course")

        now = self._now_iso()
        ref = self._generate_ref("PTR", self.db.procurement_training_record)
        ptr = ProcurementTrainingRecord(
            procurement_training_record_ref=ref,
            procurement_training_course_ref=procurement_training_course_ref,
            employee_ref=employee_ref,
            enrollment_date=now[:10],
            completion_date=None,
            score=None,
            certification_number=None,
            certification_expiry_date=None,
            certificate_file_ref=None,
            record_status="enrolled",
            created_at=now,
            updated_at=now,
        )
        self.db.procurement_training_record[ref] = ptr
        return json.dumps({
            "procurement_training_record_ref": ref,
            "procurement_training_course_ref": procurement_training_course_ref,
            "employee_ref": employee_ref,
            "record_status": "enrolled",
        })

    @is_tool(ToolType.WRITE)
    def update_training_record_status(
        self,
        procurement_training_record_ref: str,
        new_status: str,
        score: Optional[float] = None,
        certification_number: Optional[str] = None,
        certification_expiry_date: Optional[str] = None,
    ) -> str:
        """
        Update the status of a procurement training record. The agent must ask for explicit user confirmation before calling.

        Args:
            procurement_training_record_ref: The unique identifier of the training record.
            new_status: New record status (in_progress, completed, failed, cancelled).
            score: Score achieved. Required if new_status is completed or failed.
            certification_number: Certification number. Optional, for completed status.
            certification_expiry_date: Certification expiry date. Optional, for completed status.

        Returns:
            str: JSON string containing the updated training record status.

        Raises:
            ValueError: If the record is not found or invalid status transition.
        """
        ptr = self._get_procurement_training_record(procurement_training_record_ref)

        valid_statuses = {"enrolled", "in_progress", "completed", "failed", "cancelled"}
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")

        valid_transitions = {
            "enrolled": {"in_progress", "cancelled"},
            "in_progress": {"completed", "failed", "cancelled"},
            "completed": set(),
            "failed": set(),
            "cancelled": set(),
        }
        if new_status not in valid_transitions.get(ptr.record_status, set()):
            raise ValueError(f"Cannot transition from '{ptr.record_status}' to '{new_status}'")

        now = self._now_iso()
        ptr.record_status = new_status

        if new_status in ("completed", "failed"):
            ptr.completion_date = now[:10]
            if score is not None:
                ptr.score = score

        if new_status == "completed":
            if certification_number is not None:
                ptr.certification_number = certification_number
            if certification_expiry_date is not None:
                ptr.certification_expiry_date = certification_expiry_date

        ptr.updated_at = now
        return json.dumps({
            "procurement_training_record_ref": ptr.procurement_training_record_ref,
            "record_status": ptr.record_status,
            "score": ptr.score,
            "completion_date": ptr.completion_date,
        })

    # =========================================================================
    # Procurement Issue Tickets (采购系统异常处理)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_issue_ticket_details(self, procurement_issue_ticket_ref: str) -> str:
        """
        Get detailed information about a specific procurement issue ticket.

        Args:
            procurement_issue_ticket_ref: The unique identifier of the issue ticket.

        Returns:
            str: JSON string containing the issue ticket details.

        Raises:
            ValueError: If the issue ticket is not found.
        """
        pit = self._get_procurement_issue_ticket(procurement_issue_ticket_ref)
        return json.dumps({
            "procurement_issue_ticket_ref": pit.procurement_issue_ticket_ref,
            "ticket_code": pit.ticket_code,
            "issue_type": pit.issue_type,
            "related_resource_type": pit.related_resource_type,
            "related_resource_ref": pit.related_resource_ref,
            "title": pit.title,
            "description": pit.description,
            "severity": pit.severity,
            "reporter_ref": pit.reporter_ref,
            "assignee_ref": pit.assignee_ref,
            "resolution": pit.resolution,
            "ticket_status": pit.ticket_status,
            "resolved_at": pit.resolved_at,
            "created_at": pit.created_at,
            "updated_at": pit.updated_at,
        })

    @is_tool(ToolType.READ)
    def list_procurement_issue_tickets(
        self,
        issue_type: Optional[str] = None,
        severity: Optional[str] = None,
        ticket_status: Optional[str] = None,
        reporter_ref: Optional[str] = None,
        assignee_ref: Optional[str] = None,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
    ) -> str:
        """
        List procurement issue tickets with optional filters.

        Args:
            issue_type: Filter by issue type. None returns all.
            severity: Filter by severity. None returns all.
            ticket_status: Filter by ticket status. None returns all.
            reporter_ref: Filter by reporter employee. None returns all.
            assignee_ref: Filter by assignee employee. None returns all.
            related_resource_type: Filter by related resource type. None returns all.
            related_resource_ref: Filter by related resource ref. None returns all.

        Returns:
            str: JSON string containing a list of matching issue tickets.

        Raises:
            ValueError: If invalid filter values are provided.
        """
        results = []
        for ref, pit in self.db.procurement_issue_ticket.items():
            if issue_type is not None and pit.issue_type != issue_type:
                continue
            if severity is not None and pit.severity != severity:
                continue
            if ticket_status is not None and pit.ticket_status != ticket_status:
                continue
            if reporter_ref is not None and pit.reporter_ref != reporter_ref:
                continue
            if assignee_ref is not None and pit.assignee_ref != assignee_ref:
                continue
            if related_resource_type is not None and pit.related_resource_type != related_resource_type:
                continue
            if related_resource_ref is not None and pit.related_resource_ref != related_resource_ref:
                continue
            results.append({
                "procurement_issue_ticket_ref": pit.procurement_issue_ticket_ref,
                "ticket_code": pit.ticket_code,
                "issue_type": pit.issue_type,
                "title": pit.title,
                "severity": pit.severity,
                "ticket_status": pit.ticket_status,
                "reporter_ref": pit.reporter_ref,
                "assignee_ref": pit.assignee_ref,
                "created_at": pit.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_procurement_issue_ticket(
        self,
        ticket_code: str,
        issue_type: str,
        title: str,
        description: str,
        severity: str,
        reporter_ref: str,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
        assignee_ref: Optional[str] = None,
    ) -> str:
        """
        Create a new procurement issue ticket. The agent must ask for explicit user confirmation before calling.

        Args:
            ticket_code: Short code for the issue ticket.
            issue_type: Type of issue (system_error, process_issue, supplier_complaint, delivery_issue, quality_issue, other).
            title: Title of the issue ticket.
            description: Detailed description of the issue.
            severity: Severity level (low, medium, high, critical).
            reporter_ref: Employee ref of the reporter.
            related_resource_type: Type of related resource. Defaults to None.
            related_resource_ref: Reference to related resource. Defaults to None.
            assignee_ref: Employee ref of the assignee. Defaults to None.

        Returns:
            str: JSON string containing the created issue ticket details.

        Raises:
            ValueError: If required references are not found or invalid values are provided.
        """
        valid_issue_types = {"system_error", "process_issue", "supplier_complaint", "delivery_issue", "quality_issue", "other"}
        if issue_type not in valid_issue_types:
            raise ValueError(f"Invalid issue_type: {issue_type}. Must be one of {valid_issue_types}")

        valid_severities = {"low", "medium", "high", "critical"}
        if severity not in valid_severities:
            raise ValueError(f"Invalid severity: {severity}. Must be one of {valid_severities}")

        self._get_employee(reporter_ref)
        if assignee_ref is not None:
            self._get_employee(assignee_ref)

        now = self._now_iso()
        ref = self._generate_ref("PIT", self.db.procurement_issue_ticket)
        pit = ProcurementIssueTicket(
            procurement_issue_ticket_ref=ref,
            ticket_code=ticket_code,
            issue_type=issue_type,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            title=title,
            description=description,
            severity=severity,
            reporter_ref=reporter_ref,
            assignee_ref=assignee_ref,
            resolution=None,
            ticket_status="open",
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.procurement_issue_ticket[ref] = pit
        return json.dumps({
            "procurement_issue_ticket_ref": ref,
            "ticket_code": ticket_code,
            "issue_type": issue_type,
            "severity": severity,
            "ticket_status": "open",
        })

    @is_tool(ToolType.WRITE)
    def update_procurement_issue_ticket(
        self,
        procurement_issue_ticket_ref: str,
        ticket_status: Optional[str] = None,
        assignee_ref: Optional[str] = None,
        resolution: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> str:
        """
        Update a procurement issue ticket. The agent must ask for explicit user confirmation before calling.

        Args:
            procurement_issue_ticket_ref: The unique identifier of the issue ticket.
            ticket_status: New ticket status (in_progress, resolved, closed, cancelled). None to keep unchanged.
            assignee_ref: New assignee employee ref. None to keep unchanged.
            resolution: Resolution description. None to keep unchanged.
            severity: New severity level. None to keep unchanged.

        Returns:
            str: JSON string containing the updated issue ticket details.

        Raises:
            ValueError: If the ticket is not found or invalid values are provided.
        """
        pit = self._get_procurement_issue_ticket(procurement_issue_ticket_ref)

        if ticket_status is not None:
            valid_statuses = {"open", "in_progress", "resolved", "closed", "cancelled"}
            if ticket_status not in valid_statuses:
                raise ValueError(f"Invalid ticket_status: {ticket_status}. Must be one of {valid_statuses}")

            valid_transitions = {
                "open": {"in_progress", "cancelled"},
                "in_progress": {"resolved", "cancelled"},
                "resolved": {"closed", "in_progress"},
                "closed": set(),
                "cancelled": set(),
            }
            if ticket_status not in valid_transitions.get(pit.ticket_status, set()):
                raise ValueError(f"Cannot transition from '{pit.ticket_status}' to '{ticket_status}'")

            pit.ticket_status = ticket_status
            if ticket_status == "resolved":
                pit.resolved_at = self._now_iso()

        if assignee_ref is not None:
            self._get_employee(assignee_ref)
            pit.assignee_ref = assignee_ref

        if resolution is not None:
            pit.resolution = resolution

        if severity is not None:
            valid_severities = {"low", "medium", "high", "critical"}
            if severity not in valid_severities:
                raise ValueError(f"Invalid severity: {severity}. Must be one of {valid_severities}")
            pit.severity = severity

        pit.updated_at = self._now_iso()
        return json.dumps({
            "procurement_issue_ticket_ref": pit.procurement_issue_ticket_ref,
            "ticket_status": pit.ticket_status,
            "assignee_ref": pit.assignee_ref,
            "severity": pit.severity,
        })

    # =========================================================================
    # Procurement System Operation Guide (采购系统操作指引)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_process_guide(self, process_type: str) -> str:
        """
        Get a guide for a specific procurement process type.

        Args:
            process_type: The type of procurement process to get guidance for
                (requisition, order, contract, sourcing, supplier_onboarding, goods_receipt, acceptance, change_request).

        Returns:
            str: JSON string containing the process guide with steps and descriptions.

        Raises:
            ValueError: If the process type is not recognized.
        """
        guides = {
            "requisition": {
                "process_type": "requisition",
                "title": "Purchase Requisition Process",
                "steps": [
                    "1. Create a purchase requisition using create_purchase_requisition",
                    "2. Add line items using add_requisition_item",
                    "3. Submit the requisition using submit_purchase_requisition",
                    "4. Track approval status using list_approval_instances",
                    "5. Once approved, the requisition can be converted to a purchase order",
                ],
                "required_permissions": ["create_requisition"],
                "related_approval_templates": "purchase_requisition",
            },
            "order": {
                "process_type": "order",
                "title": "Purchase Order Process",
                "steps": [
                    "1. Create a purchase order using create_purchase_order",
                    "2. Add line items using add_purchase_order_item",
                    "3. Submit the order using update_purchase_order_status (submitted)",
                    "4. Wait for approval, then send to supplier",
                    "5. Track supplier confirmation and delivery",
                    "6. Create goods receipt upon delivery",
                ],
                "required_permissions": ["create_order"],
                "related_approval_templates": "purchase_order",
            },
            "contract": {
                "process_type": "contract",
                "title": "Purchase Contract Process",
                "steps": [
                    "1. Create a purchase contract using create_purchase_contract",
                    "2. Submit for approval using update_purchase_contract_status (pending_approval)",
                    "3. Once approved, activate the contract",
                    "4. Create purchase orders against the contract",
                    "5. Track contract consumption and expiry",
                ],
                "required_permissions": ["create_contract"],
                "related_approval_templates": "purchase_contract",
            },
            "sourcing": {
                "process_type": "sourcing",
                "title": "Sourcing Project Process",
                "steps": [
                    "1. Create a sourcing project using create_sourcing_project",
                    "2. Invite suppliers using invite_supplier_to_sourcing",
                    "3. Open the project for submissions",
                    "4. Evaluate supplier quotations",
                    "5. Award the project to the winning supplier",
                    "6. Create a contract or purchase order based on the award",
                ],
                "required_permissions": ["create_order", "manage_supplier"],
                "related_approval_templates": "N/A",
            },
            "supplier_onboarding": {
                "process_type": "supplier_onboarding",
                "title": "Supplier Onboarding Process",
                "steps": [
                    "1. Create a supplier record using create_supplier",
                    "2. Add contacts using create_supplier_contact",
                    "3. Submit qualifications for verification",
                    "4. Associate with procurement categories using add_supplier_to_category",
                    "5. Approve the supplier using approve_supplier",
                ],
                "required_permissions": ["manage_supplier"],
                "related_approval_templates": "supplier_onboarding",
            },
            "goods_receipt": {
                "process_type": "goods_receipt",
                "title": "Goods Receipt Process",
                "steps": [
                    "1. Create a goods receipt using create_goods_receipt",
                    "2. Add received items using add_goods_receipt_item",
                    "3. Update receipt status to inspected",
                    "4. Create acceptance record for quality inspection",
                    "5. Complete the receipt process",
                ],
                "required_permissions": ["create_order"],
                "related_approval_templates": "N/A",
            },
            "acceptance": {
                "process_type": "acceptance",
                "title": "Acceptance/Inspection Process",
                "steps": [
                    "1. Create an acceptance record using create_acceptance_record",
                    "2. Add inspection items using add_acceptance_item",
                    "3. Update status to in_progress, then completed",
                    "4. Update goods receipt status based on results",
                ],
                "required_permissions": ["create_order"],
                "related_approval_templates": "N/A",
            },
            "change_request": {
                "process_type": "change_request",
                "title": "Purchase Change Request Process",
                "steps": [
                    "1. Create a change request using create_purchase_change_request",
                    "2. Submit for approval",
                    "3. Once approved, execute the change using execute_purchase_change_request",
                    "4. Verify the changes are reflected in the target document",
                ],
                "required_permissions": ["create_order"],
                "related_approval_templates": "purchase_change_request",
            },
        }

        if process_type not in guides:
            raise ValueError(f"Unknown process_type: {process_type}. Must be one of {list(guides.keys())}")

        return json.dumps(guides[process_type])

    # =========================================================================
    # Procurement Method Selection (采购方式选择)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_procurement_method_recommendation(
        self,
        estimated_amount: float,
        currency: str,
        procurement_category_ref: Optional[str] = None,
    ) -> str:
        """
        Get procurement method recommendations based on amount and category.

        Args:
            estimated_amount: The estimated procurement amount.
            currency: Currency code.
            procurement_category_ref: Reference to the procurement category. Defaults to None.

        Returns:
            str: JSON string containing procurement method recommendations and applicable templates.

        Raises:
            ValueError: If the procurement category is not found (when provided).
        """
        if procurement_category_ref is not None:
            self._get_procurement_category(procurement_category_ref)

        # Find applicable approval templates
        applicable_templates = []
        for aft in self.db.approval_flow_template.values():
            if aft.template_status != "active":
                continue
            rules = aft.condition_rules
            # Check amount threshold
            if "amount_threshold" in rules:
                if estimated_amount < rules["amount_threshold"]:
                    continue
            # Check category
            if "procurement_category_ref" in rules and procurement_category_ref is not None:
                if rules["procurement_category_ref"] != procurement_category_ref:
                    continue
            applicable_templates.append({
                "approval_flow_template_ref": aft.approval_flow_template_ref,
                "template_name": aft.template_name,
                "applicable_type": aft.applicable_type,
                "condition_rules": aft.condition_rules,
                "priority": aft.priority,
            })

        # Find relevant permission rules
        relevant_rules = []
        for ppr in self.db.procurement_permission_rule.values():
            if ppr.rule_status != "active":
                continue
            if ppr.procurement_category_ref is not None and procurement_category_ref is not None:
                if ppr.procurement_category_ref != procurement_category_ref:
                    continue
            if ppr.max_single_amount is not None and estimated_amount > ppr.max_single_amount:
                relevant_rules.append({
                    "rule_name": ppr.rule_name,
                    "max_single_amount": ppr.max_single_amount,
                    "note": "Amount exceeds single transaction limit",
                })

        recommendations = {
            "estimated_amount": estimated_amount,
            "currency": currency,
            "applicable_approval_templates": applicable_templates,
            "amount_limit_warnings": relevant_rules,
            "suggested_methods": [],
        }

        # Basic recommendations based on amount
        if estimated_amount > 500000:
            recommendations["suggested_methods"].append({
                "method": "competitive_bid",
                "reason": "High-value procurement should use competitive bidding",
            })
        elif estimated_amount > 100000:
            recommendations["suggested_methods"].append({
                "method": "negotiation",
                "reason": "Medium-value procurement can use negotiation",
            })
        else:
            recommendations["suggested_methods"].append({
                "method": "sole_source",
                "reason": "Low-value procurement can use direct sourcing",
            })

        return json.dumps(recommendations)

    # =========================================================================
    # Contract-based ordering (采购合同关联下单)
    # =========================================================================

    @is_tool(ToolType.READ)
    def get_contract_remaining_amount(self, purchase_contract_ref: str) -> str:
        """
        Get the remaining available amount for a purchase contract.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.

        Returns:
            str: JSON string containing the contract amount details and remaining balance.

        Raises:
            ValueError: If the purchase contract is not found.
        """
        pc = self._get_purchase_contract(purchase_contract_ref)

        # Calculate ordered amounts from purchase orders linked to this contract
        ordered_amount = 0.0
        for po in self.db.purchase_order.values():
            if po.purchase_contract_ref == purchase_contract_ref and po.order_status not in ("cancelled", "rejected"):
                ordered_amount += po.total_amount

        remaining = pc.total_amount - pc.consumed_amount
        return json.dumps({
            "purchase_contract_ref": pc.purchase_contract_ref,
            "contract_title": pc.contract_title,
            "total_amount": pc.total_amount,
            "consumed_amount": pc.consumed_amount,
            "ordered_amount": ordered_amount,
            "remaining_amount": remaining,
            "currency": pc.currency,
            "contract_status": pc.contract_status,
            "effective_date": pc.effective_date,
            "expiry_date": pc.expiry_date,
        })

    @is_tool(ToolType.READ)
    def list_orders_for_contract(self, purchase_contract_ref: str) -> str:
        """
        List all purchase orders associated with a specific contract.

        Args:
            purchase_contract_ref: The unique identifier of the purchase contract.

        Returns:
            str: JSON string containing a list of purchase orders for the contract.

        Raises:
            ValueError: If the purchase contract is not found.
        """
        self._get_purchase_contract(purchase_contract_ref)
        results = []
        for po in self.db.purchase_order.values():
            if po.purchase_contract_ref == purchase_contract_ref:
                results.append({
                    "purchase_order_ref": po.purchase_order_ref,
                    "order_code": po.order_code,
                    "order_type": po.order_type,
                    "total_amount": po.total_amount,
                    "currency": po.currency,
                    "order_status": po.order_status,
                    "expected_delivery_date": po.expected_delivery_date,
                    "created_at": po.created_at,
                })
        return json.dumps(results)