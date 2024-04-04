from sqlalchemy import and_
from fastapi import status, HTTPException
from pydantic import BaseModel
from .schema import Request,Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.message import Message


class Model(BaseModel):
    async def exec(self, body: Request,token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        query = Message.__table__.select().where(Message.cid == body.cid,)
        result = await database.fetch_all(query)

        arry = []  # dataリストを初期化
        for msg in result:
            # ここでisUserCreatedを設定する。
            is_user_created = msg.uid == token.uid
            dt = Data(
                isUserCreated=is_user_created,
                id=msg.id,
                message=msg.message,
                created_at=msg.created_at,
            )
            arry.append(dt)
        return Response(status=1, data=arry)
