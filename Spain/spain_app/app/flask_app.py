from flask import Flask, jsonify, render_template
import serv
import requests
from flask_swagger_ui import get_swaggerui_blueprint
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
import time
from datetime import datetime


from pyspark import SparkContext, SparkConf
from pyspark.conf import SparkConf

conf = SparkConf()
conf.setMaster("local").setAppName("flask_app")
sc = SparkContext.getOrCreate(conf=conf)

from pyspark import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, ArrayType

sqlContext = SQLContext(sc)
spark = SparkSession.builder.getOrCreate()

# from pyspark.sql.functions import regexp_replace, regexp_extract, col



# client = Elasticsearch(
#     cloud_id='hello:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDQxZDRkZmZlYWNiYTQ4MGJhNWY2OTAwYmJhYzYwMWE1JGY0ZjM2NzU5NjFkNDRlNjE5MGQwYzZlYzYwYTgwYTRj',
#     basic_auth=('elastic', 'RNwz2XcJGWZgKhWhqBB9w8Bn')
# )

# es_pw = 'jq+bhLm5UJvlRadXWkHw'
# client = Elasticsearch("http://elastic:{}@localhost:9200".format(es_pw))

client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Spain App'
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

import psycopg2
from psycopg2 import Error


def check_index_exist(client, index_name):
    res = client.indices.exists(index=index_name)
    return res


@app.route("/")
def index():
    return (
        """
            <a class="button" href="/swagger">Swagger</a><br>
            <a class="button" href="/api/visa-center">Info about visa center</a><br>
            <a class="button" href="/api/to-file">Visa center to file</a><br>
            <a class="button" href="/api/to-file-2">Moscow Visa center to file</a><br>
            <a class="button" href="/api/visa-center-2">Info about Moscow visa center</a><br>
            <a class="button" href="/api/news">News</a><br>
            <a class="button" href="/api/news_in_file">News to file</a><br>
            <br>
            <a class="button" href="/api/index_vc">Create index visaac</a><br>
            <a class="button" href="/api/visa_to_es">Write visa centres to Elasticsearch</a><br>
            <a class="button" href="/api/all_visa_from_es">Get all visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/one_visa_from_es">Get certain (id = 1) visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/visa_from_es">Get <b>Spain</b> visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/minsk_visa_from_es">Get visa centres <b>located in Minsk</b> from Elasticsearch</a><br>
            <a class="button" href="/api/delete_visa_from_es">Delete index visaac</a><br>
            <br>
            <a class="button" href="/api/create_news_index">Create index news in elasticsearch</a><br>
            <a class="button" href="/api/delete_index_news_in_elastic">Delete index news in elasticsearch</a><br>
            <a class="button" href="/api/insert_data_in_news_elastic">Insert data in index news</a><br>
            <a class="button" href="/api/get_data_in_news_elastic">Get data in index news</a><br>
            <br>
            <a class="button" href="/api/html_news">News html</a><br>
            <a class="button" href="/api/html_courses">Courses html</a><br>
            <a class="button" href="/api/html_tickets">Tickets html</a><br>
        """
    )

@app.route("/api/to-file")
def to_file():
    all_centres = serv.create_file()
    return (
        "<p>{}</p>"
        "<p>wrote to file</p>".format(all_centres)
    )

@app.route("/api/visa-center")
def visa_center():
    center = serv.read_visa_center()
    return jsonify(center)

@app.route("/api/to-file-2")
def to_file2():
    all_centres = serv.create_file2()
    return (
        "<p>{}</p>"
        "<p>wrote to file</p>".format(all_centres)
    )

@app.route("/api/visa-center-2")
def visa_center2():
    center2 = serv.read_visa_center2()
    return jsonify(center2)

@app.route("/api/news", methods=['POST', 'GET'])
def news():
    return jsonify(serv.create_correct_data(
        serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))
            )


@app.route("/api/news_in_file", methods=["POST", "GET"])
def news_in_file():
    serv.save_in_file(serv.create_correct_data(
        serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))
            )
    return "<h3>File save</h3>"


@app.route("/api/index_vc")
def index_vc():
    if check_index_exist(client, 'visaac'):
        return 'index visaac already exists'
    client.indices.create(index='visaac')
    # client.indices.close(index='visaac')
    # settings = '''
    #     {
    #         "analysis": {
    #           "analyzer": {
    #             "rebuilt_keyword": {
    #               "tokenizer": "keyword",
    #               "filter": [ "word_delimiter" ]
    #             }
    #           }
    #         }
    #     }
    #     '''
    # client.indices.put_settings(index="visaac", body=settings)
    # client.indices.open(index='visaac')

    return "Index visaac created."

@app.route("/api/visa_to_es")
def visa_to_es():
    ######### if site is not working - read from file
    # center = serv.read_visa_center()

    ######### if site is working
    # html = serv.get_info_site('https://blsspain-belarus.com/contact.php')
    # center = serv.collect_info_data(html)

    ######### if site is not working - read from local php file
    # file = open('D:\\IBA PROJECT\\IBA-LAB-2022spring\\Spain\\spain_pyspark\\templates\\contact.php', "r", encoding='utf-8')
    # html = file.read()
    # center = serv.collect_info_data(html)

    try:
        requests.get('https://blsspain-belarus.com/contact.php')
        html = serv.get_info_site('https://blsspain-belarus.com/contact.php')
        center = serv.collect_info_data(html)
    except requests.exceptions.ConnectionError:
        file = open('D:\\IBA PROJECT\\IBA-LAB-2022spring\\Spain\\spain_pyspark\\templates\\contact.php', "r",
                    encoding='utf-8')
        html = file.read()
        center = serv.collect_info_data(html)


    columns = ['country', 'type', 'address', 'issue_working_hours', 'apply_working_hours', 'phone', 'email']
    vals = []

    vis_cen = spark.createDataFrame(vals, schema='country string, type string, address string, \
        issue_working_hours string, apply_working_hours string, phone string, email string')

    for i in range(len(center)):
        newVal = [(center[i]['Страна'], center[i]['Тип'], center[i]['Адрес'], center[i]['Время выдачи паспортов'], \
                  center[i]['Время приема'], center[i]['Тел'], center[i]['почта'])]
        newRow = spark.createDataFrame(newVal, columns)
        vis_cen = vis_cen.union(newRow)


    html = serv.get_info_site('https://blsspain-russia.com/moscow/contact.php')
    center2 = serv.collect_info_data2(html)

    for i in range(len(center2)):
        newVal = [(center2[i]['Страна'], center2[i]['Тип'], center2[i]['Адрес'], center2[i]['Время выдачи паспортов'], \
                  center2[i]['Время приема'], center2[i]['Тел'], center2[i]['почта'])]
        newRow = spark.createDataFrame(newVal, columns)
        vis_cen = vis_cen.union(newRow)

    vis_cen = vis_cen.withColumn("phone", regexp_replace(regexp_replace(regexp_replace(regexp_replace("phone", " ", ""), "\\-", ""), "\\(", ""), "\\)", ""))
    vis_cen = vis_cen.withColumn("address", regexp_replace(regexp_replace(regexp_replace('address', "\n\t", ""), " ,", ","), "г. ", ""))

    split_col = split(vis_cen['address'], ', ')
    vis_cen = vis_cen.withColumn('splitted_address', split_col)

    vis_cen = vis_cen.withColumn('index', split_col.getItem(1))
    vis_cen = vis_cen.withColumn('city', split_col.getItem(0))

    vis_cen = vis_cen.withColumn('index', vis_cen['index'].cast(StringType()))

    vis_cen = vis_cen.select('country', 'type', 'address', 'issue_working_hours', 'apply_working_hours', 'phone', 'email', 'splitted_address',
        when(vis_cen['index']<='999999', col("index")).otherwise(col("city")).alias("index"),
        when(vis_cen['index']<='999999', col("city")).otherwise(col("index")).alias("city")
    )

    vis_cen = vis_cen.withColumn("index", split(col("index"), ", ").cast(ArrayType(StringType())))

    # vis_cen = vis_cen.withColumn('address1', array_remove(vis_cen['splitted_address'], vis_cen['index']))
    vis_cen = vis_cen.withColumn('address', array_except(vis_cen['splitted_address'], vis_cen['index']))

    vis_cen = vis_cen.withColumn('address', concat_ws(', ', vis_cen['address']))
    vis_cen = vis_cen.withColumn('index', concat_ws(', ', vis_cen['index']))

    vis_cen = vis_cen.drop('splitted_address')

    vis_cen.show(truncate=False)

    i = 0
    for row in vis_cen.collect()[0:]:
        doc = {}
        doc['country'] = row['country']
        doc['city'] = row['city']
        doc['address'] = row['address']
        doc['index'] = row['index']
        doc['email'] = row['email']
        doc['issue_worktime'] = row['issue_working_hours']
        doc['apply_worktime'] = row['apply_working_hours']
        doc['telephone1'] = row['phone']
        client.index(index="visaac", id=i+1, document=doc)
        i+=1

    client.indices.refresh(index="visaac")

    return "Wrote to Elastic.<br><br><br>" + str(vis_cen.collect())


@app.route("/api/all_visa_from_es")
def all_visa_from_es():
    resp = client.search(index="visaac")
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:
        report += str(hit['_source']) + "<br>"
    return report

@app.route("/api/one_visa_from_es")
def one_visa_from_es():
    id = 1
    query = {
        "terms": {
            "_id": [id]
        }
    }
    resp = client.search(index="visaac", query=query)
    return str(resp['hits']['hits'][0]['_source'])

@app.route("/api/visa_from_es")
def visa_from_es():
    country = 'Испания'
    query = {
        "match": {
            "country": country
        }
    }
    resp = client.search(index="visaac", query=query)
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:
        report += str(hit['_source']) + "<br>"
    return report

@app.route("/api/minsk_visa_from_es")
def minsk_visa_from_es():
    city = 'минск'
    query = {
        "match": {
            "address": city
        }
    }
    resp = client.search(index="visaac", query=query)
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:
        report += str(hit['_source']) + "<br>"
    return report

@app.route("/api/delete_visa_from_es")
def delete_visa_from_es():
    if not check_index_exist(client, 'visaac'):
        return 'index visaac does not exist'
    client.indices.delete(index='visaac')
    return "Index visaac deleted."


@app.route('/api/create_news_index')
def create_news_index():
    if check_index_exist(client, 'news'):
        return 'index news created'

    request_body = {
	    "settings" : {
	        "number_of_shards": 3,
	        "number_of_replicas": 3
	    },
	    'mappings': {
            'properties': {
                'title': {'type': 'text'},
                'date': {'format': 'dd-MM-yyyy', 'type': 'date'},
                'body': {'type': 'text'},
                'link': {'type': 'text'}
	        }
        }
	}

    client.indices.create(index = 'news', body = request_body)
    return "created index news"

@app.route('/api/get_data_in_news_elastic')
def get_data_in_news_elastic():
    if not check_index_exist(client, 'news'):
        return 'index news not create'
    
    print(client.search(index="news", query={"match_all": {}})['hits'])
    return jsonify([item['_source'] for item in client.search(index="news", body={"size": 100, "query": {"match_all": {}}})['hits']['hits']])



@app.route('/api/insert_data_in_news_elastic')
def insert_data_in_news_elastic():
    if not check_index_exist(client, 'news'):
        return 'index news not create'

    data = serv.create_correct_data(serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))
    
    df = spark.read.json(sc.parallelize([data]))
    df = df.drop('image').drop('sourceName')\
        .withColumnRenamed('description', 'body').withColumnRenamed('url', 'link').withColumnRenamed('time', 'date')
    df = df.withColumn('date', regexp_replace(substring(df['date'], 0, 10), r'\.', r'-'))

    for item in df.collect():
        q = {
            "bool": {
                "must": [
                    
                    {"match" : {"title": item['title']}},
                    {"match" : {"body":  item['body']}},
                    {"match" : {"date":  item['date']}},
                    {"match" : {"link":  item['link']}}
                ]
            }
        }

        res = client.search(index="news",query=q)
        
        if res['hits']['total']['value'] == 0:
            client.index(
                index="news", 
                document={
                    "title": item['title'],
                    "body":  item['body'],
                    "date":  item['date'],
                    "link":  item['link']
                })
        else:
            res_id = res['hits']['hits'][0]['_id']
            document = {
                "title": item['title'],
                "body":  item['body'],
                "date":  item['date'],
                "link":  item['link']
            }

            client.update(index='news', id=res_id, doc=document)

    client.indices.refresh(index="news")
    return ('inserted data in news')

@app.route('/api/delete_index_news_in_elastic')
def delete_data_in_news():
    if not check_index_exist(client, 'news'):
        return 'index news not create'
    
    client.options(ignore_status=[400,404]).indices.delete(index='news')
    return ('index deleted')

@app.route('/api/html_news')
def html_news():
    report = []
    resp = client.search(index="news")
    for hit in resp['hits']['hits']:
        news_doc = hit['_source']
        news_date = datetime.strptime(news_doc["date"], "%d-%m-%Y")
        report.append((
            news_doc["title"],
            news_doc["body"],
            news_doc["link"],
            # news_doc["date"].strftime("%d-%m-%Y"))
            news_date.date())
        )
    report.sort(key=lambda y: y[3], reverse=True)

    return render_template("news.html", report=report)

@app.route('/api/html_courses')
def html_courses():
    report = []
    body = {
        "size": 100,
        "query": {
            "match_all": {}
        }
    }
    resp = client.search(index="courses", body=body)
    for hit in resp['hits']['hits']:
        courses_doc = hit['_source']
        report.append((
            courses_doc["language"],
            courses_doc["level"],
            courses_doc["url"],
            courses_doc["price"])
        )
    return render_template("courses.html", report=report)

@app.route('/api/html_tickets')
def html_tickets():
    report = []
    body = {
        "size": 100,
        "query": {
            "match_all": {}
        }
    }
    resp = client.search(index="tickets", body=body)
    for hit in resp['hits']['hits']:
        tickets_doc = hit['_source']
        ticket_date = datetime.strptime(tickets_doc["departure_date"] + " " + tickets_doc["departure_time"], "%d.%m.%y %H:%M")
        datetime_now = datetime.now().strftime("%d.%m.%y %H:%M")
        dt_now = datetime.strptime(datetime_now, "%d.%m.%y %H:%M")
        if (ticket_date > dt_now):
            report.append((
                tickets_doc["departure_city"],
                tickets_doc["arrival_city"],
                tickets_doc["departure_time"],
                tickets_doc["departure_day"],
                tickets_doc["departure_date"],
                tickets_doc["arrival_time"],
                tickets_doc["arrival_day"],
                tickets_doc["departure_date"],
                tickets_doc["travel_time"],
                tickets_doc["url"],
                tickets_doc["cost"])
            )
    # report.sort(key=lambda y: (y[4], y[2]))
    print(len(report))
    return render_template("tickets.html", report=report)

if __name__ == "__main__":
    # app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', debug=True)
