from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    from app.routes.auth import auth_bp
    from app.routes.todos import todos_bp
    from app.routes.users import users_bp

    api.register_blueprint(auth_bp)
    api.register_blueprint(users_bp)
    api.register_blueprint(todos_bp)

    return app
