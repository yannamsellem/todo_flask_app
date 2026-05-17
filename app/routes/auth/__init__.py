from flask_smorest import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth', description='Authentication operations')

from .register import Register
from .login import Login
