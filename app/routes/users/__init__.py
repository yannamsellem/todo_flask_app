from flask_smorest import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/api/users', description='Operations on users')

from .list import Users
from .detail import UserById
