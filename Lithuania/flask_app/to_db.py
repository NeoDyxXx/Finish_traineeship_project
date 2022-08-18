from embassy_to_db import insert_info
from visa_centre_to_db import insert_visa_info
from news_to_db import insert_news_details


def config(filename='database.ini', section='postgresql'):
    """Parse config file"""

    from configparser import ConfigParser
    parser = ConfigParser()
    try:
        parser.read(filename)
    except FileNotFoundError:
        print(f'File {filename} not found')
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def get_conn():
    """ Connect to the PostgreSQL database server """

    import psycopg2
    params = config()
    try:
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_id(conn, country_name):
    """get id of country by its name"""

    sql = f'select id from country where name = %s'
    cur = conn.cursor()
    cur.execute(sql, (country_name,))
    res = cur.fetchone()
    if res:
        return res[0]
    else:
        sql = 'insert into country (name) values (%s) returning id'
        cur.execute(sql, (country_name,))
        id = cur.fetchone()[0]
        conn.commit()
        return id


def check_info(info, db_values):
    if db_values:
        for row in db_values:
            if row[2:] == tuple(info.values())[1:]:
                return False
    return True


def insert():
    conn = get_conn()
    insert_info(conn)
    insert_visa_info(conn)
    insert_news_details(conn)


if __name__ == '__main__':
    insert()
