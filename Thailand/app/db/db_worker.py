from sqlalchemy import create_engine
from sqlalchemy import text
import time
import datetime
from elasticsearch import Elasticsearch

# get and transfor data from DB to JSON
def db_selector(table):
    time.sleep(5)
    db = create_engine("postgresql://SV:db_sv123@db/test_db")
    res = db.execute(
        text(
            f"SELECT column_name from information_schema.columns where table_name = '{table}'"
        )
    )
    columns = list()
    for i in res:
        print(i)
        columns.append(i[0])

    columns = tuple(columns)
    print(columns)
    res = db.execute(text(f"SELECT * FROM {table}"))
    response_data = list()
    for i in res:
        data = {}
        for index, val in enumerate(i):
            data[f"{columns[index]}"] = val
        response_data.append(data)

    return response_data


# check if this data exist in DB
def check_data(func):
    def wrap(*args):
        db, table, fields, values = args
        res = db.execute(text(f"SELECT * FROM {table}"))
        for i in res:
            if values == i[1:] or i[1] == "Thailand":
                return
            if type(i[-1]) == datetime.datetime:
                date = values[:-2]
                date = date[8:]
                if date == i[-1].strftime("%Y-%m-%d"):
                    return
        func(db, table, fields, values)

    return wrap


# insert data in DB
@check_data
def insert(db, table, fields, values):
    fields = str(fields).replace("'", "")
    sql = text(f"INSERT INTO {table} {fields} VALUES{values}")
    db.execute(sql)


def factory(data, db):
    data_keys = list(data.keys())
    insert(db, "COUNTRY", "(NAME)", "('Thailand')")

    # id страны получаем
    COUNTRY_ID_sql = db.execute(text("SELECT ID FROM COUNTRY WHERE NAME='Thailand'"))
    COUNTRY_ID = None

    for i in COUNTRY_ID_sql:
        COUNTRY_ID = i[0]

    for key in data_keys:
        if key == "NEWS_DETAILS":
            news = data[key]
            for item in news:
                fields = list(item.keys())
                values = list(item.values())

                fields.pop()
                date = values.pop()
                insert(db, key, tuple(fields), tuple(values))

                res = db.execute(
                    f"SELECT ID FROM NEWS_DETAILS WHERE LINK='{values[-1]}'"
                )
                news_detaild_id = None
                for i in res:
                    news_detaild_id = i[0]
                insert(
                    db,
                    "NEWS",
                    "(COUNTRY_ID, NEWS_ID, DATE)",
                    f"({COUNTRY_ID}, {news_detaild_id}, '{date}')",
                )
        else:
            fields = (f"COUNTRY_ID",) + tuple(data[key].keys())
            values = (COUNTRY_ID,) + tuple(data[key].values())
            insert(db, key, fields, values)


def db_worker(data):
    time.sleep(5)
    db = create_engine("postgresql://SV:db_sv123@db/test_db")
    factory(data, db)
