from datetime import datetime, timedelta
from utils.current_user import get_current_user_email
from utils.exceptions import NotFoundException, BadRequestException
from repositories.employee_repository import get_user_by_email
from repositories.attendance_repository import (
    get_today_attendance,
    create_attendance,
    get_employee_attendance,
    commit,
    rollback
)
from flask import current_app


# ✅ COMMON HELPER (IMPORTANT)
def _get_employee():
    email = get_current_user_email()

    user = get_user_by_email(email)
    if not user or not user.employee:
        raise NotFoundException("Employee not found")

    return user.employee


# ✅ PUNCH IN
def punch_in():
    try:
        employee = _get_employee()
        today = datetime.utcnow().date()

        attendance = get_today_attendance(employee.id, today)

        if attendance:
            if attendance.punch_in_time:
                raise BadRequestException("Already punched in")

            attendance.punch_in_time = datetime.utcnow()
            attendance.status = "InProgress"
        else:
            create_attendance(employee.id)

        commit()
        return "Punched in"

    except Exception as e:
        rollback()
        current_app.logger.error("Punch in failed: %s", str(e))
        raise


# ✅ PUNCH OUT
def punch_out():
    try:
        employee = _get_employee()
        today = datetime.utcnow().date()

        attendance = get_today_attendance(employee.id, today)

        if not attendance:
            raise BadRequestException("Punch in first")

        if attendance.punch_out_time:
            raise BadRequestException("Already punched out")

        if not attendance.punch_in_time:
            raise BadRequestException("Invalid punch-in data")

        attendance.punch_out_time = datetime.utcnow()

        duration = attendance.punch_out_time - attendance.punch_in_time
        hours = round(duration.total_seconds() / 3600, 2)

        if hours < 0:
            raise BadRequestException("Invalid time calculation")

        attendance.work_hours = hours

        if hours >= 7:
            attendance.status = "FullDay"
        elif hours >= 4:
            attendance.status = "HalfDay"
        else:
            attendance.status = "Absent"

        commit()
        return "Punched out"

    except Exception as e:
        rollback()
        current_app.logger.error("Punch out failed: %s", str(e))
        raise


# ✅ GET ATTENDANCE
def get_my_attendance():
    employee = _get_employee()

    records = get_employee_attendance(employee.id)

    return [
        {
            "date": a.date.date(),
            "punchIn": a.punch_in_time.isoformat() if a.punch_in_time else None,
            "punchOut": a.punch_out_time.isoformat() if a.punch_out_time else None,
            "workHours": a.work_hours,
            "status": a.status
        }
        for a in records
    ]