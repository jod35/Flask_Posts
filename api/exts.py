# a module for loading Flask third party extensions

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title="Flask Posts",
    doc="/",
    version="1.0",
    description="As simple REST API built for a simple posts service",
)
jwt = JWTManager()
