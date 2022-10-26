from dependency_injector import containers, providers

from .postgres import (
    UserRepository,
    AccessTokenRepository,
    RefreshTokenRepository,
    LectureRepository,
    CourseRepository,
)


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Factory(
        UserRepository
    )
    access_token_repository = providers.Factory(
        AccessTokenRepository
    )
    refresh_token_repository = providers.Factory(
        RefreshTokenRepository
    )
    lecture_repository = providers.Factory(
        LectureRepository
    )
    course_repository = providers.Factory(
        CourseRepository
    )
