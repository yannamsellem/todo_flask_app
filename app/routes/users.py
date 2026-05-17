from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app import db
from app.models import User
from app.schemas import UserSchema, UserNoTodosSchema
from sqlalchemy.orm import selectinload
from marshmallow import Schema, fields
from flask import jsonify

users_bp = Blueprint('users', __name__, url_prefix='/api/users', description='Operations on users')

class UserQueryArgsSchema(Schema):
    username = fields.String()
    extend = fields.String()

@users_bp.route('')
class Users(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location='query')
    @users_bp.response(200, UserSchema(many=True))
    def get(self, query_args):
        """List all users"""
        username = query_args.get('username')
        extend = query_args.get('extend')
        query = User.query
        
        if username:
            query = query.filter(User.username.ilike(f'%{username}%'))
        
        if extend == 'todos':
            query = query.options(selectinload(User.todos))
        
        users = query.all()
        
        if extend == 'todos':
            return users
        
        return jsonify(UserNoTodosSchema(many=True).dump(users))

    @users_bp.arguments(UserSchema)
    @users_bp.response(201, UserNoTodosSchema)
    def post(self, new_user):
        """Create a new user"""
        db.session.add(new_user)
        db.session.commit()
        return new_user

@users_bp.route('/<int:id>')
class UserById(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location='query')
    @users_bp.response(200, UserSchema)
    def get(self, query_args, id):
        """Get user by ID"""
        extend = query_args.get('extend')
        query = User.query
        if extend == 'todos':
            query = query.options(selectinload(User.todos))
            
        user = query.filter_by(id=id).first_or_404()
        
        if extend == 'todos':
            return user
            
        return jsonify(UserNoTodosSchema().dump(user))

    @users_bp.arguments(UserSchema(partial=True, load_instance=False))
    @users_bp.response(200, UserNoTodosSchema)
    def put(self, data, id):
        """Update user by ID"""
        user = db.get_or_404(User, id)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @users_bp.response(204)
    def delete(self, id):
        """Delete user by ID"""
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
