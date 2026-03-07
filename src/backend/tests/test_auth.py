"""
Integration tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    }
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email"""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password123"
    }
    
    # First registration
    response1 = await client.post("/auth/register", json=user_data)
    assert response1.status_code == 200
    
    # Second registration with same email
    user_data["username"] = "user2"
    response2 = await client.post("/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login"""
    # Register first
    register_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "password123"
    }
    await client.post("/auth/register", json=register_data)
    
    # Login
    login_data = {
        "email": "login@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password"""
    # Register first
    register_data = {
        "email": "wrongpass@example.com",
        "username": "wrongpassuser",
        "password": "correctpassword"
    }
    await client.post("/auth/register", json=register_data)
    
    # Login with wrong password
    login_data = {
        "email": "wrongpass@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_verify_token(authenticated_client: AsyncClient):
    """Test token verification"""
    response = await authenticated_client.get("/auth/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert "user" in data

@pytest.mark.asyncio
async def test_get_current_user(authenticated_client: AsyncClient):
    """Test getting current user profile"""
    response = await authenticated_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
