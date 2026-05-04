from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import SoftDeleteMixin, TimeStampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User, Comment


class Post(Base, TimeStampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    author: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="posts",  # there should be a field called 'posts' in the 'User' Model
        lazy="noload",
    )

    editor: Mapped["User | None"] = relationship(
        "User", foreign_keys=[updated_by], lazy="noload"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",  # there should be a field called 'post' in the 'Comment' model
        cascade="all, delete-orphan",
        lazy="noload",
    )
