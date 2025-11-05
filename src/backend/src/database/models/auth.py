from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from sqlalchemy import select
from src.schemas.auth import UserCreate, UserLogin, UserResponse, Token


from src.auth.security import (
    verify_password, 
    get_password_hash, 
)

async def get_user( user_id: int, db: AsyncSession  ):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user

async def register_user(user_data: UserCreate, db: AsyncSession):
    """Регистрация нового пользователя"""
    
    try:
        # Проверяем, существует ли пользователь с таким email
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            return {"error": -6, "message": "Email already registered"}
        
        # Проверяем, существует ли пользователь с таким username
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            return {"error": -7, "message": "Username already taken"}

        # Создаем нового пользователя
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"error": 0, "message": "User registered successfully", "user": db_user.id}
    
    except Exception as e:
        await db.rollback()
        return {"error": -1, "message": f"Database error: {str(e)}"}

async def authenticate_user(user_credentials: UserLogin, db: AsyncSession):
    try:
        result = await db.execute(select(User).where(User.email == user_credentials.email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(user_credentials.password, user.hashed_password):
            return {"error": -8, "message": "Incorrect email or password"}
        
        return {"error": 0, "message": "Authentication successful", "user": user.id}
    
    except Exception as e:
        return {"error": -1, "message": f"Database error: {str(e)}"}