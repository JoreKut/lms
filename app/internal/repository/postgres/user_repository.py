from typing import List

from app.pkg.models import *
from .connection import get_connection
from .connection import get_cursor_with_connection
from app.internal.pkg.handlers.repository.postgres import collect_response


class UserRepository:

    @staticmethod
    def __build_where_filter(cmd: BaseApiModel) -> str:
        filters = [f"{v.name}=%({v.name})s" for v in cmd.__fields__.values() if v.required]
        return ' or '.join(filters)

    @staticmethod
    @collect_response(nullable=True)
    async def read_by_email(cmd: ReadUserByEmailCommand) -> UserModel:
        async with get_connection() as cur:
            query = """
                select *
                from users
                where email=%(email)s
            """

            await cur.execute(query, cmd.dict())

            resp = await cur.fetchone()

            return resp

    @collect_response
    async def read_user_by_identifier(self, cmd: ReadUserByIdentifier) -> UserModel:
        where_filters = self.__build_where_filter(cmd)

        async with get_connection() as cur:
            q = f"""
                select *
                from users
                where {where_filters}
            """

            await cur.execute(q, cmd.dict())

            resp = await cur.fetchone()

            return resp

    @staticmethod
    @collect_response
    async def read_lecture_for_course(cmd: ReadLectureByCourseId) -> List[LectureModel]:
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
    @collect_response(nullable=True)
    async def read_lecture_for_course_by_date(cmd: ReadLecturesByDate) -> List[LectureModel]:
        query = """
                select
                    l.id,
                    l.created_at,
                    l.title,
                    l.description,
                    l.course_id,
                    l.starts_at
                from users_courses
                join lectures l on users_courses.course_id = l.course_id
                where user_id = %(user_id)s and date(l.starts_at) = date(%(lecture_date)s)
                group by l.id;
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            courses_fetch = await cur.fetchall()

            return courses_fetch

    @staticmethod
    @collect_response(nullable=True)
    async def read_by_phone(cmd: ReadUserByPhoneCommand) -> UserModel:
        async with get_connection() as cur:
            query = """
                select *
                from users
                where phone=%(phone)s
            """

            await cur.execute(query, cmd.dict())

            resp = await cur.fetchone()

            return resp

    @staticmethod
    @collect_response(nullable=True)
    async def create(user: CreateUserCommand) -> UserModel:
        async with get_cursor_with_connection() as (cur, conn):
            create_query = """
                insert into users(username, hashed_password, email, phone, firstname, lastname) 
                values (%(username)s, %(hashed_password)s, %(email)s, %(phone)s, %(firstname)s, %(lastname)s)
                on conflict do nothing
                returning 
                    id::text,
                    created_at,
                    hashed_password,
                    username,
                    email,
                    phone,
                    firstname,
                    lastname
            """

            await cur.execute(create_query, user.dict())

            return await cur.fetchone()

    @staticmethod
    @collect_response(nullable=True)
    async def read_by_id(cmd: ReadUserByIdCommand) -> UserModel:
        async with get_connection() as cur:
            query = """
                select *
                from users u
                where id=%(id)s
            """

            await cur.execute(query, cmd.dict())

            resp = await cur.fetchone()

            return resp

    @staticmethod
    async def subscribe_course(cmd: SubscribeCourseCommand):
        query = """
            insert into users_courses(user_id, course_id)
            values (%(user_id)s, %(course_id)s)
            returning 
                id,
                created_at,
                user_id,
                course_id
        """

        async with get_connection() as cur:

            await cur.execute(query, cmd.to_dict(show_secrets=True))
