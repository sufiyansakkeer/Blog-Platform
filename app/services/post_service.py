from app.models.user import User
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostRead, PostUpdate


class PostService:
    def __init__(self, post_repository: PostRepository) -> None:
        self.post_repository = post_repository

    async def create_post(self, data: PostCreate, current_user: User) -> PostRead:
        post = await self.post_repository.create(
            title=data.title, content=data.content, created_by=current_user.id
        )
        return PostRead.model_validate(post)

    async def get_post(self, post_id: int) -> PostRead:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        return PostRead.model_validate(post)

    async def get_all_post(self, skip: int = 0, limit: int = 10) -> list[PostRead]:
        posts = await self.post_repository.get_all(skip=skip, limit=limit)
        return [PostRead.model_validate(post) for post in posts]

    async def update_post(
        self, post_id: int, data: PostUpdate, current_user: User
    ) -> PostRead:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        if post.created_by != current_user.id and not current_user.is_admin:
            raise ValueError("You are not allowed to update this post")

        updated_post = await self.post_repository.update(
            post=post,
            title=data.title,
            content=data.content,
            updated_by=current_user.id,
        )
        return PostRead.model_validate(updated_post)

    async def delete_post(self, post_id: int, current_user: User) -> None:
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise ValueError("Post not found")

        if post.created_by != current_user.id and not current_user.is_admin:
            raise ValueError("You are not allowed to delete this post")

        await self.post_repository.soft_delete(post, deleted_by=current_user.id)
