from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.polls import router as polls_router  
from src.api.admin import router as admin_router
from src.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Application startup")
    # Таблицы уже созданы через Alembic, ничего не делаем
    yield
    # Shutdown  
    print("🛑 Application shutdown")

app = FastAPI(
    title="Poll App API",
    description="Voting System API",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(polls_router, prefix="/polls", tags=["polls"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Poll App API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}