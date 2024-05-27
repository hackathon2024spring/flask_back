from typing import List
from fastapi import APIRouter, Depends
from ddd.domain.entity import ExerciseSelectedResponse
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.getexercises_setting.schema import Response, Data, ResponseExamples


router = APIRouter()
oauth2_scheme = Token(tokenUrl="token")


@router.get(
    "/exercises_setting",
    summary="登録されている運動の取得",
    description="""登録されている運動の取得""",
    response_model=Response,
    responses=ResponseExamples,
)
async def get_user_exercises_setting(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    usecase = UseCase(userRepository=user_repository)
    user_exercise_selected: List[ExerciseSelectedResponse] = (
        await usecase.get_user_exercises_selected(token=token)
    )

    # DDDの世界から取り出すための変換
    exercises_selected = [
        Data(
            exerciseId=int(exe.id()),
            exerciseName=exe.exercise_name(),
            exerciseSelected=exe.selected(),
        )
        for exe in user_exercise_selected
    ]

    return Response(status=1, data=exercises_selected)
