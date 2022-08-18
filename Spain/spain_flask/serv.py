import json
from bs4 import BeautifulSoup
import requests
import os

url = 'https://blsspain-belarus.com/contact.php'

def get_info_site(url: str):
    r = requests.get(url)
    return r.text


def collect_info_data(html):
    all_centres = []

    soup = BeautifulSoup(html, 'lxml')

    centers = soup.find_all('table', class_='table')

    for center in centers:

        info = {}

        country_and_type = center.find('th')
        if country_and_type is None:
            break
        country_and_type = country_and_type.text.split(' ')

        info["Страна"] = country_and_type[0]
        info["Тип"] = country_and_type[1] + ' ' + country_and_type[2]

        parts = center.find_all('div', class_='marginBottom')

        for part in parts:
            rows = part.find_all('div', class_='row')
            if (rows[0].text == "Часы работы:"):
                info[rows[0].text[:-1:]] = {rows[1].text: rows[2].text,
                                            rows[3].text: rows[4].text}

            elif (rows[0].text == "Адрес"):
                address = rows[1].text.replace('\n\t', '').split(', ')
                info["Город"] = address[0]
                info["Адрес"] = address[2][:-1:] + ', ' + address[3]

            else:
                info[rows[0].text] = rows[1].text

        all_centres.append(info)

    return all_centres

def visa_center_to_file(all_centres):
    with open("data_spain.json", "w", encoding="utf-8") as file:
        json.dump(all_centres, file, ensure_ascii=False)

def read_visa_center():
    with open("data_spain.json", "r", encoding="utf-8") as file:
        text = json.load(file)
    return text

def create_file():
    html = get_info_site(url)
    all_centres = collect_info_data(html)
    visa_center_to_file(all_centres)
    return all_centres


def get_info_site1(*urls):
    return [requests.get(url).text for url in urls]


def create_correct_data(jsons_data):
    result_data = []

    for json_data in jsons_data:
        data = json.loads(json_data)
        list_of_news = data['data']['stories']

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



