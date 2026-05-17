from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_smorest import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    api = Api(app)

    from app.routes.users import users_bp
    from app.routes.todos import todos_bp

    api.register_blueprint(users_bp)
    api.register_blueprint(todos_bp)

    return app
