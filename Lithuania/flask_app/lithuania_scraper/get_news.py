# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import requests
import json
import os

es = Elasticsearch('http://localhost:9200')

def parse(url):
    """parse data from given url and return an html-page"""
    try:
        page = requests.get(url)
    except TimeoutError:
        print('Url is unavailable')
        return False
    parser = BeautifulSoup(page.text, 'html.parser')
    return parser


def get_news(parser):
    hrefs = []
    headers = []
    dates = []
    URL = 'https://by.mfa.lt/by/ru/'
    if parser == False:
        return [hrefs, headers, dates]
    info = parser.find_all("a", class_="link")
    date = parser.find_all("span", class_="date")
    for each in date:
        dates.append(each.text.replace('Добавлено ', ''))
    for each in info:
        hrefs.append(URL+each.get('href'))
        headers.append(each.text)
    return [hrefs, headers, dates]


def get_res(data):
    news = {}
    hrefs, headers, dates = data
    if hrefs == []:
        print('Program can not parse the data, use json that you saved before')
        with open('flask_app\\lithuania_scraper\\jsons\\embassy_news.json','r',encoding='utf-8') as f:
            news = json.load(f)
        return news
    news_mas = [{"Страна": "Литва", "Тип": "Новости"}]
    for pos in range(0, len(hrefs)):
        news['link'] = hrefs[pos]
        news['title'] = headers[pos]
        news['date'] = dates[pos]
        news_mas.append(news.copy())
    return news


"""def get_clean_news(data):
    news = {}
    list_news = []
    URL = 'https://by.mfa.lt/by/ru/'
    hrefs, headers, dates = data
    if hrefs == []:
        with open(os.path.join('jsons', 'embassy_news.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    for i in range(len(hrefs)):
        news['href'] = URL + hrefs[i]
        news['header'] = headers[i]
        news['date'] = dates[i]
        list_news.append(news.copy())
    return list_news"""


def news_main():
    url = 'https://by.mfa.lt/by/ru/news'
    return get_res(get_news(parse(url)))


if __name__ == '__main__':
    print(news_main())
