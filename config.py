import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")

    # Session configuration
    SESSION_EXPIRATION_SECS = int(os.getenv("SESSION_EXPIRATION_SECS", 2592000))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    JWT_EXPIRATION_SECS = int(os.getenv("JWT_EXPIRATION_SECS", 900))
