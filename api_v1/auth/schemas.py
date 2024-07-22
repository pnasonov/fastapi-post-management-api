from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str


class CreateUser(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
