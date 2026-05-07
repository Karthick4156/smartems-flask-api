from extensions import db
from models.base import BaseEntity

class Department(BaseEntity):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(20), nullable=False)  # HR, IT, FINANCE
    name = db.Column(db.String(100), nullable=False)

    # Relationship
    designations = db.relationship("Designation", back_populates="department")