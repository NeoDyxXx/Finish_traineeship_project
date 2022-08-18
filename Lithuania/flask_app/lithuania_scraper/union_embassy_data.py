# -*- coding: utf-8 -*-
from Lithuania.flask_app.lithuania_scraper_embassy.get_news import parse, get_clean_news, get_news
from Lithuania.flask_app.lithuania_scraper_embassy.get_info import get_data, get_embassy
import json

URL = 'https://by.mfa.lt/by/ru/'


def union_embassy_data():
    embassy = get_embassy(get_data(parse(f'{URL}/konsul-jskaaa-iformatsiaa')))
    news = get_clean_news(get_news(parse(f'{URL}/news')))
    with open('union_embassy_data.json', 'w') as f:
        json.dump({'info': embassy, 'news': news}, f, ensure_ascii=False)


if __name__ == '__main__':
    union_embassy_data()
