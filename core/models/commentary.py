from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base
from core.models.mixins import UserRelationMixin


if TYPE_CHECKING:
    from core.models.post import Post


class Commentary(UserRelationMixin, Base):
    __tablename__ = "commentaries"

    _user_back_populates = "commentaries"

    text: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_offensive: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=None,
        nullable=True,
    )

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="commentaries")
