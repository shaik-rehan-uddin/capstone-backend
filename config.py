import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("DB_USER")

CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTH_TYPE = 1
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "Intelli-Edge Chatbot API"
FAB_API_SWAGGER_UI = True
