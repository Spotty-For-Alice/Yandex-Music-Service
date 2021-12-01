from marshmallow import Schema, fields, post_load

import validate_functions
from models.accounts import User


class UserRegisterSchema(Schema):
    login = fields.String(validate=validate_functions.validate_user_exist, required=True)
    password = fields.String(required=True)

    @post_load
    def register_user(self, data, **kwargs):
        user = User(**data)
        return user


class TrackSchema(Schema):
    author = fields.String()
    title = fields.String()


class SynchronizeTracksSchema(Schema):
    user_id = fields.String(validate=validate_functions.validate_exist_user_by_id, required=True)
    service = fields.String(validate=validate_functions.validate_service_name, required=True)
    tracks = TrackSchema(many=True)
