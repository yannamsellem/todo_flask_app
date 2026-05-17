from typing import List, Optional

from sqlalchemy import select

from app.modules.identity.domain.user import User
from app.modules.task_management.domain.todo import Todo, TodoRepository
from app.modules.task_management.infrastructure.models import TodoModel
from app.shared.infrastructure.database import db


class SQLAlchemyTodoRepository(TodoRepository):
    def _to_domain(self, model: TodoModel) -> Todo:
        todo = Todo(
            id=model.id,
            title=model.title,
            description=model.description,
            completed=model.completed,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        if "author" in model.__dict__:
            todo.author = User(
                id=model.author.id,
                username=model.author.username,
                email=model.author.email,
                created_at=model.author.created_at,
            )

        return todo

    def _to_model(self, todo: Todo) -> TodoModel:
        if todo.id:
            model = db.session.get(TodoModel, todo.id)
            if model:
                model.title = todo.title
                model.description = todo.description
                model.completed = todo.completed
                model.user_id = todo.user_id
                return model

        return TodoModel(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id,
        )

    def get_by_id(self, todo_id: int, extend: Optional[str] = None) -> Optional[Todo]:
        from .specifications import JoinedLoadSpecification

        stmt = select(TodoModel).where(TodoModel.id == todo_id)
        if extend == "author":
            stmt = JoinedLoadSpecification("author").apply(stmt)

        result = db.session.execute(stmt)
        if extend == "author":
            result = result.unique()
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    def list_by_user(
        self,
        user_id: int,
        completed: Optional[bool] = None,
        extend: Optional[str] = None,
        sort: Optional[str] = None,
        order: Optional[str] = "asc",
    ) -> List[Todo]:
        from .specifications import (
            CompletedTodosSpec,
            JoinedLoadSpecification,
            SortSpecification,
            TodosByUserSpec,
        )

        stmt = select(TodoModel)

        # Apply specifications
        stmt = TodosByUserSpec(user_id).apply(stmt)

        if completed is not None:
            stmt = CompletedTodosSpec(completed).apply(stmt)

        if extend == "author":
            stmt = JoinedLoadSpecification("author").apply(stmt)

        if sort:
            stmt = SortSpecification(sort, order or "asc").apply(stmt)

        result = db.session.execute(stmt)
        if extend == "author":
            result = result.unique()
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    def save(self, todo: Todo) -> Todo:
        model = self._to_model(todo)
        db.session.add(model)
        db.session.commit()
        return self._to_domain(model)

    def delete(self, todo_id: int) -> None:
        model = db.session.get(TodoModel, todo_id)
        if model:
            db.session.delete(model)
            db.session.commit()
