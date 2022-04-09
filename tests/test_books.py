import pytest


def test_get_books_no_records(client):
    response = client.get('/api/v1/books')

    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/books?page=1'
        }
    }
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


def test_get_books(client, sample_data):
    response = client.get('/api/v1/books')

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 5
    assert response_data['number_of_records'] == 5
    assert response_data['pagination'] == {
        'total_pages': 3,
        'total_records': 14,
        'current_page': '/api/v1/books?page=1',
        'next_page': '/api/v1/books?page=2'
    }


def test_get_books_with_params(client, sample_data):
    response = client.get(
        '/api/v1/books?fields=title&sort=-number_of_pages&number_of_pages[gte]=400&page=2&limit=2'
    )

    response_data = response.get_json()
    print(response_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 2
    assert response_data['pagination'] == {
        'total_pages': 4,
        'total_records': 7,
        'current_page': '/api/v1/books?page=2&fields=title&sort=-number_of_pages&number_of_pages%5Bgte%5D=400&limit=2',
        'next_page': '/api/v1/books?page=3&fields=title&sort=-number_of_pages&number_of_pages%5Bgte%5D=400&limit=2',
        'previous_page': '/api/v1/books?page=1&fields=title&sort=-number_of_pages&number_of_pages%5Bgte%5D=400&limit=2'
    }
    assert response_data['data'] == [
        {
            'title': 'Inferno'
        },
        {
            'title': 'Mockingjay'
        },
    ]


def test_get_single_book(client, sample_data):
    response = client.get('/api/v1/books/4')

    expected_author = {
        'id': 3,
        'first_name': 'Roald',
        'last_name': 'Dahl'
    }
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['title'] == 'Matilda: Be Outrageous'
    assert response_data['data']['isbn'] == 9781524793616
    assert response_data['data']['number_of_pages'] == 32
    assert response_data['data']['author'] == expected_author


def test_get_single_book_not_found(client, sample_data):
    response = client.get('/api/v1/books/43')

    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_book(client, sample_data, book_author_id, token):
    response = client.put('/api/v1/books/5',
                          json=book_author_id,
                          headers={
                              'Authorization': f'Bearer {token}'
                          })
    expected_author = {
        'id': 1,
        'first_name': 'George',
        'last_name': 'Orwell'
    }
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['title'] == book_author_id['title']
    assert response_data['data']['isbn'] == book_author_id['isbn']
    assert response_data['data']['number_of_pages'] == book_author_id['number_of_pages']
    assert response_data['data']['description'] == book_author_id['description']
    assert response_data['data']['author'] == expected_author


@pytest.mark.parametrize(
    'data, missing_field',
    [
        ({'title': 'Jas Fasola', 'isbn': 9781524793616, 'author_id': 2}, 'number_of_pages'),
        ({'title': 'Jas Fasola', 'author_id': 2, 'number_of_pages': 532}, 'isbn'),
        ({'author_id': 2, 'isbn': 9781524793616, 'number_of_pages': 532}, 'title'),
    ]
)
def test_update_book_missing_field(client, sample_data, token, data, missing_field):
    response = client.put('/api/v1/books/7',
                          json=data,
                          headers={
                              'Authorization': f'Bearer {token}'
                          })

    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_update_book_missing_token(client, sample_data, book_author_id):
    response = client.put('/api/v1/books/5', json=book_author_id)

    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_book_invalid_content_type(client, sample_data, book_author_id, token):
    response = client.put('/api/v1/books/5',
                          data=book_author_id,
                          headers={
                              'Authorization': f'Bearer {token}'
                          })

    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_update_book_not_found(client, sample_data, book_author_id, token):
    response = client.put('/api/v1/books/58',
                          json=book_author_id,
                          headers={
                              'Authorization': f'Bearer {token}'
                          })

    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_delete_book(client, sample_data, token):
    response = client.delete('/api/v1/books/2',
                             headers={
                                 'Authorization': f'Bearer {token}'
                             })

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True

    response = client.delete('/api/v1/books/2',
                             headers={
                                 'Authorization': f'Bearer {token}'
                             })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False


def test_delete_author_not_found(client, sample_data, token):
    response = client.delete('/api/v1/books/42',
                             headers={
                                 'Authorization': f'Bearer {token}'
                             })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False


def test_create_book(client, token, sample_data, book):
    response = client.post('/api/v1/authors/1/books',
                           json=book,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })

    expected_result = {
        'success': True,
        'data': {
            **book,
            'id': 15,
            'author': {
                'first_name': 'George',
                'last_name': 'Orwell',
                'id': 1
            }
        }
    }
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result

    response = client.get('/api/v1/books/1')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data == expected_result


@pytest.mark.parametrize(
    'data, missing_field',
    [
        ({'title': 'Jas Fasola', 'isbn': 9781524793616}, 'number_of_pages'),
        ({'title': 'Jas Fasola', 'number_of_pages': 532}, 'isbn'),
        ({'isbn': 9781524793616, 'number_of_pages': 532}, 'title'),
    ]
)
def test_create_book_invalid_data(client, token, data, missing_field):
    response = client.post('/api/v1/authors/1/books',
                           json=data,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })

    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_create_book_missing_token(client, book):
    response = client.post('/api/v1/authors/1/books', json=book)

    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_invalid_content_type(client, book, token):
    response = client.post('/api/v1/authors/1/books',
                           data=book,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })

    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_get_all_author_books(client, sample_data):
    response = client.get('/api/v1/authors/6/books')

    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 3
    assert response_data['number_of_record'] == 3


def test_get_all_author_books_not_found(client, sample_data):
    response = client.get('/api/v1/authors/53/books')

    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
