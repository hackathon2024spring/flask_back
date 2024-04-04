from pydantic import BaseModel, Field, validator
import re


class Request(BaseModel):
    email: str = Field(
        ...,
        title="email",
        description="usernameは一意ではないのでメールアドレスを使う。",
    )
    password: str = Field(..., title="パスワード", description="パスワード")

    # メールアドレスの形式を確認
    @validator("email")
    def validate_email_format(cls, email):
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email) is None:
            raise ValueError("Invalid email format")
        return email


RequestExample = {"email": "hoge@gmail.com", "password": "hogehoge"}
