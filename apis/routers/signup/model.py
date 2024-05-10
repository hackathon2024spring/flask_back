from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy import select, insert
from uuid import uuid4
from apis.services.authfunctions import database, get_pwd_context, select_by_email
from apis.bases.user import User
from apis.bases.exercise import Exercise
from apis.bases.exercise_selected import ExerciseSelected
from .schema import Request, Response, Data


class Model(BaseModel):
    async def exec(self, body: Request) -> Response:
        # 既に登録されているユーザーかを確認
        DBuser = await select_by_email(body.email)
        if DBuser is not None:
            raise HTTPException(status_code=409, detail="登録済みです")
        else:
            # hash用ヘルパー関数を取得
            pwd_context = get_pwd_context()
            # パスワードをhash化
            hashed_password = pwd_context.hash(body.password1)
            # ユーザーidをuuidで生成
            new_uuid = str(uuid4())
            # Userテーブルに挿入するクエリ作成
            query_user = User.__table__.insert().values(
                uid=new_uuid,
                email=body.email,
                username=body.username,
                password=hashed_password,
            )

            # 運動を全て実施できるようにする（初期設定）
            # exercises_selectedテーブルに、全てのexercise_id、該当するユーザーid、selected=trueでinsertする
            
            # exercisesテーブルから全てのidをselect
            query_exe = select(Exercise.id)
            res_exe = await database.fetch_all(query_exe)

            # ユーザーid、selected=trueを付加し、クエリ作成
            data_insert = [{"user_id": new_uuid, "exercise_id": exe.id, "selected": True}
                       for exe in res_exe]
            query_selected = insert(ExerciseSelected).values(data_insert)

            try:
                async with database.transaction():
                    # userテーブル更新
                    await database.execute(query_user)
                    # exercises_selectedテーブル更新
                    await database.execute(query_selected)

                    return Response(status=1, data=Data(uid=new_uuid, username=body.username))
            
            except Exception:
                # エラーが発生した場合の処理
                return Response(status=0)

            
