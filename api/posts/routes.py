from flask import Blueprint


posts_bp = Blueprint("posts", __name__)


@posts_bp.get("/")
def list_all_posts():
    pass
