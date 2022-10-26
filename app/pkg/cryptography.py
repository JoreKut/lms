import hmac
from app.pkg.models import TokenPayload
import jwt
from app.pkg.settings import settings


def sha256_encode_password(
    key: str,
    body: str
):
    hashed_password = hmac.new(
        key=key.encode() if key else bytes(),
        msg=body.encode(),
        digestmod="sha256",
    ).hexdigest()

    return hashed_password


def get_payload(jwt_token: str) -> TokenPayload:
    token_payload = jwt.decode(jwt_token, key=settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
    payload = TokenPayload(**token_payload)
    return payload


def get_jwt_from_data(data: dict):
    encoded_jwt = jwt.encode(data, key=settings.JWT_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
