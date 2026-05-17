from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from marshmallow import Schema, fields

from app.modules.identity.presentation.schemas import UserSchema
from app.shared.infrastructure.container import container

from . import users_bp


class UserQueryArgsSchema(Schema):
    username = fields.String()
    extend = fields.String()


@users_bp.route("/<int:id>")
class UserById(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location="query")
    @users_bp.response(200, UserSchema)
    @jwt_required()
    def get(self, query_args, id):
        """Get user by ID"""
        extend = query_args.get("extend")
        user = container.user_service.get_user(id, extend=extend)
        if not user:
            abort(404, message="User not found")
        return user

    @users_bp.arguments(UserSchema(partial=True))
    @users_bp.response(200, UserSchema)
    @jwt_required()
    def put(self, user_data, id):
        """Update user by ID"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != id:
            abort(403, message="You can only update your own profile")

        user = container.user_service.get_user(id)
        if not user:
            abort(404, message="User not found")

        if "password" in user_data:
            from werkzeug.security import generate_password_hash

            user_data["password_hash"] = generate_password_hash(
                user_data.pop("password")
            )

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return container.user_repo.save(user)

    @users_bp.response(204)
    @jwt_required()
    def delete(self, id):
        """Delete user by ID"""
        current_user_id = int(get_jwt_identity())
        if current_user_id != id:
            abort(403, message="You can only delete your own profile")

        container.user_repo.delete(id)
        return ""
