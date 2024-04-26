from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert
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
        
        # exercise_selectedテーブルから、該当するuser_idのデータを全て削除する。
        # 先に確認はいる？→対象レコード0でもエラーにはならないので大丈夫そう？
        delete_query = delete(ExerciseSelected).where(ExerciseSelected.user_id == token.uid,)
        await database.execute(delete_query)

        # exercise_selectedテーブルに、postされたexecise_idを登録する。
        # user_idとpostされたexecise_idのそれぞれの辞書を作り、それをリストにまとめる=data_insert
        data_insert = [{"user_id": token.uid, "exercise_id": item.exerciseId} for item in body.selected]

        # data_insertリストをexercise_selectedテーブルにinsertするqueryを作成する
        query = insert(ExerciseSelected).values(data_insert)
        # テーブルを更新する
        await database.execute(query)
        
        # レスポンスを返す。
        return Response(status=1)


        # # Channelテーブルに挿入するクエリ作成
        # query = Message.__table__.insert().values(
        #     uid=token.uid,
        #     cid=body.cid,
        #     message=body.message,
        # )
        # # テーブル更新
        # await database.execute(query)

        # dt = Data(uid=token.uid, cid=body.cid, message=body.message)
        # return Response(status=1, data=dt)
