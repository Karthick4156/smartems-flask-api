from app import create_app
from extensions import db
from models.department import Department
from models.designation import Designation

app = create_app()

with app.app_context():

    if Department.query.first():
        print("Data already seeded")
    else:
        # Departments
        hr = Department(code="HR", name="Human Resources")
        it = Department(code="IT", name="Information Technology")
        fin = Department(code="FINANCE", name="Finance")

        db.session.add_all([hr, it, fin])
        db.session.flush()

        # Designations
        designations = [
            Designation(name="HR Executive", department_id=hr.id),
            Designation(name="HR Manager", department_id=hr.id),

            Designation(name="Software Developer", department_id=it.id),
            Designation(name="QA Engineer", department_id=it.id),

            Designation(name="Accountant", department_id=fin.id),
        ]

        db.session.add_all(designations)
        db.session.commit()

        print("✅ Departments & Designations seeded!")