from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "26257")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "poll_app")

# URL для psycopg2 async (поддерживается CockroachDB)
ASYNC_DATABASE_URL = f"postgresql+psycopg://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# URL для psycopg2 (с sslmode для Alembic)
SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"


import sqlalchemy.dialects.postgresql.base as pg_base
original_get_server_version_info = pg_base.PGDialect._get_server_version_info

def _get_server_version_info(self, connection):
    try:
        return original_get_server_version_info(self, connection)
    except AssertionError:
        return (13, 0)

pg_base.PGDialect._get_server_version_info = _get_server_version_info

engine = create_async_engine(
    ASYNC_DATABASE_URL, 
    echo=True
)

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()