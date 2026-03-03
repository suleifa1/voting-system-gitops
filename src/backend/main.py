from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.api.polls import router as polls_router  
from src.api.admin import router as admin_router
from src.api.surveys import router as surveys_router
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
    lifespan=lifespan,
    root_path="/api"  # Add root path for reverse proxy
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(polls_router, prefix="/polls", tags=["polls"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(surveys_router)

@app.get("/")
async def root():
    return {"message": "Poll App API is running!"}

@app.get("/health")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)