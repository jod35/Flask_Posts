from ..exts import db
from datetime import datetime


"""
class Post:
 - id
 - title
 - body
 - created_at
 
"""


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"Post {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(id=id).first()

    @classmethod
    def get_all(cls, page_number, per_page):
        return cls.query.paginate(page_number, per_page)
