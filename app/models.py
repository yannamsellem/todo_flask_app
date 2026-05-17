from datetime import datetime, UTC
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    
    todos: Mapped[List["Todo"]] = relationship("Todo", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Todo(db.Model):
    __tablename__ = 'todos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    
    author: Mapped["User"] = relationship("User", back_populates="todos")

    def __repr__(self) -> str:
        return f'<Todo {self.title}>'
