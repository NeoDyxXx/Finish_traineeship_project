from flask import jsonify
import smtplib
from email.message import EmailMessage
import requests
import schedule
import time
from elasticsearch import Elasticsearch, helpers

# for advertisements
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

# for users
client = Elasticsearch(
    cloud_id='Nikita:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRmMDNkNTM2NjZlZDc0ODg0OTZhNThmMjUxMGE0MDJkYSQwNGQzODU4ZDVlYTA0MTkxYmIxZjY4YmUwOGUxNmIxYQ==',
    http_auth=('elastic', 'EEekFX8RuRgffcR4QsD0tT4C')
)

def format_message(data: dict):
    report = ''
    for key in data.keys():
        if data[key][key] == []:
            report += "В {0} нет мест на запись.\n".format(key)
        else:
            for item in data[key][key]:
                report += "Места на запись в {0}:\n".format(key)
                for key, value in item.items():
                    report += "{0}: {1}\n".format(key, value)
                report += '\n'
    
    return report


def mail():
    login = 'kraynov.kirill2015@yandex.ru'
    pw = 'ciegbfbiiodeggmb'

    report = dict()
    report['Poland'] = requests.get("http://localhost:5050/pol").json()
    report['Latvia'] = requests.get("http://localhost:5050/lva").json()
    report['Lithuania'] = requests.get("http://localhost:5050/ltu").json()
    # report['Spain'] = requests.get("http://localhost:5050/esp").json()
    report['Norway'] = requests.get("http://localhost:5050/nor").json()
    report['Thailand'] = requests.get("http://localhost:5050/tha").json()
    report['Austria'] = requests.get("http://localhost:5050/aut").json()
    report = format_message(report)
    
    users_to_mail = []
    try:
        users = client.search(index="mailing")
        for user in users['hits']['hits']:
            if 'Vacancies for visa application' in user['_source']['type_mailing']:
                users_to_mail.append(user['_source']['user'])
    except:
        print("Not create index in elastic.")
    # users_to_mail.append("kraynov.kirill2015@yandex.ru")

    msg = EmailMessage()
    msg.set_content(report)
    msg['Subject'] = 'Свободные места для записи'
    msg['From'] = login
    msg['To'] = users_to_mail

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(login, pw)
    server.send_message(msg)
    server.quit()

schedule.every().day.at("16:00").do(mail)

while True:
    schedule.run_pending()
    time.sleep(60)

# mail()