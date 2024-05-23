from pydantic import BaseModel, Field
from typing import Optional, List


class TokenData(BaseModel):
    data: str = Field(
        ..., title="デコードされたtoken", description="cookieから取得したtoken一式"
    )


class Data(BaseModel):
    exerciseId: int = Field(..., title="exercise_id", description="運動のid")
    exerciseName: str = Field(..., title="exercise_name", description="運動の名前")
    exerciseDone: bool = Field(
        ..., title="exercise_done", description="運動の実施の有無"
    )


class Response(BaseModel):
    status: int = Field(
        ...,
        title="ステータス",
        description="正しい場合1、不正の場合0",
    )
    data: Optional[List[Data]] = Field(
        None, title="1日の運動の編集画面", description="運動項目、実施の有無"
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
                                    "exerciseDone": True,
                                },
                                {
                                    "exerciseId": 5,
                                    "exerciseName": "一駅分歩く",
                                    "exerciseDone": False,
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
