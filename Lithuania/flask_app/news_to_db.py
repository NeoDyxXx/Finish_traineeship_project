from to_db import get_id


def news_from_json(path1, path2):
    """get news from json and edit it"""

    import json
    from datetime import datetime

    res = []
    news = {}
    with open(path1, 'r', encoding='utf-8') as f:
        res_json = json.load(f)
    with open(path2, 'r', encoding='utf-8') as f:
        visa_news_json = json.load(f)
    country_info = res_json[0]
    url = 'https://by.mfa.lt/default/ru/'
    for embassy_news in res_json[1:]:
        news['country_id'] = country_info['Страна']
        news['date'] = datetime.strptime(embassy_news['date'], '%Y.%m.%d')
        news['title'] = embassy_news['header'][:149]
        news['body'] = ''
        news['link'] = url + embassy_news['href']
        res.append(news.copy())
    for visa_news in visa_news_json:
        news['country_id'] = country_info['Страна']
        news['date'] = datetime.strptime(visa_news['date'], '%Y-%m-%d')
        news['title'] = visa_news['title'][:149]
        news['body'] = ''
        news['link'] = visa_news['link']
        res.append(news.copy())
    return sorted(res, key=lambda news: news['date'])


def get_news_values(conn):
    """get last news"""
    cur = conn.cursor()
    sql = 'select link from news_details'
    cur.execute(sql)
    return cur.fetchone()


def check_news(link, db_values):
    """check if news should be inserted"""
    if db_values:
        for row in db_values:
            if row == link:
                return False
    return True


def insert_news_details(conn):
    """insert embassy news details into table"""

    path1 = 'lithuania_scraper\\jsons\\embassy_news.json'
    path2 = 'lithuania_scraper\\jsons\\lithuania_visa_centre_news.json'
    news_array = news_from_json(path1, path2)
    db_values = get_news_values(conn)
    for news in news_array:
        if check_news(news['link'], db_values):
            keys_datails = ','.join(tuple(news.keys())[2:])
            values_details = tuple(news.values())[2:]
            sql = f'insert into news_details ({keys_datails}) values (%s,%s,%s) returning id'
            cur = conn.cursor()
            cur.execute(sql, values_details, )
            news_id = cur.fetchone()[0]
            insert_news(conn, news, news_id)
        else:
            break
    conn.commit()


def insert_news(conn, news, news_id):
    """insert embassy and visa_centre news into table"""

    id = get_id(conn, news['country_id'])
    date = news['date']
    values = (id, news_id, date)
    sql = f'insert into news (country_id,news_details_id,date) values (%s,%s,%s)'
    cur = conn.cursor()
    cur.execute(sql, values, )
