from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag

from flask_poetry_api import app
from flask_poetry_api.routes.requests.course_request import (
    CourseBody,
    CoursePath,
)
from flask_poetry_api.routes.responses.course_response import (
    CourseListResponse,
    CourseResponse,
    ErrorsResponse,
    NoContentResponse,
)
from flask_poetry_api.services.course_service import CourseService

tag: Tag = Tag(name='Courses', description='List of routes')
api_courses: APIBlueprint = APIBlueprint(
    'courses', __name__, url_prefix='/api/v1/courses', abp_tags=[tag]
)


@api_courses.post(
    '/',
    summary='Create a new course',
    description='Responsible to create and return a new course',
    responses={'201': CourseResponse},
)
@jwt_required()
async def store(body: CourseBody):
    return CourseService.create_course(body)


@api_courses.get(
    '/',
    summary='Return a list of courses',
    description='Responsible to return a list of courses',
    responses={'200': CourseListResponse},
)
@jwt_required()
async def index():
    return CourseService.list_courses()


@api_courses.get(
    '/<int:course_id>/',
    summary='Return some course by id',
    description='Responsible to return some course by id',
    responses={'200': CourseResponse, '404': ErrorsResponse},
)
@jwt_required()
async def show(path: CoursePath):
    return CourseService.show_course(path.course_id)


@api_courses.put(
    '/<int:course_id>/',
    summary='Update the data course by id',
    description='Responsible to update the data course by id',
    responses={'202': CourseResponse, '404': ErrorsResponse},
)
@jwt_required()
async def update(path: CoursePath, body: CourseBody):
    return CourseService.update_course(path.course_id, body)


@api_courses.delete(
    '/<int:course_id>/',
    summary='Remove some course by id',
    description='Responsible to remove some course by id',
    responses={'204': NoContentResponse, '404': ErrorsResponse},
)
@jwt_required()
async def delete(path: CoursePath):
    return CourseService.delete_course(path.course_id)


app.register_api(api_courses)
