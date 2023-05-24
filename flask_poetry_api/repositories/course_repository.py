from typing import List

from sqlalchemy import desc

from flask_poetry_api import db
from flask_poetry_api.entities.course_entity import CourseEntity
from flask_poetry_api.interfaces.course_interface import CourseInteface
from flask_poetry_api.models.course_model import CourseModel


class CourseRespository(CourseInteface):
    def create(entity: CourseEntity) -> CourseModel:
        course_db: CourseModel = CourseModel(
            name=entity.name, description=entity.description
        )

        db.session.add(course_db)
        db.session.commit()
        return course_db

    def find_all() -> List[CourseModel]:
        return CourseModel.query.all()

    def find_by_id(course_id: int) -> CourseModel:
        return CourseModel.query.filter_by(id=course_id).first()

    def update(course_db: CourseModel, course_entity: CourseEntity) -> None:
        course_db.name = course_entity.name
        course_db.description = course_entity.description
        db.session.commit()

    def delete(course_db: CourseModel) -> None:
        db.session.delete(course_db)
        db.session.commit()

    def find_last_course_register() -> CourseModel:
        return CourseModel.query.first()
