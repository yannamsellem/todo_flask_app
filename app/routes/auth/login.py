from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import create_access_token

from app.models import User
from app.schemas import LoginSchema
from . import auth_bp

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
