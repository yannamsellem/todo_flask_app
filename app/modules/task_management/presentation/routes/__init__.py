from flask_smorest import Blueprint

todos_bp = Blueprint("todos", "todos", description="Todo operations")

# Import routes to register them
from . import todo_detail, todos
