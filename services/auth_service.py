from models.enums import AccountStatus
from utils.password import verify_password
from flask_jwt_extended import create_access_token
from flask import current_app

from utils.exceptions import BadRequestException, UnauthorizedException
from repositories.employee_repository import get_user_by_email


def login_user(email, password):

    user = get_user_by_email(email)

    if not user:
        raise UnauthorizedException("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedException("Invalid credentials")

    if user.status != AccountStatus.Active:
        raise BadRequestException("Account is inactive")

    token = create_access_token(
        identity=user.email,
        additional_claims={
            "role": user.role.value,
            "userId": user.id
        }
    )

    current_app.logger.info("User logged in: %s", email)

    return {
        "token": token,
        "role": user.role.value
    }