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
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(id=id).first()

    @classmethod
    def get_all(cls, page_number, per_page):
        return cls.query.paginate(page_number, per_page)


# database model for in
class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(255), db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.String(255), db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    accepted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Invitation {self.id}>"
