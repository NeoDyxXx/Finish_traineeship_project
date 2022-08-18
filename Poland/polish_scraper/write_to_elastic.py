import os
from polish_scraper import PolishScraper
from elasticsearch import Elasticsearch


class Writer:
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://elasticsearch:9200'
    scraper = PolishScraper()

    elasticsearch = Elasticsearch(ELASTICSEARCH_URL) \
        if ELASTICSEARCH_URL else None

    def add_to_index(self, index, item):
        if not self.elasticsearch:
            return
        self.elasticsearch.index(index=index, id=item['id'], document=item)

    def add_consulates_to_elasticsearch(self):
        consulates = self.scraper.get_consulates()
        for i in range(1, len(consulates) + 1):
            consulates[i - 1]['id'] = i
            self.add_to_index('consulate', consulates[i - 1])

    def add_visa_centers_to_elasticsearch(self):
        visa_centers = self.scraper.get_visa_centers()
        for i in range(1, len(visa_centers) + 1):
            visa_centers[i - 1]['id'] = i
            self.add_to_index('visaac', visa_centers[i - 1])

    def add_news_to_elasticsearch(self):
        all_news = self.scraper.get_news()

        for i in range(1, len(all_news) + 1):
            all_news[i - 1]['id'] = i
            self.add_to_index('news', all_news[i - 1])
