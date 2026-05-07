from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.services.comment_service import CommentService

router = APIRouter(prefix="/posts", tags=["Comments"])


def get_comment_service(session: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(
        comment_repository=CommentRepository(session=session),
        post_repository=PostRepository(session=session),
    )


@router.post(
    "/{post_id}/comments",
    response_model=CommentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    post_id: int,
    data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
) -> CommentRead:
    try:
        return await service.create_comment(
            post_id=post_id, data=data, current_user=current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get(
    "/{post_id}/comments",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_post_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 20,
    service: CommentService = Depends(get_comment_service),
) -> list[CommentRead]:
    try:
        return await service.get_comments_for_post(
            post_id=post_id,
            skip=skip,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/comments/{comment_id}",
    response_model=CommentRead,
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
) -> CommentRead:
    try:
        return await service.update_comment(
            comment_id=comment_id,
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


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        return await service.delete_comment(
            comment_id=comment_id, current_user=current_user
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
