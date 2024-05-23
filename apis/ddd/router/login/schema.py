from pydantic import BaseModel


class Request(BaseModel):
    email: str
    password: str


RequestExample = {"email": "hoge@gmail.com", "password": "hogehoge"}

ResponseExamples = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "success": {
                        "summary": "成功",
                        "value": {
                            "status": 200,
                            "data": {
                                "token_type": "bearer",
                            },
                        },
                    },
                    "error": {
                        "summary": "失敗",
                        "value": {
                            "status": 500,
                            "data": {
                                "detail": "message about 500 error",
                            },
                        },
                    },
                }
            }
        },
    }
}
