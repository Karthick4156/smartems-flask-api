from models.user import User
from models.employee import Employee
from models.enums import UserRole, AccountStatus
from models.department import Department
from models.designation import Designation
from utils.password import hash_password
from utils.id_generator import generate_user_id, generate_employee_code
from utils.validators import validate_password, validate_confirm_password
from utils.pagination import paginate_query, build_pagination_response

from datetime import datetime

from sqlalchemy.orm import joinedload
from repositories.employee_repository import (
    get_user_by_email,
    add_user,
    add_employee,
    commit,
    rollback,
    get_employee_by_id as repo_get_employee_by_id,
    get_department_by_id,
    get_designation,
    get_employee_basic,
    get_user_with_employee
)


from flask import current_app

from utils.exceptions import NotFoundException, BadRequestException
from utils.pagination import paginate_query, build_pagination_response
from sqlalchemy.exc import IntegrityError

def create_employee(data):
    try:
       
        if get_user_by_email(data["email"]):
            raise BadRequestException("Email already exists")

        validate_password(data["password"])
        validate_confirm_password(data["password"], data["confirmPassword"])

        department = get_department_by_id(data["departmentId"])
        if not department:
            raise BadRequestException("Invalid Department")

        designation = get_designation(
            data["departmentId"],
            data["designationId"]
        )
        if not designation:
            raise BadRequestException("Invalid Designation")

        user = User(
            user_id=generate_user_id("Employee"),
            email=data["email"],
            password_hash=hash_password(data["password"]),
            role=UserRole.Employee,
            status=AccountStatus.Active
        )

        add_user(user)

        employee = Employee(
            employee_code=generate_employee_code(),
            name=data["name"],
            department_id=data["departmentId"],
            designation_id=data["designationId"],
            joining_date=data["joiningDate"],
            phone=data.get("phone"),
            address=data.get("address"),
            user_id=user.id
        )

        add_employee(employee)
        commit()

        return "Employee created successfully"

    except Exception:
        rollback()
        raise

def get_all_employees(page=1, page_size=10, search=None):

    current_app.logger.info(
        "Employees API called page=%s pageSize=%s search=%s",
        page, page_size, search
    )

    total_count, employees = get_paginated_employees(page, page_size, search)

    items = []
    for e in employees:
        user = e.user

        items.append({
            "id": e.id,
            "employeeCode": e.employee_code,
            "name": e.name,
            "email": user.email,
            "phone": e.phone,
            "address": e.address,
            "inactiveReason": user.inactive_reason,
            "departmentId": e.department_id,
            "department": e.department.code,
            "designationId": e.designation_id,
            "designation": e.designation.name,
            "joiningDate": e.joining_date,
            "status": user.status.value
        })

    return build_pagination_response(page, page_size, total_count, items)

def get_paginated_employees(page, page_size, search):
    query = (
        Employee.query
        .options(
            joinedload(Employee.user),
            joinedload(Employee.department),
            joinedload(Employee.designation)
        )
    )

    if search:
        search_term = f"%{search}%"
        query = query.join(User).filter(
            Employee.name.ilike(search_term) |
            User.email.ilike(search_term) |
            Employee.employee_code.ilike(search_term)
        )

    return paginate_query(query, page, page_size)
  
  
def get_employee_by_id(employee_id):

    employee = repo_get_employee_by_id(employee_id)

    if not employee:
        raise NotFoundException("Employee not found")

    user = employee.user

    return {
        "id": employee.id,
        "employeeCode": employee.employee_code,
        "userId": user.user_id,
        "name": employee.name,
        "email": user.email,
        "phone": employee.phone,
        "address": employee.address,
        "departmentId": employee.department_id,
        "department": employee.department.code,
        "designationId": employee.designation_id,
        "designation": employee.designation.name,
        "joiningDate": employee.joining_date,
        "status": user.status.value
    }
    
def update_employee(employee_id, data):

    employee = get_employee_basic(employee_id)

    if not employee:
        raise NotFoundException("Employee not found")

    department = get_department_by_id(data["departmentId"])
    if not department:
        raise BadRequestException("Invalid Department")

    designation = get_designation(
        data["departmentId"],
        data["designationId"]
    )

    if not designation:
        raise BadRequestException("Invalid Designation")

    employee.name = data["name"]
    employee.phone = data.get("phone")
    employee.address = data.get("address")
    employee.department_id = data["departmentId"]
    employee.designation_id = data["designationId"]
    employee.joining_date = data["joiningDate"]
    employee.updated_at = datetime.utcnow()

    commit()

    return "Updated successfully"

from models.enums import AccountStatus

def toggle_employee_status(emp_id, is_active, reason):

    current_app.logger.info(
        "Toggle employee status started emp_id=%s is_active=%s",
        emp_id, is_active
    )

    emp = get_employee_basic(emp_id)

    if not emp:
        current_app.logger.warning(
            "Toggle employee status failed - employee not found emp_id=%s",
            emp_id
        )
        raise NotFoundException("Employee not found")

    user = emp.user

    if user.role.value == "Admin" and not is_active:
        current_app.logger.warning(
            "Attempt to deactivate admin blocked emp_id=%s",
            emp_id
        )
        raise BadRequestException("Admin cannot be deactivated")

    old_status = user.status

    if is_active:
        user.status = AccountStatus.Active
        user.inactive_reason = None
    else:
        user.status = AccountStatus.Inactive
        user.inactive_reason = reason

    commit()

    current_app.logger.info(
        "Toggle employee status success emp_id=%s old_status=%s new_status=%s",
        emp_id, old_status, user.status
    )

    return "Status updated"

def reset_employee_password(data):

    user = get_user_by_email(data.get("email"))

    if not user:
        raise NotFoundException("User not found")

    validate_password(data["newPassword"])
    validate_confirm_password(data["newPassword"], data["confirmPassword"])

    user.password_hash = hash_password(data["newPassword"])

    commit()

    return "Password reset successful"