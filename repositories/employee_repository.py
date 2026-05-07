from models.user import User
from models.employee import Employee
from models.department import Department
from models.designation import Designation
from sqlalchemy.orm import joinedload
from extensions import db

# 🔹 CREATE
def add_user(user):
    db.session.add(user)
    db.session.flush()

def add_employee(employee):
    db.session.add(employee)

def commit():
    db.session.commit()

def rollback():
    db.session.rollback()


# 🔹 READ
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_department_by_id(dept_id):
    return Department.query.get(dept_id)

def get_designation(dept_id, designation_id):
    return Designation.query.filter_by(
        id=designation_id,
        department_id=dept_id
    ).first()

def get_employee_by_id(employee_id):
    return (
        Employee.query
        .options(
            joinedload(Employee.user),
            joinedload(Employee.department),
            joinedload(Employee.designation)
        )
        .filter(Employee.id == employee_id)
        .first()
    )

def get_employee_basic(employee_id):
    return Employee.query.get(employee_id)

def get_user_with_employee(email):
    return (
        User.query
        .options(
            joinedload(User.employee)
            .joinedload(Employee.department),
            joinedload(User.employee)
            .joinedload(Employee.designation)
        )
        .filter_by(email=email)
        .first()
    )