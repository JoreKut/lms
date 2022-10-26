import datetime
import decimal
from typing import Optional
from uuid import UUID
from app.pkg.models.base import BaseApiModel


class BaseUser(BaseApiModel):
    pass


class UserModel(BaseUser):
    id: UUID
    created_at: datetime.datetime
    hashed_password: Optional[str]
    username: str
    phone: Optional[str]
    email: Optional[str]
    firstname: str
    lastname: str


class User(BaseUser):
    id: UUID
    username: str
    phone: Optional[str]
    email: Optional[str]
    firstname: str
    lastname: str


class AuthorizationForm(BaseUser):
    email: str
    password: str
    username: Optional[str]
    phone: Optional[str]


class RegistrationForm(BaseUser):
    username: str
    email: str
    password: str
    phone: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]


class CreateUserCommand(BaseUser):
    email: str
    username: str
    hashed_password: str
    phone: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]


class ReadUserByEmailCommand(BaseUser):
    email: str


class ReadCoursesByUserCommand(BaseApiModel):
    id: UUID


class ReadLectureById(BaseApiModel):
    course_id: UUID


class ReadLectureByCourseId(BaseApiModel):
    course_id: UUID


class ReadLectureByDatetime(BaseApiModel):
    course_id: UUID
    starts_at: datetime.date


class ReadLecturesByDate(BaseApiModel):
    user_id: UUID
    lecture_date: datetime.date


class ReadUserByIdentifier(BaseUser):
    email: Optional[str]
    username: Optional[str]


class ReadUserByPhoneCommand(BaseUser):
    phone: str


class ReadUserByIdCommand(BaseUser):
    id: str


class UpdateBalanceCommand(BaseUser):
    user_id: str
    addition: decimal.Decimal


class SubscribeCourseCommand(BaseApiModel):
    user_id: Optional[UUID]
    course_id: UUID


class ReadLecturesCommandAtDate(BaseApiModel):
    date: datetime.datetime


class ReadLecturesBetweenCommand(BaseApiModel):
    user_id: UUID
    start: datetime.datetime
    end: datetime.datetime


class AddLectureCommand(BaseApiModel):
    id: UUID
    lecture_id: UUID
