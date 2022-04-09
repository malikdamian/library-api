from flask import Blueprint

authors_bp = Blueprint('authors', __name__)

from library_app.authors import authors
