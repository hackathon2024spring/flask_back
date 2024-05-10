from fastapi import Depends, APIRouter, status
from datetime import date
from apis.services.authfunctions import get_current_user
from .schema import Request, RequestExample, Response, ResponseExamples, TokenData
from .model import Model
from ..endpoints import AddExercises as ep

router = APIRouter()


@router.post(
    ep.endpoint,
    summary=ep.summary,
    description=ep.description,
    status_code=status.HTTP_200_OK,
    response_model=Response,
    responses=ResponseExamples,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def get_payloads(
    date: date, body: Request = RequestExample, token: TokenData = Depends(get_current_user)
):
    res = await Model().exec(date, body, token)
    return res