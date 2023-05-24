from sqlalchemy import desc

from flask_poetry_api import db
from flask_poetry_api.entities.user_entity import UserEntity
from flask_poetry_api.interfaces.user_interface import UserInterface
from flask_poetry_api.models.user_model import UserModel


class UserRepository(UserInterface):
    def create(entity: UserEntity) -> UserModel:
        user_db: UserModel = UserModel(
            name=entity.name, email=entity.email, password=entity.password
        )

        user_db.encrypt_password()
        db.session.add(user_db)
        db.session.commit()
        return user_db

    def find_by_email(email: str) -> UserModel:
        return UserModel.query.filter_by(email=email).first()

    def find_by_id(user_id: int) -> UserModel:
        return UserModel.query.filter_by(id=user_id).first()

    def find_last_register() -> UserModel:
        return UserModel.query.order_by(desc(UserModel.id)).first()
