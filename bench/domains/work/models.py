from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from bench.environment.db import DB
from bench.domains.base.models import OfficeDB


# --- Enums as Literal types ---

ArrangementType = Literal["remote", "hybrid", "onsite", "flexible"]
ArrangementStatus = Literal["active", "inactive", "pending", "expired"]
WorkDay = Literal["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

ActivityType = Literal["team_building", "training", "workshop", "celebration", "offsite", "hackathon", "other"]
ActivityStatus = Literal["draft", "planned", "ongoing", "completed", "cancelled"]
ParticipantRole = Literal["organizer", "participant", "facilitator", "observer"]
RsvpStatus = Literal["pending", "accepted", "declined", "tentative"]

ProjectType = Literal["development", "research", "infrastructure", "maintenance", "consulting", "other"]
ProjectStatus = Literal["draft", "active", "on_hold", "completed", "cancelled", "archived"]
ProjectPriority = Literal["critical", "high", "medium", "low"]
ProjectRiskLevel = Literal["critical", "high", "medium", "low"]
ProjectRole = Literal["owner", "lead", "member", "observer"]
ProjectMemberStatus = Literal["active", "removed"]

MilestoneStatus = Literal["pending", "in_progress", "completed", "delayed", "cancelled"]

TaskType = Literal["development", "design", "testing", "documentation", "review", "bugfix", "research", "other"]
TaskStatus = Literal["todo", "in_progress", "in_review", "done", "blocked", "cancelled"]
TaskPriority = Literal["critical", "high", "medium", "low"]

RiskLevel = Literal["critical", "high", "medium", "low"]
RiskProbability = Literal["very_high", "high", "medium", "low", "very_low"]
RiskImpact = Literal["critical", "high", "medium", "low", "negligible"]
RiskStatus = Literal["open", "mitigating", "resolved", "accepted", "closed"]

EventType = Literal["meeting", "appointment", "reminder", "out_of_office", "focus_time", "other"]
EventStatus = Literal["tentative", "confirmed", "cancelled"]
EventVisibility = Literal["default", "public", "private", "confidential"]
AttendeeRole = Literal["required", "optional", "resource"]
AttendeeRsvpStatus = Literal["pending", "accepted", "declined", "tentative"]

TodoStatus = Literal["pending", "in_progress", "completed", "cancelled"]
TodoPriority = Literal["critical", "high", "medium", "low"]

ReminderChannel = Literal["in_app", "email", "sms", "push"]
ReminderStatus = Literal["pending", "triggered", "cancelled", "failed"]

MeetingType = Literal["video", "audio", "in_person", "hybrid"]
MeetingStatus = Literal["scheduled", "in_progress", "completed", "cancelled"]
MeetingPlatform = Literal["internal", "zoom", "teams", "dingtalk", "other"]
MeetingParticipantRole = Literal["host", "co_host", "attendee", "presenter"]
AttendanceStatus = Literal["invited", "joined", "absent", "excused"]

OkrScope = Literal["individual", "team", "department", "company"]
PeriodType = Literal["quarterly", "semi_annual", "annual", "monthly"]
ObjectiveStatus = Literal["draft", "active", "completed", "cancelled", "deferred"]
MetricType = Literal["percentage", "number", "currency", "boolean", "milestone"]
KeyResultStatus = Literal["active", "completed", "cancelled", "at_risk"]

ReportType = Literal["daily", "weekly", "monthly", "quarterly"]
ReportStatus = Literal["draft", "submitted", "reviewed", "returned"]

DocumentType = Literal["project", "team", "department", "personal", "company", "other"]
DocumentCategory = Literal[
    "technical_spec", "design_doc", "user_guide", "api_doc", "meeting_notes",
    "policy", "process", "template", "report", "other"
]
DocumentStatus = Literal["draft", "in_review", "published", "archived", "deprecated"]
AccessLevel = Literal["public", "internal", "restricted", "confidential"]
CollaboratorRole = Literal["owner", "editor", "commenter", "viewer"]
CollaboratorStatus = Literal["active", "revoked"]

RequirementType = Literal["feature", "enhancement", "bugfix", "technical_debt", "compliance", "other"]
RequirementStatus = Literal["draft", "under_review", "approved", "in_progress", "completed", "voided", "deferred"]
RequirementPriority = Literal["critical", "high", "medium", "low"]

SoftwareProductType = Literal["internal", "external", "platform", "library", "service"]
SoftwareProductStatus = Literal["active", "deprecated", "retired", "planning"]
SoftwarePlatform = Literal["web", "mobile", "desktop", "api", "cross_platform"]

CertificationType = Literal["professional", "technical", "compliance", "safety", "language", "other"]
CertificationStatus = Literal["active", "deprecated", "retired"]
JobFamily = Literal["Engineering", "Product", "Design", "HR", "Finance", "Legal", "Marketing", "Operations", "Data", "Research"]
EmployeeCertificationStatus = Literal["active", "expired", "revoked", "pending"]

ExamStatus = Literal["open", "closed", "completed", "cancelled"]
RegistrationStatus = Literal["registered", "cancelled", "completed", "no_show"]
ExamResult = Literal["pass", "fail", "pending"]

SnapshotType = Literal["daily", "weekly", "monthly"]

InfoType = Literal["string", "integer", "boolean", "json"]
InfoCategory = Literal["basic", "contact", "legal", "financial", "branding", "other"]


# --- Models ---


class WorkArrangement(BaseModel):
    """Represents a work arrangement for an employee defining their work schedule, location and type"""

    work_arrangement_ref: str = Field(description="Unique identifier for the work arrangement")
    employee_ref: str = Field(description="Reference to the employee this arrangement applies to")
    arrangement_type: ArrangementType = Field(
        description="Type of work arrangement (remote, hybrid, onsite, flexible)"
    )
    arrangement_status: ArrangementStatus = Field(
        description="Current status of the arrangement (active, inactive, pending, expired)"
    )
    start_date: str = Field(description="Start date of the arrangement (ISO 8601 date)")
    end_date: Optional[str] = Field(
        description="End date of the arrangement, null if ongoing (ISO 8601 date)",
        default=None,
    )
    recurrence_rule: Optional[str] = Field(
        description="Recurrence rule for the arrangement, null if not recurring",
        default=None,
    )
    work_days: List[WorkDay] = Field(
        description="List of work days in the arrangement (monday through sunday)"
    )
    work_start_time: str = Field(description="Daily work start time (HH:MM format)")
    work_end_time: str = Field(description="Daily work end time (HH:MM format)")
    timezone: str = Field(description="Timezone for the work schedule (e.g., Asia/Shanghai)")
    work_location: str = Field(description="Primary work location (e.g., home, office, coworking)")
    location_detail: str = Field(description="Detailed description of the work location")
    reason: str = Field(description="Reason for the work arrangement")
    approved_by_ref: Optional[str] = Field(
        description="Employee reference of the approver, null if not yet approved",
        default=None,
    )
    approved_at: Optional[str] = Field(
        description="Timestamp when the arrangement was approved, null if not yet approved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the arrangement was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the arrangement was last updated (ISO 8601)")


class TeamActivity(BaseModel):
    """Represents a team activity or event such as team building, training or workshop"""

    team_activity_ref: str = Field(description="Unique identifier for the team activity")
    activity_name: str = Field(description="Name of the activity")
    activity_type: ActivityType = Field(
        description="Type of activity (team_building, training, workshop, celebration, offsite, hackathon, other)"
    )
    description: str = Field(description="Description of the activity")
    organizer_employee_ref: str = Field(description="Employee reference of the activity organizer")
    department_ref: Optional[str] = Field(
        description="Reference to the associated department, null if not department-specific",
        default=None,
    )
    team_ref: Optional[str] = Field(
        description="Reference to the associated team, null if not team-specific",
        default=None,
    )
    venue_name: str = Field(description="Name of the venue where the activity takes place")
    venue_address: str = Field(description="Address of the venue")
    start_time: str = Field(description="Start time of the activity (ISO 8601)")
    end_time: str = Field(description="End time of the activity (ISO 8601)")
    headcount_limit: int = Field(description="Maximum number of participants allowed")
    budget_amount: float = Field(description="Budget amount allocated for the activity")
    budget_currency: str = Field(description="Currency of the budget amount (e.g., CNY, USD)")
    actual_cost: Optional[float] = Field(
        description="Actual cost of the activity, null if not yet determined",
        default=None,
    )
    activity_status: ActivityStatus = Field(
        description="Current status of the activity (draft, planned, ongoing, completed, cancelled)"
    )
    agenda: str = Field(description="Agenda or schedule of the activity")
    notes: str = Field(description="Additional notes about the activity")
    created_at: str = Field(description="Timestamp when the activity was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the activity was last updated (ISO 8601)")


class TeamActivityParticipant(BaseModel):
    """Represents the participation of an employee in a team activity"""

    team_activity_participant_ref: str = Field(description="Unique identifier for the activity participation")
    team_activity_ref: str = Field(description="Reference to the team activity")
    employee_ref: str = Field(description="Reference to the participating employee")
    participant_role: ParticipantRole = Field(
        description="Role of the participant (organizer, participant, facilitator, observer)"
    )
    rsvp_status: RsvpStatus = Field(
        description="RSVP status of the participant (pending, accepted, declined, tentative)"
    )
    check_in_at: Optional[str] = Field(
        description="Timestamp when the participant checked in, null if not checked in (ISO 8601)",
        default=None,
    )
    notes: str = Field(description="Additional notes from or about the participant")
    created_at: str = Field(description="Timestamp when the participation record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the participation record was last updated (ISO 8601)")


class Project(BaseModel):
    """Represents a project with planning, status, budget and hierarchy information"""

    project_ref: str = Field(description="Unique identifier for the project")
    project_name: str = Field(description="Name of the project")
    project_code: str = Field(description="Short code for the project")
    description: str = Field(description="Description of the project's purpose and scope")
    project_type: ProjectType = Field(
        description="Type of project (development, research, infrastructure, maintenance, consulting, other)"
    )
    project_status: ProjectStatus = Field(
        description="Current status of the project (draft, active, on_hold, completed, cancelled, archived)"
    )
    priority: ProjectPriority = Field(
        description="Priority level of the project (critical, high, medium, low)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the project owner")
    department_ref: Optional[str] = Field(
        description="Reference to the associated department, null if not department-specific",
        default=None,
    )
    team_ref: Optional[str] = Field(
        description="Reference to the associated team, null if not team-specific",
        default=None,
    )
    planned_start_date: str = Field(description="Planned start date of the project (ISO 8601 date)")
    planned_end_date: str = Field(description="Planned end date of the project (ISO 8601 date)")
    actual_start_date: Optional[str] = Field(
        description="Actual start date of the project, null if not yet started (ISO 8601 date)",
        default=None,
    )
    actual_end_date: Optional[str] = Field(
        description="Actual end date of the project, null if not yet completed (ISO 8601 date)",
        default=None,
    )
    progress_percent: int = Field(description="Overall progress of the project as a percentage (0-100)")
    budget_amount: Optional[float] = Field(
        description="Budget amount allocated for the project, null if not set",
        default=None,
    )
    budget_currency: str = Field(description="Currency of the budget amount (e.g., CNY, USD)")
    risk_level: ProjectRiskLevel = Field(
        description="Overall risk level of the project (critical, high, medium, low)"
    )
    parent_project_ref: Optional[str] = Field(
        description="Reference to the parent project, null if top-level project",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the project was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the project was last updated (ISO 8601)")


class ProjectMember(BaseModel):
    """Represents the membership relationship between an employee and a project"""

    project_member_ref: str = Field(description="Unique identifier for the project membership")
    project_ref: str = Field(description="Reference to the project")
    employee_ref: str = Field(description="Reference to the employee")
    project_role: ProjectRole = Field(
        description="Role within the project (owner, lead, member, observer)"
    )
    joined_at: str = Field(description="Timestamp when the employee joined the project (ISO 8601)")
    left_at: Optional[str] = Field(
        description="Timestamp when the employee left the project, null if still active (ISO 8601)",
        default=None,
    )
    status: ProjectMemberStatus = Field(
        description="Current membership status (active, removed)"
    )
    created_at: str = Field(description="Timestamp when the membership record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the membership record was last updated (ISO 8601)")


class ProjectMilestone(BaseModel):
    """Represents a milestone within a project with planned and actual dates"""

    project_milestone_ref: str = Field(description="Unique identifier for the project milestone")
    project_ref: str = Field(description="Reference to the project")
    milestone_name: str = Field(description="Name of the milestone")
    description: str = Field(description="Description of the milestone")
    planned_date: str = Field(description="Planned date for the milestone (ISO 8601 date)")
    actual_date: Optional[str] = Field(
        description="Actual date the milestone was reached, null if not yet reached (ISO 8601 date)",
        default=None,
    )
    milestone_status: MilestoneStatus = Field(
        description="Current status of the milestone (pending, in_progress, completed, delayed, cancelled)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the milestone owner")
    display_order: int = Field(description="Order for display/sorting purposes")
    created_at: str = Field(description="Timestamp when the milestone was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the milestone was last updated (ISO 8601)")


class ProjectTask(BaseModel):
    """Represents a task within a project with assignment, scheduling and progress tracking"""

    project_task_ref: str = Field(description="Unique identifier for the project task")
    project_ref: str = Field(description="Reference to the project")
    project_milestone_ref: Optional[str] = Field(
        description="Reference to the associated milestone, null if not linked to a milestone",
        default=None,
    )
    parent_task_ref: Optional[str] = Field(
        description="Reference to the parent task, null if top-level task",
        default=None,
    )
    task_title: str = Field(description="Title of the task")
    task_description: str = Field(description="Detailed description of the task")
    task_type: TaskType = Field(
        description="Type of task (development, design, testing, documentation, review, bugfix, research, other)"
    )
    task_status: TaskStatus = Field(
        description="Current status of the task (todo, in_progress, in_review, done, blocked, cancelled)"
    )
    priority: TaskPriority = Field(
        description="Priority level of the task (critical, high, medium, low)"
    )
    assignee_employee_ref: str = Field(description="Employee reference of the task assignee")
    reporter_employee_ref: str = Field(description="Employee reference of the task reporter")
    planned_start_date: str = Field(description="Planned start date of the task (ISO 8601 date)")
    planned_end_date: str = Field(description="Planned end date of the task (ISO 8601 date)")
    actual_start_date: Optional[str] = Field(
        description="Actual start date of the task, null if not yet started (ISO 8601 date)",
        default=None,
    )
    actual_end_date: Optional[str] = Field(
        description="Actual end date of the task, null if not yet completed (ISO 8601 date)",
        default=None,
    )
    estimated_hours: float = Field(description="Estimated hours to complete the task")
    actual_hours: Optional[float] = Field(
        description="Actual hours spent on the task, null if not tracked",
        default=None,
    )
    progress_percent: int = Field(description="Progress of the task as a percentage (0-100)")
    display_order: int = Field(description="Order for display/sorting purposes")
    created_at: str = Field(description="Timestamp when the task was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the task was last updated (ISO 8601)")


class ProjectRisk(BaseModel):
    """Represents a risk identified within a project with assessment and mitigation details"""

    project_risk_ref: str = Field(description="Unique identifier for the project risk")
    project_ref: str = Field(description="Reference to the project")
    risk_title: str = Field(description="Title of the risk")
    risk_description: str = Field(description="Detailed description of the risk")
    risk_level: RiskLevel = Field(
        description="Overall risk level (critical, high, medium, low)"
    )
    probability: RiskProbability = Field(
        description="Probability of the risk occurring (very_high, high, medium, low, very_low)"
    )
    impact: RiskImpact = Field(
        description="Impact if the risk occurs (critical, high, medium, low, negligible)"
    )
    mitigation_plan: str = Field(description="Plan to mitigate the risk")
    owner_employee_ref: str = Field(description="Employee reference of the risk owner")
    risk_status: RiskStatus = Field(
        description="Current status of the risk (open, mitigating, resolved, accepted, closed)"
    )
    identified_at: str = Field(description="Timestamp when the risk was identified (ISO 8601)")
    resolved_at: Optional[str] = Field(
        description="Timestamp when the risk was resolved, null if not yet resolved (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the risk record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the risk record was last updated (ISO 8601)")


class ScheduleEvent(BaseModel):
    """Represents a calendar event with scheduling, recurrence and visibility settings"""

    schedule_event_ref: str = Field(description="Unique identifier for the schedule event")
    organizer_employee_ref: str = Field(description="Employee reference of the event organizer")
    event_title: str = Field(description="Title of the event")
    event_description: str = Field(description="Description of the event")
    event_type: EventType = Field(
        description="Type of event (meeting, appointment, reminder, out_of_office, focus_time, other)"
    )
    event_status: EventStatus = Field(
        description="Current status of the event (tentative, confirmed, cancelled)"
    )
    start_time: str = Field(description="Start time of the event (ISO 8601)")
    end_time: str = Field(description="End time of the event (ISO 8601)")
    timezone: str = Field(description="Timezone for the event (e.g., Asia/Shanghai)")
    is_all_day: bool = Field(description="Whether the event spans the entire day")
    recurrence_rule: Optional[str] = Field(
        description="Recurrence rule for the event (e.g., RRULE format), null if not recurring",
        default=None,
    )
    location: str = Field(description="Location of the event")
    meeting_ref: Optional[str] = Field(
        description="Reference to the associated meeting, null if not a meeting event",
        default=None,
    )
    visibility: EventVisibility = Field(
        description="Visibility of the event (default, public, private, confidential)"
    )
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource, null if not linked to a resource",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference ID of the related resource, null if not linked to a resource",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the event was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the event was last updated (ISO 8601)")


class ScheduleEventAttendee(BaseModel):
    """Represents an attendee of a schedule event with their role and RSVP status"""

    schedule_event_attendee_ref: str = Field(description="Unique identifier for the event attendee")
    schedule_event_ref: str = Field(description="Reference to the schedule event")
    employee_ref: str = Field(description="Reference to the attending employee")
    attendee_role: AttendeeRole = Field(
        description="Role of the attendee (required, optional, resource)"
    )
    rsvp_status: AttendeeRsvpStatus = Field(
        description="RSVP status of the attendee (pending, accepted, declined, tentative)"
    )
    responded_at: Optional[str] = Field(
        description="Timestamp when the attendee responded, null if not yet responded (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the attendee record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the attendee record was last updated (ISO 8601)")


class TodoItem(BaseModel):
    """Represents a personal to-do item with priority, due date and optional resource linkage"""

    todo_item_ref: str = Field(description="Unique identifier for the to-do item")
    owner_employee_ref: str = Field(description="Employee reference of the to-do item owner")
    title: str = Field(description="Title of the to-do item")
    description: str = Field(description="Description of the to-do item")
    todo_status: TodoStatus = Field(
        description="Current status of the to-do item (pending, in_progress, completed, cancelled)"
    )
    priority: TodoPriority = Field(
        description="Priority level of the to-do item (critical, high, medium, low)"
    )
    due_date: str = Field(description="Due date and time for the to-do item (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the to-do item was completed, null if not completed (ISO 8601)",
        default=None,
    )
    related_resource_type: Optional[str] = Field(
        description="Type of the related resource, null if not linked to a resource",
        default=None,
    )
    related_resource_ref: Optional[str] = Field(
        description="Reference ID of the related resource, null if not linked to a resource",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the to-do item was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the to-do item was last updated (ISO 8601)")


class ReminderRule(BaseModel):
    """Represents a reminder rule linked to a resource with scheduling and delivery channel"""

    reminder_rule_ref: str = Field(description="Unique identifier for the reminder rule")
    employee_ref: str = Field(description="Reference to the employee who set the reminder")
    related_resource_type: str = Field(
        description="Type of the related resource (e.g., schedule_event, todo_item, project_task)"
    )
    related_resource_ref: str = Field(description="Reference ID of the related resource")
    remind_at: str = Field(description="Timestamp when the reminder should trigger (ISO 8601)")
    offset_minutes: int = Field(description="Number of minutes before the event to trigger the reminder")
    channel: ReminderChannel = Field(
        description="Delivery channel for the reminder (in_app, email, sms, push)"
    )
    reminder_status: ReminderStatus = Field(
        description="Current status of the reminder (pending, triggered, cancelled, failed)"
    )
    triggered_at: Optional[str] = Field(
        description="Timestamp when the reminder was triggered, null if not yet triggered (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the reminder rule was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the reminder rule was last updated (ISO 8601)")


class Meeting(BaseModel):
    """Represents a meeting with platform, recording and configuration details"""

    meeting_ref: str = Field(description="Unique identifier for the meeting")
    meeting_title: str = Field(description="Title of the meeting")
    meeting_type: MeetingType = Field(
        description="Type of meeting (video, audio, in_person, hybrid)"
    )
    meeting_status: MeetingStatus = Field(
        description="Current status of the meeting (scheduled, in_progress, completed, cancelled)"
    )
    organizer_employee_ref: str = Field(description="Employee reference of the meeting organizer")
    schedule_event_ref: Optional[str] = Field(
        description="Reference to the associated schedule event, null if not linked",
        default=None,
    )
    start_time: str = Field(description="Start time of the meeting (ISO 8601)")
    end_time: str = Field(description="End time of the meeting (ISO 8601)")
    timezone: str = Field(description="Timezone for the meeting (e.g., Asia/Shanghai)")
    meeting_platform: MeetingPlatform = Field(
        description="Platform used for the meeting (internal, zoom, teams, dingtalk, other)"
    )
    meeting_link: str = Field(description="URL link to join the meeting")
    meeting_password: str = Field(description="Password required to join the meeting")
    meeting_room: str = Field(description="Physical meeting room name or identifier")
    is_recorded: bool = Field(description="Whether the meeting is being recorded")
    recording_file_ref: Optional[str] = Field(
        description="Reference to the recording file attachment, null if not recorded",
        default=None,
    )
    allow_screen_share: bool = Field(description="Whether screen sharing is allowed in the meeting")
    notes: str = Field(description="Meeting notes or agenda")
    created_at: str = Field(description="Timestamp when the meeting was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the meeting was last updated (ISO 8601)")


class MeetingParticipant(BaseModel):
    """Represents a participant in a meeting with their role and attendance status"""

    meeting_participant_ref: str = Field(description="Unique identifier for the meeting participant")
    meeting_ref: str = Field(description="Reference to the meeting")
    employee_ref: str = Field(description="Reference to the participating employee")
    participant_role: MeetingParticipantRole = Field(
        description="Role of the participant (host, co_host, attendee, presenter)"
    )
    join_time: Optional[str] = Field(
        description="Timestamp when the participant joined the meeting, null if not yet joined (ISO 8601)",
        default=None,
    )
    leave_time: Optional[str] = Field(
        description="Timestamp when the participant left the meeting, null if not yet left (ISO 8601)",
        default=None,
    )
    attendance_status: AttendanceStatus = Field(
        description="Attendance status of the participant (invited, joined, absent, excused)"
    )
    created_at: str = Field(description="Timestamp when the participant record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the participant record was last updated (ISO 8601)")


class OkrObjective(BaseModel):
    """Represents an OKR objective with scope, period and progress tracking"""

    okr_objective_ref: str = Field(description="Unique identifier for the OKR objective")
    owner_employee_ref: str = Field(description="Employee reference of the objective owner")
    objective_title: str = Field(description="Title of the objective")
    description: str = Field(description="Description of the objective")
    okr_scope: OkrScope = Field(
        description="Scope of the objective (individual, team, department, company)"
    )
    scope_ref: Optional[str] = Field(
        description="Reference to the scoped entity (team_ref or department_ref), null when scope is individual or company",
        default=None,
    )
    period_type: PeriodType = Field(
        description="Type of period (quarterly, semi_annual, annual, monthly)"
    )
    period_label: str = Field(description="Label for the period (e.g., 2025-Q1, 2025-H1)")
    start_date: str = Field(description="Start date of the objective period (ISO 8601 date)")
    end_date: str = Field(description="End date of the objective period (ISO 8601 date)")
    parent_objective_ref: Optional[str] = Field(
        description="Reference to the parent objective, null if top-level objective",
        default=None,
    )
    progress_percent: int = Field(description="Overall progress of the objective as a percentage (0-100)")
    objective_status: ObjectiveStatus = Field(
        description="Current status of the objective (draft, active, completed, cancelled, deferred)"
    )
    score: Optional[float] = Field(
        description="Final score of the objective, null if not yet scored",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the objective was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the objective was last updated (ISO 8601)")


class OkrKeyResult(BaseModel):
    """Represents a key result under an OKR objective with metric tracking"""

    okr_key_result_ref: str = Field(description="Unique identifier for the OKR key result")
    okr_objective_ref: str = Field(description="Reference to the parent OKR objective")
    key_result_title: str = Field(description="Title of the key result")
    description: str = Field(description="Description of the key result")
    metric_type: MetricType = Field(
        description="Type of metric used to measure the key result (percentage, number, currency, boolean, milestone)"
    )
    target_value: float = Field(description="Target value to achieve for the key result")
    current_value: float = Field(description="Current value of the key result metric")
    start_value: float = Field(description="Starting value of the key result metric")
    unit: str = Field(description="Unit of measurement for the key result (e.g., %, count, USD)")
    progress_percent: int = Field(description="Progress of the key result as a percentage (0-100)")
    key_result_status: KeyResultStatus = Field(
        description="Current status of the key result (active, completed, cancelled, at_risk)"
    )
    owner_employee_ref: str = Field(description="Employee reference of the key result owner")
    score: Optional[float] = Field(
        description="Final score of the key result, null if not yet scored",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the key result was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the key result was last updated (ISO 8601)")


class WorkReport(BaseModel):
    """Represents a periodic work report submitted by an employee"""

    work_report_ref: str = Field(description="Unique identifier for the work report")
    author_employee_ref: str = Field(description="Employee reference of the report author")
    report_type: ReportType = Field(
        description="Type of report (daily, weekly, monthly, quarterly)"
    )
    report_title: str = Field(description="Title of the report")
    period_start_date: str = Field(description="Start date of the reporting period (ISO 8601 date)")
    period_end_date: str = Field(description="End date of the reporting period (ISO 8601 date)")
    summary: str = Field(description="Summary of the report")
    accomplishments: str = Field(description="Accomplishments during the reporting period")
    issues_and_risks: str = Field(description="Issues and risks encountered during the reporting period")
    next_period_plan: str = Field(description="Plan for the next reporting period")
    report_status: ReportStatus = Field(
        description="Current status of the report (draft, submitted, reviewed, returned)"
    )
    submitted_at: Optional[str] = Field(
        description="Timestamp when the report was submitted, null if not yet submitted (ISO 8601)",
        default=None,
    )
    related_okr_objective_ref: Optional[str] = Field(
        description="Reference to the related OKR objective, null if not linked",
        default=None,
    )
    related_project_ref: Optional[str] = Field(
        description="Reference to the related project, null if not linked",
        default=None,
    )
    recipients: List[str] = Field(
        description="List of employee references who are recipients of the report"
    )
    created_at: str = Field(description="Timestamp when the report was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the report was last updated (ISO 8601)")


class Document(BaseModel):
    """Represents a document with content, versioning, access control and categorization"""

    document_ref: str = Field(description="Unique identifier for the document")
    document_title: str = Field(description="Title of the document")
    document_type: DocumentType = Field(
        description="Type of document (project, team, department, personal, company, other)"
    )
    document_category: DocumentCategory = Field(
        description="Category of the document (technical_spec, design_doc, user_guide, api_doc, meeting_notes, policy, process, template, report, other)"
    )
    description: str = Field(description="Description of the document")
    content: str = Field(description="Content body of the document")
    document_status: DocumentStatus = Field(
        description="Current status of the document (draft, in_review, published, archived, deprecated)"
    )
    version: str = Field(description="Version string of the document (e.g., 1.0, 2.1)")
    owner_employee_ref: str = Field(description="Employee reference of the document owner")
    scope_type: str = Field(
        description="Scope type of the document (e.g., project, team, department, personal, company)"
    )
    scope_ref: Optional[str] = Field(
        description="Reference to the scoped entity, null if personal or company scope",
        default=None,
    )
    parent_document_ref: Optional[str] = Field(
        description="Reference to the parent document, null if top-level document",
        default=None,
    )
    file_attachment_ref: Optional[str] = Field(
        description="Reference to the associated file attachment, null if no attachment",
        default=None,
    )
    access_level: AccessLevel = Field(
        description="Access level of the document (public, internal, restricted, confidential)"
    )
    tags: List[str] = Field(description="List of tags associated with the document")
    view_count: int = Field(description="Number of times the document has been viewed")
    created_at: str = Field(description="Timestamp when the document was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the document was last updated (ISO 8601)")


class DocumentCollaborator(BaseModel):
    """Represents a collaborator on a document with their role and access permissions"""

    document_collaborator_ref: str = Field(description="Unique identifier for the document collaborator")
    document_ref: str = Field(description="Reference to the document")
    employee_ref: str = Field(description="Reference to the collaborating employee")
    collaborator_role: CollaboratorRole = Field(
        description="Role of the collaborator (owner, editor, commenter, viewer)"
    )
    granted_by_ref: str = Field(description="Employee reference of the person who granted access")
    granted_at: str = Field(description="Timestamp when access was granted (ISO 8601)")
    status: CollaboratorStatus = Field(
        description="Current status of the collaboration (active, revoked)"
    )
    created_at: str = Field(description="Timestamp when the collaborator record was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the collaborator record was last updated (ISO 8601)")


class ProductRequirement(BaseModel):
    """Represents a product requirement with type, priority, status and traceability"""

    product_requirement_ref: str = Field(description="Unique identifier for the product requirement")
    requirement_title: str = Field(description="Title of the requirement")
    requirement_code: str = Field(description="Human-readable requirement code (e.g., PRD-2025-0001)")
    description: str = Field(description="Detailed description of the requirement")
    requirement_type: RequirementType = Field(
        description="Type of requirement (feature, enhancement, bugfix, technical_debt, compliance, other)"
    )
    requirement_status: RequirementStatus = Field(
        description="Current status of the requirement (draft, under_review, approved, in_progress, completed, voided, deferred)"
    )
    priority: RequirementPriority = Field(
        description="Priority level of the requirement (critical, high, medium, low)"
    )
    business_value: str = Field(description="Description of the business value this requirement delivers")
    acceptance_criteria: str = Field(description="Acceptance criteria for the requirement")
    owner_employee_ref: str = Field(description="Employee reference of the requirement owner")
    project_ref: Optional[str] = Field(
        description="Reference to the associated project, null if not linked to a project",
        default=None,
    )
    software_product_ref: Optional[str] = Field(
        description="Reference to the associated software product, null if not linked",
        default=None,
    )
    parent_requirement_ref: Optional[str] = Field(
        description="Reference to the parent requirement, null if top-level requirement",
        default=None,
    )
    target_version: str = Field(description="Target version for the requirement delivery")
    planned_release_date: Optional[str] = Field(
        description="Planned release date for the requirement, null if not set (ISO 8601 date)",
        default=None,
    )
    impact_analysis: str = Field(description="Analysis of the impact of implementing this requirement")
    change_reason: Optional[str] = Field(
        description="Reason for changes to the requirement, null if no changes",
        default=None,
    )
    closed_at: Optional[str] = Field(
        description="Timestamp when the requirement was closed, null if not closed (ISO 8601)",
        default=None,
    )
    voided_at: Optional[str] = Field(
        description="Timestamp when the requirement was voided, null if not voided (ISO 8601)",
        default=None,
    )
    document_ref: Optional[str] = Field(
        description="Reference to the associated document, null if no document linked",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the requirement was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the requirement was last updated (ISO 8601)")


class SoftwareProduct(BaseModel):
    """Represents a software product with ownership, versioning and platform information"""

    software_product_ref: str = Field(description="Unique identifier for the software product")
    product_name: str = Field(description="Name of the software product")
    product_code: str = Field(description="Short code for the software product")
    description: str = Field(description="Description of the software product")
    product_type: SoftwareProductType = Field(
        description="Type of software product (internal, external, platform, library, service)"
    )
    product_status: SoftwareProductStatus = Field(
        description="Current status of the software product (active, deprecated, retired, planning)"
    )
    current_version: str = Field(description="Current version of the software product")
    access_url: str = Field(description="URL to access the software product")
    documentation_url: str = Field(description="URL to the product documentation")
    owner_employee_ref: str = Field(description="Employee reference of the product owner")
    owner_department_ref: Optional[str] = Field(
        description="Reference to the owning department, null if not department-owned",
        default=None,
    )
    support_contact: str = Field(description="Support contact information for the product")
    features_summary: str = Field(description="Summary of the product's key features")
    platform: SoftwarePlatform = Field(
        description="Platform the product runs on (web, mobile, desktop, api, cross_platform)"
    )
    created_at: str = Field(description="Timestamp when the product was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the product was last updated (ISO 8601)")


class Certification(BaseModel):
    """Represents a certification that employees can obtain"""

    certification_ref: str = Field(description="Unique identifier for the certification")
    certification_name: str = Field(description="Name of the certification")
    certification_code: str = Field(description="Short code for the certification")
    issuing_authority: str = Field(description="Authority or organization that issues the certification")
    description: str = Field(description="Description of the certification")
    certification_type: CertificationType = Field(
        description="Type of certification (professional, technical, compliance, safety, language, other)"
    )
    validity_period_months: int = Field(description="Validity period of the certification in months")
    exam_required: bool = Field(description="Whether an exam is required to obtain the certification")
    training_required: bool = Field(description="Whether training is required before the certification")
    certification_status: CertificationStatus = Field(
        description="Current status of the certification (active, deprecated, retired)"
    )
    related_job_family: JobFamily = Field(
        description="Job family related to this certification (Engineering, Product, Design, HR, Finance, Legal, Marketing, Operations, Data, Research)"
    )
    created_at: str = Field(description="Timestamp when the certification was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the certification was last updated (ISO 8601)")


class EmployeeCertification(BaseModel):
    """Represents an employee's obtained certification with validity and status"""

    employee_certification_ref: str = Field(description="Unique identifier for the employee certification")
    employee_ref: str = Field(description="Reference to the employee")
    certification_ref: str = Field(description="Reference to the certification")
    certificate_number: str = Field(description="Certificate number issued to the employee")
    obtained_date: str = Field(description="Date the certification was obtained (ISO 8601 date)")
    expiry_date: Optional[str] = Field(
        description="Expiry date of the certification, null if no expiry (ISO 8601 date)",
        default=None,
    )
    certification_status: EmployeeCertificationStatus = Field(
        description="Current status of the employee's certification (active, expired, revoked, pending)"
    )
    score: Optional[float] = Field(
        description="Score achieved in the certification exam, null if not applicable",
        default=None,
    )
    certificate_file_ref: Optional[str] = Field(
        description="Reference to the certificate file attachment, null if not uploaded",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the employee certification was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the employee certification was last updated (ISO 8601)")


class ExamSchedule(BaseModel):
    """Represents a scheduled exam for a certification"""

    exam_schedule_ref: str = Field(description="Unique identifier for the exam schedule")
    certification_ref: str = Field(description="Reference to the associated certification")
    exam_name: str = Field(description="Name of the exam")
    exam_date: str = Field(description="Date and time of the exam (ISO 8601)")
    registration_deadline: str = Field(description="Deadline for exam registration (ISO 8601)")
    location: str = Field(description="Location where the exam takes place")
    capacity: int = Field(description="Maximum number of examinees allowed")
    exam_status: ExamStatus = Field(
        description="Current status of the exam (open, closed, completed, cancelled)"
    )
    description: str = Field(description="Description of the exam")
    created_at: str = Field(description="Timestamp when the exam schedule was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the exam schedule was last updated (ISO 8601)")


class ExamRegistration(BaseModel):
    """Represents an employee's registration for a scheduled exam"""

    exam_registration_ref: str = Field(description="Unique identifier for the exam registration")
    exam_schedule_ref: str = Field(description="Reference to the exam schedule")
    employee_ref: str = Field(description="Reference to the registered employee")
    registration_status: RegistrationStatus = Field(
        description="Current registration status (registered, cancelled, completed, no_show)"
    )
    exam_result: Optional[ExamResult] = Field(
        description="Result of the exam (pass, fail, pending), null if not yet taken",
        default=None,
    )
    score: Optional[float] = Field(
        description="Score achieved in the exam, null if not yet taken",
        default=None,
    )
    registered_at: str = Field(description="Timestamp when the employee registered (ISO 8601)")
    completed_at: Optional[str] = Field(
        description="Timestamp when the exam was completed, null if not yet completed (ISO 8601)",
        default=None,
    )
    created_at: str = Field(description="Timestamp when the registration was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the registration was last updated (ISO 8601)")


class ManagerSnapshot(BaseModel):
    """Represents a periodic snapshot of a manager's team and project metrics"""

    manager_snapshot_ref: str = Field(description="Unique identifier for the manager snapshot")
    manager_employee_ref: str = Field(description="Employee reference of the manager")
    snapshot_date: str = Field(description="Date of the snapshot (ISO 8601 date)")
    snapshot_type: SnapshotType = Field(
        description="Type of snapshot (daily, weekly, monthly)"
    )
    department_ref: str = Field(description="Reference to the manager's department")
    team_headcount: int = Field(description="Total headcount of the manager's team")
    active_projects_count: int = Field(description="Number of active projects under the manager")
    overdue_tasks_count: int = Field(description="Number of overdue tasks under the manager")
    pending_approvals_count: int = Field(description="Number of pending approvals for the manager")
    open_risks_count: int = Field(description="Number of open risks in the manager's projects")
    avg_okr_progress_percent: int = Field(description="Average OKR progress percentage across the team")
    upcoming_milestones_count: int = Field(description="Number of upcoming milestones in the manager's projects")
    on_leave_count: int = Field(description="Number of team members currently on leave")
    remote_work_count: int = Field(description="Number of team members currently working remotely")
    snapshot_data: Dict[str, Any] = Field(
        description="Additional snapshot data including top risks, overdue items and key metrics"
    )
    created_at: str = Field(description="Timestamp when the snapshot was created (ISO 8601)")


class CompanyInfo(BaseModel):
    """Represents a company-level information entry as a key-value pair with categorization"""

    company_info_ref: str = Field(description="Unique identifier for the company info entry")
    info_key: str = Field(
        description="Information key (e.g., company_name, legal_entity, tax_id)"
    )
    info_value: str = Field(description="Information value")
    info_type: InfoType = Field(
        description="Data type of the information value (string, integer, boolean, json)"
    )
    info_category: InfoCategory = Field(
        description="Category of the information (basic, contact, legal, financial, branding, other)"
    )
    description: str = Field(description="Description of the information entry")
    is_public: bool = Field(description="Whether the information is publicly visible")
    updated_by_ref: str = Field(description="Employee reference of the last editor")
    created_at: str = Field(description="Timestamp when the info entry was created (ISO 8601)")
    updated_at: str = Field(description="Timestamp when the info entry was last updated (ISO 8601)")


class WorkDB(OfficeDB):
    """Database extending OfficeDB with work domain data including projects, tasks, meetings, OKRs, documents and more"""

    work_arrangement: Dict[str, WorkArrangement] = Field(
        description="Dictionary of all work arrangements indexed by work_arrangement_ref"
    )
    team_activity: Dict[str, TeamActivity] = Field(
        description="Dictionary of all team activities indexed by team_activity_ref"
    )
    team_activity_participant: Dict[str, TeamActivityParticipant] = Field(
        description="Dictionary of all team activity participants indexed by team_activity_participant_ref"
    )
    project: Dict[str, Project] = Field(
        description="Dictionary of all projects indexed by project_ref"
    )
    project_member: Dict[str, ProjectMember] = Field(
        description="Dictionary of all project memberships indexed by project_member_ref"
    )
    project_milestone: Dict[str, ProjectMilestone] = Field(
        description="Dictionary of all project milestones indexed by project_milestone_ref"
    )
    project_task: Dict[str, ProjectTask] = Field(
        description="Dictionary of all project tasks indexed by project_task_ref"
    )
    project_risk: Dict[str, ProjectRisk] = Field(
        description="Dictionary of all project risks indexed by project_risk_ref"
    )
    schedule_event: Dict[str, ScheduleEvent] = Field(
        description="Dictionary of all schedule events indexed by schedule_event_ref"
    )
    schedule_event_attendee: Dict[str, ScheduleEventAttendee] = Field(
        description="Dictionary of all schedule event attendees indexed by schedule_event_attendee_ref"
    )
    todo_item: Dict[str, TodoItem] = Field(
        description="Dictionary of all to-do items indexed by todo_item_ref"
    )
    reminder_rule: Dict[str, ReminderRule] = Field(
        description="Dictionary of all reminder rules indexed by reminder_rule_ref"
    )
    meeting: Dict[str, Meeting] = Field(
        description="Dictionary of all meetings indexed by meeting_ref"
    )
    meeting_participant: Dict[str, MeetingParticipant] = Field(
        description="Dictionary of all meeting participants indexed by meeting_participant_ref"
    )
    okr_objective: Dict[str, OkrObjective] = Field(
        description="Dictionary of all OKR objectives indexed by okr_objective_ref"
    )
    okr_key_result: Dict[str, OkrKeyResult] = Field(
        description="Dictionary of all OKR key results indexed by okr_key_result_ref"
    )
    work_report: Dict[str, WorkReport] = Field(
        description="Dictionary of all work reports indexed by work_report_ref"
    )
    document: Dict[str, Document] = Field(
        description="Dictionary of all documents indexed by document_ref"
    )
    document_collaborator: Dict[str, DocumentCollaborator] = Field(
        description="Dictionary of all document collaborators indexed by document_collaborator_ref"
    )
    product_requirement: Dict[str, ProductRequirement] = Field(
        description="Dictionary of all product requirements indexed by product_requirement_ref"
    )
    software_product: Dict[str, SoftwareProduct] = Field(
        description="Dictionary of all software products indexed by software_product_ref"
    )
    certification: Dict[str, Certification] = Field(
        description="Dictionary of all certifications indexed by certification_ref"
    )
    employee_certification: Dict[str, EmployeeCertification] = Field(
        description="Dictionary of all employee certifications indexed by employee_certification_ref"
    )
    exam_schedule: Dict[str, ExamSchedule] = Field(
        description="Dictionary of all exam schedules indexed by exam_schedule_ref"
    )
    exam_registration: Dict[str, ExamRegistration] = Field(
        description="Dictionary of all exam registrations indexed by exam_registration_ref"
    )
    manager_snapshot: Dict[str, ManagerSnapshot] = Field(
        description="Dictionary of all manager snapshots indexed by manager_snapshot_ref"
    )
    company_info: Dict[str, CompanyInfo] = Field(
        description="Dictionary of all company info entries indexed by company_info_ref"
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
        work_stats = {
            "num_work_arrangements": len(self.work_arrangement),
            "num_team_activities": len(self.team_activity),
            "num_team_activity_participants": len(self.team_activity_participant),
            "num_projects": len(self.project),
            "num_project_members": len(self.project_member),
            "num_project_milestones": len(self.project_milestone),
            "num_project_tasks": len(self.project_task),
            "num_project_risks": len(self.project_risk),
            "num_schedule_events": len(self.schedule_event),
            "num_schedule_event_attendees": len(self.schedule_event_attendee),
            "num_todo_items": len(self.todo_item),
            "num_reminder_rules": len(self.reminder_rule),
            "num_meetings": len(self.meeting),
            "num_meeting_participants": len(self.meeting_participant),
            "num_okr_objectives": len(self.okr_objective),
            "num_okr_key_results": len(self.okr_key_result),
            "num_work_reports": len(self.work_report),
            "num_documents": len(self.document),
            "num_document_collaborators": len(self.document_collaborator),
            "num_product_requirements": len(self.product_requirement),
            "num_software_products": len(self.software_product),
            "num_certifications": len(self.certification),
            "num_employee_certifications": len(self.employee_certification),
            "num_exam_schedules": len(self.exam_schedule),
            "num_exam_registrations": len(self.exam_registration),
            "num_manager_snapshots": len(self.manager_snapshot),
            "num_company_info": len(self.company_info),
        }
        return {**base_stats, **work_stats}