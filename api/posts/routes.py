from flask import Blueprint, request, jsonify
from .db_models import Post,Invitation
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
    Delete a post by id

    """
    post = Post.query.filter_by(id=id).first()

    post.delete()
    
    return {} , 204



@posts_bp.post('/post/<int:post_id>/invite_user/<string:username>')
@jwt_required()
def invite_user(post_id, username):
    """Invite a user to view a post

    Args:
        post_id (int): ID of post a user is to view
        username (str): username of a user to be invited
    """

    #get logged in user from JWT
    current_username = get_jwt_identity()

    sender =  User.query.filter_by(username=current_username).first()
    
    sender_id = sender.id

    #query for receiver via id provided in path param
    receiver = User.query.filter_by(username=username).first()

    receiver_id = receiver.id

    #get the post you want to invite a user to view
    post = Post.get_by_id(post_id)

    #handle sending invitation to missing receiver
    if not (receiver and post):
        return jsonify({'message': 'Invalid receiver, or post ID'}), 404

    #check if invitation has already been sent
    invitation = Invitation.query.filter_by(sender_id=sender_id, receiver_id=receiver_id, post_id=post_id).first()

    if invitation:
        return jsonify({'message': 'Invitation already sent'}), 400

    #create invitation
    invitation = Invitation(sender_id=sender_id, receiver_id=receiver_id, post_id=post_id)
    db.session.add(invitation)
    db.session.commit()

    return jsonify({"status": 200, "message":  f"{username} has been invited to {post.title}"}), 201



@posts_bp.put('/posts/<int:invitation_id>/accept')
def accept_invitation(invitation_id):
    """Accept Invitation

    Args:
        invitation_id (int): ID of invitation to accept
    """
    invitation = Invitation.query.get(invitation_id)

    if not invitation:
        return jsonify({'message': 'Invitation not found'}), 404

    invitation.accepted = True
    db.session.commit()

    return jsonify({'message': 'Invitation accepted successfully'}), 200


@posts_bp.put('/post/<int:post_id>/revoke_user_invite/<string:username>/')
@jwt_required()
def revoke_invitation(post_id,username):
    """Revoke user invitation

    Args:
        post_id (int): ID of post to revoke access from
        username (_type_): Username of the user whose access if to revoked
    """
    post = Post.query.get_or_404(post_id)
    receiver = User.query.filter_by(username = username).first()

    #current user's name
    _user_name = get_jwt_identity()

    current_user = User.query.filter_by(username = _user_name).first()


    invitation = Invitation.query.filter(sender_id = current_user.id, receiver_id = receiver.id,post_id=post.id)

    db.session.delete(invitation)
    db.session.commit()

    return jsonify({"status": 200, "message": f"Username access has been revoked to {post.title}"}), 200