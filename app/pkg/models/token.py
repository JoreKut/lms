from app.pkg.models.base import BaseApiModel


class BaseToken(BaseApiModel):
    pass


class ReadAccessTokenByUserId(BaseToken):
    user_id: str


class ReadRefreshTokenByUserId(BaseToken):
    user_id: str


class TokenPayload(BaseToken):
    id: str
    expired: str


class Auth(BaseToken):
    access_token: str
    refresh_token: str


class TokenModel(BaseToken):
    token: str
    user_id: str


class CreateTokenCommand(TokenModel):
    pass


class ReadTokenCommand(CreateTokenCommand):
    pass


class ReadTokenByUserCommand(BaseToken):
    user_id: str


class DeleteTokenCommand(BaseToken):
    token: str


class DeleteAllTokenByUserCommand(BaseToken):
    user_id: str


class ReadUserByTokenCommand(BaseToken):
    token: str
