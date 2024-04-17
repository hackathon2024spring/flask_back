from sqlalchemy import and_
from fastapi import status, HTTPException
from pydantic import BaseModel
from .schema import Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.channel import Channel


class Model(BaseModel):
    async def exec(self, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        query = Channel.__table__.select()
        result = await database.fetch_all(query)

        arry = []  # dataリストを初期化
        for channel in result:
            # ここでisUserCreatedを設定する。
            is_user_created = channel.uid == token.uid
            dt = Data(
                isUserCreated=is_user_created,
                cid=channel.id,
                name=channel.name,
                abstract=channel.abstract,
            )
            arry.append(dt)
        return Response(status=1, data=arry)
