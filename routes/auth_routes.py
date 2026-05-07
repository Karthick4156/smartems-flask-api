from flask import Blueprint, request
from services.auth_service import login_user
from utils.api_response import success_response
from utils.pagination import get_pagination_params  # not needed here, just pattern consistency
from utils.exceptions import BadRequestException

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        raise BadRequestException("Invalid request body")

    email = data.get('email', '').strip().lower()
    password = data.get('password')

    if not email or not password:
        raise BadRequestException("Email and password required")

    result = login_user(email, password)

    return success_response("Login successful", result)