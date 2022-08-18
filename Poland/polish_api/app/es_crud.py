from . import app


class ES_CRUD:
    @staticmethod
    def add_to_index(index, item):
        if not app.elasticsearch:
            return
        app.elasticsearch.index(index=index, id=item['id'], document=item)

    @staticmethod
    def remove_index(index):
        if not app.elasticsearch:
            return
        app.elasticsearch.delete(index=index)

    @staticmethod
    def get_by_id(index, id):
        if not app.elasticsearch:
            return
        search = app.elasticsearch.get(index=index, id=id)
        return search['_source']

    @staticmethod
    def get_by_city(index, city):
        if not app.elasticsearch:
            return []
        search = app.elasticsearch.search(index=index, body={
            'query':
                {
                    'match':
                        {
                            'address': city,
                        }
                }
        })

        return [hit['_source'] for hit in search['hits']['hits']]

    @staticmethod
    def get_all(index):
        if not app.elasticsearch:
            return []
        search = app.elasticsearch.search(index=index, body={
            'query':
                {
                    'match_all': {}
                }
        })

        return [hit['_source'] for hit in search['hits']['hits']]

