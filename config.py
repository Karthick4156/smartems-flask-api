import os
from dotenv import load_dotenv
import secrets

load_dotenv()

class Config:
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///smartems.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    jwt_secret = os.getenv('JWT_SECRET_KEY')

    if not jwt_secret:
        if os.getenv('FLASK_ENV') == 'development':
            jwt_secret = secrets.token_hex(32)
        else:
            raise ValueError("JWT_SECRET_KEY must be set")

    JWT_SECRET_KEY = jwt_secret
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 604800))

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')

    # Logging
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')