from typing import List

from fastapi import APIRouter, Depends
from fastapi import status

from app.pkg.models import *
from dependency_injector.wiring import inject, Provide
from app.internal.services import Services, current_user
from app.internal.services.course_service import CourseService

__all__ = [
    "router"
]

router = APIRouter(
    prefix="/courses",
    tags=['/course']
)


@router.post(
    "/",
    description="Create New Course",
    response_model=CourseModelWithLectures,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_courses(
    cmd: CreateCourseCommand,
    course_service: CourseService = Depends(Provide[Services.course_service])
):
    return await course_service.create_course(cmd)


@router.get(
    "/get",
    description="Create New Course",
    response_model=List[CourseModel],
    status_code=status.HTTP_201_CREATED
)
@inject
async def get_course(
    course_id: UUID,
    user=Depends(current_user),
    course_service: CourseService = Depends(Provide[Services.course_service])
):
    return await course_service.read_courses(
        ReadCoursesByUserCommand(
            course_id=course_id,
            id=user.id
        )
    )


@router.get(
    "/get-all",
    description="Create New Course",
    response_model=List[CourseModel],
    status_code=status.HTTP_201_CREATED
)
@inject
async def get_course(
    course_service: CourseService = Depends(Provide[Services.course_service])
):
    return await course_service.read_all_courses()


@router.post(
    "/add-lecture",
    description="Create New Course",
    response_model=List[CourseModel],
    status_code=status.HTTP_201_CREATED
)
@inject
async def add_lecture(
    cmd: AddLectureCommand,
    course_service: CourseService = Depends(Provide[Services.course_service])
):
    return await course_service.add_lecture(cmd)
