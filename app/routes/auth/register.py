from flask.views import MethodView
from flask_smorest import abort

from app import db
from app.models import User
from app.schemas import UserSchema, UserNoTodosSchema
from . import auth_bp

@auth_bp.route('/register')
class Register(MethodView):
    @auth_bp.arguments(UserSchema(load_instance=False))
    @auth_bp.response(201, UserNoTodosSchema)
    def post(self, user_data):
        """Register a new user"""
        if User.query.filter_by(username=user_data['username']).first():
            abort(400, message="Username already exists")
        
        password = user_data.pop('password')
        new_user = User(**user_data)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return new_user
