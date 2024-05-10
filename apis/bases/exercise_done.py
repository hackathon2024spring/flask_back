from sqlalchemy import Column, Date, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER as Integer
from apis.bases.base import Base
from apis.bases.user import User
from apis.bases.exercise import Exercise


class ExerciseDone(Base):
    __tablename__ = "exercises_done"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    user_id = Column(String(255), ForeignKey(User.uid), nullable=False)
    exercise_id = Column(
        Integer(unsigned=True),
        ForeignKey(Exercise.id, ondelete="CASCADE"),
        nullable=False
    )
    date = Column(Date, nullable=False)
    done = Column(Boolean, nullable=False)
    # 複合主キー設定。既存テーブルの再定義を認める。
    __table_args__ = (
        PrimaryKeyConstraint(user_id, exercise_id, date),
        {"extend_existing": True}
    )