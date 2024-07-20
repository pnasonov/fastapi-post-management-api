from sqlalchemy import Column, String

from core.models.base import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(32), unique=True, nullable=False)
