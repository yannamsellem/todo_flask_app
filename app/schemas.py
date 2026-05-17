from marshmallow import Schema, fields

from app import ma
from app.models import Todo, User


class TodoNoAuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True
        exclude = ("author",)

    user_id = fields.Integer(dump_only=True)


class UserNoTodosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("todos", "password_hash")

    password = fields.String(load_only=True, required=True)


class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True

    author = fields.Nested(UserNoTodosSchema, dump_only=True)
    user_id = fields.Integer(dump_only=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

    password = fields.String(load_only=True, required=True)
    todos = fields.Nested(TodoNoAuthorSchema, many=True, dump_only=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


# Pre-initialized schemas for convenience
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_no_todos_schema = UserNoTodosSchema()
users_no_todos_schema = UserNoTodosSchema(many=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
todo_no_author_schema = TodoNoAuthorSchema()
todos_no_author_schema = TodoNoAuthorSchema(many=True)
