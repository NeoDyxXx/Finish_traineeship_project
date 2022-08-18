import requests

from base_scraper import BaseScraper
from typing import List


class NewsScraper(BaseScraper):

    def __init__(self, language, dest_country, country):
        super().__init__('countryNews', language, dest_country, country)

    def get_json_response(self) -> dict:
        payload = {
            'content_type': self._content_type,
            'fields.locale': (f'{self._dest_country} > {self._country} > {self._language}'
                              f'&{self._dest_country} > {self._language}'),
            'fields.permanent': 'true'
        }

        return requests.get(self.url, params=payload, headers=self.headers).json()

    def get_data(self) -> List[dict]:
        data = self.get_json_response()
        all_news = [item['fields'] for item in data['items']]
        contents = [
            news['intro']['content'][0]['content'][0]['value'] for news in all_news
        ]
        dates = [news['date'] for news in all_news]
        urls = [
            f'https://visa.vfsglobal.com/{self._country}/{self._language}/{self._dest_country}/news/' + news['slug']
            for news in all_news
        ]

        news_data = [{
            'date': date,
            'title': content.strip()[:50],
            'body': content.strip(),
            'link': url
        } for date, content, url in zip(dates, contents, urls)]

        return news_data
