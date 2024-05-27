import uuid
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator
import re
import hashlib


# pydanticは_から始まる属性を宣言できない。そのためget_hoge()になりがちなのでa_をつけることにする。
class Password(BaseModel):
    a_password: str = Field(..., title="パスワード", description="hash化されている")

    # パスワードをバリデートし、ハッシュ化してその値を保存
    @field_validator("a_password", mode="before")
    def validate_and_hash_password(cls, v):
        if not isinstance(v, str):
            raise ValueError("文字列のみ受け付けます。")
        if not re.match(r"^[a-zA-Z0-9_.+\-@/]+$", v):
            raise ValueError("パスワード半角英数と_.+-@のみです")
        if len(v) < 8:
            raise ValueError("パスワードは8文字以上です。")
        return hashlib.sha256(v.encode("utf-8")).hexdigest()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.a_password == other.a_password

    def __hash__(self):
        return hash(self.a_password)

    def password(self):
        # hash化されたpasswordを返す。
        return self.a_password

    def change_password(self, new_password: str):
        # passwordを更新すると@validatorが発火し、検証を経て直接hash化される。
        self.password = new_password

    def verify_password(self, hashed_password: str):
        # 属性で持つhash化passwordと入力されたpasswordを比較
        return self.password() == hashed_password


class UserName(BaseModel):
    a_name: str = Field(..., title="username", description="")

    @field_validator("a_name", mode="before")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_.+]+$", v):
            raise ValueError("ユーザー名は半角英数と_.+のみです")
        if len(v) < 8:
            raise ValueError("ユーザー名は8文字以上です。")
        return v

    def name(self):
        return self.a_name

    def change_username(self, new_username: str):
        self.a_name = new_username


class UserId(BaseModel):
    a_uid: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.a_uid == other.a_uid

    def __hash__(self) -> int:
        return hash(self.a_uid)

    def id(self):
        return self.a_uid


class SessionID:
    def __init__(self, value: str = None):
        self.value = value or str(uuid4())

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, SessionID):
            return self.value == other.value
        return False
