from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy.dialects.mysql import insert
from .schema import Request, Response, TokenData
from apis.services.authfunctions import database
from apis.bases.exercise_selected import ExerciseSelected


class Model(BaseModel):
    async def exec(self, body: Request, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # exercise_selectedテーブルに、postされたexecise_id,selectedを登録する。
        # user_idとpostされたexecise_id,selectedのそれぞれの辞書を作り、それをリストにまとめる=data_insert
        data_insert = [{"user_id": token.uid, "exercise_id": item.exerciseId, "selected": item.selected}
                       for item in body.data]

        # data_insertリストをexercise_selectedテーブルにinsertするqueryを作成する
        insert_stmt = insert(ExerciseSelected).values(data_insert)
        # すでに同じプライマリーキーのレコードがある場合、selectedのみをupdateする
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            selected=insert_stmt.inserted.selected
        )
        # UPSERT操作
        await database.execute(query=on_duplicate_key_stmt)

        return Response(status=1)

        
        