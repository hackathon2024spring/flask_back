from pydantic import BaseModel, Field
from typing import Optional


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")

class Data(BaseModel):
    username: str = Field(..., title="user_name", description="ユーザー名")
    email: str = Field(..., title="email", description="登録メールアドレス")

class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[Data] = Field(
        None, title="ログインしているuser", description="ログインしているuserのusernameとemail"
    )



ResponseExamples = {
    200: {
        "description": "Success resuls must be list.",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "クエリリクエスト成功",
                        "value": {
                            "status": 1,
                            "data": {
                                "username": "hogehoge",
                                "email": "hoge@gmail.com",
                            },
                        },
                    },
                    "error": {
                        "summary": "クエリリクエスト失敗",
                        "value": {"status": 0},
                    },
                }
            }
        },
    }
}