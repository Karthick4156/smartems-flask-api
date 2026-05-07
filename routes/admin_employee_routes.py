from flask import Blueprint, request
from services.admin_employee_service import (
    create_employee, get_all_employees, get_employee_by_id,
    update_employee, toggle_employee_status, reset_employee_password
)
from utils.api_response import success_response
from middleware.auth_middleware import admin_required
from services.leave_service import approve_leave, reject_leave, get_all_leaves
from services.correction_service import get_all_corrections, approve_correction, reject_correction
from services.dashboard_service import admin_dashboard

from schemas.employee_schema import CreateEmployeeSchema
from utils.validators import validate_schema

from utils.pagination import get_pagination_params
from utils.pagination import paginate_query, build_pagination_response

admin_employee_bp = Blueprint("admin_employee", __name__)


@admin_employee_bp.route("/employees", methods=["POST"])
@admin_required
def create_employee_api():
    schema = CreateEmployeeSchema()
    data = validate_schema(schema, request.get_json())

    result = create_employee(data)
    return success_response(data=result)


@admin_employee_bp.route("/employees", methods=["GET"])
@admin_required
def get_all_employees_api():
    page, page_size = get_pagination_params(request.args)
    search = request.args.get("Search")

    result = get_all_employees(page, page_size, search)
    return success_response(data=result)


@admin_employee_bp.route("/employees/<int:id>", methods=["GET"])
@admin_required
def get_employee_by_id_api(id):
    result = get_employee_by_id(id)
    return success_response(data=result)


@admin_employee_bp.route("/employees/<int:id>", methods=["PUT"])
@admin_required
def update_employee_api(id):
    data = request.get_json()
    result = update_employee(id, data)
    return success_response(result)


@admin_employee_bp.route("/employees/<int:emp_id>/status", methods=["PATCH"])
@admin_required
def toggle_status_api(emp_id):

    is_active = request.args.get("isActive") == "true"
    reason = request.args.get("reason")

    result = toggle_employee_status(emp_id, is_active, reason)
    return success_response(result)


@admin_employee_bp.route("/employees/reset-password", methods=["POST"])
@admin_required
def reset_password_api():
    data = request.get_json()
    result = reset_employee_password(data)
    return success_response(result)


@admin_employee_bp.route("/leaves", methods=["GET"])
@admin_required
def get_all_leaves_api():
    return success_response(data=get_all_leaves())


@admin_employee_bp.route("/leaves/<int:id>/approve", methods=["PATCH"])
@admin_required
def approve_leave_api(id):
    return success_response(approve_leave(id))


@admin_employee_bp.route("/leaves/<int:id>/reject", methods=["PATCH"])
@admin_required
def reject_leave_api(id):
    return success_response(reject_leave(id))


@admin_employee_bp.route("/corrections", methods=["GET"])
@admin_required
def get_all_corrections_api():
    return success_response(data=get_all_corrections())


@admin_employee_bp.route("/corrections/<int:id>/approve", methods=["PATCH"])
@admin_required
def approve_correction_api(id):
    return success_response(approve_correction(id))


@admin_employee_bp.route("/corrections/<int:id>/reject", methods=["PATCH"])
@admin_required
def reject_correction_api(id):
    return success_response(reject_correction(id))


@admin_employee_bp.route("/employees/dashboard-summary", methods=["GET"])
@admin_required
def admin_dashboard_api():
    return success_response(data=admin_dashboard())