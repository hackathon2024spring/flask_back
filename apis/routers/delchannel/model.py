from sqlalchemy import and_
from fastapi import status, HTTPException
from pydantic import BaseModel
from .schema import Request, Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.channel import Channel


class Model(BaseModel):
    async def exec(self, body: Request, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # 特定のIDを持つメッセージを選択するクエリ
        query = Channel.__table__.select().where(
            and_(Channel.id == body.id, Channel.uid == token.uid)
        )

        result = await database.fetch_one(query)

        if result is None:
            # レコードが存在しない場合の処理
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
            )

        # レコードが存在する場合、削除するクエリ
        delete_query = Channel.__table__.delete().where(
            and_(Channel.id == body.id, Channel.uid == token.uid)
        )
        await database.execute(delete_query)

        dt = Data(id=body.id, name=result.name)
        return Response(status=1, data=dt)
