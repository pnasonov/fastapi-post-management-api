from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from core.models.base import Base


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(
        Text, nullable=True, default="", server_default=""
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
