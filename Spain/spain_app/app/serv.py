import json
from bs4 import BeautifulSoup
import requests
import os
# from flask_app import connection, cursor

from app import db, CountryModel, VisaCenterModel

url = 'https://blsspain-belarus.com/contact.php'
url2 = 'https://blsspain-russia.com/moscow/contact.php'

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
                info[rows[1].text] = rows[2].text
                info[rows[3].text] = rows[4].text

            elif (rows[0].text == "Адрес"):
                # address = rows[1].text.replace('\n\t', '')
                address = rows[1].text
                info['Адрес'] = address

            else:
                info[rows[0].text] = rows[1].text

        all_centres.append(info)

    return all_centres

def collect_info_data2(html):
    all_centres2 = []

    soup = BeautifulSoup(html, 'lxml')

    center = soup.find('table', class_='table')


    info = {}

    country_and_type = center.find('th')
    # if country_and_type is None:
    #     break
    country_and_type = country_and_type.text.split(' ')

    info["Страна"] = country_and_type[2][:-1:] + "я"
    info["Тип"] = country_and_type[0] + ' ' + country_and_type[1]

    parts = center.find('td').find_all('div', class_='marginBottom')

    for part in parts:
        rows = part.find_all('div', class_='row')
        if (rows[0].text == "Режим работы:"):
            info["Время приема"] = rows[2].text
            info["Время выдачи паспортов"] = rows[4].text

        elif (rows[0].text == "Адрес:"):
            # address = rows[1].text.replace('\n\t', '').replace('г. ', '')[:77:]
            address = rows[1].text
            info['Адрес'] = address

        elif (rows[0].text == "Адрес электронной почты:"):
            address = rows[1].text
            info['почта'] = address

        elif (rows[0].text == "Тел:"):
            # phone = rows[1].text.replace(' (', '').replace(') ', '').replace('-', '')
            phone = rows[1].text
            info['Тел'] = phone

        else:
            info[rows[0].text] = rows[1].text

    all_centres2.append(info)

    return all_centres2


def visa_center_to_file(all_centres):
    with open("data_spain.json", "w", encoding="utf-8") as file:
        json.dump(all_centres, file, ensure_ascii=False)

def visa_center_to_file2(all_centres2):
    with open("data_spain_moscow.json", "w", encoding="utf-8") as file:
        json.dump(all_centres2, file, ensure_ascii=False)

def read_visa_center():
    with open("data_spain.json", "r", encoding="utf-8") as file:
        text = json.load(file)
    return text

def read_visa_center2():
    with open("data_spain_moscow.json", "r", encoding="utf-8") as file:
        text = json.load(file)
    return text

def create_file():
    html = get_info_site(url)
    all_centres = collect_info_data(html)
    visa_center_to_file(all_centres)
    return all_centres

def create_file2():
    html = get_info_site(url2)
    all_centres2 = collect_info_data2(html)
    visa_center_to_file2(all_centres2)
    return all_centres2


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

###############################################################################

def add_country(country):
    new_country = CountryModel(name=country)
    db.session.add(new_country)
    db.session.commit()
    return new_country

def add_vc(vc):
    id_add = db.session.query(CountryModel.id).filter(CountryModel.name == vc["Страна"])
    new_vc = VisaCenterModel(country_id=id_add, address=vc["Адрес"], email=vc["почта"], apply_working_hours=vc["Время приема"],
                             issue_working_hours=vc["Время выдачи паспортов"], phone_number=vc["Тел"])
    db.session.add(new_vc)
    db.session.commit()


#################################################

def fill_country(country):
    sql = '''insert into country (name) values ('{}');'''.format(country)
    cursor.execute(sql)
    connection.commit()
    return ('country {} added'.format(country))

def fill_vc(info_array):
    sql = '''select id from country where name='{}';'''.format(info_array["Страна"])
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    # sql = '''insert into visa_application_centre (country_id, adress, email,
    #     apply_working_hours_1, issue_working_hours_2, phone_number)
    #     values ({}, '{}', '{}', '{}', '{}', '{}');'''.format(id, info_array['Адрес'], info_array['почта'],
    #     info_array['Время выдачи паспортов'], info_array['Время приема'], info_array['Тел'])
    sql = '''insert into visa_application_centre (country_id, adress, email, 
            apply_working_hours_1, issue_working_hours_2, phone_number)
            select {country_id}, '{adress}', '{email}', '{apply_working_hours_1}', '{issue_working_hours_2}', '{phone_number}'
            where not exists (select * from visa_application_centre where 
            adress='{adress}' and email='{email}' and apply_working_hours_1='{apply_working_hours_1}'
            and issue_working_hours_2='{issue_working_hours_2}' and phone_number='{phone_number}');'''.format(country_id=id,
            adress=info_array['Адрес'], email=info_array['почта'], apply_working_hours_1=info_array['Время выдачи паспортов'],
            issue_working_hours_2=info_array['Время приема'], phone_number=info_array['Тел'])
    cursor.execute(sql)
    connection.commit()
    return ('info about {} visa center added'.format(info_array["Страна"]))

def create_str_of_json(json_data):
    result_str = '[\n'

    for item in json_data:
        print(item)
        result_str += '{\n'
        for key, value in item.items():
            result_str += '\t\"{0}\": \"{1}\",'.format(key.replace('\'', '').replace('\"', ''), value.replace('\'', '').replace('\"', ''))
        result_str = result_str[:-1]
        result_str += '},\n'
    
    result_str = result_str[:-2]
    result_str += ']'

    return result_str


