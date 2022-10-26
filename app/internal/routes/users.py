import datetime
from typing import List

from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide
from app.pkg.models import *
from app.internal.services import Services, current_user
from app.internal.services.user_service import UserService

__all__ = [
    "router"
]

router = APIRouter(
    prefix="/users",
    tags=['/users']
)


@router.post(
    "/subscribe_course",
    description="Subscribe on course"
)
@inject
async def add_course(
    cmd: SubscribeCourseCommand,
    user=Depends(current_user),
    user_service: UserService = Depends(Provide[Services.user_service])
):
    cmd.user_id = user.id
    return await user_service.subscribe_course(cmd)


@router.post(
    "/get-lectures",
    description="Get all available lectures for user"
)
@inject
async def get_courses(
    lecture_date: datetime.date = datetime.date.today(),
    user=Depends(current_user),
    user_service: UserService = Depends(Provide[Services.user_service])
) -> List[LectureModel]:
    return await user_service.read_lecture_by_date(
        ReadLecturesByDate(
            lecture_date=lecture_date,
            user_id=user.id
        )
    )
