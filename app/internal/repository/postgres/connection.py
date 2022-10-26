from contextlib import asynccontextmanager

from aiopg.connection import Cursor
from aiopg.connection import Connection
from psycopg2.extras import RealDictCursor

from app.internal.pkg.connectors import MyPostgres


@asynccontextmanager
async def get_connection() -> Cursor:
    async with MyPostgres().get_connect() as connection:
        async with (await connection.cursor(cursor_factory=RealDictCursor)) as cur:
            yield cur


@asynccontextmanager
async def get_cursor_with_connection() -> (Cursor, Connection):
    async with MyPostgres().get_connect() as connection:
        async with (await connection.cursor(cursor_factory=RealDictCursor)) as cur:
            yield cur, connection
