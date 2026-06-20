from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional, Protocol

from app.modules.task_management.domain.todo import Todo
from app.shared.domain.entities import Entity


@dataclass
class User(Entity):
    username: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None
    todos: List[Todo] = field(default_factory=list)


class UserRepository(Protocol):
    def get_by_id(
        self, user_id: int, extend: Optional[str] = None
    ) -> Optional[User]: ...

    def get_by_username(
        self, username: str, extend: Optional[str] = None
    ) -> Optional[User]: ...

    def get_by_email(self, email: str) -> Optional[User]: ...

    def list_all(self) -> List[User]: ...

    def save(self, user: User) -> User: ...

    def delete(self, user_id: int) -> None: ...
