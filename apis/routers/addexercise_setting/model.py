from fastapi import status, HTTPException
from pydantic import BaseModel
from .schema import Request, Response, TokenData, Data
from apis.services.authfunctions import database
from apis.bases.message import Message


class Model(BaseModel):
    async def exec(self, body: Request, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # exercise_selectedテーブルから、該当するuser_idのデータを全て削除する。
        # exercise_selectedテーブルに、postされたexecise_idを登録する。
        # レスポンスを返す。


        # Channelテーブルに挿入するクエリ作成
        query = Message.__table__.insert().values(
            uid=token.uid,
            cid=body.cid,
            message=body.message,
        )
        # テーブル更新
        await database.execute(query)

        dt = Data(uid=token.uid, cid=body.cid, message=body.message)
        return Response(status=1, data=dt)
