from pydantic import BaseModel, Field


class Request(BaseModel):
    username: str
    email: str
    password1: str
    password2: str


RequestExample = {
    "username": "hogehoge",
    "email": "hoge@gmail.com",
    "password1": "hogehoge",
    "password2": "hogehoge",
}


class Data(BaseModel):
    uid: str = Field(..., title="uuid", description="一意のid")
    username: str = Field(..., title="ユーザー名", description="ユーザー名")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
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
                            "data": {
                                "uid": "550e8400-e29b-41d4-a716-446655440000",
                                "username": "hogehoge",
                            },
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
