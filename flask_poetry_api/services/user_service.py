import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Response, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from flask_poetry_api.entities.user_entity import UserEntity
from flask_poetry_api.models.user_model import UserModel
from flask_poetry_api.repositories.user_repository import UserRepository
from flask_poetry_api.routes.requests.user_request import (
    AuthorizationQuery,
    LoginBody,
    UserBody,
)
from flask_poetry_api.schemas.user_schema import UserSchema

load_dotenv()


class UserService:
    def create_user(request: UserBody) -> Response:
        user_schema: UserSchema = UserSchema()

        user_entity: UserEntity = UserEntity(
            name=request.name, email=request.email, password=request.password
        )

        user_db: UserModel = UserRepository.create(user_entity)
        return make_response(user_schema.jsonify(user_db), 201)

    def login_user(request: LoginBody) -> Response:
        user_db: UserModel = UserRepository.find_by_email(request.email)

        if user_db and user_db.check_password(password=request.password):
            access: str = create_access_token(
                identity=user_db.id,
                expires_delta=timedelta(
                    seconds=int(os.environ.get('EXPIRES_DELTA'))
                ),
            )

            refresh: str = create_refresh_token(identity=user_db.id)

            return make_response(
                jsonify(
                    {
                        'access_token': access,
                        'refresh_token': refresh,
                        'message': 'Login are successfully',
                    }
                ),
                200,
            )

        return make_response(
            jsonify({'message': "Credentials aren't valid"}), 401
        )

    def refresh_token(query: AuthorizationQuery) -> Response:
        user_token: str = query.authorization

        access: str = create_access_token(
            identity=user_token,
            expires_delta=timedelta(
                seconds=int(os.environ.get('EXPIRES_DELTA'))
            ),
        )

        refresh: str = create_refresh_token(identity=user_token)

        return make_response(
            {'access_token': access, 'refresh_token': refresh}, 200
        )
