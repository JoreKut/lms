from typing import List

from app.pkg.models import *
from app.internal.repository.postgres.lecture_repository import LectureRepository


class LectureService:
    lecture_repository: LectureRepository

    def __init__(
        self,
        lecture_repository: LectureRepository,
    ):
        self.lecture_repository = lecture_repository

    async def create_lecture(
        self,
        cmd: CreateLectureCommand
    ) -> LectureModel:
        return await self.lecture_repository.create_lecture(cmd)

    async def read_lectures(
        self,
        cmd: ReadLectureByCourseId
    ) -> List[LectureModel]:
        return await self.lecture_repository.read_lectures(cmd)
