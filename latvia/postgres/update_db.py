import psycopg2
from config import host, user, password, db_name

def connect_to_db():
    try:
        # connect to existing database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        return connection
    except Exception as _ex:
        print("[INFO] Error while working with postgres")

def create_db_objects(connection):
    #creating objects
    with connection.cursor() as cursor:
        cursor.execute(
            open("db_objects.sql", "r").read()
        )
    connection.commit()


def retrieve_news_json():
    import json
    from datetime import date
    result = []
    result_dict = {}
    with open("../embassy_information.json", 'r', encoding='utf-8') as f:
        retrieve_json = json.load(f)
        news = retrieve_json['news']
        for key in news:
            result_dict['COUNTRY_ID'] = 1
            result_dict['DATE'] = date.today().strftime("%Y-%m-%d")
            result_dict['TITLE'] = key[0:60]
            result_dict['BODY'] = ""
            result_dict['LINK'] = news[key]
            result.append(result_dict.copy())
    return result

def retrieve_consulate_info():
    import json
    result_dict = {}
    result = []
    with open("../consulate_info.json", 'r', encoding='utf-8') as f:
        retrieve_json = json.load(f)
        result_dict['COUNTRY_ID'] = 1
        result_dict['ADRESS'] = retrieve_json['address']
        result_dict['EMAIL'] = ''
        result_dict['WORKING_HOURS'] = retrieve_json['time'][0:100]
        result_dict['PHONE_NUMBER_1'] = retrieve_json['phone']
        result_dict['PHONE_NUMBER_2'] = ''
        result.append(result_dict.copy())
    return result


def retrieve_visa_center():
    import json
    minsk_visa_dict = {}
    vitebsk_data_dict = {}
    result = []
    with open("../latviya_visa_centers_info.json", 'r', encoding='utf-8') as f:
        retrieved_json = json.load(f)
        minsk_visa_dict['COUNTRY_ID'] = 1
        minsk_visa_dict['ADRESS'] = retrieved_json['АДРЕСА ВИЗОВЫХ ЦЕНТРОВ:'].rpartition('В')[0]
        minsk_visa_dict['EMAIL'] = ''
        minsk_visa_dict['APPLY_WORKING_HOURS_1'] = retrieved_json['ГРАФИК РАБОТЫ ВИЗОВЫХ ЦЕНТРОВ:'][0:100]
        minsk_visa_dict['ISSUE_WORKING_HOURS_2'] = ''
        minsk_visa_dict['PHONE_NUMBER'] = retrieved_json['ТЕЛЕФОН:'].rpartition('+')[0][0:16]

        vitebsk_data_dict['COUNTRY_ID'] = 1
        vitebsk_data_dict['ADRESS'] = retrieved_json['АДРЕСА ВИЗОВЫХ ЦЕНТРОВ:'].rpartition('2')[2]
        vitebsk_data_dict['EMAIL'] = ''
        vitebsk_data_dict['APPLY_WORKING_HOURS_1'] = retrieved_json['ГРАФИК РАБОТЫ ВИЗОВЫХ ЦЕНТРОВ:'][0:100]
        vitebsk_data_dict['ISSUE_WORKING_HOURS_2'] = ''
        vitebsk_data_dict['PHONE_NUMBER'] = retrieved_json['ТЕЛЕФОН:'].rpartition('+')[2][0:15]
    result.append(minsk_visa_dict.copy())
    result.append(vitebsk_data_dict.copy())
    return result

def insert_news(connection):
    news_data = retrieve_news_json()
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO 
            news
            (country_id, date)
        VALUES
            (%(COUNTRY_ID)s, %(DATE)s)
    """, news_data)
    connection.commit()

def insert_country(connection):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO 
            country
            (name)
        VALUES
            ('Latvia');
    """)
    connection.commit()

def insert_news_details(connection):
    news_data = retrieve_news_json()
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO 
            news_details
            (title, body, link)
        VALUES
            (%(TITLE)s, %(BODY)s, %(LINK)s)
    """, news_data)
    connection.commit()

def insert_consulate(connection):
    consulate_data = retrieve_consulate_info()
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO 
            consulate
            (country_id, adress, email, working_hours, phone_number_1, phone_number_2)
        VALUES
            (%(COUNTRY_ID)s, %(ADRESS)s, %(EMAIL)s, %(WORKING_HOURS)s, %(PHONE_NUMBER_1)s, %(PHONE_NUMBER_2)s)
    """, consulate_data)
    connection.commit()

def insert_visa_center(connection):
    visa_center_data = retrieve_visa_center()
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO 
            visa_application_centre
            (country_id, adress, email, apply_working_hours_1, issue_working_hours_2, phone_number)
        VALUES
            (%(COUNTRY_ID)s, %(ADRESS)s, %(EMAIL)s, %(APPLY_WORKING_HOURS_1)s, %(ISSUE_WORKING_HOURS_2)s, %(PHONE_NUMBER)s)
    """, visa_center_data)
    connection.commit()

def insert_appointment(connection):
    visa_center_data = retrieve_visa_center()
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO 
            visa_application_centre
            (country_id, adress, email, apply_working_hours_1, issue_working_hours_2, phone_number)
        VALUES
            (%(COUNTRY_ID)s, %(ADRESS)s, %(EMAIL)s, %(APPLY_WORKING_HOURS_1)s, %(ISSUE_WORKING_HOURS_2)s, %(PHONE_NUMBER)s)
    """, visa_center_data)
    connection.commit()

con = connect_to_db()
create_db_objects(con)
insert_country(con)
insert_news_details(con)
insert_news(con)
insert_consulate(con)
insert_visa_center(con)