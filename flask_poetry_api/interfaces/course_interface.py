from abc import ABC, abstractmethod
from typing import List

from flask_poetry_api.entities.course_entity import CourseEntity
from flask_poetry_api.models.course_model import CourseModel


class CourseInteface(ABC):
    @abstractmethod
    def create(entity: CourseEntity) -> CourseModel:
        pass

    @abstractmethod
    def find_all() -> List[CourseModel]:
        pass

    @abstractmethod
    def find_by_id(course_id: int) -> CourseModel:
        pass

    @abstractmethod
    def update(course_db: CourseModel, course_entity: CourseEntity) -> None:
        pass

    @abstractmethod
    def delete(course_db: CourseModel) -> None:
        pass

    @abstractmethod
    def find_last_register() -> CourseModel:
        pass
