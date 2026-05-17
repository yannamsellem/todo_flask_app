import pytest
from app import create_app, db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Create a user
    client.post('/api/auth/register', json={
        'username': 'authuser',
        'email': 'auth@ex.com',
        'password': 'password123'
    })
    # Login
    resp = client.post('/api/auth/login', json={
        'username': 'authuser',
        'password': 'password123'
    })
    token = resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def auth_user_id(client):
    resp = client.post('/api/auth/register', json={
        'username': 'iduser',
        'email': 'id@ex.com',
        'password': 'password123'
    })
    return resp.get_json()['id']
