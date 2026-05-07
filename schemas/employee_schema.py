from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


class CreateEmployeeSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=2)
    )

    email = fields.Email(required=True)

    password = fields.String(
        required=True,
        validate=validate.Length(min=6)
    )

    confirmPassword = fields.String(required=True)

    phone = fields.String()
    address = fields.String()

    departmentId = fields.Integer(required=True)
    designationId = fields.Integer(required=True)

    joiningDate = fields.DateTime(required=True)

    @validates("joiningDate")
    def validate_joining_date(self, value, **kwargs):
        if value > datetime.utcnow():
            raise ValidationError(
                "Joining date cannot be in future"
            )