from typing import List
from fastapi import APIRouter, Depends
from datetime import date
from ddd.domain.entity import ExerciseDoneResponse
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.getexercises.schema import Response, ResponseExamples, Data


router = APIRouter()
oauth2_scheme = Token(tokenUrl="token")


@router.get(
    "/exercises/{date}",
    summary="実施できる運動の取得",
    description="""実施できる運動の取得""",
    response_model=Response,
    responses=ResponseExamples,
)
async def get_exercises(
    date: date,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):

    usecase = UseCase(userRepository=user_repository)

    user_exercises_done: List[ExerciseDoneResponse] = (
        await usecase.get_user_exercises_done(token=token, date=date)
    )

    # DDDの世界から取り出すための変換
    exercises_done = [
        Data(
            exerciseId=int(exe.id()),
            exerciseName=exe.exercise_name(),
            exerciseDone=exe.done(),
        )
        for exe in user_exercises_done
    ]

    return Response(status=1, data=exercises_done)
