from http import HTTPStatus
from flask import request, jsonify
from models import User
from schemas import UserRegisterSchema, SynchronizeTracksSchema
from yandex_music import Client
from yandex_music.exceptions import YandexMusicError
from marshmallow import ValidationError
from flask import Blueprint
from pg_db import db

yandex = Blueprint('yandex', __name__)


@yandex.route('/register', methods=['POST'])
def register():
    try:
        user = UserRegisterSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        yandex_user = Client.fromCredentials(username=user.login,
                                             password=user.password)
    except YandexMusicError:
        return jsonify({
            'status': 'error',
            'message': f'Ошибка при попытке авторизации',
        }), HTTPStatus.BAD_REQUEST
    user.access_token = yandex_user.token
    user.yandex_id = ""
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'status': 'ok',
        'message': f'Пользователь успешно зарегистрирован',
        'yandex_login': user.login,
    }), HTTPStatus.CREATED


@yandex.route('/synchronize_tracks', methods=['POST'])
def synchronize_tracks():
    try:
        synchronize_info = SynchronizeTracksSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = User.query.filter_by(login=synchronize_info['username']).first()
    # if not user:
    #     return jsonify({
    #         'status': 'error',
    #         'message': f'Пользователь не найден',
    #     }), HTTPStatus.NOT_FOUND
    yandex_client = Client.fromToken(user.access_token)

    playlist = yandex_client.users_playlists_create(title=synchronize_info['name'])
    user.set_playlist_by_service(service_name=synchronize_info['name'],
                                 uid=playlist.kind)
    playlist = yandex_client.users_playlists(kind=user.get_playlist_by_service(synchronize_info['name']))
    playlist.delete_tracks(from_=0, to=playlist.track_count)
    for track in synchronize_info['tracks']:
        artists = yandex_client.search(text=track['artist'],
                                       type_='artist')
        if not artists:
            continue

        check = False
        for artist in artists['artists']['results']:
            artist_tracks = yandex_client.artists_tracks(artist_id=artist['id'],
                                                         page_size=300)
            if check:
                break
            for artist_track in artist_tracks:

                if artist_track['title'] == track['name']:
                    playlist = yandex_client.users_playlists(kind=user.get_playlist_by_service(synchronize_info['name']))
                    yandex_client.track_supplement(track_id=artist_track.real_id)
                    yandex_client.albums_with_tracks(album_id=artist_track['albums'][0].id)
                    playlist.insert_track(track_id=artist_track.real_id, album_id=artist_track['albums'][0].id)
                    check = True
                    break
    return jsonify({
        'status': 'ok',
        'message': f'Треки успешно синхронизированы',
    }), HTTPStatus.CREATED
