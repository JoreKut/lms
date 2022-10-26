from app.internal.pkg.handlers.repository.postgres import collect_response
from app.internal.repository.postgres.connection import get_connection
from app.pkg.models import *
from app.pkg.models.lecturers import LecturerModel, CreateLecturerModel


class LecturerRepository:

    @staticmethod
    @collect_response(nullable=True)
    async def create_lecturer(cmd: CreateLecturerModel) -> LecturerModel:
        query = """
                insert into lecturers(firstname, lastname, patronymic)
                values(%(firstname)s, %(lastname)s, %(patronymic)s)
                returning 
                    id,
                    firstname,
                    lastname,
                    patronymic
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            lecture_fetch = await cur.fetchone()

            return lecture_fetch

    @staticmethod
    @collect_response
    async def read_lecturers() -> List[LecturerModel]:
        query = """
                select *
                from lecturers
            """

        async with get_connection() as cur:
            await cur.execute(query)

            lecture_fetch = await cur.fetchall()

            return lecture_fetch
