from flask_openapi3 import APIBlueprint, Tag

from flask_poetry_api import app
from flask_poetry_api.routes.requests.user_request import (
    AuthorizationQuery,
    LoginBody,
    UserBody,
)
from flask_poetry_api.routes.responses.user_response import (
    LoginResponse,
    RefreshResponse,
    UnauthorizedResponse,
    UserResponse,
)
from flask_poetry_api.services.user_service import UserService

tag: Tag = Tag(name='Users', description='List of users')
api_user: APIBlueprint = APIBlueprint(
    'users', __name__, url_prefix='/api/v1/users', abp_tags=[tag]
)


@api_user.post(
    '/',
    summary='create a new user',
    description='Responsible to create and return a new user',
    responses={'201': UserResponse},
)
async def store(body: UserBody):
    return UserService.create_user(body)


@api_user.post(
    '/login/',
    summary='login user',
    description='Responsible to login user and return a access token',
    responses={'200': LoginResponse, '401': UnauthorizedResponse},
)
async def login(body: LoginBody):
    return UserService.login_user(body)


@api_user.post(
    '/token/refresh',
    summary='refresh token to access',
    description='Responsible to refresh token to new access',
    responses={'200': RefreshResponse},
)
async def refresh(query: AuthorizationQuery):
    return UserService.refresh_token(query)


app.register_api(api_user)
