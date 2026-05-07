from flask import Blueprint
from services.department_service import get_all_departments
from utils.api_response import success_response

department_bp = Blueprint("departments", __name__)


@department_bp.route("/", methods=["GET"], strict_slashes=False)
def get_departments():
    return success_response(data=get_all_departments())