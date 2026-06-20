from app import create_app
from app.modules.identity.infrastructure.models import UserModel
from app.modules.task_management.infrastructure.models import TodoModel
from app.shared.infrastructure.database import db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": UserModel, "Todo": TodoModel}


if __name__ == "__main__":
    app.run(debug=True)
