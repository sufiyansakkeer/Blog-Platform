from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    content: str


class PostUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    content: str | None = None


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_by: int
    updated_by: int | None
    created_at: datetime
    updated_at: datetime
