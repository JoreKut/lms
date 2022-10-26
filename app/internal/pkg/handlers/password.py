import random
import string

import bcrypt
from pydantic import SecretBytes

__all__ = ["crypt_password", "check_password", "generate_password"]


def crypt_password(password: bytes) -> bytes:
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_password(password: SecretBytes, hashed: SecretBytes) -> bool:
    return bcrypt.checkpw(password.get_secret_value(), hashed.get_secret_value())


def generate_password(password_range: int = 12) -> bytes:
    literals = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(random.choice(literals) for _ in range(password_range)).encode(
        "utf-8",
    )
