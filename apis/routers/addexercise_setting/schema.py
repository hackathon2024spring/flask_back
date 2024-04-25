from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")

class RequestData(BaseModel):
    exerciseId: int = Field(..., title="Exercise_id", description="選択した運動のid")

class Request(BaseModel):
    data: Optional[List[RequestData]] = Field(None, title="選択した運動idのリスト", description="選択した運動idのリスト")
    
RequestExample = [{"exerciseId": 1}, {"exerciseId": 2}]


class Data(BaseModel):
    uid: str = Field(..., title="作成者id", description="書き込み作成者id")
    cid: int = Field(..., title="掲示板id", description="掲示板やチャットルームのid")
    message: str = Field(..., title="書き込み", description="掲示板やチャットルームの書き込み")


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[Data] = Field(
        None, title="書き込んだメッセージ", description="作成者id、掲示板id、書き込み"
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