from flask.views import MethodView
from flask_smorest import abort

from app.modules.identity.presentation.schemas import UserSchema
from app.shared.infrastructure.container import container

from . import auth_bp


@auth_bp.route("/register")
class Register(MethodView):
    @auth_bp.arguments(UserSchema)
    @auth_bp.response(201, UserSchema)
    def post(self, user_data):
        """Register a new user"""
        try:
            user = container.auth_service.register(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
            )
            return user
        except Exception as e:
            abort(400, message=str(e))
