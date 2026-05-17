from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    created_at = fields.DateTime(dump_only=True)
    todos = fields.List(
        fields.Nested(
            "app.modules.task_management.presentation.schemas.TodoSchema",
            exclude=("author",),
        ),
        dump_only=True,
    )


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class TokenSchema(Schema):
    access_token = fields.String(dump_only=True)
