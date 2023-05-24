from typing import List

from flask import Response, make_response

from flask_poetry_api.entities.course_entity import CourseEntity
from flask_poetry_api.models.course_model import CourseModel
from flask_poetry_api.repositories.course_repository import CourseRespository
from flask_poetry_api.routes.requests.course_request import (
    CourseBody,
    CoursePath,
)
from flask_poetry_api.schemas.course_schema import CourseSchema


class CourseService:
    def create_course(request: CourseBody) -> Response:
        course_schema: CourseSchema = CourseSchema()

        course_entity: CourseEntity = CourseEntity(
            name=request.name, description=request.description
        )

        course_model: CourseModel = CourseRespository.create(course_entity)
        return make_response(course_schema.jsonify(course_model), 201)

    def list_courses() -> Response:
        course_schema: CourseSchema = CourseSchema(many=True)
        courses_model: List[CourseModel] = CourseRespository.find_all()
        return make_response(course_schema.jsonify(courses_model), 200)

    def show_course(course_id: int) -> Response:
        course_schema: CourseSchema = CourseSchema()
        course_db: CourseModel = CourseRespository.find_by_id(course_id)

        if course_db is None:
            return make_response({'message': 'Course not found'}, 404)

        return make_response(course_schema.jsonify(course_db), 200)

    def update_course(course_id: int, request: CourseBody) -> Response:
        course_schema: CourseSchema = CourseSchema()
        course_db: CourseModel = CourseRespository.find_by_id(course_id)

        if course_db is None:
            return make_response({'message': 'Course not found'}, 404)

        course_entity: CourseEntity = CourseEntity(
            name=request.name, description=request.description
        )

        CourseRespository.update(course_db, course_entity)
        course: CourseModel = CourseRespository.find_by_id(course_id)
        return make_response(course_schema.jsonify(course), 202)

    def delete_course(course_id: int) -> Response:
        course_db: CourseModel = CourseRespository.find_by_id(course_id)

        if course_db is None:
            return make_response({'message': 'Course not found'}, 404)

        CourseRespository.delete(course_db)
        return make_response(
            {'content': 'Course removed with successfully'}, 204
        )
