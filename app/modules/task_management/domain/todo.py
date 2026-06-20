from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional, Protocol

from app.shared.domain.entities import Entity


@dataclass
class Todo(Entity):
    title: str = ""
    description: Optional[str] = None
    completed: bool = False
    user_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    author: Optional[Any] = None


class TodoRepository(Protocol):
    def get_by_id(
        self, todo_id: int, extend: Optional[str] = None
    ) -> Optional[Todo]: ...

    def list_by_user(
        self,
        user_id: int,
        completed: Optional[bool] = None,
        extend: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[Todo]: ...

    def save(self, todo: Todo) -> Todo: ...

    def delete(self, todo_id: int) -> None: ...
