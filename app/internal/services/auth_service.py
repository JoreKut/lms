from app.pkg.models import *
from app.internal.pkg.access_token import (
    UnAuthorized,
    TokenTimeExpired,
    NonUniqueUser,
    BadRequest
)
from app.internal.repository import (
    AccessTokenRepository,
    RefreshTokenRepository
)
from app.internal.services.user_service import UserService
from fastapi import Depends

from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from app.pkg import cryptography
import jwt
from datetime import datetime, timedelta
from app.pkg.settings import settings
from app.pkg.cryptography import sha256_encode_password


class AuthService:

    user_service: UserService
    http_bearer = HTTPBearer()
    access_token_repository: AccessTokenRepository
    refresh_token_repository: RefreshTokenRepository

    def __init__(
        self,
        user_service: UserService,
        access_token_repository: AccessTokenRepository,
        refresh_token_repository: RefreshTokenRepository
    ):
        self.access_token_repository = access_token_repository
        self.refresh_token_repository = refresh_token_repository
        self.user_service = user_service

    @staticmethod
    def __is_token_expired(expired_datetime: str) -> bool:
        if datetime.strptime(expired_datetime, '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
            return True

    @staticmethod
    async def get_jwt_token(
        token_bearer: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        return token_bearer.credentials

    async def get_user(
        self,
        token_bearer: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> User:
        jwt_token = token_bearer.credentials
        try:
            # Если токен подлинный, возвращаем пользователя
            payload = cryptography.get_payload(jwt_token)

            await self.access_token_repository.read_all_by_token(
                ReadUserByTokenCommand(
                    token=jwt_token
                )
            )

            if self.__is_token_expired(payload.expired):
                await self.access_token_repository.delete(
                    DeleteTokenCommand(
                        token=jwt_token
                    )
                )
                raise TokenTimeExpired

            user = await self.user_service.read_user_by_id(
                ReadUserByIdCommand(
                    id=payload.id
                )
            )
            return user
        except jwt.exceptions.InvalidSignatureError:
            raise UnAuthorized

    async def generate_token_pair(self, user: User) -> Auth:
        access_token = await self.generate_access_token(user)
        refresh_token = await self.generate_refresh_token(user)

        await self.access_token_repository.create(
            CreateTokenCommand(
                token=access_token,
                user_id=str(user.id)
            )
        )

        await self.refresh_token_repository.create(
            CreateTokenCommand(
                token=refresh_token,
                user_id=str(user.id)
            )
        )

        return Auth(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def sign_up(
        self,
        cmd: RegistrationForm
    ) -> Auth:

        user = await self.user_service.read_user_by_identifier(
            ReadUserByIdentifier(
                email=cmd.email,
                username=cmd.username
            )
        )

        if user is not None:
            raise NonUniqueUser

        user = await self.user_service.create_user(cmd)

        return await self.generate_token_pair(user)

    async def login(self, cmd: AuthorizationForm) -> Auth:
        # If user in DB -> create ACCESS\REFRESH pair
        # Else info about it

        user = await self.user_service.read_user_by_identifier(
            ReadUserByIdentifier(
                email=cmd.email,
                username=cmd.username
            )
        )

        if user is None or not sha256_encode_password(settings.HMAC_KEY, cmd.password) == user.hashed_password:
            raise BadRequest

        return await self.generate_token_pair(
            User(
                id=user.id,
                username=user.username,
                phone=user.phone,
                email=user.email,
                firstname=user.firstname,
                lastname=user.lastname
            )
        )

    async def logout(self, cmd: DeleteAllTokenByUserCommand):
        await self.access_token_repository.delete_by_user(cmd)
        await self.refresh_token_repository.delete_by_user(cmd)

    @staticmethod
    async def generate_access_token(
        user: User
    ) -> str:
        access_payload = TokenPayload(
            id=str(user.id),
            expired=str(datetime.now() + timedelta(minutes=15))
        )
        access_token = cryptography.get_jwt_from_data(access_payload.__dict__)

        return access_token

    @staticmethod
    async def generate_refresh_token(
        user: User
    ) -> str:
        refresh_payload = TokenPayload(
            id=str(user.id),
            expired=str(datetime.now() + timedelta(days=3))
        )
        refresh_token = cryptography.get_jwt_from_data(refresh_payload.__dict__)

        return refresh_token

    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> str:
        try:
            # Если токен подлинный, возвращаем пользователя
            refresh_payload = cryptography.get_payload(refresh_token)

            if self.__is_token_expired(refresh_payload.expired):
                await self.access_token_repository.delete(
                    DeleteTokenCommand(
                        token=refresh_token
                    )
                )
                raise TokenTimeExpired

            resp = await self.refresh_token_repository.read_all_by_token(
                ReadUserByTokenCommand(
                    token=refresh_token
                )
            )

            if resp is None:
                raise UnAuthorized

            user = await self.user_service.read_user_by_id(
                ReadUserByIdCommand(id=refresh_payload.id)
            )

            await self.access_token_repository.delete()
            access_token = await self.generate_access_token(user)

            await self.access_token_repository.create(
                CreateTokenCommand(
                    token=access_token,
                    user_id=str(user.id)
                )
            )

            return access_token

        except jwt.exceptions.InvalidSignatureError:
            raise UnAuthorized
