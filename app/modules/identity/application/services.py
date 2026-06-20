from typing import Optional

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.identity.domain.user import User, UserRepository
from app.shared.domain.exceptions import UnauthorizedException


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, username: str, email: str, password: str) -> User:
        if self.user_repo.get_by_username(username):
            raise Exception("Username already exists")
        if self.user_repo.get_by_email(email):
            raise Exception("Email already exists")

        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        return self.user_repo.save(user)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            raise UnauthorizedException("Invalid username or password")

        return create_access_token(identity=str(user.id))


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int, extend: Optional[str] = None) -> Optional[User]:
        return self.user_repo.get_by_id(user_id, extend=extend)
