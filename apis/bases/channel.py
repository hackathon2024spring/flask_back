from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER as Integer
from apis.bases.base import Base
from apis.bases.user import User


class Channel(Base):
    __tablename__ = "channels"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    id = Column(
        Integer(unsigned=True), autoincrement=True, primary_key=True, index=True
    )
    uid = Column(String(36), ForeignKey(User.uid), nullable=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    abstract = Column(String(255), nullable=True)
