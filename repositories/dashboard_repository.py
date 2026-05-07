from models.user import User
from models.leave_request import LeaveRequest, LeaveStatus
from models.correction_request import CorrectionRequest, CorrectionStatus
from models.attendance import Attendance
from models.enums import AccountStatus, UserRole
from datetime import timedelta


# ✅ ADMIN COUNTS
def count_active_employees():
    return User.query.filter_by(
        status=AccountStatus.Active,
        role=UserRole.Employee
    ).count()


def count_inactive_employees():
    return User.query.filter_by(
        status=AccountStatus.Inactive,
        role=UserRole.Employee
    ).count()


def count_pending_leaves():
    return LeaveRequest.query.filter_by(
        status=LeaveStatus.Pending
    ).count()


def count_pending_corrections():
    return CorrectionRequest.query.filter_by(
        status=CorrectionStatus.Pending
    ).count()


# ✅ EMPLOYEE DATA
def get_today_attendance(employee_id, today):
    return Attendance.query.filter(
        Attendance.employee_id == employee_id,
        Attendance.date >= today,
        Attendance.date < today + timedelta(days=1)
    ).first()


def count_employee_leaves(employee_id, status):
    return LeaveRequest.query.filter_by(
        employee_id=employee_id,
        status=status
    ).count()


def count_employee_corrections(employee_id, status):
    return CorrectionRequest.query.filter_by(
        employee_id=employee_id,
        status=status
    ).count()