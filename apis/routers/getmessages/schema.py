from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Request(BaseModel):
    cid: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")


RequestExample = {"cid": 1}


class Data(BaseModel):
    isUserCreated: bool = Field(..., title="作成者ですか？", description="掲示板やチャットルームの作成者ですか？")
    id: int = Field(..., title="メッセージid", description="メッセージのid")
    message: str = Field(..., title="書き込み", description="掲示板やチャットルームの書き込み")
    created_at: str = Field(..., title="書き込み時刻", description="書き込んだ時刻")

    # created_at が datetime オブジェクトの場合に、文字列に変換するカスタムバリデータ
    @validator("created_at", pre=True, always=True)
    def datetime_to_string(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[List[Data]] = Field(
        None, title="書き込みリスト", description="作成者ですか？ メッセージid、書き込み、書き込み時刻"
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
                                    "id": 1,
                                    "message": "誰かかまってください、、",
                                    "created_at": "2024-01-12 02:18:50",
                                },
                                {
                                    "isUserCreated": False,
                                    "id": 2,
                                    "message": "何か御用で？",
                                    "created_at": "2024-01-12 02:20:43",
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
