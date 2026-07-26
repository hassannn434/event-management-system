import os


class Config:
    """Application configuration settings."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "event-mgmt-secret-key-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # MySQL database configuration
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    DB_NAME = os.environ.get("DB_NAME", "event_management")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))

    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Pagination
    ITEMS_PER_PAGE = 9
