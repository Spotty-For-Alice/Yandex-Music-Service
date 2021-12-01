from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    username = 'music'
    password = 'trofimov'
    host = '127.0.0.1'
    database_name = 'flask_auth2'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{database_name}'
    db.init_app(app)
