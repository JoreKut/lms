import datetime
from typing import Optional
from uuid import UUID

from pydantic import root_validator
from .exceptions import UpdateModelError
from app.pkg.models.base import BaseApiModel


class BaseLecture(BaseApiModel):
    pass


class LectureModel(BaseLecture):
    id: UUID
    created_at: datetime.datetime
    title: str
    description: Optional[str]
    starts_at: datetime.datetime


class DeleteLectureByIdCommand(BaseLecture):
    id: UUID


class CreateLectureCommand(BaseLecture):
    title: str
    description: Optional[str]
    course_id: UUID
    starts_at: Optional[datetime.datetime]


class UpdateLectureCommand(BaseLecture):
    id: UUID
    title: Optional[str]
    description: Optional[str]
    course_id: Optional[UUID]
    starts_at: Optional[datetime.datetime]

    @root_validator
    def validate_none_fields(cls, v):
        if not any(
            (
                v.get("title", None),
                v.get("description", None),
                v.get("course_id", None),
                v.get("starts_at", None),
            )
        ):
            raise UpdateModelError
