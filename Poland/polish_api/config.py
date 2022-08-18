import os


class BaseConfig:
    JSON_AS_ASCII = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://elasticsearch:9200'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
