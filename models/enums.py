import enum

class UserRole(enum.Enum):
    Admin = "Admin"
    Employee = "Employee"

class AccountStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"
    
    