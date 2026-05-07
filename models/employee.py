from extensions import db
from models.base import BaseEntity

class Employee(BaseEntity):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    employee_code = db.Column(db.String(10), nullable=False, unique=True)

    name = db.Column(db.String(100), nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    designation_id = db.Column(db.Integer, db.ForeignKey("designations.id"),nullable=False)

    joining_date = db.Column(db.DateTime, nullable=False)

    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))

    paid_leave_balance = db.Column(db.Integer, default=12)
    sick_leave_balance = db.Column(db.Integer, default=6)

    # FK
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="employee")
    
    department = db.relationship("Department")
    designation = db.relationship("Designation")