from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields
from sqlalchemy.orm import selectinload

from app.models import User
from app.schemas import UserNoTodosSchema, UserSchema

from . import users_bp


class UserQueryArgsSchema(Schema):
    username = fields.String()
    extend = fields.String()
    page = fields.Integer(load_default=1)
    page_size = fields.Integer(load_default=10)


@users_bp.route("")
class Users(MethodView):
    @users_bp.arguments(UserQueryArgsSchema, location="query")
    @users_bp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List all users with pagination"""
        username = query_args.get("username")
        extend = query_args.get("extend")
        page = query_args.get("page")
        page_size = query_args.get("page_size")

        query = User.query

        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))

        if extend == "todos":
            query = query.options(selectinload(User.todos))

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        users = pagination.items

        headers = {
            "X-Total-Count": pagination.total,
            "X-Total-Pages": pagination.pages,
            "X-Current-Page": pagination.page,
        }

        if extend == "todos":
            return users, 200, headers

        response_data = UserNoTodosSchema(many=True).dump(users)
        return jsonify(response_data), 200, headers
