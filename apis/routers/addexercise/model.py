from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert
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
        
        # exercise_doneテーブルから、該当するuser_id,dateのデータを全て削除する。
        delete_query = delete(ExerciseDone).where(
            ExerciseDone.user_id == token.uid, ExerciseDone.date == date
            )
        await database.execute(delete_query)

        # exercise_doneテーブルに、postされたexecise_id,dateを登録する。
        # user_idとpostされたexecise_id,dateの組それぞれの辞書を作り、それをリストにまとめる=data_insert
        data_insert = [{"user_id": token.uid, "exercise_id": item.exerciseId, "date": date} 
                       for item in body.done]

        # data_insertリストをexercise_doneテーブルにinsertするqueryを作成する
        query = insert(ExerciseDone).values(data_insert)
        # テーブルを更新する
        await database.execute(query)
        
        # レスポンスを返す。
        return Response(status=1)
