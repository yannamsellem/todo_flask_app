from flask.views import MethodView
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields

from app.modules.identity.presentation.schemas import UserSchema
from app.shared.infrastructure.container import container

from . import users_bp


class UserQueryArgsSchema(Schema):
    username = fields.String()
    extend = fields.String()


@users_bp.route("")
class Users(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location="query")
    @users_bp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List users"""
        username = query_args.get("username")
        extend = query_args.get("extend")
        if username:
            user = container.user_repo.get_by_username(username, extend=extend)
            return [user] if user else []

        return container.user_repo.list_all()
