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

        # Channelテーブルに挿入するクエリ作成
        query = Channel.__table__.insert().values(
            uid=token.uid,
            name=body.name,
            abstract=body.abstract,
        )
        # テーブル更新
        await database.execute(query)

        dt = Data(uid=token.uid, name=body.name, abstract=body.abstract)
        return Response(status=1, data=dt)
