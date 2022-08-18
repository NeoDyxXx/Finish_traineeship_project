import json
import jsonify
from flask import Flask, make_response
from flask_swagger_ui import get_swaggerui_blueprint

"""from latvia_consulate import consulate_info
from latvia_embassy import embassy_information
from latvia_visa_centr import data"""

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Latvia App"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


from elasticsearch import Elasticsearch
import json

es = Elasticsearch("http://localhost:9200")

@app.route("/")
def main():
    return """
    <a class="button" href="/latvia/visa_center">Visa center</a><br>
    <a class="button" href="/latvia/embassy">Latvia embassy</a><br>
    <a class="button" href="/latvia/consulate">Latvia consulate</a><br>  
    <a class="button" href="/latvia/info">Latvia consulate info</a><br>
    <p>Creating indexes</p>
    <a class="button" href="/create_index_visaac">create_index_visaac</a><br>
    <a class="button" href="/create_index_consulate">create_index_consulate</a><br>
    <a class="button" href="/create_index_embassy">create_index_embassy</a><br>
    <p>Inserting data</p>
    <a class="button" href="/insert_visa_ac">insert_visa_ac</a><br>
    <a class="button" href="/insert_consulate">insert_consulate</a><br>
    <a class="button" href="/insert_embassy">insert_embassy</a><br>
    <p>Get data</p>
    <a class="button" href="/get_all_visa_ac">get_all_visa_ac</a><br>
    <a class="button" href="/get_consulate">get_consulate</a><br>
    <a class="button" href="/get_embassy">get_embassy</a><br>
    <a class="button" href="/delete_all_indexes">delete_all_indexes</a><br>
    <p>Search by</p>
    <a class="button" href="/search_by_id_1">search_by_id_1</a><br>
    <a class="button" href="/search_by_city">search_by_city_minsk</a><br>
    """


@app.route("/latvia/visa_center")
def latvia_visa_center():
    with open("latviya_visa_centers_info.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

@app.route("/latvia/embassy")
def latvia_embassy():
    with open("embassy_information.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

@app.route("/latvia/consulate")
def latvia_consulate():
    return "news unavailable"

@app.route("/latvia/info")
def latvia_consulate_info():
    with open("consulate_info.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

# Bring data to elastic

@app.route("/create_index_visaac")
def create_index_visaac():
    if es.indices.exists(index='visaac'):
        return 'index visaac already exists'
    else:
        es.indices.create(index='visaac')
        es.indices.close(index='visaac')
        settings = '''
                {
                    "analysis": {
                      "analyzer": {
                        "rebuilt_keyword": {
                          "tokenizer": "keyword",
                          "filter": [ "word_delimiter" ]
                        }
                      }
                    }
                }
                '''
        es.indices.put_settings(index="visaac", body=settings)
        es.indices.open(index='visaac')
        return "Index visaac created."

@app.route("/create_index_consulate")
def create_index_consulate():
    if es.indices.exists(index='consulate'):
        return 'consulate already exists'
    else:
        es.indices.create(index='consulate')
        es.indices.close(index='consulate')
        settings = '''
                {
                    "analysis": {
                      "analyzer": {
                        "rebuilt_keyword": {
                          "tokenizer": "keyword",
                          "filter": [ "word_delimiter" ]
                        }
                      }
                    }
                }
                '''
        es.indices.put_settings(index="consulate", body=settings)
        es.indices.open(index='consulate')
        return "Index consulate created."

@app.route("/create_index_embassy")
def create_index_embassy():
    if es.indices.exists(index='embassy'):
        return 'embassy already exists'
    else:
        es.indices.create(index='embassy')
        es.indices.close(index='embassy')
        settings = '''
                {
                    "analysis": {
                      "analyzer": {
                        "rebuilt_keyword": {
                          "tokenizer": "keyword",
                          "filter": [ "word_delimiter" ]
                        }
                      }
                    }
                }
                '''
        es.indices.put_settings(index="embassy", body=settings)
        es.indices.open(index='embassy')
        return "Index embassy created."

@app.route("/insert_consulate")
def insert_consulate():
    from scrappers.consulate import spark_consulate, get_consulate_info

    consulate_info = get_consulate_info()
    consulate = spark_consulate(consulate_info)
    doc = {}
    doc['country'] = consulate[0]['country']
    doc['address'] = consulate[0]['address']
    doc['email'] = consulate[0]['email']
    doc['city'] = consulate[0]['city']
    doc['worktime'] = consulate[0]['worktime']
    doc['telephone1'] = consulate[0]['telephone1']
    es.index(index="consulate", id='1', body=doc)
    return 'Insert data to elastic'

@app.route("/get_consulate")
def get_consulate():
    resp = es.search(index="consulate")
    for hit in resp['hits']['hits']:
        body = {}
        body['analyzer'] = 'standard'
        body['text'] = hit["_source"]['address']
        tokens = es.indices.analyze(index="consulate", body=body)
        # city = tokens['tokens'][0]['token']
    result = resp['hits']['hits'][0]['_source']
    return result

@app.route("/insert_visa_ac")
def insert_visa_ac():
    from scrappers.visa_centers import get_minsk_visaac, get_vitebsk_visaac, spark_visaac

    # insert minsk visa ac to elastic
    minsk_visaac_info = get_minsk_visaac()
    minsk_visaac = spark_visaac(minsk_visaac_info)
    doc = {}
    doc['country'] = minsk_visaac[0]['country']
    doc['address'] = minsk_visaac[0]['address']
    doc['issue_worktime'] = minsk_visaac[0]['issue_worktime']
    doc['apply_worktime'] = minsk_visaac[0]['apply_worktime']
    doc['telephone1'] = minsk_visaac[0]['telephone1']
    doc['city'] = minsk_visaac[0]['city']
    es.index(index="visaac", id='1', body=doc)


    # insert vitebsk visa ac to elastic
    vitebsk_visaacc_info = get_vitebsk_visaac()
    vitebsk_visaacc = spark_visaac(vitebsk_visaacc_info)
    doc = {}
    doc['country'] = vitebsk_visaacc[0]['country']
    doc['address'] = vitebsk_visaacc[0]['address']
    doc['issue_worktime'] = vitebsk_visaacc[0]['issue_worktime']
    doc['apply_worktime'] = vitebsk_visaacc[0]['apply_worktime']
    doc['telephone1'] = vitebsk_visaacc[0]['telephone1']
    doc['city'] = vitebsk_visaacc[0]['city']
    es.index(index="visaac", id='2', body=doc)
    es.indices.refresh(index="visaac")
    return 'Insert data to elastic'

@app.route("/get_all_visa_ac")
def get_all_visa_ac():
    resp = es.search(index="visaac")
    for hit in resp['hits']['hits']:
        body = {}
        body['analyzer'] = 'standard'
        body['text'] = hit["_source"]['address']
        tokens = es.indices.analyze(index="visaac", body=body)
        city = tokens['tokens'][0]['token']
    id1 = resp['hits']['hits'][0]
    id2 = resp['hits']['hits'][1]
    """return f"id1{id1}+\n+id2{id2}"""
    result=''
    for hit in resp['hits']['hits']:
        result += ("%(country)s %(address)s: %(issue_worktime)s %(city)s %(apply_worktime)s %(telephone1)s\n" % hit["_source"])
    return result

@app.route("/insert_embassy")
def insert_embassy():
    # insert embassy to elastic

    from scrappers.latvia_embassy import get_embassy_info, spark_embassy
    embassy_info = get_embassy_info()
    embassy = spark_embassy(embassy_info)
    doc = {}
    doc['country'] = embassy[0]['country']
    doc['address'] = embassy[0]['address']
    doc['worktime'] = embassy[0]['worktime']
    doc['phone'] = embassy[0]['phone']
    doc['city'] = embassy[0]['city']
    es.index(index="embassy", id='1', body=doc)
    return 'embassy info inserted'

@app.route("/get_embassy")
def get_embassy():
    resp = es.search(index="embassy")
    for hit in resp['hits']['hits']:
        body = {}
        body['analyzer'] = 'standard'
        body['text'] = hit["_source"]['address']
        tokens = es.indices.analyze(index="embassy", body=body)
    result = resp['hits']['hits'][0]['_source']
    return result

@app.route("/search_by_id_1")
def search_by_id_1():
    id = 2
    query = {
        "query": {
            "ids": {
                "values": [id]
            }
        }
    }
    resp = es.search(index="visaac", body=query)
    return str(resp['hits']['hits'][0]['_source'])


@app.route("/delete_all_indexes")
def delete_index():
    try:
        es.indices.delete(index='visaac', ignore=[400, 404])
        es.indices.delete(index='consulate', ignore=[400, 404])
        es.indices.delete(index='embassy', ignore=[400, 404])
        return "indexes deleted"
    except:
        return "indexes aren't created"

@app.route("/search_by_city")
def search_by_city():
    city = 'минск'
    query = {
        "query": {
            "match": {
                "city": city
            }
        }
    }
    resp = es.search(index="visaac", body=query)
    return str(resp['hits']['hits'][0]['_source'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)