from app.models.user import User
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate


class CommentService:
    def __init__(
        self, comment_repository: CommentRepository, post_repository: PostRepository
    ) -> None:
        self.comment_repository = comment_repository
        self.post_repository = post_repository

    async def create_comment(
        self, post_id: int, data: CommentCreate, current_user: User
    ) -> CommentRead:
        post = await self.post_repository.get_by_id(post_id=post_id)
        if not post:
            raise ValueError("Post not found")
        comment = await self.comment_repository.create(
            content=data.content, post_id=post_id, created_by=current_user.id
        )
        return CommentRead.model_validate(comment)

    async def get_comments_for_post(
        self, post_id: int, skip: int = 0, limit: int = 20
    ) -> list[CommentRead]:
        post = await self.post_repository.get_by_id(post_id=post_id)
        if not post:
            raise ValueError("Post not found")

        comments = await self.comment_repository.get_by_post(
            post_id=post_id, skip=skip, limit=limit
        )
        return [CommentRead.model_validate(comment) for comment in comments]

    async def delete_comment(self, comment_id: int, current_user: User) -> None:
        comment = await self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.created_by != current_user.id and not current_user.is_admin:
            raise ValueError("You are not allowed to delete this comment")
        await self.comment_repository.self_delete(comment, deleted_by=current_user.id)

    async def update_comment(
        self, comment_id: int, data: CommentUpdate, current_user: User
    ) -> CommentRead:
        comment = await self.comment_repository.get_by_id(comment_id=comment_id)
        if not comment:
            raise ValueError("Comment not found")

        if comment.created_by != current_user.id and not current_user.is_admin:
            raise ValueError("You are not allowed to update this comment")

        updated_comment = await self.comment_repository.update(
            comment=comment,
            content=data.content,
            updated_by=current_user.id,
        )
        return CommentRead.model_validate(updated_comment)
