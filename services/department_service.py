from models.department import Department
from repositories.master_repository import (
    get_departments
)

def get_all_departments():

    departments = get_departments()

    return [
        {
            "id": d.id,
            "code": d.code,
            "name": d.name
        }
        for d in departments
    ]