from flask import Flask
from flask_migrate import Migrate
from pg_db import db, init_db
from routes import yandex

migrate = Migrate()


def create_app(configuration='config.Config'):
    from models import User, History
    app = Flask(__name__)
    app.config.from_object(configuration)
    init_db(app)
    migrate.init_app(app, db)
    app.register_blueprint(yandex)

    @app.before_first_request
    def setup_db():
        db.create_all()

    @app.teardown_appcontext
    def close_db(sender, **extra):
        db.session.close()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
