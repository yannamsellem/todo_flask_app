from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    page = fields.Integer(load_default=1)
    page_size = fields.Integer(load_default=10)

@users_bp.route('')
class Users(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location='query')
    @users_bp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List all users with pagination"""
        username = query_args.get('username')
        extend = query_args.get('extend')
        page = query_args.get('page')
        page_size = query_args.get('page_size')
        
        query = User.query
        
        if username:
            query = query.filter(User.username.ilike(f'%{username}%'))
        
        if extend == 'todos':
            query = query.options(selectinload(User.todos))
        
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        users = pagination.items
        
        headers = {
            "X-Total-Count": pagination.total,
            "X-Total-Pages": pagination.pages,
            "X-Current-Page": pagination.page
        }
        
        if extend == 'todos':
            return users, 200, headers
        
        response_data = UserNoTodosSchema(many=True).dump(users)
        return jsonify(response_data), 200, headers

@users_bp.route('/<int:id>')
class UserById(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location='query')
    @users_bp.response(200, UserSchema)
    @jwt_required()
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
    @jwt_required()
    def put(self, data, id):
        """Update user by ID"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != id:
            abort(403, message="You can only update your own profile")
            
        user = db.get_or_404(User, id)
        
        if 'password' in data:
            user.set_password(data.pop('password'))
            
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @users_bp.response(204)
    @jwt_required()
    def delete(self, id):
        """Delete user by ID"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != id:
            abort(403, message="You can only delete your own profile")
            
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()
