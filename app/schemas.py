from app import ma
from app.models import User, Todo
from marshmallow import fields

class TodoNoAuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True
        exclude = ("author",)

class UserNoTodosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("todos",)

class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True
    
    author = fields.Nested(UserNoTodosSchema)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    todos = fields.Nested(TodoNoAuthorSchema, many=True)

# Pre-initialized schemas for convenience
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_no_todos_schema = UserNoTodosSchema()
users_no_todos_schema = UserNoTodosSchema(many=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
todo_no_author_schema = TodoNoAuthorSchema()
todos_no_author_schema = TodoNoAuthorSchema(many=True)
