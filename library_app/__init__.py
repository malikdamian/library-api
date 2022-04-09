from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from library_app.authors import authors_bp
    from library_app.errors import errors_pb
    from library_app.commands import db_manage_bp
    from library_app.books import books_bp
    from library_app.auth import auth_bp

    app.register_blueprint(errors_pb)
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(authors_bp, url_prefix='/api/v1')
    app.register_blueprint(books_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app
