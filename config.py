from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

def generate_secure_key(length=32):
    salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=200000,  # Increased iterations for better security
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(os.urandom(16)))
    return key.decode('utf-8')

class Config:
    jwt_secret_key = generate_secure_key()
    flask_secret_key = generate_secure_key()
    secret_key = generate_secure_key()

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///local_development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = jwt_secret_key
    SECRET_KEY = flask_secret_key
    SECRET_KEY= secret_key
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # Add SameSite attribute for cookies
    REMEMBER_COOKIE_SAMESITE = 'Lax'  # Add SameSite attribute for cookies
    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 1025))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'noreply@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_password')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@example.com')