from typing import List

from fastapi import APIRouter, Depends
from app.pkg.models import *
from dependency_injector.wiring import inject, Provide
from app.internal.services import Services
from app.internal.services.lecture_service import LectureService
from fastapi import status

__all__ = [
    "router"
]

router = APIRouter(
    prefix="/lectures",
    tags=['/lecture']
)


@router.post(
    "/",
    description="Create lecture for course",
    response_model=LectureModel,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_lectures(
    cmd: CreateLectureCommand,
    lecture_service: LectureService = Depends(Provide[Services.lecture_service])
):
    return lecture_service.create_lecture(cmd)


@router.post(
    "/get",
    description="Get all lectures from course",
    response_model=List[LectureModel],
    status_code=status.HTTP_200_OK
)
@inject
async def read_lectures_by_course(
    course_id: UUID,
    lecture_service: LectureService = Depends(Provide[Services.lecture_service])
):
    return lecture_service.read_lectures(
        ReadLectureByCourseId(
            course_id=course_id
        )
    )
