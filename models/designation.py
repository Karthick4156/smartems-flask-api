from extensions import db
from models.base import BaseEntity

class Designation(BaseEntity):
    __tablename__ = "designations"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship("Department", back_populates="designations")