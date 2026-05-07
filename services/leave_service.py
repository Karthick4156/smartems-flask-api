from datetime import datetime
from models.leave_request import LeaveRequest, LeaveStatus, LeaveType
from models.user import User
from models.employee import Employee
from utils.current_user import get_current_user_email
from extensions import db
from flask import current_app
from utils.exceptions import NotFoundException, BadRequestException
from repositories.employee_repository import get_user_by_email
from datetime import timedelta
from utils.pagination import paginate_query, build_pagination_response
from repositories.leave_repository import (
    get_overlapping_leave,
    add_leave,
    get_all_leaves_query,
    get_employee_leaves_query,
    get_leave_by_id,
    rollback,
    commit
)

def apply_leave(data):
    try:
        email = get_current_user_email()

        user = get_user_by_email(email)
        if not user or not user.employee:
            raise NotFoundException("Employee not found")

        employee = user.employee

        from_date = datetime.fromisoformat(data["fromDate"]).date()
        to_date = datetime.fromisoformat(data["toDate"]).date()

        if from_date > to_date:
            raise BadRequestException("Invalid date range")

        existing = get_overlapping_leave(employee.id, from_date, to_date)

        if existing:
            raise BadRequestException("Leave already exists for this date range")

        leave = LeaveRequest(
            employee_id=employee.id,
            leave_type=LeaveType(data["leaveType"]),
            from_date=from_date,
            to_date=to_date,
            reason=data["reason"],
            status=LeaveStatus.Pending
        )

        add_leave(leave)
        commit()

        return "Leave applied"

    except Exception as e:
        rollback()
        current_app.logger.error("Apply leave failed: %s", str(e))
        raise

def get_all_leaves(page=1, page_size=10):

    query = get_all_leaves_query()

    total, leaves = paginate_query(query, page, page_size)

    items = [
        {
            "id": l.id,
            "employeeCode": l.employee.employee_code,
            "name": l.employee.name,
            "leaveType": l.leave_type.name,
            "fromDate": l.from_date,
            "toDate": l.to_date,
            "status": l.status.name
        }
        for l in leaves
    ]

    return build_pagination_response(page, page_size, total, items)

def get_my_leaves(page=1, page_size=10):

    email = get_current_user_email()

    user = get_user_by_email(email)
    if not user or not user.employee:
        raise NotFoundException("Employee not found")

    employee = user.employee

    query = get_employee_leaves_query(employee.id)

    total, leaves = paginate_query(query, page, page_size)

    items = [
        {
            "id": l.id,
            "employeeCode": employee.employee_code,
            "name": employee.name,
            "leaveType": l.leave_type.name,
            "fromDate": l.from_date,
            "toDate": l.to_date,
            "status": l.status.name
        }
        for l in leaves
    ]

    return build_pagination_response(page, page_size, total, items)

def approve_leave(leave_id):
    try:
        leave = get_leave_by_id(leave_id)

        if not leave:
            raise NotFoundException("Leave not found")

        if leave.status != LeaveStatus.Pending:
            raise BadRequestException("Already processed")

        employee = leave.employee
        days = (leave.to_date - leave.from_date).days + 1

        if leave.leave_type == LeaveType.Paid:
            if employee.paid_leave_balance < days:
                raise BadRequestException("Insufficient paid leave")
            employee.paid_leave_balance -= days

        elif leave.leave_type == LeaveType.Sick:
            if employee.sick_leave_balance < days:
                raise BadRequestException("Insufficient sick leave")
            employee.sick_leave_balance -= days

        leave.status = LeaveStatus.Approved

        commit()
        return "Approved"

    except Exception as e:
        rollback()
        current_app.logger.error("Approve leave failed: %s", str(e))
        raise

def reject_leave(leave_id):
    try:
        leave = get_leave_by_id(leave_id)

        if not leave:
            raise NotFoundException("Leave not found")

        if leave.status != LeaveStatus.Pending:
            raise BadRequestException("Already processed")

        leave.status = LeaveStatus.Rejected

        commit()
        return "Rejected"

    except Exception as e:
        rollback()
        current_app.logger.error("Reject leave failed: %s", str(e))
        raise