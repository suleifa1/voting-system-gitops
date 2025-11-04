# filepath: /Users/fedorauser/Desktop/bakalarka/poll_app/voting-system-gitops/src/backend/alembic/env.py
from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Добавляем путь к src для импорта моделей
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Импортируем модели
from src.database.connection import Base
from src.models.user import User

config = context.config

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