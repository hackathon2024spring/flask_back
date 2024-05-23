from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER as Integer
from ddd.infrastructure.orms.base import Base


class Exercise(Base):
    __tablename__ = "exercises"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    __table_args__ = {"extend_existing": True}  # 既存テーブルの再定義を認める。
    id = Column(Integer(unsigned=True), primary_key=True)
    exercise_name = Column(String(64), nullable=False, index=True)

    # printで表示するための関数
    def __repr__(self):
        return f"<Exercise(id={self.id}, exercise_name={self.exercise_name})>"

    def __str__(self):
        return f"Exercise(id={self.id}, exercise_name={self.exercise_name})"
