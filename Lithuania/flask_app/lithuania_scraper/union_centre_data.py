# -*- coding: utf-8 -*-
from Lithuania.flask_app.lithuania_scraper.visa_centre_scraper import get_visa_centre
from Lithuania.flask_app.lithuania_scraper.visa_centre_news_scraper import get_visa_centres_news
import json
import os


def union_visa_centre_data():
    visa_centre = get_visa_centre()
    news = get_visa_centres_news()
    with open(os.path.join('jsons', "union_visa_centre_data.json"), 'w') as f:
        json.dump({'visa-centre': visa_centre['Список'], 'visa-centre-news': news}, f, ensure_ascii=False)


if __name__ == '__main__':
    union_visa_centre_data()