from typing import List

from bs4 import BeautifulSoup
import requests


class ConsulatesScraper:
    def __init__(self):
        self.url = 'http://catalogpl.by/infa/99-posolstva-i-konsul-stva-polshi.html'

    def get_list_data(self) -> List[List[str]]:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'lxml')
        items = soup.find('div', class_='newsitem_text').find_all('ul')
        consulates = list(map(lambda item: item.text.strip(), items))
        return [embassy.split('\n') for embassy in consulates]

    def parse_data(self):
        consulates = self.get_list_data()
        return [{
            'address': consulate[1].split(':', maxsplit=1)[1].strip().rstrip('.'),
            'phone': consulate[2].split(':', maxsplit=1)[1].replace(' ', ' ').strip().rstrip('.'),
            'working hours': consulate[3].split(':', maxsplit=1)[1].strip().rstrip('.'),
            'working hours for get a visa':
                consulate[4].split(':', maxsplit=1)[1].strip().rstrip('.'),
            'working hours for delivery of docs': consulate[5].split(':', maxsplit=1)[1].strip().rstrip('.')
        } for consulate in consulates]

    def get_data(self) -> List[dict]:
        consulates = self.parse_data()

        return [
            {
                'address': consulate['address'],
                'email': None,
                'working_hours': consulate['working hours'],
                'phone_number_1': consulate['phone'].split(',')[0],
                'phone_number_2': consulate['phone'].split(',')[1] if
                len(consulate['phone'].split(',')) > 1 else None,
                'country': 'Poland'
            }
            for consulate in consulates]
