from marshmallow import Schema, fields, validates_schema, ValidationError
import re

PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@#$%^&+=]{6,}$"

class ChangePasswordSchema(Schema):
    currentPassword = fields.String(required=True)
    newPassword = fields.String(required=True)
    confirmPassword = fields.String(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["newPassword"] != data["confirmPassword"]:
            raise ValidationError({
                "confirmPassword": ["Passwords do not match"]
            })

        if not re.match(PASSWORD_REGEX, data["newPassword"]):
            raise ValidationError({
                "newPassword": ["Password must contain letter, number and min 6 chars"]
            })