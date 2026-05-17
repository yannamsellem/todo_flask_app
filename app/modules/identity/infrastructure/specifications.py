from typing import Any

from app.modules.identity.infrastructure.models import UserModel
from app.shared.infrastructure.specifications import Specification


class UserByUsernameSpec(Specification):
    def __init__(self, username: str):
        self.username = username

    def apply(self, query: Any) -> Any:
        return query.where(UserModel.username == self.username)


class UserByEmailSpec(Specification):
    def __init__(self, email: str):
        self.email = email

    def apply(self, query: Any) -> Any:
        return query.where(UserModel.email == self.email)


class JoinedLoadSpecification(Specification):
    def __init__(self, relationship_name: str):
        self.relationship_name = relationship_name

    def apply(self, query: Any) -> Any:
        from sqlalchemy.orm import joinedload

        attr = getattr(UserModel, self.relationship_name, None)
        if attr:
            return query.options(joinedload(attr))
        return query
