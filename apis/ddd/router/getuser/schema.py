from pydantic import BaseModel, Field

# cookieを解析してデータベースに問い合わせるので、Requestは無い。


class Data(BaseModel):
    username: str = Field(..., title="ユーザー名", description="ユーザー名")
    email: str = Field(..., title="email", description="登録メールアドレス")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1 不正はエラー処理に統合",
    )
    data: Data = Field(
        None, title="登録したuser", description="登録したuserのuidとusername"
    )


ResponseExamples = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "成功",
                        "value": {
                            "status": 1,
                            "data": {"username": "hogehoge", "email": "hoge@gmail.com"},
                        },
                    },
                    "error": {
                        "summary": "失敗",
                        "value": {
                            "detail": "エラーメッセージ",
                        },
                    },
                }
            }
        },
    }
}
