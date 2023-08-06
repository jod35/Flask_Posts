from flask import Blueprint, jsonify, request
from apifairy import body, response
from .schemas import UserSignUpSchema, UserLoginSchema, UserSchema
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from .db_models import User

users_bp = Blueprint("users", __name__)


@users_bp.post("/user/register")
def register():
    """Create a user account
    """
    data = request.get_json()

    user_exists = User.username_exists(data.get("username"))

    if not user_exists and (data.get("password") == data.get("repeat_password")):
        try:
            new_user = User(
                username=data.get("username"), phone_number=data.get("phone_number")
            )

            new_user.set_password(data.get("password"))

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
def login():
    """Login to user account"""

    data = request.get_json()
    user = User.query.filter_by(phone_number=data.get("phone_number")).first()

    if user and user.check_password(data.get("password")):
        token_pair = {
            "access": create_access_token(identity=user.username),
            "refresh": create_refresh_token(identity=user.username),
        }

        return (
            jsonify(
                {
                    "status": 200,
                    "message": "User logged in successfully",
                    "user": {
                        "name": user.username,
                        "phone_number": user.phone_number.national,
                    },
                    "token_pair": token_pair,
                }
            ),
            200,
        )

    return jsonify({"error": "Inavlid phone number or password"}), 400


@users_bp.get("/users")
@jwt_required()
def list_all_users():
    page_number = int(request.args.get("page", None))
    per_page = int(request.args.get("users"))

    user_list = User.get_all(page_number=page_number, per_page=per_page)

    users = UserSchema().dump(user_list, many=True)

    return jsonify({"status": 200, "users": users})
