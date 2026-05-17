# Flask TODO API - Learning Project

A modern, RESTful TODO API built to explore and master the Python web ecosystem. This project demonstrates industry best practices for building scalable, type-safe, and secured APIs.

## 🚀 Tech Stack

- **Framework:** [Flask](https://flask.palletsprojects.com/) (App Factory pattern)
- **Authentication:** [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- **Documentation:** [OpenAPI 3.0](https://swagger.io/specification/) with [flask-smorest](https://flask-smorest.readthedocs.io/)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with [psycopg3](https://www.psycopg.org/psycopg3/)
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modern Typed Mappings)
- **Migrations:** [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Alembic)
- **Serialization:** [Marshmallow](https://marshmallow.readthedocs.io/)
- **Testing:** [Pytest](https://docs.pytest.org/) with `pytest-flask`
- **Environment:** [Docker Compose](https://docs.docker.com/compose/) for local database development

## 🛠 Features

- **JWT Authentication:** Stateless secure user sessions.
- **RESTful Design:** Standard HTTP methods and status codes.
- **Advanced Querying:** Support for filtering, sorting, and pagination.
- **Dynamic Extensions:** Use `?extend=author` or `?extend=todos` to fetch related data.
- **Interactive Docs:** Built-in Swagger UI at `/swagger-ui`.
- **Automated Testing:** 100% core coverage with passing tests.

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.14+
- Docker & Docker Compose

### 2. Setup Environment
```bash
# Activate your virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Database
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
flask db upgrade
```

### 5. Run the Application
```bash
python run.py
```
The API will be available at `http://127.0.0.1:5000/api`.
Interactive Docs: `http://127.0.0.1:5000/swagger-ui`

## 📖 API Usage Examples

### 1. Register & Login
- `POST /api/auth/register`: Create user (`{"username": "...", "email": "...", "password": "..."}`)
- `POST /api/auth/login`: Get Token (`{"username": "...", "password": "..."}`)

### 2. Access Protected Routes
*Add `Authorization: Bearer <your_token>` header to all following requests.*

### Users
- `GET /api/users`: List all users with pagination.
- `GET /api/users/<id>?extend=todos`: Get user profile and their todos.

### Todos
- `GET /api/todos`: List **your** todos with filtering/sorting.
- `POST /api/todos`: Create a todo (Automatically linked to your account).
- `PUT /api/todos/<id>`: Update your todo.

## 🧪 Running Tests
```bash
pytest
```

## 📚 Key Concepts to Learn in this Codebase
1. **JWT Auth:** See `app/routes/auth.py` and `app/routes/todos.py` (@jwt_required).
2. **OpenAPI Integration:** Check `app/__init__.py` and the `MethodView` classes.
3. **App Factory Pattern:** See `app/__init__.py`.
4. **Typed Mappings:** Explore `app/models.py` for SQLAlchemy 2.0 syntax.
5. **REST Pagination:** See how headers are used for metadata in `routes/`.
