from marshmallow import fields

from flask_poetry_api import ma
from flask_poetry_api.models.user_model import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model: UserModel = UserModel
        load_instance: bool = True
        fields: tuple = ('id', 'name', 'email', 'password')

    name: str = fields.String(required=True)
    email: str = fields.String(required=True)
    password: str = fields.String(required=True)
