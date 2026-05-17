from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.orm import joinedload

from app import db
from app.models import Todo
from app.schemas import TodoNoAuthorSchema, TodoSchema

from . import todos_bp


class TodoQueryArgsSchema(Schema):
    user_id = fields.Integer()
    completed = fields.String()
    sort = fields.String(load_default="created_at")
    order = fields.String(load_default="desc")
    extend = fields.String()
    page = fields.Integer(load_default=1)
    page_size = fields.Integer(load_default=10)


@todos_bp.route("")
class Todos(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location="query")
    @todos_bp.response(200, TodoSchema(many=True))
    @todos_bp.alt_response(401, description="Missing or invalid token")
    @todos_bp.doc(
        parameters=[
            {
                "name": "X-Custom-Header",
                "in": "header",
                "description": "Example custom header",
                "schema": {"type": "string"},
            }
        ]
    )
    @jwt_required()
    def get(self, query_args):
        """List all todos with filtering, sorting, and pagination"""
        current_user_id = int(get_jwt_identity())
        query = Todo.query.filter_by(user_id=current_user_id)

        user_id = query_args.get("user_id")
        completed = query_args.get("completed")
        sort = query_args.get("sort")
        order = query_args.get("order")
        extend = query_args.get("extend")
        page = query_args.get("page")
        page_size = query_args.get("page_size")

        if user_id:
            query = query.filter_by(user_id=user_id)

        if completed is not None:
            is_completed = completed.lower() == "true"
            query = query.filter_by(completed=is_completed)

        if extend == "author":
            query = query.options(joinedload(Todo.author))

        if hasattr(Todo, sort):
            column = getattr(Todo, sort)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        todos = pagination.items

        headers = {
            "X-Total-Count": pagination.total,
            "X-Total-Pages": pagination.pages,
            "X-Current-Page": pagination.page,
        }

        if extend == "author":
            return todos, 200, headers

        response_data = TodoNoAuthorSchema(many=True).dump(todos)
        return jsonify(response_data), 200, headers

    @todos_bp.arguments(TodoSchema)
    @todos_bp.response(201, TodoNoAuthorSchema)
    @jwt_required()
    def post(self, new_todo):
        """Create a new todo for the current user"""
        current_user_id = int(get_jwt_identity())
        new_todo.user_id = current_user_id

        db.session.add(new_todo)
        db.session.commit()
        return new_todo
