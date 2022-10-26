from typing import List

from fastapi import APIRouter, Depends
from app.pkg.models import *
from dependency_injector.wiring import inject, Provide
from app.internal.services import Services
from app.internal.services.lecturer_service import LecturerService
from fastapi import status

__all__ = [
    "router"
]

from app.pkg.models.lecturers import LecturerModel, CreateLecturerModel

router = APIRouter(
    prefix="/lecturers",
    tags=['/lecturer']
)


@router.post(
    "/",
    description="Create lecturer",
    response_model=LecturerModel,
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_lectures(
    cmd: CreateLecturerModel,
    lecturer_service: LecturerService = Depends(Provide[Services.lecturer_service])
):
    return await lecturer_service.create_lecturer(cmd)


@router.post(
    "/get",
    description="Get all lecturers",
    response_model=List[LecturerModel],
    status_code=status.HTTP_200_OK
)
@inject
async def read_lectures(
    lecturer_service: LecturerService = Depends(Provide[Services.lecturer_service])
):
    return await lecturer_service.read_lecturers()
