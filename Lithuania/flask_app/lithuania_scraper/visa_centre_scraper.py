import json
import os
import requests

import lithuania_scraper.params_for_scraper as params_for_scraper


def parse_info_visa_centre() -> dict:
    response = requests.get(params_for_scraper.LINK, headers=params_for_scraper.headers,
                            params=params_for_scraper.address_params, verify=False)
    data = response.json()
    phone = data['items'][4]['fields']['resources']['contactus.phonenumber1']
    email = data['items'][4]['fields']['resources']['contactus.emailaddress2']
    info = dict()
    info["Страна"] = "Литва"
    info["Телефон"] = phone
    info["Email"] = email
    return info


def parse_visa_centre() -> list:
    response_address = requests.get(params_for_scraper.LINK, headers=params_for_scraper.headers,
                                    params=params_for_scraper.address_params,
                                    verify=False)
    address_data = response_address.json()

    response_time = requests.get(params_for_scraper.LINK, headers=params_for_scraper.headers,
                                 params=params_for_scraper.time_params, verify=False)
    time_data = response_time.json()

    minsk_address = {'Город': 'Минск',
                     'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.minsk']}
    gomel_address = {'Город': 'Гомель',
                     'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.gomel']}
    mogilev_address = {'Город': 'Могилев',
                       'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.mogilev']}
    vitebsk_address = {'Город': 'Витебск', 'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.vitebsk']}
    brest_address = {'Город': 'Брест',
                     'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.brest']}
    baranovichi_address = {'Город': 'Барановичи',
                           'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.baranovichi']}
    pinsk_address = {'Город': 'Пинск',
                     'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.pinsk']}
    grodno_address = {'Город': 'Гродно', 'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.grodno']}
    lida_address = {'Город': 'Лида',
                    'Адрес': address_data['items'][4]['fields']['resources']['vacaddress.lida']}

    for town in time_data['items']:
        if town['fields']['vacName'] == 'Минск':
            minsk_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            minsk_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Гомель':
            gomel_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            gomel_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Могилев':
            mogilev_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            mogilev_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Витебск':
            vitebsk_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            vitebsk_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Брест':
            brest_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            brest_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Барановичи':
            baranovichi_address['Apply_working_hours'] = " ".join(
                list(town['fields']['openingHoursObject'][0].values()))
            baranovichi_address['Issue_working_hours'] = " ".join(
                list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Пинск':
            pinsk_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            pinsk_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Гродно':
            grodno_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            grodno_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))
        if town['fields']['vacName'] == 'Лида':
            lida_address['Apply_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][0].values()))
            lida_address['Issue_working_hours'] = " ".join(list(town['fields']['openingHoursObject'][1].values()))

    visa_centre = [minsk_address, gomel_address, mogilev_address, vitebsk_address, brest_address, baranovichi_address,
                   pinsk_address, grodno_address, lida_address]

    info = parse_info_visa_centre()

    for town in visa_centre:
        town['Сountry'] = info['Страна']
        town['Phone_number'] = info['Телефон']
        town['Email'] = info['Email']

    return visa_centre


# --- to json ---

def write_visa_centres_json():
    visa_centres = dict()
    visa_centres['Список'] = parse_visa_centre()
    with open(os.path.join('jsons', "lithuania_visa_centre.json"), "w") as f:
        json.dump(visa_centres, f, ensure_ascii=False)


def get_visa_centres_json() -> dict:
    with open(os.path.join('jsons', "lithuania_visa_centre.json"), "r") as f:
        visa_centres = json.load(f)
    return visa_centres


def get_visa_centre() -> dict:
    visa_centres = dict()
    visa_centres['Список'] = parse_visa_centre()
    return visa_centres

#
if __name__ == '__main__':
    print(parse_visa_centre())