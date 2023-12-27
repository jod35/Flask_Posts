import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    FLASK_ENV = os.getenv("FLASK_ENV")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
