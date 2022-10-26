from contextlib import asynccontextmanager

import aiopg
from aiopg import Connection

from app.pkg.settings import settings

__all__ = ["MyPostgres"]


class MyPostgres:
    def __init__(self):
        self.pool = None

    @staticmethod
    def get_dsn():
        return (
            f"postgres://"
            f"{settings.API_POSTGRES_USER}:"
            f"{settings.API_POSTGRES_PASSWORD.get_secret_value()}@"
            f"{settings.API_POSTGRES_HOST}:{settings.API_POSTGRES_PORT}/"
            f"{settings.API_POSTGRES_NAME}"
        )

    @asynccontextmanager
    async def get_connect(self) -> Connection:
        """Create pool of connectors to a Postgres database.

        Yields:
            ``aiopg.Connection instance`` in asynchronous context manager.
        """
        if self.pool is None:
            self.pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self.pool as pool:
            async with pool.acquire() as conn:
                yield conn
