from fastapi import APIRouter, Depends, status
from apis.services.authfunctions import get_current_user
from .schema import TokenData
from .model import Model
from ..endpoints import Signout as ep

router = APIRouter()


# cookieをsetするJSONResponseはPydanticのBaseModelと共存できないので、response_modelを使えない。
# またrequest_modelも事前にリクエストヘッダからcookieを読むので、使わない。
@router.get(
    ep.endpoint,
    summary=ep.summary,
    description=ep.description,
    status_code=status.HTTP_200_OK,
)
async def get_payloads(token: TokenData = Depends(get_current_user)):
    json_res = await Model().exec(token)
    return json_res
