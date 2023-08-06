# a module for input and output schemas (serializers)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import marshmallow as ma
from .db_models import User


class UserSignUpSchema(SQLAlchemySchema):
    class Meta:
        model = User
        description = "This schema allows a user to create a user account"

    username = auto_field(required=True)
    phone_number = auto_field()
    password = auto_field()
    repeat_password = ma.fields.String(required=True)


class UserLoginSchema(SQLAlchemySchema):
    class Meta:
        model = User

    phone_number = ma.fields.String()
    password = ma.fields.String()


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.fields.String()
    username = ma.fields.String()
    phone_number = ma.fields.String()
