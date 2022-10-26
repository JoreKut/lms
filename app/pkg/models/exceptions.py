from .base import BaseApiException
from fastapi import status


class UpdateModelError(BaseApiException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "At least one field should be given"
