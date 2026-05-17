from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields

from app.modules.task_management.presentation.schemas import TodoSchema
from app.shared.infrastructure.container import container

from . import todos_bp


class TodoQueryArgsSchema(Schema):
    completed = fields.Boolean()
    extend = fields.String()
    sort = fields.String()
    order = fields.String()


@todos_bp.route("")
class Todos(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location="query")
    @todos_bp.response(200, TodoSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List all todos for current user"""
        user_id = int(get_jwt_identity())
        completed = query_args.get("completed")
        extend = query_args.get("extend")
        sort = query_args.get("sort")
        order = query_args.get("order")

        return container.todo_service.list_todos(
            user_id, completed=completed, extend=extend, sort=sort, order=order
        )

    @todos_bp.arguments(TodoSchema)
    @todos_bp.response(201, TodoSchema)
    @jwt_required()
    def post(self, todo_data):
        """Create a new todo"""
        user_id = int(get_jwt_identity())
        return container.todo_service.create_todo(
            user_id=user_id,
            title=todo_data["title"],
            description=todo_data.get("description"),
            completed=todo_data.get("completed", False),
        )
