from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User

from src.database.connection import get_db
from src.database.models import get_user, register_user, authenticate_user
from src.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from src.auth.security import (
    create_user_token,
    verify_token
)

router = APIRouter()
security = HTTPBearer()

async def get_current_user(token: str = Depends(security), db: AsyncSession = Depends(get_db)):
    """Получаем текущего пользователя по JWT токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = verify_token(token.credentials)
    if user_id is None:
        raise credentials_exception
    
    user = await get_user(user_id=user_id, db=db)
    
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрация нового пользователя"""
    
    # Проверяем, существует ли пользователь с таким email
    result = await register_user(user_data, db)
    if result.get("error") == -7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    elif result.get("error") == -6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    elif result.get("error") == -1:  # Добавьте эту обработку
        raise HTTPException(status_code=500, detail="Database error occurred")
    elif result.get("error") == 0:
        db_user_id = result.get("user")

    if db_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User registration failed"
        )

    # Создаем токен
    access_token = create_user_token(db_user_id)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):    
    result = await authenticate_user(user_credentials, db)
    if result.get("error") == -8:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif result.get("error") != 0:  # Обрабатываем любые другие ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server-side authentication failed"
        )
    elif result.get("error") == 0:
        user_id = result.get("user")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )
    # Создаем токен
    access_token = create_user_token(user_id)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify")
async def verify_current_user(current_user: User = Depends(get_current_user)):
    """Проверка токена и получение информации о пользователе"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "is_admin": current_user.is_admin
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Получение профиля текущего пользователя"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at.isoformat()
    )