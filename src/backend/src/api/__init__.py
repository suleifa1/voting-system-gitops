from fastapi import APIRouter

# Импортируем роутеры
from .polls import router as polls_router
from .auth import router as auth_router  
from .admin import router as admin_router

# Создаем главный API роутер
api_router = APIRouter(prefix="/api/v1")

# Подключаем все роутеры
api_router.include_router(polls_router, prefix="/polls", tags=["polls"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])