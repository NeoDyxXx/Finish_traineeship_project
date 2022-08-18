from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout
from retry import retry


class EsController:
    def __init__(self):
        self.es = EsController.create_es_connection()
        self.indices = ["consulate", "visaac", "news"]

    @staticmethod
    @retry(
        exceptions=(ConnectionError, ConnectionTimeout),
        delay=5,
    )
    def create_es_connection():
        es = Elasticsearch("http://elasticsearch:9200")

        # raise exception if connection doesn't exist
        es.info()
        return es

    def add_data(self, index, id, data):
        try:
            self.es.index(index=index, id=id, document=data)
        except Exception:
            return []

    def get_all_index_data(self, index):
        try:
            result = self.es.search(index=index, body={"query": {"match_all": {}}})
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception:
            return []

    def get_data_by_id(self, index, id):
        try:
            result = self.es.get(index=index, id=id)
            return result["_source"]
        except Exception:
            return []

    def get_data_by_field(self, index, value):
        try:
            result = self.es.search(
                index=index,
                body={
                    "query": {
                        "match": {
                            "address": value,
                        }
                    }
                },
            )
            return [hit["_source"] for hit in result["hits"]["hits"]]
        except Exception:
            return []

    def update_data(self, index, data):
        pass

    def delete_index(self, index):
        try:
            self.es.delete(index=index)
        except:
            return
