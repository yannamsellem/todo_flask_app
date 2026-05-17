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
    extend = fields.String()


@todos_bp.route("/<int:id>")
class TodoById(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location="query")
    @todos_bp.response(200, TodoSchema)
    @jwt_required()
    def get(self, query_args, id):
        """Get todo by ID"""
        current_user_id = int(get_jwt_identity())
        extend = query_args.get("extend")
        query = Todo.query.filter_by(id=id, user_id=current_user_id)

        if extend == "author":
            query = query.options(joinedload(Todo.author))

        todo = query.first_or_404()

        if extend == "author":
            return todo

        return jsonify(TodoNoAuthorSchema().dump(todo))

    @todos_bp.arguments(TodoSchema(partial=True, load_instance=False))
    @todos_bp.response(200, TodoNoAuthorSchema)
    @jwt_required()
    def put(self, data, id):
        """Update todo by ID"""
        current_user_id = int(get_jwt_identity())
        todo = Todo.query.filter_by(id=id, user_id=current_user_id).first_or_404()
        for key, value in data.items():
            setattr(todo, key, value)
        db.session.commit()
        return todo

    @todos_bp.response(204)
    @jwt_required()
    def delete(self, id):
        """Delete todo by ID"""
        current_user_id = int(get_jwt_identity())
        todo = Todo.query.filter_by(id=id, user_id=current_user_id).first_or_404()
        db.session.delete(todo)
        db.session.commit()
