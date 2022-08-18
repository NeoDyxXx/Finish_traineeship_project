import json
import os
import requests

import lithuania_scraper.params_for_scraper as params_for_scraper

main_link = 'https://visa.vfsglobal.com/blr/ru/ltu/'


def get_visa_centres_news() -> list:
    response_news_1 = requests.get(params_for_scraper.LINK, headers=params_for_scraper.headers,
                                   params=params_for_scraper.news_params_1,
                                   verify=False)
    news_data_1 = response_news_1.json()
    response_news_2 = requests.get(params_for_scraper.LINK, headers=params_for_scraper.headers,
                                   params=params_for_scraper.news_params_2,
                                   verify=False)
    news_data_2 = response_news_2.json()
    news = []
    for item in news_data_1['items']:
        news.append({'link': main_link + item['fields']['slug'],
                     'title': item['fields']['intro']['content'][0]['content'][0]['value'],
                     'date': item['fields']['date']})

    for item in news_data_2['items']:
        news.append({'link': main_link + item['fields']['slug'],
                     'title': item['fields']['intro']['content'][0]['content'][0]['value'],
                     'date': item['fields']['date']})

    return news


# --- to json ---

def write_news_visa_centres_json():
    visa_centres_news = get_visa_centres_news()
    with open(os.path.join('jsons', "lithuania_visa_centre_news.json"), "w") as f:
        json.dump(visa_centres_news, f, ensure_ascii=False)


def get_news_visa_centres_json() -> list:
    with open(os.path.join('jsons', "lithuania_visa_centre_news.json"), "r") as f:
        visa_centres = json.load(f)
    return visa_centres


if __name__ == '__main__':
    print(get_visa_centres_news())