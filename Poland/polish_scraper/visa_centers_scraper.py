import requests

from base_scraper import BaseScraper
from typing import List


class ViseCentersScraper(BaseScraper):

    def __init__(self, language, dest_country, country):
        super().__init__('countryLocation', language, dest_country, country)

    def get_json_response(self) -> dict:
        payload = {
            'content_type': self._content_type,
            'fields.title[match]': f'{self._dest_country} > {self._country} > {self._language}',
            'order': 'fields.vacName',
            'limit': '200'
        }

        return requests.get(self.url, params=payload, headers=self.headers).json()

    def get_data(self) -> List[dict]:
        items = self.get_json_response()
        visa_centers = [item['fields'] for item in items['items']]
        cities = [visa_center['vacName'] for visa_center in visa_centers]
        opening_hours = [visa_center['openingHoursObject'] for visa_center in visa_centers]
        vacaddresses = [
            visa_center['address']['content'][0]['content'][0]['value'].strip('{ }')
            for visa_center in visa_centers
        ]
        addresses = self.__get_addresses(vacaddresses)

        centers_data = [{
            'city': city,
            'address': address,
            'email': None,
            'apply_working_hours_1': hours[0]['day'] + ', ' + hours[0]['hours'],
            'issue_working_hours_2': hours[1]['day'] + ', ' + hours[1]['hours'],
            'phone_number': None,
            'country': 'Poland'
        } for city, hours, address in zip(cities, opening_hours, addresses)]

        return centers_data

    def __get_addresses(self, vacaddresses: List[str]) -> List[str]:
        payload = {
            'content_type': 'resourceGroup',
            'fields.locale': (f'vfs&{self._language}&{self._dest_country}&{self._dest_country} '
                              f'> {self._language}&{self._dest_country} > {self._country}'
                              f'&{self._dest_country} > {self._country} > {self._language}'),
            'limit': 500
        }

        response = requests.get(self.url, params=payload, headers=self.headers)
        resources = response.json()['items'][4]['fields']['resources']
        addresses = [resources[vacaddress] for vacaddress in vacaddresses]
        return addresses
