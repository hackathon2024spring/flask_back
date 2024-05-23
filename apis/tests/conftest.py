import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ddd.infrastructure.orms.user import Base
from ddd.infrastructure.sqlite.repository import UserRepositoryImpl

TEST_DATABASE_URL = UserRepositoryImpl().get_database_url()
engine = create_async_engine(TEST_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# 初期データを挿入する関数
async def insert_initial_data(session):
    insert_query = """
        INSERT INTO exercises (id, exercise_name)
        VALUES 
            (1, '階段を使う'),
            (2, '散歩する'),
            (3, 'ストレッチをする'),
            (4, '足踏み運動をする'),
            (5, '一駅分歩く'),
            (6, 'ラジオ体操をする');
    """
    await session.execute(text(insert_query))
    await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # セッションを作成して初期データを挿入
    async with AsyncSessionLocal() as session:
        await insert_initial_data(session)

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()  # エンジンを明示的にクローズ


@pytest.fixture(scope="function")
async def session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()  # セッションを明示的にクローズ
