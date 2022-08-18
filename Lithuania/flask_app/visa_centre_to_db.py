from to_db import get_id, check_info


def visa_info_from_json(path):
    import json
    res = []
    info = {}
    with open(path, 'r', encoding='utf-8') as f:
        res_json = json.load(f)
    country_info = res_json['Список'][0]['Сountry']

    for visa_info in res_json['Список']:
        info['country_id'] = country_info
        info['adress'] = visa_info['Адрес']
        info['email'] = visa_info['Email']
        info['apply_working_hours_1'] = visa_info['Apply_working_hours']
        info['issue_working_hours_2'] = visa_info['Issue_working_hours']
        info['phone_number'] = visa_info['Phone_number']
        res.append(info.copy())
    return res


def get_visa_info_values(conn):
    """check in info should be inserted"""
    cur = conn.cursor()
    sql = 'select * from visa_application_centre'
    cur.execute(sql)
    return cur.fetchall()


def insert_visa_info(conn):
    """insert visa info into table"""
    path = 'lithuania_scraper\\jsons\\lithuania_visa_centre.json'
    info_array = visa_info_from_json(path)
    db_values = get_visa_info_values(conn)
    for info in info_array:
        if check_info(info, db_values):
            id = get_id(conn, info['country_id'])
            keys = ','.join(tuple(info.keys()))
            values = tuple(info.values())[1:]
            sql = f'insert into visa_application_centre ({keys}) values ({id},%s,%s,%s,%s,%s)'
            cur = conn.cursor()
            cur.execute(sql, values, )
        else:
            break
    conn.commit()
