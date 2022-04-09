import pytest


def test_registration(client):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': 'test',
                               'email': 'test@example.com',
                               'password': '123456'
                           })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']


@pytest.mark.parametrize(
    'data, missing_field',
    [
        ({'username': 'test', 'password': '123456'}, 'email'),
        ({'username': 'test', 'email': 'test@example.com'}, 'password'),
        ({'email': 'est@example.com', 'password': '123456'}, 'username')
    ]
)
def test_register_invalid_data(client, data, missing_field):
    response = client.post('/api/v1/auth/register', json=data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_register_invalid_content_type(client):
    response = client.post('/api/v1/auth/register',
                           data={
                               'username': 'test',
                               'email': 'test@example.com',
                               'password': '123456'
                           })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_username(client, user):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': user['username'],
                               'email': 'test1@example.com',
                               'password': '123456'
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_registration_already_used_email(client, user):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': 'user1',
                               'email': user['email'],
                               'password': '123456'
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_get_current_user(client, user, token):
    response = client.get('/api/v1/auth/me',
                          headers={
                              'Authorization': f'Bearer {token}'
                          })

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == user['username']
    assert response_data['data']['email'] == user['email']
    assert 'id' in response_data['data']
    assert 'creation_date' in response_data['data']


def test_get_current_user_missing_token(client):
    response = client.get('/api/v1/auth/me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_password_user(client, user, token):
    response = client.put('/api/v1/auth/update/password',
                          headers={
                              'Authorization': f'Bearer {token}'
                          },
                          json={
                              'current_password': user['password'],
                              'new_password': 'qazwsx'
                          })

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == user['username']
    assert response_data['data']['email'] == user['email']
    assert 'id' in response_data['data']
    assert 'creation_date' in response_data['data']


def test_update_password_user_missing_token(client, user):
    response = client.put('/api/v1/auth/update/password',
                          json={
                              'current_password': user['password'],
                              'new_password': 'qazwsx'
                          })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_password_user_invalid_password(client, user, token):
    response = client.put('/api/v1/auth/update/password',
                          headers={
                              'Authorization': f'Bearer {token}'
                          },
                          json={
                              'current_password': user['password'],
                              'new_password': '12345'
                          })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Length must be between 6 and 255.' in response_data['message']['new_password']


def test_update_user_data(client, user, token):
    response = client.put('/api/v1/auth/update/data',
                          headers={
                              'Authorization': f'Bearer {token}'
                          },
                          json={
                              'email': 'test1@example.com',
                              'username': 'test1'
                          })

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == 'test1'
    assert response_data['data']['email'] == 'test1@example.com'
    assert 'id' in response_data['data']
    assert 'creation_date' in response_data['data']
