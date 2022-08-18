from flask import Flask, render_template
import psycopg2
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Ui_swagger"
    }
)


def get_db_connection():
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host='database',
        port='5432'
    )

    cur = conn.cursor()

    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)

    return conn


conn = get_db_connection()


def populate(conn):
    cur = conn.cursor()
    with open('db.sql', 'r') as sql_file:
        cur.execute(sql_file.read())
    conn.commit()


def select_all(table_name, country):
    cur = conn.cursor()
    try:
        cur.execute(f"select id from country where name like '{country}'")
    except:
        pass
    try:
        country_id = cur.fetchall()[0][0]
    except:
        country_id = ""
    print("id", country_id)
    try:
        cur.execute(
            f'select * from {table_name} where country_id = {country_id} ')
        data = cur.fetchall()
    except:
        data = []
    print(data)
    cur.close()
    return data


app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# ////////////// Latvia //////////////


@app.route('/latvia')
def latvia():
    return render_template('latvia.html')


@app.route('/latvia/viscentr')
def latvia_visacent():
    visa_cents = select_all("visa_application_centre", "latvia")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/latvia/embassy')
def latvia_embassy():
    embassy = select_all("consulate", "latvia")
    return render_template('embassy.html', seq=embassy)

# ////////////// Norway //////////////


@app.route('/norway')
def norway():
    return render_template('norway.html')


@app.route('/norway/viscentr')
def norway_visacent():
    visa_cents = select_all("visa_application_centre", "norway")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/norway/embassy')
def norway_embassy():
    embassy = select_all("consulate", "norway")
    return render_template('embassy.html', seq=embassy)


# ////////////// Poland //////////////

@app.route('/poland')
def poland():
    return render_template('poland.html')


@app.route('/poland/viscentr')
def poland_visacent():
    visa_cents = select_all("visa_application_centre", "poland")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/poland/embassy')
def poland_embassy():
    embassy = select_all("consulate", "poland")
    return render_template('embassy.html', seq=embassy)


# ////////////// Lithuania //////////////

@app.route('/lithuania')
def lithuania():
    return render_template('lithuania.html')


@app.route('/lithuania/viscentr')
def lithuania_visacent():
    visa_cents = select_all("visa_application_centre", "lithuania")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/lithuania/embassy')
def lithuania_embassy():
    embassy = select_all("consulate", "lithuania")
    return render_template('embassy.html', seq=embassy)


# ////////////// Thailand //////////////

@app.route('/thailand')
def thailand():
    return render_template('thailand.html')


@app.route('/thailand/viscentr')
def thailand_visacent():
    visa_cents = select_all("visa_application_centre", "thailand")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/thailand/embassy')
def thailand_embassy():
    embassy = select_all("consulate", "Latvia")
    return render_template('embassy.html', seq=embassy)


# ////////////// Spain //////////////

@app.route('/spain')
def spain():
    return render_template('spain.html')


@app.route('/spain/viscentr')
def spain_visacent():
    visa_cents = select_all("visa_application_centre", "spain")
    return render_template('visa_centr.html', seq=visa_cents)


@app.route('/spain/embassy')
def spain_embassy():
    embassy = select_all("consulate", "spain")
    return render_template('embassy.html', seq=embassy)


if __name__ == "__main__":
    # populate(con)
    print(select_all("visa_application_centre", "latvia"))
    app.run(host="0.0.0.0", port=5000)
    # app.run(host="0.0.0.0", port=5000, debug=True)
