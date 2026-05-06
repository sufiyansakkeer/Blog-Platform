from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate
from app.schemas.user import UserLogin, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(user_repository=UserRepository(session))


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> UserRead:
    try:
        return await service.register(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post("/login", response_model=dict)
async def login(
    data: UserLogin, service: AuthService = Depends(get_auth_service)
) -> dict[str, Any]:
    try:
        return await service.login(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
