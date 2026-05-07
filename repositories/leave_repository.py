from models.leave_request import LeaveRequest, LeaveStatus
from extensions import db


def get_overlapping_leave(employee_id, from_date, to_date):
    return LeaveRequest.query.filter(
        LeaveRequest.employee_id == employee_id,
        LeaveRequest.status != LeaveStatus.Rejected,
        LeaveRequest.from_date <= to_date,
        LeaveRequest.to_date >= from_date
    ).first()


def add_leave(leave):
    db.session.add(leave)


def get_leave_by_id(leave_id):
    return LeaveRequest.query.get(leave_id)


def get_all_leaves_query():
    return LeaveRequest.query


def get_employee_leaves_query(employee_id):
    return LeaveRequest.query.filter_by(employee_id=employee_id)


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()