import json

def test_create_user(client):
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data

def test_get_users(client):
    client.post('/api/users', json={'username': 'user1', 'email': 'u1@ex.com'})
    client.post('/api/users', json={'username': 'user2', 'email': 'u2@ex.com'})
    
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_get_user_by_id(client):
    post_resp = client.post('/api/users', json={'username': 'user1', 'email': 'u1@ex.com'})
    user_id = post_resp.get_json()['id']
    
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['username'] == 'user1'

def test_update_user(client):
    post_resp = client.post('/api/users', json={'username': 'user1', 'email': 'u1@ex.com'})
    user_id = post_resp.get_json()['id']
    
    response = client.put(f'/api/users/{user_id}', json={'username': 'updatedname'})
    assert response.status_code == 200
    assert response.get_json()['username'] == 'updatedname'

def test_delete_user(client):
    post_resp = client.post('/api/users', json={'username': 'user1', 'email': 'u1@ex.com'})
    user_id = post_resp.get_json()['id']
    
    response = client.delete(f'/api/users/{user_id}')
    assert response.status_code == 204
    
    get_resp = client.get(f'/api/users/{user_id}')
    assert get_resp.status_code == 404

def test_user_filtering(client):
    client.post('/api/users', json={'username': 'alice', 'email': 'alice@ex.com'})
    client.post('/api/users', json={'username': 'bob', 'email': 'bob@ex.com'})
    
    response = client.get('/api/users?username=ali')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['username'] == 'alice'

def test_user_extend_todos(client):
    # Create user
    post_user = client.post('/api/users', json={'username': 'alice', 'email': 'alice@ex.com'})
    user_id = post_user.get_json()['id']
    
    # Create todo for user
    client.post('/api/todos', json={'title': 'task1', 'user_id': user_id})
    
    # Get user without extend
    resp_no_extend = client.get(f'/api/users/{user_id}')
    assert 'todos' not in resp_no_extend.get_json()
    
    # Get user with extend
    resp_extend = client.get(f'/api/users/{user_id}?extend=todos')
    data = resp_extend.get_json()
    assert 'todos' in data
    assert len(data['todos']) == 1
    assert data['todos'][0]['title'] == 'task1'
