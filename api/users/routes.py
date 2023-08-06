from flask import Blueprint, jsonify
from apifairy import body
from .schemas import UserSignUpSchema, UserLoginSchema
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from flask_jwt_extended import create_access_token, create_refresh_token
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
                username=args.get("username"), phone_number=args.get("phone_number")
            )

            new_user.set_password(args.get("password"))

            new_user.save()

            return jsonify({"status": 200, "message": "User has been registered"}), 201

        except PhoneNumberParseException as e:
            return (
                jsonify({"message": "Oops, you may have entered a wrong number"}),
                400,
            )

        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify({"message": "User account already exists"})


@users_bp.post("/user/login/")
@body(UserLoginSchema)
def login(args):
    """Login to user account"""
    user = User.query.filter_by(phone_number=args.get("phone_number")).first()

    if user and user.check_password(args.get("password")):
        token_pair = {
            "access": create_access_token(identity=user.username),
            "refresh": create_refresh_token(identity=user.username),
        }

        return jsonify(
            {
                "status": 200,
                "message": "User logged in successfully",
                "user": {"name": user.username, "phone_number": user.phone_number.national},
                "token_pair": token_pair
            }
        )

    return "Hello`"
