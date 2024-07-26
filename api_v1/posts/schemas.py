from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api_v1.commentaries.schemas import Commentary


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    is_auto_response: bool = False
    response_threshold_in_seconds: int | None = None


class PostUpdate(PostBase):
    pass


class PostUpdatePartial(PostBase):
    title: str | None = None
    description: str | None = None


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    timestamp: datetime
    is_auto_response: bool = False
    response_threshold_in_seconds: int | None = None


class PostDetail(Post):
    commentaries: list[Commentary]
