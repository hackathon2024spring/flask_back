from sqlalchemy import select
from fastapi import status, HTTPException
from pydantic import BaseModel
from .schema import Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.user import User

class Model(BaseModel):
    async def exec(self, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # usersから、該当するuidのデータをselectする→res
        query = select(User).where(User.uid == token.uid)
        res = await database.fetch_one(query)

        # Responseを返す。
        return Response(status=1, data=Data(username = res.username, email = res.email))

