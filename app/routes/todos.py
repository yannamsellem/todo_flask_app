from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Todo, User
from app.schemas import TodoSchema, TodoNoAuthorSchema
from sqlalchemy.orm import joinedload
from marshmallow import Schema, fields
from flask import jsonify

todos_bp = Blueprint('todos', __name__, url_prefix='/api/todos', description='Operations on todos')

class TodoQueryArgsSchema(Schema):
    user_id = fields.Integer()
    completed = fields.String()
    sort = fields.String(load_default='created_at')
    order = fields.String(load_default='desc')
    extend = fields.String()
    page = fields.Integer(load_default=1)
    page_size = fields.Integer(load_default=10)

@todos_bp.route('')
class Todos(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location='query')
    @todos_bp.response(200, TodoSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List all todos with filtering, sorting, and pagination"""
        current_user_id = int(get_jwt_identity())
        query = Todo.query.filter_by(user_id=current_user_id)
        
        user_id = query_args.get('user_id')
        completed = query_args.get('completed')
        sort = query_args.get('sort')
        order = query_args.get('order')
        extend = query_args.get('extend')
        page = query_args.get('page')
        page_size = query_args.get('page_size')

        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if completed is not None:
            is_completed = completed.lower() == 'true'
            query = query.filter_by(completed=is_completed)

        if extend == 'author':
            query = query.options(joinedload(Todo.author))

        if hasattr(Todo, sort):
            column = getattr(Todo, sort)
            if order == 'desc':
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        todos = pagination.items
        
        headers = {
            "X-Total-Count": pagination.total,
            "X-Total-Pages": pagination.pages,
            "X-Current-Page": pagination.page
        }
        
        if extend == 'author':
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

@todos_bp.route('/<int:id>')
class TodoById(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location='query')
    @todos_bp.response(200, TodoSchema)
    @jwt_required()
    def get(self, query_args, id):
        """Get todo by ID"""
        current_user_id = int(get_jwt_identity())
        extend = query_args.get('extend')
        query = Todo.query.filter_by(id=id, user_id=current_user_id)
        
        if extend == 'author':
            query = query.options(joinedload(Todo.author))
        
        todo = query.first_or_404()
            
        if extend == 'author':
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
