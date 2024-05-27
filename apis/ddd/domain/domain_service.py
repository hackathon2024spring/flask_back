from fastapi import HTTPException, status
from pydantic import EmailStr
from ddd.domain.value_object import Password, SessionID
from ddd.domain.repository import UserRepository
from ddd.infrastructure.orms.user import User as OrmUser
from ddd.infrastructure.redis.repository import RedisRipository


class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    async def get_authorized_id(self, email: EmailStr, password: Password):
        # registered_userが帰ってこない=既にHttpExceptionが発生している
        registered_user: OrmUser = await self.userRepository.get_user_by_email(
            email=email
        )
        if password.verify_password(registered_user.password):
            return registered_user.uid
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emailアドレス・パスワードに問題があります。",
            )


class SessionService:
    def __init__(self, redis_repository: RedisRipository):
        self.redis_repository = redis_repository

    async def get_csrf_token(self, session_id: SessionID) -> str:
        return await self.redis_repository.get(str(session_id))

    async def set_csrf_token(
        self, session_id: SessionID, csrf_token: str, expire: int = 3600
    ):
        await self.redis_repository.set(str(session_id), csrf_token, expire)

    async def delete_csrf_token(self, session_id: SessionID):
        await self.redis_repository.delete(str(session_id))
