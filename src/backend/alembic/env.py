# filepath: /Users/fedorauser/Desktop/bakalarka/poll_app/voting-system-gitops/src/backend/alembic/env.py
from logging.config import fileConfig
import sys
import os
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Добавляем путь к src для импорта моделей
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Импортируем модели
from src.database.connection import Base
from src.models.user import User
from src.models.poll import Survey, Question, QuestionOption, Answer

config = context.config

# Читаем DATABASE_URL из переменных окружения если доступен
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "26257")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME", "poll_app")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"

# Переопределяем sqlalchemy.url из переменных окружения
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # Monkey patch для CockroachDB
    import sqlalchemy.dialects.postgresql.base as pg_base
    original_get_server_version_info = pg_base.PGDialect._get_server_version_info
    
    def _get_server_version_info(self, connection):
        try:
            return original_get_server_version_info(self, connection)
        except AssertionError:
            # Если CockroachDB, возвращаем fake версию PostgreSQL
            return (13, 0)
    
    pg_base.PGDialect._get_server_version_info = _get_server_version_info

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()