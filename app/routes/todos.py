from flask import Blueprint, request, jsonify
from app import db
from app.models import Todo, User
from app.schemas import todo_schema, todos_schema, TodoSchema
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('', methods=['GET'])
def get_todos():
    query = Todo.query
    
    # Query parameters
    user_id = request.args.get('user_id', type=int)
    completed = request.args.get('completed')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    extend = request.args.get('extend')

    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if completed is not None:
        is_completed = completed.lower() == 'true'
        query = query.filter_by(completed=is_completed)

    # Performance optimization if extending
    if extend == 'author':
        query = query.options(joinedload(Todo.author))

    # Sorting
    if hasattr(Todo, sort):
        column = getattr(Todo, sort)
        if order == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    todos = query.all()
    
    # Dynamic schema modification based on extend param
    if extend == 'author':
        result = todos_schema.dump(todos)
    else:
        # Default behavior: exclude author
        result = TodoSchema(many=True, exclude=('author',)).dump(todos)
        
    return jsonify(result), 200

@todos_bp.route('/<int:id>', methods=['GET'])
def get_todo(id):
    extend = request.args.get('extend')
    query = Todo.query
    if extend == 'author':
        query = query.options(joinedload(Todo.author))
    
    todo = query.filter_by(id=id).first_or_404()
    
    if extend == 'author':
        result = todo_schema.dump(todo)
    else:
        result = TodoSchema(exclude=('author',)).dump(todo)
        
    return jsonify(result), 200

@todos_bp.route('', methods=['POST'])
def create_todo():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    # Ensure user exists
    user_id = json_data.get('user_id')
    if not user_id or not db.session.get(User, user_id):
        return jsonify({"message": "Valid user_id is required"}), 400

    try:
        todo = todo_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.add(todo)
    db.session.commit()
    return jsonify(TodoSchema(exclude=('author',)).dump(todo)), 201

@todos_bp.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = db.get_or_404(Todo, id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    try:
        updated_todo = todo_schema.load(json_data, instance=todo, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.commit()
    return jsonify(TodoSchema(exclude=('author',)).dump(updated_todo)), 200

@todos_bp.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted"}), 204
