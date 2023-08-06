# a module for loading Flask third party extensions

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apifairy import APIFairy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
api = APIFairy()
jwt = JWTManager()
