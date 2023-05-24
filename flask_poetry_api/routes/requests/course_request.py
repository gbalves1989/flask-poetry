from pydantic import BaseModel, Field


class CoursePath(BaseModel):
    course_id: int = Field(description='course id')


class CourseBody(BaseModel):
    name: str = Field(min_length=3, max_length=100, description='course name')
    description: str = Field(max_length=180, description='course description')
