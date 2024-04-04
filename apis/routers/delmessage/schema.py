from pydantic import BaseModel, Field
from typing import Optional


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Request(BaseModel):
    id: int = Field(..., title="メッセージid", description="メッセージのid")
    cid: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")


RequestExample = {"id": 1, "cid": 1}


class Data(BaseModel):
    id: int = Field(..., title="メッセージid", description="メッセージのid")
    cid: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")
    message: str = Field(..., title="書き込み", description="掲示板やチャットルームの書き込み")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[Data] = Field(
        None, title="削除したメッセージ", description="メッセージid、掲示板id、削除したメッセージ"
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
                                "id": 1,
                                "cid": 1,
                                "message": "誰かかまってください、、",
                            },
                        },
                    },
                    "error": {"summary": "エラーケース1", "value": {"status": 0}},
                }
            }
        },
    }
}
