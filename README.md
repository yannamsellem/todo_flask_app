# Flask TODO API - Learning Project

A modern, RESTful TODO API built to explore and master the Python web ecosystem. This project demonstrates industry best practices for building scalable and type-safe APIs.

## 🚀 Tech Stack

- **Framework:** [Flask](https://flask.palletsprojects.com/) (App Factory pattern)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with [psycopg3](https://www.psycopg.org/psycopg3/)
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modern Typed Mappings)
- **Migrations:** [Flask-Migrate](https://flask-migrate.readthedocs.io/) (Alembic)
- **Serialization:** [Marshmallow](https://marshmallow.readthedocs.io/) & [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)
- **Testing:** [Pytest](https://docs.pytest.org/) with `pytest-flask`
- **Environment:** [Docker Compose](https://docs.docker.com/compose/) for local database development

## 🛠 Features

- **RESTful Design:** Standard HTTP methods and status codes.
- **Advanced Querying:** Support for filtering, sorting, and dynamic relationship loading.
- **Dynamic Extensions:** Use `?extend=author` or `?extend=todos` to fetch related data in a single request.
- **Type Safety:** Leveraging SQLAlchemy 2.0 `Mapped` types for better developer experience.
- **Automated Testing:** 100% core coverage with isolated in-memory testing.

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

## 📖 API Usage Examples

### Users
- `GET /api/users`: List all users.
- `GET /api/users?username=alice`: Filter users by name.
- `GET /api/users/<id>?extend=todos`: Get user and their todos.
- `POST /api/users`: Create a user (JSON: `{"username": "...", "email": "..."}`).

### Todos
- `GET /api/todos`: List all todos.
- `GET /api/todos?completed=false&sort=created_at&order=desc`: Filter and sort.
- `GET /api/todos?extend=author`: Include author details in response.
- `POST /api/todos`: Create a todo (JSON: `{"title": "...", "user_id": 1}`).

## 🧪 Running Tests
```bash
pytest
```

## 📚 Key Concepts to Learn in this Codebase
1. **App Factory Pattern:** See `app/__init__.py`.
2. **Typed Mappings:** Explore `app/models.py` for SQLAlchemy 2.0 syntax.
3. **Schemas:** Check `app/schemas.py` to see how Marshmallow handles JSON.
4. **Eager Loading:** Look at `app/routes/` to see `joinedload` and `selectinload` in action.
