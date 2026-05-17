# Flask TODO API - Modular DDD Learning Project

A modern, type-safe RESTful TODO API built to explore and master the Python web ecosystem. This project demonstrates industry best practices for building scalable APIs using **Modular Monolith** and **Domain-Driven Design (DDD)** principles.

## 🚀 Architecture & Tech Stack

- **Pattern:** Modular Monolith with DDD Layering (Domain, Infrastructure, Application, Presentation).
- **Framework:** [Flask](https://flask.palletsprojects.com/) (App Factory pattern)
- **Authentication:** [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- **Documentation:** [OpenAPI 3.0](https://swagger.io/specification/) with [flask-smorest](https://flask-smorest.readthedocs.io/)
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modern Typed Mappings)
- **Querying:** **Specification Pattern** for clean, reusable data access logic.
- **Dependency Injection:** Custom **Container Pattern** for decoupled service management.
- **Database:** [PostgreSQL](https://www.postgresql.org/) (Production/Dev) & SQLite (Testing).
- **Environment:** [Docker Compose](https://docs.docker.com/compose/) for local development.

## 🛠 Features

- **Strict Layered Separation:** Domain logic is completely decoupled from database implementation details.
- **JWT Authentication:** Stateless secure user sessions.
- **Interactive OpenAPI Docs:** Fully documented API with Swagger UI at `/swagger-ui`.
- **Dynamic Eager Loading:** Use `?extend=author` or `?extend=todos` to fetch related data efficiently.
- **Advanced Filtering/Sorting:** Built using the Specification pattern for flexible querying.
- **Automated Testing:** 100% core logic coverage with isolated Pytest suite.

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.14+
- Docker & Docker Compose

### 2. Setup Environment
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Infrastructure & Database
```bash
docker-compose up -d
flask db upgrade
```

### 4. Run the Application
```bash
python run.py
```
- **API Base:** `http://127.0.0.1:5000/api`
- **Swagger UI:** `http://127.0.0.1:5000/swagger-ui`

## 📖 API Usage Examples

### 1. Register & Login
- `POST /api/auth/register`: Create user (`{"username": "...", "email": "...", "password": "..."}`)
- `POST /api/auth/login`: Get Token (`{"username": "...", "password": "..."}`)

### 2. Protected Routes
*Add `Authorization: Bearer <your_token>` header to all requests.*

- `GET /api/users`: List users.
- `GET /api/todos`: List **your** todos (supports `sort`, `order`, `completed` filters).
- `GET /api/todos/<id>?extend=author`: Get todo details with author information.

## 🧪 Testing
```bash
pytest
```

## 📚 Architectural Concepts in this Codebase
1. **Domain-Driven Design:** Explore `app/modules/identity/domain/` for pure business logic.
2. **Infrastructure Mapping:** See `app/modules/*/infrastructure/repositories.py` for mapping between DB models and Domain entities.
3. **Specification Pattern:** Check `app/modules/task_management/infrastructure/specifications.py` for reusable query logic.
4. **DI Container:** See `app/shared/infrastructure/container.py` for centralized dependency management.
5. **Route Organization:** Modular routes following the "One Class per File" pattern in `presentation/routes/`.
