from extensions import db
from models.base import BaseEntity
import enum


class CorrectionStatus(enum.Enum):
    Pending = 1
    Approved = 2
    Rejected = 3


class CorrectionRequest(BaseEntity):
    __tablename__ = "correction_requests"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)

    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=False)

    status = db.Column(db.Enum(CorrectionStatus), default=CorrectionStatus.Pending)

    employee = db.relationship("Employee")