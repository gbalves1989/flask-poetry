from pydantic import BaseModel, Field


class CourseResponse(BaseModel):
    id: int = Field(description='course id')
    name: str = Field(description='course name')
    description: str = Field(description='course description')


class CourseListResponse(BaseModel):
    results: list[CourseResponse]


class NoContentResponse(BaseModel):
    content: str = Field(description='no content')


class ErrorsResponse(BaseModel):
    message: str = Field(description='error message')
