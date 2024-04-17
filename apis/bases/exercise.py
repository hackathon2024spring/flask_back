from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER as Integer
from apis.bases.base import Base


class Exercise(Base):
    __tablename__ = "exercise"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    id = Column(Integer, primary_key=True)
    exercise_name = Column(String(64), nullable=False, index=True)
