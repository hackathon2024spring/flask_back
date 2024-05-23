from fastapi import APIRouter, Depends
from ddd.router.getuser.schema import Response, Data
from ddd.domain.repository import UserRepository
from ddd.usecase.usecase import UseCase
from ddd.router.getuser.schema import ResponseExamples
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.oauth2 import (
    OAuth2PasswordBearerWithCookie,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


@router.get(
    "/user",
    summary="ユーザー情報の取得",
    description="""ユーザー情報の取得""",
    response_model=Response,
    responses=ResponseExamples,
)
async def getuser(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    usecase = UseCase(userRepository=user_repository)

    # userRepository.get_user_by_uidでHttpExceptionが設定されている。
    response = await usecase.get_login_user(token=token)

    return Response(
        status=1, data=Data(username=response.username, email=response.email)
    )
