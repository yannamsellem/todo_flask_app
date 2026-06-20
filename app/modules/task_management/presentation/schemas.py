from marshmallow import Schema, fields


class TodoSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    completed = fields.Boolean()
    user_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested(
        "app.modules.identity.presentation.schemas.UserSchema",
        exclude=("todos",),
        dump_only=True,
    )
