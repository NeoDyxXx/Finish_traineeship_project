from elasticsearch import Elasticsearch

def check_index_exist(es, index_name):
    res = es.indices.exists(index=index_name)
    return res

es = Elasticsearch([{'host': 'locathost', 'port': 9200, 'scheme': "http"}])
if not check_index_exist(es, "appointment"):
    print('not')