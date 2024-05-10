from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")

class RequestData(BaseModel):
    exerciseId: int = Field(..., title="Exercise_id", description="運動のid")
    selected: bool = Field(..., title="selected", description="選択したかどうか")

class Request(BaseModel):
    data: Optional[List[RequestData]] = Field(None, title="選択したかどうかの運動のリスト", description="選択したかどうかの運動のリスト")
    
RequestExample = {"data": [{"exerciseId": 1, "selected": True}, {"exerciseId": 2, "selected": True}]}


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
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
                            },
                        },
                    },
                    "error": {"summary": "エラーケース1", "value": {"status": 0}},
                }
            }
        },
    }
