from extensions import db
from models.base import BaseEntity
from models.enums import UserRole, AccountStatus

class User(BaseEntity):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(10), nullable=False, unique=True)  
    # ADM001 / EMP001

    email = db.Column(db.String(100), nullable=False, unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.Enum(UserRole), nullable=False)

    status = db.Column(
        db.Enum(AccountStatus),
        default=AccountStatus.Active,
        nullable=False
    )

    inactive_reason = db.Column(db.String(255), nullable=True)

    # Relationship (1-1)
    employee = db.relationship("Employee", back_populates="user", uselist=False)