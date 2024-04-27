from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")

class RequestData(BaseModel):
    exerciseId: int = Field(..., title="Exercise_id", description="運動のid")

# dateDoneを単なるdateにするとエラーになるためdateDoneで命名（型注釈dateと同じ名前だとField関数の関係でエラー？）
class Request(BaseModel):
    dateDone: date = Field(..., title="実施した日付", description="実施した日付")
    done: Optional[List[RequestData]] = Field(None, title="実施した運動idのリスト", description="実施した運動idのリスト")
    
RequestExample = {"dateDone": "2024-04-03", "done": [{"exerciseId": 1}, {"exerciseId": 2}]}

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
