from sqlalchemy import Column, Text, String

from core.models.base import Base


class Post(Base):
    __tablename__ = "posts"

    title = Column(String(50), nullable=False)
    description = Column(Text)
