# Configuration file with hardcoded values
DATABASE_URL = "sqlite:///tasks.db"
SECRET_KEY = "my-secret-key-123"  # Hardcoded secret!
API_BASE_URL = "http://localhost:5000"
DEBUG = True

# Admin credentials (VERY BAD!)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Email settings (hardcoded)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "admin@company.com"
EMAIL_PASSWORD = "gmail_password_123"  # Plain text password!

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY
