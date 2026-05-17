import warnings

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
    # Suppress apispec warnings about multiple schemas with the same name.
    # This is a known noise issue when using multiple variations of the same model schema.
    # Apispec handles this internally by modifying the name.
    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name.*",
        category=UserWarning,
        module="apispec.ext.marshmallow.openapi",
    )

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
