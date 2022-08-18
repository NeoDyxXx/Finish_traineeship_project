# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import requests
import re
import json
import cfscrape


es = Elasticsearch('http://localhost:9200')
scraper = cfscrape.create_scraper()

def parse(url):
    """parse data from given url and return an html-page"""
    try:
        page = scraper.get(url)
    except TimeoutError:
        print('Url is unavailable')
        return False
    parser = BeautifulSoup(page.content, 'html.parser')
    return parser


def get_data(parser):
    """Return a data as keys and values from html page"""
    is_key = True
    keys = []
    values = []
    if parser == False:
        return [keys, values]
    data = parser.find_all('td')
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans(escapes, ' ' * len(escapes))
    for each in data:
        if is_key:
            keys.append(each.text.translate(translator).strip().title())
            is_key = False
        else:
            values.append(' '.join(each.text.split()))
            is_key = True
    return [keys, values]


def clean_up(values):
    email = 3
    time_embassy = 4
    time_consular_sectiom = 5
    comtacts_consular_sectiom = 6
    important = 7
    attention = 8
    values[email] = re.sub(r'\[email.+\]', '', values[email])
    values[time_embassy] = values[time_embassy].replace('IV', ' Четверг ').replace('I', ' Понедельник ').replace('V',
                                                                                                                 ' Пятница ')
    values[time_consular_sectiom] = values[time_consular_sectiom].replace('IV', ' Четверг ').replace('II',
                                                                                                     ' Вторник ').replace(
        'I', ' Понедельник ').replace('V', ' Пятница ')
    values[comtacts_consular_sectiom] = values[comtacts_consular_sectiom].replace('Тел:', '')
    values[important] = re.sub(r'.ON-LINE.', 'ONLINE', values[important])
    values[attention] = re.sub(r'или обращаться.+', '', values[attention])


def get_res(data):
    info_dict = {}
    keys, values = data
    if keys == []:
        print('Program can not parse the data, use json that you saved before')
        with open('flask_app\\lithuania_scraper\\jsons\\embassy_info.json','r',encoding='utf-8') as f:
            info = json.load(f)
            return info
    clean_up(values)
    info = [{"Страна": "Литва", "Тип": "Посольство"}]
    for pos in range(0, 9):
        info_dict[keys[pos]] = values[pos]
    info.append(info_dict)
    return info


def main():
    url = 'https://by.mfa.lt/by/ru/konsul-jskaaa-iformatsiaa'
    return get_res(get_data(parse(url)))


if __name__ == '__main__':
    print(main())
