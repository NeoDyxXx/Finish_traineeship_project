# import imp

import pyspark.sql
from elasticsearch import Elasticsearch
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from lithuania_scraper.visa_centre_scraper import parse_visa_centre
from lithuania_scraper.visa_centre_news_scraper import get_visa_centres_news

es = Elasticsearch('http://localhost:9200')

spark = SparkSession.builder.master("local[*]").getOrCreate()


def insert_visa_centre(client: Elasticsearch, df_vs: pyspark.sql.DataFrame):
    i = 0
    vs = df_vs.toPandas().to_dict(orient='index').values()
    try:
        for info in vs:
            client.index(index='visa_centre', id=str(i + 1), body=info)
            i += 1
        client.indices.refresh(index='visa_centre')
        return True
    except Exception as e:
        print(e)
        return False


def insert_consulates(client: Elasticsearch, df_cons: pyspark.sql.DataFrame):
    return df_cons
    i = 0
    consulates = df_cons.toPandas().to_dict(orient='index').values()
    try:
        for info in consulates:
            client.index(index='consulate', id=str(i + 1), body=info)
            i += 1
        client.indices.refresh(index='consulate')
        return True
    except Exception as e:
        print(e)
        return False


def insert_news(client: Elasticsearch, df_news: pyspark.sql.DataFrame):
    i = 0
    news_dict = df_news.toPandas().to_dict(orient='index').values()
    try:
        for news in news_dict:
            client.index(index='news', id=str(i + 1), body=news)
            i += 1
        client.indices.refresh(index='news')
        return True
    except Exception as e:
        print(e)
        return False


def search(index_name: str, search_text: str):
    return es.search(index=index_name, body=search_text)


def get_visa_centers():
    search_object = {'size': 10}
    return search('visa_centre', json.dumps(search_object))


def get_consulates():
    search_object = {'size': 10}
    return search('consulate', json.dumps(search_object))


def get_news():
    search_object = {'size': 100}
    return search('news', json.dumps(search_object))


def get_res(search_res):
    res = []
    for i in range(0, search_res['hits']['total']['value']):
        res.append(search_res['hits']['hits'][i]['_source'])
    return res


def process_vs_info(centre_info: list) -> pyspark.sql.DataFrame:
    df = spark.createDataFrame(data=centre_info)
    df2 = df.withColumn('Index', regexp_extract('Адрес', r'\d{6}', 0)) \
        .withColumn('City', regexp_extract('Адрес', r'([^\s\,]+)\,\sБеларусь', 1)) \
        .withColumn('Street', regexp_extract('Адрес', r'ул[^\d]+[^\,]+|пр[^\d,]+[^\,]+', 0)) \
        .withColumn('Building', regexp_extract('Street', r'\d+.?\d?', 0)) \
        .withColumn('Street', regexp_extract('Street', r'ул[^\d]+|пр[^\d,]+', 0)) \
        .withColumn('Address', concat(col('City'), lit(','), col('Street'), lit(','), col('Building'))) \
        .withColumn('Phone_number', regexp_replace('Phone_number', ' ', '')) \
        .drop('Street', 'Building', 'Адрес')

    return df2


def process_embassy_info(path: str) -> pyspark.sql.DataFrame:
    with open(path, 'r', encoding='utf-8') as f:
        embassy_info = json.load(f)
    embassy_info[1]['Country'] = embassy_info[0]['Страна']
    df = spark.createDataFrame(data=[embassy_info[1]])
    df = df.select('Country', 'Адрес:', 'Телефон:', 'Время Работы Посольства:')
    df2 = df.withColumn('Index', regexp_extract('Адрес:', r'\d{6}', 0)) \
        .withColumn('City', regexp_extract('Адрес:', r'\s([^\s]+)\,\sБеларусь', 1)) \
        .withColumn('Street', regexp_extract('Адрес:', r'(.+)\s\d', 1)) \
        .withColumn('Building', regexp_extract('Адрес:', r'\d{2}', 0)) \
        .withColumn('Address', concat(col('City'), lit(','), col('Street'), lit(','), col('Building'))) \
        .withColumn('Телефон:', regexp_replace('Телефон:', ' ', '')) \
        .withColumn('telephone1', regexp_extract('Телефон:', r'\+\d{3}\d{2}\d{3}\d{4}', 0)) \
        .withColumn('telephone2', regexp_extract('Телефон:', r'\,(\+\d{3}\d{2}\d{3}\d{4})', 1)) \
        .drop('Street', 'Building', 'Телефон:', 'Адрес:')
    return df2


def process_news(centre_news: list, path_embassy: str) -> pyspark.sql.DataFrame:
    with open(path_embassy, 'r', encoding='utf-8') as f:
        embassy_news = json.load(f)[1:]
    news = centre_news + embassy_news
    df = spark.createDataFrame(data=news)
    df2 = df.withColumn('link', regexp_replace('link', r'https?://', '')) \
        .withColumn('date', regexp_replace('date', r'\.', '-')) \
        .withColumn('date', date_format('date', 'dd-MM-yyyy'))
    return df2


if __name__ == '__main__':
    # insert_visa_centre(es,process_vs_info('flask_app\\lithuania_scraper\\jsons\\lithuania_visa_centre.json'))
    # insert_consulates(es,process_embassy_info('flask_app\\lithuania_scraper\\jsons\\embassy_info.json'))
    # insert_news(es, process_news('flask_app\\lithuania_scraper\\jsons\\lithuania_visa_centre_news.json',
    #                              'flask_app\\lithuania_scraper\\jsons\\embassy_news.json'))
    # print_info('visa_centre')
    # print(get_news())
    # print_info('news')
    insert_visa_centre(es, process_vs_info(parse_visa_centre()))
    #insert_consulates(es, process_embassy_info('flask_app\\lithuania_scraper\\jsons\\embassy_info.json'))
    insert_news(es, process_news(get_visa_centres_news(), 'flask_app\\lithuania_scraper\\jsons\\embassy_news.json'))
