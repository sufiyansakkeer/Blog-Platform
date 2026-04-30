
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User


__all__ = ["User", "Post","Comment"]

# this helps the alembic to detect all models