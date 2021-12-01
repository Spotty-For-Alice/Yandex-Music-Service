import os


class BaseConfig:
    HOST = os.getenv('HOST')
    SECRET_KEY = os.getenv('SECRET_KEY', 'lol')
    DEBUG = False
    TESTING = False
    # Настройки Redis

    # Настройки Postgres
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'auth_database')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 1234)
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT = os.getenv('POSTGRES_DB', 5432)

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JSON_AS_ASCII = False


class DevelopmentBaseConfig(BaseConfig):
    DEBUG = True


class ProductionBaseConfig(BaseConfig):
    DEBUG = False


class TestBaseConfig(BaseConfig):
    DEBUG = False
    TESTING = True
