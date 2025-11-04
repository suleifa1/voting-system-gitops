from .connection import engine, get_db, Base

# Убираем создание таблиц при startup - используем Alembic!
async def create_tables():
    """Таблицы создаются через Alembic миграции"""
    pass  # Ничего не делаем - таблицы уже созданы через миграции