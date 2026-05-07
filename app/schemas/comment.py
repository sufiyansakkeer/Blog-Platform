from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str


class CommentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    post_id: int
    created_by: int
    updated_by: int | None
    created_at: datetime
    updated_at: datetime
