from flask import Blueprint, request, jsonify
from .db_models import Post
from ..users.db_models import User
from .schemas import PostSchema,PostCreateSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from apifairy import body, response
from ..exts import db


posts_bp = Blueprint("posts", __name__)


@posts_bp.post("/new/post/")
@jwt_required()
def create_a_post(args):
    """Create a post"""
    data = request.get_json()

    try:
        username = get_jwt_identity()

        author = User.query.filter_by(username=username).first()

        new_post = Post(
            title = data.get('title'),
            body = data.get('body')
        )

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

        posts = Post.query.paginate(page=page_number,per_page=per_page)

        post_list = PostSchema().dump(posts, many=True)

        return jsonify({"status": 200, "posts": post_list}), 200
    except  Exception as e:
        return jsonify({"error": "Opps! Something is wrong ","error":str(e)})


@posts_bp.get("/post/<int:id>")
@jwt_required()
def get_post(id):
    """
    Retrieve a post by id

    """
    post = Post.query.filter_by(id=id).first()

    response = PostSchema().dump(post)
    
    return jsonify({"status": 200, "post": response})


@posts_bp.patch("/post/<int:id>")
@jwt_required()
def update_post(id):
    """
    Update a post by id

    """

    data = request.get_json()

    post = Post.query.filter_by(id=id).first()

    post.title = data.get('title')
    post.body = data.get('body')

    db.session.commit()

    response = PostSchema().dump(post)
    
    return jsonify({"status": 200, "post": response})


@posts_bp.delete( "/post/<int:id>")
@jwt_required()
def delete_post(id):
    """
    Retrieve a post by id

    """
    post = Post.query.filter_by(id=id).first()

    post.delete()
    
    return {} , 204