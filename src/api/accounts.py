from http import HTTPStatus


from flask import Blueprint, request, jsonify

from models.accounts import User
from schemas.accounts import UserRegisterSchema, SynchronizeTracksSchema
from yandex_music import Client
from yandex_music.exceptions import YandexMusicError

accounts = Blueprint('accounts', __name__)


@accounts.route('/register', methods=['POST'])
def register():
    user = UserRegisterSchema().load(request.get_json())
    try:
        yandex_user = Client.fromCredentials(username=user.login,
                                             password=user.password)
    except YandexMusicError:
        return jsonify({
            'status': 'error',
            'message': f'Ошибка при попытке авторизации',
        }), HTTPStatus.BAD_REQUEST
    user.access_token = yandex_user.token
    user.save()
    return jsonify({
        'status': 'ok',
        'message': f'Пользователь успешно зарегистрирован',
        'data': {'yandex_id': yandex_user.me.account.uid,
                 'user_service_id': user.id}
    }), HTTPStatus.CREATED


@accounts.route('/synchronize_tracks/<service>', methods=['POST'])
def synchronize_tracks(service):
    data = request.get_json()
    data['service'] = service
    synchronize_info = SynchronizeTracksSchema().load(data)
    user = User.query.filter_by(id=synchronize_info['user_id']).first()
    yandex_client = Client.fromToken(user.access_token)
    if not user.get_playlist_by_service(service):
        playlist = yandex_client.users_playlists_create(titile=service)
        user.set_playlist_by_service(service_name=service,
                                     uid=playlist.kind)
    playlist = yandex_client.users_playlists(kind=user.get_playlist_by_service(service))
    playlist.delete_tracks(from_=0, to=playlist.track_count)
    for track in synchronize_info['tracks']:
        artists = yandex_client.search(text=track['author'],
                                       type_='artist')
        if not artists:
            continue
        for artist in artists:
            artist_tracks = artist.get_tracks(page_size=300)
            for artist_track in artist_tracks:
                if artist_track.title == track['title']:
                    playlist.insert_track(track_id=artist_track.id, album_id=artist_tracks.albums[0].id)
                    continue
    return jsonify({
        'status': 'ok',
        'message': f'Треки из {service} успешно синхронизированы',
    }), HTTPStatus.CREATED