from typing import List

from app.pkg.cryptography import sha256_encode_password
from app.pkg.models import *
from app.internal.repository import UserRepository
from app.pkg.settings import settings


class UserService:

    user_repository: UserRepository

    def __init__(
        self,
        user_repository: UserRepository
    ):
        self.user_repository = user_repository

    async def read_user_by_email(
        self,
        cmd: ReadUserByEmailCommand
    ) -> UserModel:

        user: UserModel = await self.user_repository.read_by_email(cmd)

        return user

    async def read_user_by_identifier(
        self,
        cmd: ReadUserByIdentifier
    ) -> UserModel:

        user: UserModel = await self.user_repository.read_user_by_identifier(cmd)

        return user

    async def read_user_by_phone(
        self,
        cmd: ReadUserByPhoneCommand
    ) -> UserModel:

        user: UserModel = await self.user_repository.read_by_phone(cmd)

        return user

    async def read_user_by_id(
        self,
        cmd: ReadUserByIdCommand
    ) -> User:
        user = await self.user_repository.read_by_id(
            cmd
        )

        return User(
            id=user.id,
            username=user.username,
            phone=user.phone,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname
        )

    async def create_user(
        self,
        cmd: RegistrationForm
    ) -> User:
        user = await self.user_repository.create(
            CreateUserCommand(
                username=cmd.username,
                hashed_password=sha256_encode_password(settings.HMAC_KEY, cmd.password),
                phone=cmd.phone,
                email=cmd.email,
                firstname=cmd.firstname,
                lastname=cmd.lastname,
            )
        )

        return User(
            id=user.id,
            username=user.username,
            phone=user.phone,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname
        )

    async def read_lecture_by_date(
        self,
        cmd: ReadLecturesByDate
    ) -> List[LectureModel]:
        return await self.user_repository.read_lecture_for_course_by_date(cmd)

    async def subscribe_course(
        self,
        cmd: SubscribeCourseCommand
    ):
        return await self.user_repository.subscribe_course(cmd)
