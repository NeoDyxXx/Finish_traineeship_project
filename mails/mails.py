from elasticsearch import Elasticsearch, helpers
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time



def mail():
    load_dotenv()
    es_pw = os.environ.get("elastic_password")

    mail_login = os.environ.get("mail_login")
    mail_pw = os.environ.get("mail_password")

    # for advertisements
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

    # for users
    client = Elasticsearch(
        cloud_id='Nikita:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmMDNkNTM2NjZlZDc0ODg0OTZhNThmMjUxMGE0MDJkYSQwNGQzODU4ZDVlYTA0MTkxYmIxZjY4YmUwOGUxNmIxYQ==',
        http_auth=('elastic', 'EEekFX8RuRgffcR4QsD0tT4C')
    )

    users = client.search(index="mailing")

    for user in users['hits']['hits']:

        if 'Courses' in user['_source']['type_mailing']:
            report = "\n"

            body = {
                "size": 100,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "country": user['_source']['country']
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "exists": {
                                    "field": user['_source']['user']
                                }
                            }
                        ]
                    }
                }
            }
            courses = es.search(index="courses", body=body)

            language = {"poland": "Польский", "latvia": "Латышский", "lithuania": "Литовский", "spain": "Испанский",
                        "norway": "Норвежский"}

            for course in courses['hits']['hits']:
                report += '''
                    Начните изучать {} язык!
                     Уровень - {}.
                    Цена для Вас {}
                    Зарегистрируйтесь здесь {}
                '''.format(language[course["_source"]['country']], course["_source"]['level'], course["_source"]['price'],
                           course["_source"]['url'])
                es.update(index="courses", id=course["_id"], doc={user['_source']['user']: 'true'})
                es.indices.refresh(index="courses")

            if (courses['hits']['total']['value'] == 0):
                report = 'No courses updates for ' + user['_source']['user']
                print(report)
            else:
                msg = EmailMessage()
                msg.set_content(report)

                print(report)

                msg['Subject'] = language[courses['hits']['hits'][0]["_source"]['country']] + ' язык. Курсы для Вас'
                msg['From'] = mail_login
                msg['To'] = [user['_source']['user']]

                server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
                server.login(mail_login, mail_pw)
                server.send_message(msg)
                server.quit()

                print('sent to ' + user['_source']['user'])

        if 'Air tickets' in user['_source']['type_mailing']:
            datetime_now = datetime.now().strftime("%d.%m.%y")
            report = "\n"
            body = {
                "size": 100,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "country": user['_source']['country']
                                }
                            },
                            {
                                "range": {
                                    "departure_date": {
                                        "gte": datetime_now
                                    }
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "exists": {
                                    "field": user['_source']['user']
                                }
                            }
                        ]
                    }
                }
            }
            tickets = es.search(index="tickets", body=body)
            print(tickets['hits']['total']['value'])
            check = 0
            for ticket in tickets['hits']['hits']:
                tickets_doc = ticket['_source']

                report += '''
                    {} билет!
                    {} --> {}.
                    Вылет: {} {} {}
                    Прибытие: {} {} {}
                    Время в пути {}
                    Стоимость: {}
                    Покупайте здесь - {}
                '''.format(tickets_doc['ticket_type'], tickets_doc["departure_city"],
                           tickets_doc["arrival_city"],
                           tickets_doc["departure_time"], tickets_doc["departure_day"],
                           tickets_doc["departure_date"],
                           tickets_doc["arrival_time"], tickets_doc["arrival_day"],
                           tickets_doc["departure_date"],
                           tickets_doc["travel_time"], tickets_doc["cost"], tickets_doc["url"]
                           )
                check += 1
                res = es.update(index="tickets", id=ticket["_id"], doc={user['_source']['user']: 'true'})
                es.indices.refresh(index="tickets")
            report += "\nХорошего полёта, Ваш Aviasales."

            if (tickets['hits']['total']['value'] == 0):
                report = 'No tickets updates for ' + user['_source']['user']
                print(report)
            else:
                msg = EmailMessage()
                msg.set_content(report)

                print(report)

                msg['Subject'] = 'Авиабилеты в ' + tickets['hits']['hits'][0]["_source"]['country']
                msg['From'] = mail_login
                msg['To'] = [user['_source']['user']]

                server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
                server.login(mail_login, mail_pw)
                server.send_message(msg)
                server.quit()

                print ('sent to '+ user['_source']['user'])


# mail()

schedule.every().day.at("00:00").do(mail)

while True:
    schedule.run_pending()
    time.sleep(1)

