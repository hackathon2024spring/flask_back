from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy.dialects.mysql import insert
from .schema import Request, Response, TokenData
from apis.services.authfunctions import database
from apis.bases.exercise_done import ExerciseDone


class Model(BaseModel):
    async def exec(self, date, body: Request, token: TokenData) -> Response:
        # loginしていない場合、拒否する。
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        
        # exercise_doneテーブルに、postされたdate,execise_id,doneを登録する。
        # user_idとpostされたexecise_id,date,doneの組それぞれの辞書を作り、それをリストにまとめる=data_insert 
        data_insert = [{"user_id": token.uid, "exercise_id": item.exerciseId, "date": date, "done": item.done} 
                       for item in body.data]
        
        # data_insertリストをexercise_doneテーブルにinsertするqueryを作成する
        insert_stmt = insert(ExerciseDone).values(data_insert)
        # すでに同じプライマリーキーのレコードがある場合、doneのみをupdateする
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            done=insert_stmt.inserted.done
        )
        # UPSERT操作
        await database.execute(query=on_duplicate_key_stmt)

        return Response(status=1)
