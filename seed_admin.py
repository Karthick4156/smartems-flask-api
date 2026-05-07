from app import create_app
from extensions import db
from models.user import User
from models.enums import UserRole, AccountStatus
from utils.password import hash_password

app = create_app()

with app.app_context():

    # 🔹 Check if admin already exists
    existing_admin = User.query.filter_by(email="admin@ems.com").first()

    if existing_admin:
        print("Admin already exists")
    else:
        admin = User(
            user_id="ADM001",
            email="admin@ems.com",
            password_hash=hash_password("admin123"),
            role=UserRole.Admin,
            status=AccountStatus.Active
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin created successfully!")