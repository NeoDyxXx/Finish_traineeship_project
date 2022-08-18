import requests
import json
import os


def get_info_site(url: str):
    r = requests.get(url)
    return r.text


def create_correct_data(json_data):
    data = json.loads(json_data)
    list_of_news = data['data']['stories']
    result_data = []

    for news in list_of_news:
        currect_item = {
            'image': news['docs'][0]['image'],
            'sourceName': news['docs'][0]['sourceName'],
            'title': "".join([item['text'] for item in news['docs'][0]['title']]),
            'description': "".join([item['text'] for item in news['docs'][0]['text']]),
            'url': news['docs'][0]['url'],
            'time': news['docs'][0]['time']
        }

        result_data.append(currect_item)

    return result_data


def save_in_file(result_data: dict):
    if not os.path.isdir('json_data'):
        os.mkdir('json_data')

    os.chdir('json_data')
    last_index = -1

    for _, _, filenames in os.walk("."):
        for filename in filenames:
            if "json_data" in filename:
                if last_index < int(filename.split("json_data")[1].split(".json")[0]):
                    last_index = int(filename.split("json_data")[1].split(".json")[0])

    with open("json_data" + str(last_index + 1) + ".json", 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False)

    os.chdir('..')


if __name__ == '__main__':
    data1 = create_correct_data(get_info_site('https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси'))
    data2 = create_correct_data(get_info_site('https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))

    save_in_file(data1)
    save_in_file(data2)