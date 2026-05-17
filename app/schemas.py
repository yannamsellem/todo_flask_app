from app import ma
from app.models import User, Todo
from marshmallow import fields

class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        load_instance = True
        include_fk = True
    
    author = fields.Nested("UserSchema", exclude=("todos",))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    todos = fields.Nested("TodoSchema", many=True, exclude=("author",))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
