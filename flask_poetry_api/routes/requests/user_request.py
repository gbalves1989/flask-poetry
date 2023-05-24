from pydantic import BaseModel, Field


class UserBody(BaseModel):
    name: str = Field(min_length=3, max_length=80, description='user name')
    email: str = Field(max_length=120, description='user email')
    password: str = Field(
        min_length=10, max_length=20, description='user password'
    )


class LoginBody(BaseModel):
    email: str = Field(max_length=120, description='user email')
    password: str = Field(
        min_length=10, max_length=20, description='user password'
    )


class AuthorizationQuery(BaseModel):
    authorization: str = Field(description='user token')
