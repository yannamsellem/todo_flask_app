from typing import Any

from app.modules.task_management.infrastructure.models import TodoModel
from app.shared.infrastructure.specifications import Specification


class TodosByUserSpec(Specification):
    def __init__(self, user_id: int):
        self.user_id = user_id

    def apply(self, query: Any) -> Any:
        return query.where(TodoModel.user_id == self.user_id)


class CompletedTodosSpec(Specification):
    def __init__(self, completed: bool = True):
        self.completed = completed

    def apply(self, query: Any) -> Any:
        return query.where(TodoModel.completed == self.completed)


class SortSpecification(Specification):
    def __init__(self, field: str, order: str = "asc"):
        self.field = field
        self.order = order

    def apply(self, query: Any) -> Any:
        from sqlalchemy import asc, desc

        col = getattr(TodoModel, self.field, None)
        if col:
            if self.order == "desc":
                return query.order_by(desc(col))
            return query.order_by(asc(col))
        return query


class JoinedLoadSpecification(Specification):
    def __init__(self, relationship_name: str):
        self.relationship_name = relationship_name

    def apply(self, query: Any) -> Any:
        from sqlalchemy.orm import joinedload

        attr = getattr(TodoModel, self.relationship_name, None)
        if attr:
            return query.options(joinedload(attr))
        return query
