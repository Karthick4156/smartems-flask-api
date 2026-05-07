# SmartEMS Flask API

SmartEMS is a full-stack Employee Management System backend built using Flask, MySQL, and SQLAlchemy.

This backend provides secure REST APIs for employee management, attendance tracking, leave workflows, and attendance correction management with JWT-based authentication and role-based authorization.

---

# 🚀 Features

## Authentication & Authorization
- JWT Authentication
- Role-Based Access Control (Admin / Employee)
- Secure Password Hashing using BCrypt
- Protected APIs using JWT Middleware

---

## Admin Features
- Admin Dashboard Summary
- Create Employee
- View Employees with Pagination & Search
- Update Employee Details
- Activate / Deactivate Employees
- Reset Employee Password
- Approve / Reject Leave Requests
- Approve / Reject Attendance Corrections

---

## Employee Features
- Employee Dashboard
- View & Update Profile
- Change Password
- Punch In / Punch Out Attendance
- Attendance Calendar
- Apply Leave
- Request Attendance Correction
- View Leave & Correction Status

---

# 🛠️ Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Marshmallow
- MySQL
- BCrypt
- REST API

---

# 🏗️ Architecture

The backend follows clean architecture principles:

```text
Routes → Services → Repositories → Database
```

## Layers

### Routes
Handle HTTP requests and responses.

### Services
Contain business logic and workflows.

### Repositories
Handle database operations and reusable queries.

---

# 📁 Folder Structure

```text
smartems_flask/
│
├── models/
├── routes/
├── services/
├── repositories/
├── middleware/
├── schemas/
├── utils/
├── migrations/
├── extensions.py
├── config.py
└── app.py
```

---

# 📌 Folder Responsibilities

## models/
SQLAlchemy database models.

## routes/
API endpoint definitions.

## services/
Business logic implementation.

## repositories/
Database access layer.

## middleware/
JWT role authorization middleware.

## schemas/
Marshmallow validation schemas.

## utils/
Reusable helper utilities:
- password hashing
- pagination
- exceptions
- API response formatting

## extensions.py
Centralized Flask extension initialization.

---

# 🔐 Authentication Flow

JWT-based authentication is implemented using Flask-JWT-Extended.

After successful login:
- Backend generates JWT token
- Frontend stores token
- Token is sent in Authorization header
- Protected APIs validate JWT token

---

# 🗄️ Database

Database: MySQL

Main Tables:
- Users
- Employees
- Departments
- Designations
- Attendance
- LeaveRequests
- CorrectionRequests

---

# 📦 Key Concepts Implemented

- JWT Authentication
- Role-Based Authorization
- Pagination
- Search Filtering
- Transactions
- Global Error Handling
- Validation using Marshmallow
- Attendance Workflow
- Leave Workflow
- Correction Approval Workflow
- Eager Loading Optimization

---

# ⚙️ Setup Instructions

## 1. Clone Repository

```bash
git clone <repo-url>
```

---

## 2. Navigate to Project

```bash
cd smartems_flask
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\\Scripts\\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Configure Environment Variables

Create `.env`

Example:

```env
SECRET_KEY=your_secret
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=mysql+pymysql://root:password@localhost/smartems_flask
```

---

## 7. Run Database Migrations

```bash
flask db upgrade
```

---

## 8. Run Application

```bash
python app.py
```

---

# 🌐 API Base URL

```text
http://localhost:5000/api
```

---

# 🎯 Learning Outcome

This project helped me understand:
- Flask Backend Architecture
- REST API Design
- JWT Authentication
- ORM using SQLAlchemy
- Database Relationships
- Clean Architecture
- Workflow-Based Business Logic
- Transactions & Error Handling

---

# 👨‍💻 Author

Karthick K
