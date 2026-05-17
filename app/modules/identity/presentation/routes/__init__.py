from flask_smorest import Blueprint

auth_bp = Blueprint("auth", "auth", description="Authentication operations")
users_bp = Blueprint("users", "users", description="User operations")

# Import routes to register them
from . import login, register, user_detail, users
