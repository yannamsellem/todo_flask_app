from datetime import UTC, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.infrastructure.database import Base

if TYPE_CHECKING:
    from app.modules.task_management.infrastructure.models import TodoModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64), index=True, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(120), index=True, unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    # Use string reference for TodoModel to avoid circular import
    todos: Mapped[List["TodoModel"]] = relationship(
        "TodoModel", back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<UserModel {self.username}>"
