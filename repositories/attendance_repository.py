from models.attendance import Attendance
from extensions import db
from datetime import datetime, timedelta


def get_today_attendance(employee_id, today):
    return Attendance.query.filter(
        Attendance.employee_id == employee_id,
        Attendance.date >= today,
        Attendance.date < today + timedelta(days=1)
    ).first()


def create_attendance(employee_id):
    attendance = Attendance(
        date=datetime.utcnow(),
        punch_in_time=datetime.utcnow(),
        status="InProgress",
        employee_id=employee_id
    )
    db.session.add(attendance)
    return attendance


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()


def get_employee_attendance(employee_id):
    return (
        Attendance.query
        .filter_by(employee_id=employee_id)
        .order_by(Attendance.date.desc())
        .all()
    )