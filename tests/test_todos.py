import pytest

@pytest.fixture
def user_id(client):
    resp = client.post('/api/users', json={'username': 'todo_owner', 'email': 'owner@ex.com'})
    return resp.get_json()['id']

def test_create_todo(client, user_id):
    response = client.post('/api/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description',
        'user_id': user_id
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Todo'
    assert data['user_id'] == user_id

def test_get_todos(client, user_id):
    client.post('/api/todos', json={'title': 'task1', 'user_id': user_id})
    client.post('/api/todos', json={'title': 'task2', 'user_id': user_id})
    
    response = client.get('/api/todos')
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_todo_filtering_and_sorting(client, user_id):
    client.post('/api/todos', json={'title': 'b_task', 'user_id': user_id, 'completed': True})
    client.post('/api/todos', json={'title': 'a_task', 'user_id': user_id, 'completed': False})
    
    # Filter by completed
    resp = client.get('/api/todos?completed=true')
    assert len(resp.get_json()) == 1
    assert resp.get_json()[0]['completed'] is True
    
    # Sort by title asc
    resp = client.get('/api/todos?sort=title&order=asc')
    data = resp.get_json()
    assert data[0]['title'] == 'a_task'
    assert data[1]['title'] == 'b_task'

def test_todo_extend_author(client, user_id):
    client.post('/api/todos', json={'title': 'task1', 'user_id': user_id})
    
    # No extend
    resp = client.get('/api/todos')
    assert 'author' not in resp.get_json()[0]
    
    # With extend
    resp = client.get('/api/todos?extend=author')
    data = resp.get_json()
    assert 'author' in data[0]
    assert data[0]['author']['username'] == 'todo_owner'

def test_update_todo(client, user_id):
    post_resp = client.post('/api/todos', json={'title': 'old_title', 'user_id': user_id})
    todo_id = post_resp.get_json()['id']
    
    response = client.put(f'/api/todos/{todo_id}', json={'title': 'new_title', 'completed': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'new_title'
    assert data['completed'] is True

def test_delete_todo(client, user_id):
    post_resp = client.post('/api/todos', json={'title': 'task', 'user_id': user_id})
    todo_id = post_resp.get_json()['id']
    
    assert client.delete(f'/api/todos/{todo_id}').status_code == 204
    assert client.get(f'/api/todos/{todo_id}').status_code == 404
