from to_db import get_id, check_info


def embassy_info_from_json(path):
    """get info from json and edit it"""

    import json
    import re
    res = []
    info = {}
    with open(path, 'r', encoding='utf-8') as f:
        res_json = json.load(f)
    country_info = res_json[0]
    for embassy_info in res_json[1:]:
        info['country_id'] = country_info['Страна']
        info['adress'] = embassy_info['Адрес:']
        info['email'] = ''
        info['working_hours'] = embassy_info['Время Работы Посольства:'].strip()
        phone_numbers = re.findall(r'\+\d{3}\s\d{2}\s\d{3}\s\d{4}', embassy_info['Телефон:'])
        info['phone_number_1'] = phone_numbers[0]
        info['phone_number_2'] = phone_numbers[1]
        res.append(info.copy())
    return res


def get_embassy_info_values(conn):
    """check in info should be inserted"""
    cur = conn.cursor()
    sql = 'select * from consulate'
    cur.execute(sql)
    return cur.fetchall()


def insert_info(conn):
    """insert embassy info into table"""

    path = 'lithuania_scraper\\jsons\\embassy_info.json'
    info_array = embassy_info_from_json(path)
    db_values = get_embassy_info_values(conn)
    for info in info_array:
        if check_info(info, db_values):
            id = get_id(conn, info['country_id'])
            keys = ','.join(tuple(info.keys()))
            values = tuple(info.values())[1:]
            sql = f'insert into consulate ({keys}) values ({id},%s,%s,%s,%s,%s)'
            cur = conn.cursor()
            cur.execute(sql, values, )
        else:
            break
    conn.commit()
