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

client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

def check_index_exist(client, index_name):
    res = client.indices.exists(index=index_name)
    return res

def index_vc():
    if check_index_exist(client, 'visaac'):
        return 'index visaac already exists'
    client.indices.create(index='visaac')

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

def create_news_index():
    if check_index_exist(client, 'news'):
        return 'index news created'


def insert_data_in_news_elastic():
    if not check_index_exist(client, 'news'):
        return 'index news not create'

    data = serv.create_correct_data(serv.get_info_site1(
        'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
        'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))

    df = spark.read.json(sc.parallelize([data]))
    df = df.drop('image').drop('sourceName') \
        .withColumnRenamed('description', 'body').withColumnRenamed('url', 'link').withColumnRenamed('time', 'date')
    df = df.withColumn('date', regexp_replace(substring(df['date'], 0, 10), r'\.', r'-'))

    for item in df.collect():
        q = {
            "bool": {
                "must": [

                    {"match": {"title": item['title']}},
                    {"match": {"body": item['body']}},
                    {"match": {"date": item['date']}},
                    {"match": {"link": item['link']}}
                ]
            }
        }

        res = client.search(index="news", query=q)

        if res['hits']['total']['value'] == 0:
            client.index(
                index="news",
                document={
                    "title": item['title'],
                    "body": item['body'],
                    "date": item['date'],
                    "link": item['link']
                })
        else:
            res_id = res['hits']['hits'][0]['_id']
            document = {
                "title": item['title'],
                "body": item['body'],
                "date": item['date'],
                "link": item['link']
            }

            client.update(index='news', id=res_id, doc=document)

    client.indices.refresh(index="news")

def main():
    index_vc()
    create_news_index()
    visa_to_es()
    insert_data_in_news_elastic()

if __name__ == "__main__":
    main()
# curl -X GET 'http://localhost:9200/_cat/indices?v'