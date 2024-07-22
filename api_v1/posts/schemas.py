from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentaryBase(BaseModel):
    text: str
    timestamp: datetime


class Commentary(CommentaryBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    text: str
    timestamp: datetime


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    user_id: int


class PostUpdate(PostBase):
    pass


class PostUpdatePartial(PostBase):
    title: str | None = None
    description: str | None = None


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class PostDetail(Post):
    commentaries: list[Commentary]
