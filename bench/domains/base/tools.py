"""Toolkit for the office collaboration domain."""
from typing import Dict, List, Optional
import json
from datetime import datetime, timezone

from bench.environment.toolkit import ToolKitBase, ToolType, is_tool
from bench.domains.base.models import (
    Department,
    DepartmentMember,
    Employee,
    EmployeeRole,
    Mentorship,
    Notification,
    OrgConfig,
    Permission,
    Position,
    Role,
    RolePermission,
    Team,
    TeamMember,
    UserProfile,
    OfficeDB,
)


class OfficeTools(ToolKitBase):
    """Frequently-used tools for the office collaboration domain."""

    db: OfficeDB

    def __init__(self, db: OfficeDB) -> None:
        """
        功能说明（Description）：
            初始化对象并绑定所需依赖。
        参数（Parameters）：
            - `db` (OfficeDB): 数据库对象实例；为空时通常会走默认加载逻辑。
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
    def _get_employee(self, employee_ref: str) -> Employee:
        """
        功能说明（Description）：
            获取员工，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Employee`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if employee_ref not in self.db.employee:
            raise ValueError("Employee not found")
        return self.db.employee[employee_ref]

    def _get_user_profile(self, user_profile_ref: str) -> UserProfile:
        """
        功能说明（Description）：
            获取userprofile，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `user_profile_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `UserProfile`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if user_profile_ref not in self.db.user_profile:
            raise ValueError("User profile not found")
        return self.db.user_profile[user_profile_ref]

    def _get_user_profile_for_employee(self, employee_ref: str) -> UserProfile:
        """
        功能说明（Description）：
            获取userprofilefor员工，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `UserProfile`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)
        return self._get_user_profile(emp.user_profile_ref)

    def _get_department(self, department_ref: str) -> Department:
        """
        功能说明（Description）：
            获取部门，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Department`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if department_ref not in self.db.department:
            raise ValueError("Department not found")
        return self.db.department[department_ref]

    def _get_position(self, position_ref: str) -> Position:
        """
        功能说明（Description）：
            获取position，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `position_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Position`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if position_ref not in self.db.position:
            raise ValueError("Position not found")
        return self.db.position[position_ref]

    def _get_team(self, team_ref: str) -> Team:
        """
        功能说明（Description）：
            获取团队，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `team_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Team`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if team_ref not in self.db.team:
            raise ValueError("Team not found")
        return self.db.team[team_ref]

    def _get_role(self, role_ref: str) -> Role:
        """
        功能说明（Description）：
            获取角色，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `role_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Role`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if role_ref not in self.db.role:
            raise ValueError("Role not found")
        return self.db.role[role_ref]

    def _get_notification(self, notification_ref: str) -> Notification:
        """
        功能说明（Description）：
            获取通知，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `notification_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Notification`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if notification_ref not in self.db.notification:
            raise ValueError("Notification not found")
        return self.db.notification[notification_ref]

    def _get_employee_ref_for_user_profile(self, user_profile_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工refforuserprofile，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `user_profile_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        for emp_ref, emp in self.db.employee.items():
            if emp.user_profile_ref == user_profile_ref:
                return emp_ref
        raise ValueError("Employee not found for user profile")

    def _get_descendant_department_refs(self, department_ref: str) -> List[str]:
        """
        功能说明（Description）：
            获取descendant部门refs，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `List[str]`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        descendants = []
        queue = [department_ref]
        while queue:
            current = queue.pop(0)
            for dept_ref, dept in self.db.department.items():
                if dept.parent_department_ref == current and dept_ref not in descendants:
                    descendants.append(dept_ref)
                    queue.append(dept_ref)
        return descendants

    def _generate_ref(self, prefix: str, collection: Dict) -> str:
        """
        功能说明（Description）：
            处理ref，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `prefix` (str): 业务入参，按函数语义传入。
            - `collection` (Dict): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        idx = len(collection) + 1
        while True:
            ref = f"{prefix}-{idx:05d}"
            if ref not in collection:
                return ref
            idx += 1

    def _now_iso(self) -> str:
        """
        功能说明（Description）：
            处理iso，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return datetime.now(timezone.utc).isoformat()

    # -------------
    # Generic tools
    # -------------
    @is_tool(ToolType.GENERIC)
    def calculate(self, expression: str) -> str:
        """
        功能说明（Description）：
            计算calculate，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `expression` (str): 待执行的表达式内容。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if not all(char in "0123456789+-*/(). " for char in expression):
            raise ValueError("Invalid characters in expression")
        return str(round(float(eval(expression, {"__builtins__": None}, {})), 2))

    @is_tool(ToolType.GENERIC)
    def transfer_to_human_agents(self, summary: str) -> str:
        """
        功能说明（Description）：
            转交tohumanagents，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `summary` (str): 文本说明字段，用于补充业务上下文。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return "Transfer successful"

    # ----------------
    # Lookup helpers (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def find_employee_ref_by_name(self, display_name: str) -> str:
        """
        功能说明（Description）：
            查找员工refbyname，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `display_name` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        search = display_name.lower()
        for emp_ref, emp in self.db.employee.items():
            up = self._get_user_profile(emp.user_profile_ref)
            if search in up.display_name.lower():
                return emp_ref
        raise ValueError("Employee not found")

    @is_tool(ToolType.READ)
    def find_department_ref_by_name(self, department_name: str) -> str:
        """
        功能说明（Description）：
            查找部门refbyname，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `department_name` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        search = department_name.lower()
        for dept_ref, dept in self.db.department.items():
            if search in dept.department_name.lower():
                return dept_ref
        raise ValueError("Department not found")

    @is_tool(ToolType.READ)
    def find_team_ref_by_name(self, team_name: str) -> str:
        """
        功能说明（Description）：
            查找团队refbyname，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `team_name` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        search = team_name.lower()
        for t_ref, t in self.db.team.items():
            if search in t.team_name.lower():
                return t_ref
        raise ValueError("Team not found")

    @is_tool(ToolType.READ)
    def find_role_ref_by_name(self, role_name: str) -> str:
        """
        功能说明（Description）：
            查找角色refbyname，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `role_name` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        search = role_name.lower()
        for r_ref, r in self.db.role.items():
            if r.role_name.lower() == search:
                return r_ref
        raise ValueError("Role not found")

    # ----------------
    # Employee (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_details(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工详情，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        emp = self._get_employee(employee_ref)
        up = self._get_user_profile(emp.user_profile_ref)
        result = {
            "employee_ref": emp.employee_ref,
            "employee_number": emp.employee_number,
            "worker_type": emp.worker_type,
            "employment_status": emp.employment_status,
            "hire_date": emp.hire_date,
            "termination_date": emp.termination_date,
            "direct_manager_ref": emp.direct_manager_ref,
            "position_ref": emp.position_ref,
            "display_name": up.display_name,
            "phone": up.phone,
            "bio": up.bio,
            "account_status": up.account_status,
        }
        return json.dumps(result)

    @is_tool(ToolType.READ)
    def search_employees(
        self,
        name: Optional[str] = None,
        department_ref: Optional[str] = None,
        worker_type: Optional[str] = None,
        employment_status: Optional[str] = None,
        job_family: Optional[str] = None,
        position_level: Optional[int] = None,
    ) -> str:
        """
        功能说明（Description）：
            检索员工列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `name` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `department_ref` (Optional[str]): 目标业务对象的引用 ID，用于唯一定位记录。 默认值为 `None`。
            - `worker_type` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `employment_status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `job_family` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `position_level` (Optional[int]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        # If department_ref filter is provided, get the set of employee_refs in that department
        dept_employee_refs = None
        if department_ref is not None:
            dept_employee_refs = set()
            for dm in self.db.department_member.values():
                if dm.department_ref == department_ref and dm.status == "active":
                    dept_employee_refs.add(dm.employee_ref)

        results = []
        for emp_ref, emp in self.db.employee.items():
            # worker_type filter
            if worker_type is not None and emp.worker_type != worker_type:
                continue
            # employment_status filter
            if employment_status is not None and emp.employment_status != employment_status:
                continue
            # department filter
            if dept_employee_refs is not None and emp_ref not in dept_employee_refs:
                continue
            # position-based filters
            if job_family is not None or position_level is not None:
                if emp.position_ref not in self.db.position:
                    continue
                pos = self.db.position[emp.position_ref]
                if job_family is not None and pos.job_family != job_family:
                    continue
                if position_level is not None and pos.position_level != position_level:
                    continue
            # name filter
            up = self._get_user_profile(emp.user_profile_ref)
            if name is not None and name.lower() not in up.display_name.lower():
                continue

            results.append({
                "employee_ref": emp.employee_ref,
                "display_name": up.display_name,
                "employee_number": emp.employee_number,
                "employment_status": emp.employment_status,
                "worker_type": emp.worker_type,
                "position_ref": emp.position_ref,
            })

        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_employees(
        self,
        employment_status: Optional[str] = None,
        worker_type: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出员工列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employment_status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `worker_type` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for emp_ref, emp in self.db.employee.items():
            if employment_status is not None and emp.employment_status != employment_status:
                continue
            if worker_type is not None and emp.worker_type != worker_type:
                continue
            up = self._get_user_profile(emp.user_profile_ref)
            results.append({
                "employee_ref": emp.employee_ref,
                "display_name": up.display_name,
                "employee_number": emp.employee_number,
                "employment_status": emp.employment_status,
                "worker_type": emp.worker_type,
                "position_ref": emp.position_ref,
            })
        return json.dumps(results)

    # ----------------
    # Department (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_department_details(self, department_ref: str) -> Department:
        """
        功能说明（Description）：
            获取部门详情，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Department`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_department(department_ref)

    @is_tool(ToolType.READ)
    def list_departments(
        self,
        parent_ref: Optional[str] = None,
        department_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出部门列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `parent_ref` (Optional[str]): 目标业务对象的引用 ID，用于唯一定位记录。 默认值为 `None`。
            - `department_type` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for dept_ref, dept in self.db.department.items():
            if parent_ref is not None and dept.parent_department_ref != parent_ref:
                continue
            if department_type is not None and dept.department_type != department_type:
                continue
            if status is not None and dept.department_status != status:
                continue
            results.append({
                "department_ref": dept.department_ref,
                "department_name": dept.department_name,
                "department_code": dept.department_code,
                "department_level": dept.department_level,
                "department_type": dept.department_type,
                "department_status": dept.department_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_department_members(
        self,
        department_ref: str,
        include_sub_departments: bool = False,
        membership_role: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出部门成员列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `department_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `include_sub_departments` (bool): 布尔开关参数，用于控制分支逻辑。 默认值为 `False`。
            - `membership_role` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        # Validate the department exists
        self._get_department(department_ref)

        target_dept_refs = {department_ref}
        if include_sub_departments:
            target_dept_refs.update(self._get_descendant_department_refs(department_ref))

        results = []
        for dm in self.db.department_member.values():
            if dm.status != "active":
                continue
            if dm.department_ref not in target_dept_refs:
                continue
            if membership_role is not None and dm.membership_role != membership_role:
                continue
            emp = self._get_employee(dm.employee_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            dept = self._get_department(dm.department_ref)
            results.append({
                "employee_ref": dm.employee_ref,
                "display_name": up.display_name,
                "membership_role": dm.membership_role,
                "is_primary": dm.is_primary,
                "department_ref": dm.department_ref,
                "department_name": dept.department_name,
            })
        return json.dumps(results)

    # ----------------
    # Org hierarchy (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_employee_manager_chain(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            获取员工manager链路，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        chain = []
        visited = set()
        current_ref = employee_ref

        while current_ref is not None:
            if current_ref in visited:
                break  # cycle guard
            visited.add(current_ref)
            emp = self._get_employee(current_ref)
            up = self._get_user_profile(emp.user_profile_ref)
            chain.append({
                "employee_ref": emp.employee_ref,
                "display_name": up.display_name,
                "position_ref": emp.position_ref,
            })
            current_ref = emp.direct_manager_ref

        return json.dumps(chain)

    @is_tool(ToolType.READ)
    def list_direct_reports(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            列出directreports，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        # Validate the employee exists
        self._get_employee(employee_ref)

        results = []
        for emp_ref, emp in self.db.employee.items():
            if emp.direct_manager_ref == employee_ref:
                up = self._get_user_profile(emp.user_profile_ref)
                results.append({
                    "employee_ref": emp.employee_ref,
                    "display_name": up.display_name,
                    "employment_status": emp.employment_status,
                    "position_ref": emp.position_ref,
                })
        return json.dumps(results)

    # ----------------
    # Position (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_position_details(self, position_ref: str) -> Position:
        """
        功能说明（Description）：
            获取position详情，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `position_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Position`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_position(position_ref)

    @is_tool(ToolType.READ)
    def list_positions(
        self,
        position_track: Optional[str] = None,
        job_family: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出positions，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `position_track` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `job_family` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for pos_ref, pos in self.db.position.items():
            if position_track is not None and pos.position_track != position_track:
                continue
            if job_family is not None and pos.job_family != job_family:
                continue
            results.append({
                "position_ref": pos.position_ref,
                "position_title": pos.position_title,
                "position_code": pos.position_code,
                "position_track": pos.position_track,
                "position_level": pos.position_level,
                "job_family": pos.job_family,
                "job_subfamily": pos.job_subfamily,
            })
        return json.dumps(results)

    # ----------------
    # Team (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_team_details(self, team_ref: str) -> Team:
        """
        功能说明（Description）：
            获取团队详情，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `team_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Team`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_team(team_ref)

    @is_tool(ToolType.READ)
    def list_teams(
        self,
        team_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出团队列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `team_type` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
            - `status` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for t_ref, t in self.db.team.items():
            if team_type is not None and t.team_type != team_type:
                continue
            if status is not None and t.team_status != status:
                continue
            results.append({
                "team_ref": t.team_ref,
                "team_name": t.team_name,
                "team_code": t.team_code,
                "team_type": t.team_type,
                "team_status": t.team_status,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_team_members(self, team_ref: str) -> str:
        """
        功能说明（Description）：
            列出团队成员列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `team_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_team(team_ref)

        results = []
        for tm in self.db.team_member.values():
            if tm.team_ref == team_ref and tm.status == "active":
                emp = self._get_employee(tm.employee_ref)
                up = self._get_user_profile(emp.user_profile_ref)
                results.append({
                    "employee_ref": tm.employee_ref,
                    "display_name": up.display_name,
                    "team_role": tm.team_role,
                    "joined_at": tm.joined_at,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_employee_teams(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            列出员工团队列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        results = []
        for tm in self.db.team_member.values():
            if tm.employee_ref == employee_ref and tm.status == "active":
                team = self._get_team(tm.team_ref)
                results.append({
                    "team_ref": tm.team_ref,
                    "team_name": team.team_name,
                    "team_type": team.team_type,
                    "team_role": tm.team_role,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_employee_departments(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            列出员工部门列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        results = []
        for dm in self.db.department_member.values():
            if dm.employee_ref == employee_ref and dm.status == "active":
                dept = self._get_department(dm.department_ref)
                results.append({
                    "department_ref": dm.department_ref,
                    "department_name": dept.department_name,
                    "membership_role": dm.membership_role,
                    "is_primary": dm.is_primary,
                })
        return json.dumps(results)

    # ----------------
    # Mentorship (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def list_mentorships_for_employee(
        self,
        employee_ref: str,
        role: Optional[str] = None,
    ) -> str:
        """
        功能说明（Description）：
            列出mentorshipsfor员工，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `role` (Optional[str]): 业务入参，按函数语义传入。 默认值为 `None`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        results = []
        for m in self.db.mentorship.values():
            match = False
            if role == "mentor" and m.mentor_ref == employee_ref:
                match = True
            elif role == "mentee" and m.mentee_ref == employee_ref:
                match = True
            elif role is None and (m.mentor_ref == employee_ref or m.mentee_ref == employee_ref):
                match = True

            if match:
                results.append({
                    "mentorship_ref": m.mentorship_ref,
                    "mentor_ref": m.mentor_ref,
                    "mentee_ref": m.mentee_ref,
                    "mentorship_type": m.mentorship_type,
                    "status": m.status,
                    "start_date": m.start_date,
                    "end_date": m.end_date,
                })
        return json.dumps(results)

    # ----------------
    # RBAC (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def list_roles(self) -> str:
        """
        功能说明（Description）：
            列出角色列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for r in self.db.role.values():
            results.append({
                "role_ref": r.role_ref,
                "role_name": r.role_name,
                "role_code": r.role_code,
                "role_type": r.role_type,
                "role_status": r.role_status,
                "is_default": r.is_default,
            })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def get_role_details(self, role_ref: str) -> Role:
        """
        功能说明（Description）：
            获取角色详情，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `role_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Role`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        return self._get_role(role_ref)

    @is_tool(ToolType.READ)
    def list_employee_roles(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            列出员工角色列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        results = []
        for er in self.db.employee_role.values():
            if er.employee_ref == employee_ref and er.status == "active":
                role = self._get_role(er.role_ref)
                results.append({
                    "employee_role_ref": er.employee_role_ref,
                    "role_ref": er.role_ref,
                    "role_name": role.role_name,
                    "scope": er.scope,
                    "scope_ref": er.scope_ref,
                    "assigned_at": er.assigned_at,
                    "expires_at": er.expires_at,
                })
        return json.dumps(results)

    @is_tool(ToolType.READ)
    def list_role_permissions(self, role_ref: str) -> str:
        """
        功能说明（Description）：
            列出角色权限列表，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `role_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_role(role_ref)

        results = []
        for rp in self.db.role_permission.values():
            if rp.role_ref == role_ref and rp.status == "active":
                if rp.permission_ref in self.db.permission:
                    perm = self.db.permission[rp.permission_ref]
                    results.append({
                        "permission_ref": perm.permission_ref,
                        "permission_code": perm.permission_code,
                        "resource": perm.resource,
                        "action": perm.action,
                        "scope_constraint": perm.scope_constraint,
                    })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def assign_role_to_employee(
        self,
        employee_ref: str,
        role_ref: str,
        scope: str,
        scope_ref: Optional[str],
        assigned_by_ref: str,
    ) -> EmployeeRole:
        """
        功能说明（Description）：
            处理角色to员工，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `role_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `scope` (str): 业务入参，按函数语义传入。
            - `scope_ref` (Optional[str]): 目标业务对象的引用 ID，用于唯一定位记录。
            - `assigned_by_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeRole`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        # Validate inputs
        self._get_employee(employee_ref)
        self._get_role(role_ref)
        self._get_employee(assigned_by_ref)

        valid_scopes = {"global", "department", "team"}
        if scope not in valid_scopes:
            raise ValueError(f"Invalid scope: {scope}. Must be one of {valid_scopes}")

        if scope != "global" and scope_ref is None:
            raise ValueError(f"scope_ref must be provided when scope is '{scope}'")

        # Validate scope_ref exists
        if scope == "department" and scope_ref is not None:
            self._get_department(scope_ref)
        elif scope == "team" and scope_ref is not None:
            self._get_team(scope_ref)

        now = self._now_iso()
        er_ref = self._generate_ref("ER", self.db.employee_role)

        employee_role = EmployeeRole(
            employee_role_ref=er_ref,
            employee_ref=employee_ref,
            role_ref=role_ref,
            scope=scope,
            scope_ref=scope_ref if scope != "global" else None,
            assigned_by_ref=assigned_by_ref,
            assigned_at=now,
            expires_at=None,
            status="active",
            created_at=now,
            updated_at=now,
        )

        self.db.employee_role[er_ref] = employee_role
        return employee_role

    @is_tool(ToolType.WRITE)
    def revoke_employee_role(self, employee_role_ref: str) -> EmployeeRole:
        """
        功能说明（Description）：
            处理员工角色，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_role_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `EmployeeRole`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        if employee_role_ref not in self.db.employee_role:
            raise ValueError("Employee role assignment not found")

        er = self.db.employee_role[employee_role_ref]
        if er.status in ("revoked", "expired"):
            raise ValueError(f"Employee role assignment is already {er.status}")

        er.status = "revoked"
        er.updated_at = self._now_iso()
        return er

    # ----------------
    # OrgConfig (READ)
    # ----------------
    @is_tool(ToolType.READ)
    def get_org_config(self, config_key: str) -> OrgConfig:
        """
        功能说明（Description）：
            获取orgconfig，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `config_key` (str): 业务入参，按函数语义传入。
        返回（Returns）：
            - `OrgConfig`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        for oc in self.db.org_config.values():
            if oc.config_key == config_key:
                return oc
        raise ValueError("Organization config not found")

    @is_tool(ToolType.READ)
    def list_org_configs(self) -> str:
        """
        功能说明（Description）：
            列出orgconfigs，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - 无。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        results = []
        for oc in self.db.org_config.values():
            results.append({
                "org_config_ref": oc.org_config_ref,
                "config_key": oc.config_key,
                "config_value": oc.config_value,
                "config_type": oc.config_type,
                "description": oc.description,
            })
        return json.dumps(results)

    # ----------------
    # Notification (READ + WRITE)
    # ----------------
    @is_tool(ToolType.READ)
    def list_notifications_for_employee(
        self,
        employee_ref: str,
        unread_only: bool = False,
    ) -> str:
        """
        功能说明（Description）：
            列出通知列表for员工，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
            - `unread_only` (bool): 布尔开关参数，用于控制分支逻辑。 默认值为 `False`。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        notifications = []
        for n in self.db.notification.values():
            if n.recipient_employee_ref != employee_ref:
                continue
            if unread_only and n.read_status != "unread":
                continue
            notifications.append(n)

        # Sort by created_at descending
        notifications.sort(key=lambda x: x.created_at, reverse=True)

        results = []
        for n in notifications:
            results.append({
                "notification_ref": n.notification_ref,
                "title": n.title,
                "body": n.body,
                "notification_type": n.notification_type,
                "channel": n.channel,
                "read_status": n.read_status,
                "created_at": n.created_at,
                "related_resource_type": n.related_resource_type,
                "related_resource_ref": n.related_resource_ref,
            })
        return json.dumps(results)

    @is_tool(ToolType.WRITE)
    def mark_notification_read(self, notification_ref: str) -> Notification:
        """
        功能说明（Description）：
            标记通知read，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `notification_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `Notification`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        n = self._get_notification(notification_ref)
        if n.read_status in ("read", "dismissed"):
            raise ValueError(f"Notification is already {n.read_status}")

        n.read_status = "read"
        n.read_at = self._now_iso()
        return n

    @is_tool(ToolType.WRITE)
    def mark_all_notifications_read(self, employee_ref: str) -> str:
        """
        功能说明（Description）：
            标记all通知列表read，并返回可供后续流程使用的结果。
        参数（Parameters）：
            - `employee_ref` (str): 目标业务对象的引用 ID，用于唯一定位记录。
        返回（Returns）：
            - `str`: 函数执行后的结果；具体结构以类型标注和业务上下文为准。
        异常（Raises）：
            - `ValueError`: 输入不合法、资源不存在或状态不满足业务约束时抛出。
            - `Exception`: 其他由底层依赖、类型转换或运行时错误引发的异常。
        """
        self._get_employee(employee_ref)

        now = self._now_iso()
        count = 0
        for n in self.db.notification.values():
            if n.recipient_employee_ref == employee_ref and n.read_status == "unread":
                n.read_status = "read"
                n.read_at = now
                count += 1

        return json.dumps({"updated_count": count})