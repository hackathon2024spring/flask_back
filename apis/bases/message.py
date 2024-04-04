from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER as Integer
from apis.bases.base import Base
from apis.bases.user import User
from apis.bases.channel import Channel


class Message(Base):
    __tablename__ = "messages"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    id = Column(Integer, primary_key=True)
    uid = Column(String(255), ForeignKey(User.uid), nullable=True)
    cid = Column(
        Integer(unsigned=True),
        ForeignKey(Channel.id, ondelete="CASCADE"),
        nullable=True
    )
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
