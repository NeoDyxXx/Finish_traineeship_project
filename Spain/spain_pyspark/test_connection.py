from elasticsearch import Elasticsearch, helpers

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])
res = es.indices.exists(index='news')
print(res)