import os
from typing import List
from datetime import date, timedelta
from sqlalchemy import (
    Column,
    Date,
    Table,
    and_,
    asc,
    case,
    func,
    literal,
    text,
)
from sqlalchemy.future import select
from sqlalchemy.dialects.mysql import insert
from pydantic import EmailStr
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ddd.infrastructure.orms.base import Base
from ddd.infrastructure.orms.user import User as OrmUser
from ddd.infrastructure.orms.exercise import Exercise as OrmExercise
from ddd.infrastructure.orms.exercise_selected import (
    ExerciseSelected as OrmExerciseSelected,
)
from ddd.infrastructure.orms.exercise_done import ExerciseDone as OrmExerciseDone
from ddd.domain.value_object import UserName
from ddd.domain.entity import (
    CalendarRequest,
    CalendarResponse,
    RegisteredUser,
    User as DomainUser,
    ExerciseSelectedRequest as DomainExerciseSelectedRequest,
    ExerciseSelectedResponse as DomainExerciseSelectedResponse,
    Exercise as DomainExercise,
    ExerciseDoneRequest as DomainExerciseDoneRequest,
    ExerciseDoneResponse as DomainExerciseDoneResponse,
)
from ddd.domain.repository import UserRepository


class UserRepositoryImpl(UserRepository):
    @classmethod
    def get_instance(cls) -> "UserRepository":
        return cls()

    def get_database_url(self):
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        server = os.getenv("MYSQL_HOST_FAST")
        port = os.getenv("PORT_MYSQL_FAST")
        db = os.getenv("MYSQL_DB_FAST")
        return f"mysql+aiomysql://{user}:{password}@{server}:{port}/{db}"

    def get_engine(self):
        return create_async_engine(self.get_database_url(), echo=True)

    def get_session(self):
        engine = self.get_engine()
        return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async def session_scope(self):
        async_session = self.get_session()
        async with async_session() as session:
            yield session
            await session.commit()

    # 新規ユーザーをUserテーブルに登録
    async def register_user(self, user: DomainUser) -> RegisteredUser:
        async for session in self.session_scope():
            result = await session.execute(
                select(OrmUser).filter_by(email=user.email())
            )
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Emailアドレス・パスワードに問題があります。",
                )
            orm_user = OrmUser(
                uid=user.id(),
                username=user.name(),
                email=user.email(),
                password=user.password(),
            )
            session.add(orm_user)

            registered_user = RegisteredUser(
                a_uid=user.id(), a_username=UserName(a_name=user.name())
            )

        # sessionの外で返す必要があるらしい。タブ1つで結果が大きく変わるので注意。
        return registered_user

    # emailが登録されていない等、OrmUserを返せない場合は全てHTTPExceptionにした。
    async def get_user_by_email(self, email: EmailStr) -> OrmUser:
        async for session in self.session_scope():
            result = await session.execute(select(OrmUser).filter_by(email=email))
            registered_user = result.scalars().first()
            if registered_user:
                dto_user = OrmUser(
                    uid=registered_user.uid,
                    username=registered_user.username,
                    email=registered_user.email,
                    password=registered_user.password,
                )
                return dto_user
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Emailアドレス・パスワードに問題があります。",
                )

    # uidが存在しない等、OrmUserを返せない場合は全てHTTPExceptionにした。
    async def get_user_by_uid(self, uid: str) -> OrmUser:
        async for session in self.session_scope():
            result = await session.execute(select(OrmUser).filter_by(uid=uid))
            login_user = result.scalars().first()
            if login_user:
                dto_user = OrmUser(
                    uid=login_user.uid,
                    username=login_user.username,
                    email=login_user.email,
                    password=login_user.password,
                )
                return dto_user
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="cookieに不正があるかもしれません。",
                )

    # 選択可能のexercisesを取得。ユーザー情報なし
    async def get_exercises(self) -> List[DomainExercise]:
        async for session in self.session_scope():
            result = await session.execute(
                select(OrmExercise).order_by(asc(OrmExercise.id))
            )
            exercises_dat = result.scalars().all()
            exercises = [
                # 取得したexerciseをDomainExerciseに変換して返す。
                # 面倒でもDDDの世界では値オブジェクトやエンティティで層を跨ぐべき
                DomainExercise(a_id=str(exe.id), a_exercise_name=exe.exercise_name)
                for exe in exercises_dat
            ]

        return exercises

    # 選択したexerciseを保存。ユーザー情報あり
    async def add_exercises_selected(
        self, exercises_selected: List[DomainExerciseSelectedRequest]
    ):
        async for session in self.session_scope():
            exes = [
                OrmExerciseSelected(
                    user_id=exe.user_id(),
                    exercise_id=int(exe.id()),
                    selected=True,
                )
                for exe in exercises_selected
            ]
            session.add_all(exes)
            await session.commit()
            return True

    # ユーザーidとexercise idが一致するもののselectedを上書き更新(upsertという)
    async def upsert_exercises_selected(
        self, exercises_selected: list[DomainExerciseSelectedRequest]
    ):
        async for session in self.session_scope():
            for exe in exercises_selected:
                stmt = (
                    insert(OrmExerciseSelected)
                    .values(
                        user_id=exe.user_id(),
                        exercise_id=int(exe.id()),
                        selected=exe.selected(),
                    )
                    .on_duplicate_key_update(selected=exe.selected())
                )
                await session.execute(stmt)
            await session.commit()
            return True

    # 直近のexercisesを考慮してexercises_selectedを更新。
    # 新規発生したexerciseはselected=Trueにする
    async def get_exercises_selected(
        self, uid: str
    ) -> List[DomainExerciseSelectedResponse]:
        # exercisesとexercises_selectedを左結合し、selectedがない場合はTrueを設定
        # exercisesの左結合→新規のexercise_idが追加される。FKで連携削除済。
        # exercisesで新設されたexercise_idのselectedは空欄→Trueで埋める
        async for session in self.session_scope():
            # exercisesとexercises_selectedをid==exercise_idとuser_id == uidで左結合し
            # exercise_idがNoneはuser_id = uid、selected=Trueに設定
            query = (
                select(
                    OrmExercise.id.label("exercise_id"),
                    OrmExercise.exercise_name.label("exercise_name"),
                    case(
                        (
                            OrmExerciseSelected.selected != None,
                            OrmExerciseSelected.selected,
                        ),
                        else_=literal(True),
                    ).label("selected"),
                )
                .outerjoin(
                    OrmExerciseSelected,
                    and_(
                        OrmExerciseSelected.exercise_id == OrmExercise.id,
                        OrmExerciseSelected.user_id == uid,
                    ),
                )
                .order_by(OrmExercise.id)
            )

            result = await session.execute(query)
            records = result.fetchall()

            # DDDで扱うentityに変換
            domain_exercises_selected_response = [
                DomainExerciseSelectedResponse(
                    a_id=str(record.exercise_id),
                    a_selected=record.selected,
                    a_exercise_name=record.exercise_name,
                )
                for record in records
            ]

        return domain_exercises_selected_response

    # 実施したexerciseをExerciseDoneテーブルに登録。重複はdoneのみ更新。
    async def upsert_exercises_done(
        self, exercises_done: list[DomainExerciseDoneRequest]
    ):
        async for session in self.session_scope():
            for exe in exercises_done:
                stmt = (
                    insert(OrmExerciseDone)
                    .values(
                        user_id=exe.user_id(),
                        exercise_id=int(exe.id()),
                        date=exe.date(),
                        done=exe.done(),
                    )
                    .on_duplicate_key_update(done=exe.done())
                )
                await session.execute(stmt)
            await session.commit()
        return True

    # 直近のexercisesを考慮してexercises_doneを抽出。
    async def get_exercises_done(
        self, uid: str, date: date
    ) -> List[DomainExerciseDoneResponse]:
        # Trueで抽出した結果をFalseで出力したり、条件が介在するテーブル生成は
        # ブール代数で表現できないらしい。また1つのクエリ文では挙動が不明瞭なので
        # わかりやすいSELECT文をサブクエリで先に定義し、それを組み合わせる。

        async for session in self.session_scope():

            # dateのExerciseDoneを抽出
            done_subquery = (
                select(OrmExerciseDone.exercise_id, OrmExerciseDone.done)
                .where(OrmExerciseDone.user_id == uid, OrmExerciseDone.date == date)
                .alias("done_subquery")
            )

            #
            selected_subquery = (
                select(OrmExerciseSelected.exercise_id)
                .where(
                    OrmExerciseSelected.user_id == uid,
                    OrmExerciseSelected.selected == True,
                )
                .alias("selected_subquery")
            )

            query = (
                select(
                    OrmExercise.id,
                    OrmExercise.exercise_name,
                    case(
                        (
                            (done_subquery.c.exercise_id == OrmExercise.id)
                            & (done_subquery.c.done == True),
                            literal(True),
                        ),
                        (
                            selected_subquery.c.exercise_id == OrmExercise.id,
                            literal(False),
                        ),
                        else_=literal(None),
                    ).label("done"),
                )
                .select_from(OrmExercise)
                .outerjoin(done_subquery, OrmExercise.id == done_subquery.c.exercise_id)
                .outerjoin(
                    selected_subquery, OrmExercise.id == selected_subquery.c.exercise_id
                )
                .order_by(OrmExercise.id)
                .having(text("done IS NOT NULL"))
            )

            result = await session.execute(query)
            records = result.fetchall()

            # DDDで扱うentityに変換
            domain_exercises_done_response = [
                DomainExerciseDoneResponse(
                    a_id=str(record.id),
                    a_done=record.done,
                    a_exercise_name=record.exercise_name,
                )
                for record in records
            ]

        return domain_exercises_done_response

    async def get_exercises_this_month(self, uid: str, calendar: CalendarRequest):
        # 日付範囲を生成する関数
        def generate_date_values(year, month):
            start_date = date(year, month, 1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(
                days=1
            )
            current_date = start_date
            date_values = []
            while current_date <= end_date:
                date_values.append(f"('{current_date.isoformat()}')")
                current_date += timedelta(days=1)
            return ", ".join(date_values)

        async for session in self.session_scope():
            # 日付範囲の文字列結合。一続きの文字列でなければsqlalchemyはテーブルを作れない。
            date_values = generate_date_values(calendar.year(), calendar.month())

            # 一時テーブルの定義
            date_range_table = Table(
                "date_range",
                Base.metadata,
                Column("day", Date, primary_key=True),
                extend_existing=True,
            )

            # 既存の一時テーブルを削除
            await session.execute(text("DROP TEMPORARY TABLE IF EXISTS date_range;"))

            # 一時テーブルの作成。sqlalchemyのテーブルでなければcase文で使えない。
            await session.execute(
                text(f"CREATE TEMPORARY TABLE date_range (day DATE);")
            )

            # 日付範囲を一時テーブルに挿入
            await session.execute(
                text(f"INSERT INTO date_range (day) VALUES {date_values};")
            )

            # メインクエリ
            query = (
                select(
                    date_range_table.c.day,
                    case(
                        (func.max(OrmExerciseDone.done) == 1, True), else_=False
                    ).label("exerciseDone"),
                )
                .select_from(date_range_table)
                .outerjoin(
                    OrmExerciseDone,
                    and_(
                        OrmExerciseDone.user_id == uid,
                        OrmExerciseDone.date == date_range_table.c.day,
                    ),
                )
                .group_by(date_range_table.c.day)
                .order_by(date_range_table.c.day)
            )

            # クエリの実行
            result = await session.execute(query)
            result = result.fetchall()  # ここで全行を取得し、リストとして扱う

            # 一時テーブルを削除
            await session.execute(text("DROP TEMPORARY TABLE IF EXISTS date_range;"))

            # クエリ結果を辞書形式で変換
            result_dict = {row[0]: row[1] for row in result}

            # DDDで扱うentityに変換
            exercises_this_month = [
                CalendarResponse(a_date=day, a_exerciseDone=bool(exercise_done))
                for day, exercise_done in result_dict.items()
            ]

        return exercises_this_month
