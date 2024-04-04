from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Data(BaseModel):
    isUserCreated: bool = Field(..., title="作成者ですか？", description="掲示板やチャットルームの作成者ですか？")
    cid: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")
    name: str = Field(..., title="掲示板の名前", description="掲示板やチャットルームの名前")
    abstract: str = Field(..., title="掲示板の説明", description="掲示板やチャットルームの説明")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[List[Data]] = Field(
        None, title="掲示板情報リスト", description="作成者ですか？ 掲示板id、掲示板名、説明"
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
                            "results": [
                                {
                                    "isUserCreated": True,
                                    "cid": 1,
                                    "name": "ぼっち部屋",
                                    "abstract": "hogeさんの孤独な部屋です",
                                },
                                {
                                    "isUserCreated": False,
                                    "cid": 2,
                                    "name": "サッカー部屋",
                                    "abstract": "fugaさんのサッカー部屋です",
                                },
                            ],
                        },
                    },
                    "error": {
                        "summary": "クエリリクエスト失敗",
                        "value": {"status": 0, "results": []},
                    },
                }
            }
        },
    }
}
