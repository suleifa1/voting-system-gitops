from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.api.polls import router as polls_router  
from src.api.admin import router as admin_router
from src.api.surveys import router as surveys_router
from src.database import create_tables

# CI/CD Pipeline Test - Auto-promote to staging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Application startup")
    # Таблицы уже созданы через Alembic, ничего не делаем
    yield
    # Shutdown  
    print("🛑 Application shutdown")

# Create main app without prefix
main_app = FastAPI(
    title="Poll App API",
    description="Voting System API",
    version="1.0.0",
    lifespan=lifespan
)

# Добавляем CORS middleware
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Ingress
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

# Подключаем роутеры к API router
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(polls_router, prefix="/polls", tags=["polls"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(surveys_router)

@api_router.get("/")
async def api_root():
    return {"message": "Poll App API is running!"}

@api_router.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test"""
    from src.database.connection import get_db
    from sqlalchemy import text
    
    db_status = "unknown"
    try:
        db = next(get_db())
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status
    }

# Mount API router to main app
main_app.include_router(api_router)

# Alias for uvicorn
app = main_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)