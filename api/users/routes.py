from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from .schemas import UserSignUpSchema, UserLoginSchema, UserSchema
from sqlalchemy_utils.types.phone_number import PhoneNumberParseException
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from .db_models import User

users_nspace = Namespace("users", "a namespace for users and auth")



#a parser for query params
user_parser = reqparse.RequestParser()
user_parser.add_argument('page', type=int, required=True, help='page is required')
user_parser.add_argument('users', type=int, required=True, help='users is required')



# a serialization/ validation model for signing up
register_model = users_nspace.model(
    "register_user",
    {
        "username": fields.String(),
        "phone_number": fields.String(),
        "password": fields.String(),
        "repeat_password": fields.String(),
    },
)



user_login_model = users_nspace.model(
    "login_user",{
        'phone_number' : fields.String(),
        'password': fields.String()
    }
)


@users_nspace.route("/user/register")
class RegisterUser(Resource):

    @users_nspace.expect(register_model)
    @users_nspace.response(201,"User has been created successfully")
    def post():
        """Create a user account"""
        data = users_nspace.payload #data coming from request

        user_exists = User.username_exists(data.get("username"))

        if not user_exists and (data.get("password") == data.get("repeat_password")):
            try:
                new_user = User(
                    username=data.get("username"), phone_number=data.get("phone_number")
                )

                new_user.set_password(data.get("password"))

                new_user.save()

                return (
                    jsonify({"status": 200, "message": "User has been registered"}),
                    201,
                )

            except PhoneNumberParseException as e:
                return (
                    jsonify({"message": "Oops, you may have entered a wrong number"}),
                    400,
                )

            except Exception as e:
                return jsonify({"error": str(e)})

        return jsonify({"message": "User account already exists"})


@users_nspace.route("/user/login/")
class LoginUser(Resource):

    @users_nspace.expect(user_login_model)
    @users_nspace.response(400, "Invalid Phonenumber or Password")
    @users_nspace.response(200, "Successful login")
    def post():
        """Login to user account"""

        data = users_nspace.payload
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


@users_nspace.route("/users")
class GetUsers(Resource):
    @jwt_required()
    @users_nspace.response(200,"")
    @users_nspace.doc(params={'page':'page number','users':'number of users'})
    def get():

        """Get paginated list of users
        """
        page_number = int(request.args.get("page", None))
        per_page = int(request.args.get("users"))

        user_list = User.get_all(page_number=page_number, per_page=per_page)

        users = UserSchema().dump(user_list, many=True)

        return jsonify({"status": 200, "users": users})
