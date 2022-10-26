from typing import List

from app.internal.pkg.handlers.repository.postgres import collect_response
from app.internal.repository.postgres.connection import (
    get_connection,
    get_cursor_with_connection
)
from app.pkg.models import (
    CreateTokenCommand,
    DeleteTokenCommand,
    DeleteAllTokenByUserCommand,
    ReadTokenCommand,
    TokenModel,
    ReadTokenByUserCommand,
    ReadUserByTokenCommand
)
from app.pkg.models.base import Model
from app.internal.repository.reposiroty import Repository


class AccessTokenRepository(Repository):

    async def create(self, cmd: CreateTokenCommand):
        async with get_cursor_with_connection() as (cur, conn):
            q = """
                insert into access_token_sessions(token, user_id)
                values (%(token)s, %(user_id)s)
            """

            await cur.execute(q, cmd.dict())

    @collect_response
    async def read(self, cmd: ReadTokenCommand) -> TokenModel:
        async with get_connection() as cur:
            read_query = """
                select 
                    token,
                    user_id
                from access_token_sessions
                where token=%(token)s and user_id=%(user_id)s
            """

            await cur.execute(read_query, cmd.dict())
            response = await cur.fetchone()

            return response

    async def read_all(self):
        pass

    @collect_response
    async def read_all_by_user(self, cmd: ReadTokenByUserCommand) -> List[TokenModel]:
        async with get_connection() as cur:
            read_by_user_query = """
                select 
                    token,
                    user_id
                from access_token_sessions
                where user_id=%(user_id)s
            """

            await cur.execute(read_by_user_query, cmd.dict())
            response = await cur.fetchall()

            return response

    @collect_response
    async def read_all_by_token(self, cmd: ReadUserByTokenCommand) -> TokenModel:
        async with get_connection() as cur:
            read_by_user_query = """
                select 
                    token::text,
                    user_id::text
                from access_token_sessions
                where token=%(token)s
            """

            await cur.execute(read_by_user_query, cmd.dict())
            response = await cur.fetchone()

            return response

    async def update(self, cmd: Model) -> Model:
        pass

    async def delete(self, cmd: DeleteTokenCommand):
        async with get_cursor_with_connection() as (cur, conn):
            delete_query = """
                delete from access_token_sessions
                where token=%(token)s
            """
            await cur.execute(delete_query, cmd.dict())

    async def delete_by_user(self, cmd: DeleteAllTokenByUserCommand):
        async with get_cursor_with_connection() as (cur, conn):
            delete_by_user_query = """
                delete from access_token_sessions
                where user_id=%(user_id)s
            """
            await cur.execute(delete_by_user_query, cmd.dict())
