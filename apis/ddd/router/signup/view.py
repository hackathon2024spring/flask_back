from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from ddd.domain.value_object import Password, UserName
from ddd.domain.entity import User as DomainUser
from ddd.domain.repository import UserRepository
from ddd.usecase.usecase import UseCase
from ddd.router.signup.schema import (
    Request,
    RequestExample,
    Response,
    ResponseExamples,
    Data,
)
from ddd.infrastructure.repository_provider import get_user_repository

router = APIRouter()


# Request(strなどプリミティブ型から作る)→
# Domain User(DDDでエラーチェックなど)→
# ORM User(sqlAlchemyのORM.Baseを継承する)
@router.post(
    "/signup",
    summary="ユーザー登録",
    description="ユーザーを登録します。",
    response_model=Response,
    responses=ResponseExamples,
)
async def signup(
    request: Request = RequestExample,
    user_repository: UserRepository = Depends(get_user_repository),
):

    use_case = UseCase(userRepository=user_repository)
    try:
        domain_user = DomainUser(
            a_username=UserName(a_name=request.username),
            a_email=request.email,
            a_password=Password(a_password=request.password1),
            a_confirm=Password(a_password=request.password2),
        )

        registered_user = await use_case.create_user_account(user=domain_user)

        response = Response(
            status=1,
            data=Data(uid=registered_user.id(), username=registered_user.name()),
        )
        return response

    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
