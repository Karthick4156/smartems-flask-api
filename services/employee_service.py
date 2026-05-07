from utils.current_user import get_current_user_email
from datetime import datetime
from utils.password import verify_password, hash_password
from repositories.employee_repository import (
    get_user_with_employee,
    get_user_by_email,
    commit,
    rollback
)
from utils.exceptions import NotFoundException, BadRequestException
from utils.validators import validate_password, validate_confirm_password


# ✅ GET PROFILE
def get_my_profile():
    email = get_current_user_email()

    user = get_user_with_employee(email)

    if not user or not user.employee:
        raise NotFoundException("Employee not found")

    employee = user.employee

    return {
        "employeeCode": employee.employee_code,
        "userId": user.user_id,
        "name": employee.name,
        "email": user.email,
        "department": employee.department.code,
        "designation": employee.designation.name,
        "phone": employee.phone,
        "address": employee.address,
        "paidLeaveBalance": employee.paid_leave_balance,
        "sickLeaveBalance": employee.sick_leave_balance
    }


# ✅ UPDATE PROFILE
def update_my_profile(data):
    try:
        email = get_current_user_email()

        user = get_user_by_email(email)
        if not user or not user.employee:
            raise NotFoundException("Employee not found")

        employee = user.employee

        employee.phone = data.get("phone", employee.phone)
        employee.address = data.get("address", employee.address)
        employee.updated_at = datetime.utcnow()

        commit()
        return "Profile updated"

    except Exception:
        rollback()
        raise


# ✅ CHANGE PASSWORD (CLEAN VERSION)
def change_my_password(data):
    try:
        email = get_current_user_email()

        user = get_user_by_email(email)
        if not user:
            raise NotFoundException("User not found")

        # 🔐 Current password check
        if not verify_password(data["currentPassword"], user.password_hash):
            raise BadRequestException("Invalid current password")

        # 🔐 Prevent same password reuse
        if verify_password(data["newPassword"], user.password_hash):
            raise BadRequestException("New password must be different")

        # 🔐 Reuse central validators
        validate_password(data["newPassword"])
        validate_confirm_password(data["newPassword"], data["confirmPassword"])

        user.password_hash = hash_password(data["newPassword"])

        commit()
        return "Password changed successfully"

    except Exception:
        rollback()
        raise