from app import create_app
import unittest
from http import HTTPStatus
from pg_db import db


class UserRegisterTestCase(unittest.TestCase):
    REAL_USERNAME = 'undergroundenemy616'
    REAL_PASSWORD = 'xanax322'
    FAKE_PASSWORD = 'fake'
    client = create_app().test_client()

    def setUp(self):
        self.client = create_app().test_client()

    def tearDown(self) -> None:
        db.drop_all(app=self.client.application)

    def test_register_user(self):
        response = self.client.post('/register',
                                    json={
                                        'username': self.REAL_USERNAME,
                                        'password': self.REAL_PASSWORD},
                                    )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(response.json['status'], 'ok')
        self.assertEqual(response.json['yandex_login'], self.REAL_USERNAME)

    def test_bad_creds_register_user(self):
        response = self.client.post('/register',
                                    json={
                                        'username': self.REAL_USERNAME,
                                        'password': self.FAKE_PASSWORD},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['message'], 'Ошибка при попытке авторизации')

    def test_user_exist(self):
        self.client.post('/register',
                         json={
                             'username': self.REAL_USERNAME,
                             'password': self.REAL_PASSWORD},
                         )
        response = self.client.post('/register',
                                    json={
                                        'username': self.REAL_USERNAME,
                                        'password': self.REAL_PASSWORD},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['username'], ['Пользователь с таким логином уже зарегистрирован в сервисе Yandex'])

    def test_missing_username_in_register_data(self):
        response = self.client.post('/register',
                                    json={
                                        'password': self.FAKE_PASSWORD},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['username'], ['Missing data for required field.'])

    def test_missing_password_in_register_data(self):
        response = self.client.post('/register',
                                    json={
                                        'username': self.REAL_USERNAME,
                                        'password': self.REAL_PASSWORD,
                                        'unknown_field': 'blabla'},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['unknown_field'], ['Unknown field.'])

    def test_unknown_field_in_register_data(self):
        response = self.client.post('/register',
                                    json={
                                        'userfdname': self.REAL_USERNAME},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['password'], ['Missing data for required field.'])


class SynchronizeTracksTestCase(unittest.TestCase):
    REAL_USERNAME = 'yaroslav.jr'
    REAL_PASSWORD = 'Eag5VN74usu2xG*$!!'
    FAKE_USERNAME = 'fake'
    service_names = ['spotify', 'apple']
    tracks = [{'artist': 'zavet',
               'name': '666',
               'album': 'gotika'}]

    def setUp(self):
        self.client = create_app().test_client()

    def tearDown(self) -> None:
        db.drop_all(app=self.client.application)

    def test_user_not_exists(self):
        response = self.client.post('/synchronize_tracks',
                                    json={
                                        'username': self.FAKE_USERNAME,
                                        'name': self.service_names[0],
                                        'tracks': self.tracks},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['username'], [f"Пользователь с username={self.FAKE_USERNAME} не существует"])

    def test_missing_username_in_synchronize_data(self):
        response = self.client.post('/synchronize_tracks',
                                    json={
                                        'name': self.service_names[0],
                                        'tracks': self.tracks},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['username'], ['Missing data for required field.'])

    def test_missing_name_in_synchronize_data(self):
        response = self.client.post('/synchronize_tracks',
                                    json={
                                        'username': self.FAKE_USERNAME,
                                        'tracks': self.tracks},
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['name'], ['Missing data for required field.'])

    def test_missing_tracks_in_synchronize_data(self):
        response = self.client.post('/synchronize_tracks',
                                    json={
                                        'username': self.FAKE_USERNAME,
                                        'name': self.service_names[0]}
                                    )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(response.json['tracks'], ['Missing data for required field.'])

    def test_success_synchronize_tracks(self):
        self.client.post('/register',
                         json={
                             'username': self.REAL_USERNAME,
                             'password': self.REAL_PASSWORD},
                         )
        response = self.client.post('/synchronize_tracks',
                                    json={
                                        'username': self.REAL_USERNAME,
                                        'name': self.service_names[0],
                                        'tracks': self.tracks}
                                    )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(response.json['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
