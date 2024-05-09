from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(..., title="デコードされたtoken", description="cookieから取得したtoken一式")


class Data(BaseModel):    
    exerciseId: int = Field(..., title="exercise_id", description="運動のid")
    exerciseName: str = Field(..., title="exercise_name", description="運動の名前")
    exerciseSelected: bool = Field(..., title="exercise_selected", description="運動の選択の有無")

class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[List[Data]] = Field(
        None, title="実施できる運動設定の編集画面", description="運動項目、選択の有無"
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
                            "data": [
                                {
                                    "exerciseId": 1,
                                    "exerciseName": "階段を使う",
                                    "exerciseSelected": True,
                                },
                                {
                                    "exerciseId": 5,
                                    "exerciseName": "一駅分歩く",
                                    "exerciseSelected": False,
                                },
                            ],
                        },
                    },
                    "error": {
                        "summary": "クエリリクエスト失敗",
                        "value": {"status": 0, "data": []},
                    },
                }
            }
        },
    }
}