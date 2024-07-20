from typing import TYPE_CHECKING

from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.user import User


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, nullable=True, default="", server_default=""
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates="posts")
