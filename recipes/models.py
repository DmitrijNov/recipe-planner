from typing import TYPE_CHECKING
from uuid import UUID, uuid7

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from users.models import User


class Recipe(Base):
    __tablename__ = "recipe"

    uuid: Mapped[UUID] = mapped_column(Uuid, default=uuid7, primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    author_id: Mapped[id] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="recipes")
