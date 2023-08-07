# a module for loading Flask third party extensions

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api

db = SQLAlchemy() # the ORM 
migrate = Migrate() # for easy database migrations


# framework for helping us to create and document our endpoints with Swagger
api = Api(
    title="Flask Posts",
    doc="/",
    version="1.0",
    description="As simple REST API built for a simple posts service",
    security='apiKey', authorizations={
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
)
jwt = JWTManager()
