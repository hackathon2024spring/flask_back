from abc import ABC, abstractmethod
from typing import List
from datetime import date
from pydantic import EmailStr
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from ddd.domain.entity import (
    CalendarRequest,
    RegisteredUser,
    User as DomainUser,
    Exercise as DomainExercise,
    ExerciseSelectedRequest as DomainExerciseSelectedRequest,
    ExerciseDoneRequest as DomainExerciseDoneRequest,
    ExerciseDoneResponse as DomainExerciseDoneResponse,
)


class UserRepository(ABC):

    @abstractmethod
    def get_database_url(self) -> str:
        pass

    @abstractmethod
    def get_engine(self) -> Engine:
        pass

    @abstractmethod
    def get_session(self) -> Session:
        pass

    @abstractmethod
    async def session_scope(self):
        pass

    @abstractmethod
    async def register_user(self, user: DomainUser) -> RegisteredUser:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr):
        pass

    @abstractmethod
    async def get_user_by_uid(self, uid: str):
        pass

    @abstractmethod
    async def get_exercises(self) -> List[DomainExercise]:
        pass

    @abstractmethod
    async def add_exercises_selected(
        self, exercises_selected: List[DomainExerciseSelectedRequest]
    ):
        pass

    @abstractmethod
    async def upsert_exercises_selected(
        self, exercises_selected: list[DomainExerciseSelectedRequest]
    ):
        pass

    @abstractmethod
    async def upsert_exercises_selected(
        self, exercises_selected: list[DomainExerciseSelectedRequest]
    ):
        pass

    @abstractmethod
    async def get_exercises_selected(self, uid: str):
        pass

    @abstractmethod
    async def upsert_exercises_done(
        self, exercises_done: list[DomainExerciseDoneRequest]
    ):
        pass

    @abstractmethod
    async def get_exercises_done(
        self, uid: str, date: date
    ) -> List[DomainExerciseDoneResponse]:
        pass

    @abstractmethod
    async def get_exercises_this_month(self, uid: str, calendar: CalendarRequest):
        pass
