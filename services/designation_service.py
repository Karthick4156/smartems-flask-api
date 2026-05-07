from models.designation import Designation
from repositories.master_repository import (
    get_designations
)

def get_designations_by_department(department_id):

    designations = get_designations(department_id)

    return [
        {
            "id": d.id,
            "name": d.name
        }
        for d in designations
    ]