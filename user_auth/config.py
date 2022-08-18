import os


class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'postgres'
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or 'postgres'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'auth'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}'

    MAIL_SERVER = 'smtp.rambler.ru'
    MAIL_PORT = '465'
    MAIL_USERNAME = 'visatest123@rambler.ru'
    MAIL_PASSWORD = 'Qwerty123!'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass