import os
import secrets
from typing import List, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from pydantic import EmailStr
from datetime import date, datetime, timedelta, timezone
from ddd.infrastructure.orms.user import User as OrmUser
from ddd.domain.value_object import Password
from ddd.domain.repository import UserRepository
from ddd.domain.domain_service import UserService
from ddd.domain.entity import (
    CalendarRequest,
    User as DomainUser,
    ExerciseSelected as DomainExerciseSelected,
    ExerciseSelectedRequest as DomainExerciseSelectedRequest,
    ExerciseDone as DomainExerciseDone,
    ExerciseDoneRequest as DomainExerciseDoneRequest,
)
from ddd.infrastructure.redis.repository import RedisRipository

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 720


class UseCase:
    # loginはtokenが発生していない状態でusecaseにアクセスするので、Optionalにしている。
    def __init__(self, userRepository: UserRepository, token: Optional[str] = None):
        self.userRepository = userRepository
        self.redisRepository = RedisRipository()
        self.userService = UserService(userRepository=userRepository)
        self.token = token

    async def get_exercises_in_calendar(self, calendar: CalendarRequest):
        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # 現在のexercisesで更新しつつ、uidのexercises_doneを抽出
        exercises_calendar = (
            await self.userRepository.get_exercises_this_month(
                uid=uid, calendar=calendar
            )
        ) or []

        return exercises_calendar

    # dateに実施したexercisesを取得
    async def get_user_exercises_done(self, date: date):
        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # 現在のexercisesで更新しつつ、uidのexercises_doneを抽出
        exercises_done = (
            await self.userRepository.get_exercises_done(uid=uid, date=date)
        ) or []

        return exercises_done

    async def update_user_exercises_done(
        self, date: date, exercises_done: list[DomainExerciseDone]
    ):
        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # uid・date・ExerciseDoneを組み合わせる
        exercises_done_request = [
            DomainExerciseDoneRequest(
                a_id=exe.id(), a_done=exe.done(), a_user_id=uid, a_date=date
            )
            for exe in exercises_done
        ]

        # dateに実施したexerciseを追加・更新
        is_success = await self.userRepository.upsert_exercises_done(
            exercises_done_request
        )

        if is_success:
            return is_success
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    # 登録中の実施候補のexercisesを取得
    async def get_user_exercises_selected(self):

        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # 現在のexercisesで更新しつつ、uidのexercises_selectedを抽出
        exercises_selected = (
            await self.userRepository.get_exercises_selected(uid=uid)
        ) or []

        return exercises_selected

    # 実施候補のexercisesを登録、更新
    async def update_user_exercises_selected(
        self, exercises_selected: List[DomainExerciseSelected]
    ):
        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        exercises_selected_request = [
            DomainExerciseSelectedRequest(
                a_id=exe.id(), a_user_id=uid, a_selected=exe.selected()
            )
            for exe in exercises_selected
        ]

        is_success = await self.userRepository.upsert_exercises_selected(
            exercises_selected_request
        )
        if is_success:
            return is_success
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    # ユーザーアカウントの作成とexercisesの初期リストを生成
    async def create_user_account(self, user: DomainUser):
        # registed_userが返ってこない=既にHttpExceptionが発生している。
        registered_user = await self.userRepository.register_user(user=user)

        # 選択可能のexercisesを全て取得
        exercises = await self.userRepository.get_exercises()

        # 登録したユーザーidで初期ExercisesSelectを作る。
        exercises_selected = [
            DomainExerciseSelectedRequest(
                a_id=exe.id(), a_user_id=registered_user.id(), a_selected=True
            )
            for exe in exercises
        ]

        # ExercisesSelectを保存
        await self.userRepository.add_exercises_selected(
            exercises_selected=exercises_selected
        )

        # try-exceptで呼び出されているので、usecaseでエラーキャッチしない。
        return registered_user

    # サーバーサイドでcookieを生成し、JSONResponseで返す。
    async def set_cookie(self, email: EmailStr, password: Password) -> JSONResponse:

        # authorized_idが返ってこない=既にHttpExceptionが発生している
        authorized_id = await self.userService.get_authorized_id(
            email=email, password=password
        )

        # tokenの有効期限設定
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # token生成
        access_token = self.create_access_token(
            data={"sub": authorized_id},
            expires_delta=access_token_expires,
        )

        csrf_token = secrets.token_urlsafe(32)
        await self.redisRepository.set(
            key=authorized_id, value=csrf_token, expire=access_token_expires
        )

        # cookieをサーバーから操作するresponse生成
        json_response = JSONResponse(content={"token_type": "bearer"})

        is_https = os.getenv("IS_HTTPS")
        if is_https == "True":
            mode = True
        else:
            mode = False

        # cookieに必要な情報を付与
        json_response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Strict",
            secure=mode,  # 本番環境ではHTTPSが前提のためTrue。それ以外はFalse
            # domain=".local.dev",
        )

        json_response.set_cookie(
            key="session_id",
            value=csrf_token,
            httponly=True,
            samesite="Strict",
            secure=mode,  # 本番環境ではHTTPSが前提のためTrue。それ以外はFalse
        )

        return json_response

    # cookie削除
    async def remove_cookie(self):

        # jwtとcsrf_tokenを取得
        jw_token, csrf_token = self.token.values()

        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # login_userが返ってこない=既にHttpExceptionが発生している
        login_user = await self.userRepository.get_user_by_uid(uid=uid)

        # store_tokenが返ってこない=既にHttpExceptionが発生している。
        store_token = await self.get_csrf_token(uid=uid)

        # jw_tokenに紐ついたuserとcsrf_tokenが一致
        if login_user and (csrf_token == store_token):
            #
            await self.redisRepository.delete(key=uid)
            # cookieをサーバーから操作するresponse生成
            json_response = JSONResponse(
                content={
                    "token_type": "bearer",
                    "message": "Successfully logged out",
                }
            )

            # value=""のcookieをセットする。つまりcookieを外す。
            json_response.set_cookie(
                key="access_token",
                value="",
                httponly=True,
                samesite="Strict",
                secure=False,  # 本番環境ではHTTPSが前提のためTrueに設定
                max_age=0,
                # domain=".local.dev",
            )
            json_response.set_cookie(
                key="session_id",
                value="",
                httponly=False,
                samesite="Strict",
                secure=False,  # 本番環境ではHTTPSが前提のためTrueに設定
                max_age=0,
                # domain=".local.dev",
            )

            # cookieのないresponseを返す。
            return json_response

    # JWTでcookie生成
    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()

        # expire_deltaが指定されていなければ15分に設定
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        # tokenの寿命設定
        to_encode.update({"exp": expire})

        # JWTを生成する。
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # cookieのjwtとcsrf_tokenを判定し、uidを抽出する。
    async def get_user_id(self) -> str:

        # tokenがある場合のみ
        if self.token != None:

            # 格納しているtokenをjwtとcsrftokenに分ける
            jw_token, csrf_token = self.token.values()

            try:
                # jwtを解読
                payload = jwt.decode(jw_token, SECRET_KEY, algorithms=[ALGORITHM])
                uid: str = payload.get("sub")

                # store_tokenが返ってこない=既にHttpExceptionが発生している。
                store_token = await self.get_csrf_token(uid=uid)

                # csrf_tokenが一致しない=cookieに不正あり
                if csrf_token != store_token:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="不適切なcookieです。",
                    )

                return uid

            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="不適切なcookieです。",
                )

    # uidとセットとなっているsession_idをredisから取得
    async def get_csrf_token(self, uid: str) -> str:
        csrf_token = await self.redisRepository.get(key=uid)

        if csrf_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="不適切なcookieです。",
            )
        return csrf_token

    # cookieからログイン中のユーザーを取得
    async def get_login_user(self):
        # uidが返ってこない=既にJWTErrorが発生している。
        uid = await self.get_user_id()

        # login_userが返ってこない=既にHttpExceptionが発生している
        login_user: OrmUser = await self.userRepository.get_user_by_uid(uid=uid)
        return login_user
