from pydantic import BaseModel, Field
from typing import Optional


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Request(BaseModel):
    id: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")


RequestExample = {"id": 1}


class Data(BaseModel):
    id: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")
    name: str = Field(..., title="掲示板の名前", description="掲示板やチャットルームの名前")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[Data] = Field(None, title="削除した掲示板", description="掲示板id、掲示板の名前")


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
                                "name": "ぼっち部屋",
                            },
                        },
                    },
                    "error": {"summary": "エラーケース1", "value": {"status": 0}},
                }
            }
        },
    }
}
