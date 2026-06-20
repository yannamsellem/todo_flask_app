import warnings

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api

from app.shared.infrastructure.database import db
from config import Config

migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    # Suppress apispec warnings
    warnings.filterwarnings(
        "ignore",
        message="Multiple schemas resolved to the name.*",
        category=UserWarning,
        module="apispec.ext.marshmallow.openapi",
    )

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import models to ensure they are registered with Base.metadata
    from app.shared.infrastructure import all_models

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)

    # Configure API prefix if needed, or rely on blueprints.
    # To match previous behavior where tests use /api/auth/register,
    # we can either add /api to each blueprint or use a wrapper.
    # Let's check how flask-smorest handles it.

    from app.modules.identity.presentation.routes import auth_bp, users_bp
    from app.modules.task_management.presentation.routes import todos_bp

    # Prefixing blueprints with /api to maintain compatibility
    api.register_blueprint(auth_bp, url_prefix="/api/auth")
    api.register_blueprint(users_bp, url_prefix="/api/users")
    api.register_blueprint(todos_bp, url_prefix="/api/todos")

    return app
