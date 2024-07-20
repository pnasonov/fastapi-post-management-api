from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base
from core.models.mixins import UserRelationMixin

if TYPE_CHECKING:
    from core.models.commentary import Commentary


class Post(UserRelationMixin, Base):
    __tablename__ = "posts"

    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, nullable=True, default="", server_default=""
    )
    commentaries: Mapped[list["Commentary"]] = relationship(
        back_populates="post",
    )
