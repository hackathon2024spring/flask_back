from fastapi import APIRouter, Depends
from ddd.domain.entity import CalendarRequest
from ddd.domain.entity_oauth2 import OAuth2PasswordBearerWithCookie as Token
from ddd.domain.repository import UserRepository
from ddd.usecase.usecase import UseCase
from ddd.infrastructure.repository_provider import get_user_repository
from ddd.router.getcalendars.schema import Data, Response, ResponseExamples


router = APIRouter()
oauth2_scheme = Token(tokenUrl="token")


@router.get(
    "/calendars/{year}/{month}",
    summary="カレンダーの表示情報を取得",
    description="""カレンダーの表示情報を取得""",
    response_model=Response,
    responses=ResponseExamples,
)
async def get_calendars(
    year: int,
    month: int,
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
):
    usecase = UseCase(userRepository=user_repository)

    calendar_request = CalendarRequest(a_year=year, a_month=month)

    exercises_in_calendar = await usecase.get_exercises_in_calendar(
        token=token, calendar=calendar_request
    )

    # DDDの世界から取り出すための変換
    exercises_this_month = [
        Data(
            day=exe.date(),
            exerciseDone=exe.exercise_done(),
        )
        for exe in exercises_in_calendar
    ]

    return Response(status=1, data=exercises_this_month)
