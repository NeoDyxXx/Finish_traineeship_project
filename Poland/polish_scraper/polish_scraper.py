from news_scraper import NewsScraper
from visa_centers_scraper import ViseCentersScraper
from consulates_scraper import ConsulatesScraper


class PolishScraper:
    def __init__(self, language='ru', dest_country='pol', country='blr'):
        self.visa_centers = ViseCentersScraper(language, dest_country, country)
        self.news = NewsScraper(language, dest_country, country)
        self.consulates = ConsulatesScraper()

    def get_visa_centers(self):
        return self.visa_centers.get_data()

    def get_news(self):
        return self.news.get_data()

    def get_consulates(self):
        return self.consulates.get_data()
