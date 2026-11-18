from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.environment.db import DB


# --- Enums as Literal types ---

AccountStatus = Literal["active", "inactive", "suspended", "deleted"]
PreferredLocale = Literal["zh-CN", "en-US", "ja-JP", "ko-KR", "zh-TW"]
WorkerType = Literal["full_time", "intern", "campus_recruit", "campus_intern", "contractor"]
EmploymentStatus = Literal["active", "on_leave", "terminated", "probation"]
DepartmentType = Literal["business", "functional", "virtual"]
DepartmentStatus = Literal["active", "dissolved", "merging"]
MembershipRole = Literal["head", "deputy_head", "member"]
DepartmentMemberStatus = Literal["active", "removed"]
PositionTrack = Literal["P", "M"]
PositionStatus = Literal["active", "deprecated"]
JobFamily = Literal[
    "Engineering", "Product", "Design", "HR", "Finance",
    "Legal", "Marketing", "Operations", "Data", "Research"
]
TeamType = Literal["project", "interest", "committee", "taskforce"]
TeamStatus = Literal["active", "archived", "dissolved"]
TeamRole = Literal["lead", "tech_lead", "member", "observer"]
TeamMemberStatus = Literal["active", "removed"]
MentorshipType = Literal["onboarding", "career", "technical", "leadership"]
MentorshipStatus = Literal["active", "completed", "terminated"]
RoleType = Literal["system", "custom"]
RoleStatus = Literal["active", "deprecated"]
PermissionAction = Literal["create", "read", "update", "delete", "export", "approve"]
ScopeConstraint = Literal["all", "self", "department", "team"]
PermissionStatus = Literal["active", "deprecated"]
RolePermissionStatus = Literal["active", "revoked", "expired"]
EmployeeRoleScope = Literal["global", "department", "team"]
EmployeeRoleStatus = Literal["active", "revoked", "expired"]
ActorType = Literal["employee", "system", "api_client"]
AuditAction = Literal[
    "create", "read", "update", "delete", "login", "logout",
    "export", "approve", "reject", "assign", "revoke"
]
AuditResult = Literal["success", "failure", "partial"]
FilePurpose = Literal["avatar", "document", "contract", "certificate", "attachment", "export", "other"]
FileStatus = Literal["active", "archived", "deleted"]
ConfigType = Literal["string", "integer", "boolean", "json"]
SenderType = Literal["system", "employee"]
NotificationType = Literal["system", "mention", "approval", "assignment", "reminder", "announcement"]
NotificationChannel = Literal["in_app", "email", "sms", "push"]
ReadStatus = Literal["unread", "read", "dismissed"]


# --- Models ---


class UserProfile(BaseModel):
    """Represents a user profile with identity, contact, locale and account status"""

    user_profile_ref: str = Field(description="Unique identifier for the user profile")
    given_name: str = Field(description="User's given (first) name")
    family_name: str = Field(description="User's family (last) name")
    display_name: str = Field(description="User's display name shown in the system")
    avatar_file_ref: Optional[str] = Field(
        description="Reference to the file attachment used as avatar, null if not set",
        default=None,
    )
    bio: str = Field(description="Short biography or self-introduction of the user")
    phone: str = Field(description="User's phone number")
    account_status: AccountStatus = Field(
        description="Current account status (active, inactive, suspended, deleted)"
    )
    preferred_locale: PreferredLocale = Field(
        description="User's preferred locale (zh-CN, en-US, ja-JP, ko-KR, zh-TW)"
    )
    timezone: str = Field(description="User's timezone (e.g., Asia/Shanghai)")
    created_at: str = Field(description="Timestamp when the user profile was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the user profile was last updated (ISO 8601)")


class Employee(BaseModel):
    """Represents an employee with employment details, manager relationship and external system references"""

    employee_ref: str = Field(description="Unique identifier for the employee")
    user_profile_ref: str = Field(description="Reference to the associated user profile")
    employee_number: str = Field(description="Human-readable employee number (e.g., AI-2025-0001)")
    worker_type: WorkerType = Field(
        description="Type of worker (full_time, intern, campus_recruit, campus_intern, contractor)"
    )
    hire_date: str = Field(description="Date the employee was hired (ISO 8601 date)")
    termination_date: Optional[str] = Field(
        description="Date the employee was terminated, null if currently employed (ISO 8601 date)",
        default=None,
    )
    employment_status: EmploymentStatus = Field(
        description="Current employment status (active, on_leave, terminated, probation)"
    )
    direct_manager_ref: Optional[str] = Field(
        description="Employee reference of the direct manager, null if top-level",
        default=None,
    )
    position_ref: str = Field(description="Reference to the employee's position")
    external_ids: Dict[str, str] = Field(
        description="Dictionary of external system identifiers (e.g., hris_person_ref, asset_profile_ref)"
    )
    created_at: str = Field(description="Timestamp when the employee record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the employee record was last updated (ISO 8601)")


class Department(BaseModel):
    """Represents an organizational department with hierarchy, type and status"""

    department_ref: str = Field(description="Unique identifier for the department")
    department_name: str = Field(description="Name of the department")
    department_code: str = Field(description="Short code for the department")
    parent_department_ref: Optional[str] = Field(
        description="Reference to the parent department, null if root department",
        default=None,
    )
    department_level: int = Field(
        description="Depth in the organizational tree, root = 1"
    )
    department_type: DepartmentType = Field(
        description="Type of department (business, functional, virtual)"
    )
    department_status: DepartmentStatus = Field(
        description="Current status of the department (active, dissolved, merging)"
    )
    description: str = Field(description="Description of the department's purpose and responsibilities")
    display_order: int = Field(description="Order for display/sorting purposes")
    created_at: str = Field(description="Timestamp when the department was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the department was last updated (ISO 8601)")


class DepartmentMember(BaseModel):
    """Represents the membership relationship between an employee and a department"""

    department_member_ref: str = Field(description="Unique identifier for the department membership")
    department_ref: str = Field(description="Reference to the department")
    employee_ref: str = Field(description="Reference to the employee")
    membership_role: MembershipRole = Field(
        description="Role within the department (head, deputy_head, member)"
    )
    is_primary: bool = Field(
        description="Whether this is the employee's primary department"
    )
    joined_at: str = Field(description="Timestamp when the employee joined the department (ISO 8601)")
    left_at: Optional[str] = Field(
        description="Timestamp when the employee left the department, null if still active (ISO 8601)",
        default=None,
    )
    status: DepartmentMemberStatus = Field(
        description="Current membership status (active, removed)"
    )
    created_at: str = Field(description="Timestamp when the membership record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the membership record was last updated (ISO 8601)")


class Position(BaseModel):
    """Represents a job position with track, level and job family classification"""

    position_ref: str = Field(description="Unique identifier for the position")
    position_title: str = Field(description="Title of the position")
    position_code: str = Field(description="Short code for the position")
    position_track: PositionTrack = Field(
        description="Career track of the position (P for Professional, M for Management)"
    )
    position_level: int = Field(
        description="Numeric level within the track (e.g., 7 for P7, 3 for M3)"
    )
    job_family: JobFamily = Field(
        description="Job family classification (Engineering, Product, Design, HR, Finance, Legal, Marketing, Operations, Data, Research)"
    )
    job_subfamily: str = Field(
        description="Job subfamily or specialization (e.g., Backend, Frontend, ML, Infrastructure)"
    )
    position_status: PositionStatus = Field(
        description="Current status of the position (active, deprecated)"
    )
    description: str = Field(description="Description of the position's responsibilities")
    created_at: str = Field(description="Timestamp when the position was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the position was last updated (ISO 8601)")


class Team(BaseModel):
    """Represents a team with type, ownership and optional hierarchy"""

    team_ref: str = Field(description="Unique identifier for the team")
    team_name: str = Field(description="Name of the team")
    team_code: str = Field(description="Short code for the team")
    team_type: TeamType = Field(
        description="Type of team (project, interest, committee, taskforce)"
    )
    team_status: TeamStatus = Field(
        description="Current status of the team (active, archived, dissolved)"
    )
    description: str = Field(description="Description of the team's purpose and scope")
    owner_employee_ref: str = Field(
        description="Employee reference of the team owner/creator"
    )
    parent_team_ref: Optional[str] = Field(
        description="Reference to the parent team, null if top-level team",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the team was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the team was last updated (ISO 8601)")


class TeamMember(BaseModel):
    """Represents the membership relationship between an employee and a team"""

    team_member_ref: str = Field(description="Unique identifier for the team membership")
    team_ref: str = Field(description="Reference to the team")
    employee_ref: str = Field(description="Reference to the employee")
    team_role: TeamRole = Field(
        description="Role within the team (lead, tech_lead, member, observer)"
    )
    joined_at: str = Field(description="Timestamp when the employee joined the team (ISO 8601)")
    left_at: Optional[str] = Field(
        description="Timestamp when the employee left the team, null if still active (ISO 8601)",
        default=None,
    )
    status: TeamMemberStatus = Field(
        description="Current membership status (active, removed)"
    )
    created_at: str = Field(description="Timestamp when the membership record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the membership record was last updated (ISO 8601)")


class Mentorship(BaseModel):
    """Represents a mentorship relationship between two employees"""

    mentorship_ref: str = Field(description="Unique identifier for the mentorship")
    mentor_ref: str = Field(description="Employee reference of the mentor")
    mentee_ref: str = Field(description="Employee reference of the mentee")
    mentorship_type: MentorshipType = Field(
        description="Type of mentorship (onboarding, career, technical, leadership)"
    )
    start_date: str = Field(description="Start date of the mentorship (ISO 8601 date)")
    end_date: Optional[str] = Field(
        description="End date of the mentorship, null if ongoing (ISO 8601 date)",
        default=None,
    )
    status: MentorshipStatus = Field(
        description="Current status of the mentorship (active, completed, terminated)"
    )
    notes: str = Field(description="Additional notes about the mentorship")
    created_at: str = Field(description="Timestamp when the mentorship was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the mentorship was last updated (ISO 8601)")


class Role(BaseModel):
    """Represents an access control role that can be assigned to employees"""

    role_ref: str = Field(description="Unique identifier for the role")
    role_name: str = Field(description="Name of the role")
    role_code: str = Field(description="Short code for the role")
    role_type: RoleType = Field(
        description="Type of role (system, custom)"
    )
    role_status: RoleStatus = Field(
        description="Current status of the role (active, deprecated)"
    )
    description: str = Field(description="Description of the role's purpose and scope")
    is_default: bool = Field(
        description="Whether this role is automatically assigned to new employees"
    )
    created_at: str = Field(description="Timestamp when the role was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the role was last updated (ISO 8601)")


class Permission(BaseModel):
    """Represents a granular permission defining access to a resource action"""

    permission_ref: str = Field(description="Unique identifier for the permission")
    permission_code: str = Field(
        description="Permission code in resource:action format (e.g., employee:read)"
    )
    resource: str = Field(
        description="Resource the permission applies to (e.g., employee, department, team, file, audit_log)"
    )
    action: PermissionAction = Field(
        description="Action allowed by this permission (create, read, update, delete, export, approve)"
    )
    scope_constraint: ScopeConstraint = Field(
        description="Scope constraint for the permission (all, self, department, team)"
    )
    description: str = Field(description="Description of what this permission grants")
    permission_status: PermissionStatus = Field(
        description="Current status of the permission (active, deprecated)"
    )
    created_at: str = Field(description="Timestamp when the permission was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the permission was last updated (ISO 8601)")


class RolePermission(BaseModel):
    """Represents the binding between a role and a permission"""

    role_permission_ref: str = Field(description="Unique identifier for the role-permission binding")
    role_ref: str = Field(description="Reference to the role")
    permission_ref: str = Field(description="Reference to the permission")
    granted_by_ref: str = Field(
        description="Employee reference of the person who granted this binding"
    )
    granted_at: str = Field(description="Timestamp when the binding was granted (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the binding, null if no expiration (ISO 8601)",
        default=None,
    )
    status: RolePermissionStatus = Field(
        description="Current status of the binding (active, revoked, expired)"
    )
    created_at: str = Field(description="Timestamp when the binding was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the binding was last updated (ISO 8601)")


class EmployeeRole(BaseModel):
    """Represents the assignment of a role to an employee with optional scope"""

    employee_role_ref: str = Field(description="Unique identifier for the employee-role assignment")
    employee_ref: str = Field(description="Reference to the employee")
    role_ref: str = Field(description="Reference to the role")
    scope: EmployeeRoleScope = Field(
        description="Scope of the role assignment (global, department, team)"
    )
    scope_ref: Optional[str] = Field(
        description="Reference to the scoped entity (department_ref or team_ref), null when scope is global",
        default=None,
    )
    assigned_by_ref: str = Field(
        description="Employee reference of the person who made the assignment"
    )
    assigned_at: str = Field(description="Timestamp when the role was assigned (ISO 8601)")
    expires_at: Optional[str] = Field(
        description="Expiration timestamp for the assignment, null if no expiration (ISO 8601)",
        default=None,
    )
    status: EmployeeRoleStatus = Field(
        description="Current status of the assignment (active, revoked, expired)"
    )
    created_at: str = Field(description="Timestamp when the assignment was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the assignment was last updated (ISO 8601)")


class AuditLogChange(BaseModel):
    """Represents a single field change recorded in an audit log entry"""

    before: Optional[Any] = Field(description="Value before the change", default=None)
    after: Optional[Any] = Field(description="Value after the change", default=None)


class AuditLog(BaseModel):
    """Represents an audit log entry tracking actions performed in the system"""

    audit_log_ref: str = Field(description="Unique identifier for the audit log entry")
    actor_employee_ref: Optional[str] = Field(
        description="Employee reference of the actor, null for system actions",
        default=None,
    )
    actor_type: ActorType = Field(
        description="Type of actor (employee, system, api_client)"
    )
    action: AuditAction = Field(
        description="Action performed (create, read, update, delete, login, logout, export, approve, reject, assign, revoke)"
    )
    resource_type: str = Field(
        description="Type of resource affected (e.g., employee, department, team, role, permission, file_attachment)"
    )
    resource_ref: str = Field(description="Reference ID of the affected resource")
    description: str = Field(description="Human-readable description of the action")
    changes: Dict[str, AuditLogChange] = Field(
        description="Dictionary of field changes keyed by field name, with before/after values"
    )
    ip_address: Optional[str] = Field(
        description="IP address from which the action was performed, null for system actions",
        default=None,
    )
    user_agent: Optional[str] = Field(
        description="User agent string of the client, null for system actions",
        default=None,
    )
    request_id: Optional[str] = Field(
        description="Trace ID for correlating distributed requests, null for system actions",
        default=None,
    )
    result: AuditResult = Field(
        description="Result of the action (success, failure, partial)"
    )
    occurred_at: str = Field(description="Timestamp when the action occurred (ISO 8601)")
    created_at: str = Field(description="Timestamp when the audit log entry was created (ISO 8601)")


class FileAttachment(BaseModel):
    """Represents a file attachment uploaded and associated with a resource"""

    file_attachment_ref: str = Field(description="Unique identifier for the file attachment")
    file_name: str = Field(description="Original file name")
    file_extension: str = Field(
        description="File extension (e.g., pdf, png, jpg, docx, xlsx, csv, zip)"
    )
    mime_type: str = Field(description="MIME type of the file (e.g., application/pdf, image/png)")
    file_size_bytes: int = Field(description="Size of the file in bytes")
    storage_uri: str = Field(
        description="Unified storage URI (e.g., s3://bucket/path/to/file or oss://bucket/path/to/file)"
    )
    checksum: str = Field(description="SHA-256 hash of the file content")
    uploaded_by_ref: str = Field(description="Employee reference of the uploader")
    associated_resource_type: str = Field(
        description="Type of the associated entity (e.g., employee, department, team, user_profile)"
    )
    associated_resource_ref: str = Field(
        description="Reference ID of the associated entity"
    )
    file_purpose: FilePurpose = Field(
        description="Purpose of the file (avatar, document, contract, certificate, attachment, export, other)"
    )
    file_status: FileStatus = Field(
        description="Current status of the file (active, archived, deleted)"
    )
    uploaded_at: str = Field(description="Timestamp when the file was uploaded (ISO 8601)")
    created_at: str = Field(description="Timestamp when the file record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the file record was last updated (ISO 8601)")


class OrgConfig(BaseModel):
    """Represents an organization-level configuration key-value pair"""

    org_config_ref: str = Field(description="Unique identifier for the configuration entry")
    config_key: str = Field(
        description="Configuration key (e.g., company_name, logo_file_ref, default_timezone, fiscal_year_start)"
    )
    config_value: str = Field(description="Configuration value")
    config_type: ConfigType = Field(
        description="Data type of the configuration value (string, integer, boolean, json)"
    )
    description: str = Field(description="Description of the configuration entry")
    updated_by_ref: str = Field(description="Employee reference of the last editor")
    created_at: str = Field(description="Timestamp when the configuration was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the configuration was last updated (ISO 8601)")


class Notification(BaseModel):
    """Represents a notification sent to an employee via various channels"""

    notification_ref: str = Field(description="Unique identifier for the notification")
    recipient_employee_ref: str = Field(
        description="Employee reference of the notification recipient"
    )
    sender_type: SenderType = Field(
        description="Type of sender (system, employee)"
    )
    sender_employee_ref: Optional[str] = Field(
        description="Employee reference of the sender if sender_type is employee, null if system",
        default=None,
    )
    notification_type: NotificationType = Field(
        description="Type of notification (system, mention, approval, assignment, reminder, announcement)"
    )
    channel: NotificationChannel = Field(
        description="Delivery channel (in_app, email, sms, push)"
    )
    title: str = Field(description="Title of the notification")
    body: str = Field(description="Body content of the notification")
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource (e.g., employee, team, department, audit_log), null for general announcements",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference ID of the related resource, null for general announcements",
        default=None,
    )
    read_status: ReadStatus = Field(
        description="Read status of the notification (unread, read, dismissed)"
    )
    read_at: Optional[str] = Field(
        description="Timestamp when the notification was read, null if unread (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the notification was created (ISO 8601)")


class OfficeDB(DB):
    """Database containing office collaboration system data including users, employees, departments, teams, roles, permissions and more"""

    user_profile: Dict[str, UserProfile] = Field(
        description="Dictionary of all user profiles indexed by user_profile_ref"
    )
    employee: Dict[str, Employee] = Field(
        description="Dictionary of all employees indexed by employee_ref"
    )
    department: Dict[str, Department] = Field(
        description="Dictionary of all departments indexed by department_ref"
    )
    department_member: Dict[str, DepartmentMember] = Field(
        description="Dictionary of all department memberships indexed by department_member_ref"
    )
    position: Dict[str, Position] = Field(
        description="Dictionary of all positions indexed by position_ref"
    )
    team: Dict[str, Team] = Field(
        description="Dictionary of all teams indexed by team_ref"
    )
    team_member: Dict[str, TeamMember] = Field(
        description="Dictionary of all team memberships indexed by team_member_ref"
    )
    mentorship: Dict[str, Mentorship] = Field(
        description="Dictionary of all mentorships indexed by mentorship_ref"
    )
    role: Dict[str, Role] = Field(
        description="Dictionary of all roles indexed by role_ref"
    )
    permission: Dict[str, Permission] = Field(
        description="Dictionary of all permissions indexed by permission_ref"
    )
    role_permission: Dict[str, RolePermission] = Field(
        description="Dictionary of all role-permission bindings indexed by role_permission_ref"
    )
    employee_role: Dict[str, EmployeeRole] = Field(
        description="Dictionary of all employee-role assignments indexed by employee_role_ref"
    )
    audit_log: Dict[str, AuditLog] = Field(
        description="Dictionary of all audit log entries indexed by audit_log_ref"
    )
    file_attachment: Dict[str, FileAttachment] = Field(
        description="Dictionary of all file attachments indexed by file_attachment_ref"
    )
    org_config: Dict[str, OrgConfig] = Field(
        description="Dictionary of all organization configurations indexed by org_config_ref"
    )
    notification: Dict[str, Notification] = Field(
        description="Dictionary of all notifications indexed by notification_ref"
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
        num_users = len(self.user_profile)
        num_employees = len(self.employee)
        num_departments = len(self.department)
        num_teams = len(self.team)
        num_roles = len(self.role)
        num_permissions = len(self.permission)
        return {
            "num_users": num_users,
            "num_employees": num_employees,
            "num_departments": num_departments,
            "num_teams": num_teams,
            "num_roles": num_roles,
            "num_permissions": num_permissions,
        }