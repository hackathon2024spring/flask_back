from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import date
from ddd.domain.value_object import Password, UserId, UserName


class User(BaseModel):
    a_uid: str = Field(default_factory=lambda: UserId().id())
    a_username: UserName = Field(..., title="ユーザー名", description="ユーザー名")
    a_email: EmailStr = Field(
        ..., title="emailアドレス", description="メールアドレス。変更不可"
    )
    a_password: Password = Field(..., title="パスワード", description="hash化済")
    a_confirm: Password = Field(
        ...,
        title="パスワード確認",
        description="passwordと比較し、同一かどうかチェック",
    )

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get("a_password")
        confirm = values.get("a_confirm")
        if password != confirm:
            raise ValueError("パスワードが一致しません")
        return values

    def id(self):
        return self.a_uid

    def name(self):
        return self.a_username.name()

    def email(self):
        return self.a_email

    def password(self):
        return self.a_password.password()


class RegisteredUser(BaseModel):
    a_uid: str = Field(
        ..., title="登録済のユーザーId", description="登録済のユーザーId"
    )
    a_username: UserName = Field(
        ..., title="登録済のユーザー名", description="登録済のユーザー名"
    )

    def id(self):
        return self.a_uid

    def name(self):
        return self.a_username.name()


# Exerciseテーブルの基本エンティティ
class Exercise(BaseModel):
    a_id: str = Field(..., title="運動のid", description="運動のid")
    a_exercise_name: str = Field(..., title="運動の名前", description="運動の名前")

    def id(self):
        return self.a_id

    def exercise_name(self):
        self.a_exercise_name


# 選択したExerciseをDDDに取り込む
class ExerciseSelected(BaseModel):
    a_id: str = Field(..., title="運動のid", description="運動のid")
    a_selected: bool = Field(
        ..., title="選択したらTrue", description="デフォルトはTrue"
    )

    def id(self):
        return self.a_id

    def selected(self):
        return self.a_selected


# uidはtokenから抽出するので、ExerciseSelectedと異なる層で作られる。
class ExerciseSelectedRequest(ExerciseSelected):
    a_user_id: str = Field(..., title="ユーザーのid", description="ユーザーのid")

    def user_id(self):
        return self.a_user_id


# 何を選択したのかをexcercise_nameを返す。
class ExerciseSelectedResponse(ExerciseSelected):
    a_exercise_name: str = Field(..., title="運動の名前", description="運動の名前")

    def exercise_name(self):
        return self.a_exercise_name


# 実施したExerciseをDDDに取り込む
class ExerciseDone(BaseModel):
    a_id: str = Field(..., title="運動のid", description="運動のid")
    a_done: bool = Field(..., title="選択したらTrue", description="運動の実施の有無")

    def id(self):
        return self.a_id

    def done(self):
        return self.a_done


# uidはtokenから抽出するので、ExerciseDoneと異なる層で作られる。
class ExerciseDoneRequest(ExerciseDone):
    a_user_id: str = Field(..., title="ユーザーのid", description="ユーザーのid")
    a_date: date = Field(..., title="日付", description="YYYY-MM-DDの文字列")

    def user_id(self):
        return self.a_user_id

    def date(self):
        return self.a_date


# dateに何を実施したのかをexcercise_nameを返す。
class ExerciseDoneResponse(ExerciseDone):
    a_exercise_name: str = Field(..., title="exercise_name", description="運動の名前")

    def exercise_name(self):
        return self.a_exercise_name


# 年月で実施した運動を取得
class CalendarRequest(BaseModel):
    a_year: int = Field(..., title="年", description="実施した運動を年月で取得")
    a_month: int = Field(..., title="月", description="実施した運動を年月で取得")

    def year(self):
        return self.a_year

    def month(self):
        return self.a_month


# 取得した年月の運動を返す
class CalendarResponse(BaseModel):
    a_date: date = Field(..., title="日付", description="日付")
    a_exerciseDone: bool = Field(
        ..., title="exercise_done", description="運動の実施の有無"
    )

    def date(self):
        return self.a_date

    def exercise_done(self):
        return self.a_exerciseDone
