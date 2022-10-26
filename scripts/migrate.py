from argparse import ArgumentParser

from yoyo import get_backend, read_migrations

from dotenv import find_dotenv
from pydantic import BaseSettings, SecretStr


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Settings(_Settings):
    # Postgres
    API_POSTGRES_HOST: str
    API_POSTGRES_PORT: int
    API_POSTGRES_USER: str
    API_POSTGRES_PASSWORD: SecretStr
    API_POSTGRES_NAME: str


settings = Settings(_env_file=find_dotenv(".env"))


def get_dsn():
    return (
        f"postgresql://"
        f"{settings.API_POSTGRES_USER}:"
        f"{settings.API_POSTGRES_PASSWORD.get_secret_value()}@"
        f"{settings.API_POSTGRES_HOST}:{settings.API_POSTGRES_PORT}/"
        f"{settings.API_POSTGRES_NAME}"
    )


def _apply(backend, migrations):
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def _rollback(backend, migrations):
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))


def _rollback_one(backend, migrations):
    with backend.lock():
        migrations = backend.to_rollback(migrations)
        for migration in migrations:
            backend.rollback_one(migration)
            break


def _reload(backend, migrations):
    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))
        backend.apply_migrations(backend.to_apply(migrations))


def run(action):
    backend = get_backend(get_dsn())
    migrations = read_migrations("migrations")
    action(backend, migrations)


def cli():
    parser = ArgumentParser(description="Apply migrations")
    parser.add_argument("--rollback", action="store_true", help="Rollback migrations")
    parser.add_argument(
        "--rollback-one",
        action="store_true",
        help="Rollback one migration",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Rollback all migration and applying again",
    )
    args = parser.parse_args()

    if args.rollback:
        action = _rollback
    elif args.rollback_one:
        action = _rollback_one
    elif args.reload:
        action = _reload
    else:
        action = _apply

    run(action)


if __name__ == "__main__":
    cli()
