from typing import Any

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserRead


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, data: UserCreate) -> UserRead:
        existing_email = await self.user_repository.get_by_email(data.email)
        if existing_email:
            raise ValueError("Email already registered")

        existing_username = await self.user_repository.get_by_username(data.username)
        if existing_username:
            raise ValueError("Username already taken")

        hashed = hash_password(data.password)
        user = await self.user_repository.create(
            username=data.username, email=data.email, hashed_password=hashed
        )
        return UserRead.model_validate(user)

    async def login(self, data: UserLogin) -> dict[str, Any]:
        user = await self.user_repository.get_by_email(data.email)
        if not user:
            raise ValueError("Invalid credentials")

        is_valid_password = verify_password(data.password, user.hashed_password)
        if not is_valid_password:
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User account is inactive")

        token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
