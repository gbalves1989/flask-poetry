from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(description='user id')
    name: str = Field(description='user name')
    email: str = Field(description='user email')
    password: str = Field(description='user password')


class LoginResponse(BaseModel):
    access_token: str = Field(description='token access')
    refresh_token: str = Field(description='token refresh')
    message: str = Field(description='message to return')


class RefreshResponse(BaseModel):
    access_token: str = Field(description='token access')
    refresh_token: str = Field(description='token refresh')


class UnauthorizedResponse(BaseModel):
    message: str = Field(description="Credentials aren't valid.")
