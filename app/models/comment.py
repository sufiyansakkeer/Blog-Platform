from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import SoftDeleteMixin, TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Post, User


class Comment(Base, TimeStampMixin, SoftDeleteMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",  # there should be a field called 'comments' in the 'Post' model
        lazy="noload",
    )

    author: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        lazy="noload",
        # We don't put back tracking because we don't need comments in the user model.
    )
    editor: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[
            updated_by
        ],  # here also we don't need that relation with the user
        lazy="noload",
    )
