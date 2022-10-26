from typing import List

from app.pkg.models import *
from app.internal.repository.postgres.course_repository import CourseRepository


class CourseService:

    course_repository: CourseRepository

    def __init__(
        self,
        course_repository: CourseRepository,
    ):
        self.course_repository = course_repository

    async def create_course(
        self,
        cmd: CreateCourseCommand
    ) -> CourseModelWithLectures:

        course = await self.course_repository.create_course(cmd)

        for lecturer_id in cmd.lecturer_ids:
            await self.course_repository.add_lecturer_to_course(
                AddCourseToLecturer(
                    course_id=course.id,
                    lecturer_id=lecturer_id
                )
            )

        return await self.course_repository.read_course_by_id(
            ReadCourseById(
                course_id=str(course.id)
            )
        )

    async def read_courses(
        self,
        cmd: ReadCoursesByUserCommand
    ) -> List[CourseModel]:
        return await self.course_repository.read_courses(cmd)

    async def read_all_courses(self) -> List[CourseModel]:
        return await self.course_repository.read_all()

    async def add_lecture(self, cmd: AddLectureCommand):
        return await self.course_repository.add_lecture(cmd)
