from app.internal.repository import Repositories, LecturerRepository
from dependency_injector import containers, providers
from .user_service import UserService
from .auth_service import AuthService
from .lecture_service import LectureService, LectureRepository
from .course_service import CourseService, CourseRepository
from .lecturer_service import LecturerService


class Services(containers.DeclarativeContainer):
    user_service = providers.Factory(
        UserService,
        user_repository=Repositories.user_repository
    )
    auth_service = providers.Factory(
        AuthService,
        user_service=user_service,
        access_token_repository=Repositories.access_token_repository,
        refresh_token_repository=Repositories.refresh_token_repository
    )
    lecture_service = providers.Factory(
        LectureService,
        lecture_repository=LectureRepository
    )
    lecturer_service = providers.Factory(
        LecturerService,
        lecturer_repository=LecturerRepository
    )
    course_service = providers.Factory(
        CourseService,
        course_repository=CourseRepository
    )


services = Services()

current_user = services.auth_service().get_user
refresh_secure = services.auth_service().get_jwt_token
