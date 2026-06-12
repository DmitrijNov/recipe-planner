import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from recipes.models import Recipe


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    group_id: Mapped[int] = mapped_column(ForeignKey("user_groups.id"), nullable=True)
    group: Mapped["UserGroup"] = relationship("UserGroup", back_populates="users")
    recipes: Mapped[list["Recipe"]] = relationship("Recipe")


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="group")
