from fastapi import APIRouter, Depends
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.getuser.schema import Response, ResponseExamples, Data


router = APIRouter()


@router.get(
    "/user",
    summary="ユーザー情報の取得",
    description="""ユーザー情報の取得""",
    response_model=Response,
    responses=ResponseExamples,
)
async def getuser(
    token: str = Depends(Token(tokenUrl="token")),
    user_repository: UserRepository = Depends(get_user_repository),
):
    usecase = UseCase(userRepository=user_repository, token=token)

    # userRepository.get_user_by_uidでHttpExceptionが設定されている。
    response = await usecase.get_login_user()

    return Response(
        status=1, data=Data(username=response.username, email=response.email)
    )
