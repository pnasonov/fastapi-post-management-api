from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    description: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostCreate):
    pass


class PostUpdatePartial(PostCreate):
    title: str | None = None
    description: str | None = None


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
