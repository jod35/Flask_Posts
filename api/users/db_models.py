from ..exts import db
from datetime import datetime
from sqlalchemy_utils import PhoneNumber
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

"""
class User:
    - username
    - phone number
    - password
"""


# database model for Users
class User(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4), unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    _phone_number = db.Column(db.String(20))
    country_code = db.Column(db.String(8))
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        country_code
    )
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_phone_number(self,phone_number):
        self.phone_number = PhoneNumber(phone_number,"UG")


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def username_exists(cls, username):
        return (
            db.session.query(cls.username).filter_by(username=username).first()
            is not None
        )
