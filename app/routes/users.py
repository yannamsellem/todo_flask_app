from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.schemas import user_schema, users_schema, UserSchema
from marshmallow import ValidationError
from sqlalchemy.orm import selectinload

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def get_users():
    # Example of query params: ?username=...
    username = request.args.get('username')
    extend = request.args.get('extend')
    query = User.query
    
    if username:
        query = query.filter(User.username.ilike(f'%{username}%'))
    
    if extend == 'todos':
        query = query.options(selectinload(User.todos))
    
    users = query.all()
    
    if extend == 'todos':
        result = users_schema.dump(users)
    else:
        result = UserSchema(many=True, exclude=('todos',)).dump(users)
        
    return jsonify(result), 200

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    extend = request.args.get('extend')
    query = User.query
    if extend == 'todos':
        query = query.options(selectinload(User.todos))
        
    user = query.filter_by(id=id).first_or_404()
    
    if extend == 'todos':
        result = user_schema.dump(user)
    else:
        result = UserSchema(exclude=('todos',)).dump(user)
        
    return jsonify(result), 200

@users_bp.route('', methods=['POST'])
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    try:
        user = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.add(user)
    db.session.commit()
    return jsonify(UserSchema(exclude=('todos',)).dump(user)), 201

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.get_or_404(User, id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    try:
        # Partial update
        updated_user = user_schema.load(json_data, instance=user, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    db.session.commit()
    return jsonify(UserSchema(exclude=('todos',)).dump(updated_user)), 200

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204
