from fastapi import APIRouter, Depends
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.logout.schema import ResponseExamples


router = APIRouter()
oauth2_scheme = Token(tokenUrl="token")


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
