from marshmallow import Schema, fields, post_load

import validate_functions
from models import User


class UserRegisterSchema(Schema):
    username = fields.String(validate=validate_functions.validate_user_exist, required=True)
    password = fields.String(required=True)
    tgBotId = fields.String(required=False, allow_none=True)
    yandexId = fields.String(required=False, allow_none=True)

    @post_load
    def register_user(self, data, **kwargs):
        user = User(login=data['username'], password=data['password'])
        return user


class TrackSchema(Schema):
    artist = fields.String(required=True)
    name = fields.String(required=True)
    album = fields.String(required=True)


class SynchronizeTracksSchema(Schema):
    username = fields.String(validate=validate_functions.validate_exist_user_by_id, required=True)
    name = fields.String(required=True)
    tracks = fields.Nested(TrackSchema, many=True, required=True)
    guid = fields.String(required=False, allow_none=True)
