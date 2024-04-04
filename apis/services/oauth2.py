from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Request, HTTPException, status
from typing import Optional, Dict

# ロガーの設定
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# HttpOnlyのcookieからTokenを抽出し、"Bearer "を先頭に付与する。
# https://github.com/nofoobar/JobBoard-Fastapi/blob/main/backend/apis/utils.py
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        authorization = "Bearer " + authorization
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


# HttpOnlyのcookieからTokenを抽出し、その有無を確認する。
class OAuth2RefreshTokenBearer(OAuth2):
    def __call__(self, request: Request) -> Optional[str]:
        refresh_token: str = request.cookies.get("access_token")
        # logger.info("     refresh_token " + str(refresh_token))
        if not refresh_token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return refresh_token
