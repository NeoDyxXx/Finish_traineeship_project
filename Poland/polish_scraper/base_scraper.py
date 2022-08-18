from abc import abstractmethod


class BaseScraper:

    headers = {
        'Authorization': 'Bearer 5YpTBRikGN59YHwM18CyGr5F43bFuaak9U8FSMEDmb8'
    }
    url = 'https://d2ab400qlgxn2g.cloudfront.net/dev/spaces/xxg4p8gt3sg6/environments/master/entries?'

    def __init__(self, content_type, language, dest_country, country):
        self._content_type = content_type
        self._language = language
        self._dest_country = dest_country
        self._country = country

    @abstractmethod
    def get_json_response(self):
        pass

    @abstractmethod
    def get_data(self):
        pass
