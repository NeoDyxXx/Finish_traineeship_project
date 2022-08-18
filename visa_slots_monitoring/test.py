import psycopg2
from time import sleep
import time
import random

from sqlalchemy import create_engine

def init_db():
    print('int_db')
    conn = psycopg2.connect(dbname='postgres',
                            user='postgres',
                            password='postgres',
                            host='5432',)

    print('connect')
    cursor = conn.cursor()
    print('cursor')
    cursor.execute('SELECT * FROM appointment')
    print('execute')


if __name__ == '__main__':

    db_name = 'postgres'
    db_user = 'postgres'
    db_pass = 'postgres'
    db_host = 'db'
    db_port = '5432'

    db_string = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
    print(db_string)
    db = create_engine(db_string)

    db.execute('SELECT * FROM appointment')

    while True:
        try:
            print('start')
            init_db()
        except Exception as e:
            print(e)
            sleep(10)
            continue

