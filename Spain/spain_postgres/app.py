from flask import Flask, jsonify
import serv
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from models import db, CountryModel, VisaCenterModel

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

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()

@app.route("/")
def index():
    return (
        """
            <a class="button" href="/swagger">Swagger</a><br>
            <a class="button" href="/api/visa-center">Info about visa center</a><br>
            <a class="button" href="/api/to-file">Visa center to file</a><br>
            <a class="button" href="/api/news">News</a><br>
            <a class="button" href="/api/news_in_file">News to file</a><br>
            <a class="button" href="/api/add_country">Fill table Country</a><br>
            <a class="button" href="/api/get_country">Show table Country</a><br>
            <a class="button" href="/api/add_visa_center">Fill table Visa_Application_Centre</a><br>
            <a class="button" href="/api/get_vc">Show table Visa_Application_Centre</a><br>"""
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

@app.route("/api/add_country")
def fill_country_table():
    new_country = serv.add_country('Испания')
    return (f"Country {new_country.name} has been created successfully.")

@app.route("/api/add_visa_center")
def fill_vc_table():
    spain_vc = serv.read_visa_center()
    for c in spain_vc:
        serv.add_vc(c)
    return (f"Visa center has been created successfully.")

@app.route("/api/get_country")
def get_country():
    countries = CountryModel.query.all()
    results = []
    for country in countries:
        c = {
            "id": country.id,
            "name": country.name,
        }
        results.append(c)
    return str(results)

@app.route("/api/get_vc")
def get_vc():
    vcs = VisaCenterModel.query.all()
    results = []
    for vc in vcs:
        c = {
            "id": vc.id,
            "country_id": vc.country_id,
            "address": vc.address,
            "email": vc.email,
            "apply_working_hours": vc.apply_working_hours,
            "issue_working_hours": vc.issue_working_hours,
            "phone": vc.phone_number,
        }
        results.append(c)
    return str(results)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
    #app.run(host='0.0.0.0', debug=True)
