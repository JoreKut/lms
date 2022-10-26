from fastapi import APIRouter, Depends

from dependency_injector.wiring import inject, Provide

from app.pkg.models import (
    AuthorizationForm,
    RegistrationForm
)
from app.pkg.models import DeleteAllTokenByUserCommand
from app.internal.services import AuthService, Services
from app.internal.services import current_user, refresh_secure

__all__ = [
    "router"
]

router = APIRouter(
    prefix="/auth",
    tags=['/auth']
)


@router.post(
    "/get_me"
)
@inject
async def get_me(
    user=Depends(current_user)
):
    return user


@router.post(
    "/sign_up"
)
@inject
async def sign_up(
    cmd: RegistrationForm,
    auth_service: AuthService = Depends(
        Provide[Services.auth_service]
    )
):
    return await auth_service.sign_up(cmd)


@router.post(
    "/login"
)
@inject
async def sign_in(
    cmd: AuthorizationForm,
    auth_service: AuthService = Depends(
        Provide[Services.auth_service]
    )
):
    return await auth_service.login(cmd)


@router.post(
    "/refresh"
)
@inject
async def refresh_access_token(
    refresh_token: str = Depends(refresh_secure),
    auth_service: AuthService = Depends(
        Provide[Services.auth_service]
    )
):
    return await auth_service.refresh_access_token(refresh_token)


@router.post(
    "/logout"
)
@inject
async def logout(
    user=Depends(current_user),
    auth_service: AuthService = Depends(
        Provide[Services.auth_service]
    )
):
    return await auth_service.logout(
        DeleteAllTokenByUserCommand(
            user_id=user.id
        )
    )
