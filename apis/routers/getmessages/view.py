from fastapi import APIRouter, Depends, status
from apis.services.authfunctions import get_current_user
from .schema import Request, RequestExample, Response, ResponseExamples, TokenData
from .model import Model
from ..endpoints import GetMessages as ep

router = APIRouter()


# cookieをsetするJSONResponseはPydanticのBaseModelと共存できないので、response_modelを使えない。
# またrequest_modelも事前にリクエストヘッダからcookieを読むので、使わない。
@router.get(
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
    body: Request = RequestExample, token: TokenData = Depends(get_current_user)
):
    res = await Model().exec(body, token)
    return res
