from datetime import datetime
from utils.current_user import get_current_user_email
from utils.exceptions import NotFoundException
from repositories.employee_repository import get_user_by_email
from repositories.dashboard_repository import (
    count_active_employees,
    count_inactive_employees,
    count_pending_leaves,
    count_pending_corrections,
    get_today_attendance,
    count_employee_leaves,
    count_employee_corrections
)
from models.leave_request import LeaveStatus
from models.correction_request import CorrectionStatus


# ✅ COMMON HELPER
def _get_employee():
    email = get_current_user_email()

    user = get_user_by_email(email)
    if not user or not user.employee:
        raise NotFoundException("Employee not found")

    return user.employee


# ✅ ADMIN DASHBOARD
def admin_dashboard():
    return {
        "activeEmployees": count_active_employees(),
        "inactiveEmployees": count_inactive_employees(),
        "pendingLeaves": count_pending_leaves(),
        "pendingCorrections": count_pending_corrections()
    }


# ✅ EMPLOYEE DASHBOARD
def employee_dashboard():
    employee = _get_employee()
    today = datetime.utcnow().date()

    # ✅ Weekend logic (business rule)
    if today.weekday() >= 5:
        return {
            "todayStatus": "Weekend",
            "punchIn": None,
            "punchOut": None,
            "workHours": 0,
            "leaveTaken": 0,
            "pendingLeaves": 0,
            "pendingCorrections": 0
        }

    attendance = get_today_attendance(employee.id, today)

    # ✅ Status logic
    if not attendance:
        status = "Not Marked"
    elif attendance.punch_in_time and not attendance.punch_out_time:
        status = "In Progress"
    else:
        status = attendance.status

    return {
        "todayStatus": status,
        "punchIn": attendance.punch_in_time.isoformat() if attendance and attendance.punch_in_time else None,
        "punchOut": attendance.punch_out_time.isoformat() if attendance and attendance.punch_out_time else None,
        "workHours": attendance.work_hours if attendance else 0,
        "leaveTaken": count_employee_leaves(employee.id, LeaveStatus.Approved),
        "pendingLeaves": count_employee_leaves(employee.id, LeaveStatus.Pending),
        "pendingCorrections": count_employee_corrections(employee.id, CorrectionStatus.Pending)
    }