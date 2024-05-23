from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class TokenData(BaseModel):
    data: str = Field(
        ..., title="デコードされたtoken", description="cookieから取得したtoken一式"
    )


# 日付の変数名をdateにすると型付のdateがPylanceで認識されないため、わざとdayへ変更
class Data(BaseModel):
    day: date = Field(..., title="日付", description="日付")
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
        None, title="1ヶ月の運動実施日", description="日付、実施の有無"
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
                                    "day": "2024-04-01",
                                    "exerciseDone": True,
                                },
                                {
                                    "day": "2024-04-02",
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
