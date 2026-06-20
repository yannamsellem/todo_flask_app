from typing import List, Optional

from app.modules.task_management.domain.todo import Todo, TodoRepository
from app.shared.domain.exceptions import EntityNotFoundException, UnauthorizedException


class TodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo = todo_repo

    def create_todo(
        self,
        user_id: int,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
    ) -> Todo:
        todo = Todo(
            user_id=user_id, title=title, description=description, completed=completed
        )
        return self.todo_repo.save(todo)

    def get_todo(
        self, todo_id: int, user_id: int, extend: Optional[str] = None
    ) -> Todo:
        todo = self.todo_repo.get_by_id(todo_id, extend=extend)
        if not todo:
            raise EntityNotFoundException("Todo not found")
        if todo.user_id != user_id:
            raise UnauthorizedException(
                "You do not have permission to access this todo"
            )
        return todo

    def list_todos(
        self,
        user_id: int,
        completed: Optional[bool] = None,
        extend: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[Todo]:
        return self.todo_repo.list_by_user(
            user_id, completed, extend=extend, sort=sort, order=order
        )

    def update_todo(self, todo_id: int, user_id: int, **kwargs) -> Todo:
        todo = self.get_todo(todo_id, user_id)
        for key, value in kwargs.items():
            if hasattr(todo, key):
                setattr(todo, key, value)
        return self.todo_repo.save(todo)

    def delete_todo(self, todo_id: int, user_id: int) -> None:
        todo = self.get_todo(todo_id, user_id)
        self.todo_repo.delete(todo.id)
