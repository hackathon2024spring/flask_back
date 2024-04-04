from fastapi import APIRouter, status
from .schema import Request, RequestExample
from .model import Model
from ..endpoints import Login as ep

router = APIRouter()


# cookieをsetするJSONResponseはPydanticのBaseModelと共存できない。
# response_modelはBaseModelしか受け付けないので、responseの様式を縛れない。
@router.post(
    ep.endpoint,
    summary=ep.summary,
    description=ep.description,
    status_code=status.HTTP_200_OK,
)
async def get_payloads(body: Request = RequestExample):
    json_res = await Model().exec(body)
    return json_res
