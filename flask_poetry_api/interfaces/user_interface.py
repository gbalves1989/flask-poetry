from abc import ABC, abstractmethod

from flask_poetry_api.entities.user_entity import UserEntity
from flask_poetry_api.models.user_model import UserModel


class UserInterface(ABC):
    @abstractmethod
    def create(entity: UserEntity) -> UserModel:
        pass

    @abstractmethod
    def find_by_email(email: str) -> UserModel:
        pass

    @abstractmethod
    def find_by_id(user_id: int) -> UserModel:
        pass
