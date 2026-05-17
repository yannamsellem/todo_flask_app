from app.modules.identity.application.services import AuthService, UserService
from app.modules.identity.infrastructure.repositories import SQLAlchemyUserRepository
from app.modules.task_management.application.services import TodoService
from app.modules.task_management.infrastructure.repositories import (
    SQLAlchemyTodoRepository,
)


class Container:
    def __init__(self):
        self._user_repo = None
        self._todo_repo = None
        self._auth_service = None
        self._user_service = None
        self._todo_service = None

    @property
    def user_repo(self):
        if self._user_repo is None:
            self._user_repo = SQLAlchemyUserRepository()
        return self._user_repo

    @property
    def todo_repo(self):
        if self._todo_repo is None:
            self._todo_repo = SQLAlchemyTodoRepository()
        return self._todo_repo

    @property
    def auth_service(self):
        if self._auth_service is None:
            self._auth_service = AuthService(self.user_repo)
        return self._auth_service

    @property
    def user_service(self):
        if self._user_service is None:
            self._user_service = UserService(self.user_repo)
        return self._user_service

    @property
    def todo_service(self):
        if self._todo_service is None:
            self._todo_service = TodoService(self.todo_repo)
        return self._todo_service


container = Container()
