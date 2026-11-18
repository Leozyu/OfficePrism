from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.environment.db import DB
from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

ITSystemType = Literal["business_app", "infrastructure", "platform", "tool", "saas"]
ITSystemStatus = Literal["active", "inactive", "deprecated", "maintenance"]

ITAccountType = Literal["personal", "service", "shared", "admin"]
ITAccountStatus = Literal["active", "disabled", "locked", "deprovisioned"]
ITAccountRoleInSystem = Literal["user", "admin", "power_user", "readonly"]

ITAccountPermissionLevel = Literal["read", "write", "admin", "full"]
ITAccountPermissionStatus = Literal["active", "revoked", "expired"]

AnomalyType = Literal["login_failure", "unusual_access", "privilege_escalation", "geo_anomaly", "brute_force", "data_exfiltration"]
AnomalySeverity = Literal["low", "medium", "high", "critical"]
AnomalyResolutionStatus = Literal["open", "investigating", "resolved", "dismissed"]

MigrationType = Literal["transfer", "clone", "merge", "archive"]
MigrationStatus = Literal["pending", "in_progress", "completed", "failed", "cancelled"]

EmailType = Literal["primary", "alias", "shared", "service"]
MailboxProvider = Literal["exchange", "gmail", "o365", "other"]
EmailAccountStatus = Literal["active", "suspended", "deactivated", "archived"]
EmailSecurityLevel = Literal["standard", "enhanced", "high"]
SpamFilterLevel = Literal["low", "medium", "high", "custom"]

EmailDistributionListType = Literal["department", "team", "project", "custom", "all_company"]
EmailDistributionListStatus = Literal["active", "archived", "dissolved"]

EmailDistributionListMemberRole = Literal["member", "moderator", "owner"]
EmailDistributionListMemberStatus = Literal["active", "removed"]

EmailSecurityEventType = Literal["phishing_detected", "spam_detected", "malware_detected", "unauthorized_forwarding", "policy_violation", "suspicious_attachment"]
EmailSecurityEventSeverity = Literal["low", "medium", "high", "critical"]
EmailSecurityActionTaken = Literal["quarantined", "blocked", "flagged", "deleted", "allowed"]
EmailSecurityEventStatus = Literal["open", "investigating", "resolved", "dismissed"]

RepositoryPlatform = Literal["gitlab", "github", "bitbucket", "gitee"]
RepositoryVisibility = Literal["public", "internal", "private"]
RepositoryStatus = Literal["active", "archived", "deleted"]

CodeRepositoryMemberAccessLevel = Literal["guest", "reporter", "developer", "maintainer", "owner"]
CodeRepositoryMemberStatus = Literal["active", "revoked"]

BranchType = Literal["feature", "bugfix", "hotfix", "release", "main", "develop"]
BranchStatus = Literal["active", "merged", "deleted"]

MergeRequestStatus = Literal["open", "merged", "closed"]
MergeStatus = Literal["can_be_merged", "cannot_be_merged", "checking", "unchecked"]
CloseReason = Literal["completed", "superseded", "abandoned", "duplicate", "other"]

MergeRequestReviewerRole = Literal["reviewer", "approver", "code_owner"]
MergeRequestReviewStatus = Literal["pending", "approved", "changes_requested", "commented"]

MergeRequestActivityType = Literal["created", "commented", "approved", "changes_requested", "merged", "closed", "reopened", "assigned", "label_changed", "status_changed"]

CICDPipelineType = Literal["ci", "cd", "ci_cd"]
PipelineTriggerType = Literal["push", "merge_request", "schedule", "manual", "tag", "api"]
CICDPipelineStatus = Literal["active", "disabled", "archived"]

PipelineExecutionStatus = Literal["pending", "running", "success", "failed", "cancelled", "skipped"]

DeploymentStatus = Literal["pending", "in_progress", "success", "failed", "rolled_back", "cancelled"]
DeploymentStrategy = Literal["rolling", "blue_green", "canary", "recreate", "manual"]

DeployEnvironmentType = Literal["development", "staging", "production", "testing", "demo"]
DeployEnvironmentStatus = Literal["active", "inactive", "maintenance", "decommissioned"]

ITResourceType = Literal["server", "vm", "container", "storage", "database", "load_balancer", "gpu", "other"]
ITResourceStatus = Literal["available", "in_use", "maintenance", "decommissioned", "reserved"]
ITResourceAllocatedToType = Literal["employee", "team", "department", "project"]

ITResourceRequestCategory = Literal["new_allocation", "upgrade", "replacement", "decommission", "temporary"]
ITResourceRequestUrgency = Literal["low", "normal", "high", "critical"]
ITResourceRequestStatus = Literal["pending", "approved", "rejected", "fulfilled", "cancelled"]

DevEnvironmentType = Literal["local", "remote", "cloud", "container"]
DevEnvironmentOSType = Literal["macos", "windows", "linux", "other"]
DevEnvironmentStatus = Literal["active", "inactive", "archived"]

DataSourceType = Literal["database", "api", "file", "stream", "data_warehouse", "data_lake"]
DataSourceConnectionType = Literal["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "kafka", "http", "s3", "other"]
DataSourceSensitivityLevel = Literal["public", "internal", "confidential", "restricted"]
DataSourceStatus = Literal["active", "inactive", "deprecated", "maintenance"]

DataAccessGrantLevel = Literal["read", "write", "admin", "full"]
DataAccessGrantStatus = Literal["active", "revoked", "expired"]

DataAssetType = Literal["table", "view", "collection", "index", "topic", "bucket", "file", "api_endpoint"]
DataAssetSensitivityLevel = Literal["public", "internal", "confidential", "restricted"]
DataAssetUpdateFrequency = Literal["realtime", "hourly", "daily", "weekly", "monthly", "manual", "unknown"]
DataAssetStatus = Literal["active", "deprecated", "archived"]

DataTransferType = Literal["import", "export", "sync", "migration", "backup"]
DataTransferFormat = Literal["csv", "json", "parquet", "avro", "xml", "sql", "excel", "other"]
DataTransferJobStatus = Literal["pending", "running", "completed", "failed", "cancelled"]

NetworkZoneType = Literal["corporate", "dmz", "guest", "production", "development", "restricted"]
NetworkZoneStatus = Literal["active", "inactive", "maintenance"]

VPNConnectionStatus = Literal["connected", "disconnected", "error"]

GuestWifiCredentialStatus = Literal["active", "expired", "revoked"]

NetworkAccessRuleSubjectType = Literal["employee", "team", "department", "role", "ip_range"]
NetworkAccessRuleProtocol = Literal["tcp", "udp", "icmp", "any"]
NetworkAccessRuleAction = Literal["allow", "deny"]
NetworkAccessRuleStatus = Literal["active", "disabled", "expired"]

NetworkIncidentType = Literal["connectivity_loss", "performance_degradation", "security_breach", "dns_failure", "hardware_failure", "configuration_error"]
NetworkIncidentSeverity = Literal["low", "medium", "high", "critical"]
NetworkIncidentStatus = Literal["open", "investigating", "resolved", "closed"]

SoftwareCategory = Literal["office", "development", "design", "communication", "security", "database", "monitoring", "analytics", "other"]
SoftwareComplianceStatus = Literal["approved", "pending_review", "rejected", "conditional"]
SoftwareCatalogStatus = Literal["active", "deprecated", "retired"]

SoftwareLicenseType = Literal["per_seat", "per_device", "site", "enterprise", "open_source", "trial", "subscription"]
SoftwareLicenseStatus = Literal["active", "expired", "cancelled", "pending_renewal"]

SoftwareLicenseAssignmentStatus = Literal["active", "revoked"]

SoftwareInstallationStatus = Literal["installed", "pending", "failed", "uninstalled"]

SoftwareFilingDataSensitivity = Literal["public", "internal", "confidential", "restricted"]
SoftwareFilingReviewStatus = Literal["pending", "approved", "rejected"]
SoftwareFilingStatus = Literal["pending", "approved", "rejected", "withdrawn"]

PrinterStatus = Literal["online", "offline", "error", "maintenance", "decommissioned"]

PrinterSupplyType = Literal["toner", "ink", "drum", "paper", "fuser", "waste_container", "other"]
PrinterSupplyStatus = Literal["normal", "low", "critical", "empty", "replaced"]

PrinterIncidentType = Literal["paper_jam", "toner_issue", "connectivity", "print_quality", "hardware_failure", "driver_issue", "other"]
PrinterIncidentStatus = Literal["open", "in_progress", "resolved", "closed"]

FileTransferType = Literal["upload", "download", "share", "sync"]
FileTransferStatus = Literal["pending", "in_progress", "completed", "failed", "expired"]

FileClassificationLevel = Literal["public", "internal", "confidential", "restricted", "top_secret"]
FileShareScope = Literal["public", "company", "department", "team", "individual"]
FileSecurityPolicyStatus = Literal["active", "disabled", "archived"]

TicketCategory = Literal["incident", "service_request", "change_request", "problem", "inquiry"]
TicketSubcategory = Literal[
    "software_fault", "hardware_fault", "network_issue", "access_request",
    "account_issue", "email_issue", "printer_issue", "vpn_issue",
    "security_concern", "data_request", "new_equipment", "software_install",
    "general_inquiry", "other"
]
TicketUrgency = Literal["low", "medium", "high", "critical"]
TicketImpact = Literal["individual", "team", "department", "company"]
TicketPriority = Literal["P1", "P2", "P3", "P4"]
TicketStatus = Literal["open", "in_progress", "pending", "resolved", "closed", "cancelled"]
ResolutionCategory = Literal["fixed", "workaround", "known_issue", "user_education", "no_fault_found", "escalated", "other"]

TicketCommentType = Literal["reply", "note", "resolution", "escalation", "system"]

ITServiceContactType = Literal["hotline", "email", "chat", "walk_in", "self_service"]
ITServiceContactStatus = Literal["active", "inactive"]

ITKnowledgeArticleCategory = Literal["faq", "how_to", "troubleshooting", "policy", "announcement", "best_practice"]
ITKnowledgeArticleStatus = Literal["draft", "published", "archived", "deprecated"]


# --- Models ---


class ITSystem(BaseModel):
    """Represents an IT system or application managed within the organization"""

    it_system_ref: str = Field(description="Unique identifier for the IT system")
    system_name: str = Field(description="Name of the IT system")
    system_code: str = Field(description="Short code for the IT system")
    system_type: ITSystemType = Field(
        description="Type of IT system (business_app, infrastructure, platform, tool, saas)"
    )
    system_url: str = Field(description="URL to access the IT system")
    system_status: ITSystemStatus = Field(
        description="Current status of the IT system (active, inactive, deprecated, maintenance)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the system owner")
    admin_employee_ref: str = Field(description="Employee reference of the system administrator")
    department_ref: str = Field(description="Reference to the department responsible for the system")
    description: str = Field(description="Description of the IT system's purpose and functionality")
    sso_enabled: bool = Field(description="Whether single sign-on is enabled for this system")
    mfa_required: bool = Field(description="Whether multi-factor authentication is required for this system")
    created_at: str = Field(description="Timestamp when the IT system was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the IT system was last updated (ISO 8601)")


class ITSystemAccount(BaseModel):
    """Represents a user account within an IT system"""

    it_system_account_ref: str = Field(description="Unique identifier for the IT system account")
    it_system_ref: str = Field(description="Reference to the IT system this account belongs to")
    employee_ref: str = Field(description="Reference to the employee who owns this account")
    account_username: str = Field(description="Username for the account in the IT system")
    account_type: ITAccountType = Field(
        description="Type of account (personal, service, shared, admin)"
    )
    account_status: ITAccountStatus = Field(
        description="Current status of the account (active, disabled, locked, deprovisioned)"
    )
    role_in_system: ITAccountRoleInSystem = Field(
        description="Role of the account within the IT system (user, admin, power_user, readonly)"
    )
    password_last_changed_at: str = Field(description="Timestamp when the password was last changed (ISO 8601)")
    password_expires_at: Optional[str] = Field(
        description="Timestamp when the password expires, null if no expiration (ISO 8601)",
        default=None,
    )
    last_login_at: Optional[str] = Field(
        description="Timestamp of the last login, null if never logged in (ISO 8601)",
        default=None,
    )
    mfa_enabled: bool = Field(description="Whether multi-factor authentication is enabled for this account")
    locked_at: Optional[str] = Field(
        description="Timestamp when the account was locked, null if not locked (ISO 8601)",
        default=None,
    )
    lock_reason: Optional[str] = Field(
        description="Reason for account lock, null if not locked",
        default=None,
    )
    provisioned_at: str = Field(description="Timestamp when the account was provisioned (ISO 8601)")
    deprovisioned_at: Optional[str] = Field(
        description="Timestamp when the account was deprovisioned, null if still active (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the account record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the account record was last updated (ISO 8601)")


class ITSystemAccountPermission(BaseModel):
    """Represents a permission granted to an IT system account"""

    it_system_account_permission_ref: str = Field(description="Unique identifier for the account permission")
    it_system_account_ref: str = Field(description="Reference to the IT system account")
    permission_name: str = Field(description="Name of the permission granted")
    permission_level: ITAccountPermissionLevel = Field(
        description="Level of the permission (read, write, admin, full)"
    )
    scope: str = Field(description="Scope or context of the permission within the system")
    granted_by_ref: str = Field(description="Employee reference of the person who granted this permission")
    granted_at: str = Field(description="Timestamp when the permission was granted (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the permission, null if no expiration (ISO 8601)",
        default=None,
    )
    status: ITAccountPermissionStatus = Field(
        description="Current status of the permission (active, revoked, expired)"
    )
    created_at: str = Field(description="Timestamp when the permission record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the permission record was last updated (ISO 8601)")


class AccessAnomaly(BaseModel):
    """Represents an access anomaly detected in an IT system"""

    access_anomaly_ref: str = Field(description="Unique identifier for the access anomaly")
    it_system_ref: str = Field(description="Reference to the IT system where the anomaly was detected")
    it_system_account_ref: str = Field(description="Reference to the IT system account involved")
    employee_ref: str = Field(description="Reference to the employee associated with the anomaly")
    anomaly_type: AnomalyType = Field(
        description="Type of anomaly (login_failure, unusual_access, privilege_escalation, geo_anomaly, brute_force, data_exfiltration)"
    )
    severity: AnomalySeverity = Field(
        description="Severity level of the anomaly (low, medium, high, critical)"
    )
    source_ip: str = Field(description="Source IP address from which the anomalous activity originated")
    user_agent: str = Field(description="User agent string associated with the anomalous activity")
    description: str = Field(description="Human-readable description of the anomaly")
    resolution_status: AnomalyResolutionStatus = Field(
        description="Current resolution status (open, investigating, resolved, dismissed)"
    )
    resolved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who resolved the anomaly, null if unresolved",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the anomaly was resolved, null if unresolved (ISO 8601)",
        default=None,
    )
    resolution_notes: Optional[str] = Field(
        description="Notes about the resolution, null if unresolved",
        default=None,
    )
    occurred_at: str = Field(description="Timestamp when the anomaly occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the anomaly record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the anomaly record was last updated (ISO 8601)")


class AccountMigration(BaseModel):
    """Represents a migration of an account between IT systems"""

    account_migration_ref: str = Field(description="Unique identifier for the account migration")
    employee_ref: str = Field(description="Reference to the employee whose account is being migrated")
    source_system_ref: str = Field(description="Reference to the source IT system")
    source_account_ref: str = Field(description="Reference to the source IT system account")
    target_system_ref: str = Field(description="Reference to the target IT system")
    target_account_ref: Optional[str] = Field(
        description="Reference to the target IT system account, null if not yet created",
        default=None,
    )
    migration_type: MigrationType = Field(
        description="Type of migration (transfer, clone, merge, archive)"
    )
    migration_status: MigrationStatus = Field(
        description="Current status of the migration (pending, in_progress, completed, failed, cancelled)"
    )
    data_scope: str = Field(description="Description of the data scope included in the migration")
    requested_by_ref: str = Field(description="Employee reference of the person who requested the migration")
    executed_by_ref: Optional[str] = Field(
        description="Employee reference of the person who executed the migration, null if not yet executed",
        default=None,
    )
    requested_at: str = Field(description="Timestamp when the migration was requested (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the migration was completed, null if not yet completed (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the migration")
    created_at: str = Field(description="Timestamp when the migration record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the migration record was last updated (ISO 8601)")


class EmailAccount(BaseModel):
    """Represents an email account associated with an employee"""

    email_account_ref: str = Field(description="Unique identifier for the email account")
    employee_ref: str = Field(description="Reference to the employee who owns this email account")
    email_address: str = Field(description="Email address of the account")
    email_type: EmailType = Field(
        description="Type of email account (primary, alias, shared, service)"
    )
    mailbox_provider: MailboxProvider = Field(
        description="Mailbox provider (exchange, gmail, o365, other)"
    )
    account_status: EmailAccountStatus = Field(
        description="Current status of the email account (active, suspended, deactivated, archived)"
    )
    quota_bytes: int = Field(description="Mailbox quota in bytes")
    used_bytes: int = Field(description="Mailbox storage used in bytes")
    forwarding_address: Optional[str] = Field(
        description="Email forwarding address, null if not set",
        default=None,
    )
    auto_reply_enabled: bool = Field(description="Whether auto-reply is enabled")
    auto_reply_message: Optional[str] = Field(
        description="Auto-reply message content, null if not set",
        default=None,
    )
    last_login_at: Optional[str] = Field(
        description="Timestamp of the last login to the email account, null if never logged in (ISO 8601)",
        default=None,
    )
    security_level: EmailSecurityLevel = Field(
        description="Security level of the email account (standard, enhanced, high)"
    )
    spam_filter_level: SpamFilterLevel = Field(
        description="Spam filter level (low, medium, high, custom)"
    )
    created_at: str = Field(description="Timestamp when the email account was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the email account was last updated (ISO 8601)")


class EmailDistributionList(BaseModel):
    """Represents an email distribution list for group communication"""

    email_distribution_list_ref: str = Field(description="Unique identifier for the email distribution list")
    list_address: str = Field(description="Email address of the distribution list")
    list_name: str = Field(description="Display name of the distribution list")
    list_type: EmailDistributionListType = Field(
        description="Type of distribution list (department, team, project, custom, all_company)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the list owner")
    department_ref: Optional[str] = Field(
        description="Reference to the associated department, null if not department-based",
        default=None,
    )
    member_count: int = Field(description="Current number of members in the distribution list")
    status: EmailDistributionListStatus = Field(
        description="Current status of the distribution list (active, archived, dissolved)"
    )
    description: str = Field(description="Description of the distribution list's purpose")
    created_at: str = Field(description="Timestamp when the distribution list was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the distribution list was last updated (ISO 8601)")


class EmailDistributionListMember(BaseModel):
    """Represents a member of an email distribution list"""

    email_distribution_list_member_ref: str = Field(description="Unique identifier for the distribution list membership")
    email_distribution_list_ref: str = Field(description="Reference to the email distribution list")
    email_account_ref: str = Field(description="Reference to the email account of the member")
    role: EmailDistributionListMemberRole = Field(
        description="Role within the distribution list (member, moderator, owner)"
    )
    status: EmailDistributionListMemberStatus = Field(
        description="Current membership status (active, removed)"
    )
    added_by_ref: str = Field(description="Employee reference of the person who added this member")
    added_at: str = Field(description="Timestamp when the member was added (ISO 8601)")
    removed_at: Optional[str] = Field(
        description="Timestamp when the member was removed, null if still active (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the membership record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the membership record was last updated (ISO 8601)")


class EmailSecurityEvent(BaseModel):
    """Represents a security event related to an email account"""

    email_security_event_ref: str = Field(description="Unique identifier for the email security event")
    email_account_ref: str = Field(description="Reference to the email account involved")
    event_type: EmailSecurityEventType = Field(
        description="Type of security event (phishing_detected, spam_detected, malware_detected, unauthorized_forwarding, policy_violation, suspicious_attachment)"
    )
    severity: EmailSecurityEventSeverity = Field(
        description="Severity level of the event (low, medium, high, critical)"
    )
    source_address: str = Field(description="Source email address associated with the event")
    subject: str = Field(description="Subject line of the email involved")
    description: str = Field(description="Human-readable description of the security event")
    action_taken: EmailSecurityActionTaken = Field(
        description="Action taken in response to the event (quarantined, blocked, flagged, deleted, allowed)"
    )
    status: EmailSecurityEventStatus = Field(
        description="Current status of the event (open, investigating, resolved, dismissed)"
    )
    resolved_by_ref: Optional[str] = Field(
        description="Employee reference of the person who resolved the event, null if unresolved",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the event was resolved, null if unresolved (ISO 8601)",
        default=None,
    )
    occurred_at: str = Field(description="Timestamp when the event occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the event record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the event record was last updated (ISO 8601)")


class CodeRepository(BaseModel):
    """Represents a code repository managed within the organization"""

    code_repository_ref: str = Field(description="Unique identifier for the code repository")
    repository_name: str = Field(description="Name of the code repository")
    repository_slug: str = Field(description="URL-friendly slug of the repository")
    repository_url: str = Field(description="URL to access the repository")
    platform: RepositoryPlatform = Field(
        description="Platform hosting the repository (gitlab, github, bitbucket, gitee)"
    )
    visibility: RepositoryVisibility = Field(
        description="Visibility level of the repository (public, internal, private)"
    )
    default_branch: str = Field(description="Default branch name of the repository")
    owner_employee_ref: str = Field(description="Employee reference of the repository owner")
    team_ref: Optional[str] = Field(
        description="Reference to the team that owns the repository, null if not team-owned",
        default=None,
    )
    department_ref: Optional[str] = Field(
        description="Reference to the department that owns the repository, null if not department-owned",
        default=None,
    )
    language_primary: str = Field(description="Primary programming language used in the repository")
    description: str = Field(description="Description of the repository's purpose and contents")
    repository_status: RepositoryStatus = Field(
        description="Current status of the repository (active, archived, deleted)"
    )
    created_at: str = Field(description="Timestamp when the repository was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the repository was last updated (ISO 8601)")


class CodeRepositoryMember(BaseModel):
    """Represents a member with access to a code repository"""

    code_repository_member_ref: str = Field(description="Unique identifier for the repository membership")
    code_repository_ref: str = Field(description="Reference to the code repository")
    employee_ref: str = Field(description="Reference to the employee")
    access_level: CodeRepositoryMemberAccessLevel = Field(
        description="Access level within the repository (guest, reporter, developer, maintainer, owner)"
    )
    granted_by_ref: str = Field(description="Employee reference of the person who granted access")
    granted_at: str = Field(description="Timestamp when access was granted (ISO 8601)")
    revoked_at: Optional[str] = Field(
        description="Timestamp when access was revoked, null if still active (ISO 8601)",
        default=None,
    )
    status: CodeRepositoryMemberStatus = Field(
        description="Current membership status (active, revoked)"
    )
    created_at: str = Field(description="Timestamp when the membership record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the membership record was last updated (ISO 8601)")


class CodeBranch(BaseModel):
    """Represents a branch within a code repository"""

    code_branch_ref: str = Field(description="Unique identifier for the code branch")
    code_repository_ref: str = Field(description="Reference to the code repository")
    branch_name: str = Field(description="Name of the branch")
    branch_type: BranchType = Field(
        description="Type of branch (feature, bugfix, hotfix, release, main, develop)"
    )
    source_branch: str = Field(description="Name of the branch this branch was created from")
    created_by_ref: str = Field(description="Employee reference of the person who created the branch")
    is_protected: bool = Field(description="Whether the branch is protected from direct pushes")
    status: BranchStatus = Field(
        description="Current status of the branch (active, merged, deleted)"
    )
    created_at: str = Field(description="Timestamp when the branch was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the branch was last updated (ISO 8601)")


class MergeRequest(BaseModel):
    """Represents a merge request (pull request) in a code repository"""

    merge_request_ref: str = Field(description="Unique identifier for the merge request")
    code_repository_ref: str = Field(description="Reference to the code repository")
    merge_request_number: int = Field(description="Sequential number of the merge request within the repository")
    title: str = Field(description="Title of the merge request")
    description: str = Field(description="Detailed description of the merge request")
    source_branch: str = Field(description="Source branch of the merge request")
    target_branch: str = Field(description="Target branch of the merge request")
    author_employee_ref: str = Field(description="Employee reference of the merge request author")
    assignee_employee_ref: Optional[str] = Field(
        description="Employee reference of the assignee, null if unassigned",
        default=None,
    )
    merge_request_status: MergeRequestStatus = Field(
        description="Current status of the merge request (open, merged, closed)"
    )
    merge_status: MergeStatus = Field(
        description="Merge readiness status (can_be_merged, cannot_be_merged, checking, unchecked)"
    )
    is_draft: bool = Field(description="Whether the merge request is a draft")
    labels: List[str] = Field(description="List of labels applied to the merge request")
    parent_merge_request_ref: Optional[str] = Field(
        description="Reference to the parent merge request, null if none",
        default=None,
    )
    related_merge_request_refs: List[str] = Field(description="List of references to related merge requests")
    pipeline_ref: Optional[str] = Field(
        description="Reference to the associated CI/CD pipeline, null if none",
        default=None,
    )
    merged_by_ref: Optional[str] = Field(
        description="Employee reference of the person who merged, null if not merged",
        default=None,
    )
    merged_at: Optional[str] = Field(
        description="Timestamp when the merge request was merged, null if not merged (ISO 8601)",
        default=None,
    )
    closed_by_ref: Optional[str] = Field(
        description="Employee reference of the person who closed, null if not closed",
        default=None,
    )
    closed_at: Optional[str] = Field(
        description="Timestamp when the merge request was closed, null if not closed (ISO 8601)",
        default=None,
    )
    close_reason: Optional[CloseReason] = Field(
        description="Reason for closing the merge request, null if not closed",
        default=None,
    )
    lines_added: int = Field(description="Number of lines added in the merge request")
    lines_removed: int = Field(description="Number of lines removed in the merge request")
    files_changed: int = Field(description="Number of files changed in the merge request")
    created_at: str = Field(description="Timestamp when the merge request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the merge request was last updated (ISO 8601)")


class MergeRequestReviewer(BaseModel):
    """Represents a reviewer assigned to a merge request"""

    merge_request_reviewer_ref: str = Field(description="Unique identifier for the merge request reviewer assignment")
    merge_request_ref: str = Field(description="Reference to the merge request")
    reviewer_employee_ref: str = Field(description="Employee reference of the reviewer")
    reviewer_role: MergeRequestReviewerRole = Field(
        description="Role of the reviewer (reviewer, approver, code_owner)"
    )
    review_status: MergeRequestReviewStatus = Field(
        description="Current review status (pending, approved, changes_requested, commented)"
    )
    review_comment: Optional[str] = Field(
        description="Review comment, null if not yet reviewed",
        default=None,
    )
    assigned_by_ref: str = Field(description="Employee reference of the person who assigned the reviewer")
    assigned_at: str = Field(description="Timestamp when the reviewer was assigned (ISO 8601)")
    reviewed_at: Optional[str] = Field(
        description="Timestamp when the review was completed, null if not yet reviewed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the reviewer record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the reviewer record was last updated (ISO 8601)")


class MergeRequestActivity(BaseModel):
    """Represents an activity or event on a merge request"""

    merge_request_activity_ref: str = Field(description="Unique identifier for the merge request activity")
    merge_request_ref: str = Field(description="Reference to the merge request")
    actor_employee_ref: str = Field(description="Employee reference of the person who performed the activity")
    activity_type: MergeRequestActivityType = Field(
        description="Type of activity (created, commented, approved, changes_requested, merged, closed, reopened, assigned, label_changed, status_changed)"
    )
    description: str = Field(description="Human-readable description of the activity")
    changes: Optional[Dict[str, Any]] = Field(
        description="Dictionary of changes made, null if not applicable",
        default=None,
    )
    occurred_at: str = Field(description="Timestamp when the activity occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the activity record was created (ISO 8601)")


class CICDPipeline(BaseModel):
    """Represents a CI/CD pipeline configuration"""

    ci_cd_pipeline_ref: str = Field(description="Unique identifier for the CI/CD pipeline")
    pipeline_name: str = Field(description="Name of the pipeline")
    code_repository_ref: str = Field(description="Reference to the code repository associated with the pipeline")
    pipeline_type: CICDPipelineType = Field(
        description="Type of pipeline (ci, cd, ci_cd)"
    )
    config_file_path: str = Field(description="Path to the pipeline configuration file in the repository")
    trigger_type: PipelineTriggerType = Field(
        description="Default trigger type for the pipeline (push, merge_request, schedule, manual, tag, api)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the pipeline owner")
    status: CICDPipelineStatus = Field(
        description="Current status of the pipeline (active, disabled, archived)"
    )
    description: str = Field(description="Description of the pipeline's purpose")
    created_at: str = Field(description="Timestamp when the pipeline was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the pipeline was last updated (ISO 8601)")


class PipelineExecution(BaseModel):
    """Represents a single execution of a CI/CD pipeline"""

    pipeline_execution_ref: str = Field(description="Unique identifier for the pipeline execution")
    ci_cd_pipeline_ref: str = Field(description="Reference to the CI/CD pipeline")
    execution_number: int = Field(description="Sequential execution number within the pipeline")
    trigger_type: PipelineTriggerType = Field(
        description="Trigger type for this execution (push, merge_request, schedule, manual, tag, api)"
    )
    trigger_ref: str = Field(description="Reference identifier for the trigger source")
    branch: str = Field(description="Branch on which the pipeline was executed")
    commit_sha: str = Field(description="Git commit SHA that triggered the execution")
    triggered_by_ref: str = Field(description="Employee reference of the person who triggered the execution")
    execution_status: PipelineExecutionStatus = Field(
        description="Current execution status (pending, running, success, failed, cancelled, skipped)"
    )
    started_at: str = Field(description="Timestamp when the execution started (ISO 8601)")
    finished_at: Optional[str] = Field(
        description="Timestamp when the execution finished, null if still running (ISO 8601)",
        default=None,
    )
    duration_seconds: Optional[int] = Field(
        description="Duration of the execution in seconds, null if not yet finished",
        default=None,
    )
    artifact_file_refs: List[str] = Field(description="List of file attachment references for build artifacts")
    log_uri: str = Field(description="URI to the execution log")
    error_message: Optional[str] = Field(
        description="Error message if the execution failed, null otherwise",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the execution record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the execution record was last updated (ISO 8601)")


class Deployment(BaseModel):
    """Represents a deployment of code to an environment"""

    deployment_ref: str = Field(description="Unique identifier for the deployment")
    pipeline_execution_ref: str = Field(description="Reference to the pipeline execution that triggered the deployment")
    deploy_environment_ref: str = Field(description="Reference to the target deployment environment")
    version_tag: str = Field(description="Version tag of the deployed code")
    commit_sha: str = Field(description="Git commit SHA of the deployed code")
    deployed_by_ref: str = Field(description="Employee reference of the person who initiated the deployment")
    deployment_status: DeploymentStatus = Field(
        description="Current deployment status (pending, in_progress, success, failed, rolled_back, cancelled)"
    )
    deployment_strategy: DeploymentStrategy = Field(
        description="Deployment strategy used (rolling, blue_green, canary, recreate, manual)"
    )
    rollback_ref: Optional[str] = Field(
        description="Reference to the deployment this was rolled back from, null if not a rollback",
        default=None,
    )
    started_at: str = Field(description="Timestamp when the deployment started (ISO 8601)")
    finished_at: Optional[str] = Field(
        description="Timestamp when the deployment finished, null if still in progress (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes about the deployment")
    created_at: str = Field(description="Timestamp when the deployment record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the deployment record was last updated (ISO 8601)")


class DeployEnvironment(BaseModel):
    """Represents a deployment environment (e.g., production, staging)"""

    deploy_environment_ref: str = Field(description="Unique identifier for the deployment environment")
    environment_name: str = Field(description="Name of the deployment environment")
    environment_code: str = Field(description="Short code for the deployment environment")
    environment_type: DeployEnvironmentType = Field(
        description="Type of environment (development, staging, production, testing, demo)"
    )
    environment_url: str = Field(description="URL to access the environment")
    owner_employee_ref: str = Field(description="Employee reference of the environment owner")
    team_ref: Optional[str] = Field(
        description="Reference to the team responsible for the environment, null if not team-managed",
        default=None,
    )
    status: DeployEnvironmentStatus = Field(
        description="Current status of the environment (active, inactive, maintenance, decommissioned)"
    )
    description: str = Field(description="Description of the environment's purpose")
    config_params: Dict[str, Any] = Field(description="Configuration parameters for the environment")
    created_at: str = Field(description="Timestamp when the environment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the environment was last updated (ISO 8601)")


class ITResource(BaseModel):
    """Represents an IT resource such as a server, VM, or storage device"""

    it_resource_ref: str = Field(description="Unique identifier for the IT resource")
    resource_name: str = Field(description="Name of the IT resource")
    resource_type: ITResourceType = Field(
        description="Type of resource (server, vm, container, storage, database, load_balancer, gpu, other)"
    )
    resource_identifier: str = Field(description="Unique identifier or serial number of the resource")
    specification: Dict[str, Any] = Field(description="Technical specifications of the resource")
    location: str = Field(description="Physical or logical location of the resource")
    owner_employee_ref: str = Field(description="Employee reference of the resource owner")
    department_ref: Optional[str] = Field(
        description="Reference to the department that owns the resource, null if not department-owned",
        default=None,
    )
    resource_status: ITResourceStatus = Field(
        description="Current status of the resource (available, in_use, maintenance, decommissioned, reserved)"
    )
    allocated_to_ref: Optional[str] = Field(
        description="Reference to the entity the resource is allocated to, null if not allocated",
        default=None,
    )
    allocated_to_type: Optional[ITResourceAllocatedToType] = Field(
        description="Type of entity the resource is allocated to (employee, team, department, project), null if not allocated",
        default=None,
    )
    description: str = Field(description="Description of the IT resource")
    created_at: str = Field(description="Timestamp when the resource was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the resource was last updated (ISO 8601)")


class ITResourceRequest(BaseModel):
    """Represents a request for an IT resource"""

    it_resource_request_ref: str = Field(description="Unique identifier for the resource request")
    requester_employee_ref: str = Field(description="Employee reference of the requester")
    resource_type: ITResourceType = Field(
        description="Type of resource requested (server, vm, container, storage, database, load_balancer, gpu, other)"
    )
    request_category: ITResourceRequestCategory = Field(
        description="Category of the request (new_allocation, upgrade, replacement, decommission, temporary)"
    )
    title: str = Field(description="Title of the resource request")
    description: str = Field(description="Detailed description of the request")
    specifications: Dict[str, Any] = Field(description="Desired specifications for the resource")
    business_justification: str = Field(description="Business justification for the request")
    urgency: ITResourceRequestUrgency = Field(
        description="Urgency level of the request (low, normal, high, critical)"
    )
    request_status: ITResourceRequestStatus = Field(
        description="Current status of the request (pending, approved, rejected, fulfilled, cancelled)"
    )
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the request was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    fulfilled_resource_ref: Optional[str] = Field(
        description="Reference to the IT resource that fulfilled the request, null if not yet fulfilled",
        default=None,
    )
    fulfilled_at: Optional[str] = Field(
        description="Timestamp when the request was fulfilled, null if not yet fulfilled (ISO 8601)",
        default=None,
    )
    rejected_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the request, null if no expiration (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the request was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the request was last updated (ISO 8601)")


class DevEnvironment(BaseModel):
    """Represents a developer's local or remote development environment"""

    dev_environment_ref: str = Field(description="Unique identifier for the development environment")
    environment_name: str = Field(description="Name of the development environment")
    environment_type: DevEnvironmentType = Field(
        description="Type of environment (local, remote, cloud, container)"
    )
    employee_ref: str = Field(description="Reference to the employee who owns this environment")
    os_type: DevEnvironmentOSType = Field(
        description="Operating system type (macos, windows, linux, other)"
    )
    os_version: str = Field(description="Operating system version")
    tools_installed: List[str] = Field(description="List of development tools installed")
    env_variables: Dict[str, str] = Field(description="Environment variables configured")
    database_connections: List[str] = Field(description="List of database connection identifiers")
    status: DevEnvironmentStatus = Field(
        description="Current status of the environment (active, inactive, archived)"
    )
    notes: str = Field(description="Additional notes about the development environment")
    created_at: str = Field(description="Timestamp when the environment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the environment was last updated (ISO 8601)")


class DataSource(BaseModel):
    """Represents a data source such as a database, API, or file store"""

    data_source_ref: str = Field(description="Unique identifier for the data source")
    source_name: str = Field(description="Name of the data source")
    source_type: DataSourceType = Field(
        description="Type of data source (database, api, file, stream, data_warehouse, data_lake)"
    )
    connection_type: DataSourceConnectionType = Field(
        description="Connection type (mysql, postgresql, mongodb, redis, elasticsearch, kafka, http, s3, other)"
    )
    host: str = Field(description="Host address of the data source")
    port: int = Field(description="Port number of the data source")
    database_name: str = Field(description="Name of the database or resource")
    owner_employee_ref: str = Field(description="Employee reference of the data source owner")
    department_ref: Optional[str] = Field(
        description="Reference to the department that owns the data source, null if not department-owned",
        default=None,
    )
    sensitivity_level: DataSourceSensitivityLevel = Field(
        description="Data sensitivity level (public, internal, confidential, restricted)"
    )
    status: DataSourceStatus = Field(
        description="Current status of the data source (active, inactive, deprecated, maintenance)"
    )
    description: str = Field(description="Description of the data source")
    created_at: str = Field(description="Timestamp when the data source was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the data source was last updated (ISO 8601)")


class DataAccessGrant(BaseModel):
    """Represents a grant of access to a data source for an employee"""

    data_access_grant_ref: str = Field(description="Unique identifier for the data access grant")
    data_source_ref: str = Field(description="Reference to the data source")
    grantee_employee_ref: str = Field(description="Employee reference of the grantee")
    access_level: DataAccessGrantLevel = Field(
        description="Level of access granted (read, write, admin, full)"
    )
    scope: str = Field(description="Scope of the access grant within the data source")
    granted_by_ref: str = Field(description="Employee reference of the person who granted access")
    granted_at: str = Field(description="Timestamp when access was granted (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the grant, null if no expiration (ISO 8601)",
        default=None,
    )
    status: DataAccessGrantStatus = Field(
        description="Current status of the grant (active, revoked, expired)"
    )
    business_justification: str = Field(description="Business justification for the access grant")
    created_at: str = Field(description="Timestamp when the grant record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the grant record was last updated (ISO 8601)")


class DataAsset(BaseModel):
    """Represents a data asset such as a table, view, or collection within a data source"""

    data_asset_ref: str = Field(description="Unique identifier for the data asset")
    data_source_ref: str = Field(description="Reference to the data source containing this asset")
    asset_name: str = Field(description="Name of the data asset")
    asset_type: DataAssetType = Field(
        description="Type of data asset (table, view, collection, index, topic, bucket, file, api_endpoint)"
    )
    schema_name: str = Field(description="Schema or namespace of the data asset")
    field_definitions: List[Dict[str, Any]] = Field(description="List of field definitions for the data asset")
    owner_employee_ref: str = Field(description="Employee reference of the data asset owner")
    steward_employee_ref: Optional[str] = Field(
        description="Employee reference of the data steward, null if not assigned",
        default=None,
    )
    department_ref: Optional[str] = Field(
        description="Reference to the department that owns the data asset, null if not department-owned",
        default=None,
    )
    sensitivity_level: DataAssetSensitivityLevel = Field(
        description="Data sensitivity level (public, internal, confidential, restricted)"
    )
    update_frequency: DataAssetUpdateFrequency = Field(
        description="How frequently the data asset is updated (realtime, hourly, daily, weekly, monthly, manual, unknown)"
    )
    row_count: Optional[int] = Field(
        description="Approximate number of rows or records, null if unknown",
        default=None,
    )
    last_updated_at: Optional[str] = Field(
        description="Timestamp when the data asset was last updated with data, null if unknown (ISO 8601)",
        default=None,
    )
    tags: List[str] = Field(description="List of tags for categorization and discovery")
    description: str = Field(description="Description of the data asset")
    status: DataAssetStatus = Field(
        description="Current status of the data asset (active, deprecated, archived)"
    )
    created_at: str = Field(description="Timestamp when the data asset was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the data asset record was last updated (ISO 8601)")


class DataTransferJob(BaseModel):
    """Represents a data transfer or ETL job"""

    data_transfer_job_ref: str = Field(description="Unique identifier for the data transfer job")
    job_name: str = Field(description="Name of the data transfer job")
    transfer_type: DataTransferType = Field(
        description="Type of transfer (import, export, sync, migration, backup)"
    )
    source_data_source_ref: Optional[str] = Field(
        description="Reference to the source data source, null if not applicable",
        default=None,
    )
    target_data_source_ref: Optional[str] = Field(
        description="Reference to the target data source, null if not applicable",
        default=None,
    )
    source_file_ref: Optional[str] = Field(
        description="Reference to the source file attachment, null if not applicable",
        default=None,
    )
    target_file_ref: Optional[str] = Field(
        description="Reference to the target file attachment, null if not applicable",
        default=None,
    )
    data_format: DataTransferFormat = Field(
        description="Format of the data being transferred (csv, json, parquet, avro, xml, sql, excel, other)"
    )
    record_count: Optional[int] = Field(
        description="Number of records transferred, null if not yet completed",
        default=None,
    )
    file_size_bytes: Optional[int] = Field(
        description="Size of the transferred data in bytes, null if not yet completed",
        default=None,
    )
    initiated_by_ref: str = Field(description="Employee reference of the person who initiated the transfer")
    job_status: DataTransferJobStatus = Field(
        description="Current status of the job (pending, running, completed, failed, cancelled)"
    )
    started_at: Optional[str] = Field(
        description="Timestamp when the job started, null if not yet started (ISO 8601)",
        default=None,
    )
    completed_at: Optional[str] = Field(
        description="Timestamp when the job completed, null if not yet completed (ISO 8601)",
        default=None,
    )
    error_message: Optional[str] = Field(
        description="Error message if the job failed, null otherwise",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the job record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the job record was last updated (ISO 8601)")


class NetworkZone(BaseModel):
    """Represents a network zone or segment within the organization"""

    network_zone_ref: str = Field(description="Unique identifier for the network zone")
    zone_name: str = Field(description="Name of the network zone")
    zone_type: NetworkZoneType = Field(
        description="Type of network zone (corporate, dmz, guest, production, development, restricted)"
    )
    cidr_range: str = Field(description="CIDR range of the network zone")
    location: str = Field(description="Physical or logical location of the network zone")
    vlan_id: Optional[int] = Field(
        description="VLAN ID of the network zone, null if not applicable",
        default=None,
    )
    gateway: str = Field(description="Gateway IP address of the network zone")
    dns_servers: List[str] = Field(description="List of DNS server addresses for the network zone")
    status: NetworkZoneStatus = Field(
        description="Current status of the network zone (active, inactive, maintenance)"
    )
    description: str = Field(description="Description of the network zone")
    created_at: str = Field(description="Timestamp when the network zone was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the network zone was last updated (ISO 8601)")


class VPNConnection(BaseModel):
    """Represents a VPN connection profile for an employee"""

    vpn_connection_ref: str = Field(description="Unique identifier for the VPN connection")
    employee_ref: str = Field(description="Reference to the employee")
    vpn_profile: str = Field(description="VPN profile name or configuration identifier")
    assigned_ip: str = Field(description="IP address assigned to the VPN connection")
    connection_status: VPNConnectionStatus = Field(
        description="Current connection status (connected, disconnected, error)"
    )
    last_connected_at: Optional[str] = Field(
        description="Timestamp of the last successful connection, null if never connected (ISO 8601)",
        default=None,
    )
    last_disconnected_at: Optional[str] = Field(
        description="Timestamp of the last disconnection, null if never disconnected (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the VPN connection was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the VPN connection was last updated (ISO 8601)")


class GuestWifiCredential(BaseModel):
    """Represents a guest Wi-Fi access credential"""

    guest_wifi_credential_ref: str = Field(description="Unique identifier for the guest Wi-Fi credential")
    guest_name: str = Field(description="Name of the guest")
    guest_company: str = Field(description="Company or organization of the guest")
    guest_phone: str = Field(description="Phone number of the guest")
    host_employee_ref: str = Field(description="Employee reference of the host who requested the credential")
    ssid: str = Field(description="Wi-Fi SSID for the guest network")
    access_code: str = Field(description="Access code or password for the guest Wi-Fi")
    network_zone_ref: Optional[str] = Field(
        description="Reference to the network zone for the guest Wi-Fi, null if not specified",
        default=None,
    )
    valid_from: str = Field(description="Timestamp when the credential becomes valid (ISO 8601)")
    valid_until: str = Field(description="Timestamp when the credential expires (ISO 8601)")
    max_devices: int = Field(description="Maximum number of devices allowed to connect simultaneously")
    bandwidth_limit_mbps: Optional[int] = Field(
        description="Bandwidth limit in Mbps, null if no limit",
        default=None,
    )
    status: GuestWifiCredentialStatus = Field(
        description="Current status of the credential (active, expired, revoked)"
    )
    created_at: str = Field(description="Timestamp when the credential was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the credential was last updated (ISO 8601)")


class NetworkAccessRule(BaseModel):
    """Represents a network access control rule"""

    network_access_rule_ref: str = Field(description="Unique identifier for the network access rule")
    rule_name: str = Field(description="Name of the access rule")
    subject_type: NetworkAccessRuleSubjectType = Field(
        description="Type of subject the rule applies to (employee, team, department, role, ip_range)"
    )
    subject_ref: str = Field(description="Reference to the subject entity")
    network_zone_ref: str = Field(description="Reference to the network zone the rule applies to")
    target_resource: str = Field(description="Target resource or service the rule controls access to")
    protocol: NetworkAccessRuleProtocol = Field(
        description="Network protocol (tcp, udp, icmp, any)"
    )
    port_range: str = Field(description="Port range the rule applies to (e.g., 80, 443, 8000-9000)")
    action: NetworkAccessRuleAction = Field(
        description="Action to take (allow, deny)"
    )
    priority: int = Field(description="Priority of the rule, lower numbers have higher priority")
    status: NetworkAccessRuleStatus = Field(
        description="Current status of the rule (active, disabled, expired)"
    )
    granted_by_ref: str = Field(description="Employee reference of the person who created the rule")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the rule, null if no expiration (ISO 8601)",
        default=None,
    )
    description: str = Field(description="Description of the access rule")
    created_at: str = Field(description="Timestamp when the rule was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the rule was last updated (ISO 8601)")


class NetworkIncident(BaseModel):
    """Represents a network incident or outage"""

    network_incident_ref: str = Field(description="Unique identifier for the network incident")
    reporter_employee_ref: str = Field(description="Employee reference of the person who reported the incident")
    network_zone_ref: Optional[str] = Field(
        description="Reference to the affected network zone, null if not zone-specific",
        default=None,
    )
    incident_type: NetworkIncidentType = Field(
        description="Type of incident (connectivity_loss, performance_degradation, security_breach, dns_failure, hardware_failure, configuration_error)"
    )
    severity: NetworkIncidentSeverity = Field(
        description="Severity level of the incident (low, medium, high, critical)"
    )
    affected_scope: str = Field(description="Description of the scope affected by the incident")
    description: str = Field(description="Detailed description of the incident")
    diagnosis: Optional[str] = Field(
        description="Diagnosis of the root cause, null if not yet diagnosed",
        default=None,
    )
    resolution: Optional[str] = Field(
        description="Description of the resolution, null if not yet resolved",
        default=None,
    )
    status: NetworkIncidentStatus = Field(
        description="Current status of the incident (open, investigating, resolved, closed)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the person assigned to handle the incident, null if unassigned",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the incident was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    occurred_at: str = Field(description="Timestamp when the incident occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the incident record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the incident record was last updated (ISO 8601)")


class SoftwareCatalog(BaseModel):
    """Represents a software entry in the organization's approved software catalog"""

    software_catalog_ref: str = Field(description="Unique identifier for the software catalog entry")
    software_name: str = Field(description="Name of the software")
    software_code: str = Field(description="Short code for the software")
    vendor: str = Field(description="Vendor or publisher of the software")
    category: SoftwareCategory = Field(
        description="Category of the software (office, development, design, communication, security, database, monitoring, analytics, other)"
    )
    current_version: str = Field(description="Current approved version of the software")
    supported_os: List[str] = Field(description="List of supported operating systems")
    download_uri: str = Field(description="URI to download the software")
    installation_guide_uri: Optional[str] = Field(
        description="URI to the installation guide, null if not available",
        default=None,
    )
    is_core: bool = Field(description="Whether this is a core/mandatory software for the organization")
    requires_license: bool = Field(description="Whether the software requires a license")
    requires_approval: bool = Field(description="Whether installation requires approval")
    security_reviewed: bool = Field(description="Whether the software has been security reviewed")
    compliance_status: SoftwareComplianceStatus = Field(
        description="Compliance status (approved, pending_review, rejected, conditional)"
    )
    description: str = Field(description="Description of the software")
    status: SoftwareCatalogStatus = Field(
        description="Current status of the catalog entry (active, deprecated, retired)"
    )
    created_at: str = Field(description="Timestamp when the catalog entry was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the catalog entry was last updated (ISO 8601)")


class SoftwareLicense(BaseModel):
    """Represents a software license owned by the organization"""

    software_license_ref: str = Field(description="Unique identifier for the software license")
    software_catalog_ref: str = Field(description="Reference to the software catalog entry")
    license_key: str = Field(description="License key or activation code")
    license_type: SoftwareLicenseType = Field(
        description="Type of license (per_seat, per_device, site, enterprise, open_source, trial, subscription)"
    )
    total_seats: int = Field(description="Total number of seats or activations available")
    used_seats: int = Field(description="Number of seats currently in use")
    vendor_contract_ref: str = Field(description="Reference to the vendor contract")
    purchase_date: str = Field(description="Date the license was purchased (ISO 8601 date)")
    expiry_date: str = Field(description="Date the license expires (ISO 8601 date)")
    cost_per_unit: float = Field(description="Cost per unit or seat")
    currency: str = Field(description="Currency code for the cost (e.g., CNY, USD)")
    auto_renew: bool = Field(description="Whether the license auto-renews")
    status: SoftwareLicenseStatus = Field(
        description="Current status of the license (active, expired, cancelled, pending_renewal)"
    )
    managed_by_ref: str = Field(description="Employee reference of the person managing the license")
    notes: str = Field(description="Additional notes about the license")
    created_at: str = Field(description="Timestamp when the license was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the license was last updated (ISO 8601)")


class SoftwareLicenseAssignment(BaseModel):
    """Represents the assignment of a software license to an employee"""

    software_license_assignment_ref: str = Field(description="Unique identifier for the license assignment")
    software_license_ref: str = Field(description="Reference to the software license")
    employee_ref: str = Field(description="Reference to the employee assigned the license")
    assigned_by_ref: str = Field(description="Employee reference of the person who assigned the license")
    assigned_at: str = Field(description="Timestamp when the license was assigned (ISO 8601)")
    revoked_at: Optional[str] = Field(
        description="Timestamp when the license was revoked, null if still active (ISO 8601)",
        default=None,
    )
    status: SoftwareLicenseAssignmentStatus = Field(
        description="Current status of the assignment (active, revoked)"
    )
    created_at: str = Field(description="Timestamp when the assignment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the assignment was last updated (ISO 8601)")


class SoftwareInstallation(BaseModel):
    """Represents an installation of software on a device"""

    software_installation_ref: str = Field(description="Unique identifier for the software installation")
    software_catalog_ref: str = Field(description="Reference to the software catalog entry")
    employee_ref: str = Field(description="Reference to the employee who installed the software")
    device_name: str = Field(description="Name or identifier of the device where the software is installed")
    installed_version: str = Field(description="Version of the software installed")
    installation_status: SoftwareInstallationStatus = Field(
        description="Current installation status (installed, pending, failed, uninstalled)"
    )
    installed_at: str = Field(description="Timestamp when the software was installed (ISO 8601)")
    uninstalled_at: Optional[str] = Field(
        description="Timestamp when the software was uninstalled, null if still installed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the installation record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the installation record was last updated (ISO 8601)")


class SoftwareFiling(BaseModel):
    """Represents a filing request for new or unapproved software"""

    software_filing_ref: str = Field(description="Unique identifier for the software filing")
    software_catalog_ref: Optional[str] = Field(
        description="Reference to the software catalog entry, null if new software not yet in catalog",
        default=None,
    )
    software_name: str = Field(description="Name of the software being filed")
    vendor: str = Field(description="Vendor or publisher of the software")
    version: str = Field(description="Version of the software being filed")
    purpose: str = Field(description="Purpose or use case for the software")
    data_sensitivity: SoftwareFilingDataSensitivity = Field(
        description="Data sensitivity level of the software (public, internal, confidential, restricted)"
    )
    filed_by_ref: str = Field(description="Employee reference of the person who filed the request")
    department_ref: str = Field(description="Reference to the department requesting the software")
    security_review_status: SoftwareFilingReviewStatus = Field(
        description="Security review status (pending, approved, rejected)"
    )
    compliance_review_status: SoftwareFilingReviewStatus = Field(
        description="Compliance review status (pending, approved, rejected)"
    )
    reviewed_by_ref: Optional[str] = Field(
        description="Employee reference of the reviewer, null if not yet reviewed",
        default=None,
    )
    reviewed_at: Optional[str] = Field(
        description="Timestamp when the filing was reviewed, null if not yet reviewed (ISO 8601)",
        default=None,
    )
    filing_status: SoftwareFilingStatus = Field(
        description="Current status of the filing (pending, approved, rejected, withdrawn)"
    )
    rejection_reason: Optional[str] = Field(
        description="Reason for rejection, null if not rejected",
        default=None,
    )
    notes: str = Field(description="Additional notes about the filing")
    created_at: str = Field(description="Timestamp when the filing was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the filing was last updated (ISO 8601)")


class Printer(BaseModel):
    """Represents a printer managed within the organization"""

    printer_ref: str = Field(description="Unique identifier for the printer")
    printer_name: str = Field(description="Display name of the printer")
    printer_model: str = Field(description="Model of the printer")
    manufacturer: str = Field(description="Manufacturer of the printer")
    serial_number: str = Field(description="Serial number of the printer")
    ip_address: str = Field(description="IP address of the printer on the network")
    location_building: str = Field(description="Building where the printer is located")
    location_floor: str = Field(description="Floor where the printer is located")
    location_area: str = Field(description="Area or room where the printer is located")
    capabilities: List[str] = Field(description="List of printer capabilities")
    supports_color: bool = Field(description="Whether the printer supports color printing")
    supports_duplex: bool = Field(description="Whether the printer supports duplex (double-sided) printing")
    supports_scan: bool = Field(description="Whether the printer supports scanning")
    driver_download_uri: str = Field(description="URI to download the printer driver")
    printer_status: PrinterStatus = Field(
        description="Current status of the printer (online, offline, error, maintenance, decommissioned)"
    )
    department_ref: Optional[str] = Field(
        description="Reference to the department that owns the printer, null if shared",
        default=None,
    )
    managed_by_ref: str = Field(description="Employee reference of the person managing the printer")
    description: str = Field(description="Description of the printer")
    created_at: str = Field(description="Timestamp when the printer was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the printer was last updated (ISO 8601)")


class PrinterSupply(BaseModel):
    """Represents a supply item for a printer"""

    printer_supply_ref: str = Field(description="Unique identifier for the printer supply")
    printer_ref: str = Field(description="Reference to the printer")
    supply_type: PrinterSupplyType = Field(
        description="Type of supply (toner, ink, drum, paper, fuser, waste_container, other)"
    )
    supply_name: str = Field(description="Name of the supply item")
    supply_model: str = Field(description="Model number of the supply item")
    remaining_percent: int = Field(description="Remaining percentage of the supply (0-100)")
    stock_quantity: int = Field(description="Number of replacement units in stock")
    reorder_threshold: int = Field(description="Stock quantity threshold for reordering")
    unit_cost: float = Field(description="Cost per unit of the supply")
    currency: str = Field(description="Currency code for the cost (e.g., CNY, USD)")
    supplier: str = Field(description="Name of the supplier")
    last_replaced_at: Optional[str] = Field(
        description="Timestamp when the supply was last replaced, null if never replaced (ISO 8601)",
        default=None,
    )
    status: PrinterSupplyStatus = Field(
        description="Current status of the supply (normal, low, critical, empty, replaced)"
    )
    created_at: str = Field(description="Timestamp when the supply record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the supply record was last updated (ISO 8601)")


class PrinterIncident(BaseModel):
    """Represents an incident or issue with a printer"""

    printer_incident_ref: str = Field(description="Unique identifier for the printer incident")
    printer_ref: str = Field(description="Reference to the printer")
    reporter_employee_ref: str = Field(description="Employee reference of the person who reported the incident")
    incident_type: PrinterIncidentType = Field(
        description="Type of incident (paper_jam, toner_issue, connectivity, print_quality, hardware_failure, driver_issue, other)"
    )
    description: str = Field(description="Detailed description of the incident")
    diagnosis: Optional[str] = Field(
        description="Diagnosis of the issue, null if not yet diagnosed",
        default=None,
    )
    resolution: Optional[str] = Field(
        description="Description of the resolution, null if not yet resolved",
        default=None,
    )
    status: PrinterIncidentStatus = Field(
        description="Current status of the incident (open, in_progress, resolved, closed)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the person assigned to handle the incident, null if unassigned",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the incident was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the incident record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the incident record was last updated (ISO 8601)")


class FileTransfer(BaseModel):
    """Represents a file transfer operation"""

    file_transfer_ref: str = Field(description="Unique identifier for the file transfer")
    file_attachment_ref: str = Field(description="Reference to the file attachment being transferred")
    transfer_type: FileTransferType = Field(
        description="Type of transfer (upload, download, share, sync)"
    )
    source: str = Field(description="Source location of the file transfer")
    destination: str = Field(description="Destination location of the file transfer")
    initiated_by_ref: str = Field(description="Employee reference of the person who initiated the transfer")
    recipient_employee_refs: List[str] = Field(description="List of employee references of the recipients")
    encryption_applied: bool = Field(description="Whether encryption was applied to the transfer")
    encryption_method: Optional[str] = Field(
        description="Encryption method used, null if no encryption applied",
        default=None,
    )
    transfer_status: FileTransferStatus = Field(
        description="Current status of the transfer (pending, in_progress, completed, failed, expired)"
    )
    file_size_bytes: int = Field(description="Size of the file being transferred in bytes")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the transfer link, null if no expiration (ISO 8601)",
        default=None,
    )
    access_password_set: bool = Field(description="Whether an access password is set for the transfer")
    download_count: int = Field(description="Number of times the file has been downloaded")
    max_downloads: Optional[int] = Field(
        description="Maximum number of downloads allowed, null if unlimited",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the transfer was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the transfer was last updated (ISO 8601)")


class FileSecurityPolicy(BaseModel):
    """Represents a security policy for file handling"""

    file_security_policy_ref: str = Field(description="Unique identifier for the file security policy")
    policy_name: str = Field(description="Name of the security policy")
    classification_level: FileClassificationLevel = Field(
        description="Classification level (public, internal, confidential, restricted, top_secret)"
    )
    encryption_required: bool = Field(description="Whether encryption is required for files under this policy")
    encryption_algorithm: str = Field(description="Encryption algorithm to use (e.g., AES-256)")
    allowed_share_scope: FileShareScope = Field(
        description="Allowed sharing scope (public, company, department, team, individual)"
    )
    watermark_required: bool = Field(description="Whether watermarking is required")
    download_restricted: bool = Field(description="Whether downloads are restricted")
    print_restricted: bool = Field(description="Whether printing is restricted")
    retention_days: Optional[int] = Field(
        description="Number of days to retain files, null if no retention limit",
        default=None,
    )
    applicable_file_types: List[str] = Field(description="List of file types this policy applies to")
    department_ref: Optional[str] = Field(
        description="Reference to the department this policy applies to, null if organization-wide",
        default=None,
    )
    status: FileSecurityPolicyStatus = Field(
        description="Current status of the policy (active, disabled, archived)"
    )
    description: str = Field(description="Description of the security policy")
    created_at: str = Field(description="Timestamp when the policy was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the policy was last updated (ISO 8601)")


class ITServiceTicket(BaseModel):
    """Represents an IT service desk ticket"""

    it_service_ticket_ref: str = Field(description="Unique identifier for the IT service ticket")
    ticket_number: str = Field(description="Human-readable ticket number (e.g., IT-2025-00001)")
    requester_employee_ref: str = Field(description="Employee reference of the ticket requester")
    ticket_category: TicketCategory = Field(
        description="Category of the ticket (incident, service_request, change_request, problem, inquiry)"
    )
    ticket_subcategory: TicketSubcategory = Field(
        description="Subcategory of the ticket (software_fault, hardware_fault, network_issue, access_request, account_issue, email_issue, printer_issue, vpn_issue, security_concern, data_request, new_equipment, software_install, general_inquiry, other)"
    )
    related_system_ref: Optional[str] = Field(
        description="Reference to the related IT system, null if not system-specific",
        default=None,
    )
    related_printer_ref: Optional[str] = Field(
        description="Reference to the related printer, null if not printer-specific",
        default=None,
    )
    related_email_account_ref: Optional[str] = Field(
        description="Reference to the related email account, null if not email-specific",
        default=None,
    )
    title: str = Field(description="Title of the ticket")
    description: str = Field(description="Detailed description of the issue or request")
    urgency: TicketUrgency = Field(
        description="Urgency level (low, medium, high, critical)"
    )
    impact: TicketImpact = Field(
        description="Impact level (individual, team, department, company)"
    )
    priority: TicketPriority = Field(
        description="Priority level (P1, P2, P3, P4)"
    )
    ticket_status: TicketStatus = Field(
        description="Current status of the ticket (open, in_progress, pending, resolved, closed, cancelled)"
    )
    assigned_to_ref: Optional[str] = Field(
        description="Employee reference of the person assigned to the ticket, null if unassigned",
        default=None,
    )
    assigned_group: Optional[str] = Field(
        description="Name of the support group assigned, null if not assigned to a group",
        default=None,
    )
    escalation_level: int = Field(description="Current escalation level of the ticket")
    resolution_summary: Optional[str] = Field(
        description="Summary of the resolution, null if not yet resolved",
        default=None,
    )
    resolution_category: Optional[ResolutionCategory] = Field(
        description="Category of the resolution, null if not yet resolved",
        default=None,
    )
    satisfaction_rating: Optional[int] = Field(
        description="Customer satisfaction rating (1-5), null if not yet rated",
        default=None,
    )
    satisfaction_comment: Optional[str] = Field(
        description="Customer satisfaction comment, null if not yet provided",
        default=None,
    )
    sla_due_at: Optional[str] = Field(
        description="SLA due timestamp, null if no SLA defined (ISO 8601)",
        default=None,
    )
    first_responded_at: Optional[str] = Field(
        description="Timestamp of the first response, null if not yet responded (ISO 8601)",
        default=None,
    )
    resolved_at: Optional[str] = Field(
        description="Timestamp when the ticket was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    closed_at: Optional[str] = Field(
        description="Timestamp when the ticket was closed, null if not yet closed (ISO 8601)",
        default=None,
    )
    reopened_count: int = Field(description="Number of times the ticket has been reopened")
    created_at: str = Field(description="Timestamp when the ticket was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the ticket was last updated (ISO 8601)")


class ITServiceTicketComment(BaseModel):
    """Represents a comment on an IT service ticket"""

    it_service_ticket_comment_ref: str = Field(description="Unique identifier for the ticket comment")
    it_service_ticket_ref: str = Field(description="Reference to the IT service ticket")
    author_employee_ref: str = Field(description="Employee reference of the comment author")
    comment_type: TicketCommentType = Field(
        description="Type of comment (reply, note, resolution, escalation, system)"
    )
    content: str = Field(description="Content of the comment")
    is_internal: bool = Field(description="Whether the comment is internal (not visible to requester)")
    attachment_file_refs: List[str] = Field(description="List of file attachment references")
    created_at: str = Field(description="Timestamp when the comment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the comment was last updated (ISO 8601)")


class ITServiceContact(BaseModel):
    """Represents an IT service contact point"""

    it_service_contact_ref: str = Field(description="Unique identifier for the IT service contact")
    contact_name: str = Field(description="Name of the contact point")
    contact_type: ITServiceContactType = Field(
        description="Type of contact (hotline, email, chat, walk_in, self_service)"
    )
    phone_number: str = Field(description="Phone number of the contact")
    email: str = Field(description="Email address of the contact")
    service_hours: str = Field(description="Service hours description")
    location: str = Field(description="Physical location of the contact point")
    supported_categories: List[str] = Field(description="List of ticket categories supported by this contact")
    description: str = Field(description="Description of the service contact")
    status: ITServiceContactStatus = Field(
        description="Current status of the contact (active, inactive)"
    )
    created_at: str = Field(description="Timestamp when the contact was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the contact was last updated (ISO 8601)")


class ITKnowledgeArticle(BaseModel):
    """Represents a knowledge base article for IT support"""

    it_knowledge_article_ref: str = Field(description="Unique identifier for the knowledge article")
    article_title: str = Field(description="Title of the knowledge article")
    article_category: ITKnowledgeArticleCategory = Field(
        description="Category of the article (faq, how_to, troubleshooting, policy, announcement, best_practice)"
    )
    related_categories: List[str] = Field(description="List of related categories for cross-referencing")
    content: str = Field(description="Full content of the knowledge article")
    author_employee_ref: str = Field(description="Employee reference of the article author")
    view_count: int = Field(description="Number of times the article has been viewed")
    helpful_count: int = Field(description="Number of times the article was marked as helpful")
    tags: List[str] = Field(description="List of tags for categorization and search")
    status: ITKnowledgeArticleStatus = Field(
        description="Current status of the article (draft, published, archived, deprecated)"
    )
    published_at: Optional[str] = Field(
        description="Timestamp when the article was published, null if not yet published (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the article was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the article was last updated (ISO 8601)")


class ITDB(OfficeDB):
    """Database containing IT module data including systems, accounts, code repositories, deployments, network, software, printers, and service desk"""

    it_system: Dict[str, ITSystem] = Field(
        description="Dictionary of all IT systems indexed by it_system_ref"
    )
    it_system_account: Dict[str, ITSystemAccount] = Field(
        description="Dictionary of all IT system accounts indexed by it_system_account_ref"
    )
    it_system_account_permission: Dict[str, ITSystemAccountPermission] = Field(
        description="Dictionary of all IT system account permissions indexed by it_system_account_permission_ref"
    )
    access_anomaly: Dict[str, AccessAnomaly] = Field(
        description="Dictionary of all access anomalies indexed by access_anomaly_ref"
    )
    account_migration: Dict[str, AccountMigration] = Field(
        description="Dictionary of all account migrations indexed by account_migration_ref"
    )
    email_account: Dict[str, EmailAccount] = Field(
        description="Dictionary of all email accounts indexed by email_account_ref"
    )
    email_distribution_list: Dict[str, EmailDistributionList] = Field(
        description="Dictionary of all email distribution lists indexed by email_distribution_list_ref"
    )
    email_distribution_list_member: Dict[str, EmailDistributionListMember] = Field(
        description="Dictionary of all email distribution list members indexed by email_distribution_list_member_ref"
    )
    email_security_event: Dict[str, EmailSecurityEvent] = Field(
        description="Dictionary of all email security events indexed by email_security_event_ref"
    )
    code_repository: Dict[str, CodeRepository] = Field(
        description="Dictionary of all code repositories indexed by code_repository_ref"
    )
    code_repository_member: Dict[str, CodeRepositoryMember] = Field(
        description="Dictionary of all code repository members indexed by code_repository_member_ref"
    )
    code_branch: Dict[str, CodeBranch] = Field(
        description="Dictionary of all code branches indexed by code_branch_ref"
    )
    merge_request: Dict[str, MergeRequest] = Field(
        description="Dictionary of all merge requests indexed by merge_request_ref"
    )
    merge_request_reviewer: Dict[str, MergeRequestReviewer] = Field(
        description="Dictionary of all merge request reviewers indexed by merge_request_reviewer_ref"
    )
    merge_request_activity: Dict[str, MergeRequestActivity] = Field(
        description="Dictionary of all merge request activities indexed by merge_request_activity_ref"
    )
    ci_cd_pipeline: Dict[str, CICDPipeline] = Field(
        description="Dictionary of all CI/CD pipelines indexed by ci_cd_pipeline_ref"
    )
    pipeline_execution: Dict[str, PipelineExecution] = Field(
        description="Dictionary of all pipeline executions indexed by pipeline_execution_ref"
    )
    deployment: Dict[str, Deployment] = Field(
        description="Dictionary of all deployments indexed by deployment_ref"
    )
    deploy_environment: Dict[str, DeployEnvironment] = Field(
        description="Dictionary of all deployment environments indexed by deploy_environment_ref"
    )
    it_resource: Dict[str, ITResource] = Field(
        description="Dictionary of all IT resources indexed by it_resource_ref"
    )
    it_resource_request: Dict[str, ITResourceRequest] = Field(
        description="Dictionary of all IT resource requests indexed by it_resource_request_ref"
    )
    dev_environment: Dict[str, DevEnvironment] = Field(
        description="Dictionary of all development environments indexed by dev_environment_ref"
    )
    data_source: Dict[str, DataSource] = Field(
        description="Dictionary of all data sources indexed by data_source_ref"
    )
    data_access_grant: Dict[str, DataAccessGrant] = Field(
        description="Dictionary of all data access grants indexed by data_access_grant_ref"
    )
    data_asset: Dict[str, DataAsset] = Field(
        description="Dictionary of all data assets indexed by data_asset_ref"
    )
    data_transfer_job: Dict[str, DataTransferJob] = Field(
        description="Dictionary of all data transfer jobs indexed by data_transfer_job_ref"
    )
    network_zone: Dict[str, NetworkZone] = Field(
        description="Dictionary of all network zones indexed by network_zone_ref"
    )
    vpn_connection: Dict[str, VPNConnection] = Field(
        description="Dictionary of all VPN connections indexed by vpn_connection_ref"
    )
    guest_wifi_credential: Dict[str, GuestWifiCredential] = Field(
        description="Dictionary of all guest Wi-Fi credentials indexed by guest_wifi_credential_ref"
    )
    network_access_rule: Dict[str, NetworkAccessRule] = Field(
        description="Dictionary of all network access rules indexed by network_access_rule_ref"
    )
    network_incident: Dict[str, NetworkIncident] = Field(
        description="Dictionary of all network incidents indexed by network_incident_ref"
    )
    software_catalog: Dict[str, SoftwareCatalog] = Field(
        description="Dictionary of all software catalog entries indexed by software_catalog_ref"
    )
    software_license: Dict[str, SoftwareLicense] = Field(
        description="Dictionary of all software licenses indexed by software_license_ref"
    )
    software_license_assignment: Dict[str, SoftwareLicenseAssignment] = Field(
        description="Dictionary of all software license assignments indexed by software_license_assignment_ref"
    )
    software_installation: Dict[str, SoftwareInstallation] = Field(
        description="Dictionary of all software installations indexed by software_installation_ref"
    )
    software_filing: Dict[str, SoftwareFiling] = Field(
        description="Dictionary of all software filings indexed by software_filing_ref"
    )
    printer: Dict[str, Printer] = Field(
        description="Dictionary of all printers indexed by printer_ref"
    )
    printer_supply: Dict[str, PrinterSupply] = Field(
        description="Dictionary of all printer supplies indexed by printer_supply_ref"
    )
    printer_incident: Dict[str, PrinterIncident] = Field(
        description="Dictionary of all printer incidents indexed by printer_incident_ref"
    )
    file_transfer: Dict[str, FileTransfer] = Field(
        description="Dictionary of all file transfers indexed by file_transfer_ref"
    )
    file_security_policy: Dict[str, FileSecurityPolicy] = Field(
        description="Dictionary of all file security policies indexed by file_security_policy_ref"
    )
    it_service_ticket: Dict[str, ITServiceTicket] = Field(
        description="Dictionary of all IT service tickets indexed by it_service_ticket_ref"
    )
    it_service_ticket_comment: Dict[str, ITServiceTicketComment] = Field(
        description="Dictionary of all IT service ticket comments indexed by it_service_ticket_comment_ref"
    )
    it_service_contact: Dict[str, ITServiceContact] = Field(
        description="Dictionary of all IT service contacts indexed by it_service_contact_ref"
    )
    it_knowledge_article: Dict[str, ITKnowledgeArticle] = Field(
        description="Dictionary of all IT knowledge articles indexed by it_knowledge_article_ref"
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
        it_stats = {
            "num_it_systems": len(self.it_system),
            "num_it_system_accounts": len(self.it_system_account),
            "num_it_system_account_permissions": len(self.it_system_account_permission),
            "num_access_anomalies": len(self.access_anomaly),
            "num_account_migrations": len(self.account_migration),
            "num_email_accounts": len(self.email_account),
            "num_email_distribution_lists": len(self.email_distribution_list),
            "num_email_distribution_list_members": len(self.email_distribution_list_member),
            "num_email_security_events": len(self.email_security_event),
            "num_code_repositories": len(self.code_repository),
            "num_code_repository_members": len(self.code_repository_member),
            "num_code_branches": len(self.code_branch),
            "num_merge_requests": len(self.merge_request),
            "num_merge_request_reviewers": len(self.merge_request_reviewer),
            "num_merge_request_activities": len(self.merge_request_activity),
            "num_ci_cd_pipelines": len(self.ci_cd_pipeline),
            "num_pipeline_executions": len(self.pipeline_execution),
            "num_deployments": len(self.deployment),
            "num_deploy_environments": len(self.deploy_environment),
            "num_it_resources": len(self.it_resource),
            "num_it_resource_requests": len(self.it_resource_request),
            "num_dev_environments": len(self.dev_environment),
            "num_data_sources": len(self.data_source),
            "num_data_access_grants": len(self.data_access_grant),
            "num_data_assets": len(self.data_asset),
            "num_data_transfer_jobs": len(self.data_transfer_job),
            "num_network_zones": len(self.network_zone),
            "num_vpn_connections": len(self.vpn_connection),
            "num_guest_wifi_credentials": len(self.guest_wifi_credential),
            "num_network_access_rules": len(self.network_access_rule),
            "num_network_incidents": len(self.network_incident),
            "num_software_catalog": len(self.software_catalog),
            "num_software_licenses": len(self.software_license),
            "num_software_license_assignments": len(self.software_license_assignment),
            "num_software_installations": len(self.software_installation),
            "num_software_filings": len(self.software_filing),
            "num_printers": len(self.printer),
            "num_printer_supplies": len(self.printer_supply),
            "num_printer_incidents": len(self.printer_incident),
            "num_file_transfers": len(self.file_transfer),
            "num_file_security_policies": len(self.file_security_policy),
            "num_it_service_tickets": len(self.it_service_ticket),
            "num_it_service_ticket_comments": len(self.it_service_ticket_comment),
            "num_it_service_contacts": len(self.it_service_contact),
            "num_it_knowledge_articles": len(self.it_knowledge_article),
        }
        return {**base_stats, **it_stats}