import pytest

from library_app import create_app, db
from library_app.commands.db_manage_commands import add_data


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    app.config['DB_FILE_PATH'].unlink(missing_ok=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def user(client):
    user = {
        'username': 'test',
        'email': 'test@example.com',
        'password': '123456'
    }
    client.post('/api/v1/auth/register', json=user)
    return user


@pytest.fixture
def token(client, user):
    response = client.post('/api/v1/auth/login',
                           json={
                               'username': user['username'],
                               'password': user['password']
                           })
    return response.get_json()['token']


@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)


@pytest.fixture
def author():
    return {
        'first_name': 'lata',
        'last_name': 'latanski',
        'birth_date': '01-01-1000'
    }


@pytest.fixture()
def book():
    return {
        'title': 'TEST API',
        'isbn': 1234567890000,
        'number_of_pages': 33,
        'description': 'REST API is COOL!',
    }


@pytest.fixture
def book_author_id(book):
    return {
        **book,
        'author_id': 1
    }
