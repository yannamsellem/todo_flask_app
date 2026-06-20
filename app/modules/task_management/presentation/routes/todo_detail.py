from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from marshmallow import Schema, fields

from app.modules.task_management.presentation.schemas import TodoSchema
from app.shared.domain.exceptions import EntityNotFoundException, UnauthorizedException
from app.shared.infrastructure.container import container

from . import todos_bp


class TodoQueryArgsSchema(Schema):
    completed = fields.Boolean()
    extend = fields.String()
    sort = fields.String()
    order = fields.String()


@todos_bp.route("/<int:id>")
class TodoById(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location="query")
    @todos_bp.response(200, TodoSchema)
    @jwt_required()
    def get(self, query_args, id):
        """Get todo by ID"""
        user_id = int(get_jwt_identity())
        extend = query_args.get("extend")
        try:
            return container.todo_service.get_todo(id, user_id, extend=extend)
        except EntityNotFoundException as e:
            abort(404, message=str(e))
        except UnauthorizedException as e:
            abort(403, message=str(e))

    @todos_bp.arguments(TodoSchema(partial=True))
    @todos_bp.response(200, TodoSchema)
    @jwt_required()
    def put(self, todo_data, id):
        """Update todo by ID"""
        user_id = int(get_jwt_identity())
        try:
            return container.todo_service.update_todo(id, user_id, **todo_data)
        except EntityNotFoundException as e:
            abort(404, message=str(e))
        except UnauthorizedException as e:
            abort(403, message=str(e))

    @todos_bp.response(204)
    @jwt_required()
    def delete(self, id):
        """Delete todo by ID"""
        user_id = int(get_jwt_identity())
        try:
            container.todo_service.delete_todo(id, user_id)
            return ""
        except EntityNotFoundException as e:
            abort(404, message=str(e))
        except UnauthorizedException as e:
            abort(403, message=str(e))
