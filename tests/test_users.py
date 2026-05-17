import json
import pytest

def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert 'id' in data

def test_login_user(client):
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@ex.com',
        'password': 'password123'
    })
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_get_users(client, auth_headers):
    response = client.get('/api/users', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    # At least the authuser from fixture exists
    assert len(data) >= 1

def test_get_user_by_id(client, auth_headers):
    # We can get the authuser
    response = client.get('/api/users', headers=auth_headers)
    user_id = response.get_json()[0]['id']
    
    response = client.get(f'/api/users/{user_id}', headers=auth_headers)
    assert response.status_code == 200

def test_update_own_user(client):
    # Register and login to get specific user headers
    client.post('/api/auth/register', json={
        'username': 'upduser',
        'email': 'upd@ex.com',
        'password': 'password123'
    })
    login_resp = client.post('/api/auth/login', json={
        'username': 'upduser',
        'password': 'password123'
    })
    token = login_resp.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get ID
    me_resp = client.get('/api/users?username=upduser', headers=headers)
    user_id = me_resp.get_json()[0]['id']
    
    response = client.put(f'/api/users/{user_id}', json={'username': 'newname'}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['username'] == 'newname'

def test_delete_own_user(client):
    client.post('/api/auth/register', json={
        'username': 'deluser',
        'email': 'del@ex.com',
        'password': 'password123'
    })
    login_resp = client.post('/api/auth/login', json={
        'username': 'deluser',
        'password': 'password123'
    })
    token = login_resp.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    me_resp = client.get('/api/users?username=deluser', headers=headers)
    user_id = me_resp.get_json()[0]['id']
    
    response = client.delete(f'/api/users/{user_id}', headers=headers)
    assert response.status_code == 204

def test_user_extend_todos(client, auth_headers):
    # The authuser from fixture is logged in
    # Get my ID
    me_resp = client.get('/api/users?username=authuser', headers=auth_headers)
    user_id = me_resp.get_json()[0]['id']
    
    # Create todo
    client.post('/api/todos', json={'title': 'task1'}, headers=auth_headers)
    
    # Get user with extend
    resp_extend = client.get(f'/api/users/{user_id}?extend=todos', headers=auth_headers)
    data = resp_extend.get_json()
    assert 'todos' in data
    assert len(data['todos']) == 1
