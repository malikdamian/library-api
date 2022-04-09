from flask import jsonify
from webargs.flaskparser import use_args

from library_app import db
from library_app.authors import authors_bp
from library_app.models import Author, AuthorSchema, author_schema
from library_app.utils import validate_json_content_type, get_schema_args, \
    apply_order, apply_filter, get_pagination, token_required


@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    query = Author.query

    schema_args = get_schema_args(Author)
    query = apply_order(Author, query)
    query = apply_filter(Author, query)

    items, pagination = get_pagination(query, 'authors.get_authors')

    data = AuthorSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': data,
        'number_of_records': len(items),
        'pagination': pagination
    }), 200


@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id,
                                     description=f'Author with id: {author_id} not found')
    data = author_schema.dump(author)
    return jsonify({
        'success': True,
        'data': data
    })


@authors_bp.route('/authors', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def create_authors(user_id: int, args: dict):
    author = Author(**args)

    db.session.add(author)
    db.session.commit()

    data = author_schema.dump(author)
    return jsonify({
        'success': True,
        'data': data
    }), 201


@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(user_id: int, args: dict, author_id: int):
    author = Author.query.get_or_404(author_id,
                                     description=f'Author with id: {author_id} not found')

    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']

    db.session.commit()
    data = author_schema.dump(author)
    return jsonify({
        'success': True,
        'data': data
    })


@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
@token_required
def delete_author(user_id: int, author_id: int):
    author = Author.query.get_or_404(author_id,
                                     description=f'Author with id: {author_id} not found')
    db.session.delete(author)
    db.session.commit()
    return jsonify({
        'success': True,
        'data': f'Author with id: {author_id} has been deleted'
    })
