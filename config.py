import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Configuration Class"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///todo.db")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key_here")
    JWT_ACCESS_TOKEN_EXPIRES = 7200  # 2 hour in seconds


class DevConfig(Config):
    """Development Configuration Class"""

    DEBUG = True


class TestConfig(Config):
    """Development Configuration Class"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_todo.db"


class ProdConfig(Config):
    """Production Configuration Class"""

    DEBUG = True


config = {
    "dev": DevConfig,
    "testing": TestConfig,
    "prod": ProdConfig,
    "default": DevConfig,
}
