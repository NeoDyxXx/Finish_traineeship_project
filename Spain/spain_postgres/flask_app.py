from flask import Flask, jsonify
import serv
from flask_swagger_ui import get_swaggerui_blueprint
from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Spain App'
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

import psycopg2
from psycopg2 import Error

connection = psycopg2.connect(user="nina",
                                  password="nina",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="mydb")

# connection = psycopg2.connect(user="test_user",
#                                   password="secret",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="test_db")

cursor = connection.cursor()

es_pw = 'jq+bhLm5UJvlRadXWkHw'
client = Elasticsearch("http://elastic:{}@localhost:9200".format(es_pw))

@app.route("/")
def index():
    return (
        """
            <a class="button" href="/swagger">Swagger</a><br>
            <a class="button" href="/api/visa-center">Info about visa center</a><br>
            <a class="button" href="/api/to-file">Visa center to file</a><br>
            <a class="button" href="/api/news">News</a><br>
            <a class="button" href="/api/news_in_file">News to file</a><br>
            <br>
            <a class="button" href="/api/create_country">Create table country</a><br>
            <a class="button" href="/api/add_country">Fill table country</a><br>
            <a class="button" href="/api/get_country">Show table country</a><br>
            <br>
            <a class="button" href="/api/create_vc">Create table visa_application_centre</a><br>
            <a class="button" href="/api/add_vc">Fill table visa_application_centre</a><br>
            <a class="button" href="/api/get_vc">Show table visa_application_centre</a><br>
            <br>
            <a class="button" href="/api/any_new_info">Update table visa_application_centre if it's needed</a><br>
            <br>
            <a class="button" href="/api/create_news_function">Create news function</a><br>
            <a class="button" href="/api/create_news_and_news_details">Create table news</a><br>
            <a class="button" href="/api/add_news_and_news_details">Fill table news and news_details</a><br>
            <a class="button" href="/api/get_news">Show table news</a><br>
            <a class="button" href="/api/get_news_details">Show table news_details</a><br>
            <br>
            <a class="button" href="/api/drop_vc">Drop table visa_application_centre</a><br>
            <a class="button" href="/api/drop_country">Drop table country</a><br>
            <a class="button" href="/api/drop_news_and_news_details">Drop news and news_details tables</a><br>
            <br>
            <a class="button" href="/api/index_vc">Create index visaac</a><br>
            <a class="button" href="/api/visa_to_es">Write visa centres to Elasticsearch</a><br>
            <a class="button" href="/api/all_visa_from_es">Get all visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/one_visa_from_es">Get certain (id = 1) visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/visa_from_es">Get <b>Spain</b> visa centres from Elasticsearch</a><br>
            <a class="button" href="/api/minsk_visa_from_es">Get visa centres <b>located in Minsk</b> from Elasticsearch</a><br>
            <a class="button" href="/api/delete_visa_from_es">Delete index visaac</a><br>
            <br>
        """
    )

@app.route("/api/to-file")
def to_file():
    all_centres = serv.create_file()
    return (
        "<p>{}</p>"
        "<p>wrote to file</p>".format(all_centres)
    )

@app.route("/api/visa-center")
def visa_center():
    center = serv.read_visa_center()
    return jsonify(center)

@app.route("/api/news", methods=['POST', 'GET'])
def news():
    return jsonify(serv.create_correct_data(
        serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))
            )


@app.route("/api/news_in_file", methods=["POST", "GET"])
def news_in_file():
    serv.save_in_file(serv.create_correct_data(
        serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))
            )
    return "<h3>File save</h3>"

@app.route("/api/create_country", methods=["POST", "GET"])
def create_country():
    sql = '''create table if not exists country (
    id 		serial primary key,
    name 	varchar(50) unique not null
    );'''
    cursor.execute(sql)
    connection.commit()
    return ('country created')

@app.route("/api/add_country", methods=["POST", "GET"])
def add_country():
    ret = serv.fill_country("Испания")
    return ret

@app.route("/api/get_country", methods=["POST", "GET"])
def get_country():
    sql = '''select * from country;'''
    cursor.execute(sql)
    return str(cursor.fetchall())

@app.route("/api/create_vc", methods=["POST", "GET"])
def create_visa_cen():
    sql = '''create table if not exists visa_application_centre (
                id 						serial primary key,
                country_id 				int not null,
                adress 					varchar(200),
                email 					varchar(70),
                apply_working_hours_1 	varchar(100),
                issue_working_hours_2	varchar(100),
                phone_number 			varchar(20),
                foreign key(country_id) references country(id)
                );'''
    cursor.execute(sql)
    connection.commit()
    return ('visa_application_centre created')

@app.route("/api/add_vc", methods=["POST", "GET"])
def add_visa_cen():
    center = serv.read_visa_center()
    ret = serv.fill_vc(center[0])
    return ret

@app.route("/api/get_vc", methods=["POST", "GET"])
def get_visa_cen():
    sql = '''select * from visa_application_centre;'''
    cursor.execute(sql)
    return "<br>".join([str(item) for item in list(cursor.fetchall())])


@app.route("/api/create_news_function")
def create_news_function():
    try:
        sql = '''create type news_t as (description text, image text, sourceName varchar(100), time text, title text, url text);'''
        cursor.execute(sql)
    except:
        connection.rollback()

    sql = '''CREATE OR REPLACE FUNCTION select_from_json (doc text)
            RETURNS TABLE (title varchar(70), body varchar(150), link varchar(100), date timestamp) AS
            $BODY$ 
                    select substring(title for 70)::varchar(70) as title, concat(substring(description for 147), '...')::varchar(150) as body, substring(url for 100)::varchar(100) as link, 
                    to_timestamp(concat(substring(time for 10), ' ', substring(time from 14 for 19)), 'dd.mm.yyyy hh24:mi') as date from json_populate_recordset(null::news_t, doc::json)
            $BODY$
            LANGUAGE 'sql';'''
    cursor.execute(sql)

    sql = '''create or replace procedure insert_data(doc text)
            LANGUAGE plpgsql
            AS $BODY$
            DECLARE
                curr cursor for select * from select_from_json(doc);
                i_nd int;
                i_n int;
                id_country int;
                counter int;

                title_t varchar(70);
                body_t varchar(150);
                link_t varchar(100);
                date_t timestamp;
            BEGIN
                open curr;
                select COALESCE(max(id), 0) into i_nd from news_details;
                i_nd := i_nd + 1;

                select COALESCE(max(id), 0) into i_n from news;
                i_n := i_n + 1;

                select id into id_country from country where name = 'Испания';

                loop
                    fetch curr into title_t, body_t, link_t, date_t;
                    IF NOT FOUND THEN EXIT; END IF;

                    select count(*) into counter from news_details
                    where title = title_t;

                    IF counter > 0 then
                        begin
                            update news_details set body = body_t, link = link_t
                            where title = title_t;
                        end;
                    else
                        begin
                            insert into news_details values(i_nd, title_t, body_t, link_t);
                            insert into news values(i_n, id_country, i_nd, date_t);
                        end;
                    end if;

                    i_n := i_n + 1;
                    i_nd := i_nd + 1;
                end loop;

                close curr;
            END;
            $BODY$;'''
    cursor.execute(sql)
    connection.commit()

    return ('function added')


@app.route("/api/create_news_and_news_details")
def create_news():
    sql = '''create table if not exists news_details (
            id 		serial primary key,
            title 	varchar(70),
            body 	varchar(150),
            link 	varchar(100)
        );'''

    cursor.execute(sql)

    sql = '''create table if not exists news (
            id 				serial primary key,
            country_id 		int not null,
            news_details_id int not null,
            date 			timestamp,
            foreign key (country_id) 		references country (id),
            foreign key (news_details_id)	references news_details (id)
        );'''

    cursor.execute(sql)

    connection.commit()
    return ('news and news_details tables created')

@app.route("/api/add_news_and_news_details")
def add_news_and_news_details():
    print()

    sql = 'call insert_data(\'' + serv.create_str_of_json(serv.create_correct_data(
        serv.get_info_site1(
            'https://newssearch.yandex.ru/news/search?ajax=0&from_archive=1&neo_parent_id=1647441873582156-81607431716702717200156-production-news-app-host-112-NEWS-NEWS_NEWS_SEARCH&p=2&text=испанский+визовый+центр+в+Беларуси',
            'https://newssearch.yandex.ru/news/search?from_archive=1&p=1&text=испанский+визовый+центр+в+Беларуси&ajax=1&neo_parent_id=1647442457082880-358481777924388487800157-production-news-app-host-130-NEWS-NEWS_NEWS_SEARCH'))).replace('\'', '\"') + '\');'

    cursor.execute(sql)
    connection.commit()

    return ('added')

@app.route("/api/get_news")
def get_news():
    sql = '''select * from news;'''
    cursor.execute(sql)
    return "<br>".join([str(item) for item in list(cursor.fetchall())])

@app.route("/api/get_news_details")
def get_news_details():
    sql = '''select * from news_details;'''
    cursor.execute(sql)
    return "<br>".join([str(item) for item in list(cursor.fetchall())])

@app.route("/api/drop_vc")
def drop_vc():
    sql = 'drop table if exists visa_application_centre;'
    cursor.execute(sql)
    connection.commit()
    return ('visa_application_centre deleted')

@app.route("/api/drop_country")
def drop_country():
    sql = 'drop table if exists country;'
    cursor.execute(sql)
    connection.commit()
    return ('country deleted')

@app.route('/api/drop_news_and_news_details')
def drop_news_and_news_details():
    sql = 'drop table if exists news;'
    cursor.execute(sql)

    sql = 'drop table if exists news_details;'
    cursor.execute(sql)

    connection.commit()
    return ('tables deleted')

@app.route("/api/any_new_info")
def check_new():
    all_centres = serv.create_file()
    ch = False
    for i in range(len(all_centres)):
        sql = '''select id from country where name='{}';'''.format(all_centres[i]["Страна"])
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        sql = '''select adress, email, apply_working_hours_1, issue_working_hours_2, phone_number 
                from visa_application_centre vc join country c 
                on vc.country_id=c.id where c.name='{}';'''.format(all_centres[i]["Страна"])
        cursor.execute(sql)
        stat = cursor.fetchall()[i]
        if (str(stat[0]) != all_centres[i]["Адрес"]):
            ch = True
            sql = '''update visa_application_centre set adress='{}' 
                where country_id={}'''.format(all_centres[i]["Адрес"], id)
            cursor.execute(sql)
            connection.commit()
        if (str(stat[1]) != all_centres[i]["почта"]):
            ch = True
            sql = '''update visa_application_centre set email='{}' 
                            where country_id={}'''.format(all_centres[i]["почта"], id)
            cursor.execute(sql)
            connection.commit()
        if (str(stat[2]) != all_centres[i]["Время выдачи паспортов"]):
            ch = True
            sql = '''update visa_application_centre set apply_working_hours_1='{}' 
                                        where country_id={}'''.format(all_centres[i]["Время выдачи паспортов"], id)
            cursor.execute(sql)
            connection.commit()
        if (str(stat[3]) != all_centres[i]["Время приема"]):
            ch = True
            sql = '''update visa_application_centre set issue_working_hours_2='{}' 
                                        where country_id={}'''.format(all_centres[i]["Время приема"], id)
            cursor.execute(sql)
            connection.commit()
        if (str(stat[4]) != all_centres[i]["Тел"]):
            ch = True
            sql = '''update visa_application_centre set phone_number='{}' 
                                        where country_id={}'''.format(all_centres[i]["Тел"], id)
            cursor.execute(sql)
            connection.commit()
    if (ch == True):
        return ("Info updated.")
    else:
        return ("No updates there.")

@app.route("/api/index_vc")
def index_vc():
    client.indices.create(index='visaac')
    client.indices.close(index='visaac')
    settings = '''
        {
            "analysis": {
              "analyzer": {
                "rebuilt_keyword": {
                  "tokenizer": "keyword",
                  "filter": [ "word_delimiter" ]
                }
              }
            }
        }
        '''
    client.indices.put_settings(index="visaac", body=settings)
    client.indices.open(index='visaac')
    return "Index visaac created."

@app.route("/api/visa_to_es")
def visa_to_es():
    center = serv.read_visa_center()

    for i in range(len(center)):

        body = {}
        body['analyzer'] = 'rebuilt_keyword'
        body['text'] = center[i]['Адрес']
        tokens = client.indices.analyze(index="visaac", body=body)
        index = tokens['tokens'][1]['token']

        body = {}
        body['analyzer'] = 'whitespace'
        body['text'] = center[i]['Адрес']
        tokens = client.indices.analyze(index="visaac", body=body)
        exclude_token = {1}
        address = ''
        for tok in range(len(tokens['tokens'])):
            if tok not in exclude_token:
                address += tokens['tokens'][tok]['token'] + ' '

        doc = {}
        doc['country'] = center[i]['Страна']
        doc['address'] = address
        doc['index'] = index
        doc['email'] = center[i]['почта']
        doc['issue_worktime'] = center[i]['Время выдачи паспортов']
        doc['apply_worktime'] = center[i]['Время приема']
        doc['telephone1'] = center[i]['Тел'].replace(" ", "")
        client.index(index="visaac", id=i+1, document=doc)

    client.indices.refresh(index="visaac")
    return "Wrote to Elastic."

@app.route("/api/all_visa_from_es")
def all_visa_from_es():
    resp = client.search(index="visaac")
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:

        body = {}
        body['analyzer'] = 'rebuilt_keyword'
        body['text'] = hit["_source"]['address']
        tokens = client.indices.analyze(index="visaac", body=body)
        city = tokens['tokens'][0]['token']

        body = {}
        body['analyzer'] = 'whitespace'
        body['text'] = hit["_source"]['address']
        tokens = client.indices.analyze(index="visaac", body=body)
        address = ''
        for tok in range(1, len(tokens['tokens'])):
            address += tokens['tokens'][tok]['token'] + ' '

        country = hit["_source"]['country']
        index = hit["_source"]['index']
        email = hit["_source"]['email']
        issue_worktime = hit["_source"]['issue_worktime']
        apply_worktime = hit["_source"]['apply_worktime']
        telephone1 = hit["_source"]['telephone1']

        report += "<br>Country: " + country + "<br>City: " + city + "<br>Address: " + address \
                + "<br>Index: " + index + "<br>Email: " + email + "<br>Issue worktime: " + issue_worktime \
                + "<br>Apply worktime: " + apply_worktime + "<br>Phone: " + telephone1 + "<br><br>"
    return str(report)

@app.route("/api/one_visa_from_es")
def one_visa_from_es():
    id = 1
    query = {
        "terms": {
            "_id": [id]
        }
    }
    resp = client.search(index="visaac", query=query)
    return str(resp['hits']['hits'][0]['_source'])

@app.route("/api/visa_from_es")
def visa_from_es():
    country = 'Испания'
    query = {
        "match": {
            "country": country
        }
    }
    resp = client.search(index="visaac", query=query)
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:
        report += str(hit['_source']) + "<br>"
    return report

@app.route("/api/minsk_visa_from_es")
def minsk_visa_from_es():
    city = 'минск'
    query = {
        "match": {
            "address": city
        }
    }
    resp = client.search(index="visaac", query=query)
    report = "Got %d Hits:" % resp['hits']['total']['value'] + "<br><br>"
    for hit in resp['hits']['hits']:
        report += str(hit['_source']) + "<br>"
    return report

@app.route("/api/delete_visa_from_es")
def delete_visa_from_es():
    client.indices.delete(index='visaac')
    return "Index visaac deleted."


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
    #app.run(host='0.0.0.0', debug=True)
