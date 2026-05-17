import pytest

def test_create_todo(client, auth_headers):
    response = client.post('/api/todos', json={
        'title': 'Test Todo',
        'description': 'Test Description'
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Todo'

def test_get_todos(client, auth_headers):
    client.post('/api/todos', json={'title': 'task1'}, headers=auth_headers)
    client.post('/api/todos', json={'title': 'task2'}, headers=auth_headers)
    
    response = client.get('/api/todos', headers=auth_headers)
    assert response.status_code == 200
    # The fixture might have created some, plus these 2
    assert len(response.get_json()) >= 2

def test_todo_filtering_and_sorting(client, auth_headers):
    client.post('/api/todos', json={'title': 'b_task', 'completed': True}, headers=auth_headers)
    client.post('/api/todos', json={'title': 'a_task', 'completed': False}, headers=auth_headers)
    
    # Filter by completed
    resp = client.get('/api/todos?completed=true', headers=auth_headers)
    data = resp.get_json()
    assert any(t['title'] == 'b_task' and t['completed'] is True for t in data)
    
    # Sort by title asc
    resp = client.get('/api/todos?sort=title&order=asc', headers=auth_headers)
    data = resp.get_json()
    # Find the indices of our tasks in the potentially larger list
    titles = [t['title'] for t in data if t['title'] in ['a_task', 'b_task']]
    assert titles == ['a_task', 'b_task']

def test_todo_extend_author(client, auth_headers):
    client.post('/api/todos', json={'title': 'ext_task'}, headers=auth_headers)
    
    # With extend
    resp = client.get('/api/todos?extend=author', headers=auth_headers)
    data = resp.get_json()
    target = next(t for t in data if t['title'] == 'ext_task')
    assert 'author' in target
    assert target['author']['username'] == 'authuser'

def test_update_todo(client, auth_headers):
    post_resp = client.post('/api/todos', json={'title': 'old_title'}, headers=auth_headers)
    todo_id = post_resp.get_json()['id']
    
    response = client.put(f'/api/todos/{todo_id}', json={'title': 'new_title', 'completed': True}, headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'new_title'
    assert data['completed'] is True

def test_delete_todo(client, auth_headers):
    post_resp = client.post('/api/todos', json={'title': 'task_to_del'}, headers=auth_headers)
    todo_id = post_resp.get_json()['id']
    
    assert client.delete(f'/api/todos/{todo_id}', headers=auth_headers).status_code == 204
    assert client.get(f'/api/todos/{todo_id}', headers=auth_headers).status_code == 404
