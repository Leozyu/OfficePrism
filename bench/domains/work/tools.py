"""Toolkit for the work collaboration domain, extending OfficeTools."""
from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolType, is_tool
from bench.domains.base.tools import OfficeTools
from bench.domains.work.models import (
    WorkDB,
    WorkArrangement,
    TeamActivity,
    TeamActivityParticipant,
    Project,
    ProjectMember,
    ProjectMilestone,
    ProjectTask,
    ProjectRisk,
    ScheduleEvent,
    ScheduleEventAttendee,
    TodoItem,
    ReminderRule,
    Meeting,
    MeetingParticipant,
    OkrObjective,
    OkrKeyResult,
    WorkReport,
    Document,
    DocumentCollaborator,
    ProductRequirement,
    SoftwareProduct,
    Certification,
    EmployeeCertification,
    ExamSchedule,
    ExamRegistration,
    ManagerSnapshot,
    CompanyInfo,
)


class WorkTools(OfficeTools):
    """Toolkit for the WORK domain, extending OfficeTools with work collaboration operations."""

    db: WorkDB

    def __init__(self, db: WorkDB) -> None:
        """
        Initialize the WorkTools with a WorkDB instance.

        Args:
            db: The WorkDB database instance.

        Returns:
            None
        """
        super().__init__(db)

    # -----------------------
    # Internal helper methods
    # -----------------------
    def _get_work_arrangement(self, work_arrangement_ref: str) -> WorkArrangement:
        """
        Retrieve a work arrangement by its reference.

        Args:
            work_arrangement_ref: Unique identifier for the work arrangement.

        Returns:
            WorkArrangement: The work arrangement object.

        Raises:
            ValueError: If the work arrangement is not found.
        """
        if work_arrangement_ref not in self.db.work_arrangement:
            raise ValueError("Work arrangement not found")
        return self.db.work_arrangement[work_arrangement_ref]

    def _get_team_activity(self, team_activity_ref: str) -> TeamActivity:
        """
        Retrieve a team activity by its reference.

        Args:
            team_activity_ref: Unique identifier for the team activity.

        Returns:
            TeamActivity: The team activity object.

        Raises:
            ValueError: If the team activity is not found.
        """
        if team_activity_ref not in self.db.team_activity:
            raise ValueError("Team activity not found")
        return self.db.team_activity[team_activity_ref]

    def _get_project(self, project_ref: str) -> Project:
        """
        Retrieve a project by its reference.

        Args:
            project_ref: Unique identifier for the project.

        Returns:
            Project: The project object.

        Raises:
            ValueError: If the project is not found.
        """
        if project_ref not in self.db.project:
            raise ValueError("Project not found")
        return self.db.project[project_ref]

    def _get_project_milestone(self, project_milestone_ref: str) -> ProjectMilestone:
        """
        Retrieve a project milestone by its reference.

        Args:
            project_milestone_ref: Unique identifier for the project milestone.

        Returns:
            ProjectMilestone: The project milestone object.

        Raises:
            ValueError: If the project milestone is not found.
        """
        if project_milestone_ref not in self.db.project_milestone:
            raise ValueError("Project milestone not found")
        return self.db.project_milestone[project_milestone_ref]

    def _get_project_task(self, project_task_ref: str) -> ProjectTask:
        """
        Retrieve a project task by its reference.

        Args:
            project_task_ref: Unique identifier for the project task.

        Returns:
            ProjectTask: The project task object.

        Raises:
            ValueError: If the project task is not found.
        """
        if project_task_ref not in self.db.project_task:
            raise ValueError("Project task not found")
        return self.db.project_task[project_task_ref]

    def _get_project_risk(self, project_risk_ref: str) -> ProjectRisk:
        """
        Retrieve a project risk by its reference.

        Args:
            project_risk_ref: Unique identifier for the project risk.

        Returns:
            ProjectRisk: The project risk object.

        Raises:
            ValueError: If the project risk is not found.
        """
        if project_risk_ref not in self.db.project_risk:
            raise ValueError("Project risk not found")
        return self.db.project_risk[project_risk_ref]

    def _get_schedule_event(self, schedule_event_ref: str) -> ScheduleEvent:
        """
        Retrieve a schedule event by its reference.

        Args:
            schedule_event_ref: Unique identifier for the schedule event.

        Returns:
            ScheduleEvent: The schedule event object.

        Raises:
            ValueError: If the schedule event is not found.
        """
        if schedule_event_ref not in self.db.schedule_event:
            raise ValueError("Schedule event not found")
        return self.db.schedule_event[schedule_event_ref]

    def _get_todo_item(self, todo_item_ref: str) -> TodoItem:
        """
        Retrieve a to-do item by its reference.

        Args:
            todo_item_ref: Unique identifier for the to-do item.

        Returns:
            TodoItem: The to-do item object.

        Raises:
            ValueError: If the to-do item is not found.
        """
        if todo_item_ref not in self.db.todo_item:
            raise ValueError("Todo item not found")
        return self.db.todo_item[todo_item_ref]

    def _get_reminder_rule(self, reminder_rule_ref: str) -> ReminderRule:
        """
        Retrieve a reminder rule by its reference.

        Args:
            reminder_rule_ref: Unique identifier for the reminder rule.

        Returns:
            ReminderRule: The reminder rule object.

        Raises:
            ValueError: If the reminder rule is not found.
        """
        if reminder_rule_ref not in self.db.reminder_rule:
            raise ValueError("Reminder rule not found")
        return self.db.reminder_rule[reminder_rule_ref]

    def _get_meeting(self, meeting_ref: str) -> Meeting:
        """
        Retrieve a meeting by its reference.

        Args:
            meeting_ref: Unique identifier for the meeting.

        Returns:
            Meeting: The meeting object.

        Raises:
            ValueError: If the meeting is not found.
        """
        if meeting_ref not in self.db.meeting:
            raise ValueError("Meeting not found")
        return self.db.meeting[meeting_ref]

    def _get_okr_objective(self, okr_objective_ref: str) -> OkrObjective:
        """
        Retrieve an OKR objective by its reference.

        Args:
            okr_objective_ref: Unique identifier for the OKR objective.

        Returns:
            OkrObjective: The OKR objective object.

        Raises:
            ValueError: If the OKR objective is not found.
        """
        if okr_objective_ref not in self.db.okr_objective:
            raise ValueError("OKR objective not found")
        return self.db.okr_objective[okr_objective_ref]

    def _get_okr_key_result(self, okr_key_result_ref: str) -> OkrKeyResult:
        """
        Retrieve an OKR key result by its reference.

        Args:
            okr_key_result_ref: Unique identifier for the OKR key result.

        Returns:
            OkrKeyResult: The OKR key result object.

        Raises:
            ValueError: If the OKR key result is not found.
        """
        if okr_key_result_ref not in self.db.okr_key_result:
            raise ValueError("OKR key result not found")
        return self.db.okr_key_result[okr_key_result_ref]

    def _get_work_report(self, work_report_ref: str) -> WorkReport:
        """
        Retrieve a work report by its reference.

        Args:
            work_report_ref: Unique identifier for the work report.

        Returns:
            WorkReport: The work report object.

        Raises:
            ValueError: If the work report is not found.
        """
        if work_report_ref not in self.db.work_report:
            raise ValueError("Work report not found")
        return self.db.work_report[work_report_ref]

    def _get_document(self, document_ref: str) -> Document:
        """
        Retrieve a document by its reference.

        Args:
            document_ref: Unique identifier for the document.

        Returns:
            Document: The document object.

        Raises:
            ValueError: If the document is not found.
        """
        if document_ref not in self.db.document:
            raise ValueError("Document not found")
        return self.db.document[document_ref]

    def _get_product_requirement(self, product_requirement_ref: str) -> ProductRequirement:
        """
        Retrieve a product requirement by its reference.

        Args:
            product_requirement_ref: Unique identifier for the product requirement.

        Returns:
            ProductRequirement: The product requirement object.

        Raises:
            ValueError: If the product requirement is not found.
        """
        if product_requirement_ref not in self.db.product_requirement:
            raise ValueError("Product requirement not found")
        return self.db.product_requirement[product_requirement_ref]

    def _get_software_product(self, software_product_ref: str) -> SoftwareProduct:
        """
        Retrieve a software product by its reference.

        Args:
            software_product_ref: Unique identifier for the software product.

        Returns:
            SoftwareProduct: The software product object.

        Raises:
            ValueError: If the software product is not found.
        """
        if software_product_ref not in self.db.software_product:
            raise ValueError("Software product not found")
        return self.db.software_product[software_product_ref]

    def _get_certification(self, certification_ref: str) -> Certification:
        """
        Retrieve a certification by its reference.

        Args:
            certification_ref: Unique identifier for the certification.

        Returns:
            Certification: The certification object.

        Raises:
            ValueError: If the certification is not found.
        """
        if certification_ref not in self.db.certification:
            raise ValueError("Certification not found")
        return self.db.certification[certification_ref]

    def _get_exam_schedule(self, exam_schedule_ref: str) -> ExamSchedule:
        """
        Retrieve an exam schedule by its reference.

        Args:
            exam_schedule_ref: Unique identifier for the exam schedule.

        Returns:
            ExamSchedule: The exam schedule object.

        Raises:
            ValueError: If the exam schedule is not found.
        """
        if exam_schedule_ref not in self.db.exam_schedule:
            raise ValueError("Exam schedule not found")
        return self.db.exam_schedule[exam_schedule_ref]

    def _get_manager_snapshot(self, manager_snapshot_ref: str) -> ManagerSnapshot:
        """
        Retrieve a manager snapshot by its reference.

        Args:
            manager_snapshot_ref: Unique identifier for the manager snapshot.

        Returns:
            ManagerSnapshot: The manager snapshot object.

        Raises:
            ValueError: If the manager snapshot is not found.
        """
        if manager_snapshot_ref not in self.db.manager_snapshot:
            raise ValueError("Manager snapshot not found")
        return self.db.manager_snapshot[manager_snapshot_ref]

    def _get_company_info(self, company_info_ref: str) -> CompanyInfo:
        """
        Retrieve a company info entry by its reference.

        Args:
            company_info_ref: Unique identifier for the company info entry.

        Returns:
            CompanyInfo: The company info object.

        Raises:
            ValueError: If the company info entry is not found.
        """
        if company_info_ref not in self.db.company_info:
            raise ValueError("Company info not found")
        return self.db.company_info[company_info_ref]

    # ========================================
    # Work Arrangement (居家办公 / 灵活办公)
    # ========================================

    @is_tool(ToolType.READ)
    def get_work_arrangement_details(self, work_arrangement_ref: str) -> WorkArrangement:
        """
        Retrieve the details of a specific work arrangement.

        Args:
            work_arrangement_ref: Unique identifier for the work arrangement.

        Returns:
            WorkArrangement: The work arrangement object with all details.

        Raises:
            ValueError: If the work arrangement is not found.
        """
        return self._get_work_arrangement(work_arrangement_ref)

    @is_tool(ToolType.READ)
    def list_work_arrangements_for_employee(
        self,
        employee_ref: str,
        arrangement_type: Optional[str] = None,
        arrangement_status: Optional[str] = None,
    ) -> str:
        """
        List all work arrangements for a given employee, optionally filtered by type and status.

        Args:
            employee_ref: Reference to the employee.
            arrangement_type: Optional filter by arrangement type (remote, hybrid, onsite, flexible).
            arrangement_status: Optional filter by arrangement status (active, inactive, pending, expired).

        Returns:
            str: JSON array of work arrangement summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for wa in self.db.work_arrangement.values():
            if wa.employee_ref != employee_ref:
                continue
            if arrangement_type is not None and wa.arrangement_type != arrangement_type:
                continue
            if arrangement_status is not None and wa.arrangement_status != arrangement_status:
                continue
            results.append({
                "work_arrangement_ref": wa.work_arrangement_ref,
                "arrangement_type": wa.arrangement_type,
                "arrangement_status": wa.arrangement_status,
                "start_date": wa.start_date,
                "end_date": wa.end_date,
                "work_days": wa.work_days,
                "work_start_time": wa.work_start_time,
                "work_end_time": wa.work_end_time,
                "timezone": wa.timezone,
                "work_location": wa.work_location,
                "location_detail": wa.location_detail,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_work_arrangements(
        self,
        arrangement_type: Optional[str] = None,
        arrangement_status: Optional[str] = None,
    ) -> str:
        """
        List all work arrangements, optionally filtered by type and status.

        Args:
            arrangement_type: Optional filter by arrangement type (remote, hybrid, onsite, flexible).
            arrangement_status: Optional filter by arrangement status (active, inactive, pending, expired).

        Returns:
            str: JSON array of work arrangement summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for wa in self.db.work_arrangement.values():
            if arrangement_type is not None and wa.arrangement_type != arrangement_type:
                continue
            if arrangement_status is not None and wa.arrangement_status != arrangement_status:
                continue
            results.append({
                "work_arrangement_ref": wa.work_arrangement_ref,
                "employee_ref": wa.employee_ref,
                "arrangement_type": wa.arrangement_type,
                "arrangement_status": wa.arrangement_status,
                "start_date": wa.start_date,
                "end_date": wa.end_date,
                "work_location": wa.work_location,
                "work_days": wa.work_days,
                "work_start_time": wa.work_start_time,
                "work_end_time": wa.work_end_time,
                "timezone": wa.timezone,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_work_arrangement(
        self,
        employee_ref: str,
        arrangement_type: str,
        start_date: str,
        end_date: Optional[str],
        work_days: List[str],
        work_start_time: str,
        work_end_time: str,
        timezone: str,
        work_location: str,
        location_detail: str,
        reason: str,
        approved_by_ref: Optional[str] = None,
    ) -> WorkArrangement:
        """
        Create a new work arrangement for an employee. The agent must ask for explicit user confirmation before calling.

        Args:
            employee_ref: Reference to the employee.
            arrangement_type: Type of arrangement (remote, hybrid, onsite, flexible).
            start_date: Start date (ISO 8601 date).
            end_date: End date (ISO 8601 date), or None if ongoing.
            work_days: List of work days (monday through sunday).
            work_start_time: Daily work start time (HH:MM).
            work_end_time: Daily work end time (HH:MM).
            timezone: Timezone for the schedule (e.g., Asia/Shanghai).
            work_location: Primary work location.
            location_detail: Detailed description of the work location.
            reason: Reason for the arrangement.
            approved_by_ref: Employee reference of the approver, or None.

        Returns:
            WorkArrangement: The newly created work arrangement.

        Raises:
            ValueError: If the employee is not found or inputs are invalid.
        """
        self._get_employee(employee_ref)

        valid_types = {"remote", "hybrid", "onsite", "flexible"}
        if arrangement_type not in valid_types:
            raise ValueError(f"Invalid arrangement_type: {arrangement_type}. Must be one of {valid_types}")

        valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        for d in work_days:
            if d not in valid_days:
                raise ValueError(f"Invalid work day: {d}. Must be one of {valid_days}")

        if approved_by_ref is not None:
            self._get_employee(approved_by_ref)

        now = self._now_iso()
        ref = self._generate_ref("WA", self.db.work_arrangement)

        wa = WorkArrangement(
            work_arrangement_ref=ref,
            employee_ref=employee_ref,
            arrangement_type=arrangement_type,
            arrangement_status="pending" if approved_by_ref is None else "active",
            start_date=start_date,
            end_date=end_date,
            recurrence_rule=None,
            work_days=work_days,
            work_start_time=work_start_time,
            work_end_time=work_end_time,
            timezone=timezone,
            work_location=work_location,
            location_detail=location_detail,
            reason=reason,
            approved_by_ref=approved_by_ref,
            approved_at=now if approved_by_ref is not None else None,
            created_at=now,
            updated_at=now,
        )
        self.db.work_arrangement[ref] = wa
        return wa

    @is_tool(ToolType.WRITE)
    def update_work_arrangement(
        self,
        work_arrangement_ref: str,
        arrangement_type: Optional[str] = None,
        arrangement_status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        work_days: Optional[List[str]] = None,
        work_start_time: Optional[str] = None,
        work_end_time: Optional[str] = None,
        timezone: Optional[str] = None,
        work_location: Optional[str] = None,
        location_detail: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> WorkArrangement:
        """
        Update an existing work arrangement. The agent must ask for explicit user confirmation before calling.

        Args:
            work_arrangement_ref: Reference to the work arrangement to update.
            arrangement_type: New arrangement type, or None to keep unchanged.
            arrangement_status: New arrangement status, or None to keep unchanged.
            start_date: New start date, or None to keep unchanged.
            end_date: New end date, or None to keep unchanged.
            work_days: New list of work days, or None to keep unchanged.
            work_start_time: New work start time, or None to keep unchanged.
            work_end_time: New work end time, or None to keep unchanged.
            timezone: New timezone, or None to keep unchanged.
            work_location: New work location, or None to keep unchanged.
            location_detail: New location detail, or None to keep unchanged.
            reason: New reason, or None to keep unchanged.

        Returns:
            WorkArrangement: The updated work arrangement.

        Raises:
            ValueError: If the work arrangement is not found or inputs are invalid.
        """
        wa = self._get_work_arrangement(work_arrangement_ref)

        if arrangement_type is not None:
            valid_types = {"remote", "hybrid", "onsite", "flexible"}
            if arrangement_type not in valid_types:
                raise ValueError(f"Invalid arrangement_type: {arrangement_type}. Must be one of {valid_types}")
            wa.arrangement_type = arrangement_type

        if arrangement_status is not None:
            valid_statuses = {"active", "inactive", "pending", "expired"}
            if arrangement_status not in valid_statuses:
                raise ValueError(f"Invalid arrangement_status: {arrangement_status}. Must be one of {valid_statuses}")
            wa.arrangement_status = arrangement_status

        if start_date is not None:
            wa.start_date = start_date
        if end_date is not None:
            wa.end_date = end_date
        if work_days is not None:
            valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
            for d in work_days:
                if d not in valid_days:
                    raise ValueError(f"Invalid work day: {d}")
            wa.work_days = work_days
        if work_start_time is not None:
            wa.work_start_time = work_start_time
        if work_end_time is not None:
            wa.work_end_time = work_end_time
        if timezone is not None:
            wa.timezone = timezone
        if work_location is not None:
            wa.work_location = work_location
        if location_detail is not None:
            wa.location_detail = location_detail
        if reason is not None:
            wa.reason = reason

        wa.updated_at = self._now_iso()
        return wa

    @is_tool(ToolType.WRITE)
    def approve_work_arrangement(
        self,
        work_arrangement_ref: str,
        approved_by_ref: str,
    ) -> WorkArrangement:
        """
        Approve a pending work arrangement. The agent must ask for explicit user confirmation before calling.

        Args:
            work_arrangement_ref: Reference to the work arrangement.
            approved_by_ref: Employee reference of the approver.

        Returns:
            WorkArrangement: The approved work arrangement.

        Raises:
            ValueError: If the work arrangement is not found, not in pending status, or approver not found.
        """
        wa = self._get_work_arrangement(work_arrangement_ref)
        self._get_employee(approved_by_ref)

        if wa.arrangement_status != "pending":
            raise ValueError(f"Work arrangement is not pending, current status: {wa.arrangement_status}")

        now = self._now_iso()
        wa.arrangement_status = "active"
        wa.approved_by_ref = approved_by_ref
        wa.approved_at = now
        wa.updated_at = now
        return wa

    # ========================================
    # Team Activity (团建外出活动)
    # ========================================

    @is_tool(ToolType.READ)
    def get_team_activity_details(self, team_activity_ref: str) -> TeamActivity:
        """
        Retrieve the details of a specific team activity.

        Args:
            team_activity_ref: Unique identifier for the team activity.

        Returns:
            TeamActivity: The team activity object with all details.

        Raises:
            ValueError: If the team activity is not found.
        """
        return self._get_team_activity(team_activity_ref)

    @is_tool(ToolType.READ)
    def list_team_activities(
        self,
        activity_type: Optional[str] = None,
        activity_status: Optional[str] = None,
        department_ref: Optional[str] = None,
        team_ref: Optional[str] = None,
    ) -> str:
        """
        List team activities, optionally filtered by type, status, department, or team.

        Args:
            activity_type: Optional filter by activity type.
            activity_status: Optional filter by activity status.
            department_ref: Optional filter by department reference.
            team_ref: Optional filter by team reference.

        Returns:
            str: JSON array of team activity summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for ta in self.db.team_activity.values():
            if activity_type is not None and ta.activity_type != activity_type:
                continue
            if activity_status is not None and ta.activity_status != activity_status:
                continue
            if department_ref is not None and ta.department_ref != department_ref:
                continue
            if team_ref is not None and ta.team_ref != team_ref:
                continue
            results.append({
                "team_activity_ref": ta.team_activity_ref,
                "activity_name": ta.activity_name,
                "activity_type": ta.activity_type,
                "activity_status": ta.activity_status,
                "organizer_employee_ref": ta.organizer_employee_ref,
                "department_ref": ta.department_ref,
                "team_ref": ta.team_ref,
                "venue_name": ta.venue_name,
                "start_time": ta.start_time,
                "end_time": ta.end_time,
                "headcount_limit": ta.headcount_limit,
                "budget_amount": ta.budget_amount,
                "budget_currency": ta.budget_currency,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_team_activity_participants(
        self,
        team_activity_ref: str,
        rsvp_status: Optional[str] = None,
    ) -> str:
        """
        List all participants of a specific team activity.

        Args:
            team_activity_ref: Reference to the team activity.
            rsvp_status: Optional filter by RSVP status (pending, accepted, declined, tentative).

        Returns:
            str: JSON array of participant summary objects.

        Raises:
            ValueError: If the team activity is not found.
        """
        self._get_team_activity(team_activity_ref)

        results = []
        for tap in self.db.team_activity_participant.values():
            if tap.team_activity_ref != team_activity_ref:
                continue
            if rsvp_status is not None and tap.rsvp_status != rsvp_status:
                continue
            emp = self._get_employee(tap.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "team_activity_participant_ref": tap.team_activity_participant_ref,
                "employee_ref": tap.employee_ref,
                "display_name": up.display_name,
                "participant_role": tap.participant_role,
                "rsvp_status": tap.rsvp_status,
                "check_in_at": tap.check_in_at,
                "notes": tap.notes,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_team_activities_for_employee(
        self,
        employee_ref: str,
        rsvp_status: Optional[str] = None,
    ) -> str:
        """
        List all team activities that an employee is participating in.

        Args:
            employee_ref: Reference to the employee.
            rsvp_status: Optional filter by RSVP status.

        Returns:
            str: JSON array of team activity participation objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for tap in self.db.team_activity_participant.values():
            if tap.employee_ref != employee_ref:
                continue
            if rsvp_status is not None and tap.rsvp_status != rsvp_status:
                continue
            ta = self._get_team_activity(tap.team_activity_ref)
            results.append({
                "team_activity_ref": ta.team_activity_ref,
                "activity_name": ta.activity_name,
                "activity_type": ta.activity_type,
                "activity_status": ta.activity_status,
                "start_time": ta.start_time,
                "end_time": ta.end_time,
                "participant_role": tap.participant_role,
                "rsvp_status": tap.rsvp_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_team_activity(
        self,
        activity_name: str,
        activity_type: str,
        description: str,
        organizer_employee_ref: str,
        venue_name: str,
        venue_address: str,
        start_time: str,
        end_time: str,
        headcount_limit: int,
        budget_amount: float,
        budget_currency: str,
        agenda: str,
        department_ref: Optional[str] = None,
        team_ref: Optional[str] = None,
        notes: str = "",
    ) -> TeamActivity:
        """
        Create a new team activity. The agent must ask for explicit user confirmation before calling.

        Args:
            activity_name: Name of the activity.
            activity_type: Type of activity (team_building, training, workshop, celebration, offsite, hackathon, other).
            description: Description of the activity.
            organizer_employee_ref: Employee reference of the organizer.
            venue_name: Name of the venue.
            venue_address: Address of the venue.
            start_time: Start time (ISO 8601).
            end_time: End time (ISO 8601).
            headcount_limit: Maximum number of participants.
            budget_amount: Budget amount.
            budget_currency: Currency of the budget (e.g., CNY, USD).
            agenda: Agenda or schedule.
            department_ref: Optional department reference.
            team_ref: Optional team reference.
            notes: Additional notes.

        Returns:
            TeamActivity: The newly created team activity.

        Raises:
            ValueError: If organizer not found or inputs are invalid.
        """
        self._get_employee(organizer_employee_ref)

        valid_types = {"team_building", "training", "workshop", "celebration", "offsite", "hackathon", "other"}
        if activity_type not in valid_types:
            raise ValueError(f"Invalid activity_type: {activity_type}. Must be one of {valid_types}")

        if department_ref is not None:
            self._get_department(department_ref)
        if team_ref is not None:
            self._get_team(team_ref)

        now = self._now_iso()
        ref = self._generate_ref("TA", self.db.team_activity)

        ta = TeamActivity(
            team_activity_ref=ref,
            activity_name=activity_name,
            activity_type=activity_type,
            description=description,
            organizer_employee_ref=organizer_employee_ref,
            department_ref=department_ref,
            team_ref=team_ref,
            venue_name=venue_name,
            venue_address=venue_address,
            start_time=start_time,
            end_time=end_time,
            headcount_limit=headcount_limit,
            budget_amount=budget_amount,
            budget_currency=budget_currency,
            actual_cost=None,
            activity_status="planned",
            agenda=agenda,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.team_activity[ref] = ta
        return ta

    @is_tool(ToolType.WRITE)
    def update_team_activity(
        self,
        team_activity_ref: str,
        activity_name: Optional[str] = None,
        activity_type: Optional[str] = None,
        description: Optional[str] = None,
        venue_name: Optional[str] = None,
        venue_address: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        headcount_limit: Optional[int] = None,
        budget_amount: Optional[float] = None,
        actual_cost: Optional[float] = None,
        activity_status: Optional[str] = None,
        agenda: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> TeamActivity:
        """
        Update an existing team activity. The agent must ask for explicit user confirmation before calling.

        Args:
            team_activity_ref: Reference to the team activity to update.
            activity_name: New name, or None to keep unchanged.
            activity_type: New type, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            venue_name: New venue name, or None to keep unchanged.
            venue_address: New venue address, or None to keep unchanged.
            start_time: New start time, or None to keep unchanged.
            end_time: New end time, or None to keep unchanged.
            headcount_limit: New headcount limit, or None to keep unchanged.
            budget_amount: New budget amount, or None to keep unchanged.
            actual_cost: New actual cost, or None to keep unchanged.
            activity_status: New status, or None to keep unchanged.
            agenda: New agenda, or None to keep unchanged.
            notes: New notes, or None to keep unchanged.

        Returns:
            TeamActivity: The updated team activity.

        Raises:
            ValueError: If the team activity is not found or inputs are invalid.
        """
        ta = self._get_team_activity(team_activity_ref)

        if activity_name is not None:
            ta.activity_name = activity_name
        if activity_type is not None:
            valid_types = {"team_building", "training", "workshop", "celebration", "offsite", "hackathon", "other"}
            if activity_type not in valid_types:
                raise ValueError(f"Invalid activity_type: {activity_type}. Must be one of {valid_types}")
            ta.activity_type = activity_type
        if description is not None:
            ta.description = description
        if venue_name is not None:
            ta.venue_name = venue_name
        if venue_address is not None:
            ta.venue_address = venue_address
        if start_time is not None:
            ta.start_time = start_time
        if end_time is not None:
            ta.end_time = end_time
        if headcount_limit is not None:
            ta.headcount_limit = headcount_limit
        if budget_amount is not None:
            ta.budget_amount = budget_amount
        if actual_cost is not None:
            ta.actual_cost = actual_cost
        if activity_status is not None:
            valid_statuses = {"draft", "planned", "ongoing", "completed", "cancelled"}
            if activity_status not in valid_statuses:
                raise ValueError(f"Invalid activity_status: {activity_status}. Must be one of {valid_statuses}")
            ta.activity_status = activity_status
        if agenda is not None:
            ta.agenda = agenda
        if notes is not None:
            ta.notes = notes

        ta.updated_at = self._now_iso()
        return ta

    @is_tool(ToolType.WRITE)
    def add_team_activity_participant(
        self,
        team_activity_ref: str,
        employee_ref: str,
        participant_role: str,
        notes: str = "",
    ) -> TeamActivityParticipant:
        """
        Add a participant to a team activity. The agent must ask for explicit user confirmation before calling.

        Args:
            team_activity_ref: Reference to the team activity.
            employee_ref: Reference to the employee to add.
            participant_role: Role of the participant (organizer, participant, facilitator, observer).
            notes: Additional notes.

        Returns:
            TeamActivityParticipant: The newly created participation record.

        Raises:
            ValueError: If the team activity or employee is not found, or inputs are invalid.
        """
        ta = self._get_team_activity(team_activity_ref)
        self._get_employee(employee_ref)

        valid_roles = {"organizer", "participant", "facilitator", "observer"}
        if participant_role not in valid_roles:
            raise ValueError(f"Invalid participant_role: {participant_role}. Must be one of {valid_roles}")

        # Check if already a participant
        for tap in self.db.team_activity_participant.values():
            if tap.team_activity_ref == team_activity_ref and tap.employee_ref == employee_ref:
                raise ValueError("Employee is already a participant in this activity")

        now = self._now_iso()
        ref = self._generate_ref("TAP", self.db.team_activity_participant)

        tap = TeamActivityParticipant(
            team_activity_participant_ref=ref,
            team_activity_ref=team_activity_ref,
            employee_ref=employee_ref,
            participant_role=participant_role,
            rsvp_status="pending",
            check_in_at=None,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.team_activity_participant[ref] = tap
        return tap

    @is_tool(ToolType.WRITE)
    def update_team_activity_participant_rsvp(
        self,
        team_activity_participant_ref: str,
        rsvp_status: str,
    ) -> TeamActivityParticipant:
        """
        Update the RSVP status of a team activity participant. The agent must ask for explicit user confirmation before calling.

        Args:
            team_activity_participant_ref: Reference to the participant record.
            rsvp_status: New RSVP status (pending, accepted, declined, tentative).

        Returns:
            TeamActivityParticipant: The updated participation record.

        Raises:
            ValueError: If the participant record is not found or status is invalid.
        """
        if team_activity_participant_ref not in self.db.team_activity_participant:
            raise ValueError("Team activity participant not found")

        valid_statuses = {"pending", "accepted", "declined", "tentative"}
        if rsvp_status not in valid_statuses:
            raise ValueError(f"Invalid rsvp_status: {rsvp_status}. Must be one of {valid_statuses}")

        tap = self.db.team_activity_participant[team_activity_participant_ref]
        tap.rsvp_status = rsvp_status
        tap.updated_at = self._now_iso()
        return tap

    # ========================================
    # Project (项目计划生成 / 项目进度跟踪)
    # ========================================

    @is_tool(ToolType.READ)
    def get_project_details(self, project_ref: str) -> Project:
        """
        Retrieve the details of a specific project.

        Args:
            project_ref: Unique identifier for the project.

        Returns:
            Project: The project object with all details.

        Raises:
            ValueError: If the project is not found.
        """
        return self._get_project(project_ref)

    @is_tool(ToolType.READ)
    def list_projects(
        self,
        project_type: Optional[str] = None,
        project_status: Optional[str] = None,
        priority: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
        department_ref: Optional[str] = None,
        team_ref: Optional[str] = None,
    ) -> str:
        """
        List projects with optional filters.

        Args:
            project_type: Optional filter by project type.
            project_status: Optional filter by project status.
            priority: Optional filter by priority.
            owner_employee_ref: Optional filter by owner employee reference.
            department_ref: Optional filter by department reference.
            team_ref: Optional filter by team reference.

        Returns:
            str: JSON array of project summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for p in self.db.project.values():
            if project_type is not None and p.project_type != project_type:
                continue
            if project_status is not None and p.project_status != project_status:
                continue
            if priority is not None and p.priority != priority:
                continue
            if owner_employee_ref is not None and p.owner_employee_ref != owner_employee_ref:
                continue
            if department_ref is not None and p.department_ref != department_ref:
                continue
            if team_ref is not None and p.team_ref != team_ref:
                continue
            results.append({
                "project_ref": p.project_ref,
                "project_name": p.project_name,
                "project_code": p.project_code,
                "project_type": p.project_type,
                "project_status": p.project_status,
                "priority": p.priority,
                "owner_employee_ref": p.owner_employee_ref,
                "progress_percent": p.progress_percent,
                "planned_start_date": p.planned_start_date,
                "planned_end_date": p.planned_end_date,
                "risk_level": p.risk_level,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_project_ref_by_name(self, project_name: str) -> str:
        """
        Find a project reference by its name (partial match, case-insensitive).

        Args:
            project_name: The project name to search for.

        Returns:
            str: The project reference.

        Raises:
            ValueError: If no matching project is found.
        """
        search = project_name.lower()
        for p_ref, p in self.db.project.items():
            if search in p.project_name.lower():
                return p_ref
        raise ValueError("Project not found")

    @is_tool(ToolType.WRITE)
    def create_project(
        self,
        project_name: str,
        project_code: str,
        description: str,
        project_type: str,
        priority: str,
        owner_employee_ref: str,
        planned_start_date: str,
        planned_end_date: str,
        budget_amount: Optional[float] = None,
        budget_currency: str = "CNY",
        department_ref: Optional[str] = None,
        team_ref: Optional[str] = None,
        parent_project_ref: Optional[str] = None,
    ) -> Project:
        """
        Create a new project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_name: Name of the project.
            project_code: Short code for the project.
            description: Description of the project.
            project_type: Type (development, research, infrastructure, maintenance, consulting, other).
            priority: Priority (critical, high, medium, low).
            owner_employee_ref: Employee reference of the project owner.
            planned_start_date: Planned start date (ISO 8601 date).
            planned_end_date: Planned end date (ISO 8601 date).
            budget_amount: Budget amount, or None.
            budget_currency: Currency of the budget.
            department_ref: Optional department reference.
            team_ref: Optional team reference.
            parent_project_ref: Optional parent project reference.

        Returns:
            Project: The newly created project.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(owner_employee_ref)

        valid_types = {"development", "research", "infrastructure", "maintenance", "consulting", "other"}
        if project_type not in valid_types:
            raise ValueError(f"Invalid project_type: {project_type}. Must be one of {valid_types}")

        valid_priorities = {"critical", "high", "medium", "low"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        if department_ref is not None:
            self._get_department(department_ref)
        if team_ref is not None:
            self._get_team(team_ref)
        if parent_project_ref is not None:
            self._get_project(parent_project_ref)

        now = self._now_iso()
        ref = self._generate_ref("PRJ", self.db.project)

        project = Project(
            project_ref=ref,
            project_name=project_name,
            project_code=project_code,
            description=description,
            project_type=project_type,
            project_status="draft",
            priority=priority,
            owner_employee_ref=owner_employee_ref,
            department_ref=department_ref,
            team_ref=team_ref,
            planned_start_date=planned_start_date,
            planned_end_date=planned_end_date,
            actual_start_date=None,
            actual_end_date=None,
            progress_percent=0,
            budget_amount=budget_amount,
            budget_currency=budget_currency,
            risk_level="low",
            parent_project_ref=parent_project_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.project[ref] = project
        return project

    @is_tool(ToolType.WRITE)
    def update_project(
        self,
        project_ref: str,
        project_name: Optional[str] = None,
        description: Optional[str] = None,
        project_status: Optional[str] = None,
        priority: Optional[str] = None,
        progress_percent: Optional[int] = None,
        actual_start_date: Optional[str] = None,
        actual_end_date: Optional[str] = None,
        budget_amount: Optional[float] = None,
        risk_level: Optional[str] = None,
    ) -> Project:
        """
        Update an existing project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_ref: Reference to the project to update.
            project_name: New name, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            project_status: New status, or None to keep unchanged.
            priority: New priority, or None to keep unchanged.
            progress_percent: New progress percentage, or None to keep unchanged.
            actual_start_date: New actual start date, or None to keep unchanged.
            actual_end_date: New actual end date, or None to keep unchanged.
            budget_amount: New budget amount, or None to keep unchanged.
            risk_level: New risk level, or None to keep unchanged.

        Returns:
            Project: The updated project.

        Raises:
            ValueError: If the project is not found or inputs are invalid.
        """
        project = self._get_project(project_ref)

        if project_name is not None:
            project.project_name = project_name
        if description is not None:
            project.description = description
        if project_status is not None:
            valid_statuses = {"draft", "active", "on_hold", "completed", "cancelled", "archived"}
            if project_status not in valid_statuses:
                raise ValueError(f"Invalid project_status: {project_status}. Must be one of {valid_statuses}")
            project.project_status = project_status
        if priority is not None:
            valid_priorities = {"critical", "high", "medium", "low"}
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
            project.priority = priority
        if progress_percent is not None:
            if progress_percent < 0 or progress_percent > 100:
                raise ValueError("progress_percent must be between 0 and 100")
            project.progress_percent = progress_percent
        if actual_start_date is not None:
            project.actual_start_date = actual_start_date
        if actual_end_date is not None:
            project.actual_end_date = actual_end_date
        if budget_amount is not None:
            project.budget_amount = budget_amount
        if risk_level is not None:
            valid_risk = {"critical", "high", "medium", "low"}
            if risk_level not in valid_risk:
                raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_risk}")
            project.risk_level = risk_level

        project.updated_at = self._now_iso()
        return project

    # ----------------
    # Project Member
    # ----------------

    @is_tool(ToolType.READ)
    def list_project_members(self, project_ref: str, status: Optional[str] = None) -> str:
        """
        List all members of a project.

        Args:
            project_ref: Reference to the project.
            status: Optional filter by membership status (active, removed).

        Returns:
            str: JSON array of project member summary objects.

        Raises:
            ValueError: If the project is not found.
        """
        self._get_project(project_ref)

        results = []
        for pm in self.db.project_member.values():
            if pm.project_ref != project_ref:
                continue
            if status is not None and pm.status != status:
                continue
            emp = self._get_employee(pm.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "project_member_ref": pm.project_member_ref,
                "employee_ref": pm.employee_ref,
                "display_name": up.display_name,
                "project_role": pm.project_role,
                "joined_at": pm.joined_at,
                "left_at": pm.left_at,
                "status": pm.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_employee_projects(
        self,
        employee_ref: str,
        status: Optional[str] = None,
    ) -> str:
        """
        List all projects that an employee is a member of.

        Args:
            employee_ref: Reference to the employee.
            status: Optional filter by membership status (active, removed).

        Returns:
            str: JSON array of project membership objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for pm in self.db.project_member.values():
            if pm.employee_ref != employee_ref:
                continue
            if status is not None and pm.status != status:
                continue
            project = self._get_project(pm.project_ref)
            results.append({
                "project_ref": pm.project_ref,
                "project_name": project.project_name,
                "project_status": project.project_status,
                "project_role": pm.project_role,
                "joined_at": pm.joined_at,
                "status": pm.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def add_project_member(
        self,
        project_ref: str,
        employee_ref: str,
        project_role: str,
    ) -> ProjectMember:
        """
        Add a member to a project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_ref: Reference to the project.
            employee_ref: Reference to the employee to add.
            project_role: Role within the project (owner, lead, member, observer).

        Returns:
            ProjectMember: The newly created project membership.

        Raises:
            ValueError: If the project or employee is not found, or inputs are invalid.
        """
        self._get_project(project_ref)
        self._get_employee(employee_ref)

        valid_roles = {"owner", "lead", "member", "observer"}
        if project_role not in valid_roles:
            raise ValueError(f"Invalid project_role: {project_role}. Must be one of {valid_roles}")

        # Check for existing active membership
        for pm in self.db.project_member.values():
            if pm.project_ref == project_ref and pm.employee_ref == employee_ref and pm.status == "active":
                raise ValueError("Employee is already an active member of this project")

        now = self._now_iso()
        ref = self._generate_ref("PM", self.db.project_member)

        pm = ProjectMember(
            project_member_ref=ref,
            project_ref=project_ref,
            employee_ref=employee_ref,
            project_role=project_role,
            joined_at=now,
            left_at=None,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.project_member[ref] = pm
        return pm

    @is_tool(ToolType.WRITE)
    def remove_project_member(self, project_member_ref: str) -> ProjectMember:
        """
        Remove a member from a project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_member_ref: Reference to the project membership to remove.

        Returns:
            ProjectMember: The updated project membership.

        Raises:
            ValueError: If the membership is not found or already removed.
        """
        if project_member_ref not in self.db.project_member:
            raise ValueError("Project member not found")

        pm = self.db.project_member[project_member_ref]
        if pm.status == "removed":
            raise ValueError("Project member is already removed")

        now = self._now_iso()
        pm.status = "removed"
        pm.left_at = now
        pm.updated_at = now
        return pm

    # ----------------
    # Project Milestone
    # ----------------

    @is_tool(ToolType.READ)
    def get_project_milestone_details(self, project_milestone_ref: str) -> ProjectMilestone:
        """
        Retrieve the details of a specific project milestone.

        Args:
            project_milestone_ref: Unique identifier for the project milestone.

        Returns:
            ProjectMilestone: The project milestone object.

        Raises:
            ValueError: If the project milestone is not found.
        """
        return self._get_project_milestone(project_milestone_ref)

    @is_tool(ToolType.READ)
    def list_project_milestones(
        self,
        project_ref: str,
        milestone_status: Optional[str] = None,
    ) -> str:
        """
        List all milestones for a project.

        Args:
            project_ref: Reference to the project.
            milestone_status: Optional filter by milestone status.

        Returns:
            str: JSON array of milestone summary objects.

        Raises:
            ValueError: If the project is not found.
        """
        self._get_project(project_ref)

        results = []
        for ms in self.db.project_milestone.values():
            if ms.project_ref != project_ref:
                continue
            if milestone_status is not None and ms.milestone_status != milestone_status:
                continue
            results.append({
                "project_milestone_ref": ms.project_milestone_ref,
                "milestone_name": ms.milestone_name,
                "description": ms.description,
                "planned_date": ms.planned_date,
                "actual_date": ms.actual_date,
                "milestone_status": ms.milestone_status,
                "owner_employee_ref": ms.owner_employee_ref,
                "display_order": ms.display_order,
            })
        results.sort(key=lambda x: x["display_order"])
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_project_milestone(
        self,
        project_ref: str,
        milestone_name: str,
        description: str,
        planned_date: str,
        owner_employee_ref: str,
        display_order: int = 0,
    ) -> ProjectMilestone:
        """
        Create a new milestone for a project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_ref: Reference to the project.
            milestone_name: Name of the milestone.
            description: Description of the milestone.
            planned_date: Planned date (ISO 8601 date).
            owner_employee_ref: Employee reference of the milestone owner.
            display_order: Order for display/sorting.

        Returns:
            ProjectMilestone: The newly created milestone.

        Raises:
            ValueError: If the project or owner is not found.
        """
        self._get_project(project_ref)
        self._get_employee(owner_employee_ref)

        now = self._now_iso()
        ref = self._generate_ref("PMS", self.db.project_milestone)

        ms = ProjectMilestone(
            project_milestone_ref=ref,
            project_ref=project_ref,
            milestone_name=milestone_name,
            description=description,
            planned_date=planned_date,
            actual_date=None,
            milestone_status="pending",
            owner_employee_ref=owner_employee_ref,
            display_order=display_order,
            created_at=now,
            updated_at=now,
        )
        self.db.project_milestone[ref] = ms
        return ms

    @is_tool(ToolType.WRITE)
    def update_project_milestone(
        self,
        project_milestone_ref: str,
        milestone_name: Optional[str] = None,
        description: Optional[str] = None,
        planned_date: Optional[str] = None,
        actual_date: Optional[str] = None,
        milestone_status: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
        display_order: Optional[int] = None,
    ) -> ProjectMilestone:
        """
        Update an existing project milestone. The agent must ask for explicit user confirmation before calling.

        Args:
            project_milestone_ref: Reference to the milestone.
            milestone_name: New name, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            planned_date: New planned date, or None to keep unchanged.
            actual_date: New actual date, or None to keep unchanged.
            milestone_status: New status, or None to keep unchanged.
            owner_employee_ref: New owner, or None to keep unchanged.
            display_order: New display order, or None to keep unchanged.

        Returns:
            ProjectMilestone: The updated milestone.

        Raises:
            ValueError: If the milestone is not found or inputs are invalid.
        """
        ms = self._get_project_milestone(project_milestone_ref)

        if milestone_name is not None:
            ms.milestone_name = milestone_name
        if description is not None:
            ms.description = description
        if planned_date is not None:
            ms.planned_date = planned_date
        if actual_date is not None:
            ms.actual_date = actual_date
        if milestone_status is not None:
            valid_statuses = {"pending", "in_progress", "completed", "delayed", "cancelled"}
            if milestone_status not in valid_statuses:
                raise ValueError(f"Invalid milestone_status: {milestone_status}. Must be one of {valid_statuses}")
            ms.milestone_status = milestone_status
        if owner_employee_ref is not None:
            self._get_employee(owner_employee_ref)
            ms.owner_employee_ref = owner_employee_ref
        if display_order is not None:
            ms.display_order = display_order

        ms.updated_at = self._now_iso()
        return ms

    # ----------------
    # Project Task
    # ----------------

    @is_tool(ToolType.READ)
    def get_project_task_details(self, project_task_ref: str) -> ProjectTask:
        """
        Retrieve the details of a specific project task.

        Args:
            project_task_ref: Unique identifier for the project task.

        Returns:
            ProjectTask: The project task object.

        Raises:
            ValueError: If the project task is not found.
        """
        return self._get_project_task(project_task_ref)

    @is_tool(ToolType.READ)
    def list_project_tasks(
        self,
        project_ref: str,
        task_status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_employee_ref: Optional[str] = None,
        project_milestone_ref: Optional[str] = None,
    ) -> str:
        """
        List tasks for a project with optional filters.

        Args:
            project_ref: Reference to the project.
            task_status: Optional filter by task status.
            priority: Optional filter by priority.
            assignee_employee_ref: Optional filter by assignee.
            project_milestone_ref: Optional filter by milestone.

        Returns:
            str: JSON array of task summary objects.

        Raises:
            ValueError: If the project is not found.
        """
        self._get_project(project_ref)

        results = []
        for t in self.db.project_task.values():
            if t.project_ref != project_ref:
                continue
            if task_status is not None and t.task_status != task_status:
                continue
            if priority is not None and t.priority != priority:
                continue
            if assignee_employee_ref is not None and t.assignee_employee_ref != assignee_employee_ref:
                continue
            if project_milestone_ref is not None and t.project_milestone_ref != project_milestone_ref:
                continue
            results.append({
                "project_task_ref": t.project_task_ref,
                "task_title": t.task_title,
                "task_type": t.task_type,
                "task_status": t.task_status,
                "priority": t.priority,
                "assignee_employee_ref": t.assignee_employee_ref,
                "planned_start_date": t.planned_start_date,
                "planned_end_date": t.planned_end_date,
                "progress_percent": t.progress_percent,
                "estimated_hours": t.estimated_hours,
                "actual_hours": t.actual_hours,
                "project_milestone_ref": t.project_milestone_ref,
                "display_order": t.display_order,
            })
        results.sort(key=lambda x: x["display_order"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_tasks_for_employee(
        self,
        employee_ref: str,
        task_status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> str:
        """
        List all project tasks assigned to an employee.

        Args:
            employee_ref: Reference to the employee.
            task_status: Optional filter by task status.
            priority: Optional filter by priority.

        Returns:
            str: JSON array of task summary objects with project info.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for t in self.db.project_task.values():
            if t.assignee_employee_ref != employee_ref:
                continue
            if task_status is not None and t.task_status != task_status:
                continue
            if priority is not None and t.priority != priority:
                continue
            project = self._get_project(t.project_ref)
            results.append({
                "project_task_ref": t.project_task_ref,
                "task_title": t.task_title,
                "task_type": t.task_type,
                "task_status": t.task_status,
                "priority": t.priority,
                "project_ref": t.project_ref,
                "project_name": project.project_name,
                "planned_start_date": t.planned_start_date,
                "planned_end_date": t.planned_end_date,
                "progress_percent": t.progress_percent,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_project_task(
        self,
        project_ref: str,
        task_title: str,
        task_description: str,
        task_type: str,
        priority: str,
        assignee_employee_ref: str,
        reporter_employee_ref: str,
        planned_start_date: str,
        planned_end_date: str,
        estimated_hours: float,
        project_milestone_ref: Optional[str] = None,
        parent_task_ref: Optional[str] = None,
        display_order: int = 0,
    ) -> ProjectTask:
        """
        Create a new task within a project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_ref: Reference to the project.
            task_title: Title of the task.
            task_description: Detailed description.
            task_type: Type (development, design, testing, documentation, review, bugfix, research, other).
            priority: Priority (critical, high, medium, low).
            assignee_employee_ref: Employee reference of the assignee.
            reporter_employee_ref: Employee reference of the reporter.
            planned_start_date: Planned start date (ISO 8601 date).
            planned_end_date: Planned end date (ISO 8601 date).
            estimated_hours: Estimated hours to complete.
            project_milestone_ref: Optional milestone reference.
            parent_task_ref: Optional parent task reference.
            display_order: Order for display/sorting.

        Returns:
            ProjectTask: The newly created task.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_project(project_ref)
        self._get_employee(assignee_employee_ref)
        self._get_employee(reporter_employee_ref)

        valid_types = {"development", "design", "testing", "documentation", "review", "bugfix", "research", "other"}
        if task_type not in valid_types:
            raise ValueError(f"Invalid task_type: {task_type}. Must be one of {valid_types}")

        valid_priorities = {"critical", "high", "medium", "low"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        if project_milestone_ref is not None:
            self._get_project_milestone(project_milestone_ref)
        if parent_task_ref is not None:
            self._get_project_task(parent_task_ref)

        now = self._now_iso()
        ref = self._generate_ref("PT", self.db.project_task)

        task = ProjectTask(
            project_task_ref=ref,
            project_ref=project_ref,
            project_milestone_ref=project_milestone_ref,
            parent_task_ref=parent_task_ref,
            task_title=task_title,
            task_description=task_description,
            task_type=task_type,
            task_status="todo",
            priority=priority,
            assignee_employee_ref=assignee_employee_ref,
            reporter_employee_ref=reporter_employee_ref,
            planned_start_date=planned_start_date,
            planned_end_date=planned_end_date,
            actual_start_date=None,
            actual_end_date=None,
            estimated_hours=estimated_hours,
            actual_hours=None,
            progress_percent=0,
            display_order=display_order,
            created_at=now,
            updated_at=now,
        )
        self.db.project_task[ref] = task
        return task

    @is_tool(ToolType.WRITE)
    def update_project_task(
        self,
        project_task_ref: str,
        task_title: Optional[str] = None,
        task_description: Optional[str] = None,
        task_type: Optional[str] = None,
        task_status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_employee_ref: Optional[str] = None,
        actual_start_date: Optional[str] = None,
        actual_end_date: Optional[str] = None,
        actual_hours: Optional[float] = None,
        progress_percent: Optional[int] = None,
    ) -> ProjectTask:
        """
        Update an existing project task. The agent must ask for explicit user confirmation before calling.

        Args:
            project_task_ref: Reference to the task.
            task_title: New title, or None to keep unchanged.
            task_description: New description, or None to keep unchanged.
            task_type: New type, or None to keep unchanged.
            task_status: New status, or None to keep unchanged.
            priority: New priority, or None to keep unchanged.
            assignee_employee_ref: New assignee, or None to keep unchanged.
            actual_start_date: New actual start date, or None to keep unchanged.
            actual_end_date: New actual end date, or None to keep unchanged.
            actual_hours: New actual hours, or None to keep unchanged.
            progress_percent: New progress percentage, or None to keep unchanged.

        Returns:
            ProjectTask: The updated task.

        Raises:
            ValueError: If the task is not found or inputs are invalid.
        """
        task = self._get_project_task(project_task_ref)

        if task_title is not None:
            task.task_title = task_title
        if task_description is not None:
            task.task_description = task_description
        if task_type is not None:
            valid_types = {"development", "design", "testing", "documentation", "review", "bugfix", "research", "other"}
            if task_type not in valid_types:
                raise ValueError(f"Invalid task_type: {task_type}. Must be one of {valid_types}")
            task.task_type = task_type
        if task_status is not None:
            valid_statuses = {"todo", "in_progress", "in_review", "done", "blocked", "cancelled"}
            if task_status not in valid_statuses:
                raise ValueError(f"Invalid task_status: {task_status}. Must be one of {valid_statuses}")
            task.task_status = task_status
        if priority is not None:
            valid_priorities = {"critical", "high", "medium", "low"}
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
            task.priority = priority
        if assignee_employee_ref is not None:
            self._get_employee(assignee_employee_ref)
            task.assignee_employee_ref = assignee_employee_ref
        if actual_start_date is not None:
            task.actual_start_date = actual_start_date
        if actual_end_date is not None:
            task.actual_end_date = actual_end_date
        if actual_hours is not None:
            task.actual_hours = actual_hours
        if progress_percent is not None:
            if progress_percent < 0 or progress_percent > 100:
                raise ValueError("progress_percent must be between 0 and 100")
            task.progress_percent = progress_percent

        task.updated_at = self._now_iso()
        return task

    # ----------------
    # Project Risk
    # ----------------

    @is_tool(ToolType.READ)
    def get_project_risk_details(self, project_risk_ref: str) -> ProjectRisk:
        """
        Retrieve the details of a specific project risk.

        Args:
            project_risk_ref: Unique identifier for the project risk.

        Returns:
            ProjectRisk: The project risk object.

        Raises:
            ValueError: If the project risk is not found.
        """
        return self._get_project_risk(project_risk_ref)

    @is_tool(ToolType.READ)
    def list_project_risks(
        self,
        project_ref: str,
        risk_status: Optional[str] = None,
        risk_level: Optional[str] = None,
    ) -> str:
        """
        List all risks for a project.

        Args:
            project_ref: Reference to the project.
            risk_status: Optional filter by risk status.
            risk_level: Optional filter by risk level.

        Returns:
            str: JSON array of risk summary objects.

        Raises:
            ValueError: If the project is not found.
        """
        self._get_project(project_ref)

        results = []
        for r in self.db.project_risk.values():
            if r.project_ref != project_ref:
                continue
            if risk_status is not None and r.risk_status != risk_status:
                continue
            if risk_level is not None and r.risk_level != risk_level:
                continue
            results.append({
                "project_risk_ref": r.project_risk_ref,
                "risk_title": r.risk_title,
                "risk_level": r.risk_level,
                "probability": r.probability,
                "impact": r.impact,
                "risk_status": r.risk_status,
                "owner_employee_ref": r.owner_employee_ref,
                "mitigation_plan": r.mitigation_plan,
                "identified_at": r.identified_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_project_risk(
        self,
        project_ref: str,
        risk_title: str,
        risk_description: str,
        risk_level: str,
        probability: str,
        impact: str,
        mitigation_plan: str,
        owner_employee_ref: str,
    ) -> ProjectRisk:
        """
        Create a new risk for a project. The agent must ask for explicit user confirmation before calling.

        Args:
            project_ref: Reference to the project.
            risk_title: Title of the risk.
            risk_description: Detailed description.
            risk_level: Overall risk level (critical, high, medium, low).
            probability: Probability (very_high, high, medium, low, very_low).
            impact: Impact (critical, high, medium, low, negligible).
            mitigation_plan: Plan to mitigate the risk.
            owner_employee_ref: Employee reference of the risk owner.

        Returns:
            ProjectRisk: The newly created risk.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_project(project_ref)
        self._get_employee(owner_employee_ref)

        valid_levels = {"critical", "high", "medium", "low"}
        if risk_level not in valid_levels:
            raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_levels}")

        valid_probs = {"very_high", "high", "medium", "low", "very_low"}
        if probability not in valid_probs:
            raise ValueError(f"Invalid probability: {probability}. Must be one of {valid_probs}")

        valid_impacts = {"critical", "high", "medium", "low", "negligible"}
        if impact not in valid_impacts:
            raise ValueError(f"Invalid impact: {impact}. Must be one of {valid_impacts}")

        now = self._now_iso()
        ref = self._generate_ref("PR", self.db.project_risk)

        risk = ProjectRisk(
            project_risk_ref=ref,
            project_ref=project_ref,
            risk_title=risk_title,
            risk_description=risk_description,
            risk_level=risk_level,
            probability=probability,
            impact=impact,
            mitigation_plan=mitigation_plan,
            owner_employee_ref=owner_employee_ref,
            risk_status="open",
            identified_at=now,
            resolved_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.project_risk[ref] = risk
        return risk

    @is_tool(ToolType.WRITE)
    def update_project_risk(
        self,
        project_risk_ref: str,
        risk_title: Optional[str] = None,
        risk_description: Optional[str] = None,
        risk_level: Optional[str] = None,
        probability: Optional[str] = None,
        impact: Optional[str] = None,
        mitigation_plan: Optional[str] = None,
        risk_status: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
    ) -> ProjectRisk:
        """
        Update an existing project risk. The agent must ask for explicit user confirmation before calling.

        Args:
            project_risk_ref: Reference to the risk.
            risk_title: New title, or None to keep unchanged.
            risk_description: New description, or None to keep unchanged.
            risk_level: New risk level, or None to keep unchanged.
            probability: New probability, or None to keep unchanged.
            impact: New impact, or None to keep unchanged.
            mitigation_plan: New mitigation plan, or None to keep unchanged.
            risk_status: New status, or None to keep unchanged.
            owner_employee_ref: New owner, or None to keep unchanged.

        Returns:
            ProjectRisk: The updated risk.

        Raises:
            ValueError: If the risk is not found or inputs are invalid.
        """
        risk = self._get_project_risk(project_risk_ref)

        if risk_title is not None:
            risk.risk_title = risk_title
        if risk_description is not None:
            risk.risk_description = risk_description
        if risk_level is not None:
            valid_levels = {"critical", "high", "medium", "low"}
            if risk_level not in valid_levels:
                raise ValueError(f"Invalid risk_level: {risk_level}. Must be one of {valid_levels}")
            risk.risk_level = risk_level
        if probability is not None:
            valid_probs = {"very_high", "high", "medium", "low", "very_low"}
            if probability not in valid_probs:
                raise ValueError(f"Invalid probability: {probability}. Must be one of {valid_probs}")
            risk.probability = probability
        if impact is not None:
            valid_impacts = {"critical", "high", "medium", "low", "negligible"}
            if impact not in valid_impacts:
                raise ValueError(f"Invalid impact: {impact}. Must be one of {valid_impacts}")
            risk.impact = impact
        if mitigation_plan is not None:
            risk.mitigation_plan = mitigation_plan
        if risk_status is not None:
            valid_statuses = {"open", "mitigating", "resolved", "accepted", "closed"}
            if risk_status not in valid_statuses:
                raise ValueError(f"Invalid risk_status: {risk_status}. Must be one of {valid_statuses}")
            risk.risk_status = risk_status
            if risk_status in ("resolved", "closed"):
                risk.resolved_at = self._now_iso()
        if owner_employee_ref is not None:
            self._get_employee(owner_employee_ref)
            risk.owner_employee_ref = owner_employee_ref

        risk.updated_at = self._now_iso()
        return risk

    # ========================================
    # Schedule Event (日程/待办汇总 / 日程/待办提醒)
    # ========================================

    @is_tool(ToolType.READ)
    def get_schedule_event_details(self, schedule_event_ref: str) -> ScheduleEvent:
        """
        Retrieve the details of a specific schedule event.

        Args:
            schedule_event_ref: Unique identifier for the schedule event.

        Returns:
            ScheduleEvent: The schedule event object.

        Raises:
            ValueError: If the schedule event is not found.
        """
        return self._get_schedule_event(schedule_event_ref)

    @is_tool(ToolType.READ)
    def list_schedule_events_for_employee(
        self,
        employee_ref: str,
        event_type: Optional[str] = None,
        event_status: Optional[str] = None,
        start_after: Optional[str] = None,
        start_before: Optional[str] = None,
    ) -> str:
        """
        List schedule events for an employee (as organizer or attendee).

        Args:
            employee_ref: Reference to the employee.
            event_type: Optional filter by event type.
            event_status: Optional filter by event status.
            start_after: Optional filter for events starting after this time (ISO 8601).
            start_before: Optional filter for events starting before this time (ISO 8601).

        Returns:
            str: JSON array of schedule event summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        # Collect event refs where employee is organizer or attendee
        event_refs = set()
        for se in self.db.schedule_event.values():
            if se.organizer_employee_ref == employee_ref:
                event_refs.add(se.schedule_event_ref)
        for sea in self.db.schedule_event_attendee.values():
            if sea.employee_ref == employee_ref:
                event_refs.add(sea.schedule_event_ref)

        results = []
        for se_ref in event_refs:
            se = self.db.schedule_event[se_ref]
            if event_type is not None and se.event_type != event_type:
                continue
            if event_status is not None and se.event_status != event_status:
                continue
            if start_after is not None and se.start_time < start_after:
                continue
            if start_before is not None and se.start_time > start_before:
                continue
            results.append({
                "schedule_event_ref": se.schedule_event_ref,
                "event_title": se.event_title,
                "event_type": se.event_type,
                "event_status": se.event_status,
                "start_time": se.start_time,
                "end_time": se.end_time,
                "is_all_day": se.is_all_day,
                "location": se.location,
                "organizer_employee_ref": se.organizer_employee_ref,
                "visibility": se.visibility,
            })
        results.sort(key=lambda x: x["start_time"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_schedule_event_attendees(self, schedule_event_ref: str) -> str:
        """
        List all attendees of a schedule event.

        Args:
            schedule_event_ref: Reference to the schedule event.

        Returns:
            str: JSON array of attendee summary objects.

        Raises:
            ValueError: If the schedule event is not found.
        """
        self._get_schedule_event(schedule_event_ref)

        results = []
        for sea in self.db.schedule_event_attendee.values():
            if sea.schedule_event_ref != schedule_event_ref:
                continue
            emp = self._get_employee(sea.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "schedule_event_attendee_ref": sea.schedule_event_attendee_ref,
                "employee_ref": sea.employee_ref,
                "display_name": up.display_name,
                "attendee_role": sea.attendee_role,
                "rsvp_status": sea.rsvp_status,
                "responded_at": sea.responded_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_schedule_event(
        self,
        organizer_employee_ref: str,
        event_title: str,
        event_description: str,
        event_type: str,
        start_time: str,
        end_time: str,
        timezone: str,
        is_all_day: bool = False,
        location: str = "",
        visibility: str = "default",
        recurrence_rule: Optional[str] = None,
        meeting_ref: Optional[str] = None,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
    ) -> ScheduleEvent:
        """
        Create a new schedule event. The agent must ask for explicit user confirmation before calling.

        Args:
            organizer_employee_ref: Employee reference of the organizer.
            event_title: Title of the event.
            event_description: Description of the event.
            event_type: Type (meeting, appointment, reminder, out_of_office, focus_time, other).
            start_time: Start time (ISO 8601).
            end_time: End time (ISO 8601).
            timezone: Timezone (e.g., Asia/Shanghai).
            is_all_day: Whether the event spans the entire day.
            location: Location of the event.
            visibility: Visibility (default, public, private, confidential).
            recurrence_rule: Optional recurrence rule.
            meeting_ref: Optional meeting reference.
            related_resource_type: Optional related resource type.
            related_resource_ref: Optional related resource reference.

        Returns:
            ScheduleEvent: The newly created schedule event.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(organizer_employee_ref)

        valid_types = {"meeting", "appointment", "reminder", "out_of_office", "focus_time", "other"}
        if event_type not in valid_types:
            raise ValueError(f"Invalid event_type: {event_type}. Must be one of {valid_types}")

        valid_vis = {"default", "public", "private", "confidential"}
        if visibility not in valid_vis:
            raise ValueError(f"Invalid visibility: {visibility}. Must be one of {valid_vis}")

        now = self._now_iso()
        ref = self._generate_ref("SE", self.db.schedule_event)

        se = ScheduleEvent(
            schedule_event_ref=ref,
            organizer_employee_ref=organizer_employee_ref,
            event_title=event_title,
            event_description=event_description,
            event_type=event_type,
            event_status="confirmed",
            start_time=start_time,
            end_time=end_time,
            timezone=timezone,
            is_all_day=is_all_day,
            recurrence_rule=recurrence_rule,
            location=location,
            meeting_ref=meeting_ref,
            visibility=visibility,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.schedule_event[ref] = se
        return se

    @is_tool(ToolType.WRITE)
    def update_schedule_event(
        self,
        schedule_event_ref: str,
        event_title: Optional[str] = None,
        event_description: Optional[str] = None,
        event_type: Optional[str] = None,
        event_status: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        location: Optional[str] = None,
        visibility: Optional[str] = None,
    ) -> ScheduleEvent:
        """
        Update an existing schedule event. The agent must ask for explicit user confirmation before calling.

        Args:
            schedule_event_ref: Reference to the schedule event.
            event_title: New title, or None to keep unchanged.
            event_description: New description, or None to keep unchanged.
            event_type: New type, or None to keep unchanged.
            event_status: New status, or None to keep unchanged.
            start_time: New start time, or None to keep unchanged.
            end_time: New end time, or None to keep unchanged.
            location: New location, or None to keep unchanged.
            visibility: New visibility, or None to keep unchanged.

        Returns:
            ScheduleEvent: The updated schedule event.

        Raises:
            ValueError: If the event is not found or inputs are invalid.
        """
        se = self._get_schedule_event(schedule_event_ref)

        if event_title is not None:
            se.event_title = event_title
        if event_description is not None:
            se.event_description = event_description
        if event_type is not None:
            valid_types = {"meeting", "appointment", "reminder", "out_of_office", "focus_time", "other"}
            if event_type not in valid_types:
                raise ValueError(f"Invalid event_type: {event_type}. Must be one of {valid_types}")
            se.event_type = event_type
        if event_status is not None:
            valid_statuses = {"tentative", "confirmed", "cancelled"}
            if event_status not in valid_statuses:
                raise ValueError(f"Invalid event_status: {event_status}. Must be one of {valid_statuses}")
            se.event_status = event_status
        if start_time is not None:
            se.start_time = start_time
        if end_time is not None:
            se.end_time = end_time
        if location is not None:
            se.location = location
        if visibility is not None:
            valid_vis = {"default", "public", "private", "confidential"}
            if visibility not in valid_vis:
                raise ValueError(f"Invalid visibility: {visibility}. Must be one of {valid_vis}")
            se.visibility = visibility

        se.updated_at = self._now_iso()
        return se

    @is_tool(ToolType.WRITE)
    def add_schedule_event_attendee(
        self,
        schedule_event_ref: str,
        employee_ref: str,
        attendee_role: str = "required",
    ) -> ScheduleEventAttendee:
        """
        Add an attendee to a schedule event. The agent must ask for explicit user confirmation before calling.

        Args:
            schedule_event_ref: Reference to the schedule event.
            employee_ref: Reference to the employee to add.
            attendee_role: Role of the attendee (required, optional, resource).

        Returns:
            ScheduleEventAttendee: The newly created attendee record.

        Raises:
            ValueError: If the event or employee is not found, or inputs are invalid.
        """
        self._get_schedule_event(schedule_event_ref)
        self._get_employee(employee_ref)

        valid_roles = {"required", "optional", "resource"}
        if attendee_role not in valid_roles:
            raise ValueError(f"Invalid attendee_role: {attendee_role}. Must be one of {valid_roles}")

        # Check for duplicate
        for sea in self.db.schedule_event_attendee.values():
            if sea.schedule_event_ref == schedule_event_ref and sea.employee_ref == employee_ref:
                raise ValueError("Employee is already an attendee of this event")

        now = self._now_iso()
        ref = self._generate_ref("SEA", self.db.schedule_event_attendee)

        sea = ScheduleEventAttendee(
            schedule_event_attendee_ref=ref,
            schedule_event_ref=schedule_event_ref,
            employee_ref=employee_ref,
            attendee_role=attendee_role,
            rsvp_status="pending",
            responded_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.schedule_event_attendee[ref] = sea
        return sea

    @is_tool(ToolType.WRITE)
    def update_schedule_event_attendee_rsvp(
        self,
        schedule_event_attendee_ref: str,
        rsvp_status: str,
    ) -> ScheduleEventAttendee:
        """
        Update the RSVP status of a schedule event attendee. The agent must ask for explicit user confirmation before calling.

        Args:
            schedule_event_attendee_ref: Reference to the attendee record.
            rsvp_status: New RSVP status (pending, accepted, declined, tentative).

        Returns:
            ScheduleEventAttendee: The updated attendee record.

        Raises:
            ValueError: If the attendee record is not found or status is invalid.
        """
        if schedule_event_attendee_ref not in self.db.schedule_event_attendee:
            raise ValueError("Schedule event attendee not found")

        valid_statuses = {"pending", "accepted", "declined", "tentative"}
        if rsvp_status not in valid_statuses:
            raise ValueError(f"Invalid rsvp_status: {rsvp_status}. Must be one of {valid_statuses}")

        sea = self.db.schedule_event_attendee[schedule_event_attendee_ref]
        sea.rsvp_status = rsvp_status
        sea.responded_at = self._now_iso()
        sea.updated_at = self._now_iso()
        return sea

    # ========================================
    # Todo Item (日程/待办汇总 / 日程/待办提醒)
    # ========================================

    @is_tool(ToolType.READ)
    def get_todo_item_details(self, todo_item_ref: str) -> TodoItem:
        """
        Retrieve the details of a specific to-do item.

        Args:
            todo_item_ref: Unique identifier for the to-do item.

        Returns:
            TodoItem: The to-do item object.

        Raises:
            ValueError: If the to-do item is not found.
        """
        return self._get_todo_item(todo_item_ref)

    @is_tool(ToolType.READ)
    def list_todo_items_for_employee(
        self,
        employee_ref: str,
        todo_status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> str:
        """
        List all to-do items for an employee.

        Args:
            employee_ref: Reference to the employee.
            todo_status: Optional filter by status (pending, in_progress, completed, cancelled).
            priority: Optional filter by priority (critical, high, medium, low).

        Returns:
            str: JSON array of to-do item summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for ti in self.db.todo_item.values():
            if ti.owner_employee_ref != employee_ref:
                continue
            if todo_status is not None and ti.todo_status != todo_status:
                continue
            if priority is not None and ti.priority != priority:
                continue
            results.append({
                "todo_item_ref": ti.todo_item_ref,
                "title": ti.title,
                "description": ti.description,
                "todo_status": ti.todo_status,
                "priority": ti.priority,
                "due_date": ti.due_date,
                "completed_at": ti.completed_at,
                "related_resource_type": ti.related_resource_type,
                "related_resource_ref": ti.related_resource_ref,
            })
        results.sort(key=lambda x: x["due_date"])
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_todo_item(
        self,
        owner_employee_ref: str,
        title: str,
        description: str,
        priority: str,
        due_date: str,
        related_resource_type: Optional[str] = None,
        related_resource_ref: Optional[str] = None,
    ) -> TodoItem:
        """
        Create a new to-do item. The agent must ask for explicit user confirmation before calling.

        Args:
            owner_employee_ref: Employee reference of the owner.
            title: Title of the to-do item.
            description: Description.
            priority: Priority (critical, high, medium, low).
            due_date: Due date (ISO 8601).
            related_resource_type: Optional related resource type.
            related_resource_ref: Optional related resource reference.

        Returns:
            TodoItem: The newly created to-do item.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(owner_employee_ref)

        valid_priorities = {"critical", "high", "medium", "low"}
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")

        now = self._now_iso()
        ref = self._generate_ref("TODO", self.db.todo_item)

        ti = TodoItem(
            todo_item_ref=ref,
            owner_employee_ref=owner_employee_ref,
            title=title,
            description=description,
            todo_status="pending",
            priority=priority,
            due_date=due_date,
            completed_at=None,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            created_at=now,
            updated_at=now,
        )
        self.db.todo_item[ref] = ti
        return ti

    @is_tool(ToolType.WRITE)
    def update_todo_item(
        self,
        todo_item_ref: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        todo_status: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> TodoItem:
        """
        Update an existing to-do item. The agent must ask for explicit user confirmation before calling.

        Args:
            todo_item_ref: Reference to the to-do item.
            title: New title, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            todo_status: New status, or None to keep unchanged.
            priority: New priority, or None to keep unchanged.
            due_date: New due date, or None to keep unchanged.

        Returns:
            TodoItem: The updated to-do item.

        Raises:
            ValueError: If the to-do item is not found or inputs are invalid.
        """
        ti = self._get_todo_item(todo_item_ref)

        if title is not None:
            ti.title = title
        if description is not None:
            ti.description = description
        if todo_status is not None:
            valid_statuses = {"pending", "in_progress", "completed", "cancelled"}
            if todo_status not in valid_statuses:
                raise ValueError(f"Invalid todo_status: {todo_status}. Must be one of {valid_statuses}")
            ti.todo_status = todo_status
            if todo_status == "completed":
                ti.completed_at = self._now_iso()
        if priority is not None:
            valid_priorities = {"critical", "high", "medium", "low"}
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
            ti.priority = priority
        if due_date is not None:
            ti.due_date = due_date

        ti.updated_at = self._now_iso()
        return ti

    # ========================================
    # Reminder Rule (日程/待办提醒)
    # ========================================

    @is_tool(ToolType.READ)
    def get_reminder_rule_details(self, reminder_rule_ref: str) -> ReminderRule:
        """
        Retrieve the details of a specific reminder rule.

        Args:
            reminder_rule_ref: Unique identifier for the reminder rule.

        Returns:
            ReminderRule: The reminder rule object.

        Raises:
            ValueError: If the reminder rule is not found.
        """
        return self._get_reminder_rule(reminder_rule_ref)

    @is_tool(ToolType.READ)
    def list_reminder_rules_for_employee(
        self,
        employee_ref: str,
        reminder_status: Optional[str] = None,
    ) -> str:
        """
        List all reminder rules for an employee.

        Args:
            employee_ref: Reference to the employee.
            reminder_status: Optional filter by status (pending, triggered, cancelled, failed).

        Returns:
            str: JSON array of reminder rule summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for rr in self.db.reminder_rule.values():
            if rr.employee_ref != employee_ref:
                continue
            if reminder_status is not None and rr.reminder_status != reminder_status:
                continue
            results.append({
                "reminder_rule_ref": rr.reminder_rule_ref,
                "related_resource_type": rr.related_resource_type,
                "related_resource_ref": rr.related_resource_ref,
                "remind_at": rr.remind_at,
                "offset_minutes": rr.offset_minutes,
                "channel": rr.channel,
                "reminder_status": rr.reminder_status,
                "triggered_at": rr.triggered_at,
            })
        results.sort(key=lambda x: x["remind_at"])
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_reminder_rule(
        self,
        employee_ref: str,
        related_resource_type: str,
        related_resource_ref: str,
        remind_at: str,
        offset_minutes: int,
        channel: str,
    ) -> ReminderRule:
        """
        Create a new reminder rule. The agent must ask for explicit user confirmation before calling.

        Args:
            employee_ref: Reference to the employee.
            related_resource_type: Type of the related resource (e.g., schedule_event, todo_item, project_task).
            related_resource_ref: Reference to the related resource.
            remind_at: Timestamp when the reminder should trigger (ISO 8601).
            offset_minutes: Minutes before the event to trigger.
            channel: Delivery channel (in_app, email, sms, push).

        Returns:
            ReminderRule: The newly created reminder rule.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(employee_ref)

        valid_channels = {"in_app", "email", "sms", "push"}
        if channel not in valid_channels:
            raise ValueError(f"Invalid channel: {channel}. Must be one of {valid_channels}")

        now = self._now_iso()
        ref = self._generate_ref("RR", self.db.reminder_rule)

        rr = ReminderRule(
            reminder_rule_ref=ref,
            employee_ref=employee_ref,
            related_resource_type=related_resource_type,
            related_resource_ref=related_resource_ref,
            remind_at=remind_at,
            offset_minutes=offset_minutes,
            channel=channel,
            reminder_status="pending",
            triggered_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.reminder_rule[ref] = rr
        return rr

    @is_tool(ToolType.WRITE)
    def cancel_reminder_rule(self, reminder_rule_ref: str) -> ReminderRule:
        """
        Cancel a pending reminder rule. The agent must ask for explicit user confirmation before calling.

        Args:
            reminder_rule_ref: Reference to the reminder rule.

        Returns:
            ReminderRule: The updated reminder rule.

        Raises:
            ValueError: If the reminder rule is not found or not in pending status.
        """
        rr = self._get_reminder_rule(reminder_rule_ref)

        if rr.reminder_status != "pending":
            raise ValueError(f"Reminder rule is not pending, current status: {rr.reminder_status}")

        rr.reminder_status = "cancelled"
        rr.updated_at = self._now_iso()
        return rr

    # ========================================
    # Meeting (远程会议设置)
    # ========================================

    @is_tool(ToolType.READ)
    def get_meeting_details(self, meeting_ref: str) -> Meeting:
        """
        Retrieve the details of a specific meeting.

        Args:
            meeting_ref: Unique identifier for the meeting.

        Returns:
            Meeting: The meeting object.

        Raises:
            ValueError: If the meeting is not found.
        """
        return self._get_meeting(meeting_ref)

    @is_tool(ToolType.READ)
    def list_meetings(
        self,
        meeting_type: Optional[str] = None,
        meeting_status: Optional[str] = None,
        organizer_employee_ref: Optional[str] = None,
    ) -> str:
        """
        List meetings with optional filters.

        Args:
            meeting_type: Optional filter by meeting type (video, audio, in_person, hybrid).
            meeting_status: Optional filter by meeting status.
            organizer_employee_ref: Optional filter by organizer.

        Returns:
            str: JSON array of meeting summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for m in self.db.meeting.values():
            if meeting_type is not None and m.meeting_type != meeting_type:
                continue
            if meeting_status is not None and m.meeting_status != meeting_status:
                continue
            if organizer_employee_ref is not None and m.organizer_employee_ref != organizer_employee_ref:
                continue
            results.append({
                "meeting_ref": m.meeting_ref,
                "meeting_title": m.meeting_title,
                "meeting_type": m.meeting_type,
                "meeting_status": m.meeting_status,
                "organizer_employee_ref": m.organizer_employee_ref,
                "start_time": m.start_time,
                "end_time": m.end_time,
                "meeting_platform": m.meeting_platform,
                "meeting_link": m.meeting_link,
                "meeting_room": m.meeting_room,
                "is_recorded": m.is_recorded,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_meetings_for_employee(
        self,
        employee_ref: str,
        meeting_status: Optional[str] = None,
    ) -> str:
        """
        List all meetings that an employee is participating in (as organizer or participant).

        Args:
            employee_ref: Reference to the employee.
            meeting_status: Optional filter by meeting status.

        Returns:
            str: JSON array of meeting summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        meeting_refs = set()
        for m in self.db.meeting.values():
            if m.organizer_employee_ref == employee_ref:
                meeting_refs.add(m.meeting_ref)
        for mp in self.db.meeting_participant.values():
            if mp.employee_ref == employee_ref:
                meeting_refs.add(mp.meeting_ref)

        results = []
        for m_ref in meeting_refs:
            m = self.db.meeting[m_ref]
            if meeting_status is not None and m.meeting_status != meeting_status:
                continue
            results.append({
                "meeting_ref": m.meeting_ref,
                "meeting_title": m.meeting_title,
                "meeting_type": m.meeting_type,
                "meeting_status": m.meeting_status,
                "start_time": m.start_time,
                "end_time": m.end_time,
                "meeting_platform": m.meeting_platform,
                "meeting_link": m.meeting_link,
            })
        results.sort(key=lambda x: x["start_time"])
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_meeting_participants(self, meeting_ref: str) -> str:
        """
        List all participants of a meeting.

        Args:
            meeting_ref: Reference to the meeting.

        Returns:
            str: JSON array of participant summary objects.

        Raises:
            ValueError: If the meeting is not found.
        """
        self._get_meeting(meeting_ref)

        results = []
        for mp in self.db.meeting_participant.values():
            if mp.meeting_ref != meeting_ref:
                continue
            emp = self._get_employee(mp.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "meeting_participant_ref": mp.meeting_participant_ref,
                "employee_ref": mp.employee_ref,
                "display_name": up.display_name,
                "participant_role": mp.participant_role,
                "attendance_status": mp.attendance_status,
                "join_time": mp.join_time,
                "leave_time": mp.leave_time,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_meeting(
        self,
        meeting_title: str,
        meeting_type: str,
        organizer_employee_ref: str,
        start_time: str,
        end_time: str,
        timezone: str,
        meeting_platform: str,
        meeting_link: str = "",
        meeting_password: str = "",
        meeting_room: str = "",
        is_recorded: bool = False,
        allow_screen_share: bool = True,
        notes: str = "",
        schedule_event_ref: Optional[str] = None,
    ) -> Meeting:
        """
        Create a new meeting. The agent must ask for explicit user confirmation before calling.

        Args:
            meeting_title: Title of the meeting.
            meeting_type: Type (video, audio, in_person, hybrid).
            organizer_employee_ref: Employee reference of the organizer.
            start_time: Start time (ISO 8601).
            end_time: End time (ISO 8601).
            timezone: Timezone (e.g., Asia/Shanghai).
            meeting_platform: Platform (internal, zoom, teams, dingtalk, other).
            meeting_link: URL link to join.
            meeting_password: Password for the meeting.
            meeting_room: Physical meeting room.
            is_recorded: Whether to record.
            allow_screen_share: Whether screen sharing is allowed.
            notes: Meeting notes or agenda.
            schedule_event_ref: Optional linked schedule event.

        Returns:
            Meeting: The newly created meeting.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(organizer_employee_ref)

        valid_types = {"video", "audio", "in_person", "hybrid"}
        if meeting_type not in valid_types:
            raise ValueError(f"Invalid meeting_type: {meeting_type}. Must be one of {valid_types}")

        valid_platforms = {"internal", "zoom", "teams", "dingtalk", "other"}
        if meeting_platform not in valid_platforms:
            raise ValueError(f"Invalid meeting_platform: {meeting_platform}. Must be one of {valid_platforms}")

        if schedule_event_ref is not None:
            self._get_schedule_event(schedule_event_ref)

        now = self._now_iso()
        ref = self._generate_ref("MTG", self.db.meeting)

        meeting = Meeting(
            meeting_ref=ref,
            meeting_title=meeting_title,
            meeting_type=meeting_type,
            meeting_status="scheduled",
            organizer_employee_ref=organizer_employee_ref,
            schedule_event_ref=schedule_event_ref,
            start_time=start_time,
            end_time=end_time,
            timezone=timezone,
            meeting_platform=meeting_platform,
            meeting_link=meeting_link,
            meeting_password=meeting_password,
            meeting_room=meeting_room,
            is_recorded=is_recorded,
            recording_file_ref=None,
            allow_screen_share=allow_screen_share,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        self.db.meeting[ref] = meeting
        return meeting

    @is_tool(ToolType.WRITE)
    def update_meeting(
        self,
        meeting_ref: str,
        meeting_title: Optional[str] = None,
        meeting_type: Optional[str] = None,
        meeting_status: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        meeting_platform: Optional[str] = None,
        meeting_link: Optional[str] = None,
        meeting_password: Optional[str] = None,
        meeting_room: Optional[str] = None,
        is_recorded: Optional[bool] = None,
        allow_screen_share: Optional[bool] = None,
        notes: Optional[str] = None,
    ) -> Meeting:
        """
        Update an existing meeting. The agent must ask for explicit user confirmation before calling.

        Args:
            meeting_ref: Reference to the meeting.
            meeting_title: New title, or None to keep unchanged.
            meeting_type: New type, or None to keep unchanged.
            meeting_status: New status, or None to keep unchanged.
            start_time: New start time, or None to keep unchanged.
            end_time: New end time, or None to keep unchanged.
            meeting_platform: New platform, or None to keep unchanged.
            meeting_link: New link, or None to keep unchanged.
            meeting_password: New password, or None to keep unchanged.
            meeting_room: New room, or None to keep unchanged.
            is_recorded: New recording flag, or None to keep unchanged.
            allow_screen_share: New screen share flag, or None to keep unchanged.
            notes: New notes, or None to keep unchanged.

        Returns:
            Meeting: The updated meeting.

        Raises:
            ValueError: If the meeting is not found or inputs are invalid.
        """
        meeting = self._get_meeting(meeting_ref)

        if meeting_title is not None:
            meeting.meeting_title = meeting_title
        if meeting_type is not None:
            valid_types = {"video", "audio", "in_person", "hybrid"}
            if meeting_type not in valid_types:
                raise ValueError(f"Invalid meeting_type: {meeting_type}. Must be one of {valid_types}")
            meeting.meeting_type = meeting_type
        if meeting_status is not None:
            valid_statuses = {"scheduled", "in_progress", "completed", "cancelled"}
            if meeting_status not in valid_statuses:
                raise ValueError(f"Invalid meeting_status: {meeting_status}. Must be one of {valid_statuses}")
            meeting.meeting_status = meeting_status
        if start_time is not None:
            meeting.start_time = start_time
        if end_time is not None:
            meeting.end_time = end_time
        if meeting_platform is not None:
            valid_platforms = {"internal", "zoom", "teams", "dingtalk", "other"}
            if meeting_platform not in valid_platforms:
                raise ValueError(f"Invalid meeting_platform: {meeting_platform}. Must be one of {valid_platforms}")
            meeting.meeting_platform = meeting_platform
        if meeting_link is not None:
            meeting.meeting_link = meeting_link
        if meeting_password is not None:
            meeting.meeting_password = meeting_password
        if meeting_room is not None:
            meeting.meeting_room = meeting_room
        if is_recorded is not None:
            meeting.is_recorded = is_recorded
        if allow_screen_share is not None:
            meeting.allow_screen_share = allow_screen_share
        if notes is not None:
            meeting.notes = notes

        meeting.updated_at = self._now_iso()
        return meeting

    @is_tool(ToolType.WRITE)
    def add_meeting_participant(
        self,
        meeting_ref: str,
        employee_ref: str,
        participant_role: str = "attendee",
    ) -> MeetingParticipant:
        """
        Add a participant to a meeting. The agent must ask for explicit user confirmation before calling.

        Args:
            meeting_ref: Reference to the meeting.
            employee_ref: Reference to the employee to add.
            participant_role: Role (host, co_host, attendee, presenter).

        Returns:
            MeetingParticipant: The newly created participant record.

        Raises:
            ValueError: If the meeting or employee is not found, or inputs are invalid.
        """
        self._get_meeting(meeting_ref)
        self._get_employee(employee_ref)

        valid_roles = {"host", "co_host", "attendee", "presenter"}
        if participant_role not in valid_roles:
            raise ValueError(f"Invalid participant_role: {participant_role}. Must be one of {valid_roles}")

        # Check for duplicate
        for mp in self.db.meeting_participant.values():
            if mp.meeting_ref == meeting_ref and mp.employee_ref == employee_ref:
                raise ValueError("Employee is already a participant in this meeting")

        now = self._now_iso()
        ref = self._generate_ref("MP", self.db.meeting_participant)

        mp = MeetingParticipant(
            meeting_participant_ref=ref,
            meeting_ref=meeting_ref,
            employee_ref=employee_ref,
            participant_role=participant_role,
            join_time=None,
            leave_time=None,
            attendance_status="invited",
            created_at=now,
            updated_at=now,
        )
        self.db.meeting_participant[ref] = mp
        return mp

    @is_tool(ToolType.WRITE)
    def update_meeting_participant_attendance(
        self,
        meeting_participant_ref: str,
        attendance_status: str,
        join_time: Optional[str] = None,
        leave_time: Optional[str] = None,
    ) -> MeetingParticipant:
        """
        Update the attendance status of a meeting participant. The agent must ask for explicit user confirmation before calling.

        Args:
            meeting_participant_ref: Reference to the participant record.
            attendance_status: New status (invited, joined, absent, excused).
            join_time: Join time (ISO 8601), or None.
            leave_time: Leave time (ISO 8601), or None.

        Returns:
            MeetingParticipant: The updated participant record.

        Raises:
            ValueError: If the participant record is not found or status is invalid.
        """
        if meeting_participant_ref not in self.db.meeting_participant:
            raise ValueError("Meeting participant not found")

        valid_statuses = {"invited", "joined", "absent", "excused"}
        if attendance_status not in valid_statuses:
            raise ValueError(f"Invalid attendance_status: {attendance_status}. Must be one of {valid_statuses}")

        mp = self.db.meeting_participant[meeting_participant_ref]
        mp.attendance_status = attendance_status
        if join_time is not None:
            mp.join_time = join_time
        if leave_time is not None:
            mp.leave_time = leave_time
        mp.updated_at = self._now_iso()
        return mp

    # ========================================
    # OKR (周月报/OKR生成)
    # ========================================

    @is_tool(ToolType.READ)
    def get_okr_objective_details(self, okr_objective_ref: str) -> OkrObjective:
        """
        Retrieve the details of a specific OKR objective.

        Args:
            okr_objective_ref: Unique identifier for the OKR objective.

        Returns:
            OkrObjective: The OKR objective object.

        Raises:
            ValueError: If the OKR objective is not found.
        """
        return self._get_okr_objective(okr_objective_ref)

    @is_tool(ToolType.READ)
    def list_okr_objectives(
        self,
        owner_employee_ref: Optional[str] = None,
        okr_scope: Optional[str] = None,
        scope_ref: Optional[str] = None,
        period_label: Optional[str] = None,
        objective_status: Optional[str] = None,
    ) -> str:
        """
        List OKR objectives with optional filters.

        Args:
            owner_employee_ref: Optional filter by owner.
            okr_scope: Optional filter by scope (individual, team, department, company).
            scope_ref: Optional filter by scope reference.
            period_label: Optional filter by period label (e.g., 2025-Q1).
            objective_status: Optional filter by status.

        Returns:
            str: JSON array of OKR objective summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for obj in self.db.okr_objective.values():
            if owner_employee_ref is not None and obj.owner_employee_ref != owner_employee_ref:
                continue
            if okr_scope is not None and obj.okr_scope != okr_scope:
                continue
            if scope_ref is not None and obj.scope_ref != scope_ref:
                continue
            if period_label is not None and obj.period_label != period_label:
                continue
            if objective_status is not None and obj.objective_status != objective_status:
                continue
            results.append({
                "okr_objective_ref": obj.okr_objective_ref,
                "objective_title": obj.objective_title,
                "okr_scope": obj.okr_scope,
                "scope_ref": obj.scope_ref,
                "period_type": obj.period_type,
                "period_label": obj.period_label,
                "progress_percent": obj.progress_percent,
                "objective_status": obj.objective_status,
                "score": obj.score,
                "owner_employee_ref": obj.owner_employee_ref,
                "parent_objective_ref": obj.parent_objective_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_okr_key_results(self, okr_objective_ref: str) -> str:
        """
        List all key results for an OKR objective.

        Args:
            okr_objective_ref: Reference to the OKR objective.

        Returns:
            str: JSON array of key result summary objects.

        Raises:
            ValueError: If the OKR objective is not found.
        """
        self._get_okr_objective(okr_objective_ref)

        results = []
        for kr in self.db.okr_key_result.values():
            if kr.okr_objective_ref != okr_objective_ref:
                continue
            results.append({
                "okr_key_result_ref": kr.okr_key_result_ref,
                "key_result_title": kr.key_result_title,
                "description": kr.description,
                "metric_type": kr.metric_type,
                "target_value": kr.target_value,
                "current_value": kr.current_value,
                "start_value": kr.start_value,
                "unit": kr.unit,
                "progress_percent": kr.progress_percent,
                "key_result_status": kr.key_result_status,
                "owner_employee_ref": kr.owner_employee_ref,
                "score": kr.score,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_okr_key_result_details(self, okr_key_result_ref: str) -> OkrKeyResult:
        """
        Retrieve the details of a specific OKR key result.

        Args:
            okr_key_result_ref: Unique identifier for the OKR key result.

        Returns:
            OkrKeyResult: The OKR key result object.

        Raises:
            ValueError: If the OKR key result is not found.
        """
        return self._get_okr_key_result(okr_key_result_ref)

    @is_tool(ToolType.WRITE)
    def create_okr_objective(
        self,
        owner_employee_ref: str,
        objective_title: str,
        description: str,
        okr_scope: str,
        period_type: str,
        period_label: str,
        start_date: str,
        end_date: str,
        scope_ref: Optional[str] = None,
        parent_objective_ref: Optional[str] = None,
    ) -> OkrObjective:
        """
        Create a new OKR objective. The agent must ask for explicit user confirmation before calling.

        Args:
            owner_employee_ref: Employee reference of the owner.
            objective_title: Title of the objective.
            description: Description.
            okr_scope: Scope (individual, team, department, company).
            period_type: Period type (quarterly, semi_annual, annual, monthly).
            period_label: Period label (e.g., 2025-Q1).
            start_date: Start date (ISO 8601 date).
            end_date: End date (ISO 8601 date).
            scope_ref: Optional scope reference (team_ref or department_ref).
            parent_objective_ref: Optional parent objective reference.

        Returns:
            OkrObjective: The newly created OKR objective.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(owner_employee_ref)

        valid_scopes = {"individual", "team", "department", "company"}
        if okr_scope not in valid_scopes:
            raise ValueError(f"Invalid okr_scope: {okr_scope}. Must be one of {valid_scopes}")

        valid_periods = {"quarterly", "semi_annual", "annual", "monthly"}
        if period_type not in valid_periods:
            raise ValueError(f"Invalid period_type: {period_type}. Must be one of {valid_periods}")

        if parent_objective_ref is not None:
            self._get_okr_objective(parent_objective_ref)

        now = self._now_iso()
        ref = self._generate_ref("OKR", self.db.okr_objective)

        obj = OkrObjective(
            okr_objective_ref=ref,
            owner_employee_ref=owner_employee_ref,
            objective_title=objective_title,
            description=description,
            okr_scope=okr_scope,
            scope_ref=scope_ref,
            period_type=period_type,
            period_label=period_label,
            start_date=start_date,
            end_date=end_date,
            parent_objective_ref=parent_objective_ref,
            progress_percent=0,
            objective_status="draft",
            score=None,
            created_at=now,
            updated_at=now,
        )
        self.db.okr_objective[ref] = obj
        return obj

    @is_tool(ToolType.WRITE)
    def update_okr_objective(
        self,
        okr_objective_ref: str,
        objective_title: Optional[str] = None,
        description: Optional[str] = None,
        objective_status: Optional[str] = None,
        progress_percent: Optional[int] = None,
        score: Optional[float] = None,
    ) -> OkrObjective:
        """
        Update an existing OKR objective. The agent must ask for explicit user confirmation before calling.

        Args:
            okr_objective_ref: Reference to the OKR objective.
            objective_title: New title, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            objective_status: New status, or None to keep unchanged.
            progress_percent: New progress percentage, or None to keep unchanged.
            score: New score, or None to keep unchanged.

        Returns:
            OkrObjective: The updated OKR objective.

        Raises:
            ValueError: If the objective is not found or inputs are invalid.
        """
        obj = self._get_okr_objective(okr_objective_ref)

        if objective_title is not None:
            obj.objective_title = objective_title
        if description is not None:
            obj.description = description
        if objective_status is not None:
            valid_statuses = {"draft", "active", "completed", "cancelled", "deferred"}
            if objective_status not in valid_statuses:
                raise ValueError(f"Invalid objective_status: {objective_status}. Must be one of {valid_statuses}")
            obj.objective_status = objective_status
        if progress_percent is not None:
            if progress_percent < 0 or progress_percent > 100:
                raise ValueError("progress_percent must be between 0 and 100")
            obj.progress_percent = progress_percent
        if score is not None:
            obj.score = score

        obj.updated_at = self._now_iso()
        return obj

    @is_tool(ToolType.WRITE)
    def create_okr_key_result(
        self,
        okr_objective_ref: str,
        key_result_title: str,
        description: str,
        metric_type: str,
        target_value: float,
        start_value: float,
        unit: str,
        owner_employee_ref: str,
    ) -> OkrKeyResult:
        """
        Create a new key result under an OKR objective. The agent must ask for explicit user confirmation before calling.

        Args:
            okr_objective_ref: Reference to the parent OKR objective.
            key_result_title: Title of the key result.
            description: Description.
            metric_type: Metric type (percentage, number, currency, boolean, milestone).
            target_value: Target value.
            start_value: Starting value.
            unit: Unit of measurement.
            owner_employee_ref: Employee reference of the owner.

        Returns:
            OkrKeyResult: The newly created key result.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_okr_objective(okr_objective_ref)
        self._get_employee(owner_employee_ref)

        valid_metrics = {"percentage", "number", "currency", "boolean", "milestone"}
        if metric_type not in valid_metrics:
            raise ValueError(f"Invalid metric_type: {metric_type}. Must be one of {valid_metrics}")

        now = self._now_iso()
        ref = self._generate_ref("KR", self.db.okr_key_result)

        kr = OkrKeyResult(
            okr_key_result_ref=ref,
            okr_objective_ref=okr_objective_ref,
            key_result_title=key_result_title,
            description=description,
            metric_type=metric_type,
            target_value=target_value,
            current_value=start_value,
            start_value=start_value,
            unit=unit,
            progress_percent=0,
            key_result_status="active",
            owner_employee_ref=owner_employee_ref,
            score=None,
            created_at=now,
            updated_at=now,
        )
        self.db.okr_key_result[ref] = kr
        return kr

    @is_tool(ToolType.WRITE)
    def update_okr_key_result(
        self,
        okr_key_result_ref: str,
        key_result_title: Optional[str] = None,
        description: Optional[str] = None,
        current_value: Optional[float] = None,
        progress_percent: Optional[int] = None,
        key_result_status: Optional[str] = None,
        score: Optional[float] = None,
    ) -> OkrKeyResult:
        """
        Update an existing OKR key result. The agent must ask for explicit user confirmation before calling.

        Args:
            okr_key_result_ref: Reference to the key result.
            key_result_title: New title, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            current_value: New current value, or None to keep unchanged.
            progress_percent: New progress percentage, or None to keep unchanged.
            key_result_status: New status, or None to keep unchanged.
            score: New score, or None to keep unchanged.

        Returns:
            OkrKeyResult: The updated key result.

        Raises:
            ValueError: If the key result is not found or inputs are invalid.
        """
        kr = self._get_okr_key_result(okr_key_result_ref)

        if key_result_title is not None:
            kr.key_result_title = key_result_title
        if description is not None:
            kr.description = description
        if current_value is not None:
            kr.current_value = current_value
        if progress_percent is not None:
            if progress_percent < 0 or progress_percent > 100:
                raise ValueError("progress_percent must be between 0 and 100")
            kr.progress_percent = progress_percent
        if key_result_status is not None:
            valid_statuses = {"active", "completed", "cancelled", "at_risk"}
            if key_result_status not in valid_statuses:
                raise ValueError(f"Invalid key_result_status: {key_result_status}. Must be one of {valid_statuses}")
            kr.key_result_status = key_result_status
        if score is not None:
            kr.score = score

        kr.updated_at = self._now_iso()
        return kr

    # ========================================
    # Work Report (周月报/OKR生成)
    # ========================================

    @is_tool(ToolType.READ)
    def get_work_report_details(self, work_report_ref: str) -> WorkReport:
        """
        Retrieve the details of a specific work report.

        Args:
            work_report_ref: Unique identifier for the work report.

        Returns:
            WorkReport: The work report object.

        Raises:
            ValueError: If the work report is not found.
        """
        return self._get_work_report(work_report_ref)

    @is_tool(ToolType.READ)
    def list_work_reports(
        self,
        author_employee_ref: Optional[str] = None,
        report_type: Optional[str] = None,
        report_status: Optional[str] = None,
    ) -> str:
        """
        List work reports with optional filters.

        Args:
            author_employee_ref: Optional filter by author.
            report_type: Optional filter by type (daily, weekly, monthly, quarterly).
            report_status: Optional filter by status (draft, submitted, reviewed, returned).

        Returns:
            str: JSON array of work report summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for wr in self.db.work_report.values():
            if author_employee_ref is not None and wr.author_employee_ref != author_employee_ref:
                continue
            if report_type is not None and wr.report_type != report_type:
                continue
            if report_status is not None and wr.report_status != report_status:
                continue
            results.append({
                "work_report_ref": wr.work_report_ref,
                "report_title": wr.report_title,
                "report_type": wr.report_type,
                "report_status": wr.report_status,
                "author_employee_ref": wr.author_employee_ref,
                "period_start_date": wr.period_start_date,
                "period_end_date": wr.period_end_date,
                "submitted_at": wr.submitted_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_work_report(
        self,
        author_employee_ref: str,
        report_type: str,
        report_title: str,
        period_start_date: str,
        period_end_date: str,
        summary: str,
        accomplishments: str,
        issues_and_risks: str,
        next_period_plan: str,
        recipients: List[str],
        related_okr_objective_ref: Optional[str] = None,
        related_project_ref: Optional[str] = None,
    ) -> WorkReport:
        """
        Create a new work report. The agent must ask for explicit user confirmation before calling.

        Args:
            author_employee_ref: Employee reference of the author.
            report_type: Type (daily, weekly, monthly, quarterly).
            report_title: Title of the report.
            period_start_date: Start date of the reporting period (ISO 8601 date).
            period_end_date: End date of the reporting period (ISO 8601 date).
            summary: Summary of the report.
            accomplishments: Accomplishments during the period.
            issues_and_risks: Issues and risks encountered.
            next_period_plan: Plan for the next period.
            recipients: List of employee references who are recipients.
            related_okr_objective_ref: Optional OKR objective reference.
            related_project_ref: Optional project reference.

        Returns:
            WorkReport: The newly created work report.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(author_employee_ref)

        valid_types = {"daily", "weekly", "monthly", "quarterly"}
        if report_type not in valid_types:
            raise ValueError(f"Invalid report_type: {report_type}. Must be one of {valid_types}")

        for r in recipients:
            self._get_employee(r)

        if related_okr_objective_ref is not None:
            self._get_okr_objective(related_okr_objective_ref)
        if related_project_ref is not None:
            self._get_project(related_project_ref)

        now = self._now_iso()
        ref = self._generate_ref("WR", self.db.work_report)

        wr = WorkReport(
            work_report_ref=ref,
            author_employee_ref=author_employee_ref,
            report_type=report_type,
            report_title=report_title,
            period_start_date=period_start_date,
            period_end_date=period_end_date,
            summary=summary,
            accomplishments=accomplishments,
            issues_and_risks=issues_and_risks,
            next_period_plan=next_period_plan,
            report_status="draft",
            submitted_at=None,
            related_okr_objective_ref=related_okr_objective_ref,
            related_project_ref=related_project_ref,
            recipients=recipients,
            created_at=now,
            updated_at=now,
        )
        self.db.work_report[ref] = wr
        return wr

    @is_tool(ToolType.WRITE)
    def update_work_report(
        self,
        work_report_ref: str,
        report_title: Optional[str] = None,
        summary: Optional[str] = None,
        accomplishments: Optional[str] = None,
        issues_and_risks: Optional[str] = None,
        next_period_plan: Optional[str] = None,
        report_status: Optional[str] = None,
        recipients: Optional[List[str]] = None,
    ) -> WorkReport:
        """
        Update an existing work report. The agent must ask for explicit user confirmation before calling.

        Args:
            work_report_ref: Reference to the work report.
            report_title: New title, or None to keep unchanged.
            summary: New summary, or None to keep unchanged.
            accomplishments: New accomplishments, or None to keep unchanged.
            issues_and_risks: New issues and risks, or None to keep unchanged.
            next_period_plan: New plan, or None to keep unchanged.
            report_status: New status, or None to keep unchanged.
            recipients: New recipients list, or None to keep unchanged.

        Returns:
            WorkReport: The updated work report.

        Raises:
            ValueError: If the report is not found or inputs are invalid.
        """
        wr = self._get_work_report(work_report_ref)

        if report_title is not None:
            wr.report_title = report_title
        if summary is not None:
            wr.summary = summary
        if accomplishments is not None:
            wr.accomplishments = accomplishments
        if issues_and_risks is not None:
            wr.issues_and_risks = issues_and_risks
        if next_period_plan is not None:
            wr.next_period_plan = next_period_plan
        if report_status is not None:
            valid_statuses = {"draft", "submitted", "reviewed", "returned"}
            if report_status not in valid_statuses:
                raise ValueError(f"Invalid report_status: {report_status}. Must be one of {valid_statuses}")
            wr.report_status = report_status
            if report_status == "submitted":
                wr.submitted_at = self._now_iso()
        if recipients is not None:
            for r in recipients:
                self._get_employee(r)
            wr.recipients = recipients

        wr.updated_at = self._now_iso()
        return wr

    # ========================================
    # Document (项目文档查询 / 产品文档查询 / 个人文档查询)
    # ========================================

    @is_tool(ToolType.READ)
    def get_document_details(self, document_ref: str) -> Document:
        """
        Retrieve the details of a specific document.

        Args:
            document_ref: Unique identifier for the document.

        Returns:
            Document: The document object.

        Raises:
            ValueError: If the document is not found.
        """
        return self._get_document(document_ref)

    @is_tool(ToolType.READ)
    def list_documents(
        self,
        document_type: Optional[str] = None,
        document_category: Optional[str] = None,
        document_status: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
        scope_type: Optional[str] = None,
        scope_ref: Optional[str] = None,
        access_level: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> str:
        """
        List documents with optional filters.

        Args:
            document_type: Optional filter by document type.
            document_category: Optional filter by category.
            document_status: Optional filter by status.
            owner_employee_ref: Optional filter by owner.
            scope_type: Optional filter by scope type.
            scope_ref: Optional filter by scope reference.
            access_level: Optional filter by access level.
            tag: Optional filter by tag (partial match).

        Returns:
            str: JSON array of document summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for doc in self.db.document.values():
            if document_type is not None and doc.document_type != document_type:
                continue
            if document_category is not None and doc.document_category != document_category:
                continue
            if document_status is not None and doc.document_status != document_status:
                continue
            if owner_employee_ref is not None and doc.owner_employee_ref != owner_employee_ref:
                continue
            if scope_type is not None and doc.scope_type != scope_type:
                continue
            if scope_ref is not None and doc.scope_ref != scope_ref:
                continue
            if access_level is not None and doc.access_level != access_level:
                continue
            if tag is not None:
                tag_lower = tag.lower()
                if not any(tag_lower in t.lower() for t in doc.tags):
                    continue
            results.append({
                "document_ref": doc.document_ref,
                "document_title": doc.document_title,
                "document_type": doc.document_type,
                "document_category": doc.document_category,
                "document_status": doc.document_status,
                "version": doc.version,
                "owner_employee_ref": doc.owner_employee_ref,
                "scope_type": doc.scope_type,
                "scope_ref": doc.scope_ref,
                "access_level": doc.access_level,
                "tags": doc.tags,
                "view_count": doc.view_count,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def search_documents(
        self,
        keyword: str,
        document_type: Optional[str] = None,
        document_status: Optional[str] = None,
    ) -> str:
        """
        Search documents by keyword in title, description, or content.

        Args:
            keyword: Search keyword (case-insensitive).
            document_type: Optional filter by document type.
            document_status: Optional filter by document status.

        Returns:
            str: JSON array of matching document summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        search = keyword.lower()
        results = []
        for doc in self.db.document.values():
            if document_type is not None and doc.document_type != document_type:
                continue
            if document_status is not None and doc.document_status != document_status:
                continue
            if (search in doc.document_title.lower() or
                search in doc.description.lower() or
                search in doc.content.lower()):
                results.append({
                    "document_ref": doc.document_ref,
                    "document_title": doc.document_title,
                    "document_type": doc.document_type,
                    "document_category": doc.document_category,
                    "document_status": doc.document_status,
                    "version": doc.version,
                    "owner_employee_ref": doc.owner_employee_ref,
                    "scope_type": doc.scope_type,
                    "scope_ref": doc.scope_ref,
                    "access_level": doc.access_level,
                    "description": doc.description,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_document_collaborators(self, document_ref: str) -> str:
        """
        List all collaborators of a document.

        Args:
            document_ref: Reference to the document.

        Returns:
            str: JSON array of collaborator summary objects.

        Raises:
            ValueError: If the document is not found.
        """
        self._get_document(document_ref)

        results = []
        for dc in self.db.document_collaborator.values():
            if dc.document_ref != document_ref:
                continue
            emp = self._get_employee(dc.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "document_collaborator_ref": dc.document_collaborator_ref,
                "employee_ref": dc.employee_ref,
                "display_name": up.display_name,
                "collaborator_role": dc.collaborator_role,
                "granted_by_ref": dc.granted_by_ref,
                "granted_at": dc.granted_at,
                "status": dc.status,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def create_document(
        self,
        document_title: str,
        document_type: str,
        document_category: str,
        description: str,
        content: str,
        owner_employee_ref: str,
        scope_type: str,
        access_level: str = "internal",
        scope_ref: Optional[str] = None,
        parent_document_ref: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Document:
        """
        Create a new document. The agent must ask for explicit user confirmation before calling.

        Args:
            document_title: Title of the document.
            document_type: Type (project, team, department, personal, company, other).
            document_category: Category (technical_spec, design_doc, user_guide, api_doc, meeting_notes, policy, process, template, report, other).
            description: Description.
            content: Content body.
            owner_employee_ref: Employee reference of the owner.
            scope_type: Scope type.
            access_level: Access level (public, internal, restricted, confidential).
            scope_ref: Optional scope reference.
            parent_document_ref: Optional parent document reference.
            tags: Optional list of tags.

        Returns:
            Document: The newly created document.

        Raises:
            ValueError: If inputs are invalid or referenced entities not found.
        """
        self._get_employee(owner_employee_ref)

        valid_types = {"project", "team", "department", "personal", "company", "other"}
        if document_type not in valid_types:
            raise ValueError(f"Invalid document_type: {document_type}. Must be one of {valid_types}")

        valid_categories = {
            "technical_spec", "design_doc", "user_guide", "api_doc", "meeting_notes",
            "policy", "process", "template", "report", "other"
        }
        if document_category not in valid_categories:
            raise ValueError(f"Invalid document_category: {document_category}. Must be one of {valid_categories}")

        valid_access = {"public", "internal", "restricted", "confidential"}
        if access_level not in valid_access:
            raise ValueError(f"Invalid access_level: {access_level}. Must be one of {valid_access}")

        if parent_document_ref is not None:
            self._get_document(parent_document_ref)

        now = self._now_iso()
        ref = self._generate_ref("DOC", self.db.document)

        doc = Document(
            document_ref=ref,
            document_title=document_title,
            document_type=document_type,
            document_category=document_category,
            description=description,
            content=content,
            document_status="draft",
            version="1.0",
            owner_employee_ref=owner_employee_ref,
            scope_type=scope_type,
            scope_ref=scope_ref,
            parent_document_ref=parent_document_ref,
            file_attachment_ref=None,
            access_level=access_level,
            tags=tags or [],
            view_count=0,
            created_at=now,
            updated_at=now,
        )
        self.db.document[ref] = doc
        return doc

    @is_tool(ToolType.WRITE)
    def update_document(
        self,
        document_ref: str,
        document_title: Optional[str] = None,
        description: Optional[str] = None,
        content: Optional[str] = None,
        document_status: Optional[str] = None,
        version: Optional[str] = None,
        access_level: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Document:
        """
        Update an existing document. The agent must ask for explicit user confirmation before calling.

        Args:
            document_ref: Reference to the document.
            document_title: New title, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            content: New content, or None to keep unchanged.
            document_status: New status, or None to keep unchanged.
            version: New version, or None to keep unchanged.
            access_level: New access level, or None to keep unchanged.
            tags: New tags list, or None to keep unchanged.

        Returns:
            Document: The updated document.

        Raises:
            ValueError: If the document is not found or inputs are invalid.
        """
        doc = self._get_document(document_ref)

        if document_title is not None:
            doc.document_title = document_title
        if description is not None:
            doc.description = description
        if content is not None:
            doc.content = content
        if document_status is not None:
            valid_statuses = {"draft", "in_review", "published", "archived", "deprecated"}
            if document_status not in valid_statuses:
                raise ValueError(f"Invalid document_status: {document_status}. Must be one of {valid_statuses}")
            doc.document_status = document_status
        if version is not None:
            doc.version = version
        if access_level is not None:
            valid_access = {"public", "internal", "restricted", "confidential"}
            if access_level not in valid_access:
                raise ValueError(f"Invalid access_level: {access_level}. Must be one of {valid_access}")
            doc.access_level = access_level
        if tags is not None:
            doc.tags = tags

        doc.updated_at = self._now_iso()
        return doc

    @is_tool(ToolType.WRITE)
    def add_document_collaborator(
        self,
        document_ref: str,
        employee_ref: str,
        collaborator_role: str,
        granted_by_ref: str,
    ) -> DocumentCollaborator:
        """
        Add a collaborator to a document. The agent must ask for explicit user confirmation before calling.

        Args:
            document_ref: Reference to the document.
            employee_ref: Reference to the employee to add.
            collaborator_role: Role (owner, editor, commenter, viewer).
            granted_by_ref: Employee reference of the person granting access.

        Returns:
            DocumentCollaborator: The newly created collaborator record.

        Raises:
            ValueError: If the document or employee is not found, or inputs are invalid.
        """
        self._get_document(document_ref)
        self._get_employee(employee_ref)
        self._get_employee(granted_by_ref)

        valid_roles = {"owner", "editor", "commenter", "viewer"}
        if collaborator_role not in valid_roles:
            raise ValueError(f"Invalid collaborator_role: {collaborator_role}. Must be one of {valid_roles}")

        # Check for existing active collaborator
        for dc in self.db.document_collaborator.values():
            if dc.document_ref == document_ref and dc.employee_ref == employee_ref and dc.status == "active":
                raise ValueError("Employee is already an active collaborator on this document")

        now = self._now_iso()
        ref = self._generate_ref("DC", self.db.document_collaborator)

        dc = DocumentCollaborator(
            document_collaborator_ref=ref,
            document_ref=document_ref,
            employee_ref=employee_ref,
            collaborator_role=collaborator_role,
            granted_by_ref=granted_by_ref,
            granted_at=now,
            status="active",
            created_at=now,
            updated_at=now,
        )
        self.db.document_collaborator[ref] = dc
        return dc

    @is_tool(ToolType.WRITE)
    def revoke_document_collaborator(self, document_collaborator_ref: str) -> DocumentCollaborator:
        """
        Revoke a collaborator's access to a document. The agent must ask for explicit user confirmation before calling.

        Args:
            document_collaborator_ref: Reference to the collaborator record.

        Returns:
            DocumentCollaborator: The updated collaborator record.

        Raises:
            ValueError: If the collaborator record is not found or already revoked.
        """
        if document_collaborator_ref not in self.db.document_collaborator:
            raise ValueError("Document collaborator not found")

        dc = self.db.document_collaborator[document_collaborator_ref]
        if dc.status == "revoked":
            raise ValueError("Document collaborator is already revoked")

        dc.status = "revoked"
        dc.updated_at = self._now_iso()
        return dc

    # ========================================
    # Product Requirement (产品需求修改与调整 / 产品需求作废与关闭)
    # ========================================

    @is_tool(ToolType.READ)
    def get_product_requirement_details(self, product_requirement_ref: str) -> ProductRequirement:
        """
        Retrieve the details of a specific product requirement.

        Args:
            product_requirement_ref: Unique identifier for the product requirement.

        Returns:
            ProductRequirement: The product requirement object.

        Raises:
            ValueError: If the product requirement is not found.
        """
        return self._get_product_requirement(product_requirement_ref)

    @is_tool(ToolType.READ)
    def list_product_requirements(
        self,
        requirement_type: Optional[str] = None,
        requirement_status: Optional[str] = None,
        priority: Optional[str] = None,
        owner_employee_ref: Optional[str] = None,
        project_ref: Optional[str] = None,
        software_product_ref: Optional[str] = None,
    ) -> str:
        """
        List product requirements with optional filters.

        Args:
            requirement_type: Optional filter by type.
            requirement_status: Optional filter by status.
            priority: Optional filter by priority.
            owner_employee_ref: Optional filter by owner.
            project_ref: Optional filter by project.
            software_product_ref: Optional filter by software product.

        Returns:
            str: JSON array of requirement summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for pr in self.db.product_requirement.values():
            if requirement_type is not None and pr.requirement_type != requirement_type:
                continue
            if requirement_status is not None and pr.requirement_status != requirement_status:
                continue
            if priority is not None and pr.priority != priority:
                continue
            if owner_employee_ref is not None and pr.owner_employee_ref != owner_employee_ref:
                continue
            if project_ref is not None and pr.project_ref != project_ref:
                continue
            if software_product_ref is not None and pr.software_product_ref != software_product_ref:
                continue
            results.append({
                "product_requirement_ref": pr.product_requirement_ref,
                "requirement_title": pr.requirement_title,
                "requirement_code": pr.requirement_code,
                "requirement_type": pr.requirement_type,
                "requirement_status": pr.requirement_status,
                "priority": pr.priority,
                "owner_employee_ref": pr.owner_employee_ref,
                "project_ref": pr.project_ref,
                "software_product_ref": pr.software_product_ref,
                "target_version": pr.target_version,
                "planned_release_date": pr.planned_release_date,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_product_requirement_ref_by_code(self, requirement_code: str) -> str:
        """
        Find a product requirement reference by its code.

        Args:
            requirement_code: The requirement code to search for (e.g., PRD-2025-0001).

        Returns:
            str: The product requirement reference.

        Raises:
            ValueError: If no matching requirement is found.
        """
        for pr_ref, pr in self.db.product_requirement.items():
            if pr.requirement_code == requirement_code:
                return pr_ref
        raise ValueError("Product requirement not found")

    @is_tool(ToolType.WRITE)
    def update_product_requirement(
        self,
        product_requirement_ref: str,
        requirement_title: Optional[str] = None,
        description: Optional[str] = None,
        requirement_type: Optional[str] = None,
        requirement_status: Optional[str] = None,
        priority: Optional[str] = None,
        business_value: Optional[str] = None,
        acceptance_criteria: Optional[str] = None,
        target_version: Optional[str] = None,
        planned_release_date: Optional[str] = None,
        impact_analysis: Optional[str] = None,
        change_reason: Optional[str] = None,
    ) -> ProductRequirement:
        """
        Update an existing product requirement. The agent must ask for explicit user confirmation before calling.

        Args:
            product_requirement_ref: Reference to the requirement.
            requirement_title: New title, or None to keep unchanged.
            description: New description, or None to keep unchanged.
            requirement_type: New type, or None to keep unchanged.
            requirement_status: New status, or None to keep unchanged.
            priority: New priority, or None to keep unchanged.
            business_value: New business value, or None to keep unchanged.
            acceptance_criteria: New acceptance criteria, or None to keep unchanged.
            target_version: New target version, or None to keep unchanged.
            planned_release_date: New planned release date, or None to keep unchanged.
            impact_analysis: New impact analysis, or None to keep unchanged.
            change_reason: Reason for the change.

        Returns:
            ProductRequirement: The updated product requirement.

        Raises:
            ValueError: If the requirement is not found or inputs are invalid.
        """
        pr = self._get_product_requirement(product_requirement_ref)

        if requirement_title is not None:
            pr.requirement_title = requirement_title
        if description is not None:
            pr.description = description
        if requirement_type is not None:
            valid_types = {"feature", "enhancement", "bugfix", "technical_debt", "compliance", "other"}
            if requirement_type not in valid_types:
                raise ValueError(f"Invalid requirement_type: {requirement_type}. Must be one of {valid_types}")
            pr.requirement_type = requirement_type
        if requirement_status is not None:
            valid_statuses = {"draft", "under_review", "approved", "in_progress", "completed", "voided", "deferred"}
            if requirement_status not in valid_statuses:
                raise ValueError(f"Invalid requirement_status: {requirement_status}. Must be one of {valid_statuses}")
            pr.requirement_status = requirement_status
        if priority is not None:
            valid_priorities = {"critical", "high", "medium", "low"}
            if priority not in valid_priorities:
                raise ValueError(f"Invalid priority: {priority}. Must be one of {valid_priorities}")
            pr.priority = priority
        if business_value is not None:
            pr.business_value = business_value
        if acceptance_criteria is not None:
            pr.acceptance_criteria = acceptance_criteria
        if target_version is not None:
            pr.target_version = target_version
        if planned_release_date is not None:
            pr.planned_release_date = planned_release_date
        if impact_analysis is not None:
            pr.impact_analysis = impact_analysis
        if change_reason is not None:
            pr.change_reason = change_reason

        pr.updated_at = self._now_iso()
        return pr

    @is_tool(ToolType.WRITE)
    def void_product_requirement(
        self,
        product_requirement_ref: str,
        change_reason: str,
    ) -> ProductRequirement:
        """
        Void (作废) a product requirement. The agent must ask for explicit user confirmation before calling.

        Args:
            product_requirement_ref: Reference to the requirement.
            change_reason: Reason for voiding.

        Returns:
            ProductRequirement: The voided product requirement.

        Raises:
            ValueError: If the requirement is not found or already voided/completed.
        """
        pr = self._get_product_requirement(product_requirement_ref)

        if pr.requirement_status in ("voided", "completed"):
            raise ValueError(f"Product requirement is already {pr.requirement_status}")

        now = self._now_iso()
        pr.requirement_status = "voided"
        pr.voided_at = now
        pr.change_reason = change_reason
        pr.updated_at = now
        return pr

    @is_tool(ToolType.WRITE)
    def close_product_requirement(
        self,
        product_requirement_ref: str,
    ) -> ProductRequirement:
        """
        Close (关闭) a completed product requirement. The agent must ask for explicit user confirmation before calling.

        Args:
            product_requirement_ref: Reference to the requirement.

        Returns:
            ProductRequirement: The closed product requirement.

        Raises:
            ValueError: If the requirement is not found or not in a closable state.
        """
        pr = self._get_product_requirement(product_requirement_ref)

        if pr.requirement_status in ("voided", "completed"):
            raise ValueError(f"Product requirement is already {pr.requirement_status}")

        now = self._now_iso()
        pr.requirement_status = "completed"
        pr.closed_at = now
        pr.updated_at = now
        return pr

    # ========================================
    # Software Product (产品软件入口查询 / 产品软件基本介绍 / 具体产品问题咨询)
    # ========================================

    @is_tool(ToolType.READ)
    def get_software_product_details(self, software_product_ref: str) -> SoftwareProduct:
        """
        Retrieve the details of a specific software product.

        Args:
            software_product_ref: Unique identifier for the software product.

        Returns:
            SoftwareProduct: The software product object.

        Raises:
            ValueError: If the software product is not found.
        """
        return self._get_software_product(software_product_ref)

    @is_tool(ToolType.READ)
    def list_software_products(
        self,
        product_type: Optional[str] = None,
        product_status: Optional[str] = None,
        platform: Optional[str] = None,
    ) -> str:
        """
        List software products with optional filters.

        Args:
            product_type: Optional filter by type (internal, external, platform, library, service).
            product_status: Optional filter by status (active, deprecated, retired, planning).
            platform: Optional filter by platform (web, mobile, desktop, api, cross_platform).

        Returns:
            str: JSON array of software product summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for sp in self.db.software_product.values():
            if product_type is not None and sp.product_type != product_type:
                continue
            if product_status is not None and sp.product_status != product_status:
                continue
            if platform is not None and sp.platform != platform:
                continue
            results.append({
                "software_product_ref": sp.software_product_ref,
                "product_name": sp.product_name,
                "product_code": sp.product_code,
                "product_type": sp.product_type,
                "product_status": sp.product_status,
                "current_version": sp.current_version,
                "access_url": sp.access_url,
                "documentation_url": sp.documentation_url,
                "platform": sp.platform,
                "owner_employee_ref": sp.owner_employee_ref,
                "support_contact": sp.support_contact,
                "features_summary": sp.features_summary,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def find_software_product_ref_by_name(self, product_name: str) -> str:
        """
        Find a software product reference by its name (partial match, case-insensitive).

        Args:
            product_name: The product name to search for.

        Returns:
            str: The software product reference.

        Raises:
            ValueError: If no matching product is found.
        """
        search = product_name.lower()
        for sp_ref, sp in self.db.software_product.items():
            if search in sp.product_name.lower():
                return sp_ref
        raise ValueError("Software product not found")

    # ========================================
    # Certification & Exam (认证与考试)
    # ========================================

    @is_tool(ToolType.READ)
    def get_certification_details(self, certification_ref: str) -> Certification:
        """
        Retrieve the details of a specific certification.

        Args:
            certification_ref: Unique identifier for the certification.

        Returns:
            Certification: The certification object.

        Raises:
            ValueError: If the certification is not found.
        """
        return self._get_certification(certification_ref)

    @is_tool(ToolType.READ)
    def list_certifications(
        self,
        certification_type: Optional[str] = None,
        certification_status: Optional[str] = None,
        related_job_family: Optional[str] = None,
    ) -> str:
        """
        List certifications with optional filters.

        Args:
            certification_type: Optional filter by type (professional, technical, compliance, safety, language, other).
            certification_status: Optional filter by status (active, deprecated, retired).
            related_job_family: Optional filter by related job family.

        Returns:
            str: JSON array of certification summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for cert in self.db.certification.values():
            if certification_type is not None and cert.certification_type != certification_type:
                continue
            if certification_status is not None and cert.certification_status != certification_status:
                continue
            if related_job_family is not None and cert.related_job_family != related_job_family:
                continue
            results.append({
                "certification_ref": cert.certification_ref,
                "certification_name": cert.certification_name,
                "certification_code": cert.certification_code,
                "issuing_authority": cert.issuing_authority,
                "certification_type": cert.certification_type,
                "validity_period_months": cert.validity_period_months,
                "exam_required": cert.exam_required,
                "training_required": cert.training_required,
                "certification_status": cert.certification_status,
                "related_job_family": cert.related_job_family,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_employee_certifications(
        self,
        employee_ref: str,
        certification_status: Optional[str] = None,
    ) -> str:
        """
        List all certifications held by an employee.

        Args:
            employee_ref: Reference to the employee.
            certification_status: Optional filter by status (active, expired, revoked, pending).

        Returns:
            str: JSON array of employee certification summary objects.

        Raises:
            ValueError: If the employee is not found.
        """
        self._get_employee(employee_ref)

        results = []
        for ec in self.db.employee_certification.values():
            if ec.employee_ref != employee_ref:
                continue
            if certification_status is not None and ec.certification_status != certification_status:
                continue
            cert = self._get_certification(ec.certification_ref)
            results.append({
                "employee_certification_ref": ec.employee_certification_ref,
                "certification_ref": ec.certification_ref,
                "certification_name": cert.certification_name,
                "certificate_number": ec.certificate_number,
                "obtained_date": ec.obtained_date,
                "expiry_date": ec.expiry_date,
                "certification_status": ec.certification_status,
                "score": ec.score,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_employee_certification_details(self, employee_certification_ref: str) -> str:
        """
        Retrieve the details of a specific employee certification.

        Args:
            employee_certification_ref: Unique identifier for the employee certification.

        Returns:
            str: JSON object with employee certification details and certification info.

        Raises:
            ValueError: If the employee certification is not found.
        """
        if employee_certification_ref not in self.db.employee_certification:
            raise ValueError("Employee certification not found")

        ec = self.db.employee_certification[employee_certification_ref]
        cert = self._get_certification(ec.certification_ref)

        result = {
            "employee_certification_ref": ec.employee_certification_ref,
            "employee_ref": ec.employee_ref,
            "certification_ref": ec.certification_ref,
            "certification_name": cert.certification_name,
            "certificate_number": ec.certificate_number,
            "obtained_date": ec.obtained_date,
            "expiry_date": ec.expiry_date,
            "certification_status": ec.certification_status,
            "score": ec.score,
            "certificate_file_ref": ec.certificate_file_ref,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def get_exam_schedule_details(self, exam_schedule_ref: str) -> ExamSchedule:
        """
        Retrieve the details of a specific exam schedule.

        Args:
            exam_schedule_ref: Unique identifier for the exam schedule.

        Returns:
            ExamSchedule: The exam schedule object.

        Raises:
            ValueError: If the exam schedule is not found.
        """
        return self._get_exam_schedule(exam_schedule_ref)

    @is_tool(ToolType.READ)
    def list_exam_schedules(
        self,
        certification_ref: Optional[str] = None,
        exam_status: Optional[str] = None,
    ) -> str:
        """
        List exam schedules with optional filters.

        Args:
            certification_ref: Optional filter by certification reference.
            exam_status: Optional filter by status (open, closed, completed, cancelled).

        Returns:
            str: JSON array of exam schedule summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for es in self.db.exam_schedule.values():
            if certification_ref is not None and es.certification_ref != certification_ref:
                continue
            if exam_status is not None and es.exam_status != exam_status:
                continue
            results.append({
                "exam_schedule_ref": es.exam_schedule_ref,
                "certification_ref": es.certification_ref,
                "exam_name": es.exam_name,
                "exam_date": es.exam_date,
                "registration_deadline": es.registration_deadline,
                "location": es.location,
                "capacity": es.capacity,
                "exam_status": es.exam_status,
                "description": es.description,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_exam_registrations(
        self,
        exam_schedule_ref: Optional[str] = None,
        employee_ref: Optional[str] = None,
        registration_status: Optional[str] = None,
    ) -> str:
        """
        List exam registrations with optional filters.

        Args:
            exam_schedule_ref: Optional filter by exam schedule.
            employee_ref: Optional filter by employee.
            registration_status: Optional filter by status (registered, cancelled, completed, no_show).

        Returns:
            str: JSON array of exam registration summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for er in self.db.exam_registration.values():
            if exam_schedule_ref is not None and er.exam_schedule_ref != exam_schedule_ref:
                continue
            if employee_ref is not None and er.employee_ref != employee_ref:
                continue
            if registration_status is not None and er.registration_status != registration_status:
                continue
            results.append({
                "exam_registration_ref": er.exam_registration_ref,
                "exam_schedule_ref": er.exam_schedule_ref,
                "employee_ref": er.employee_ref,
                "registration_status": er.registration_status,
                "exam_result": er.exam_result,
                "score": er.score,
                "registered_at": er.registered_at,
                "completed_at": er.completed_at,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def register_for_exam(
        self,
        exam_schedule_ref: str,
        employee_ref: str,
    ) -> ExamRegistration:
        """
        Register an employee for an exam. The agent must ask for explicit user confirmation before calling.

        Args:
            exam_schedule_ref: Reference to the exam schedule.
            employee_ref: Reference to the employee.

        Returns:
            ExamRegistration: The newly created exam registration.

        Raises:
            ValueError: If the exam or employee is not found, exam is not open, or already registered.
        """
        es = self._get_exam_schedule(exam_schedule_ref)
        self._get_employee(employee_ref)

        if es.exam_status != "open":
            raise ValueError(f"Exam is not open for registration, current status: {es.exam_status}")

        # Check current registrations count
        current_count = sum(
            1 for er in self.db.exam_registration.values()
            if er.exam_schedule_ref == exam_schedule_ref and er.registration_status == "registered"
        )
        if current_count >= es.capacity:
            raise ValueError("Exam has reached its capacity")

        # Check for duplicate registration
        for er in self.db.exam_registration.values():
            if (er.exam_schedule_ref == exam_schedule_ref and
                er.employee_ref == employee_ref and
                er.registration_status == "registered"):
                raise ValueError("Employee is already registered for this exam")

        now = self._now_iso()
        ref = self._generate_ref("ER", self.db.exam_registration)

        registration = ExamRegistration(
            exam_registration_ref=ref,
            exam_schedule_ref=exam_schedule_ref,
            employee_ref=employee_ref,
            registration_status="registered",
            exam_result=None,
            score=None,
            registered_at=now,
            completed_at=None,
            created_at=now,
            updated_at=now,
        )
        self.db.exam_registration[ref] = registration
        return registration

    @is_tool(ToolType.WRITE)
    def cancel_exam_registration(self, exam_registration_ref: str) -> ExamRegistration:
        """
        Cancel an exam registration. The agent must ask for explicit user confirmation before calling.

        Args:
            exam_registration_ref: Reference to the exam registration.

        Returns:
            ExamRegistration: The updated exam registration.

        Raises:
            ValueError: If the registration is not found or not in registered status.
        """
        if exam_registration_ref not in self.db.exam_registration:
            raise ValueError("Exam registration not found")

        er = self.db.exam_registration[exam_registration_ref]
        if er.registration_status != "registered":
            raise ValueError(f"Exam registration is not in registered status, current status: {er.registration_status}")

        er.registration_status = "cancelled"
        er.updated_at = self._now_iso()
        return er

    @is_tool(ToolType.WRITE)
    def update_exam_registration_result(
        self,
        exam_registration_ref: str,
        exam_result: str,
        score: Optional[float] = None,
    ) -> ExamRegistration:
        """
        Update the result of an exam registration. The agent must ask for explicit user confirmation before calling.

        Args:
            exam_registration_ref: Reference to the exam registration.
            exam_result: Result (pass, fail, pending).
            score: Score achieved, or None.

        Returns:
            ExamRegistration: The updated exam registration.

        Raises:
            ValueError: If the registration is not found or inputs are invalid.
        """
        if exam_registration_ref not in self.db.exam_registration:
            raise ValueError("Exam registration not found")

        valid_results = {"pass", "fail", "pending"}
        if exam_result not in valid_results:
            raise ValueError(f"Invalid exam_result: {exam_result}. Must be one of {valid_results}")

        er = self.db.exam_registration[exam_registration_ref]
        er.exam_result = exam_result
        if score is not None:
            er.score = score
        if exam_result in ("pass", "fail"):
            er.registration_status = "completed"
            er.completed_at = self._now_iso()
        er.updated_at = self._now_iso()
        return er

    # ========================================
    # Manager Snapshot (管理者快照)
    # ========================================

    @is_tool(ToolType.READ)
    def get_manager_snapshot_details(self, manager_snapshot_ref: str) -> ManagerSnapshot:
        """
        Retrieve the details of a specific manager snapshot.

        Args:
            manager_snapshot_ref: Unique identifier for the manager snapshot.

        Returns:
            ManagerSnapshot: The manager snapshot object.

        Raises:
            ValueError: If the manager snapshot is not found.
        """
        return self._get_manager_snapshot(manager_snapshot_ref)

    @is_tool(ToolType.READ)
    def list_manager_snapshots(
        self,
        manager_employee_ref: Optional[str] = None,
        snapshot_type: Optional[str] = None,
        department_ref: Optional[str] = None,
        snapshot_date: Optional[str] = None,
    ) -> str:
        """
        List manager snapshots with optional filters.

        Args:
            manager_employee_ref: Optional filter by manager.
            snapshot_type: Optional filter by type (daily, weekly, monthly).
            department_ref: Optional filter by department.
            snapshot_date: Optional filter by snapshot date.

        Returns:
            str: JSON array of manager snapshot summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for ms in self.db.manager_snapshot.values():
            if manager_employee_ref is not None and ms.manager_employee_ref != manager_employee_ref:
                continue
            if snapshot_type is not None and ms.snapshot_type != snapshot_type:
                continue
            if department_ref is not None and ms.department_ref != department_ref:
                continue
            if snapshot_date is not None and ms.snapshot_date != snapshot_date:
                continue
            results.append({
                "manager_snapshot_ref": ms.manager_snapshot_ref,
                "manager_employee_ref": ms.manager_employee_ref,
                "snapshot_date": ms.snapshot_date,
                "snapshot_type": ms.snapshot_type,
                "department_ref": ms.department_ref,
                "team_headcount": ms.team_headcount,
                "active_projects_count": ms.active_projects_count,
                "overdue_tasks_count": ms.overdue_tasks_count,
                "pending_approvals_count": ms.pending_approvals_count,
                "open_risks_count": ms.open_risks_count,
                "avg_okr_progress_percent": ms.avg_okr_progress_percent,
                "upcoming_milestones_count": ms.upcoming_milestones_count,
                "on_leave_count": ms.on_leave_count,
                "remote_work_count": ms.remote_work_count,
                "snapshot_data": ms.snapshot_data,
            })
        results.sort(key=lambda x: x["snapshot_date"], reverse=True)
        return json.dumps(results)

    # ========================================
    # Company Info (公司基本信息查询)
    # ========================================

    @is_tool(ToolType.READ)
    def get_company_info(self, info_key: str) -> str:
        """
        Retrieve a company info entry by its key.

        Args:
            info_key: The information key (e.g., company_name, legal_entity, tax_id).

        Returns:
            str: JSON object with the company info details.

        Raises:
            ValueError: If the company info key is not found.
        """
        for ci in self.db.company_info.values():
            if ci.info_key == info_key:
                return json.dumps({
                    "company_info_ref": ci.company_info_ref,
                    "info_key": ci.info_key,
                    "info_value": ci.info_value,
                    "info_type": ci.info_type,
                    "info_category": ci.info_category,
                    "description": ci.description,
                    "is_public": ci.is_public,
                })
        raise ValueError("Company info not found")

    @is_tool(ToolType.READ)
    def list_company_info(
        self,
        info_category: Optional[str] = None,
        is_public: Optional[bool] = None,
    ) -> str:
        """
        List company information entries with optional filters.

        Args:
            info_category: Optional filter by category (basic, contact, legal, financial, branding, other).
            is_public: Optional filter by public visibility.

        Returns:
            str: JSON array of company info summary objects.

        Raises:
            ValueError: If any referenced data is invalid.
        """
        results = []
        for ci in self.db.company_info.values():
            if info_category is not None and ci.info_category != info_category:
                continue
            if is_public is not None and ci.is_public != is_public:
                continue
            results.append({
                "company_info_ref": ci.company_info_ref,
                "info_key": ci.info_key,
                "info_value": ci.info_value,
                "info_type": ci.info_type,
                "info_category": ci.info_category,
                "description": ci.description,
                "is_public": ci.is_public,
            })
        return json.dumps(results)