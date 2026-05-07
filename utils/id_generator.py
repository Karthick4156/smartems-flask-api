from models.user import User
from models.employee import Employee

def generate_user_id(role: str):
    if role == "Admin":
        prefix = "ADM"
    else:
        prefix = "EMP"

    last_user = User.query.order_by(User.id.desc()).first()

    next_id = 1 if not last_user else last_user.id + 1

    return f"{prefix}{str(next_id).zfill(3)}"


def generate_employee_code():
    last_employee = Employee.query.order_by(Employee.id.desc()).first()

    next_id = 1 if not last_employee else last_employee.id + 1

    return f"EMS{str(next_id).zfill(3)}"