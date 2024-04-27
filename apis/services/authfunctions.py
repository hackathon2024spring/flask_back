from fastapi import Depends, HTTPException, status
from .oauth2 import OAuth2PasswordBearerWithCookie
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from databases import Database
from apis.bases.user import User
from pydantic import BaseModel
from typing import Optional  # 追加
import os

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
server = os.getenv("MYSQL_HOST_FAST")
port = os.getenv("PORT_MYSQL_FAST")
db = os.getenv("MYSQL_DB_FAST")
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{server}:{port}/{db}"
database = Database(DATABASE_URL)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


# Dependの引数にするには関数型で渡す。インスタンスはエラーになる。
def get_pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


# ユーザーの新規登録の際、そのemailが登録済かどうかを確認。
async def select_by_email(email: str):
    query = select(User).where(User.email == email)
    result = await database.fetch_one(query)
    return result


# ユーザーの認証
async def authenticate_user(email: str, password: str):
    user = await select_by_email(email)

    # userが見つからなかったり、passwordが不一致だったらFalseを返す。
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


# 文字列のpasswordとデータベースの暗号化されたpasswordが一致するか検証。
def verify_password(password, db_password):
    pwd_context = get_pwd_context()
    return pwd_context.verify(password, db_password)


# JWTを生成
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    # expire_deltaが指定されていなければ15分に設定
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # tokenの寿命設定
    to_encode.update({"exp": expire})

    # JWTを生成する。
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    uid: str


# tokenのuuidでデータベースを検索し、ユーザー情報を返す。
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # トークンが存在しない場合のエラーハンドリングを追加
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # 渡されたtokenをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")

        if uid is None:
            raise credential_exception

        # tokenのuidを取得
        token_data = TokenData(uid=uid)

    except JWTError:
        raise credential_exception

    # uidに見合うuserをデータベースから取得
    user = await get_user_by_uid(uid=token_data.uid)
    if user is None:
        raise credential_exception
    return user


# 登録されたuuidかどうかを確認。Refresh Tokenに使う。
async def get_user_by_uid(uid: str):
    query = select(User).where(User.uid == uid)
    result = await database.fetch_one(query)
    return result
