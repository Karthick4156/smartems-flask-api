from models.correction_request import CorrectionRequest, CorrectionStatus
from models.attendance import Attendance
from extensions import db
from datetime import timedelta
from sqlalchemy import func

def get_attendance_by_date(employee_id, target_date):
    return Attendance.query.filter(
        Attendance.employee_id == employee_id,
        func.date(Attendance.date) == target_date
    ).first()


def get_pending_correction(employee_id, target_date):
    return CorrectionRequest.query.filter(
        CorrectionRequest.employee_id == employee_id,
        CorrectionRequest.date >= target_date,
        CorrectionRequest.date < target_date + timedelta(days=1),
        CorrectionRequest.status == CorrectionStatus.Pending
    ).first()


def add_correction(correction):
    db.session.add(correction)


def get_correction_by_id(correction_id):
    return CorrectionRequest.query.get(correction_id)


def get_all_corrections_query():
    return CorrectionRequest.query.order_by(CorrectionRequest.date.desc())


def get_employee_corrections_query(employee_id):
    return (
        CorrectionRequest.query
        .filter_by(employee_id=employee_id)
        .order_by(CorrectionRequest.date.desc())
    )


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()