from fastapi import APIRouter, Depends
from ddd.domain.repository import UserRepository
from ddd.usecase.usecase import UseCase
from ddd.router.logout.schema import ResponseExamples
from ddd.infrastructure.repository_provider import get_user_repository


from ddd.usecase.oauth2 import (
    OAuth2PasswordBearerWithCookie,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


@router.get(
    "/logout",
    summary="ログアウト",
    description="""ログアウト""",
    responses=ResponseExamples,
)
async def logout(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    usecase = UseCase(userRepository=user_repository)

    # userService.get_authorized_idでHttpExceptionが設定されている。
    # cookieの無いresponse=cookieが外れる
    response = await usecase.remove_cookie(token=token)
    return response
