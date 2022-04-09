# Library REST API

REST API for online library. It supports authors of books and books resources including authentication (JWT Token).

## Setup

- Clone repository
- Create database and user
- Rename .env.example to `.env` and set your values
```buildoutcfg
# SQLALCHEMY_DATABASE_URI PostgreSQL template
SQLALCHEMY_DATABASE_URI=postgresql://<db_user>:<db_password>@<db_host>/<db_name>
```
- Create a virtual environment
```buildoutcfg
python -m venv venv
```
- Install packages from `requirements.txt`
```buildoutcfg
pip install -r requirements.txt
```
- Migrate database
```buildoutcfg
flask db upgrade
```
- Run command
```buildoutcfg
flask run
```


**NOTE**

Import / delete example data from `book_library_app/samples`:

```buildoutcfg
# import
flask db-manage add-data

# remove
flask db-manage remove-data
```

## Tests

In order to execute tests located in `tests/` run the command:

```buildoutcfg
python -m pytest tests/
```

## Technologies / Tools

- Python
- Flask
- Alembic
- SQLAlchemy
- Pytest
- PostgreSQL
- Postman