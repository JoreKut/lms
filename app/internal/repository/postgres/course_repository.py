from typing import List

from app.internal.pkg.handlers.repository.postgres import collect_response
from app.internal.repository.postgres.connection import get_connection
from app.pkg.models import (
    ReadCoursesByUserCommand,
    CourseModel,
    CreateCourseCommand,
    UpdateCourseCommand,
    DeleteCourseByIdCommand, BaseApiModel, ReadLectureByCourseId, LectureModel, AddCourseToLecturer, ReadCourseById,
    CourseModelWithLectures,
)


class CourseRepository:

    @staticmethod
    async def add_lecturer_to_course(cmd: AddCourseToLecturer):
        query = """
            insert into courses_lecturers(course_id, lecturer_id)
            values (%(course_id)s, %(lecturer_id)s)
        """
        async with get_connection() as cur:

            await cur.execute(query, cmd.dict())

    @staticmethod
    @collect_response
    async def read_course_by_id(cmd: ReadCourseById) -> CourseModelWithLectures:
        q = """
            select
                c.id,
                c.created_at,
                c.title,
                c.description,
                json_agg(cl.lecturer_id) as lecturer_ids
            from courses c
            left join courses_lecturers cl on c.id = cl.course_id
            where c.id =%(course_id)s
            group by
                c.id,
                c.created_at,
                c.title,
                c.description
        """

        async with get_connection() as cur:
            await cur.execute(q, cmd.dict())
            f = await cur.fetchone()
            return f

    @staticmethod
    @collect_response(nullable=True)
    async def create_course(cmd: CreateCourseCommand) -> CourseModel:
        query = """
            insert into courses(title, description)
            values(%(title)s, %(description)s)
            returning 
                id,
                created_at,
                title,
                description;
        """

        async with get_connection() as cur:

            await cur.execute(query, cmd.dict())

            course_fetch = await cur.fetchone()
            return course_fetch

    @staticmethod
    @collect_response(nullable=True)
    async def update_course(cmd: UpdateCourseCommand) -> CourseModel:
        update_builder = CourseRepository.__update_builder(cmd)
        query = f"""
            update courses
            set {update_builder}
            where id = %(id)s
            returning 
                id,
                created_at,
                title,
                description;
        """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())
            course_fetch = await cur.fetchone()
            return course_fetch

    @staticmethod
    @collect_response(nullable=True)
    async def delete_course_by_id(cmd: DeleteCourseByIdCommand) -> CourseModel:
        query = """
            delete from courses
            where  id = %(id)s
            returning
                id,
                created_at,
                title,
                description
        """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            course_fetch = await cur.fetchone()

            return course_fetch

    @staticmethod
    @collect_response
    async def read_courses(cmd: ReadCoursesByUserCommand) -> List[CourseModel]:
        query = """
                select *
                from users_courses
                where user_id = %(id)s
            """

        async with get_connection() as cur:
            await cur.execute(query, cmd.dict())

            courses_fetch = await cur.fetchall()

            return courses_fetch

    @staticmethod
    @collect_response
    async def read_all() -> List[CourseModel]:
        q = """
            select *
            from courses
        """

        async with get_connection() as cur:
            await cur.execute(q)

            return await cur.fetchall()

    @staticmethod
    @collect_response
    async def add_lecture():
        q = """
            
        """

    @staticmethod
    def __update_builder(cmd: BaseApiModel):

        values = [
            f"{v.name} = %({v.name})s" for v in cmd.__fields__.values() if v.required
        ]

        return ", ".join(values)
