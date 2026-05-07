from models.department import Department
from models.designation import Designation


def get_departments():
    return Department.query.all()


def get_designations(department_id):
    return Designation.query.filter_by(
        department_id=department_id
    ).all()