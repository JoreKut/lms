from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateLecturerModel(BaseModel):
    firstname: str
    lastname: str
    patronymic: Optional[str]


class LecturerModel(BaseModel):
    id: UUID
    firstname: str
    lastname: str
    patronymic: Optional[str]
