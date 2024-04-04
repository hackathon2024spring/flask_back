from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .schema import TokenData


class Model(BaseModel):
    async def exec(self, token: TokenData):
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # value=""のcookieをセット=cookieを外す。
        content = {"detail": "Access token removed"}
        response = JSONResponse(content=content)
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            samesite="Strict",
            secure=False,
            max_age=0
            # domain=".local.dev",
        )

        return response
