from http import HTTPStatus

from flasgger import Swagger
from flask import Flask, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from db.pg_db import init_db, db


migrate = Migrate()


def validation_bad_request_handler(e):
    return jsonify({
        'status': 'error',
        'message': e.messages,
    }), HTTPStatus.BAD_REQUEST


def forbidden_handler(e):
    return jsonify({
            'status': 'error',
            'message': 'Ошибка доступа',
        }), HTTPStatus.FORBIDDEN


def create_app(configuration='core.config.DevelopmentBaseConfig'):
    from api.accounts import accounts
    app = Flask(__name__)
    app.config.from_object(configuration)
    init_db(app)
    migrate.init_app(app, db)
    app.register_blueprint(accounts, url_prefix='/api/v1/accounts')

    swagger = Swagger(app)
    app.register_error_handler(ValidationError, validation_bad_request_handler)
    app.register_error_handler(403, forbidden_handler)

    @app.before_first_request
    def setup_db():
        db.create_all()

    @app.teardown_appcontext
    def close_db(sender, **extra):
        db.session.close()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
