from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.repositories.base import BaseRepository


class PostRepository(BaseRepository):
    """Provides async data access operations for blog posts.
    This repository encapsulates common CRUD-style operations for the Post model.
    Args:
        session: Async database session used to perform queries and persistence.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, title: str, content: str, created_by: int) -> Post:
        post = Post(title=title, content=content, created_by=created_by)
        self.session.add(post)
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def get_by_id(self, post_id: int) -> Post | None:
        result = await self.session.execute(
            select(Post).where(Post.id == post_id).where(Post.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[Post]:
        result = await self.session.execute(
            select(Post)
            .where(Post.deleted_at.is_(None))
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(
        self, post: Post, title: str | None, content: str | None, updated_by: int
    ) -> Post:
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        post.updated_by = updated_by
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def soft_delete(self, post: Post, deleted_by: int) -> None:
        post.deleted_at = datetime.now(timezone.utc)
        post.updated_by = deleted_by
        await self.session.flush()
