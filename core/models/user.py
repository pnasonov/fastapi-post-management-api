from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.post import Post
    from core.models.commentary import Commentary


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
    commentaries: Mapped[list["Commentary"]] = relationship(
        back_populates="user", cascade="all, delete"
    )
