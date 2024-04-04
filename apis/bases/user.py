from sqlalchemy import Column, String
from apis.bases.base import Base
import uuid


# emailの重複を禁止し、uuidでtokenを作る。emailで作るとcookie解析でバレる。
class User(Base):
    __tablename__ = "users"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    # 新しいレコードが挿入される際に、lambdaで指定する関数の出力をデフォルト値として使う
    uid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(64), unique=True, nullable=False, index=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(255), nullable=False)
