from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")

class RequestData(BaseModel):
    exerciseId: int = Field(..., title="Exercise_id", description="運動のid")

class Request(BaseModel):
    done: Optional[List[RequestData]] = Field(None, title="実施した運動idのリスト", description="実施した運動idのリスト")
    
RequestExample = {"done": [{"exerciseId": 1}, {"exerciseId": 2}]}

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
                    "error": {"summary": "エラーケース1", "value": {"status": 0}},
                }
            }
        },
    }
}
