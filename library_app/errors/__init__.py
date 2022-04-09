from flask import Blueprint

errors_pb = Blueprint('errors', __name__)

from library_app.errors import errors
