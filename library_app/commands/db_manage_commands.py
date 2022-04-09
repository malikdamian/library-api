import json
from pathlib import Path
from datetime import datetime

from library_app import db
from library_app.models import Author, Book
from library_app.commands import db_manage_bp


def load_json_data(filename: str) -> list:
    json_patch = Path(__file__).parent.parent / 'samples' / filename
    with open(json_patch) as file:
        data_json = json.load(file)
    return data_json


# @app.cli.group()
@db_manage_bp.cli.group()
def db_manage():
    """Database management commands"""
    pass


@db_manage.command()
def add_data():
    """Add sample data to database"""
    try:
        data_json = load_json_data('authors.json')
        for item in data_json:
            item['birth_date'] = datetime.strptime(
                item['birth_date'], '%d-%m-%Y'
            ).date()
            author = Author(**item)
            db.session.add(author)

        data_json = load_json_data('books.json')
        for item in data_json:
            book = Book(**item)
            db.session.add(book)

        db.session.commit()
        print('Data has been successfully added to database')
    except Exception as e:
        print(f'Unexpected error {e}')


@db_manage.command()
def remove_data():
    """Remove all data from the database"""
    try:
        db.session.execute('DELETE FROM books')
        db.session.execute('ALTER TABLE authors AUTO_INCREMENT = 1')

        db.session.execute('DELETE FROM authors')
        db.session.execute('ALTER TABLE authors AUTO_INCREMENT = 1')

        db.session.commit()
        print('Data has been successfully removed from database')

    except Exception as e:
        print(f'Unexpected error {e}')
