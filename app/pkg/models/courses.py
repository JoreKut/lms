import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import root_validator
from .exceptions import UpdateModelError
from app.pkg.models.base import BaseApiModel


class BaseCourse(BaseApiModel):
    pass


class CourseModel(BaseCourse):
    id: UUID
    created_at: datetime.datetime
    title: str
    description: Optional[str]


class CourseModelWithLectures(CourseModel):
    lecturer_ids: List[str]


class DeleteCourseByIdCommand(BaseCourse):
    id: UUID


class CreateCourseCommand(BaseCourse):
    title: str
    description: Optional[str]
    lecturer_ids: List[UUID]


class ReadCourseById(BaseCourse):
    course_id: str


class AddCourseToLecturer(BaseCourse):
    course_id: UUID
    lecturer_id: UUID


class UpdateCourseCommand(BaseCourse):
    id: UUID
    title: Optional[str]
    description: Optional[str]

    @root_validator
    def validate_none_fields(cls, v):
        if not any(
            (
                v.get("title", None),
                v.get("description", None),
            )
        ):
            raise UpdateModelError
