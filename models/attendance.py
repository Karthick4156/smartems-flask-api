from extensions import db
from models.base import BaseEntity

from sqlalchemy import UniqueConstraint, CheckConstraint

class Attendance(BaseEntity):
    __tablename__ = "attendances"
    

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, nullable=False)

    punch_in_time = db.Column(db.DateTime, nullable=True)
    punch_out_time = db.Column(db.DateTime, nullable=True)

    work_hours = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default="Pending")

    # FK
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    employee = db.relationship("Employee")
    
    __table_args__ = (
    UniqueConstraint('employee_id', 'date', name='uq_employee_date'),
    CheckConstraint('work_hours >= 0', name='check_work_hours_positive'),
    )