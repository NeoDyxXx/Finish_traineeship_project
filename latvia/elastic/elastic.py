from elasticsearch import Elasticsearch
import json
from elasticsearch.helpers import scan
import pandas as pd
from time import sleep
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

with open('D:\programming\python\ibaHomeworks\ibaLab\latvia\scrappers\consulate_info.json', 'r', encoding='utf-8') as f:
    visa_centers = json.load(f)
print(visa_centers)

#resp = es.index(index="consulate", document=visa_centers)

def insert_consulate_info(client: Elasticsearch, data):
    try:
        for i, visa_centers in enumerate(data):
            visa_data = dict()
            visa_data['country'] = 'Latvia'
            visa_data['address'] = visa_centers['address']
            visa_data['issue_worktime'] = visa_centers['time']
            visa_data['telephone'] = visa_centers['phone']
            client.index(index='consulate', id=str(i + 1), document=visa_data)
        client.indices.refresh(index='consulate')
        return True
    except:
        return False


with open('D:\programming\python\ibaHomeworks\ibaLab\latvia\scrappers\embassy_information.json', 'r', encoding='utf-8') as f:
    embassy = json.load(f)
print(embassy)

def insert_embassy(client: Elasticsearch, data):
    try:
        for i, embassy in enumerate(data):
            embassy_info = dict()
            embassy_info['country'] = embassy['country']
            embassy_info['address'] = embassy['address']
            embassy_info['phone'] = embassy['phone']
            embassy_info['worktime'] = embassy['worktime']
            client.index(index='embassy', id=str(i + 1), document=embassy_info)
        client.indices.refresh(index='embassy')
        return True
    except:
        return False

insert_consulate_info(es, visa_centers)
insert_embassy(es, embassy)

def get_data_from_elastic():
    query = {
        "query": {
            "match_all": {}
        }
    }

    rel = scan(client=es,
               query=query,
               scroll='1m',
               index='tweets',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)

    # Keep response in a list.
    result = list(rel)

    temp = []

    # We need only '_source', which has all the fields required.
    # This elimantes the elasticsearch metdata like _id, _type, _index.
    for hit in result:
        temp.append(hit['_source'])

    # Create a dataframe.
    df = pd.DataFrame(temp)

    return df

get_data_from_elastic()