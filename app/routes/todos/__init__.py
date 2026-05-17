from flask_smorest import Blueprint

todos_bp = Blueprint('todos', __name__, url_prefix='/api/todos', description='Operations on todos')

from .list import Todos
from .detail import TodoById
