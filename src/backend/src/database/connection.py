from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Базовые параметры подключения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "26257")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "poll_app")

# URL для asyncpg (без JSON кодеков для CockroachDB)
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# URL для psycopg2 (с sslmode для Alembic)
SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"

# Асинхронный движок для приложения (отключаем JSON кодеки)
engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=True,
    connect_args={
        "server_settings": {
            "jit": "off",
        }
    }
)

# Синхронный движок для Alembic
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Создаем сессию
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Dependency для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()