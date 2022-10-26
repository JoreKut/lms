from functools import lru_cache
from dotenv import find_dotenv
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):

    API_POSTGRES_HOST: str
    API_POSTGRES_PORT: int
    API_POSTGRES_NAME: str
    API_POSTGRES_PASSWORD: SecretStr
    API_POSTGRES_USER: str
    HMAC_KEY: str
    JWT_KEY: str
    JWT_ALGORITHM: str

    PORT: str
    SMTP_SERVER: str
    SENDER_EMAIL: str
    EMAIL_PASSWORD: str


@lru_cache()
def get_settings(env_file: str = '.env') -> Settings:
    return Settings(_env_file=find_dotenv(env_file))
