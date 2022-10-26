from fastapi import status

from app.pkg.models.base import BaseApiException

__all__ = [
    "UnAuthorized",
    "TokenTimeExpired",
    "WrongToken",
    "CSRFError",
    "InvalidRefreshSession",
    "NonUniqueUser",
    "BadRequest"
]


class BadRequest(BaseApiException):
    message = "Incorrect params"
    status_code = status.HTTP_400_BAD_REQUEST


class UnAuthorized(BaseApiException):
    message = "Not authorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class TokenTimeExpired(BaseApiException):
    message = "Token time expired"
    status_code = status.HTTP_401_UNAUTHORIZED


class WrongToken(BaseApiException):
    def __init__(self, message: Exception = None):
        if message:
            self.message = f"Wrong token: {message}"

    message = "Wrong token"
    status_code = status.HTTP_401_UNAUTHORIZED


class CSRFError(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "CSRF double submit tokens do not match"


class InvalidRefreshSession(BaseApiException):
    status_code = status.HTTP_403_FORBIDDEN  # Think
    message = "Invalid refresh session"


class NonUniqueUser(BaseApiException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE  # Think
    message = "There is a user with the same email or username"
