from flask import Blueprint
from flask_jwt_extended import jwt_required
from services.attendance_service import punch_in, punch_out, get_my_attendance
from utils.api_response import success_response

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/attendance/punch-in", methods=["POST"])
@jwt_required()
def punch_in_api():
    return success_response(punch_in())


@attendance_bp.route("/attendance/punch-out", methods=["POST"])
@jwt_required()
def punch_out_api():
    return success_response(punch_out())


@attendance_bp.route("/attendance", methods=["GET"])
@jwt_required()
def get_attendance_api():
    return success_response(data=get_my_attendance())