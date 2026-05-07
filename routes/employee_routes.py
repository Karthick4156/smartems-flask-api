from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.employee_service import (
    get_my_profile,
    update_my_profile,
    change_my_password
)

from services.leave_service import apply_leave, get_my_leaves
from services.correction_service import request_correction, get_my_corrections
from services.dashboard_service import employee_dashboard

from utils.api_response import success_response
from utils.validators import validate_schema

from schemas.auth_schema import ChangePasswordSchema
# (You should create UpdateProfileSchema, LeaveSchema, CorrectionSchema)

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    return success_response(data=get_my_profile())


@employee_bp.route("/profile-edit", methods=["PUT"])
@jwt_required()
def update_profile():
    data = request.get_json()
    return success_response(update_my_profile(data))


@employee_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    schema = ChangePasswordSchema()
    data = validate_schema(schema, request.get_json())

    return success_response(change_my_password(data))


@employee_bp.route("/leaves", methods=["POST"])
@jwt_required()
def apply_leave_api():
    data = request.get_json()
    return success_response(apply_leave(data))


@employee_bp.route("/leaves", methods=["GET"])
@jwt_required()
def get_my_leaves_api():
    return success_response(data=get_my_leaves())


@employee_bp.route("/corrections", methods=["GET"])
@jwt_required()
def get_my_corrections_api():
    return success_response(data=get_my_corrections())


@employee_bp.route("/correction", methods=["POST"])
@jwt_required()
def request_correction_api():
    data = request.get_json()
    return success_response(request_correction(data))


@employee_bp.route("/dashboard-summary", methods=["GET"])
@jwt_required()
def employee_dashboard_api():
    return success_response(data=employee_dashboard())