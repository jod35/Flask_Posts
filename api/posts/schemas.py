from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .db_models import Post


class PostSchema(SQLAlchemySchema):
    class Meta:
        model = Post

    id = auto_field()
    title = auto_field()
    body = auto_field()
    date_created = auto_field()


class PostCreateSchema(SQLAlchemySchema):
    class Meta:
        model = Post

    title = auto_field()
    body = auto_field()
