from typing import List, Optional

from sqlalchemy import select

from app.modules.identity.domain.user import User, UserRepository
from app.modules.identity.infrastructure.models import UserModel
from app.modules.task_management.domain.todo import Todo
from app.shared.infrastructure.database import db


class SQLAlchemyUserRepository(UserRepository):
    def _to_domain(self, model: UserModel) -> User:
        user = User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            created_at=model.created_at,
        )
        if "todos" in model.__dict__:
            user.todos = [
                Todo(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    completed=t.completed,
                    user_id=t.user_id,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                )
                for t in model.todos
            ]
        return user

    def _to_model(self, user: User) -> UserModel:
        if user.id:
            model = db.session.get(UserModel, user.id)
            if model:
                model.username = user.username
                model.email = user.email
                model.password_hash = user.password_hash
                return model

        return UserModel(
            username=user.username, email=user.email, password_hash=user.password_hash
        )

    def get_by_id(self, user_id: int, extend: Optional[str] = None) -> Optional[User]:
        from .specifications import JoinedLoadSpecification

        stmt = select(UserModel).where(UserModel.id == user_id)
        if extend == "todos":
            stmt = JoinedLoadSpecification("todos").apply(stmt)

        result = db.session.execute(stmt)
        if extend == "todos":
            result = result.unique()
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    def get_by_username(
        self, username: str, extend: Optional[str] = None
    ) -> Optional[User]:
        from .specifications import JoinedLoadSpecification, UserByUsernameSpec

        stmt = select(UserModel)
        stmt = UserByUsernameSpec(username).apply(stmt)

        if extend == "todos":
            stmt = JoinedLoadSpecification("todos").apply(stmt)

        result = db.session.execute(stmt)
        if extend == "todos":
            result = result.unique()
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    def list_all(self) -> List[User]:
        stmt = select(UserModel)
        models = db.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def get_by_email(self, email: str) -> Optional[User]:
        from .specifications import UserByEmailSpec

        stmt = select(UserModel)
        stmt = UserByEmailSpec(email).apply(stmt)

        model = db.session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def save(self, user: User) -> User:
        model = self._to_model(user)
        db.session.add(model)
        db.session.commit()
        return self._to_domain(model)

    def delete(self, user_id: int) -> None:
        model = db.session.get(UserModel, user_id)
        if model:
            db.session.delete(model)
            db.session.commit()
