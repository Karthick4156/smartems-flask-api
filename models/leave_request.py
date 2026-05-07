from extensions import db
from models.base import BaseEntity
import enum


class LeaveType(enum.Enum):
    Paid = "Paid"
    Sick = "Sick"


class LeaveStatus(enum.Enum):
    Pending = 1
    Approved = 2
    Rejected = 3


class LeaveRequest(BaseEntity):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    leave_type = db.Column(db.Enum(LeaveType), nullable=False)

    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)

    reason = db.Column(db.String(200), nullable=False)

    status = db.Column(db.Enum(LeaveStatus), default=LeaveStatus.Pending)

    employee = db.relationship("Employee")