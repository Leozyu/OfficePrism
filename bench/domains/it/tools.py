"""IT 域工具集：在 OfficeTools 上扩展 IT 相关操作。"""
from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.it.models import (
    ITDB,
    ITSystem,
    ITSystemAccount,
    ITSystemAccountPermission,
    AccessAnomaly,
    AccountMigration,
    EmailAccount,
    EmailDistributionList,
    EmailDistributionListMember,
    EmailSecurityEvent,
    CodeRepository,
    CodeRepositoryMember,
    CodeBranch,
    MergeRequest,
    MergeRequestReviewer,
    MergeRequestActivity,
    CICDPipeline,
    PipelineExecution,
    Deployment,
    DeployEnvironment,
    ITResource,
    ITResourceRequest,
    DevEnvironment,
    DataSource,
    DataAccessGrant,
    DataAsset,
    DataTransferJob,
    NetworkZone,
    VPNConnection,
    GuestWifiCredential,
    NetworkAccessRule,
    NetworkIncident,
    SoftwareCatalog,
    SoftwareLicense,
    SoftwareLicenseAssignment,
    SoftwareInstallation,
    SoftwareFiling,
    Printer,
    PrinterSupply,
    PrinterIncident,
    FileTransfer,
    FileSecurityPolicy,
    ITServiceTicket,
    ITServiceTicketComment,
    ITServiceContact,
    ITKnowledgeArticle,
)


class ITTools(OfficeTools):
    """IT 域工具集：在 OfficeTools 上扩展 IT 相关操作。"""

    db: ITDB

    def __init__(self, db: ITDB) -> None:
        """
        使用 IT 数据库初始化 IT 工具集。

        参数：
            db：包含全部 IT 域数据的 ITDB 实例。

        返回：
            无
        """
        super().__init__(db)

    # ===========================
    # 内部辅助方法
    # ===========================

    def _get_it_system(self, it_system_ref: str) -> ITSystem:
        """根据 ref 获取 IT 系统；不存在则抛出 ValueError。"""
        if it_system_ref not in self.db.it_system:
            raise ValueError("IT system not found")
        return self.db.it_system[it_system_ref]

    def _get_it_system_account(self, it_system_account_ref: str) -> ITSystemAccount:
        """根据 ref 获取 IT 系统账号；不存在则抛出 ValueError。"""
        if it_system_account_ref not in self.db.it_system_account:
            raise ValueError("IT system account not found")
        return self.db.it_system_account[it_system_account_ref]

    def _get_it_system_account_permission(self, ref: str) -> ITSystemAccountPermission:
        """根据 ref 获取 IT 系统账号权限。"""
        if ref not in self.db.it_system_account_permission:
            raise ValueError("IT system account permission not found")
        return self.db.it_system_account_permission[ref]

    def _get_access_anomaly(self, access_anomaly_ref: str) -> AccessAnomaly:
        """根据 ref 获取访问异常。"""
        if access_anomaly_ref not in self.db.access_anomaly:
            raise ValueError("Access anomaly not found")
        return self.db.access_anomaly[access_anomaly_ref]

    def _get_account_migration(self, account_migration_ref: str) -> AccountMigration:
        """根据 ref 获取账号迁移记录。"""
        if account_migration_ref not in self.db.account_migration:
            raise ValueError("Account migration not found")
        return self.db.account_migration[account_migration_ref]

    def _get_email_account(self, email_account_ref: str) -> EmailAccount:
        """根据 ref 获取邮箱账号。"""
        if email_account_ref not in self.db.email_account:
            raise ValueError("Email account not found")
        return self.db.email_account[email_account_ref]

    def _get_email_distribution_list(self, ref: str) -> EmailDistributionList:
        """根据 ref 获取邮件组。"""
        if ref not in self.db.email_distribution_list:
            raise ValueError("Email distribution list not found")
        return self.db.email_distribution_list[ref]

    def _get_email_security_event(self, ref: str) -> EmailSecurityEvent:
        """根据 ref 获取邮箱安全事件。"""
        if ref not in self.db.email_security_event:
            raise ValueError("Email security event not found")
        return self.db.email_security_event[ref]

    def _get_code_repository(self, code_repository_ref: str) -> CodeRepository:
        """根据 ref 获取代码仓库。"""
        if code_repository_ref not in self.db.code_repository:
            raise ValueError("Code repository not found")
        return self.db.code_repository[code_repository_ref]

    def _get_code_branch(self, code_branch_ref: str) -> CodeBranch:
        """根据 ref 获取代码分支。"""
        if code_branch_ref not in self.db.code_branch:
            raise ValueError("Code branch not found")
        return self.db.code_branch[code_branch_ref]

    def _get_merge_request(self, merge_request_ref: str) -> MergeRequest:
        """根据 ref 获取合并请求。"""
        if merge_request_ref not in self.db.merge_request:
            raise ValueError("Merge request not found")
        return self.db.merge_request[merge_request_ref]

    def _get_merge_request_reviewer(self, ref: str) -> MergeRequestReviewer:
        """根据 ref 获取合并请求评审人。"""
        if ref not in self.db.merge_request_reviewer:
            raise ValueError("Merge request reviewer not found")
        return self.db.merge_request_reviewer[ref]

    def _get_ci_cd_pipeline(self, ci_cd_pipeline_ref: str) -> CICDPipeline:
        """根据 ref 获取 CI/CD 流水线。"""
        if ci_cd_pipeline_ref not in self.db.ci_cd_pipeline:
            raise ValueError("CI/CD pipeline not found")
        return self.db.ci_cd_pipeline[ci_cd_pipeline_ref]

    def _get_pipeline_execution(self, pipeline_execution_ref: str) -> PipelineExecution:
        """根据 ref 获取流水线执行记录。"""
        if pipeline_execution_ref not in self.db.pipeline_execution:
            raise ValueError("Pipeline execution not found")
        return self.db.pipeline_execution[pipeline_execution_ref]

    def _get_deployment(self, deployment_ref: str) -> Deployment:
        """根据 ref 获取部署记录。"""
        if deployment_ref not in self.db.deployment:
            raise ValueError("Deployment not found")
        return self.db.deployment[deployment_ref]

    def _get_deploy_environment(self, deploy_environment_ref: str) -> DeployEnvironment:
        """根据 ref 获取部署环境。"""
        if deploy_environment_ref not in self.db.deploy_environment:
            raise ValueError("Deploy environment not found")
        return self.db.deploy_environment[deploy_environment_ref]

    def _get_it_resource(self, it_resource_ref: str) -> ITResource:
        """根据 ref 获取 IT 资源。"""
        if it_resource_ref not in self.db.it_resource:
            raise ValueError("IT resource not found")
        return self.db.it_resource[it_resource_ref]

    def _get_it_resource_request(self, ref: str) -> ITResourceRequest:
        """根据 ref 获取 IT 资源申请。"""
        if ref not in self.db.it_resource_request:
            raise ValueError("IT resource request not found")
        return self.db.it_resource_request[ref]

    def _get_dev_environment(self, dev_environment_ref: str) -> DevEnvironment:
        """根据 ref 获取开发环境。"""
        if dev_environment_ref not in self.db.dev_environment:
            raise ValueError("Dev environment not found")
        return self.db.dev_environment[dev_environment_ref]

    def _get_data_source(self, data_source_ref: str) -> DataSource:
        """根据 ref 获取数据源。"""
        if data_source_ref not in self.db.data_source:
            raise ValueError("Data source not found")
        return self.db.data_source[data_source_ref]

    def _get_data_access_grant(self, data_access_grant_ref: str) -> DataAccessGrant:
        """根据 ref 获取数据访问授权。"""
        if data_access_grant_ref not in self.db.data_access_grant:
            raise ValueError("Data access grant not found")
        return self.db.data_access_grant[data_access_grant_ref]

    def _get_data_asset(self, data_asset_ref: str) -> DataAsset:
        """根据 ref 获取数据资产。"""
        if data_asset_ref not in self.db.data_asset:
            raise ValueError("Data asset not found")
        return self.db.data_asset[data_asset_ref]

    def _get_data_transfer_job(self, data_transfer_job_ref: str) -> DataTransferJob:
        """根据 ref 获取数据传输任务。"""
        if data_transfer_job_ref not in self.db.data_transfer_job:
            raise ValueError("Data transfer job not found")
        return self.db.data_transfer_job[data_transfer_job_ref]

    def _get_network_zone(self, network_zone_ref: str) -> NetworkZone:
        """根据 ref 获取网络分区。"""
        if network_zone_ref not in self.db.network_zone:
            raise ValueError("Network zone not found")
        return self.db.network_zone[network_zone_ref]

    def _get_vpn_connection(self, vpn_connection_ref: str) -> VPNConnection:
        """根据 ref 获取 VPN 连接。"""
        if vpn_connection_ref not in self.db.vpn_connection:
            raise ValueError("VPN connection not found")
        return self.db.vpn_connection[vpn_connection_ref]

    def _get_guest_wifi_credential(self, ref: str) -> GuestWifiCredential:
        """根据 ref 获取访客 Wi‑Fi 凭证。"""
        if ref not in self.db.guest_wifi_credential:
            raise ValueError("Guest Wi-Fi credential not found")
        return self.db.guest_wifi_credential[ref]

    def _get_network_access_rule(self, ref: str) -> NetworkAccessRule:
        """根据 ref 获取网络访问规则。"""
        if ref not in self.db.network_access_rule:
            raise ValueError("Network access rule not found")
        return self.db.network_access_rule[ref]

    def _get_network_incident(self, ref: str) -> NetworkIncident:
        """根据 ref 获取网络事件。"""
        if ref not in self.db.network_incident:
            raise ValueError("Network incident not found")
        return self.db.network_incident[ref]

    def _get_software_catalog(self, software_catalog_ref: str) -> SoftwareCatalog:
        """根据 ref 获取软件目录条目。"""
        if software_catalog_ref not in self.db.software_catalog:
            raise ValueError("Software catalog entry not found")
        return self.db.software_catalog[software_catalog_ref]

    def _get_software_license(self, software_license_ref: str) -> SoftwareLicense:
        """根据 ref 获取软件许可证。"""
        if software_license_ref not in self.db.software_license:
            raise ValueError("Software license not found")
        return self.db.software_license[software_license_ref]

    def _get_software_license_assignment(self, ref: str) -> SoftwareLicenseAssignment:
        """根据 ref 获取软件许可证分配。"""
        if ref not in self.db.software_license_assignment:
            raise ValueError("Software license assignment not found")
        return self.db.software_license_assignment[ref]

    def _get_software_installation(self, ref: str) -> SoftwareInstallation:
        """根据 ref 获取软件安装记录。"""
        if ref not in self.db.software_installation:
            raise ValueError("Software installation not found")
        return self.db.software_installation[ref]

    def _get_software_filing(self, software_filing_ref: str) -> SoftwareFiling:
        """根据 ref 获取软件报备。"""
        if software_filing_ref not in self.db.software_filing:
            raise ValueError("Software filing not found")
        return self.db.software_filing[software_filing_ref]

    def _get_printer(self, printer_ref: str) -> Printer:
        """根据 ref 获取打印机。"""
        if printer_ref not in self.db.printer:
            raise ValueError("Printer not found")
        return self.db.printer[printer_ref]

    def _get_printer_supply(self, printer_supply_ref: str) -> PrinterSupply:
        """根据 ref 获取打印耗材。"""
        if printer_supply_ref not in self.db.printer_supply:
            raise ValueError("Printer supply not found")
        return self.db.printer_supply[printer_supply_ref]

    def _get_printer_incident(self, printer_incident_ref: str) -> PrinterIncident:
        """根据 ref 获取打印故障记录。"""
        if printer_incident_ref not in self.db.printer_incident:
            raise ValueError("Printer incident not found")
        return self.db.printer_incident[printer_incident_ref]

    def _get_file_transfer(self, file_transfer_ref: str) -> FileTransfer:
        """根据 ref 获取文件传输记录。"""
        if file_transfer_ref not in self.db.file_transfer:
            raise ValueError("File transfer not found")
        return self.db.file_transfer[file_transfer_ref]

    def _get_file_security_policy(self, ref: str) -> FileSecurityPolicy:
        """根据 ref 获取文件安全策略。"""
        if ref not in self.db.file_security_policy:
            raise ValueError("File security policy not found")
        return self.db.file_security_policy[ref]

    def _get_it_service_ticket(self, ref: str) -> ITServiceTicket:
        """根据 ref 获取 IT 服务工单。"""
        if ref not in self.db.it_service_ticket:
            raise ValueError("IT service ticket not found")
        return self.db.it_service_ticket[ref]

    def _get_it_service_ticket_comment(self, ref: str) -> ITServiceTicketComment:
        """根据 ref 获取工单评论。"""
        if ref not in self.db.it_service_ticket_comment:
            raise ValueError("IT service ticket comment not found")
        return self.db.it_service_ticket_comment[ref]

    def _get_it_service_contact(self, ref: str) -> ITServiceContact:
        """根据 ref 获取 IT 服务联系人。"""
        if ref not in self.db.it_service_contact:
            raise ValueError("IT service contact not found")
        return self.db.it_service_contact[ref]

    def _get_it_knowledge_article(self, ref: str) -> ITKnowledgeArticle:
        """根据 ref 获取 IT 知识库文章。"""
        if ref not in self.db.it_knowledge_article:
            raise ValueError("IT knowledge article not found")
        return self.db.it_knowledge_article[ref]

    # ===================================================================
    # IT 系统与账号管理（账号管理 / 账号登录问题）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_it_system_details(self, it_system_ref: str) -> ITSystem:
        """
        获取 IT 系统的详情。

        参数：
            it_system_ref: IT 系统的唯一标识。

        返回：
            ITSystem：IT 系统对象。

        异常：
            ValueError：若未找到 IT 系统。
        """
        return self._get_it_system(it_system_ref)

    @is_tool(ToolType.READ)
    def list_it_systems(
        self,
        system_type: Optional[str] = None,
        system_status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出 IT 系统（可选筛选）。

        参数：
            system_type: 按系统类型筛选（business_app, infrastructure, platform, tool, saas).
            system_status: 按系统状态筛选（active, inactive, deprecated, maintenance).
            department_ref: 按责任部门 ref 筛选。

        返回：
            str：IT 系统摘要的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sys in self.db.it_system.items():
            if system_type is not None and sys.system_type != system_type:
                continue
            if system_status is not None and sys.system_status != system_status:
                continue
            if department_ref is not None and sys.department_ref != department_ref:
                continue
            results.append({
                "it_system_ref": sys.it_system_ref,
                "system_name": sys.system_name,
                "system_code": sys.system_code,
                "system_type": sys.system_type,
                "system_status": sys.system_status,
                "sso_enabled": sys.sso_enabled,
                "mfa_required": sys.mfa_required,
                "owner_employee_ref": sys.owner_employee_ref,
                "department_ref": sys.department_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_it_system_ref_by_name(self, system_name: str) -> str:
        """
        按名称查找 IT 系统 ref（部分匹配，不区分大小写）。

        参数：
            system_name: IT 系统名称（可部分匹配）。

        返回：
            str：匹配到的 IT 系统的 it_system_ref。

        异常：
            ValueError：若未匹配到 IT 系统。
        """
        search = system_name.lower()
        for ref, sys in self.db.it_system.items():
            if search in sys.system_name.lower():
                return ref
        raise ValueError("IT system not found")

    @is_tool(ToolType.READ)
    def get_it_system_account_details(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        获取 IT 系统账号的详情。

        参数：
            it_system_account_ref: IT 系统账号的唯一标识。

        返回：
            ITSystemAccount：IT 系统账号对象。

        异常：
            ValueError：若未找到账号。
        """
        return self._get_it_system_account(it_system_account_ref)

    @is_tool(ToolType.READ)
    def list_it_system_accounts_for_employee(
        self,
        employee_ref: str,
        account_status: Optional[str] = None,
    ) -> str:
        """
        列出某员工的全部 IT 系统账号。

        参数：
            employee_ref: 员工引用。
            account_status: 可选按账号状态筛选（active、disabled、locked、deprovisioned）。

        返回：
            str：IT system account summaries 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, acct in self.db.it_system_account.items():
            if acct.employee_ref != employee_ref:
                continue
            if account_status is not None and acct.account_status != account_status:
                continue
            results.append({
                "it_system_account_ref": acct.it_system_account_ref,
                "it_system_ref": acct.it_system_ref,
                "account_username": acct.account_username,
                "account_type": acct.account_type,
                "account_status": acct.account_status,
                "role_in_system": acct.role_in_system,
                "mfa_enabled": acct.mfa_enabled,
                "last_login_at": acct.last_login_at,
                "password_expires_at": acct.password_expires_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_it_system_accounts_for_system(
        self,
        it_system_ref: str,
        account_status: Optional[str] = None,
        role_in_system: Optional[str] = None,
    ) -> str:
        """
        列出某 IT 系统内的全部账号。

        参数：
            it_system_ref: IT 系统引用。
            account_status: 可选按账号状态筛选。
            role_in_system: 可选按系统内角色筛选。

        返回：
            str：account summaries 的 JSON 数组。

        异常：
            ValueError：若未找到 IT 系统。
        """
        self._get_it_system(it_system_ref)
        results = []
        for ref, acct in self.db.it_system_account.items():
            if acct.it_system_ref != it_system_ref:
                continue
            if account_status is not None and acct.account_status != account_status:
                continue
            if role_in_system is not None and acct.role_in_system != role_in_system:
                continue
            emp = self._get_employee(acct.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "it_system_account_ref": acct.it_system_account_ref,
                "employee_ref": acct.employee_ref,
                "display_name": up.display_name,
                "account_username": acct.account_username,
                "account_type": acct.account_type,
                "account_status": acct.account_status,
                "role_in_system": acct.role_in_system,
                "mfa_enabled": acct.mfa_enabled,
                "last_login_at": acct.last_login_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_it_system_account(
        self,
        it_system_ref: str,
        employee_ref: str,
        account_username: str,
        account_type: str,
        role_in_system: str,
        mfa_enabled: bool = False,
    ) -> ITSystemAccount:
        """
        Create a new IT system account for an employee. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_ref: 引用the IT system.
            employee_ref: 引用the employee.
            account_username: 新账号用户名。
            account_type: 账号类型（personal、service、shared、admin）。
            role_in_system: 系统内角色（user、admin、power_user、readonly）。
            mfa_enabled: Whether to enable MFA。默认 False。

        返回：
            ITSystemAccount：新建的账号。

        异常：
            ValueError：若系统或员工不存在，或参数无效。
        """
        self._get_it_system(it_system_ref)
        self._get_employee(employee_ref)

        valid_types = {"personal", "service", "shared", "admin"}
        if account_type not in valid_types:
            raise ValueError(f"Invalid account_type: {account_type}. Must be one of {valid_types}")
        valid_roles = {"user", "admin", "power_user", "readonly"}
        if role_in_system not in valid_roles:
            raise ValueError(f"Invalid role_in_system: {role_in_system}. Must be one of {valid_roles}")

        # 检查同一系统内用户名是否重复
        for acct in self.db.it_system_account.values():
            if acct.it_system_ref == it_system_ref and acct.account_username == account_username and acct.account_status != "deprovisioned":
                raise ValueError(f"Username '{account_username}' already exists in this IT system")

        now = self._now_iso()
        ref = self._generate_ref("ITSA", self.db.it_system_account)

        account = ITSystemAccount(
            it_system_account_ref=ref,
            it_system_ref=it_system_ref,
            employee_ref=employee_ref,
            account_username=account_username,
            account_type=account_type,
            account_status="active",
            role_in_system=role_in_system,
            password_last_changed_at=now,
            password_expires_at=None,
            last_login_at=None,
            mfa_enabled=mfa_enabled,
            locked_at=None,
            lock_reason=None,
            provisioned_at=now,
            deprovisioned_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.it_system_account[ref] = account
        return account

    @is_tool(ToolType.WRITE)
    def disable_it_system_account(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        Disable an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或已禁用/已注销。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status in ("disabled", "deprovisioned"):
            raise ValueError(f"Account is already {acct.account_status}")
        acct.account_status = "disabled"
        acct.updated_at = self._now_iso()
        return acct

    @is_tool(ToolType.WRITE)
    def enable_it_system_account(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        Re-enable a disabled IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或非禁用/锁定状态。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status not in ("disabled", "locked"):
            raise ValueError(f"Account is in '{acct.account_status}' state and cannot be enabled")
        acct.account_status = "active"
        acct.locked_at = None
        acct.lock_reason = None
        acct.updated_at = self._now_iso()
        return acct

    @is_tool(ToolType.WRITE)
    def lock_it_system_account(self, it_system_account_ref: str, lock_reason: str) -> ITSystemAccount:
        """
        Lock an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.
            lock_reason: 锁定账号原因。

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或已锁定/已注销。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status in ("locked", "deprovisioned"):
            raise ValueError(f"Account is already {acct.account_status}")
        now = self._now_iso()
        acct.account_status = "locked"
        acct.locked_at = now
        acct.lock_reason = lock_reason
        acct.updated_at = now
        return acct

    @is_tool(ToolType.WRITE)
    def unlock_it_system_account(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        Unlock a locked IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或未锁定。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status != "locked":
            raise ValueError("Account is not locked")
        acct.account_status = "active"
        acct.locked_at = None
        acct.lock_reason = None
        acct.updated_at = self._now_iso()
        return acct

    @is_tool(ToolType.WRITE)
    def deprovision_it_system_account(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        Deprovision an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或已注销。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status == "deprovisioned":
            raise ValueError("Account is already deprovisioned")
        now = self._now_iso()
        acct.account_status = "deprovisioned"
        acct.deprovisioned_at = now
        acct.updated_at = now
        return acct

    @is_tool(ToolType.WRITE)
    def reset_it_system_account_password(self, it_system_account_ref: str) -> ITSystemAccount:
        """
        Reset the password of an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.

        返回：
            ITSystemAccount：更新后的账号（已刷新密码时间戳）。

        异常：
            ValueError：若未找到账号或已注销。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        if acct.account_status == "deprovisioned":
            raise ValueError("Cannot reset password for a deprovisioned account")
        now = self._now_iso()
        acct.password_last_changed_at = now
        # 若因密码问题被锁定则解锁
        if acct.account_status == "locked":
            acct.account_status = "active"
            acct.locked_at = None
            acct.lock_reason = None
        acct.updated_at = now
        return acct

    @is_tool(ToolType.WRITE)
    def update_it_system_account_role(
        self,
        it_system_account_ref: str,
        role_in_system: str,
    ) -> ITSystemAccount:
        """
        Update the role of an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.
            role_in_system: 新角色（user、admin、power_user、readonly）。

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号或角色无效。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        valid_roles = {"user", "admin", "power_user", "readonly"}
        if role_in_system not in valid_roles:
            raise ValueError(f"Invalid role_in_system: {role_in_system}. Must be one of {valid_roles}")
        acct.role_in_system = role_in_system
        acct.updated_at = self._now_iso()
        return acct

    @is_tool(ToolType.WRITE)
    def toggle_it_system_account_mfa(
        self,
        it_system_account_ref: str,
        mfa_enabled: bool,
    ) -> ITSystemAccount:
        """
        Enable or disable MFA for an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.
            mfa_enabled: 是否启用 MFA。

        返回：
            ITSystemAccount：更新后的账号。

        异常：
            ValueError：若未找到账号。
        """
        acct = self._get_it_system_account(it_system_account_ref)
        acct.mfa_enabled = mfa_enabled
        acct.updated_at = self._now_iso()
        return acct

    # ===================================================================
    # IT 系统账号权限（账号权限管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_it_system_account_permissions(
        self,
        it_system_account_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        列出 IT 系统账号的权限。

        参数：
            it_system_account_ref: 引用the IT system account.
            status: 可选按权限状态筛选（active、revoked、expired）。

        返回：
            str：permission details 的 JSON 数组。

        异常：
            ValueError：若未找到账号。
        """
        self._get_it_system_account(it_system_account_ref)
        results = []
        for ref, perm in self.db.it_system_account_permission.items():
            if perm.it_system_account_ref != it_system_account_ref:
                continue
            if status is not None and perm.status != status:
                continue
            results.append({
                "it_system_account_permission_ref": perm.it_system_account_permission_ref,
                "permission_name": perm.permission_name,
                "permission_level": perm.permission_level,
                "scope": perm.scope,
                "granted_by_ref": perm.granted_by_ref,
                "granted_at": perm.granted_at,
                "expires_at": perm.expires_at,
                "status": perm.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def grant_it_system_account_permission(
        self,
        it_system_account_ref: str,
        permission_name: str,
        permission_level: str,
        scope: str,
        granted_by_ref: str,
        expires_at: Optional[str] = None,
    ) -> ITSystemAccountPermission:
        """
        Grant a permission to an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_ref: 引用the IT system account.
            permission_name: 要授予的权限名称。
            permission_level: 权限级别（read、write、admin、full）。
            scope: 权限在系统内的作用范围。
            granted_by_ref: 员工 ref：the person granting the permission.
            expires_at: 可选过期时间（ISO 8601）。

        返回：
            ITSystemAccountPermission：新建的权限。

        异常：
            ValueError：若账号或授权人员工不存在，或参数无效。
        """
        self._get_it_system_account(it_system_account_ref)
        self._get_employee(granted_by_ref)

        valid_levels = {"read", "write", "admin", "full"}
        if permission_level not in valid_levels:
            raise ValueError(f"Invalid permission_level: {permission_level}. Must be one of {valid_levels}")

        now = self._now_iso()
        ref = self._generate_ref("ITSAP", self.db.it_system_account_permission)

        perm = ITSystemAccountPermission(
            it_system_account_permission_ref=ref,
            it_system_account_ref=it_system_account_ref,
            permission_name=permission_name,
            permission_level=permission_level,
            scope=scope,
            granted_by_ref=granted_by_ref,
            granted_at=now,
            expires_at=expires_at,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.it_system_account_permission[ref] = perm
        return perm

    @is_tool(ToolType.WRITE)
    def revoke_it_system_account_permission(
        self,
        it_system_account_permission_ref: str,
    ) -> ITSystemAccountPermission:
        """
        Revoke a permission from an IT system account. 调用前 Agent 须向用户明确确认。

        参数：
            it_system_account_permission_ref: 引用the permission.

        返回：
            ITSystemAccountPermission：更新后的权限。

        异常：
            ValueError：若未找到权限或已撤销/已过期。
        """
        perm = self._get_it_system_account_permission(it_system_account_permission_ref)
        if perm.status in ("revoked", "expired"):
            raise ValueError(f"Permission is already {perm.status}")
        perm.status = "revoked"
        perm.updated_at = self._now_iso()
        return perm

    # ===================================================================
    # 访问异常（访问异常处理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_access_anomaly_details(self, access_anomaly_ref: str) -> AccessAnomaly:
        """
        获取访问异常的详情。

        参数：
            access_anomaly_ref: 访问异常的唯一标识。

        返回：
            AccessAnomaly：访问异常对象。

        异常：
            ValueError：若未找到异常。
        """
        return self._get_access_anomaly(access_anomaly_ref)

    @is_tool(ToolType.READ)
    def list_access_anomalies(
        self,
        employee_ref: Optional[str] = None,
        it_system_ref: Optional[str] = None,
        anomaly_type: Optional[str] = None,
        severity: Optional[str] = None,
        resolution_status: Optional[str] = None,
    ) -> str:
        """
        列出访问异常（可选筛选）。

        参数：
            employee_ref: 按员工筛选。
            it_system_ref: 按 IT system.
            anomaly_type: 按异常类型筛选。
            severity: 按严重程度筛选（low, medium, high, critical).
            resolution_status: 按处理状态筛选（open, investigating, resolved, dismissed).

        返回：
            str：access anomaly summaries 的 JSON 数组。

        异常：
            ValueError：若引用实体不存在。
        """
        results = []
        for ref, anomaly in self.db.access_anomaly.items():
            if employee_ref is not None and anomaly.employee_ref != employee_ref:
                continue
            if it_system_ref is not None and anomaly.it_system_ref != it_system_ref:
                continue
            if anomaly_type is not None and anomaly.anomaly_type != anomaly_type:
                continue
            if severity is not None and anomaly.severity != severity:
                continue
            if resolution_status is not None and anomaly.resolution_status != resolution_status:
                continue
            results.append({
                "access_anomaly_ref": anomaly.access_anomaly_ref,
                "it_system_ref": anomaly.it_system_ref,
                "it_system_account_ref": anomaly.it_system_account_ref,
                "employee_ref": anomaly.employee_ref,
                "anomaly_type": anomaly.anomaly_type,
                "severity": anomaly.severity,
                "source_ip": anomaly.source_ip,
                "description": anomaly.description,
                "resolution_status": anomaly.resolution_status,
                "occurred_at": anomaly.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def resolve_access_anomaly(
        self,
        access_anomaly_ref: str,
        resolved_by_ref: str,
        resolution_notes: str,
    ) -> AccessAnomaly:
        """
        Resolve an access anomaly. 调用前 Agent 须向用户明确确认。

        参数：
            access_anomaly_ref: 引用the access anomaly.
            resolved_by_ref: 员工 ref：the person resolving it.
            resolution_notes: 解决过程说明。

        返回：
            AccessAnomaly：更新后的异常记录。

        异常：
            ValueError：若未找到异常或已解决/已忽略。
        """
        anomaly = self._get_access_anomaly(access_anomaly_ref)
        self._get_employee(resolved_by_ref)
        if anomaly.resolution_status in ("resolved", "dismissed"):
            raise ValueError(f"Anomaly is already {anomaly.resolution_status}")
        now = self._now_iso()
        anomaly.resolution_status = "resolved"
        anomaly.resolved_by_ref = resolved_by_ref
        anomaly.resolved_at = now
        anomaly.resolution_notes = resolution_notes
        anomaly.updated_at = now
        return anomaly

    @is_tool(ToolType.WRITE)
    def dismiss_access_anomaly(
        self,
        access_anomaly_ref: str,
        resolved_by_ref: str,
        resolution_notes: str,
    ) -> AccessAnomaly:
        """
        Dismiss an access anomaly as a false positive. 调用前 Agent 须向用户明确确认。

        参数：
            access_anomaly_ref: 引用the access anomaly.
            resolved_by_ref: 员工 ref：the person dismissing it.
            resolution_notes: 忽略原因说明。

        返回：
            AccessAnomaly：更新后的异常记录。

        异常：
            ValueError：若未找到异常或已解决/已忽略。
        """
        anomaly = self._get_access_anomaly(access_anomaly_ref)
        self._get_employee(resolved_by_ref)
        if anomaly.resolution_status in ("resolved", "dismissed"):
            raise ValueError(f"Anomaly is already {anomaly.resolution_status}")
        now = self._now_iso()
        anomaly.resolution_status = "dismissed"
        anomaly.resolved_by_ref = resolved_by_ref
        anomaly.resolved_at = now
        anomaly.resolution_notes = resolution_notes
        anomaly.updated_at = now
        return anomaly

    @is_tool(ToolType.WRITE)
    def update_access_anomaly_status(
        self,
        access_anomaly_ref: str,
        resolution_status: str,
    ) -> AccessAnomaly:
        """
        Update the resolution status of an access anomaly (e.g., to 'investigating'). 调用前 Agent 须向用户明确确认。

        参数：
            access_anomaly_ref: 引用the access anomaly.
            resolution_status: 新状态（open、investigating、resolved、dismissed）。

        返回：
            AccessAnomaly：更新后的异常记录。

        异常：
            ValueError：若未找到异常或状态无效。
        """
        anomaly = self._get_access_anomaly(access_anomaly_ref)
        valid_statuses = {"open", "investigating", "resolved", "dismissed"}
        if resolution_status not in valid_statuses:
            raise ValueError(f"Invalid resolution_status: {resolution_status}. Must be one of {valid_statuses}")
        anomaly.resolution_status = resolution_status
        anomaly.updated_at = self._now_iso()
        return anomaly

    # ===================================================================
    # 账号迁移（账号迁移与变更）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_account_migration_details(self, account_migration_ref: str) -> AccountMigration:
        """
        获取账号迁移的详情。

        参数：
            account_migration_ref: 账号迁移的唯一标识。

        返回：
            AccountMigration：账号迁移对象。

        异常：
            ValueError：若未找到迁移记录。
        """
        return self._get_account_migration(account_migration_ref)

    @is_tool(ToolType.READ)
    def list_account_migrations(
        self,
        employee_ref: Optional[str] = None,
        migration_status: Optional[str] = None,
        migration_type: Optional[str] = None,
    ) -> str:
        """
        列出账号迁移（可选筛选）。

        参数：
            employee_ref: 按员工筛选。
            migration_status: 按迁移状态筛选（pending, in_progress, completed, failed, cancelled).
            migration_type: 按迁移类型筛选（transfer, clone, merge, archive).

        返回：
            str：account migration summaries 的 JSON 数组。

        异常：
            ValueError：若引用实体不存在。
        """
        results = []
        for ref, mig in self.db.account_migration.items():
            if employee_ref is not None and mig.employee_ref != employee_ref:
                continue
            if migration_status is not None and mig.migration_status != migration_status:
                continue
            if migration_type is not None and mig.migration_type != migration_type:
                continue
            results.append({
                "account_migration_ref": mig.account_migration_ref,
                "employee_ref": mig.employee_ref,
                "source_system_ref": mig.source_system_ref,
                "target_system_ref": mig.target_system_ref,
                "migration_type": mig.migration_type,
                "migration_status": mig.migration_status,
                "requested_by_ref": mig.requested_by_ref,
                "requested_at": mig.requested_at,
                "completed_at": mig.completed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_account_migration(
        self,
        employee_ref: str,
        source_system_ref: str,
        source_account_ref: str,
        target_system_ref: str,
        migration_type: str,
        data_scope: str,
        requested_by_ref: str,
        notes: str = "",
    ) -> AccountMigration:
        """
        Create a new account migration request. 调用前 Agent 须向用户明确确认。

        参数：
            employee_ref: 被迁移账号所属员工。
            source_system_ref: 源 IT 系统 ref。
            source_account_ref: 源账号 ref。
            target_system_ref: 目标 IT 系统 ref。
            migration_type: 迁移类型（transfer、clone、merge、archive）。
            data_scope: 待迁移数据范围说明。
            requested_by_ref: 员工 ref：the requester.
            notes: 附加说明。

        返回：
            AccountMigration：新建的迁移记录。

        异常：
            ValueError：若引用实体不存在或参数无效。
        """
        self._get_employee(employee_ref)
        self._get_it_system(source_system_ref)
        self._get_it_system_account(source_account_ref)
        self._get_it_system(target_system_ref)
        self._get_employee(requested_by_ref)

        valid_types = {"transfer", "clone", "merge", "archive"}
        if migration_type not in valid_types:
            raise ValueError(f"Invalid migration_type: {migration_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("AM", self.db.account_migration)

        migration = AccountMigration(
            account_migration_ref=ref,
            employee_ref=employee_ref,
            source_system_ref=source_system_ref,
            source_account_ref=source_account_ref,
            target_system_ref=target_system_ref,
            target_account_ref=None,
            migration_type=migration_type,
            migration_status="pending",
            data_scope=data_scope,
            requested_by_ref=requested_by_ref,
            executed_by_ref=None,
            requested_at=now,
            completed_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.account_migration[ref] = migration
        return migration

    @is_tool(ToolType.WRITE)
    def update_account_migration_status(
        self,
        account_migration_ref: str,
        migration_status: str,
        executed_by_ref: Optional[str] = None,
        target_account_ref: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> AccountMigration:
        """
        Update the status of an account migration. 调用前 Agent 须向用户明确确认。

        参数：
            account_migration_ref: 引用the account migration.
            migration_status: 新状态（pending、in_progress、completed、failed、cancelled）。
            executed_by_ref: 员工 ref who executed the migration (required for completed).
            target_account_ref: 目标账号 ref（迁移完成时）。
            notes: 追加备注。

        返回：
            AccountMigration：更新后的迁移记录。

        异常：
            ValueError：若未找到迁移或状态流转无效。
        """
        mig = self._get_account_migration(account_migration_ref)
        valid_statuses = {"pending", "in_progress", "completed", "failed", "cancelled"}
        if migration_status not in valid_statuses:
            raise ValueError(f"Invalid migration_status: {migration_status}. Must be one of {valid_statuses}")

        now = self._now_iso()
        mig.migration_status = migration_status
        if executed_by_ref is not None:
            self._get_employee(executed_by_ref)
            mig.executed_by_ref = executed_by_ref
        if target_account_ref is not None:
            mig.target_account_ref = target_account_ref
        if migration_status == "completed":
            mig.completed_at = now
        if notes is not None:
            mig.notes = notes
        mig.updated_at = now
        return mig

    # ===================================================================
    # 邮箱账号管理（邮箱账号管理 / 邮件收发问题 / 邮箱容量与清理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_email_account_details(self, email_account_ref: str) -> EmailAccount:
        """
        获取邮箱账号的详情。

        参数：
            email_account_ref: 邮箱账号的唯一标识。

        返回：
            EmailAccount：邮箱账号对象。

        异常：
            ValueError：若未找到邮箱账号。
        """
        return self._get_email_account(email_account_ref)

    @is_tool(ToolType.READ)
    def list_email_accounts_for_employee(self, employee_ref: str) -> str:
        """
        列出某员工的全部邮箱账号。

        参数：
            employee_ref: 员工引用。

        返回：
            str：email account summaries 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, ea in self.db.email_account.items():
            if ea.employee_ref != employee_ref:
                continue
            results.append({
                "email_account_ref": ea.email_account_ref,
                "email_address": ea.email_address,
                "email_type": ea.email_type,
                "mailbox_provider": ea.mailbox_provider,
                "account_status": ea.account_status,
                "quota_bytes": ea.quota_bytes,
                "used_bytes": ea.used_bytes,
                "auto_reply_enabled": ea.auto_reply_enabled,
                "security_level": ea.security_level,
                "spam_filter_level": ea.spam_filter_level,
                "forwarding_address": ea.forwarding_address,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_email_account_ref_by_address(self, email_address: str) -> str:
        """
        按邮箱地址查找邮箱账号 ref。

        参数：
            email_address: 要查找的邮箱地址。

        返回：
            str：匹配到的 email_account_ref。

        异常：
            ValueError：若未匹配到邮箱账号。
        """
        search = email_address.lower()
        for ref, ea in self.db.email_account.items():
            if ea.email_address.lower() == search:
                return ref
        raise ValueError("Email account not found")

    @is_tool(ToolType.WRITE)
    def update_email_account_settings(
        self,
        email_account_ref: str,
        forwarding_address: Optional[str] = None,
        auto_reply_enabled: Optional[bool] = None,
        auto_reply_message: Optional[str] = None,
        spam_filter_level: Optional[str] = None,
    ) -> EmailAccount:
        """
        Update email account settings. 调用前 Agent 须向用户明确确认。

        参数：
            email_account_ref: 引用the email account.
            forwarding_address: 新转发地址（传空字符串表示清空）。
            auto_reply_enabled: 是否启用自动回复。
            auto_reply_message: 自动回复内容。
            spam_filter_level: 垃圾邮件过滤级别（low、medium、high、custom）。

        返回：
            EmailAccount：更新后的邮箱账号。

        异常：
            ValueError：若未找到邮箱账号或参数无效。
        """
        ea = self._get_email_account(email_account_ref)
        if forwarding_address is not None:
            ea.forwarding_address = forwarding_address if forwarding_address != "" else None
        if auto_reply_enabled is not None:
            ea.auto_reply_enabled = auto_reply_enabled
        if auto_reply_message is not None:
            ea.auto_reply_message = auto_reply_message if auto_reply_message != "" else None
        if spam_filter_level is not None:
            valid_levels = {"low", "medium", "high", "custom"}
            if spam_filter_level not in valid_levels:
                raise ValueError(f"Invalid spam_filter_level: {spam_filter_level}. Must be one of {valid_levels}")
            ea.spam_filter_level = spam_filter_level
        ea.updated_at = self._now_iso()
        return ea

    @is_tool(ToolType.WRITE)
    def update_email_account_status(
        self,
        email_account_ref: str,
        account_status: str,
    ) -> EmailAccount:
        """
        Update the status of an email account (activate, suspend, deactivate, archive). 调用前 Agent 须向用户明确确认。

        参数：
            email_account_ref: 引用the email account.
            account_status: 新状态（active、suspended、deactivated、archived）。

        返回：
            EmailAccount：更新后的邮箱账号。

        异常：
            ValueError：若未找到邮箱账号或状态无效。
        """
        ea = self._get_email_account(email_account_ref)
        valid_statuses = {"active", "suspended", "deactivated", "archived"}
        if account_status not in valid_statuses:
            raise ValueError(f"Invalid account_status: {account_status}. Must be one of {valid_statuses}")
        ea.account_status = account_status
        ea.updated_at = self._now_iso()
        return ea

    # ===================================================================
    # 邮件组（邮箱账号管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_email_distribution_list_details(self, email_distribution_list_ref: str) -> EmailDistributionList:
        """
        获取邮件组的详情。

        参数：
            email_distribution_list_ref: 邮件组的唯一标识。

        返回：
            EmailDistributionList：邮件组对象。

        异常：
            ValueError：若未找到邮件组。
        """
        return self._get_email_distribution_list(email_distribution_list_ref)

    @is_tool(ToolType.READ)
    def list_email_distribution_lists(
        self,
        list_type: Optional[str] = None,
        status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出邮件组（可选筛选）。

        参数：
            list_type: 按列表类型筛选（department, team, project, custom, all_company).
            status: 按状态筛选（active, archived, dissolved).
            department_ref: 按关联部门筛选。

        返回：
            str：distribution list summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, dl in self.db.email_distribution_list.items():
            if list_type is not None and dl.list_type != list_type:
                continue
            if status is not None and dl.status != status:
                continue
            if department_ref is not None and dl.department_ref != department_ref:
                continue
            results.append({
                "email_distribution_list_ref": dl.email_distribution_list_ref,
                "list_address": dl.list_address,
                "list_name": dl.list_name,
                "list_type": dl.list_type,
                "member_count": dl.member_count,
                "status": dl.status,
                "owner_employee_ref": dl.owner_employee_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_email_distribution_list_members(
        self,
        email_distribution_list_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        列出邮件组成员。

        参数：
            email_distribution_list_ref: 引用the distribution list.
            status: 可选按成员状态筛选（active、removed）。

        返回：
            str：member details 的 JSON 数组。

        异常：
            ValueError：若未找到邮件组。
        """
        self._get_email_distribution_list(email_distribution_list_ref)
        results = []
        for ref, m in self.db.email_distribution_list_member.items():
            if m.email_distribution_list_ref != email_distribution_list_ref:
                continue
            if status is not None and m.status != status:
                continue
            ea = self._get_email_account(m.email_account_ref)
            results.append({
                "email_distribution_list_member_ref": m.email_distribution_list_member_ref,
                "email_account_ref": m.email_account_ref,
                "email_address": ea.email_address,
                "role": m.role,
                "status": m.status,
                "added_at": m.added_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_member_to_email_distribution_list(
        self,
        email_distribution_list_ref: str,
        email_account_ref: str,
        role: str,
        added_by_ref: str,
    ) -> EmailDistributionListMember:
        """
        Add a member to an email distribution list. 调用前 Agent 须向用户明确确认。

        参数：
            email_distribution_list_ref: 引用the distribution list.
            email_account_ref: 引用the email account to add.
            role: 在列表中的角色（member、moderator、owner）。
            added_by_ref: 员工 ref：the person adding the member.

        返回：
            EmailDistributionListMember：新建的成员关系。

        异常：
            ValueError：若未找到邮件组或账号，或成员已存在。
        """
        dl = self._get_email_distribution_list(email_distribution_list_ref)
        self._get_email_account(email_account_ref)
        self._get_employee(added_by_ref)

        valid_roles = {"member", "moderator", "owner"}
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {valid_roles}")

        # 检查是否已有有效成员身份
        for m in self.db.email_distribution_list_member.values():
            if (m.email_distribution_list_ref == email_distribution_list_ref
                    and m.email_account_ref == email_account_ref
                    and m.status == "active"):
                raise ValueError("Member is already active in this distribution list")

        now = self._now_iso()
        ref = self._generate_ref("EDLM", self.db.email_distribution_list_member)

        member = EmailDistributionListMember(
            email_distribution_list_member_ref=ref,
            email_distribution_list_ref=email_distribution_list_ref,
            email_account_ref=email_account_ref,
            role=role,
            status="active",
            added_by_ref=added_by_ref,
            added_at=now,
            removed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.email_distribution_list_member[ref] = member
        dl.member_count += 1
        dl.updated_at = now
        return member

    @is_tool(ToolType.WRITE)
    def remove_member_from_email_distribution_list(
        self,
        email_distribution_list_member_ref: str,
    ) -> EmailDistributionListMember:
        """
        Remove a member from an email distribution list. 调用前 Agent 须向用户明确确认。

        参数：
            email_distribution_list_member_ref: 引用the membership record.

        返回：
            EmailDistributionListMember：更新后的成员关系。

        异常：
            ValueError：若未找到成员关系或已移除。
        """
        if email_distribution_list_member_ref not in self.db.email_distribution_list_member:
            raise ValueError("Distribution list member not found")
        m = self.db.email_distribution_list_member[email_distribution_list_member_ref]
        if m.status == "removed":
            raise ValueError("Member is already removed")
        now = self._now_iso()
        m.status = "removed"
        m.removed_at = now
        m.updated_at = now
        # 更新成员数量
        dl = self._get_email_distribution_list(m.email_distribution_list_ref)
        dl.member_count = max(0, dl.member_count - 1)
        dl.updated_at = now
        return m

    # ===================================================================
    # 邮箱安全（邮箱安全）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_email_security_event_details(self, email_security_event_ref: str) -> EmailSecurityEvent:
        """
        获取邮箱安全事件的详情。

        参数：
            email_security_event_ref: 邮箱安全事件的唯一标识。

        返回：
            EmailSecurityEvent：邮箱安全事件对象。

        异常：
            ValueError：若未找到事件。
        """
        return self._get_email_security_event(email_security_event_ref)

    @is_tool(ToolType.READ)
    def list_email_security_events(
        self,
        email_account_ref: Optional[str] = None,
        event_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出邮箱安全事件（可选筛选）。

        参数：
            email_account_ref: 按邮箱账号筛选。
            event_type: 按事件类型筛选。
            severity: 按严重程度筛选（low, medium, high, critical).
            status: 按状态筛选（open, investigating, resolved, dismissed).

        返回：
            str：email security event summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, evt in self.db.email_security_event.items():
            if email_account_ref is not None and evt.email_account_ref != email_account_ref:
                continue
            if event_type is not None and evt.event_type != event_type:
                continue
            if severity is not None and evt.severity != severity:
                continue
            if status is not None and evt.status != status:
                continue
            results.append({
                "email_security_event_ref": evt.email_security_event_ref,
                "email_account_ref": evt.email_account_ref,
                "event_type": evt.event_type,
                "severity": evt.severity,
                "source_address": evt.source_address,
                "subject": evt.subject,
                "description": evt.description,
                "action_taken": evt.action_taken,
                "status": evt.status,
                "occurred_at": evt.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def resolve_email_security_event(
        self,
        email_security_event_ref: str,
        resolved_by_ref: str,
    ) -> EmailSecurityEvent:
        """
        Resolve an email security event. 调用前 Agent 须向用户明确确认。

        参数：
            email_security_event_ref: 引用the email security event.
            resolved_by_ref: 员工 ref：the person resolving it.

        返回：
            EmailSecurityEvent：更新后的事件。

        异常：
            ValueError：若未找到事件或已解决/已忽略。
        """
        evt = self._get_email_security_event(email_security_event_ref)
        self._get_employee(resolved_by_ref)
        if evt.status in ("resolved", "dismissed"):
            raise ValueError(f"Event is already {evt.status}")
        now = self._now_iso()
        evt.status = "resolved"
        evt.resolved_by_ref = resolved_by_ref
        evt.resolved_at = now
        evt.updated_at = now
        return evt

    @is_tool(ToolType.WRITE)
    def dismiss_email_security_event(
        self,
        email_security_event_ref: str,
        resolved_by_ref: str,
    ) -> EmailSecurityEvent:
        """
        Dismiss an email security event. 调用前 Agent 须向用户明确确认。

        参数：
            email_security_event_ref: 引用the email security event.
            resolved_by_ref: 员工 ref：the person dismissing it.

        返回：
            EmailSecurityEvent：更新后的事件。

        异常：
            ValueError：若未找到事件或已解决/已忽略。
        """
        evt = self._get_email_security_event(email_security_event_ref)
        self._get_employee(resolved_by_ref)
        if evt.status in ("resolved", "dismissed"):
            raise ValueError(f"Event is already {evt.status}")
        now = self._now_iso()
        evt.status = "dismissed"
        evt.resolved_by_ref = resolved_by_ref
        evt.resolved_at = now
        evt.updated_at = now
        return evt

    # ===================================================================
    # 代码仓库（代码管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_code_repository_details(self, code_repository_ref: str) -> CodeRepository:
        """
        获取代码仓库的详情。

        参数：
            code_repository_ref: 代码仓库的唯一标识。

        返回：
            CodeRepository：代码仓库对象。

        异常：
            ValueError：若未找到仓库。
        """
        return self._get_code_repository(code_repository_ref)

    @is_tool(ToolType.READ)
    def list_code_repositories(
        self,
        platform: Optional[str] = None,
        visibility: Optional[str] = None,
        repository_status: Optional[str] = None,
        team_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出代码仓库（可选筛选）。

        参数：
            platform: 按平台筛选（gitlab, github, bitbucket, gitee).
            visibility: 按可见性筛选（public, internal, private).
            repository_status: 按仓库状态筛选（active, archived, deleted).
            team_ref: 按团队筛选。
            department_ref: 按部门筛选。
            owner_employee_ref: 按负责人筛选。

        返回：
            str：code repository summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, repo in self.db.code_repository.items():
            if platform is not None and repo.platform != platform:
                continue
            if visibility is not None and repo.visibility != visibility:
                continue
            if repository_status is not None and repo.repository_status != repository_status:
                continue
            if team_ref is not None and repo.team_ref != team_ref:
                continue
            if department_ref is not None and repo.department_ref != department_ref:
                continue
            if owner_employee_ref is not None and repo.owner_employee_ref != owner_employee_ref:
                continue
            results.append({
                "code_repository_ref": repo.code_repository_ref,
                "repository_name": repo.repository_name,
                "repository_slug": repo.repository_slug,
                "platform": repo.platform,
                "visibility": repo.visibility,
                "default_branch": repo.default_branch,
                "language_primary": repo.language_primary,
                "repository_status": repo.repository_status,
                "owner_employee_ref": repo.owner_employee_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_code_repository_ref_by_name(self, repository_name: str) -> str:
        """
        按名称查找代码仓库 ref（部分匹配，不区分大小写）。

        参数：
            repository_name: 仓库名称（可部分匹配）。

        返回：
            str：匹配到的 code_repository_ref。

        异常：
            ValueError：若未匹配到代码仓库。
        """
        search = repository_name.lower()
        for ref, repo in self.db.code_repository.items():
            if search in repo.repository_name.lower():
                return ref
        raise ValueError("Code repository not found")

    @is_tool(ToolType.READ)
    def list_code_repository_members(
        self,
        code_repository_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        列出代码仓库成员。

        参数：
            code_repository_ref: 引用the code repository.
            status: 可选按成员状态筛选（active、revoked）。

        返回：
            str：repository member details 的 JSON 数组。

        异常：
            ValueError：若未找到仓库。
        """
        self._get_code_repository(code_repository_ref)
        results = []
        for ref, m in self.db.code_repository_member.items():
            if m.code_repository_ref != code_repository_ref:
                continue
            if status is not None and m.status != status:
                continue
            emp = self._get_employee(m.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "code_repository_member_ref": m.code_repository_member_ref,
                "employee_ref": m.employee_ref,
                "display_name": up.display_name,
                "access_level": m.access_level,
                "status": m.status,
                "granted_at": m.granted_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_code_repository_member(
        self,
        code_repository_ref: str,
        employee_ref: str,
        access_level: str,
        granted_by_ref: str,
    ) -> CodeRepositoryMember:
        """
        Add a member to a code repository. 调用前 Agent 须向用户明确确认。

        参数：
            code_repository_ref: 引用the code repository.
            employee_ref: 员工 ref to add.
            access_level: 访问级别（guest、reporter、developer、maintainer、owner）。
            granted_by_ref: 员工 ref who granted access.

        返回：
            CodeRepositoryMember：新建的成员关系。

        异常：
            ValueError：若实体不存在、access_level 无效或成员已活跃。
        """
        self._get_code_repository(code_repository_ref)
        self._get_employee(employee_ref)
        self._get_employee(granted_by_ref)

        valid_levels = {"guest", "reporter", "developer", "maintainer", "owner"}
        if access_level not in valid_levels:
            raise ValueError(f"Invalid access_level: {access_level}. Must be one of {valid_levels}")

        for m in self.db.code_repository_member.values():
            if (m.code_repository_ref == code_repository_ref
                    and m.employee_ref == employee_ref
                    and m.status == "active"):
                raise ValueError("Employee is already an active member of this repository")

        now = self._now_iso()
        ref = self._generate_ref("CRM", self.db.code_repository_member)

        member = CodeRepositoryMember(
            code_repository_member_ref=ref,
            code_repository_ref=code_repository_ref,
            employee_ref=employee_ref,
            access_level=access_level,
            granted_by_ref=granted_by_ref,
            granted_at=now,
            revoked_at=None,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.code_repository_member[ref] = member
        return member

    @is_tool(ToolType.WRITE)
    def update_code_repository_member_access(
        self,
        code_repository_member_ref: str,
        access_level: str,
    ) -> CodeRepositoryMember:
        """
        Update the access level of a code repository member. 调用前 Agent 须向用户明确确认。

        参数：
            code_repository_member_ref: 引用the membership.
            access_level: 新访问级别（guest、reporter、developer、maintainer、owner）。

        返回：
            CodeRepositoryMember：更新后的成员关系。

        异常：
            ValueError：若未找到成员关系、已撤销或 access_level 无效。
        """
        if code_repository_member_ref not in self.db.code_repository_member:
            raise ValueError("Code repository member not found")
        m = self.db.code_repository_member[code_repository_member_ref]
        if m.status == "revoked":
            raise ValueError("Cannot update access for a revoked member")
        valid_levels = {"guest", "reporter", "developer", "maintainer", "owner"}
        if access_level not in valid_levels:
            raise ValueError(f"Invalid access_level: {access_level}. Must be one of {valid_levels}")
        m.access_level = access_level
        m.updated_at = self._now_iso()
        return m

    @is_tool(ToolType.WRITE)
    def revoke_code_repository_member(
        self,
        code_repository_member_ref: str,
    ) -> CodeRepositoryMember:
        """
        Revoke a member's access to a code repository. 调用前 Agent 须向用户明确确认。

        参数：
            code_repository_member_ref: 引用the membership.

        返回：
            CodeRepositoryMember：更新后的成员关系。

        异常：
            ValueError：若未找到成员关系或已撤销。
        """
        if code_repository_member_ref not in self.db.code_repository_member:
            raise ValueError("Code repository member not found")
        m = self.db.code_repository_member[code_repository_member_ref]
        if m.status == "revoked":
            raise ValueError("Member is already revoked")
        now = self._now_iso()
        m.status = "revoked"
        m.revoked_at = now
        m.updated_at = now
        return m

    # ===================================================================
    # 代码分支（代码管理 - 分支管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_code_branch_details(self, code_branch_ref: str) -> CodeBranch:
        """
        获取代码分支的详情。

        参数：
            code_branch_ref: 代码分支的唯一标识。

        返回：
            CodeBranch：代码分支对象。

        异常：
            ValueError：若未找到分支。
        """
        return self._get_code_branch(code_branch_ref)

    @is_tool(ToolType.READ)
    def list_code_branches(
        self,
        code_repository_ref: str,
        branch_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出代码仓库中的分支。

        参数：
            code_repository_ref: 引用the code repository.
            branch_type: 可选按分支类型筛选（feature、bugfix、hotfix、release、main、develop）。
            status: 可选按状态筛选（active、merged、deleted）。

        返回：
            str：branch summaries 的 JSON 数组。

        异常：
            ValueError：若未找到仓库。
        """
        self._get_code_repository(code_repository_ref)
        results = []
        for ref, b in self.db.code_branch.items():
            if b.code_repository_ref != code_repository_ref:
                continue
            if branch_type is not None and b.branch_type != branch_type:
                continue
            if status is not None and b.status != status:
                continue
            results.append({
                "code_branch_ref": b.code_branch_ref,
                "branch_name": b.branch_name,
                "branch_type": b.branch_type,
                "source_branch": b.source_branch,
                "created_by_ref": b.created_by_ref,
                "is_protected": b.is_protected,
                "status": b.status,
                "created_at": b.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_code_branch(
        self,
        code_repository_ref: str,
        branch_name: str,
        branch_type: str,
        source_branch: str,
        created_by_ref: str,
        is_protected: bool = False,
    ) -> CodeBranch:
        """
        Create a new branch in a code repository. 调用前 Agent 须向用户明确确认。

        参数：
            code_repository_ref: 引用the code repository.
            branch_name: 新分支名称。
            branch_type: 分支类型（feature、bugfix、hotfix、release、main、develop）。
            source_branch: 源分支名称。
            created_by_ref: 员工 ref：the creator.
            is_protected: 分支是否受保护。

        返回：
            CodeBranch：新建的分支。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_code_repository(code_repository_ref)
        self._get_employee(created_by_ref)

        valid_types = {"feature", "bugfix", "hotfix", "release", "main", "develop"}
        if branch_type not in valid_types:
            raise ValueError(f"Invalid branch_type: {branch_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("CB", self.db.code_branch)

        branch = CodeBranch(
            code_branch_ref=ref,
            code_repository_ref=code_repository_ref,
            branch_name=branch_name,
            branch_type=branch_type,
            source_branch=source_branch,
            created_by_ref=created_by_ref,
            is_protected=is_protected,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.code_branch[ref] = branch
        return branch

    @is_tool(ToolType.WRITE)
    def delete_code_branch(self, code_branch_ref: str) -> CodeBranch:
        """
        Delete (mark as deleted) a code branch. 调用前 Agent 须向用户明确确认。

        参数：
            code_branch_ref: 引用the code branch.

        返回：
            CodeBranch：更新后的分支。

        异常：
            ValueError：若未找到分支、受保护或已删除。
        """
        b = self._get_code_branch(code_branch_ref)
        if b.status == "deleted":
            raise ValueError("Branch is already deleted")
        if b.is_protected:
            raise ValueError("Cannot delete a protected branch")
        b.status = "deleted"
        b.updated_at = self._now_iso()
        return b

    # ===================================================================
    # 合并请求（代码合并请求 - 创建/提交/修改/变更/作废/取消/拆分/合并/转交/查询）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_merge_request_details(self, merge_request_ref: str) -> MergeRequest:
        """
        获取合并请求的详情。

        参数：
            merge_request_ref: 合并请求的唯一标识。

        返回：
            MergeRequest：合并请求对象。

        异常：
            ValueError：若未找到合并请求。
        """
        return self._get_merge_request(merge_request_ref)

    @is_tool(ToolType.READ)
    def list_merge_requests(
        self,
        code_repository_ref: Optional[str] = None,
        author_employee_ref: Optional[str] = None,
        assignee_employee_ref: Optional[str] = None,
        merge_request_status: Optional[str] = None,
        target_branch: Optional[str] = None,
        is_draft: Optional[bool] = None,
        label: Optional[str] = None,
    ) -> str:
        """
        列出合并请求（可选筛选）。

        参数：
            code_repository_ref: 按仓库筛选。
            author_employee_ref: 按作者筛选。
            assignee_employee_ref: 按经办人筛选。
            merge_request_status: 按合并请求状态筛选（open, merged, closed).
            target_branch: 按目标分支筛选。
            is_draft: 按草稿状态筛选。
            label: 按标签筛选（部分匹配）。

        返回：
            str：merge request summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, mr in self.db.merge_request.items():
            if code_repository_ref is not None and mr.code_repository_ref != code_repository_ref:
                continue
            if author_employee_ref is not None and mr.author_employee_ref != author_employee_ref:
                continue
            if assignee_employee_ref is not None and mr.assignee_employee_ref != assignee_employee_ref:
                continue
            if merge_request_status is not None and mr.merge_request_status != merge_request_status:
                continue
            if target_branch is not None and mr.target_branch != target_branch:
                continue
            if is_draft is not None and mr.is_draft != is_draft:
                continue
            if label is not None and not any(label.lower() in l.lower() for l in mr.labels):
                continue
            results.append({
                "merge_request_ref": mr.merge_request_ref,
                "code_repository_ref": mr.code_repository_ref,
                "merge_request_number": mr.merge_request_number,
                "title": mr.title,
                "source_branch": mr.source_branch,
                "target_branch": mr.target_branch,
                "author_employee_ref": mr.author_employee_ref,
                "assignee_employee_ref": mr.assignee_employee_ref,
                "merge_request_status": mr.merge_request_status,
                "merge_status": mr.merge_status,
                "is_draft": mr.is_draft,
                "labels": mr.labels,
                "lines_added": mr.lines_added,
                "lines_removed": mr.lines_removed,
                "files_changed": mr.files_changed,
                "created_at": mr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_merge_request(
        self,
        code_repository_ref: str,
        title: str,
        description: str,
        source_branch: str,
        target_branch: str,
        author_employee_ref: str,
        assignee_employee_ref: Optional[str] = None,
        is_draft: bool = False,
        labels: Optional[List[str]] = None,
    ) -> MergeRequest:
        """
        Create a new merge request. 调用前 Agent 须向用户明确确认。

        参数：
            code_repository_ref: 引用the code repository.
            title: 合并请求标题。
            description: 合并请求描述。
            source_branch: 源分支名。
            target_branch: 目标分支名。
            author_employee_ref: 员工 ref：the author.
            assignee_employee_ref: 可选经办人员工 ref。
            is_draft: 合并请求是否为草稿。
            labels: 可选标签列表。

        返回：
            MergeRequest：新建的合并请求。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_code_repository(code_repository_ref)
        self._get_employee(author_employee_ref)
        if assignee_employee_ref is not None:
            self._get_employee(assignee_employee_ref)

        # 计算本仓库下一个 MR 编号
        max_num = 0
        for mr in self.db.merge_request.values():
            if mr.code_repository_ref == code_repository_ref:
                max_num = max(max_num, mr.merge_request_number)

        now = self._now_iso()
        ref = self._generate_ref("MR", self.db.merge_request)

        merge_request = MergeRequest(
            merge_request_ref=ref,
            code_repository_ref=code_repository_ref,
            merge_request_number=max_num + 1,
            title=title,
            description=description,
            source_branch=source_branch,
            target_branch=target_branch,
            author_employee_ref=author_employee_ref,
            assignee_employee_ref=assignee_employee_ref,
            merge_request_status="open",
            merge_status="unchecked",
            is_draft=is_draft,
            labels=labels or [],
            parent_merge_request_ref=None,
            related_merge_request_refs=[],
            pipeline_ref=None,
            merged_by_ref=None,
            merged_at=None,
            closed_by_ref=None,
            closed_at=None,
            close_reason=None,
            lines_added=0,
            lines_removed=0,
            files_changed=0,
            created_at=now,
            updated_at=now,
        )
        self.db.merge_request[ref] = merge_request
        return merge_request

    @is_tool(ToolType.WRITE)
    def update_merge_request(
        self,
        merge_request_ref: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        assignee_employee_ref: Optional[str] = None,
        is_draft: Optional[bool] = None,
        labels: Optional[List[str]] = None,
        target_branch: Optional[str] = None,
    ) -> MergeRequest:
        """
        Update a merge request's details. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.
            title: 新标题。
            description: 新描述。
            assignee_employee_ref: 新经办人员工 ref。
            is_draft: 新草稿状态。
            labels: 新标签列表。
            target_branch: 新目标分支。

        返回：
            MergeRequest：更新后的合并请求。

        异常：
            ValueError：若未找到合并请求或未开放。
        """
        mr = self._get_merge_request(merge_request_ref)
        if mr.merge_request_status != "open":
            raise ValueError(f"Cannot update a merge request with status '{mr.merge_request_status}'")
        if title is not None:
            mr.title = title
        if description is not None:
            mr.description = description
        if assignee_employee_ref is not None:
            self._get_employee(assignee_employee_ref)
            mr.assignee_employee_ref = assignee_employee_ref
        if is_draft is not None:
            mr.is_draft = is_draft
        if labels is not None:
            mr.labels = labels
        if target_branch is not None:
            mr.target_branch = target_branch
        mr.updated_at = self._now_iso()
        return mr

    @is_tool(ToolType.WRITE)
    def merge_merge_request(
        self,
        merge_request_ref: str,
        merged_by_ref: str,
    ) -> MergeRequest:
        """
        Merge a merge request. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.
            merged_by_ref: 员工 ref：the person performing the merge.

        返回：
            MergeRequest：更新后的合并请求。

        异常：
            ValueError：若未找到 MR、未开放、为草稿或不可合并。
        """
        mr = self._get_merge_request(merge_request_ref)
        self._get_employee(merged_by_ref)
        if mr.merge_request_status != "open":
            raise ValueError(f"Cannot merge a merge request with status '{mr.merge_request_status}'")
        if mr.is_draft:
            raise ValueError("Cannot merge a draft merge request")
        if mr.merge_status == "cannot_be_merged":
            raise ValueError("Merge request has conflicts and cannot be merged")
        now = self._now_iso()
        mr.merge_request_status = "merged"
        mr.merged_by_ref = merged_by_ref
        mr.merged_at = now
        mr.updated_at = now
        return mr

    @is_tool(ToolType.WRITE)
    def close_merge_request(
        self,
        merge_request_ref: str,
        closed_by_ref: str,
        close_reason: str,
    ) -> MergeRequest:
        """
        Close a merge request without merging. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.
            closed_by_ref: 员工 ref：the person closing it.
            close_reason: 关闭原因（completed、superseded、abandoned、duplicate、other）。

        返回：
            MergeRequest：更新后的合并请求。

        异常：
            ValueError：若未找到 MR、未开放或 close_reason 无效。
        """
        mr = self._get_merge_request(merge_request_ref)
        self._get_employee(closed_by_ref)
        if mr.merge_request_status != "open":
            raise ValueError(f"Cannot close a merge request with status '{mr.merge_request_status}'")
        valid_reasons = {"completed", "superseded", "abandoned", "duplicate", "other"}
        if close_reason not in valid_reasons:
            raise ValueError(f"Invalid close_reason: {close_reason}. Must be one of {valid_reasons}")
        now = self._now_iso()
        mr.merge_request_status = "closed"
        mr.closed_by_ref = closed_by_ref
        mr.closed_at = now
        mr.close_reason = close_reason
        mr.updated_at = now
        return mr

    @is_tool(ToolType.WRITE)
    def reopen_merge_request(self, merge_request_ref: str) -> MergeRequest:
        """
        Reopen a closed merge request. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.

        返回：
            MergeRequest：更新后的合并请求。

        异常：
            ValueError：若未找到 MR 或非关闭状态。
        """
        mr = self._get_merge_request(merge_request_ref)
        if mr.merge_request_status != "closed":
            raise ValueError("Can only reopen a closed merge request")
        mr.merge_request_status = "open"
        mr.closed_by_ref = None
        mr.closed_at = None
        mr.close_reason = None
        mr.updated_at = self._now_iso()
        return mr

    @is_tool(ToolType.WRITE)
    def link_merge_requests(
        self,
        merge_request_ref: str,
        related_merge_request_ref: str,
    ) -> MergeRequest:
        """
        Link two merge requests as related (for split/merge tracking). 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the primary merge request.
            related_merge_request_ref: 引用the related merge request.

        返回：
            MergeRequest：更新后的主合并请求。

        异常：
            ValueError：若未找到任一合并请求或二者为同一 MR。
        """
        mr = self._get_merge_request(merge_request_ref)
        self._get_merge_request(related_merge_request_ref)
        if merge_request_ref == related_merge_request_ref:
            raise ValueError("Cannot link a merge request to itself")
        if related_merge_request_ref not in mr.related_merge_request_refs:
            mr.related_merge_request_refs.append(related_merge_request_ref)
        mr.updated_at = self._now_iso()
        return mr

    @is_tool(ToolType.WRITE)
    def set_merge_request_parent(
        self,
        merge_request_ref: str,
        parent_merge_request_ref: str,
    ) -> MergeRequest:
        """
        Set the parent merge request (for split MR tracking). 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the child merge request.
            parent_merge_request_ref: 引用the parent merge request.

        返回：
            MergeRequest：更新后的子合并请求。

        异常：
            ValueError：若未找到任一合并请求或二者为同一 MR。
        """
        mr = self._get_merge_request(merge_request_ref)
        self._get_merge_request(parent_merge_request_ref)
        if merge_request_ref == parent_merge_request_ref:
            raise ValueError("Cannot set a merge request as its own parent")
        mr.parent_merge_request_ref = parent_merge_request_ref
        mr.updated_at = self._now_iso()
        return mr

    # ===================================================================
    # 合并请求评审人（代码合并请求转交与角色管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_merge_request_reviewers(self, merge_request_ref: str) -> str:
        """
        列出合并请求的评审人。

        参数：
            merge_request_ref: 引用the merge request.

        返回：
            str：reviewer details 的 JSON 数组。

        异常：
            ValueError：若未找到合并请求。
        """
        self._get_merge_request(merge_request_ref)
        results = []
        for ref, r in self.db.merge_request_reviewer.items():
            if r.merge_request_ref != merge_request_ref:
                continue
            emp = self._get_employee(r.reviewer_employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "merge_request_reviewer_ref": r.merge_request_reviewer_ref,
                "reviewer_employee_ref": r.reviewer_employee_ref,
                "display_name": up.display_name,
                "reviewer_role": r.reviewer_role,
                "review_status": r.review_status,
                "review_comment": r.review_comment,
                "assigned_at": r.assigned_at,
                "reviewed_at": r.reviewed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_merge_request_reviewer(
        self,
        merge_request_ref: str,
        reviewer_employee_ref: str,
        reviewer_role: str,
        assigned_by_ref: str,
    ) -> MergeRequestReviewer:
        """
        Assign a reviewer to a merge request. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.
            reviewer_employee_ref: 员工 ref：the reviewer.
            reviewer_role: 角色（reviewer、approver、code_owner）。
            assigned_by_ref: 员工 ref：the person assigning.

        返回：
            MergeRequestReviewer：新建的评审指派。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_merge_request(merge_request_ref)
        self._get_employee(reviewer_employee_ref)
        self._get_employee(assigned_by_ref)

        valid_roles = {"reviewer", "approver", "code_owner"}
        if reviewer_role not in valid_roles:
            raise ValueError(f"Invalid reviewer_role: {reviewer_role}. Must be one of {valid_roles}")

        now = self._now_iso()
        ref = self._generate_ref("MRR", self.db.merge_request_reviewer)

        reviewer = MergeRequestReviewer(
            merge_request_reviewer_ref=ref,
            merge_request_ref=merge_request_ref,
            reviewer_employee_ref=reviewer_employee_ref,
            reviewer_role=reviewer_role,
            review_status="pending",
            review_comment=None,
            assigned_by_ref=assigned_by_ref,
            assigned_at=now,
            reviewed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.merge_request_reviewer[ref] = reviewer
        return reviewer

    @is_tool(ToolType.WRITE)
    def submit_merge_request_review(
        self,
        merge_request_reviewer_ref: str,
        review_status: str,
        review_comment: Optional[str] = None,
    ) -> MergeRequestReviewer:
        """
        Submit a review for a merge request. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_reviewer_ref: 引用the reviewer assignment.
            review_status: 评审结论（approved、changes_requested、commented）。
            review_comment: 可选评审意见。

        返回：
            MergeRequestReviewer：更新后的评审人。

        异常：
            ValueError：若未找到评审人或状态无效。
        """
        r = self._get_merge_request_reviewer(merge_request_reviewer_ref)
        valid_statuses = {"approved", "changes_requested", "commented"}
        if review_status not in valid_statuses:
            raise ValueError(f"Invalid review_status: {review_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        r.review_status = review_status
        r.review_comment = review_comment
        r.reviewed_at = now
        r.updated_at = now
        return r

    # ===================================================================
    # 合并请求活动（代码合并请求查询与状态跟踪）
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_merge_request_activities(self, merge_request_ref: str) -> str:
        """
        列出某合并请求上的活动/事件。

        参数：
            merge_request_ref: 引用the merge request.

        返回：
            str：activity details sorted by occurred_at 的 JSON 数组。

        异常：
            ValueError：若未找到合并请求。
        """
        self._get_merge_request(merge_request_ref)
        activities = []
        for ref, a in self.db.merge_request_activity.items():
            if a.merge_request_ref != merge_request_ref:
                continue
            activities.append(a)
        activities.sort(key=lambda x: x.occurred_at)
        results = []
        for a in activities:
            results.append({
                "merge_request_activity_ref": a.merge_request_activity_ref,
                "actor_employee_ref": a.actor_employee_ref,
                "activity_type": a.activity_type,
                "description": a.description,
                "changes": a.changes,
                "occurred_at": a.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_merge_request_activity(
        self,
        merge_request_ref: str,
        actor_employee_ref: str,
        activity_type: str,
        description: str,
        changes: Optional[Dict[str, Any]] = None,
    ) -> MergeRequestActivity:
        """
        Add an activity record to a merge request. 调用前 Agent 须向用户明确确认。

        参数：
            merge_request_ref: 引用the merge request.
            actor_employee_ref: 员工 ref：the actor.
            activity_type: 活动类型（created、commented、approved、changes_requested、merged、closed、reopened、assigned、label_changed、status_changed）。
            description: 活动描述。
            changes: 可选变更字典。

        返回：
            MergeRequestActivity：新建的活动记录。

        异常：
            ValueError：若实体不存在或 activity_type 无效。
        """
        self._get_merge_request(merge_request_ref)
        self._get_employee(actor_employee_ref)

        valid_types = {"created", "commented", "approved", "changes_requested", "merged", "closed", "reopened", "assigned", "label_changed", "status_changed"}
        if activity_type not in valid_types:
            raise ValueError(f"Invalid activity_type: {activity_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("MRA", self.db.merge_request_activity)

        activity = MergeRequestActivity(
            merge_request_activity_ref=ref,
            merge_request_ref=merge_request_ref,
            actor_employee_ref=actor_employee_ref,
            activity_type=activity_type,
            description=description,
            changes=changes,
            occurred_at=now,
            created_at=now,
        )
        self.db.merge_request_activity[ref] = activity
        return activity

    # ===================================================================
    # CI/CD 流水线与执行（代码构建部署）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_ci_cd_pipeline_details(self, ci_cd_pipeline_ref: str) -> CICDPipeline:
        """
        获取 CI/CD 流水线的详情。

        参数：
            ci_cd_pipeline_ref: CI/CD 流水线的唯一标识。

        返回：
            CICDPipeline：流水线对象。

        异常：
            ValueError：若未找到流水线。
        """
        return self._get_ci_cd_pipeline(ci_cd_pipeline_ref)

    @is_tool(ToolType.READ)
    def list_ci_cd_pipelines(
        self,
        code_repository_ref: Optional[str] = None,
        pipeline_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出CI/CD 流水线（可选筛选）。

        参数：
            code_repository_ref: 按代码仓库筛选。
            pipeline_type: 按流水线类型筛选（ci, cd, ci_cd).
            status: 按状态筛选（active, disabled, archived).

        返回：
            str：pipeline summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.ci_cd_pipeline.items():
            if code_repository_ref is not None and p.code_repository_ref != code_repository_ref:
                continue
            if pipeline_type is not None and p.pipeline_type != pipeline_type:
                continue
            if status is not None and p.status != status:
                continue
            results.append({
                "ci_cd_pipeline_ref": p.ci_cd_pipeline_ref,
                "pipeline_name": p.pipeline_name,
                "code_repository_ref": p.code_repository_ref,
                "pipeline_type": p.pipeline_type,
                "trigger_type": p.trigger_type,
                "status": p.status,
                "owner_employee_ref": p.owner_employee_ref,
                "description": p.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_pipeline_execution_details(self, pipeline_execution_ref: str) -> PipelineExecution:
        """
        获取流水线执行的详情。

        参数：
            pipeline_execution_ref: 流水线执行的唯一标识。

        返回：
            PipelineExecution：流水线执行对象。

        异常：
            ValueError：若未找到执行记录。
        """
        return self._get_pipeline_execution(pipeline_execution_ref)

    @is_tool(ToolType.READ)
    def list_pipeline_executions(
        self,
        ci_cd_pipeline_ref: Optional[str] = None,
        execution_status: Optional[str] = None,
        branch: Optional[str] = None,
        triggered_by_ref: Optional[str] = None,
    ) -> str:
        """
        列出流水线执行（可选筛选）。

        参数：
            ci_cd_pipeline_ref: 按流水线筛选。
            execution_status: 按执行状态筛选（pending, running, success, failed, cancelled, skipped).
            branch: 按分支筛选。
            triggered_by_ref: 按触发人员工筛选。

        返回：
            str：pipeline execution summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, pe in self.db.pipeline_execution.items():
            if ci_cd_pipeline_ref is not None and pe.ci_cd_pipeline_ref != ci_cd_pipeline_ref:
                continue
            if execution_status is not None and pe.execution_status != execution_status:
                continue
            if branch is not None and pe.branch != branch:
                continue
            if triggered_by_ref is not None and pe.triggered_by_ref != triggered_by_ref:
                continue
            results.append({
                "pipeline_execution_ref": pe.pipeline_execution_ref,
                "ci_cd_pipeline_ref": pe.ci_cd_pipeline_ref,
                "execution_number": pe.execution_number,
                "trigger_type": pe.trigger_type,
                "branch": pe.branch,
                "commit_sha": pe.commit_sha,
                "execution_status": pe.execution_status,
                "started_at": pe.started_at,
                "finished_at": pe.finished_at,
                "duration_seconds": pe.duration_seconds,
                "error_message": pe.error_message,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def trigger_pipeline_execution(
        self,
        ci_cd_pipeline_ref: str,
        branch: str,
        commit_sha: str,
        triggered_by_ref: str,
        trigger_type: str = "manual",
    ) -> PipelineExecution:
        """
        Trigger a new pipeline execution. 调用前 Agent 须向用户明确确认。

        参数：
            ci_cd_pipeline_ref: 引用the CI/CD pipeline.
            branch: 执行所用分支。
            commit_sha: Git 提交 SHA。
            triggered_by_ref: 员工 ref who triggered the execution.
            trigger_type: 触发类型（push、merge_request、schedule、manual、tag、api）。

        返回：
            PipelineExecution：新建的执行记录。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        pipeline = self._get_ci_cd_pipeline(ci_cd_pipeline_ref)
        self._get_employee(triggered_by_ref)

        if pipeline.status != "active":
            raise ValueError(f"Cannot trigger execution on a pipeline with status '{pipeline.status}'")

        valid_triggers = {"push", "merge_request", "schedule", "manual", "tag", "api"}
        if trigger_type not in valid_triggers:
            raise ValueError(f"Invalid trigger_type: {trigger_type}. Must be one of {valid_triggers}")

        # 计算下一次执行编号
        max_num = 0
        for pe in self.db.pipeline_execution.values():
            if pe.ci_cd_pipeline_ref == ci_cd_pipeline_ref:
                max_num = max(max_num, pe.execution_number)

        now = self._now_iso()
        ref = self._generate_ref("PE", self.db.pipeline_execution)

        execution = PipelineExecution(
            pipeline_execution_ref=ref,
            ci_cd_pipeline_ref=ci_cd_pipeline_ref,
            execution_number=max_num + 1,
            trigger_type=trigger_type,
            trigger_ref=triggered_by_ref,
            branch=branch,
            commit_sha=commit_sha,
            triggered_by_ref=triggered_by_ref,
            execution_status="pending",
            started_at=now,
            finished_at=None,
            duration_seconds=None,
            artifact_file_refs=[],
            log_uri="",
            error_message=None,
            created_at=now,
            updated_at=now,
        )
        self.db.pipeline_execution[ref] = execution
        return execution

    @is_tool(ToolType.WRITE)
    def cancel_pipeline_execution(self, pipeline_execution_ref: str) -> PipelineExecution:
        """
        Cancel a running or pending pipeline execution. 调用前 Agent 须向用户明确确认。

        参数：
            pipeline_execution_ref: 引用the pipeline execution.

        返回：
            PipelineExecution：更新后的执行记录。

        异常：
            ValueError：若未找到执行或不可取消。
        """
        pe = self._get_pipeline_execution(pipeline_execution_ref)
        if pe.execution_status not in ("pending", "running"):
            raise ValueError(f"Cannot cancel execution with status '{pe.execution_status}'")
        now = self._now_iso()
        pe.execution_status = "cancelled"
        pe.finished_at = now
        pe.updated_at = now
        return pe

    # ===================================================================
    # 部署与部署环境（代码构建部署）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_deployment_details(self, deployment_ref: str) -> Deployment:
        """
        获取部署的详情。

        参数：
            deployment_ref: 部署的唯一标识。

        返回：
            Deployment：部署对象。

        异常：
            ValueError：若未找到部署。
        """
        return self._get_deployment(deployment_ref)

    @is_tool(ToolType.READ)
    def list_deployments(
        self,
        deploy_environment_ref: Optional[str] = None,
        deployment_status: Optional[str] = None,
        deployed_by_ref: Optional[str] = None,
    ) -> str:
        """
        列出部署记录（可选筛选）。

        参数：
            deploy_environment_ref: 按部署环境筛选。
            deployment_status: 按部署状态筛选（pending, in_progress, success, failed, rolled_back, cancelled).
            deployed_by_ref: 按部署人筛选。

        返回：
            str：deployment summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, d in self.db.deployment.items():
            if deploy_environment_ref is not None and d.deploy_environment_ref != deploy_environment_ref:
                continue
            if deployment_status is not None and d.deployment_status != deployment_status:
                continue
            if deployed_by_ref is not None and d.deployed_by_ref != deployed_by_ref:
                continue
            results.append({
                "deployment_ref": d.deployment_ref,
                "pipeline_execution_ref": d.pipeline_execution_ref,
                "deploy_environment_ref": d.deploy_environment_ref,
                "version_tag": d.version_tag,
                "commit_sha": d.commit_sha,
                "deployed_by_ref": d.deployed_by_ref,
                "deployment_status": d.deployment_status,
                "deployment_strategy": d.deployment_strategy,
                "started_at": d.started_at,
                "finished_at": d.finished_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_deployment(
        self,
        pipeline_execution_ref: str,
        deploy_environment_ref: str,
        version_tag: str,
        commit_sha: str,
        deployed_by_ref: str,
        deployment_strategy: str = "rolling",
        notes: str = "",
    ) -> Deployment:
        """
        Create a new deployment. 调用前 Agent 须向用户明确确认。

        参数：
            pipeline_execution_ref: 引用the pipeline execution.
            deploy_environment_ref: 引用the target environment.
            version_tag: 版本标签。
            commit_sha: Git 提交 SHA。
            deployed_by_ref: 员工 ref：the deployer.
            deployment_strategy: 策略（rolling、blue_green、canary、recreate、manual）。
            notes: 附加说明。

        返回：
            Deployment：新建的部署。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_pipeline_execution(pipeline_execution_ref)
        self._get_deploy_environment(deploy_environment_ref)
        self._get_employee(deployed_by_ref)

        valid_strategies = {"rolling", "blue_green", "canary", "recreate", "manual"}
        if deployment_strategy not in valid_strategies:
            raise ValueError(f"Invalid deployment_strategy: {deployment_strategy}. Must be one of {valid_strategies}")

        now = self._now_iso()
        ref = self._generate_ref("DEP", self.db.deployment)

        deployment = Deployment(
            deployment_ref=ref,
            pipeline_execution_ref=pipeline_execution_ref,
            deploy_environment_ref=deploy_environment_ref,
            version_tag=version_tag,
            commit_sha=commit_sha,
            deployed_by_ref=deployed_by_ref,
            deployment_status="pending",
            deployment_strategy=deployment_strategy,
            rollback_ref=None,
            started_at=now,
            finished_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.deployment[ref] = deployment
        return deployment

    @is_tool(ToolType.WRITE)
    def update_deployment_status(
        self,
        deployment_ref: str,
        deployment_status: str,
    ) -> Deployment:
        """
        Update the status of a deployment. 调用前 Agent 须向用户明确确认。

        参数：
            deployment_ref: 引用the deployment.
            deployment_status: 新状态（pending、in_progress、success、failed、rolled_back、cancelled）。

        返回：
            Deployment：更新后的部署。

        异常：
            ValueError：若未找到部署或状态无效。
        """
        d = self._get_deployment(deployment_ref)
        valid_statuses = {"pending", "in_progress", "success", "failed", "rolled_back", "cancelled"}
        if deployment_status not in valid_statuses:
            raise ValueError(f"Invalid deployment_status: {deployment_status}. Must be one of {valid_statuses}")
        now = self._now_iso()
        d.deployment_status = deployment_status
        if deployment_status in ("success", "failed", "rolled_back", "cancelled"):
            d.finished_at = now
        d.updated_at = now
        return d

    @is_tool(ToolType.WRITE)
    def rollback_deployment(
        self,
        deployment_ref: str,
        deployed_by_ref: str,
        notes: str = "",
    ) -> Deployment:
        """
        Rollback a deployment by creating a new rollback deployment. 调用前 Agent 须向用户明确确认。

        参数：
            deployment_ref: 引用the deployment to rollback.
            deployed_by_ref: 员工 ref：the person performing the rollback.
            notes: 附加说明。

        返回：
            Deployment：新建的回滚部署。

        异常：
            ValueError：若未找到部署或不可回滚。
        """
        orig = self._get_deployment(deployment_ref)
        self._get_employee(deployed_by_ref)
        if orig.deployment_status not in ("success", "in_progress", "failed"):
            raise ValueError(f"Cannot rollback a deployment with status '{orig.deployment_status}'")

        now = self._now_iso()
        ref = self._generate_ref("DEP", self.db.deployment)

        rollback = Deployment(
            deployment_ref=ref,
            pipeline_execution_ref=orig.pipeline_execution_ref,
            deploy_environment_ref=orig.deploy_environment_ref,
            version_tag=orig.version_tag,
            commit_sha=orig.commit_sha,
            deployed_by_ref=deployed_by_ref,
            deployment_status="pending",
            deployment_strategy=orig.deployment_strategy,
            rollback_ref=deployment_ref,
            started_at=now,
            finished_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.deployment[ref] = rollback
        # 将原部署标记为已回滚
        orig.deployment_status = "rolled_back"
        orig.updated_at = now
        return rollback

    @is_tool(ToolType.READ)
    def get_deploy_environment_details(self, deploy_environment_ref: str) -> DeployEnvironment:
        """
        获取部署环境的详情。

        参数：
            deploy_environment_ref: 部署环境的唯一标识。

        返回：
            DeployEnvironment：部署环境对象。

        异常：
            ValueError：若未找到环境。
        """
        return self._get_deploy_environment(deploy_environment_ref)

    @is_tool(ToolType.READ)
    def list_deploy_environments(
        self,
        environment_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出部署环境（可选筛选）。

        参数：
            environment_type: 按环境类型筛选（development, staging, production, testing, demo).
            status: 按状态筛选（active, inactive, maintenance, decommissioned).

        返回：
            str：environment summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, env in self.db.deploy_environment.items():
            if environment_type is not None and env.environment_type != environment_type:
                continue
            if status is not None and env.status != status:
                continue
            results.append({
                "deploy_environment_ref": env.deploy_environment_ref,
                "environment_name": env.environment_name,
                "environment_code": env.environment_code,
                "environment_type": env.environment_type,
                "environment_url": env.environment_url,
                "status": env.status,
                "owner_employee_ref": env.owner_employee_ref,
            })
        return json.dumps(results)

    # ===================================================================
    # 开发环境（开发环境配置）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_dev_environment_details(self, dev_environment_ref: str) -> DevEnvironment:
        """
        获取开发环境的详情。

        参数：
            dev_environment_ref: 开发环境的唯一标识。

        返回：
            DevEnvironment：开发环境对象。

        异常：
            ValueError：若未找到环境。
        """
        return self._get_dev_environment(dev_environment_ref)

    @is_tool(ToolType.READ)
    def list_dev_environments_for_employee(self, employee_ref: str) -> str:
        """
        列出某员工的开发环境。

        参数：
            employee_ref: 员工引用。

        返回：
            str：dev environment summaries 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, env in self.db.dev_environment.items():
            if env.employee_ref != employee_ref:
                continue
            results.append({
                "dev_environment_ref": env.dev_environment_ref,
                "environment_name": env.environment_name,
                "environment_type": env.environment_type,
                "os_type": env.os_type,
                "os_version": env.os_version,
                "tools_installed": env.tools_installed,
                "status": env.status,
                "database_connections": env.database_connections,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def update_dev_environment(
        self,
        dev_environment_ref: str,
        tools_installed: Optional[List[str]] = None,
        env_variables: Optional[Dict[str, str]] = None,
        database_connections: Optional[List[str]] = None,
        notes: Optional[str] = None,
        status: Optional[str] = None,
    ) -> DevEnvironment:
        """
        Update a development environment configuration. 调用前 Agent 须向用户明确确认。

        参数：
            dev_environment_ref: 引用the dev environment.
            tools_installed: 更新后的已安装工具列表。
            env_variables: 更新后的环境变量。
            database_connections: 更新后的数据库连接。
            notes: 更新后的备注。
            status: 更新后状态（active、inactive、archived）。

        返回：
            DevEnvironment：更新后的开发环境。

        异常：
            ValueError：若未找到环境或参数无效。
        """
        env = self._get_dev_environment(dev_environment_ref)
        if tools_installed is not None:
            env.tools_installed = tools_installed
        if env_variables is not None:
            env.env_variables = env_variables
        if database_connections is not None:
            env.database_connections = database_connections
        if notes is not None:
            env.notes = notes
        if status is not None:
            valid_statuses = {"active", "inactive", "archived"}
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
            env.status = status
        env.updated_at = self._now_iso()
        return env

    # ===================================================================
    # IT 资源与资源申请（资源申请）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_it_resource_details(self, it_resource_ref: str) -> ITResource:
        """
        获取 IT 资源的详情。

        参数：
            it_resource_ref: IT 资源的唯一标识。

        返回：
            ITResource：IT 资源对象。

        异常：
            ValueError：若未找到资源。
        """
        return self._get_it_resource(it_resource_ref)

    @is_tool(ToolType.READ)
    def list_it_resources(
        self,
        resource_type: Optional[str] = None,
        resource_status: Optional[str] = None,
        department_ref: Optional[str] = None,
        allocated_to_ref: Optional[str] = None,
    ) -> str:
        """
        列出IT 资源（可选筛选）。

        参数：
            resource_type: 按资源类型筛选（server, vm, container, storage, database, load_balancer, gpu, other).
            resource_status: 按资源状态筛选（available, in_use, maintenance, decommissioned, reserved).
            department_ref: 按部门筛选。
            allocated_to_ref: 按分配对象筛选。

        返回：
            str：IT resource summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.it_resource.items():
            if resource_type is not None and r.resource_type != resource_type:
                continue
            if resource_status is not None and r.resource_status != resource_status:
                continue
            if department_ref is not None and r.department_ref != department_ref:
                continue
            if allocated_to_ref is not None and r.allocated_to_ref != allocated_to_ref:
                continue
            results.append({
                "it_resource_ref": r.it_resource_ref,
                "resource_name": r.resource_name,
                "resource_type": r.resource_type,
                "resource_identifier": r.resource_identifier,
                "location": r.location,
                "resource_status": r.resource_status,
                "allocated_to_ref": r.allocated_to_ref,
                "allocated_to_type": r.allocated_to_type,
                "owner_employee_ref": r.owner_employee_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_it_resource_request_details(self, it_resource_request_ref: str) -> ITResourceRequest:
        """
        获取 IT 资源申请的详情。

        参数：
            it_resource_request_ref: IT 资源申请的唯一标识。

        返回：
            ITResourceRequest：资源申请对象。

        异常：
            ValueError：若未找到申请。
        """
        return self._get_it_resource_request(it_resource_request_ref)

    @is_tool(ToolType.READ)
    def list_it_resource_requests(
        self,
        requester_employee_ref: Optional[str] = None,
        resource_type: Optional[str] = None,
        request_status: Optional[str] = None,
        urgency: Optional[str] = None,
    ) -> str:
        """
        列出IT 资源申请（可选筛选）。

        参数：
            requester_employee_ref: 按申请人筛选。
            resource_type: 按资源类型筛选。
            request_status: 按申请状态筛选（pending, approved, rejected, fulfilled, cancelled).
            urgency: 按紧急程度筛选（low, normal, high, critical).

        返回：
            str：resource request summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, rr in self.db.it_resource_request.items():
            if requester_employee_ref is not None and rr.requester_employee_ref != requester_employee_ref:
                continue
            if resource_type is not None and rr.resource_type != resource_type:
                continue
            if request_status is not None and rr.request_status != request_status:
                continue
            if urgency is not None and rr.urgency != urgency:
                continue
            results.append({
                "it_resource_request_ref": rr.it_resource_request_ref,
                "requester_employee_ref": rr.requester_employee_ref,
                "resource_type": rr.resource_type,
                "request_category": rr.request_category,
                "title": rr.title,
                "urgency": rr.urgency,
                "request_status": rr.request_status,
                "approved_by_ref": rr.approved_by_ref,
                "created_at": rr.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_it_resource_request(
        self,
        requester_employee_ref: str,
        resource_type: str,
        request_category: str,
        title: str,
        description: str,
        specifications: Dict[str, Any],
        business_justification: str,
        urgency: str = "normal",
    ) -> ITResourceRequest:
        """
        Create a new IT resource request. 调用前 Agent 须向用户明确确认。

        参数：
            requester_employee_ref: 员工 ref：the requester.
            resource_type: 资源类型（server、vm、container、storage、database、load_balancer、gpu、other）。
            request_category: 类别（new_allocation、upgrade、replacement、decommission、temporary）。
            title: 申请标题。
            description: 详细描述。
            specifications: 期望规格。
            business_justification: 业务理由。
            urgency: 紧急级别（low、normal、high、critical）。

        返回：
            ITResourceRequest：新建的申请。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(requester_employee_ref)

        valid_types = {"server", "vm", "container", "storage", "database", "load_balancer", "gpu", "other"}
        if resource_type not in valid_types:
            raise ValueError(f"Invalid resource_type: {resource_type}. Must be one of {valid_types}")
        valid_categories = {"new_allocation", "upgrade", "replacement", "decommission", "temporary"}
        if request_category not in valid_categories:
            raise ValueError(f"Invalid request_category: {request_category}. Must be one of {valid_categories}")
        valid_urgencies = {"low", "normal", "high", "critical"}
        if urgency not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {urgency}. Must be one of {valid_urgencies}")

        now = self._now_iso()
        ref = self._generate_ref("ITRR", self.db.it_resource_request)

        request = ITResourceRequest(
            it_resource_request_ref=ref,
            requester_employee_ref=requester_employee_ref,
            resource_type=resource_type,
            request_category=request_category,
            title=title,
            description=description,
            specifications=specifications,
            business_justification=business_justification,
            urgency=urgency,
            request_status="pending",
            approved_by_ref=None,
            approved_at=None,
            fulfilled_resource_ref=None,
            fulfilled_at=None,
            rejected_reason=None,
            expires_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.it_resource_request[ref] = request
        return request

    @is_tool(ToolType.WRITE)
    def approve_it_resource_request(
        self,
        it_resource_request_ref: str,
        approved_by_ref: str,
    ) -> ITResourceRequest:
        """
        Approve an IT resource request. 调用前 Agent 须向用户明确确认。

        参数：
            it_resource_request_ref: 引用the resource request.
            approved_by_ref: 员工 ref：the approver.

        返回：
            ITResourceRequest：更新后的申请。

        异常：
            ValueError：若未找到申请或非待处理。
        """
        rr = self._get_it_resource_request(it_resource_request_ref)
        self._get_employee(approved_by_ref)
        if rr.request_status != "pending":
            raise ValueError(f"Cannot approve a request with status '{rr.request_status}'")
        now = self._now_iso()
        rr.request_status = "approved"
        rr.approved_by_ref = approved_by_ref
        rr.approved_at = now
        rr.updated_at = now
        return rr

    @is_tool(ToolType.WRITE)
    def reject_it_resource_request(
        self,
        it_resource_request_ref: str,
        rejected_reason: str,
    ) -> ITResourceRequest:
        """
        Reject an IT resource request. 调用前 Agent 须向用户明确确认。

        参数：
            it_resource_request_ref: 引用the resource request.
            rejected_reason: 拒绝原因。

        返回：
            ITResourceRequest：更新后的申请。

        异常：
            ValueError：若未找到申请或非待处理。
        """
        rr = self._get_it_resource_request(it_resource_request_ref)
        if rr.request_status != "pending":
            raise ValueError(f"Cannot reject a request with status '{rr.request_status}'")
        rr.request_status = "rejected"
        rr.rejected_reason = rejected_reason
        rr.updated_at = self._now_iso()
        return rr

    @is_tool(ToolType.WRITE)
    def fulfill_it_resource_request(
        self,
        it_resource_request_ref: str,
        fulfilled_resource_ref: str,
    ) -> ITResourceRequest:
        """
        Fulfill an approved IT resource request by assigning a resource. 调用前 Agent 须向用户明确确认。

        参数：
            it_resource_request_ref: 引用the resource request.
            fulfilled_resource_ref: 引用the IT resource fulfilling the request.

        返回：
            ITResourceRequest：更新后的申请。

        异常：
            ValueError：若申请未批准或未找到资源。
        """
        rr = self._get_it_resource_request(it_resource_request_ref)
        self._get_it_resource(fulfilled_resource_ref)
        if rr.request_status != "approved":
            raise ValueError(f"Cannot fulfill a request with status '{rr.request_status}'")
        now = self._now_iso()
        rr.request_status = "fulfilled"
        rr.fulfilled_resource_ref = fulfilled_resource_ref
        rr.fulfilled_at = now
        rr.updated_at = now
        return rr

    @is_tool(ToolType.WRITE)
    def cancel_it_resource_request(self, it_resource_request_ref: str) -> ITResourceRequest:
        """
        Cancel an IT resource request. 调用前 Agent 须向用户明确确认。

        参数：
            it_resource_request_ref: 引用the resource request.

        返回：
            ITResourceRequest：更新后的申请。

        异常：
            ValueError：若未找到申请或不可取消。
        """
        rr = self._get_it_resource_request(it_resource_request_ref)
        if rr.request_status not in ("pending", "approved"):
            raise ValueError(f"Cannot cancel a request with status '{rr.request_status}'")
        rr.request_status = "cancelled"
        rr.updated_at = self._now_iso()
        return rr

    # ===================================================================
    # 数据源与数据访问（数据访问获取）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_data_source_details(self, data_source_ref: str) -> DataSource:
        """
        获取数据源的详情。

        参数：
            data_source_ref: 数据源的唯一标识。

        返回：
            DataSource：数据源对象。

        异常：
            ValueError：若未找到数据源。
        """
        return self._get_data_source(data_source_ref)

    @is_tool(ToolType.READ)
    def list_data_sources(
        self,
        source_type: Optional[str] = None,
        connection_type: Optional[str] = None,
        sensitivity_level: Optional[str] = None,
        status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出数据源（可选筛选）。

        参数：
            source_type: 按数据源类型筛选（database, api, file, stream, data_warehouse, data_lake).
            connection_type: 按连接类型筛选。
            sensitivity_level: 按敏感级别筛选（public, internal, confidential, restricted).
            status: 按状态筛选（active, inactive, deprecated, maintenance).
            department_ref: 按部门筛选。

        返回：
            str：data source summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ds in self.db.data_source.items():
            if source_type is not None and ds.source_type != source_type:
                continue
            if connection_type is not None and ds.connection_type != connection_type:
                continue
            if sensitivity_level is not None and ds.sensitivity_level != sensitivity_level:
                continue
            if status is not None and ds.status != status:
                continue
            if department_ref is not None and ds.department_ref != department_ref:
                continue
            results.append({
                "data_source_ref": ds.data_source_ref,
                "source_name": ds.source_name,
                "source_type": ds.source_type,
                "connection_type": ds.connection_type,
                "host": ds.host,
                "port": ds.port,
                "database_name": ds.database_name,
                "sensitivity_level": ds.sensitivity_level,
                "status": ds.status,
                "owner_employee_ref": ds.owner_employee_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_data_access_grant_details(self, data_access_grant_ref: str) -> DataAccessGrant:
        """
        获取数据访问授权的详情。

        参数：
            data_access_grant_ref: 数据访问授权的唯一标识。

        返回：
            DataAccessGrant：数据访问授权对象。

        异常：
            ValueError：若未找到授权。
        """
        return self._get_data_access_grant(data_access_grant_ref)

    @is_tool(ToolType.READ)
    def list_data_access_grants(
        self,
        data_source_ref: Optional[str] = None,
        grantee_employee_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出数据访问授权（可选筛选）。

        参数：
            data_source_ref: 按数据源筛选。
            grantee_employee_ref: 按被授权人员工筛选。
            status: 按状态筛选（active, revoked, expired).

        返回：
            str：data access grant summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, g in self.db.data_access_grant.items():
            if data_source_ref is not None and g.data_source_ref != data_source_ref:
                continue
            if grantee_employee_ref is not None and g.grantee_employee_ref != grantee_employee_ref:
                continue
            if status is not None and g.status != status:
                continue
            results.append({
                "data_access_grant_ref": g.data_access_grant_ref,
                "data_source_ref": g.data_source_ref,
                "grantee_employee_ref": g.grantee_employee_ref,
                "access_level": g.access_level,
                "scope": g.scope,
                "granted_by_ref": g.granted_by_ref,
                "granted_at": g.granted_at,
                "expires_at": g.expires_at,
                "status": g.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def grant_data_access(
        self,
        data_source_ref: str,
        grantee_employee_ref: str,
        access_level: str,
        scope: str,
        granted_by_ref: str,
        business_justification: str,
        expires_at: Optional[str] = None,
    ) -> DataAccessGrant:
        """
        Grant data access to an employee. 调用前 Agent 须向用户明确确认。

        参数：
            data_source_ref: 引用the data source.
            grantee_employee_ref: 员工 ref：the grantee.
            access_level: 访问级别（read、write、admin、full）。
            scope: 访问范围。
            granted_by_ref: 员工 ref：the granter.
            business_justification: 授权业务理由。
            expires_at: 可选过期时间。

        返回：
            DataAccessGrant：新建的授权。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_data_source(data_source_ref)
        self._get_employee(grantee_employee_ref)
        self._get_employee(granted_by_ref)

        valid_levels = {"read", "write", "admin", "full"}
        if access_level not in valid_levels:
            raise ValueError(f"Invalid access_level: {access_level}. Must be one of {valid_levels}")

        now = self._now_iso()
        ref = self._generate_ref("DAG", self.db.data_access_grant)

        grant = DataAccessGrant(
            data_access_grant_ref=ref,
            data_source_ref=data_source_ref,
            grantee_employee_ref=grantee_employee_ref,
            access_level=access_level,
            scope=scope,
            granted_by_ref=granted_by_ref,
            granted_at=now,
            expires_at=expires_at,
            status="active",
            business_justification=business_justification,
            created_at=now,
            updated_at=now,
        )
        self.db.data_access_grant[ref] = grant
        return grant

    @is_tool(ToolType.WRITE)
    def revoke_data_access_grant(self, data_access_grant_ref: str) -> DataAccessGrant:
        """
        Revoke a data access grant. 调用前 Agent 须向用户明确确认。

        参数：
            data_access_grant_ref: 引用the data access grant.

        返回：
            DataAccessGrant：更新后的授权。

        异常：
            ValueError：若未找到授权或已撤销/已过期。
        """
        g = self._get_data_access_grant(data_access_grant_ref)
        if g.status in ("revoked", "expired"):
            raise ValueError(f"Grant is already {g.status}")
        g.status = "revoked"
        g.updated_at = self._now_iso()
        return g

    # ===================================================================
    # 数据资产（数据资产查询）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_data_asset_details(self, data_asset_ref: str) -> DataAsset:
        """
        获取数据资产的详情。

        参数：
            data_asset_ref: 数据资产的唯一标识。

        返回：
            DataAsset：数据资产对象。

        异常：
            ValueError：若未找到数据资产。
        """
        return self._get_data_asset(data_asset_ref)

    @is_tool(ToolType.READ)
    def list_data_assets(
        self,
        data_source_ref: Optional[str] = None,
        asset_type: Optional[str] = None,
        sensitivity_level: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出数据资产（可选筛选）。

        参数：
            data_source_ref: 按数据源筛选。
            asset_type: 按资产类型筛选（table, view, collection, index, topic, bucket, file, api_endpoint).
            sensitivity_level: 按敏感级别筛选（public, internal, confidential, restricted).
            status: 按状态筛选（active, deprecated, archived).
            tag: 按标签筛选（部分匹配）。
            owner_employee_ref: 按负责人筛选。

        返回：
            str：data asset summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, a in self.db.data_asset.items():
            if data_source_ref is not None and a.data_source_ref != data_source_ref:
                continue
            if asset_type is not None and a.asset_type != asset_type:
                continue
            if sensitivity_level is not None and a.sensitivity_level != sensitivity_level:
                continue
            if status is not None and a.status != status:
                continue
            if tag is not None and not any(tag.lower() in t.lower() for t in a.tags):
                continue
            if owner_employee_ref is not None and a.owner_employee_ref != owner_employee_ref:
                continue
            results.append({
                "data_asset_ref": a.data_asset_ref,
                "data_source_ref": a.data_source_ref,
                "asset_name": a.asset_name,
                "asset_type": a.asset_type,
                "schema_name": a.schema_name,
                "sensitivity_level": a.sensitivity_level,
                "update_frequency": a.update_frequency,
                "row_count": a.row_count,
                "tags": a.tags,
                "status": a.status,
                "owner_employee_ref": a.owner_employee_ref,
                "steward_employee_ref": a.steward_employee_ref,
                "description": a.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def search_data_assets(self, keyword: str) -> str:
        """
        按关键词搜索数据资产（名称、描述、标签、schema）。

        参数：
            keyword: Search keyword（不区分大小写）。

        返回：
            str：匹配「data asset summaries」的 JSON 数组。

        异常：
            ValueError：若关键词为空。
        """
        if not keyword.strip():
            raise ValueError("Search keyword cannot be empty")
        search = keyword.lower()
        results = []
        for ref, a in self.db.data_asset.items():
            match = (
                search in a.asset_name.lower()
                or search in a.description.lower()
                or search in a.schema_name.lower()
                or any(search in t.lower() for t in a.tags)
            )
            if match:
                results.append({
                    "data_asset_ref": a.data_asset_ref,
                    "data_source_ref": a.data_source_ref,
                    "asset_name": a.asset_name,
                    "asset_type": a.asset_type,
                    "schema_name": a.schema_name,
                    "sensitivity_level": a.sensitivity_level,
                    "status": a.status,
                    "description": a.description,
                    "tags": a.tags,
                })
        return json.dumps(results)

    # ===================================================================
    # 数据传输任务（数据导入导出）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_data_transfer_job_details(self, data_transfer_job_ref: str) -> DataTransferJob:
        """
        获取数据传输任务的详情。

        参数：
            data_transfer_job_ref: 数据传输任务的唯一标识。

        返回：
            DataTransferJob：数据传输任务对象。

        异常：
            ValueError：若未找到任务。
        """
        return self._get_data_transfer_job(data_transfer_job_ref)

    @is_tool(ToolType.READ)
    def list_data_transfer_jobs(
        self,
        initiated_by_ref: Optional[str] = None,
        transfer_type: Optional[str] = None,
        job_status: Optional[str] = None,
        source_data_source_ref: Optional[str] = None,
        target_data_source_ref: Optional[str] = None,
    ) -> str:
        """
        列出数据传输任务（可选筛选）。

        参数：
            initiated_by_ref: 按发起人筛选。
            transfer_type: 按传输类型筛选（import, export, sync, migration, backup).
            job_status: 按任务状态筛选（pending, running, completed, failed, cancelled).
            source_data_source_ref: 按源数据源筛选。
            target_data_source_ref: 按目标数据源筛选。

        返回：
            str：data transfer job summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, j in self.db.data_transfer_job.items():
            if initiated_by_ref is not None and j.initiated_by_ref != initiated_by_ref:
                continue
            if transfer_type is not None and j.transfer_type != transfer_type:
                continue
            if job_status is not None and j.job_status != job_status:
                continue
            if source_data_source_ref is not None and j.source_data_source_ref != source_data_source_ref:
                continue
            if target_data_source_ref is not None and j.target_data_source_ref != target_data_source_ref:
                continue
            results.append({
                "data_transfer_job_ref": j.data_transfer_job_ref,
                "job_name": j.job_name,
                "transfer_type": j.transfer_type,
                "source_data_source_ref": j.source_data_source_ref,
                "target_data_source_ref": j.target_data_source_ref,
                "data_format": j.data_format,
                "record_count": j.record_count,
                "job_status": j.job_status,
                "started_at": j.started_at,
                "completed_at": j.completed_at,
                "error_message": j.error_message,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_data_transfer_job(
        self,
        job_name: str,
        transfer_type: str,
        data_format: str,
        initiated_by_ref: str,
        source_data_source_ref: Optional[str] = None,
        target_data_source_ref: Optional[str] = None,
        source_file_ref: Optional[str] = None,
        target_file_ref: Optional[str] = None,
    ) -> DataTransferJob:
        """
        Create a new data transfer job. 调用前 Agent 须向用户明确确认。

        参数：
            job_name: 任务名称。
            transfer_type: 类型（import、export、sync、migration、backup）。
            data_format: 格式（csv、json、parquet、avro、xml、sql、excel、other）。
            initiated_by_ref: 员工 ref：the initiator.
            source_data_source_ref: 可选源数据源 ref。
            target_data_source_ref: 可选目标数据源 ref。
            source_file_ref: 可选源文件 ref。
            target_file_ref: 可选目标文件 ref。

        返回：
            DataTransferJob：新建的任务。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(initiated_by_ref)

        valid_types = {"import", "export", "sync", "migration", "backup"}
        if transfer_type not in valid_types:
            raise ValueError(f"Invalid transfer_type: {transfer_type}. Must be one of {valid_types}")
        valid_formats = {"csv", "json", "parquet", "avro", "xml", "sql", "excel", "other"}
        if data_format not in valid_formats:
            raise ValueError(f"Invalid data_format: {data_format}. Must be one of {valid_formats}")

        if source_data_source_ref is not None:
            self._get_data_source(source_data_source_ref)
        if target_data_source_ref is not None:
            self._get_data_source(target_data_source_ref)

        now = self._now_iso()
        ref = self._generate_ref("DTJ", self.db.data_transfer_job)

        job = DataTransferJob(
            data_transfer_job_ref=ref,
            job_name=job_name,
            transfer_type=transfer_type,
            source_data_source_ref=source_data_source_ref,
            target_data_source_ref=target_data_source_ref,
            source_file_ref=source_file_ref,
            target_file_ref=target_file_ref,
            data_format=data_format,
            record_count=None,
            file_size_bytes=None,
            initiated_by_ref=initiated_by_ref,
            job_status="pending",
            started_at=None,
            completed_at=None,
            error_message=None,
            created_at=now,
            updated_at=now,
        )
        self.db.data_transfer_job[ref] = job
        return job

    @is_tool(ToolType.WRITE)
    def cancel_data_transfer_job(self, data_transfer_job_ref: str) -> DataTransferJob:
        """
        Cancel a data transfer job. 调用前 Agent 须向用户明确确认。

        参数：
            data_transfer_job_ref: 引用the data transfer job.

        返回：
            DataTransferJob：更新后的任务。

        异常：
            ValueError：若未找到任务或不可取消。
        """
        j = self._get_data_transfer_job(data_transfer_job_ref)
        if j.job_status not in ("pending", "running"):
            raise ValueError(f"Cannot cancel a job with status '{j.job_status}'")
        j.job_status = "cancelled"
        j.updated_at = self._now_iso()
        return j

    # ===================================================================
    # 网络分区与 VPN（内网连接）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_network_zone_details(self, network_zone_ref: str) -> NetworkZone:
        """
        获取网络分区的详情。

        参数：
            network_zone_ref: 网络分区的唯一标识。

        返回：
            NetworkZone：网络分区对象。

        异常：
            ValueError：若未找到网络分区。
        """
        return self._get_network_zone(network_zone_ref)

    @is_tool(ToolType.READ)
    def list_network_zones(
        self,
        zone_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出网络分区（可选筛选）。

        参数：
            zone_type: 按分区类型筛选（corporate, dmz, guest, production, development, restricted).
            status: 按状态筛选（active, inactive, maintenance).

        返回：
            str：network zone summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, nz in self.db.network_zone.items():
            if zone_type is not None and nz.zone_type != zone_type:
                continue
            if status is not None and nz.status != status:
                continue
            results.append({
                "network_zone_ref": nz.network_zone_ref,
                "zone_name": nz.zone_name,
                "zone_type": nz.zone_type,
                "cidr_range": nz.cidr_range,
                "location": nz.location,
                "gateway": nz.gateway,
                "status": nz.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_vpn_connection_details(self, vpn_connection_ref: str) -> VPNConnection:
        """
        获取 VPN 连接的详情。

        参数：
            vpn_connection_ref: VPN 连接的唯一标识。

        返回：
            VPNConnection：VPN 连接对象。

        异常：
            ValueError：若未找到 VPN 连接。
        """
        return self._get_vpn_connection(vpn_connection_ref)

    @is_tool(ToolType.READ)
    def list_vpn_connections_for_employee(self, employee_ref: str) -> str:
        """
        列出某员工的 VPN 连接。

        参数：
            employee_ref: 员工引用。

        返回：
            str：VPN connection summaries 的 JSON 数组。

        异常：
            ValueError：若未找到员工。
        """
        self._get_employee(employee_ref)
        results = []
        for ref, vpn in self.db.vpn_connection.items():
            if vpn.employee_ref != employee_ref:
                continue
            results.append({
                "vpn_connection_ref": vpn.vpn_connection_ref,
                "vpn_profile": vpn.vpn_profile,
                "assigned_ip": vpn.assigned_ip,
                "connection_status": vpn.connection_status,
                "last_connected_at": vpn.last_connected_at,
                "last_disconnected_at": vpn.last_disconnected_at,
            })
        return json.dumps(results)

    # ===================================================================
    # 访客 Wi‑Fi（访客网络）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_guest_wifi_credential_details(self, guest_wifi_credential_ref: str) -> GuestWifiCredential:
        """
        获取访客 Wi‑Fi 凭证的详情。

        参数：
            guest_wifi_credential_ref: 访客 Wi‑Fi 凭证的唯一标识。

        返回：
            GuestWifiCredential：凭证对象。

        异常：
            ValueError：若未找到凭证。
        """
        return self._get_guest_wifi_credential(guest_wifi_credential_ref)

    @is_tool(ToolType.READ)
    def list_guest_wifi_credentials(
        self,
        host_employee_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出访客 Wi‑Fi 凭证（可选筛选）。

        参数：
            host_employee_ref: 按接待人员工筛选。
            status: 按状态筛选（active, expired, revoked).

        返回：
            str：guest Wi-Fi credential summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, cred in self.db.guest_wifi_credential.items():
            if host_employee_ref is not None and cred.host_employee_ref != host_employee_ref:
                continue
            if status is not None and cred.status != status:
                continue
            results.append({
                "guest_wifi_credential_ref": cred.guest_wifi_credential_ref,
                "guest_name": cred.guest_name,
                "guest_company": cred.guest_company,
                "host_employee_ref": cred.host_employee_ref,
                "ssid": cred.ssid,
                "access_code": cred.access_code,
                "valid_from": cred.valid_from,
                "valid_until": cred.valid_until,
                "max_devices": cred.max_devices,
                "status": cred.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_guest_wifi_credential(
        self,
        guest_name: str,
        guest_company: str,
        guest_phone: str,
        host_employee_ref: str,
        ssid: str,
        access_code: str,
        valid_from: str,
        valid_until: str,
        max_devices: int = 3,
        bandwidth_limit_mbps: Optional[int] = None,
        network_zone_ref: Optional[str] = None,
    ) -> GuestWifiCredential:
        """
        Create a guest Wi-Fi credential. 调用前 Agent 须向用户明确确认。

        参数：
            guest_name: 访客姓名。
            guest_company: 访客公司。
            guest_phone: 访客电话。
            host_employee_ref: 接待人员工 ref。
            ssid: Wi‑Fi 网络名称（SSID）。
            access_code: 访问码/密码。
            valid_from: 有效期开始（ISO 8601）。
            valid_until: 有效期结束（ISO 8601）。
            max_devices: 最大并发设备数。
            bandwidth_limit_mbps: 可选带宽上限（Mbps）。
            network_zone_ref: 可选网络分区 ref。

        返回：
            GuestWifiCredential：新建的凭证。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(host_employee_ref)
        if network_zone_ref is not None:
            self._get_network_zone(network_zone_ref)

        now = self._now_iso()
        ref = self._generate_ref("GWC", self.db.guest_wifi_credential)

        cred = GuestWifiCredential(
            guest_wifi_credential_ref=ref,
            guest_name=guest_name,
            guest_company=guest_company,
            guest_phone=guest_phone,
            host_employee_ref=host_employee_ref,
            ssid=ssid,
            access_code=access_code,
            network_zone_ref=network_zone_ref,
            valid_from=valid_from,
            valid_until=valid_until,
            max_devices=max_devices,
            bandwidth_limit_mbps=bandwidth_limit_mbps,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.guest_wifi_credential[ref] = cred
        return cred

    @is_tool(ToolType.WRITE)
    def revoke_guest_wifi_credential(self, guest_wifi_credential_ref: str) -> GuestWifiCredential:
        """
        Revoke a guest Wi-Fi credential. 调用前 Agent 须向用户明确确认。

        参数：
            guest_wifi_credential_ref: 引用the credential.

        返回：
            GuestWifiCredential：更新后的凭证。

        异常：
            ValueError：若未找到凭证或已撤销/已过期。
        """
        cred = self._get_guest_wifi_credential(guest_wifi_credential_ref)
        if cred.status in ("revoked", "expired"):
            raise ValueError(f"Credential is already {cred.status}")
        cred.status = "revoked"
        cred.updated_at = self._now_iso()
        return cred

    # ===================================================================
    # 网络访问规则（网络权限管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_network_access_rule_details(self, network_access_rule_ref: str) -> NetworkAccessRule:
        """
        获取网络访问规则的详情。

        参数：
            network_access_rule_ref: 网络访问规则的唯一标识。

        返回：
            NetworkAccessRule：网络访问规则对象。

        异常：
            ValueError：若未找到规则。
        """
        return self._get_network_access_rule(network_access_rule_ref)

    @is_tool(ToolType.READ)
    def list_network_access_rules(
        self,
        network_zone_ref: Optional[str] = None,
        subject_type: Optional[str] = None,
        subject_ref: Optional[str] = None,
        action: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出网络访问规则（可选筛选）。

        参数：
            network_zone_ref: 按网络分区筛选。
            subject_type: 按主体类型筛选（employee, team, department, role, ip_range).
            subject_ref: 按主体 ref 筛选。
            action: 按动作筛选（allow, deny).
            status: 按状态筛选（active, disabled, expired).

        返回：
            str：network access rule summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, r in self.db.network_access_rule.items():
            if network_zone_ref is not None and r.network_zone_ref != network_zone_ref:
                continue
            if subject_type is not None and r.subject_type != subject_type:
                continue
            if subject_ref is not None and r.subject_ref != subject_ref:
                continue
            if action is not None and r.action != action:
                continue
            if status is not None and r.status != status:
                continue
            results.append({
                "network_access_rule_ref": r.network_access_rule_ref,
                "rule_name": r.rule_name,
                "subject_type": r.subject_type,
                "subject_ref": r.subject_ref,
                "network_zone_ref": r.network_zone_ref,
                "target_resource": r.target_resource,
                "protocol": r.protocol,
                "port_range": r.port_range,
                "action": r.action,
                "priority": r.priority,
                "status": r.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_network_access_rule(
        self,
        rule_name: str,
        subject_type: str,
        subject_ref: str,
        network_zone_ref: str,
        target_resource: str,
        protocol: str,
        port_range: str,
        action: str,
        priority: int,
        granted_by_ref: str,
        description: str = "",
        expires_at: Optional[str] = None,
    ) -> NetworkAccessRule:
        """
        Create a new network access rule. 调用前 Agent 须向用户明确确认。

        参数：
            rule_name: 规则名称。
            subject_type: 主体类型（employee、team、department、role、ip_range）。
            subject_ref: 引用the subject.
            network_zone_ref: 引用the network zone.
            target_resource: 目标资源。
            protocol: 协议（tcp、udp、icmp、any）。
            port_range: 端口范围（如 "80"、"8000-9000"）。
            action: 动作（allow、deny）。
            priority: 优先级（数值越小越紧急）。
            granted_by_ref: 员工 ref：the creator.
            description: 描述。
            expires_at: 可选过期时间。

        返回：
            NetworkAccessRule：新建的规则。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_network_zone(network_zone_ref)
        self._get_employee(granted_by_ref)

        valid_subject_types = {"employee", "team", "department", "role", "ip_range"}
        if subject_type not in valid_subject_types:
            raise ValueError(f"Invalid subject_type: {subject_type}. Must be one of {valid_subject_types}")
        valid_protocols = {"tcp", "udp", "icmp", "any"}
        if protocol not in valid_protocols:
            raise ValueError(f"Invalid protocol: {protocol}. Must be one of {valid_protocols}")
        valid_actions = {"allow", "deny"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}")

        now = self._now_iso()
        ref = self._generate_ref("NAR", self.db.network_access_rule)

        rule = NetworkAccessRule(
            network_access_rule_ref=ref,
            rule_name=rule_name,
            subject_type=subject_type,
            subject_ref=subject_ref,
            network_zone_ref=network_zone_ref,
            target_resource=target_resource,
            protocol=protocol,
            port_range=port_range,
            action=action,
            priority=priority,
            status="active",
            granted_by_ref=granted_by_ref,
            expires_at=expires_at,
            description=description,
            created_at=now,
            updated_at=now,
        )
        self.db.network_access_rule[ref] = rule
        return rule

    @is_tool(ToolType.WRITE)
    def disable_network_access_rule(self, network_access_rule_ref: str) -> NetworkAccessRule:
        """
        Disable a network access rule. 调用前 Agent 须向用户明确确认。

        参数：
            network_access_rule_ref: 引用the rule.

        返回：
            NetworkAccessRule：更新后的规则。

        异常：
            ValueError：若未找到规则或已禁用/已过期。
        """
        r = self._get_network_access_rule(network_access_rule_ref)
        if r.status in ("disabled", "expired"):
            raise ValueError(f"Rule is already {r.status}")
        r.status = "disabled"
        r.updated_at = self._now_iso()
        return r

    # ===================================================================
    # 网络事件（网络异常排查）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_network_incident_details(self, network_incident_ref: str) -> NetworkIncident:
        """
        获取网络事件的详情。

        参数：
            network_incident_ref: 网络事件的唯一标识。

        返回：
            NetworkIncident：网络事件对象。

        异常：
            ValueError：若未找到事件。
        """
        return self._get_network_incident(network_incident_ref)

    @is_tool(ToolType.READ)
    def list_network_incidents(
        self,
        network_zone_ref: Optional[str] = None,
        incident_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
    ) -> str:
        """
        列出网络事件（可选筛选）。

        参数：
            network_zone_ref: 按网络分区筛选。
            incident_type: 按事件类型筛选。
            severity: 按严重程度筛选（low, medium, high, critical).
            status: 按状态筛选（open, investigating, resolved, closed).
            assigned_to_ref: 按经办人员工筛选。

        返回：
            str：network incident summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ni in self.db.network_incident.items():
            if network_zone_ref is not None and ni.network_zone_ref != network_zone_ref:
                continue
            if incident_type is not None and ni.incident_type != incident_type:
                continue
            if severity is not None and ni.severity != severity:
                continue
            if status is not None and ni.status != status:
                continue
            if assigned_to_ref is not None and ni.assigned_to_ref != assigned_to_ref:
                continue
            results.append({
                "network_incident_ref": ni.network_incident_ref,
                "reporter_employee_ref": ni.reporter_employee_ref,
                "network_zone_ref": ni.network_zone_ref,
                "incident_type": ni.incident_type,
                "severity": ni.severity,
                "affected_scope": ni.affected_scope,
                "description": ni.description,
                "status": ni.status,
                "assigned_to_ref": ni.assigned_to_ref,
                "occurred_at": ni.occurred_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_network_incident(
        self,
        reporter_employee_ref: str,
        incident_type: str,
        severity: str,
        affected_scope: str,
        description: str,
        network_zone_ref: Optional[str] = None,
    ) -> NetworkIncident:
        """
        Report a new network incident. 调用前 Agent 须向用户明确确认。

        参数：
            reporter_employee_ref: 员工 ref：the reporter.
            incident_type: 类型（connectivity_loss、performance_degradation、security_breach、dns_failure、hardware_failure、configuration_error）。
            severity: 严重程度（low、medium、high、critical）。
            affected_scope: 受影响范围说明。
            description: 详细描述。
            network_zone_ref: 可选受影响网络分区 ref。

        返回：
            NetworkIncident：新建的事件。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(reporter_employee_ref)
        if network_zone_ref is not None:
            self._get_network_zone(network_zone_ref)

        valid_types = {"connectivity_loss", "performance_degradation", "security_breach", "dns_failure", "hardware_failure", "configuration_error"}
        if incident_type not in valid_types:
            raise ValueError(f"Invalid incident_type: {incident_type}. Must be one of {valid_types}")
        valid_severities = {"low", "medium", "high", "critical"}
        if severity not in valid_severities:
            raise ValueError(f"Invalid severity: {severity}. Must be one of {valid_severities}")

        now = self._now_iso()
        ref = self._generate_ref("NI", self.db.network_incident)

        incident = NetworkIncident(
            network_incident_ref=ref,
            reporter_employee_ref=reporter_employee_ref,
            network_zone_ref=network_zone_ref,
            incident_type=incident_type,
            severity=severity,
            affected_scope=affected_scope,
            description=description,
            diagnosis=None,
            resolution=None,
            status="open",
            assigned_to_ref=None,
            resolved_at=None,
            occurred_at=now,
            created_at=now,
            updated_at=now,
        )
        self.db.network_incident[ref] = incident
        return incident

    @is_tool(ToolType.WRITE)
    def update_network_incident(
        self,
        network_incident_ref: str,
        status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
        diagnosis: Optional[str] = None,
        resolution: Optional[str] = None,
    ) -> NetworkIncident:
        """
        Update a network incident. 调用前 Agent 须向用户明确确认。

        参数：
            network_incident_ref: 引用the network incident.
            status: 新状态（open、investigating、resolved、closed）。
            assigned_to_ref: 员工 ref to assign.
            diagnosis: 诊断说明。
            resolution: 解决说明。

        返回：
            NetworkIncident：更新后的事件。

        异常：
            ValueError：若未找到事件或参数无效。
        """
        ni = self._get_network_incident(network_incident_ref)
        if status is not None:
            valid_statuses = {"open", "investigating", "resolved", "closed"}
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
            ni.status = status
            if status == "resolved":
                ni.resolved_at = self._now_iso()
        if assigned_to_ref is not None:
            self._get_employee(assigned_to_ref)
            ni.assigned_to_ref = assigned_to_ref
        if diagnosis is not None:
            ni.diagnosis = diagnosis
        if resolution is not None:
            ni.resolution = resolution
        ni.updated_at = self._now_iso()
        return ni

    # ===================================================================
    # 软件目录（核心软件下载安装 / 办公软件使用咨询）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_software_catalog_details(self, software_catalog_ref: str) -> SoftwareCatalog:
        """
        获取软件目录条目的详情。

        参数：
            software_catalog_ref: 软件目录条目的唯一标识。

        返回：
            SoftwareCatalog：软件目录条目。

        异常：
            ValueError：若未找到条目。
        """
        return self._get_software_catalog(software_catalog_ref)

    @is_tool(ToolType.READ)
    def list_software_catalog(
        self,
        category: Optional[str] = None,
        is_core: Optional[bool] = None,
        compliance_status: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出软件目录条目（可选筛选）。

        参数：
            category: 按类别筛选（office, development, design, communication, security, database, monitoring, analytics, other).
            is_core: 按是否核心/必选状态筛选。
            compliance_status: 按合规状态筛选（approved, pending_review, rejected, conditional).
            status: 按目录状态筛选（active, deprecated, retired).

        返回：
            str：software catalog summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sc in self.db.software_catalog.items():
            if category is not None and sc.category != category:
                continue
            if is_core is not None and sc.is_core != is_core:
                continue
            if compliance_status is not None and sc.compliance_status != compliance_status:
                continue
            if status is not None and sc.status != status:
                continue
            results.append({
                "software_catalog_ref": sc.software_catalog_ref,
                "software_name": sc.software_name,
                "software_code": sc.software_code,
                "vendor": sc.vendor,
                "category": sc.category,
                "current_version": sc.current_version,
                "supported_os": sc.supported_os,
                "download_uri": sc.download_uri,
                "installation_guide_uri": sc.installation_guide_uri,
                "is_core": sc.is_core,
                "requires_license": sc.requires_license,
                "requires_approval": sc.requires_approval,
                "compliance_status": sc.compliance_status,
                "status": sc.status,
                "description": sc.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def search_software_catalog(self, keyword: str) -> str:
        """
        按关键词搜索软件目录（名称、描述、厂商、类别）。

        参数：
            keyword: Search keyword（不区分大小写）。

        返回：
            str：匹配「software catalog entries」的 JSON 数组。

        异常：
            ValueError：若关键词为空。
        """
        if not keyword.strip():
            raise ValueError("Search keyword cannot be empty")
        search = keyword.lower()
        results = []
        for ref, sc in self.db.software_catalog.items():
            match = (
                search in sc.software_name.lower()
                or search in sc.description.lower()
                or search in sc.vendor.lower()
                or search in sc.category.lower()
            )
            if match:
                results.append({
                    "software_catalog_ref": sc.software_catalog_ref,
                    "software_name": sc.software_name,
                    "vendor": sc.vendor,
                    "category": sc.category,
                    "current_version": sc.current_version,
                    "download_uri": sc.download_uri,
                    "is_core": sc.is_core,
                    "status": sc.status,
                    "description": sc.description,
                })
        return json.dumps(results)

    # ===================================================================
    # 软件许可证（软件许可证管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_software_license_details(self, software_license_ref: str) -> SoftwareLicense:
        """
        获取软件许可证的详情。

        参数：
            software_license_ref: 软件许可证的唯一标识。

        返回：
            SoftwareLicense：软件许可证对象。

        异常：
            ValueError：若未找到许可证。
        """
        return self._get_software_license(software_license_ref)

    @is_tool(ToolType.READ)
    def list_software_licenses(
        self,
        software_catalog_ref: Optional[str] = None,
        license_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出软件许可证（可选筛选）。

        参数：
            software_catalog_ref: 按软件目录条目筛选。
            license_type: 按许可证类型筛选。
            status: 按状态筛选（active, expired, cancelled, pending_renewal).

        返回：
            str：software license summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sl in self.db.software_license.items():
            if software_catalog_ref is not None and sl.software_catalog_ref != software_catalog_ref:
                continue
            if license_type is not None and sl.license_type != license_type:
                continue
            if status is not None and sl.status != status:
                continue
            results.append({
                "software_license_ref": sl.software_license_ref,
                "software_catalog_ref": sl.software_catalog_ref,
                "license_type": sl.license_type,
                "total_seats": sl.total_seats,
                "used_seats": sl.used_seats,
                "purchase_date": sl.purchase_date,
                "expiry_date": sl.expiry_date,
                "cost_per_unit": sl.cost_per_unit,
                "currency": sl.currency,
                "auto_renew": sl.auto_renew,
                "status": sl.status,
                "managed_by_ref": sl.managed_by_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_software_license_assignments(
        self,
        software_license_ref: Optional[str] = None,
        employee_ref: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出软件许可证分配（可选筛选）。

        参数：
            software_license_ref: 按许可证筛选。
            employee_ref: 按员工筛选。
            status: 按状态筛选（active, revoked).

        返回：
            str：license assignment summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sla in self.db.software_license_assignment.items():
            if software_license_ref is not None and sla.software_license_ref != software_license_ref:
                continue
            if employee_ref is not None and sla.employee_ref != employee_ref:
                continue
            if status is not None and sla.status != status:
                continue
            results.append({
                "software_license_assignment_ref": sla.software_license_assignment_ref,
                "software_license_ref": sla.software_license_ref,
                "employee_ref": sla.employee_ref,
                "assigned_by_ref": sla.assigned_by_ref,
                "assigned_at": sla.assigned_at,
                "revoked_at": sla.revoked_at,
                "status": sla.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_software_license(
        self,
        software_license_ref: str,
        employee_ref: str,
        assigned_by_ref: str,
    ) -> SoftwareLicenseAssignment:
        """
        Assign a software license to an employee. 调用前 Agent 须向用户明确确认。

        参数：
            software_license_ref: 引用the software license.
            employee_ref: 员工 ref to assign the license to.
            assigned_by_ref: 员工 ref：the assigner.

        返回：
            SoftwareLicenseAssignment：新建的分配。

        异常：
            ValueError：若实体不存在或无可用席位。
        """
        sl = self._get_software_license(software_license_ref)
        self._get_employee(employee_ref)
        self._get_employee(assigned_by_ref)

        if sl.status != "active":
            raise ValueError(f"Cannot assign a license with status '{sl.status}'")
        if sl.used_seats >= sl.total_seats:
            raise ValueError("No available seats for this license")

        # 检查是否已有有效分配
        for sla in self.db.software_license_assignment.values():
            if (sla.software_license_ref == software_license_ref
                    and sla.employee_ref == employee_ref
                    and sla.status == "active"):
                raise ValueError("Employee already has an active assignment for this license")

        now = self._now_iso()
        ref = self._generate_ref("SLA", self.db.software_license_assignment)

        assignment = SoftwareLicenseAssignment(
            software_license_assignment_ref=ref,
            software_license_ref=software_license_ref,
            employee_ref=employee_ref,
            assigned_by_ref=assigned_by_ref,
            assigned_at=now,
            revoked_at=None,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.software_license_assignment[ref] = assignment
        sl.used_seats += 1
        sl.updated_at = now
        return assignment

    @is_tool(ToolType.WRITE)
    def revoke_software_license_assignment(
        self,
        software_license_assignment_ref: str,
    ) -> SoftwareLicenseAssignment:
        """
        Revoke a software license assignment. 调用前 Agent 须向用户明确确认。

        参数：
            software_license_assignment_ref: 引用the license assignment.

        返回：
            SoftwareLicenseAssignment：更新后的分配。

        异常：
            ValueError：若未找到分配或已撤销。
        """
        sla = self._get_software_license_assignment(software_license_assignment_ref)
        if sla.status == "revoked":
            raise ValueError("Assignment is already revoked")
        now = self._now_iso()
        sla.status = "revoked"
        sla.revoked_at = now
        sla.updated_at = now
        # 更新已用席位数
        sl = self._get_software_license(sla.software_license_ref)
        sl.used_seats = max(0, sl.used_seats - 1)
        sl.updated_at = now
        return sla

    # ===================================================================
    # 软件安装（核心软件下载安装 / 软件故障）
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_software_installations(
        self,
        employee_ref: Optional[str] = None,
        software_catalog_ref: Optional[str] = None,
        installation_status: Optional[str] = None,
    ) -> str:
        """
        列出软件安装（可选筛选）。

        参数：
            employee_ref: 按员工筛选。
            software_catalog_ref: 按软件目录条目筛选。
            installation_status: 按安装状态筛选（installed, pending, failed, uninstalled).

        返回：
            str：installation summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, si in self.db.software_installation.items():
            if employee_ref is not None and si.employee_ref != employee_ref:
                continue
            if software_catalog_ref is not None and si.software_catalog_ref != software_catalog_ref:
                continue
            if installation_status is not None and si.installation_status != installation_status:
                continue
            results.append({
                "software_installation_ref": si.software_installation_ref,
                "software_catalog_ref": si.software_catalog_ref,
                "employee_ref": si.employee_ref,
                "device_name": si.device_name,
                "installed_version": si.installed_version,
                "installation_status": si.installation_status,
                "installed_at": si.installed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_software_installation_details(self, software_installation_ref: str) -> SoftwareInstallation:
        """
        获取软件安装的详情。

        参数：
            software_installation_ref: 软件安装记录的唯一标识。

        返回：
            SoftwareInstallation：安装记录对象。

        异常：
            ValueError：若未找到安装记录。
        """
        return self._get_software_installation(software_installation_ref)

    # ===================================================================
    # 软件报备（软件报备）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_software_filing_details(self, software_filing_ref: str) -> SoftwareFiling:
        """
        获取软件报备的详情。

        参数：
            software_filing_ref: 软件报备的唯一标识。

        返回：
            SoftwareFiling：软件报备对象。

        异常：
            ValueError：若未找到报备。
        """
        return self._get_software_filing(software_filing_ref)

    @is_tool(ToolType.READ)
    def list_software_filings(
        self,
        filed_by_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        filing_status: Optional[str] = None,
    ) -> str:
        """
        列出软件报备（可选筛选）。

        参数：
            filed_by_ref: 按报备人筛选。
            department_ref: 按部门筛选。
            filing_status: 按报备状态筛选（pending, approved, rejected, withdrawn).

        返回：
            str：software filing summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sf in self.db.software_filing.items():
            if filed_by_ref is not None and sf.filed_by_ref != filed_by_ref:
                continue
            if department_ref is not None and sf.department_ref != department_ref:
                continue
            if filing_status is not None and sf.filing_status != filing_status:
                continue
            results.append({
                "software_filing_ref": sf.software_filing_ref,
                "software_name": sf.software_name,
                "vendor": sf.vendor,
                "version": sf.version,
                "purpose": sf.purpose,
                "data_sensitivity": sf.data_sensitivity,
                "filed_by_ref": sf.filed_by_ref,
                "department_ref": sf.department_ref,
                "security_review_status": sf.security_review_status,
                "compliance_review_status": sf.compliance_review_status,
                "filing_status": sf.filing_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_software_filing(
        self,
        software_name: str,
        vendor: str,
        version: str,
        purpose: str,
        data_sensitivity: str,
        filed_by_ref: str,
        department_ref: str,
        notes: str = "",
        software_catalog_ref: Optional[str] = None,
    ) -> SoftwareFiling:
        """
        Create a new software filing request. 调用前 Agent 须向用户明确确认。

        参数：
            software_name: 软件名称。
            vendor: 软件厂商。
            version: 软件版本。
            purpose: 用途/场景。
            data_sensitivity: 数据敏感度（public、internal、confidential、restricted）。
            filed_by_ref: 员工 ref：the filer.
            department_ref: 部门 ref。
            notes: 附加说明。
            software_catalog_ref: 可选已有目录条目 ref。

        返回：
            SoftwareFiling：新建的报备。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(filed_by_ref)
        self._get_department(department_ref)
        if software_catalog_ref is not None:
            self._get_software_catalog(software_catalog_ref)

        valid_sensitivities = {"public", "internal", "confidential", "restricted"}
        if data_sensitivity not in valid_sensitivities:
            raise ValueError(f"Invalid data_sensitivity: {data_sensitivity}. Must be one of {valid_sensitivities}")

        now = self._now_iso()
        ref = self._generate_ref("SF", self.db.software_filing)

        filing = SoftwareFiling(
            software_filing_ref=ref,
            software_catalog_ref=software_catalog_ref,
            software_name=software_name,
            vendor=vendor,
            version=version,
            purpose=purpose,
            data_sensitivity=data_sensitivity,
            filed_by_ref=filed_by_ref,
            department_ref=department_ref,
            security_review_status="pending",
            compliance_review_status="pending",
            reviewed_by_ref=None,
            reviewed_at=None,
            filing_status="pending",
            rejection_reason=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.software_filing[ref] = filing
        return filing

    @is_tool(ToolType.WRITE)
    def approve_software_filing(
        self,
        software_filing_ref: str,
        reviewed_by_ref: str,
    ) -> SoftwareFiling:
        """
        Approve a software filing. 调用前 Agent 须向用户明确确认。

        参数：
            software_filing_ref: 引用the software filing.
            reviewed_by_ref: 员工 ref：the reviewer.

        返回：
            SoftwareFiling：更新后的报备。

        异常：
            ValueError：若未找到报备或非待处理状态。
        """
        sf = self._get_software_filing(software_filing_ref)
        self._get_employee(reviewed_by_ref)
        if sf.filing_status != "pending":
            raise ValueError(f"Cannot approve a filing with status '{sf.filing_status}'")
        now = self._now_iso()
        sf.filing_status = "approved"
        sf.security_review_status = "approved"
        sf.compliance_review_status = "approved"
        sf.reviewed_by_ref = reviewed_by_ref
        sf.reviewed_at = now
        sf.updated_at = now
        return sf

    @is_tool(ToolType.WRITE)
    def reject_software_filing(
        self,
        software_filing_ref: str,
        reviewed_by_ref: str,
        rejection_reason: str,
    ) -> SoftwareFiling:
        """
        Reject a software filing. 调用前 Agent 须向用户明确确认。

        参数：
            software_filing_ref: 引用the software filing.
            reviewed_by_ref: 员工 ref：the reviewer.
            rejection_reason: 拒绝原因。

        返回：
            SoftwareFiling：更新后的报备。

        异常：
            ValueError：若未找到报备或非待处理状态。
        """
        sf = self._get_software_filing(software_filing_ref)
        self._get_employee(reviewed_by_ref)
        if sf.filing_status != "pending":
            raise ValueError(f"Cannot reject a filing with status '{sf.filing_status}'")
        now = self._now_iso()
        sf.filing_status = "rejected"
        sf.reviewed_by_ref = reviewed_by_ref
        sf.reviewed_at = now
        sf.rejection_reason = rejection_reason
        sf.updated_at = now
        return sf

    @is_tool(ToolType.WRITE)
    def withdraw_software_filing(self, software_filing_ref: str) -> SoftwareFiling:
        """
        Withdraw a software filing. 调用前 Agent 须向用户明确确认。

        参数：
            software_filing_ref: 引用the software filing.

        返回：
            SoftwareFiling：更新后的报备。

        异常：
            ValueError：若未找到报备或非待处理状态。
        """
        sf = self._get_software_filing(software_filing_ref)
        if sf.filing_status != "pending":
            raise ValueError(f"Cannot withdraw a filing with status '{sf.filing_status}'")
        sf.filing_status = "withdrawn"
        sf.updated_at = self._now_iso()
        return sf

    # ===================================================================
    # 打印机（打印机查询 / 打印故障）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_printer_details(self, printer_ref: str) -> Printer:
        """
        获取打印机的详情。

        参数：
            printer_ref: 打印机的唯一标识。

        返回：
            Printer：打印机对象。

        异常：
            ValueError：若未找到打印机。
        """
        return self._get_printer(printer_ref)

    @is_tool(ToolType.READ)
    def list_printers(
        self,
        location_building: Optional[str] = None,
        location_floor: Optional[str] = None,
        printer_status: Optional[str] = None,
        supports_color: Optional[bool] = None,
        supports_duplex: Optional[bool] = None,
        supports_scan: Optional[bool] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出打印机（可选筛选）。

        参数：
            location_building: 按楼宇筛选。
            location_floor: 按楼层筛选。
            printer_status: 按打印机状态筛选（online, offline, error, maintenance, decommissioned).
            supports_color: 按是否支持彩色筛选。
            supports_duplex: 按是否支持双面筛选。
            supports_scan: 按是否支持扫描筛选。
            department_ref: 按部门筛选。

        返回：
            str：printer summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, p in self.db.printer.items():
            if location_building is not None and p.location_building != location_building:
                continue
            if location_floor is not None and p.location_floor != location_floor:
                continue
            if printer_status is not None and p.printer_status != printer_status:
                continue
            if supports_color is not None and p.supports_color != supports_color:
                continue
            if supports_duplex is not None and p.supports_duplex != supports_duplex:
                continue
            if supports_scan is not None and p.supports_scan != supports_scan:
                continue
            if department_ref is not None and p.department_ref != department_ref:
                continue
            results.append({
                "printer_ref": p.printer_ref,
                "printer_name": p.printer_name,
                "printer_model": p.printer_model,
                "manufacturer": p.manufacturer,
                "ip_address": p.ip_address,
                "location_building": p.location_building,
                "location_floor": p.location_floor,
                "location_area": p.location_area,
                "capabilities": p.capabilities,
                "supports_color": p.supports_color,
                "supports_duplex": p.supports_duplex,
                "supports_scan": p.supports_scan,
                "printer_status": p.printer_status,
                "driver_download_uri": p.driver_download_uri,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_printer_ref_by_name(self, printer_name: str) -> str:
        """
        按名称查找打印机 ref（部分匹配，不区分大小写）。

        参数：
            printer_name: 打印机名称（可部分匹配）。

        返回：
            str：匹配到的 printer_ref。

        异常：
            ValueError：若未匹配到打印机。
        """
        search = printer_name.lower()
        for ref, p in self.db.printer.items():
            if search in p.printer_name.lower():
                return ref
        raise ValueError("Printer not found")

    # ===================================================================
    # 打印耗材（打印耗材管理）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_printer_supply_details(self, printer_supply_ref: str) -> PrinterSupply:
        """
        获取打印耗材的详情。

        参数：
            printer_supply_ref: 打印耗材的唯一标识。

        返回：
            PrinterSupply：打印耗材对象。

        异常：
            ValueError：若未找到耗材。
        """
        return self._get_printer_supply(printer_supply_ref)

    @is_tool(ToolType.READ)
    def list_printer_supplies(
        self,
        printer_ref: Optional[str] = None,
        supply_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出打印耗材（可选筛选）。

        参数：
            printer_ref: 按打印机筛选。
            supply_type: 按耗材类型筛选（toner, ink, drum, paper, fuser, waste_container, other).
            status: 按状态筛选（normal, low, critical, empty, replaced).

        返回：
            str：printer supply summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ps in self.db.printer_supply.items():
            if printer_ref is not None and ps.printer_ref != printer_ref:
                continue
            if supply_type is not None and ps.supply_type != supply_type:
                continue
            if status is not None and ps.status != status:
                continue
            results.append({
                "printer_supply_ref": ps.printer_supply_ref,
                "printer_ref": ps.printer_ref,
                "supply_type": ps.supply_type,
                "supply_name": ps.supply_name,
                "supply_model": ps.supply_model,
                "remaining_percent": ps.remaining_percent,
                "stock_quantity": ps.stock_quantity,
                "reorder_threshold": ps.reorder_threshold,
                "unit_cost": ps.unit_cost,
                "currency": ps.currency,
                "supplier": ps.supplier,
                "status": ps.status,
            })
        return json.dumps(results)

    # ===================================================================
    # 打印故障（打印故障）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_printer_incident_details(self, printer_incident_ref: str) -> PrinterIncident:
        """
        获取打印故障的详情。

        参数：
            printer_incident_ref: 打印故障的唯一标识。

        返回：
            PrinterIncident：打印故障对象。

        异常：
            ValueError：若未找到事件。
        """
        return self._get_printer_incident(printer_incident_ref)

    @is_tool(ToolType.READ)
    def list_printer_incidents(
        self,
        printer_ref: Optional[str] = None,
        incident_type: Optional[str] = None,
        status: Optional[str] = None,
        reporter_employee_ref: Optional[str] = None,
    ) -> str:
        """
        列出打印故障（可选筛选）。

        参数：
            printer_ref: 按打印机筛选。
            incident_type: 按事件类型筛选。
            status: 按状态筛选（open, in_progress, resolved, closed).
            reporter_employee_ref: 按报告人筛选。

        返回：
            str：printer incident summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, pi in self.db.printer_incident.items():
            if printer_ref is not None and pi.printer_ref != printer_ref:
                continue
            if incident_type is not None and pi.incident_type != incident_type:
                continue
            if status is not None and pi.status != status:
                continue
            if reporter_employee_ref is not None and pi.reporter_employee_ref != reporter_employee_ref:
                continue
            results.append({
                "printer_incident_ref": pi.printer_incident_ref,
                "printer_ref": pi.printer_ref,
                "reporter_employee_ref": pi.reporter_employee_ref,
                "incident_type": pi.incident_type,
                "description": pi.description,
                "status": pi.status,
                "assigned_to_ref": pi.assigned_to_ref,
                "created_at": pi.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_printer_incident(
        self,
        printer_ref: str,
        reporter_employee_ref: str,
        incident_type: str,
        description: str,
    ) -> PrinterIncident:
        """
        Report a new printer incident. 调用前 Agent 须向用户明确确认。

        参数：
            printer_ref: 引用the printer.
            reporter_employee_ref: 员工 ref：the reporter.
            incident_type: 类型（paper_jam、toner_issue、connectivity、print_quality、hardware_failure、driver_issue、other）。
            description: 详细描述。

        返回：
            PrinterIncident：新建的故障记录。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_printer(printer_ref)
        self._get_employee(reporter_employee_ref)

        valid_types = {"paper_jam", "toner_issue", "connectivity", "print_quality", "hardware_failure", "driver_issue", "other"}
        if incident_type not in valid_types:
            raise ValueError(f"Invalid incident_type: {incident_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("PI", self.db.printer_incident)

        incident = PrinterIncident(
            printer_incident_ref=ref,
            printer_ref=printer_ref,
            reporter_employee_ref=reporter_employee_ref,
            incident_type=incident_type,
            description=description,
            diagnosis=None,
            resolution=None,
            status="open",
            assigned_to_ref=None,
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.printer_incident[ref] = incident
        return incident

    @is_tool(ToolType.WRITE)
    def update_printer_incident(
        self,
        printer_incident_ref: str,
        status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
        diagnosis: Optional[str] = None,
        resolution: Optional[str] = None,
    ) -> PrinterIncident:
        """
        Update a printer incident. 调用前 Agent 须向用户明确确认。

        参数：
            printer_incident_ref: 引用the printer incident.
            status: 新状态（open、in_progress、resolved、closed）。
            assigned_to_ref: 员工 ref to assign.
            diagnosis: 诊断说明。
            resolution: 解决说明。

        返回：
            PrinterIncident：更新后的故障记录。

        异常：
            ValueError：若未找到事件或参数无效。
        """
        pi = self._get_printer_incident(printer_incident_ref)
        if status is not None:
            valid_statuses = {"open", "in_progress", "resolved", "closed"}
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
            pi.status = status
            if status == "resolved":
                pi.resolved_at = self._now_iso()
        if assigned_to_ref is not None:
            self._get_employee(assigned_to_ref)
            pi.assigned_to_ref = assigned_to_ref
        if diagnosis is not None:
            pi.diagnosis = diagnosis
        if resolution is not None:
            pi.resolution = resolution
        pi.updated_at = self._now_iso()
        return pi

    # ===================================================================
    # 文件传输（文件传输）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_file_transfer_details(self, file_transfer_ref: str) -> FileTransfer:
        """
        获取文件传输的详情。

        参数：
            file_transfer_ref: 文件传输的唯一标识。

        返回：
            FileTransfer：文件传输对象。

        异常：
            ValueError：若未找到传输任务。
        """
        return self._get_file_transfer(file_transfer_ref)

    @is_tool(ToolType.READ)
    def list_file_transfers(
        self,
        initiated_by_ref: Optional[str] = None,
        transfer_type: Optional[str] = None,
        transfer_status: Optional[str] = None,
    ) -> str:
        """
        列出文件传输（可选筛选）。

        参数：
            initiated_by_ref: 按发起人筛选。
            transfer_type: 按传输类型筛选（upload、download、share、sync）。
            transfer_status: 按传输状态筛选（pending, in_progress, completed, failed, expired).

        返回：
            str：file transfer summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ft in self.db.file_transfer.items():
            if initiated_by_ref is not None and ft.initiated_by_ref != initiated_by_ref:
                continue
            if transfer_type is not None and ft.transfer_type != transfer_type:
                continue
            if transfer_status is not None and ft.transfer_status != transfer_status:
                continue
            results.append({
                "file_transfer_ref": ft.file_transfer_ref,
                "file_attachment_ref": ft.file_attachment_ref,
                "transfer_type": ft.transfer_type,
                "source": ft.source,
                "destination": ft.destination,
                "initiated_by_ref": ft.initiated_by_ref,
                "encryption_applied": ft.encryption_applied,
                "transfer_status": ft.transfer_status,
                "file_size_bytes": ft.file_size_bytes,
                "download_count": ft.download_count,
                "expires_at": ft.expires_at,
                "created_at": ft.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_file_transfer(
        self,
        file_attachment_ref: str,
        transfer_type: str,
        source: str,
        destination: str,
        initiated_by_ref: str,
        recipient_employee_refs: List[str],
        file_size_bytes: int,
        encryption_applied: bool = False,
        encryption_method: Optional[str] = None,
        access_password_set: bool = False,
        max_downloads: Optional[int] = None,
        expires_at: Optional[str] = None,
    ) -> FileTransfer:
        """
        Create a new file transfer. 调用前 Agent 须向用户明确确认。

        参数：
            file_attachment_ref: 引用the file attachment.
            transfer_type: 类型（upload、download、share、sync）。
            source: 来源位置。
            destination: 目标位置。
            initiated_by_ref: 员工 ref：the initiator.
            recipient_employee_refs: 收件人员工 ref 列表。
            file_size_bytes: 文件大小（字节）。
            encryption_applied: 是否已加密。
            encryption_method: 若已加密则填写加密方式。
            access_password_set: 是否已设置访问密码。
            max_downloads: 可选最大下载次数。
            expires_at: 可选过期时间。

        返回：
            FileTransfer：新建的文件传输。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(initiated_by_ref)
        for emp_ref in recipient_employee_refs:
            self._get_employee(emp_ref)

        valid_types = {"upload", "download", "share", "sync"}
        if transfer_type not in valid_types:
            raise ValueError(f"Invalid transfer_type: {transfer_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("FT", self.db.file_transfer)

        transfer = FileTransfer(
            file_transfer_ref=ref,
            file_attachment_ref=file_attachment_ref,
            transfer_type=transfer_type,
            source=source,
            destination=destination,
            initiated_by_ref=initiated_by_ref,
            recipient_employee_refs=recipient_employee_refs,
            encryption_applied=encryption_applied,
            encryption_method=encryption_method,
            transfer_status="pending",
            file_size_bytes=file_size_bytes,
            expires_at=expires_at,
            access_password_set=access_password_set,
            download_count=0,
            max_downloads=max_downloads,
            created_at=now,
            updated_at=now,
        )
        self.db.file_transfer[ref] = transfer
        return transfer

    @is_tool(ToolType.WRITE)
    def cancel_file_transfer(self, file_transfer_ref: str) -> FileTransfer:
        """
        Cancel a file transfer. 调用前 Agent 须向用户明确确认。

        参数：
            file_transfer_ref: 引用the file transfer.

        返回：
            FileTransfer：更新后的文件传输。

        异常：
            ValueError：若未找到传输任务或不可取消。
        """
        ft = self._get_file_transfer(file_transfer_ref)
        if ft.transfer_status not in ("pending", "in_progress"):
            raise ValueError(f"Cannot cancel a transfer with status '{ft.transfer_status}'")
        ft.transfer_status = "failed"
        ft.updated_at = self._now_iso()
        return ft

    # ===================================================================
    # 文件安全策略（文件安全与加密）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_file_security_policy_details(self, file_security_policy_ref: str) -> FileSecurityPolicy:
        """
        获取文件安全策略的详情。

        参数：
            file_security_policy_ref: 文件安全策略的唯一标识。

        返回：
            FileSecurityPolicy：文件安全策略对象。

        异常：
            ValueError：若未找到策略。
        """
        return self._get_file_security_policy(file_security_policy_ref)

    @is_tool(ToolType.READ)
    def list_file_security_policies(
        self,
        classification_level: Optional[str] = None,
        status: Optional[str] = None,
        department_ref: Optional[str] = None,
    ) -> str:
        """
        列出文件安全策略（可选筛选）。

        参数：
            classification_level: 按密级筛选（public, internal, confidential, restricted, top_secret).
            status: 按状态筛选（active, disabled, archived).
            department_ref: 按部门筛选。

        返回：
            str：file security policy summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, fsp in self.db.file_security_policy.items():
            if classification_level is not None and fsp.classification_level != classification_level:
                continue
            if status is not None and fsp.status != status:
                continue
            if department_ref is not None and fsp.department_ref != department_ref:
                continue
            results.append({
                "file_security_policy_ref": fsp.file_security_policy_ref,
                "policy_name": fsp.policy_name,
                "classification_level": fsp.classification_level,
                "encryption_required": fsp.encryption_required,
                "encryption_algorithm": fsp.encryption_algorithm,
                "allowed_share_scope": fsp.allowed_share_scope,
                "watermark_required": fsp.watermark_required,
                "download_restricted": fsp.download_restricted,
                "print_restricted": fsp.print_restricted,
                "retention_days": fsp.retention_days,
                "status": fsp.status,
                "description": fsp.description,
            })
        return json.dumps(results)

    # ===================================================================
    # IT 服务工单（信息技术服务台查询 / 软件故障 / 账号登录问题）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_it_service_ticket_details(self, it_service_ticket_ref: str) -> ITServiceTicket:
        """
        获取 IT 服务工单的详情。

        参数：
            it_service_ticket_ref: IT 服务工单的唯一标识。

        返回：
            ITServiceTicket：服务工单对象。

        异常：
            ValueError：若未找到工单。
        """
        return self._get_it_service_ticket(it_service_ticket_ref)

    @is_tool(ToolType.READ)
    def list_it_service_tickets(
        self,
        requester_employee_ref: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
        ticket_category: Optional[str] = None,
        ticket_subcategory: Optional[str] = None,
        ticket_status: Optional[str] = None,
        priority: Optional[str] = None,
        related_system_ref: Optional[str] = None,
    ) -> str:
        """
        列出IT 服务工单（可选筛选）。

        参数：
            requester_employee_ref: 按申请人筛选。
            assigned_to_ref: 按经办人筛选。
            ticket_category: 按类别筛选（incident, service_request, change_request, problem, inquiry).
            ticket_subcategory: 按子类别筛选。
            ticket_status: 按工单状态筛选（open, in_progress, pending, resolved, closed, cancelled).
            priority: 按优先级筛选（P1, P2, P3, P4).
            related_system_ref: 按关联 IT 系统筛选。

        返回：
            str：service ticket summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, t in self.db.it_service_ticket.items():
            if requester_employee_ref is not None and t.requester_employee_ref != requester_employee_ref:
                continue
            if assigned_to_ref is not None and t.assigned_to_ref != assigned_to_ref:
                continue
            if ticket_category is not None and t.ticket_category != ticket_category:
                continue
            if ticket_subcategory is not None and t.ticket_subcategory != ticket_subcategory:
                continue
            if ticket_status is not None and t.ticket_status != ticket_status:
                continue
            if priority is not None and t.priority != priority:
                continue
            if related_system_ref is not None and t.related_system_ref != related_system_ref:
                continue
            results.append({
                "it_service_ticket_ref": t.it_service_ticket_ref,
                "ticket_number": t.ticket_number,
                "requester_employee_ref": t.requester_employee_ref,
                "ticket_category": t.ticket_category,
                "ticket_subcategory": t.ticket_subcategory,
                "title": t.title,
                "urgency": t.urgency,
                "impact": t.impact,
                "priority": t.priority,
                "ticket_status": t.ticket_status,
                "assigned_to_ref": t.assigned_to_ref,
                "assigned_group": t.assigned_group,
                "created_at": t.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_it_service_ticket(
        self,
        requester_employee_ref: str,
        ticket_category: str,
        ticket_subcategory: str,
        title: str,
        description: str,
        urgency: str = "medium",
        impact: str = "individual",
        priority: str = "P3",
        related_system_ref: Optional[str] = None,
        related_printer_ref: Optional[str] = None,
        related_email_account_ref: Optional[str] = None,
    ) -> ITServiceTicket:
        """
        Create a new IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            requester_employee_ref: 员工 ref：the requester.
            ticket_category: 类别（incident、service_request、change_request、problem、inquiry）。
            ticket_subcategory: 子类别。
            title: 工单标题。
            description: 详细描述。
            urgency: 紧急程度（low、medium、high、critical）。
            impact: 影响范围（individual、team、department、company）。
            priority: 优先级（P1、P2、P3、P4）。
            related_system_ref: 可选关联 IT 系统 ref。
            related_printer_ref: 可选关联打印机 ref。
            related_email_account_ref: 可选关联邮箱 ref。

        返回：
            ITServiceTicket：新建的工单。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_employee(requester_employee_ref)

        valid_categories = {"incident", "service_request", "change_request", "problem", "inquiry"}
        if ticket_category not in valid_categories:
            raise ValueError(f"Invalid ticket_category: {ticket_category}. Must be one of {valid_categories}")

        valid_subcategories = {
            "software_fault", "hardware_fault", "network_issue", "access_request",
            "account_issue", "email_issue", "printer_issue", "vpn_issue",
            "security_concern", "data_request", "new_equipment", "software_install",
            "general_inquiry", "other"
        }
        if ticket_subcategory not in valid_subcategories:
            raise ValueError(f"Invalid ticket_subcategory: {ticket_subcategory}. Must be one of {valid_subcategories}")

        valid_urgencies = {"low", "medium", "high", "critical"}
        if urgency not in valid_urgencies:
            raise ValueError(f"Invalid urgency: {urgency}. Must be one of {valid_urgencies}")
        valid_impacts = {"individual", "team", "department", "company"}
        if impact not in valid_impacts:
            raise ValueError(f"Invalid impact: {impact}. Must be one of {valid_impacts}")
        valid_priorities = {"P1", "P2", "P3", "P4"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        if related_system_ref is not None:
            self._get_it_system(related_system_ref)
        if related_printer_ref is not None:
            self._get_printer(related_printer_ref)
        if related_email_account_ref is not None:
            self._get_email_account(related_email_account_ref)

        # 生成工单编号
        year = datetime.now(timezone.utc).year
        max_num = 0
        for t in self.db.it_service_ticket.values():
            if t.ticket_number.startswith(f"IT-{year}-"):
                try:
                    num = int(t.ticket_number.split("-")[-1])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        ticket_number = f"IT-{year}-{max_num + 1:05d}"

        now = self._now_iso()
        ref = self._generate_ref("ITST", self.db.it_service_ticket)

        ticket = ITServiceTicket(
            it_service_ticket_ref=ref,
            ticket_number=ticket_number,
            requester_employee_ref=requester_employee_ref,
            ticket_category=ticket_category,
            ticket_subcategory=ticket_subcategory,
            related_system_ref=related_system_ref,
            related_printer_ref=related_printer_ref,
            related_email_account_ref=related_email_account_ref,
            title=title,
            description=description,
            urgency=urgency,
            impact=impact,
            priority=priority,
            ticket_status="open",
            assigned_to_ref=None,
            assigned_group=None,
            escalation_level=0,
            resolution_summary=None,
            resolution_category=None,
            satisfaction_rating=None,
            satisfaction_comment=None,
            sla_due_at=None,
            first_responded_at=None,
            resolved_at=None,
            closed_at=None,
            reopened_count=0,
            created_at=now,
            updated_at=now,
        )
        self.db.it_service_ticket[ref] = ticket
        return ticket

    @is_tool(ToolType.WRITE)
    def update_it_service_ticket(
        self,
        it_service_ticket_ref: str,
        ticket_status: Optional[str] = None,
        assigned_to_ref: Optional[str] = None,
        assigned_group: Optional[str] = None,
        priority: Optional[str] = None,
        escalation_level: Optional[int] = None,
    ) -> ITServiceTicket:
        """
        Update an IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            it_service_ticket_ref: 引用the ticket.
            ticket_status: 新状态（open、in_progress、pending、resolved、closed、cancelled）。
            assigned_to_ref: 员工 ref to assign.
            assigned_group: 要指派的支撑组。
            priority: 新优先级（P1、P2、P3、P4）。
            escalation_level: 新升级级别。

        返回：
            ITServiceTicket：更新后的工单。

        异常：
            ValueError：若未找到工单或参数无效。
        """
        t = self._get_it_service_ticket(it_service_ticket_ref)
        now = self._now_iso()

        if ticket_status is not None:
            valid_statuses = {"open", "in_progress", "pending", "resolved", "closed", "cancelled"}
            if ticket_status not in valid_statuses:
                raise ValueError(f"Invalid ticket_status: {ticket_status}. Must be one of {valid_statuses}")
            t.ticket_status = ticket_status
            if ticket_status == "resolved":
                t.resolved_at = now
            elif ticket_status == "closed":
                t.closed_at = now
            elif ticket_status == "in_progress" and t.first_responded_at is None:
                t.first_responded_at = now
            elif ticket_status == "open" and t.resolved_at is not None:
                # 重新打开
                t.reopened_count += 1
                t.resolved_at = None

        if assigned_to_ref is not None:
            self._get_employee(assigned_to_ref)
            t.assigned_to_ref = assigned_to_ref
        if assigned_group is not None:
            t.assigned_group = assigned_group
        if priority is not None:
            valid_priorities = {"P1", "P2", "P3", "P4"}
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
            t.priority = priority
        if escalation_level is not None:
            t.escalation_level = escalation_level

        t.updated_at = now
        return t

    @is_tool(ToolType.WRITE)
    def resolve_it_service_ticket(
        self,
        it_service_ticket_ref: str,
        resolution_summary: str,
        resolution_category: str,
    ) -> ITServiceTicket:
        """
        Resolve an IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            it_service_ticket_ref: 引用the ticket.
            resolution_summary: 解决摘要。
            resolution_category: 类别（fixed、workaround、known_issue、user_education、no_fault_found、escalated、other）。

        返回：
            ITServiceTicket：更新后的工单。

        异常：
            ValueError：若未找到工单、已解决/已关闭或 category 无效。
        """
        t = self._get_it_service_ticket(it_service_ticket_ref)
        if t.ticket_status in ("resolved", "closed"):
            raise ValueError(f"Ticket is already {t.ticket_status}")

        valid_categories = {"fixed", "workaround", "known_issue", "user_education", "no_fault_found", "escalated", "other"}
        if resolution_category not in valid_categories:
            raise ValueError(f"Invalid resolution_category: {resolution_category}. Must be one of {valid_categories}")

        now = self._now_iso()
        t.ticket_status = "resolved"
        t.resolution_summary = resolution_summary
        t.resolution_category = resolution_category
        t.resolved_at = now
        t.updated_at = now
        return t

    @is_tool(ToolType.WRITE)
    def close_it_service_ticket(
        self,
        it_service_ticket_ref: str,
        satisfaction_rating: Optional[int] = None,
        satisfaction_comment: Optional[str] = None,
    ) -> ITServiceTicket:
        """
        Close an IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            it_service_ticket_ref: 引用the ticket.
            satisfaction_rating: 可选满意度评分（1-5）。
            satisfaction_comment: 可选满意度评语。

        返回：
            ITServiceTicket：更新后的工单。

        异常：
            ValueError：若未找到工单、未解决或评分无效。
        """
        t = self._get_it_service_ticket(it_service_ticket_ref)
        if t.ticket_status == "closed":
            raise ValueError("Ticket is already closed")

        if satisfaction_rating is not None:
            if satisfaction_rating < 1 or satisfaction_rating > 5:
                raise ValueError("Satisfaction rating must be between 1 and 5")
            t.satisfaction_rating = satisfaction_rating
        if satisfaction_comment is not None:
            t.satisfaction_comment = satisfaction_comment

        now = self._now_iso()
        t.ticket_status = "closed"
        t.closed_at = now
        t.updated_at = now
        return t

    @is_tool(ToolType.WRITE)
    def cancel_it_service_ticket(self, it_service_ticket_ref: str) -> ITServiceTicket:
        """
        Cancel an IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            it_service_ticket_ref: 引用the ticket.

        返回：
            ITServiceTicket：更新后的工单。

        异常：
            ValueError：若未找到工单或已关闭/已取消。
        """
        t = self._get_it_service_ticket(it_service_ticket_ref)
        if t.ticket_status in ("closed", "cancelled"):
            raise ValueError(f"Ticket is already {t.ticket_status}")
        t.ticket_status = "cancelled"
        t.updated_at = self._now_iso()
        return t

    # ===================================================================
    # IT 服务工单评论
    # ===================================================================

    @is_tool(ToolType.READ)
    def list_it_service_ticket_comments(self, it_service_ticket_ref: str) -> str:
        """
        列出 IT 服务工单上的评论。

        参数：
            it_service_ticket_ref: 引用the IT service ticket.

        返回：
            str：comment details sorted by created_at 的 JSON 数组。

        异常：
            ValueError：若未找到工单。
        """
        self._get_it_service_ticket(it_service_ticket_ref)
        comments = []
        for ref, c in self.db.it_service_ticket_comment.items():
            if c.it_service_ticket_ref != it_service_ticket_ref:
                continue
            comments.append(c)
        comments.sort(key=lambda x: x.created_at)
        results = []
        for c in comments:
            results.append({
                "it_service_ticket_comment_ref": c.it_service_ticket_comment_ref,
                "author_employee_ref": c.author_employee_ref,
                "comment_type": c.comment_type,
                "content": c.content,
                "is_internal": c.is_internal,
                "attachment_file_refs": c.attachment_file_refs,
                "created_at": c.created_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_it_service_ticket_comment(
        self,
        it_service_ticket_ref: str,
        author_employee_ref: str,
        comment_type: str,
        content: str,
        is_internal: bool = False,
        attachment_file_refs: Optional[List[str]] = None,
    ) -> ITServiceTicketComment:
        """
        Add a comment to an IT service ticket. 调用前 Agent 须向用户明确确认。

        参数：
            it_service_ticket_ref: 引用the ticket.
            author_employee_ref: 员工 ref：the comment author.
            comment_type: 类型（reply、note、resolution、escalation、system）。
            content: 评论内容。
            is_internal: 是否为内部评论。
            attachment_file_refs: 可选附件文件 ref 列表。

        返回：
            ITServiceTicketComment：新建的评论。

        异常：
            ValueError：若实体不存在或参数无效。
        """
        self._get_it_service_ticket(it_service_ticket_ref)
        self._get_employee(author_employee_ref)

        valid_types = {"reply", "note", "resolution", "escalation", "system"}
        if comment_type not in valid_types:
            raise ValueError(f"Invalid comment_type: {comment_type}. Must be one of {valid_types}")

        now = self._now_iso()
        ref = self._generate_ref("ITSTC", self.db.it_service_ticket_comment)

        comment = ITServiceTicketComment(
            it_service_ticket_comment_ref=ref,
            it_service_ticket_ref=it_service_ticket_ref,
            author_employee_ref=author_employee_ref,
            comment_type=comment_type,
            content=content,
            is_internal=is_internal,
            attachment_file_refs=attachment_file_refs or [],
            created_at=now,
            updated_at=now,
        )
        self.db.it_service_ticket_comment[ref] = comment
        return comment

    # ===================================================================
    # IT 服务联系人（信息技术热线查询）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_it_service_contact_details(self, it_service_contact_ref: str) -> ITServiceContact:
        """
        获取 IT 服务联系人的详情。

        参数：
            it_service_contact_ref: IT 服务联系人的唯一标识。

        返回：
            ITServiceContact：服务联系人对象。

        异常：
            ValueError：若未找到联系人。
        """
        return self._get_it_service_contact(it_service_contact_ref)

    @is_tool(ToolType.READ)
    def list_it_service_contacts(
        self,
        contact_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        列出IT 服务联系人（可选筛选）。

        参数：
            contact_type: 按联系方式类型筛选（hotline, email, chat, walk_in, self_service).
            status: 按状态筛选（active, inactive).

        返回：
            str：service contact summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, sc in self.db.it_service_contact.items():
            if contact_type is not None and sc.contact_type != contact_type:
                continue
            if status is not None and sc.status != status:
                continue
            results.append({
                "it_service_contact_ref": sc.it_service_contact_ref,
                "contact_name": sc.contact_name,
                "contact_type": sc.contact_type,
                "phone_number": sc.phone_number,
                "email": sc.email,
                "service_hours": sc.service_hours,
                "location": sc.location,
                "supported_categories": sc.supported_categories,
                "description": sc.description,
                "status": sc.status,
            })
        return json.dumps(results)

    # ===================================================================
    # IT 知识库文章（信息技术服务台查询 / 办公软件使用咨询）
    # ===================================================================

    @is_tool(ToolType.READ)
    def get_it_knowledge_article_details(self, it_knowledge_article_ref: str) -> ITKnowledgeArticle:
        """
        获取 IT 知识库文章的详情。

        参数：
            it_knowledge_article_ref: IT 知识库文章的唯一标识。

        返回：
            ITKnowledgeArticle：知识库文章对象。

        异常：
            ValueError：若未找到文章。
        """
        return self._get_it_knowledge_article(it_knowledge_article_ref)

    @is_tool(ToolType.READ)
    def list_it_knowledge_articles(
        self,
        article_category: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> str:
        """
        列出IT 知识库文章（可选筛选）。

        参数：
            article_category: 按类别筛选（faq, how_to, troubleshooting, policy, announcement, best_practice).
            status: 按状态筛选（draft, published, archived, deprecated).
            tag: 按标签筛选（部分匹配）。

        返回：
            str：knowledge article summaries 的 JSON 数组。

        异常：
            ValueError：若筛选值无效。
        """
        results = []
        for ref, ka in self.db.it_knowledge_article.items():
            if article_category is not None and ka.article_category != article_category:
                continue
            if status is not None and ka.status != status:
                continue
            if tag is not None and not any(tag.lower() in t.lower() for t in ka.tags):
                continue
            results.append({
                "it_knowledge_article_ref": ka.it_knowledge_article_ref,
                "article_title": ka.article_title,
                "article_category": ka.article_category,
                "related_categories": ka.related_categories,
                "author_employee_ref": ka.author_employee_ref,
                "view_count": ka.view_count,
                "helpful_count": ka.helpful_count,
                "tags": ka.tags,
                "status": ka.status,
                "published_at": ka.published_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def search_it_knowledge_articles(self, keyword: str) -> str:
        """
        按关键词搜索 IT 知识库文章（标题、正文、标签）。

        参数：
            keyword: Search keyword（不区分大小写）。

        返回：
            str：匹配「knowledge article summaries」的 JSON 数组。

        异常：
            ValueError：若关键词为空。
        """
        if not keyword.strip():
            raise ValueError("Search keyword cannot be empty")
        search = keyword.lower()
        results = []
        for ref, ka in self.db.it_knowledge_article.items():
            if ka.status != "published":
                continue
            match = (
                search in ka.article_title.lower()
                or search in ka.content.lower()
                or any(search in t.lower() for t in ka.tags)
                or any(search in c.lower() for c in ka.related_categories)
            )
            if match:
                results.append({
                    "it_knowledge_article_ref": ka.it_knowledge_article_ref,
                    "article_title": ka.article_title,
                    "article_category": ka.article_category,
                    "tags": ka.tags,
                    "view_count": ka.view_count,
                    "helpful_count": ka.helpful_count,
                    "content": ka.content[:500],  # 仅返回前 500 字符作为预览
                })
        return json.dumps(results)