from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from ddd.domain.entity import ExerciseDone as DomainExerciseDone
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.usecase.usecase import UseCase
from ddd.router.addexercises.schema import (
    Request,
    RequestExample,
    Response,
    ResponseExamples,
)

router = APIRouter()
oauth2_scheme = Token(tokenUrl="token")


@router.post(
    "/exercises/{date}",
    summary="実施した運動の変更",
    description="""実施した運動の変更""",
    response_model=Response,
    responses=ResponseExamples,
)
async def add_exercises(
    date: date,
    token: str = Depends(oauth2_scheme),
    request: Request = RequestExample,
    user_repository: UserRepository = Depends(get_user_repository),
):

    if not request.data:
        raise HTTPException(status_code=400, detail="No data provided")

    usecase = UseCase(userRepository=user_repository)

    # DDDの世界で扱うエンティティに変換
    exercises_done = [
        DomainExerciseDone(a_id=str(dat.exerciseId), a_done=dat.done)
        for dat in request.data
    ]

    # tokenとexercise_doneでExerciseDoneテーブルをupsert
    await usecase.update_user_exercises_done(
        token=token, date=date, exercises_done=exercises_done
    )

    return Response(status=1)
