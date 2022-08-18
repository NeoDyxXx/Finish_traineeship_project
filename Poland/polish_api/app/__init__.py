from elasticsearch import Elasticsearch
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
import config

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    app.config['SWAGGER_URL'],
    app.config['API_URL'],
    config={
        'app_name': 'polish api'
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=app.config['SWAGGER_URL'])

from . import routes
