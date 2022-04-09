from flask import Blueprint

db_manage_bp = Blueprint('db_manage', __name__, cli_group=None)

from library_app.commands import db_manage_commands