from fastapi import HTTPException, status
from pydantic import EmailStr
from ddd.domain.value_object import Password
from ddd.domain.repository import UserRepository
from ddd.infrastructure.orms.user import User as OrmUser


class UserService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    async def get_authorized_id(self, email: EmailStr, password: Password):
        # registered_userが帰ってこない=既にHttpExceptionが発生している
        registered_user: OrmUser = await self.userRepository.get_user_by_email(email=email)
        if password.verify_password(registered_user.password):
            return registered_user.uid
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emailアドレス・パスワードに問題があります。",
            )
