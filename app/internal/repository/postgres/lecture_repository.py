from typing import List

from app.internal.pkg.handlers.repository.postgres import collect_response
from app.internal.repository.postgres.connection import get_connection
from app.pkg.models import *


class LectureRepository:

    @staticmethod
    @collect_response(nullable=True)
    async def create_lecture(cmd: CreateLectureCommand) -> LectureModel:
        query = """
                insert into lectures(title, description, course_id)
                values(%(title)s, %(description)s, %(course_id)s)
                returning 
                    id,
                    created_at,
                    title,
                    description,
                    course_id;
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            lecture_fetch = await cur.fetchone()

            return lecture_fetch

    @staticmethod
    @collect_response(nullable=True)
    async def update_lecture(cmd: UpdateLectureCommand) -> LectureModel:
        update_builder = LectureRepository.__update_builder(cmd)
        query = f"""
                update lectures
                set {update_builder}
                where id = %(id)s
                returning 
                    id,
                    created_at,
                    title,
                    description,
                    course_id,
                    starts_at;
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())
            lecture_fetch = await cur.fetchone()
            return lecture_fetch

    @staticmethod
    @collect_response(nullable=True)
    async def delete_lecture_by_id(cmd: DeleteLectureByIdCommand) -> LectureModel:
        query = """
                delete from lectures
                where  id = %(id)s
                returning
                    id,
                    created_at,
                    title,
                    description,
                    course_id,
                    starts_at;
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            lecture_fetch = await cur.fetchone()

            return lecture_fetch

    @staticmethod
    @collect_response()
    async def read_lectures(cmd: ReadLectureByCourseId) -> List[LectureModel]:
        query = """
                select *
                from lectures
                where course_id = %(course_id)s
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            courses_fetch = await cur.fetchall()

            return courses_fetch

    @staticmethod
    def __update_builder(cmd: BaseApiModel):
        values = [
            f"{v.name} = %({v.name})s" for v in cmd.__fields__.values() if v.required
        ]

        return ", ".join(values)
