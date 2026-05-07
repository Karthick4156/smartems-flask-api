from flask import Flask
from config import Config
from extensions import db, migrate, jwt
from flask_cors import CORS

# Import models (for migrations)
from models.user import User
from models.employee import Employee
from models.department import Department
from models.designation import Designation
from models.attendance import Attendance
from models.leave_request import LeaveRequest
from models.correction_request import CorrectionRequest

from utils.validators import validate_schema
from utils.logger import setup_logger

from sqlalchemy.exc import IntegrityError


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    setup_logger(app)
    app.logger.info("App started successfully")
    
    # CORS (from .env)
    CORS(
        app,
        supports_credentials=True,
        origins=app.config.get("CORS_ORIGINS")
    )

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    from routes.auth_routes import auth_bp
    from routes.admin_employee_routes import admin_employee_bp
    from routes.department_routes import department_bp
    from routes.designation_routes import designation_bp
    from routes.employee_routes import employee_bp
    from routes.attendance_routes import attendance_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_employee_bp, url_prefix='/api/admin')
    app.register_blueprint(department_bp, url_prefix='/api/departments')
    app.register_blueprint(designation_bp, url_prefix='/api/designations')
    app.register_blueprint(employee_bp, url_prefix='/api/employee')
    app.register_blueprint(attendance_bp, url_prefix='/api/employee')

    # Health check
    @app.route("/")
    def health():
        return {"status": "SmartEMS Flask API running"}
    
    from utils.api_response import error_response
    from utils.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException)

    @app.errorhandler(BadRequestException)
    def handle_bad_request(e):
        return error_response(e.message, status=400)


    @app.errorhandler(NotFoundException)
    def handle_not_found(e):
        return error_response(e.message, status=404)


    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized(e):
        return error_response(e.message, status=401)


    @app.errorhandler(ForbiddenException)
    def handle_forbidden(e):
        return error_response(e.message, status=403)


    @app.errorhandler(Exception)
    def handle_exception(e):
        from flask import current_app

        current_app.logger.error(f"Unhandled error: {str(e)}")

        return error_response("Something went wrong", status=500)
    
    @app.errorhandler(IntegrityError)
    def handle_db_error(e):
        return error_response("Database constraint violation", status=400)
        
        
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config.get("FLASK_HOST", "127.0.0.1"),
        port=int(app.config.get("FLASK_PORT", 5000)),
        debug=app.config.get("DEBUG", False)
    )