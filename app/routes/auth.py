from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from app import db
from app.models import User
from app.schemas import UserSchema, UserNoTodosSchema, LoginSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth', description='Authentication operations')

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

@auth_bp.route('/login')
class Login(MethodView):
    @auth_bp.arguments(LoginSchema)
    def post(self, login_data):
        """User login to receive JWT"""
        user = User.query.filter_by(username=login_data['username']).first()
        if user and user.check_password(login_data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        
        abort(401, message="Invalid username or password")
