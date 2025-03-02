from fastapi import APIRouter, Depends, HTTPException
from ddd.domain.entity import ExerciseSelected as DomainExerciseSelected
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.addexercises_setting.schema import (
    Request,
    RequestExample,
    Response,
    ResponseExamples,
)


router = APIRouter()


@router.post(
    "/exercises_setting",
    summary="登録されている運動の変更",
    description="""登録されている運動の登録変更""",
    response_model=Response,
    responses=ResponseExamples,
)
async def add_exercises_setting(
    token: str = Depends(Token(tokenUrl="token")),
    request: Request = RequestExample,
    user_repository: UserRepository = Depends(get_user_repository),
):

    if not request.data:
        raise HTTPException(status_code=400, detail="No data provided")

    usecase = UseCase(userRepository=user_repository, token=token)

    # DDDの世界で扱うエンティティに変換
    exercises_selected = [
        DomainExerciseSelected(a_id=str(dat.exerciseId), a_selected=dat.selected)
        for dat in request.data
    ]

    # tokenとexercise_selectedでExercises_settingテーブルをupsert
    await usecase.update_user_exercises_selected(exercises_selected=exercises_selected)

    return Response(status=1)
