from flask.views import MethodView
from flask_smorest import Blueprint, abort
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
    def get(self, query_args):
        """List all todos with filtering, sorting, and pagination"""
        query = Todo.query
        
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
    def post(self, new_todo):
        """Create a new todo"""
        if not db.session.get(User, new_todo.user_id):
            abort(400, message="Valid user_id is required")
            
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

@todos_bp.route('/<int:id>')
class TodoById(MethodView):
    @todos_bp.arguments(TodoQueryArgsSchema, location='query')
    @todos_bp.response(200, TodoSchema)
    def get(self, query_args, id):
        """Get todo by ID"""
        extend = query_args.get('extend')
        query = Todo.query
        if extend == 'author':
            query = query.options(joinedload(Todo.author))
        
        todo = query.filter_by(id=id).first_or_404()
        
        if extend == 'author':
            return todo
            
        return jsonify(TodoNoAuthorSchema().dump(todo))

    @todos_bp.arguments(TodoSchema(partial=True, load_instance=False))
    @todos_bp.response(200, TodoNoAuthorSchema)
    def put(self, data, id):
        """Update todo by ID"""
        todo = db.get_or_404(Todo, id)
        for key, value in data.items():
            setattr(todo, key, value)
        db.session.commit()
        return todo

    @todos_bp.response(204)
    def delete(self, id):
        """Delete todo by ID"""
        todo = db.get_or_404(Todo, id)
        db.session.delete(todo)
        db.session.commit()
