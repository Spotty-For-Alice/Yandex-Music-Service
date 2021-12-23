from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from pg_db import db
from mixins import BaseModelMixin


class User(db.Model, BaseModelMixin):
    __tablename__ = 'user'

    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    yandex_id = db.Column(db.String, unique=True, nullable=False)
    history = db.relationship('History', backref='user')
    access_token = db.Column(db.String, nullable=True)
    spotify_playlist_id = db.Column(db.String, nullable=True)
    apple_playlist_id = db.Column(db.String, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_playlist_by_service(self, service_name):
        if service_name == 'spotify':
            return self.spotify_playlist_id
        return self.apple_playlist_id

    def set_playlist_by_service(self, service_name, uid):
        if service_name == 'spotify':
            self.spotify_playlist_id = uid
        else:
            self.apple_playlist_id = uid
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return f'<User {self.login}>'


class History(db.Model, BaseModelMixin):

    user_id = db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id', ondelete='CASCADE'))
    user_agent = db.Column(db.String)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    info = db.Column(db.String)

    def __str__(self):
        return f'<History {self.user_id}>'
