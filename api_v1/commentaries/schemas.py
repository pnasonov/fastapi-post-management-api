from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentaryBase(BaseModel):
    text: str


class CommentaryCreate(CommentaryBase):
    pass


class Commentary(CommentaryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    user_id: int
    post_id: int
