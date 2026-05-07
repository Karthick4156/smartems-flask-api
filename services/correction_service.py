from datetime import datetime
from models.correction_request import CorrectionRequest, CorrectionStatus
from utils.current_user import get_current_user_email
from utils.exceptions import NotFoundException, BadRequestException
from repositories.employee_repository import get_user_by_email
from repositories.correction_repository import (
    get_attendance_by_date,
    get_pending_correction,
    add_correction,
    get_correction_by_id,
    get_all_corrections_query,
    get_employee_corrections_query,
    commit,
    rollback
)
from utils.pagination import paginate_query, build_pagination_response
from flask import current_app


# ✅ COMMON HELPER
def _get_employee():
    email = get_current_user_email()

    user = get_user_by_email(email)
    if not user or not user.employee:
        raise NotFoundException("Employee not found")

    return user.employee


# ✅ REQUEST CORRECTION
def request_correction(data):
    try:
        employee = _get_employee()

        reason = data.get("reason")
        if not reason or not reason.strip():
            raise BadRequestException("Reason is required")

        target_date = datetime.fromisoformat(data["date"]).date()
        today = datetime.utcnow().date()

        current_app.logger.info(
            "Checking attendance for employee=%s, target_date=%s",
            employee.id, target_date
        )
        
        if target_date >= today:
            raise BadRequestException("Correction allowed only for past dates")

        attendance = get_attendance_by_date(employee.id, target_date)
        if not attendance:
            raise NotFoundException("Attendance record not found")

        if get_pending_correction(employee.id, target_date):
            raise BadRequestException("Correction request already exists")

        correction = CorrectionRequest(
            employee_id=employee.id,
            date=target_date,
            reason=reason,
            status=CorrectionStatus.Pending
        )

        add_correction(correction)
        commit()

        return "Request submitted"

    except Exception as e:
        rollback()
        current_app.logger.error("Request correction failed: %s", str(e))
        raise


# ✅ ADMIN - GET ALL
def get_all_corrections(page=1, page_size=10):
    query = get_all_corrections_query()

    total, corrections = paginate_query(query, page, page_size)

    items = [
        {
            "id": c.id,
            "employeeCode": c.employee.employee_code,
            "employeeName": c.employee.name,
            "date": c.date,
            "reason": c.reason,
            "status": c.status.name
        }
        for c in corrections
    ]

    return build_pagination_response(page, page_size, total, items)


# ✅ EMPLOYEE - GET OWN
def get_my_corrections(page=1, page_size=10):
    employee = _get_employee()

    query = get_employee_corrections_query(employee.id)

    total, corrections = paginate_query(query, page, page_size)

    items = [
        {
            "id": c.id,
            "date": c.date.isoformat(),
            "reason": c.reason,
            "status": c.status.name
        }
        for c in corrections
    ]

    return build_pagination_response(page, page_size, total, items)


# ✅ APPROVE
def approve_correction(correction_id):
    try:
        correction = get_correction_by_id(correction_id)

        if not correction:
            raise NotFoundException("Request not found")

        if correction.status != CorrectionStatus.Pending:
            raise BadRequestException("Already processed")

        attendance = get_attendance_by_date(
            correction.employee_id,
            correction.date
        )

        if not attendance:
            raise NotFoundException("Attendance not found")

        attendance.work_hours = 8
        attendance.status = "FullDay"

        correction.status = CorrectionStatus.Approved

        commit()
        return "Approved"

    except Exception as e:
        rollback()
        current_app.logger.error("Approve correction failed: %s", str(e))
        raise


# ✅ REJECT
def reject_correction(correction_id):
    try:
        correction = get_correction_by_id(correction_id)

        if not correction:
            raise NotFoundException("Request not found")

        if correction.status != CorrectionStatus.Pending:
            raise BadRequestException("Already processed")

        correction.status = CorrectionStatus.Rejected

        commit()
        return "Rejected"

    except Exception as e:
        rollback()
        current_app.logger.error("Reject correction failed: %s", str(e))
        raise