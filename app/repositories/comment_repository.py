from datetime import datetime, timezone

from sqlalchemy import select

from app.models.comment import Comment
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(
        self,
        content: str,
        post_id: int,
        created_by: int,
    ) -> Comment:
        comment = Comment(content=content, post_id=post_id, created_by=created_by)
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def get_by_id(self, comment_id: int) -> None | Comment:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.id == comment_id)
            .where(Comment.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_post(
        self,
        post_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Comment]:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.post_id == post_id)
            .where(Comment.deleted_at.is_(None))
            .order_by(Comment.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, comment: Comment, content: str, updated_by: int) -> Comment:
        comment.content = content
        comment.updated_by = updated_by
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def self_delete(self, comment: Comment, deleted_by: int) -> None:
        comment.deleted_at = datetime.now(timezone.utc)
        comment.updated_by = deleted_by
        await self.session.flush()
