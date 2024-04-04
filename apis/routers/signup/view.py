from fastapi import APIRouter, status
from .schema import Request, RequestExample, Response, ResponseExamples
from .model import Model
from ..endpoints import Signup as ep

router = APIRouter()


# tokenなし・BaseModelのRequestとResponse
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
async def get_payloads(body: Request = RequestExample):
    res = await Model().exec(body)
    return res
