from pydantic import BaseModel
from fastapi import HTTPException
from uuid import uuid4
from apis.services.authfunctions import database, get_pwd_context, select_by_email
from apis.bases.user import User
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
            query = User.__table__.insert().values(
                uid=new_uuid,
                email=body.email,
                username=body.username,
                password=hashed_password,
            )
            # テーブル更新
            await database.execute(query)
            return Response(status=1, data=Data(uid=new_uuid, username=body.username))
