# a module for input and output schemas (serializers)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import marshmallow as ma
from .db_models import User



class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.fields.String()
    username = ma.fields.String()
    phone_number = ma.fields.String()
