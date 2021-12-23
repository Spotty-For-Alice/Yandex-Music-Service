from decouple import config
import os


class Config:
    HOST = os.getenv('APP_HOST')
    POSTGRES_DB = config('POSTGRES_DB')
    POSTGRES_USER = config('POSTGRES_USER')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_HOST = config('POSTGRES_HOST')
    POSTGRES_PORT = config('POSTGRES_PORT')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
