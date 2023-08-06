from flask import Blueprint, jsonify
from apifairy import body
from .schemas import UserSignUpSchema
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from .db_models import User

users_bp = Blueprint("users", __name__)


@users_bp.post("/user/register")
@body(UserSignUpSchema)
def register(args):
    """Create a user account

    Args:
        args (dict): a payload of data to create a user account
    """

    user_exists = User.username_exists(args.get("username"))

    schema = UserSignUpSchema()

    

    if not user_exists and (args.get("password") == args.get("repeat_password")):
        try:
            new_user = User(
                username=args.get("username"),
            )

            new_user.set_password(args.get('phone_number'))

            new_user.set_password(args.get("password"))

            new_user.save()

            return jsonify({"status": 200, "message": "User has been registered"}), 201

        except PhoneNumberParseException as e:
            return (
                jsonify({"message": "Oops, you may have entered a wrong number"}),
                400,
            )

    return jsonify({"message":"User account already exists"})
