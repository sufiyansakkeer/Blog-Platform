import pytest
from httpx import AsyncClient

from app.models.user import User
from tests.factories import UserFactory


@pytest.mark.asyncio
async def test_register_success(test_client: AsyncClient) -> None:
    """Test successful user registration."""
    user_data = UserFactory.create_user_data(
        username="newuser",
        email="newuser@example.com",
        password="SecurePass123!"
    )
    
    response = await test_client.post("/auth/register", json=user_data.model_dump())
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["is_active"] is True
    assert data["is_admin"] is False
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_username(test_client: AsyncClient, test_user: User) -> None:
    """Test registration with duplicate username."""
    user_data = UserFactory.create_user_data(
        username=test_user.username,
        email="different@example.com",
        password="SecurePass123!"
    )
    
    response = await test_client.post("/auth/register", json=user_data.model_dump())
    
    assert response.status_code == 400
    assert "username" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_duplicate_email(test_client: AsyncClient, test_user: User) -> None:
    """Test registration with duplicate email."""
    user_data = UserFactory.create_user_data(
        username="differentuser",
        email=test_user.email,
        password="SecurePass123!"
    )
    
    response = await test_client.post("/auth/register", json=user_data.model_dump())
    
    assert response.status_code == 400
    assert "email" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email(test_client: AsyncClient) -> None:
    """Test registration with invalid email format."""
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "SecurePass123!"
    }
    
    response = await test_client.post("/auth/register", json=user_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(test_client: AsyncClient, test_user: User) -> None:
    """Test successful user login."""
    login_data = UserFactory.create_login_data(
        email=test_user.email,
        password="TestPassword123!"
    )
    
    response = await test_client.post("/auth/login", json=login_data.model_dump())
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_email(test_client: AsyncClient) -> None:
    """Test login with non-existent email."""
    login_data = UserFactory.create_login_data(
        email="nonexistent@example.com",
        password="SomePassword123!"
    )
    
    response = await test_client.post("/auth/login", json=login_data.model_dump())
    
    assert response.status_code == 400
    assert "WWW-Authenticate" in response.headers


@pytest.mark.asyncio
async def test_login_invalid_password(test_client: AsyncClient, test_user: User) -> None:
    """Test login with incorrect password."""
    login_data = UserFactory.create_login_data(
        email=test_user.email,
        password="WrongPassword123!"
    )
    
    response = await test_client.post("/auth/login", json=login_data.model_dump())
    
    assert response.status_code == 400
    assert "WWW-Authenticate" in response.headers


@pytest.mark.asyncio
async def test_login_missing_fields(test_client: AsyncClient) -> None:
    """Test login with missing required fields."""
    response = await test_client.post("/auth/login", json={"email": "test@example.com"})
    
    assert response.status_code == 422
