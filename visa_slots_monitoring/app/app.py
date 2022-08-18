import os
from elasticsearch import Elasticsearch
from distutils.log import debug
from flask import Flask, render_template, request, url_for, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from sqlalchemy.sql import func
import json
from flask import jsonify
import psycopg2

DRIVER_PATH = os.getenv('DRIVER_PATH')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app-name': "Real-Time-Monitoring"})
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exampledb',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'database', # set in docker-compose.yml
        'PORT': 5432 # default postgres port
    }
}


countresURL = {
    'Poland': 'pol',  #  1 Работал, но перестал, без поняти, что случилось
    'Latvia': 'lva',  #  2 Нет для нашей страны
    'Lithuania': 'ltu',# 3 работает, но мест для записи небыло ни разу
    'Spain': '-',  #     4 вообще без понятия
    'Norway': 'nor',  #  5 запись только по электронной почте
    'Thailand': 'tha', # 6 запись только по электронной почте
    'Austria': 'aut',
}


def check_index_exist(es, index_name):
    res = es.indices.exists(index=index_name)
    return res


def get_from_es(country):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': "http"}])
    if not check_index_exist(es, "appointment"):
        return "Table is not exist"

    result = es.search(
        index="appointment",
        query={
            "match": {
                "country": country
            }
        }
    )
    result_list = {country: []}

    for hit in result['hits']['hits']:
        result_list[country].append([
            {"address": hit['_source']['address']},
            {"category": hit['_source']['category']},
            {"subcategory": hit['_source']['subcategory']},
            {"appointmentTime": hit['_source']['appointment']}
        ])

    return result_list


@app.route('/')
def home():
    return (
        '<a class="button" href="/lva">Latvia</a>''<br>'
        '<a class="button" href="/aut">Austria</a>''<br>'
        '<a class="button" href="/ltu">Lithuania</a>''<br>'
        '<a class="button" href="/pol">Poland</a>''<br>'
        '<a class="button" href="/esp">Spain</a>''<br>'
        '<a class="button" href="/nor">Norway</a>''<br>'
        '<a class="button" href="/tha">Thailand</a>'
    )

@app.route('/aut', methods=('GET', 'POST'))
def home_aut():
    return jsonify(get_from_es('Austria'))

@app.route('/lva', methods=('GET', 'POST'))
def home_lva():
    return jsonify(get_from_es('Latvia'))


@app.route('/ltu', methods=('GET', 'POST'))
def home_ltu():
    return jsonify(get_from_es('Lithuania'))


@app.route('/pol', methods=('GET', 'POST'))
def home_pol():
    return jsonify(get_from_es('Poland'))


@app.route('/esp', methods=('GET', 'POST'))
def home_esp():
    return jsonify(get_from_es('Norway'))


@app.route('/nor', methods=('GET', 'POST'))
def home_nor():
    return jsonify(get_from_es('Norway'))


@app.route('/tha', methods=('GET', 'POST'))
def home_tha():
    return jsonify(get_from_es('Thailand'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
