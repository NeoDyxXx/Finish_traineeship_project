import json
import os
from autoselenium import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


def get_all_html():
    with Driver('firefox', root='drivers') as driver:
        driver.get('https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси')

        try:
            while True:
                WebDriverWait(driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id=\"neo-page\"]/div/div[1]/div/div[1]/div/div[2]/button"))
                ).click()
        finally:
            html = driver.execute_script("return document.body.innerHTML;")
            driver.quit()
            return html


def parse_html():
    soup: BeautifulSoup = BeautifulSoup(get_all_html(), 'lxml')
    news = soup.find_all('article', class_='news-search-story')
    return list(map(create_data_from_article, news))


def create_data_from_article(html: BeautifulSoup):
    data = dict()

    data['image'] = html.find('img', class_='neo-image').get('src')
    data['sourceName'] = html.find('span', class_='mg-snippet-source-info__agency-name').text
    data['title'] = html.find('div', class_='mg-snippet__title').text
    data['description'] = html.find('span', class_='mg-snippet__text').text
    data['time'] = html.find('span', class_='mg-snippet-source-info__time').text
    data['url'] = html.find('a', class_='mg-snippet__url').get('href')

    return data


def save_in_file(result_data):
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
    save_in_file(parse_html())

