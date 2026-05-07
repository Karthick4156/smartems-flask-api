from flask import Blueprint
from services.designation_service import get_designations_by_department
from utils.api_response import success_response

designation_bp = Blueprint("designations", __name__)


@designation_bp.route("/by-department/<int:department_id>", methods=["GET"], strict_slashes=False)
def get_designations(department_id):
    return success_response(
        data=get_designations_by_department(department_id)
    )