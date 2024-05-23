from sqlalchemy import Column, Date, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER as Integer
from ddd.infrastructure.orms.base import Base
from ddd.infrastructure.orms.user import User
from ddd.infrastructure.orms.exercise import Exercise


class ExerciseDone(Base):
    __tablename__ = "exercises_done"  # テーブル名 __tablename__はsqlalchemyの特別な変数
    user_id = Column(String(255), ForeignKey(User.uid), nullable=False)
    exercise_id = Column(
        Integer(unsigned=True),
        ForeignKey(Exercise.id, ondelete="CASCADE"),
        nullable=False,
    )
    date = Column(Date, nullable=False)
    done = Column(Boolean, nullable=False)
    # 複合主キー設定。既存テーブルの再定義を認める。
    __table_args__ = (
        PrimaryKeyConstraint(user_id, exercise_id, date),
        {"extend_existing": True},
    )

    # printで表示するための関数
    def __repr__(self):
        return f"<ExerciseDone(user_id={self.user_id}, exercise_id={self.exercise_id}, date={self.date}, done={self.done})>"

    def __str__(self):
        return f"ExerciseDone(user_id={self.user_id}, exercise_id={self.exercise_id}, date={self.date}, done={self.done})"
