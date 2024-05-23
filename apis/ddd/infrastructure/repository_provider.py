import os
from ddd.infrastructure.mysql.repository import (
    UserRepositoryImpl as MySQLUserRepository,
)
from ddd.infrastructure.sqlite.repository import (
    UserRepositoryImpl as SQLiteUserRepository,
)


def get_user_repository():
    environment = os.getenv("IS_TEST")
    if environment == "True":
        return SQLiteUserRepository.get_instance()
    else:
        return MySQLUserRepository.get_instance()
