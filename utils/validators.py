import re

from marshmallow import ValidationError
from utils.exceptions import BadRequestException

PASSWORD_REGEX = r'^(?=.*[A-Za-z])(?=.*\d).{6,}$'

def validate_password(password: str):
    if not password:
        raise Exception("Password is required")

    if not re.match(PASSWORD_REGEX, password):
        raise Exception(
            "Password must be at least 6 characters and contain at least one letter and one number"
        )


def validate_confirm_password(password: str, confirm_password: str):
    if password != confirm_password:
        raise Exception("Passwords do not match")

def validate_schema(schema, data):
    try:
        return schema.load(data)
    except ValidationError as err:
        # Convert to clean error message
        messages = []
        for field, errors in err.messages.items():
            for e in errors:
                messages.append(f"{field}: {e}")

        raise BadRequestException(", ".join(messages))