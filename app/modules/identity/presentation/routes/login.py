from flask.views import MethodView
from flask_smorest import abort

from app.modules.identity.presentation.schemas import LoginSchema, TokenSchema
from app.shared.domain.exceptions import UnauthorizedException
from app.shared.infrastructure.container import container

from . import auth_bp


@auth_bp.route("/login")
class Login(MethodView):
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(200, TokenSchema)
    def post(self, login_data):
        """User login to receive JWT"""
        try:
            token = container.auth_service.login(
                username=login_data["username"], password=login_data["password"]
            )
            return {"access_token": token}
        except UnauthorizedException as e:
            abort(401, message=str(e))
