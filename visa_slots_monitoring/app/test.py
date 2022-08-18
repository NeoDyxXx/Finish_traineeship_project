
import psycopg2


def get_from_db(country):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host='localhost',
        port='5432'
    )

    cur = conn.cursor()

    cur.execute("SELECT id FROM country WHERE name = '{}'".format(country))
    county_id = cur.fetchone()

    print(county_id)


    cur.execute("SELECT vac_id FROM visa_application_centre WHERE country_id={}".format(county_id[0]))
    visa_application_centre_id = cur.fetchall()
    string = ''
    for id in visa_application_centre_id:
        cur.execute('''SELECT DISTINCT c.name as CATEGORY, a.date, sc.name as SUBCAT 
                        FROM category c INNER JOIN sub_category sc ON c.id=sc.category_id
                        INNER JOIN appointment a ON a.subcat_id=sc.id WHERE a.vac_id={}'''.format(id[0]))
        res_str = cur.fetchall()
        print(res_str)
        cur.execute("SELECT address FROM visa_application_centre WHERE id={}".format(id[0]))
        visa_application_centre = cur.fetchone()
        res_json = {"visa_application_centre": visa_application_centre[0]}
        print(res_json)

    return string

get_from_db('Austria')