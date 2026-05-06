from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_post_service(
    session: AsyncSession = Depends(get_db),
) -> PostService:
    return PostService(post_repository=PostRepository(session=session))


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostCreate,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
) -> PostRead:
    return await service.create_post(data=data, current_user=current_user)


@router.get("", response_model=list[PostRead])
async def get_all_post(
    skip: int = 0,
    limit: int = 10,
    service: PostService = Depends(get_post_service),
) -> list[PostRead]:
    return await service.get_all_post(
        skip=skip,
        limit=limit,
    )


@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id(
    post_id: int, service: PostService = Depends(get_post_service)
) -> PostRead:
    try:
        return await service.get_post(post_id=post_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    data: PostUpdate,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
) -> PostRead:
    try:
        return await service.update_post(
            post_id=post_id,
            data=data,
            current_user=current_user,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        return await service.delete_post(post_id, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
