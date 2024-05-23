from fastapi import APIRouter, Depends
from ddd.domain.value_object import Password
from ddd.domain.repository import UserRepository
from ddd.usecase.usecase import UseCase
from ddd.router.login.schema import Request, RequestExample, ResponseExamples
from ddd.infrastructure.repository_provider import get_user_repository

router = APIRouter()


@router.post(
    "/login",
    summary="ログイン",
    description="ログイン",
    responses=ResponseExamples,
)
async def login(
    request: Request = RequestExample,
    user_repository: UserRepository = Depends(get_user_repository),
):

    usecase = UseCase(userRepository=user_repository)

    # userService.get_authorized_idでHttpExceptionが設定されている。
    response = await usecase.set_cookie(
        email=request.email, password=Password(a_password=request.password)
    )

    return response
