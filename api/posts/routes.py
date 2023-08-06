from flask import Blueprint, request, jsonify
from .db_models import Post
from ..users.db_models import User
from .schemas import PostSchema,PostCreateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from apifairy import body


posts_bp = Blueprint("posts", __name__)


@posts_bp.post("/new/post/")
@jwt_required()
@body(PostCreateSchema)
def create_a_post(args):
    """Create a post"""

    try:
        username = get_jwt_identity()
        print(username)

        author = User.query.filter_by(username=username).first()

        new_post = Post(**args)

        new_post.user_id = author.id

        new_post.save()

        return jsonify(
            {
                "status": 200,
                "message": "Post has been created",
                "post": {"id": new_post.id},
            }
        )

    except Exception as e:
        return jsonify({"error": "Oops! Something went wrong","detail":str(e)}), 400


@posts_bp.get("/posts/")
def list_all_posts():
    """List all posts"""

    try:
        page_number = int(request.args.get("page", None))
        per_page = int(request.args.get("posts", None))

        posts = Post.get_all(page_number=page_number, per_page=per_page)

        post_list = PostSchema().dump(posts, many=True)
    except:
        return jsonify({"error": "Opps! Something is wrong "})
    finally:
        posts = Post.query.all()

        post_list = PostSchema().dump(posts, many=True)
        return jsonify({"status": 200, "posts": post_list}), 200
