from app.pkg.models import *
from app.internal.repository.postgres.lecturers import LecturerRepository
from app.pkg.models.lecturers import LecturerModel, CreateLecturerModel


class LecturerService:
    lecturer_repository: LecturerRepository

    def __init__(
        self,
        lecturer_repository: LecturerRepository,
    ):
        self.lecturer_repository = lecturer_repository

    async def create_lecturer(
        self,
        cmd: CreateLecturerModel
    ) -> LecturerModel:
        return await self.lecturer_repository.create_lecturer(cmd)

    async def read_lecturers(self) -> List[LecturerModel]:
        return await self.lecturer_repository.read_lecturers()
