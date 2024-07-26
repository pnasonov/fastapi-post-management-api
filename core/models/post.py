import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, String, Boolean, DateTime
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
    timestamp: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(),
        nullable=True,
    )
    commentaries: Mapped[list["Commentary"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    is_offensive: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=None,
        nullable=True,
    )
