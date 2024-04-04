from pydantic import BaseModel, Field
from typing import Optional


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Request(BaseModel):
    name: str = Field(..., title="掲示板の名前", description="掲示板やチャットルームの名前")
    abstract: str = Field(..., title="掲示板の説明", description="掲示板やチャットルームの説明")


RequestExample = {"name": "ぼっち部屋", "abstract": "hogeさんの孤独な部屋です"}


class Data(BaseModel):
    uid: str = Field(..., title="作成者のid", description="掲示板やチャットルームの作成者id")
    name: str = Field(..., title="掲示板の名前", description="掲示板やチャットルームの名前")
    abstract: str = Field(..., title="掲示板の説明", description="掲示板やチャットルームの説明")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[Data] = Field(None, title="作成した掲示板情報", description="作成者id、掲示板名、説明")


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
                                "name": "ぼっち部屋",
                                "abstract": "テストさんの孤独な部屋です",
                            },
                        },
                    },
                    "error": {"summary": "エラーケース1", "value": {"status": 0}},
                }
            }
        },
    }
}
