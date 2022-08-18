from flask import Flask, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from es.EsController import EsController

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

CONSULATE = "consulate"
VISA_CENTER = "visaac"
NEWS = "news"

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "testip_api"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


REQUEST_KEYS = {
    "news": "NEWS_DETAILS",
    "consulate": "CONSULATE",
    "visa-centre": "VISA_APPLICATION_CENTRE",
}


@app.route("/Thailand/<index>/", methods=["GET"])
def get_index_data(index):
    data = es_controller.get_all_index_data(index)
    response = {f"{index}": data} if data else {"error": "Not found"}
    return jsonify(response)


@app.route("/Thailand/<index>/<string:city>", methods=["GET"])
def get_index_data_by_field(index, city):
    data = es_controller.get_data_by_field(index, city)
    response = {f"{index}_in_{city}": data} if data else {"error": "Not found"}
    return jsonify(response)


@app.route("/Thailand/<index>/<int:id>", methods=["GET"])
def get_index_data_by_id(index, id):
    data = es_controller.get_data_by_id(index, id)
    response = {f"{index}.{id}": data} if data else {"error": "Not found"}
    return jsonify(response)


@app.route("/Thailand/cons_visaac/", methods=["GET"])
def get_consulates_and_visa_centers():
    cons = es_controller.get_all_index_data(CONSULATE)
    visaac = es_controller.get_all_index_data(VISA_CENTER)
    response = (
        {"data": {"cons": cons, "visaac": visaac}}
        if cons and visaac
        else {"error": "Not found"}
    )
    return jsonify(response)


@app.route("/Thailand/cons_visaac_by_city/<city>", methods=["GET"])
def get_consulates_and_visa_centers_by_city(city):
    cons = es_controller.get_data_by_field(CONSULATE, city)
    visaac = es_controller.get_data_by_field(VISA_CENTER, city)
    response = (
        {f"cons_in_{city}": cons, f"visaac_in_{city}": visaac}
        if cons and visaac
        else {"error": "Not found"}
    )
    return jsonify(response)


@app.route("/Thailand/all_data/", methods=["GET"])
def get_all_data():
    cons = es_controller.get_all_index_data(CONSULATE)
    visaac = es_controller.get_all_index_data(VISA_CENTER)
    news = es_controller.get_all_index_data(NEWS)
    response = (
        {"data": {"cons": cons, "visaac": visaac, "news": news}}
        if cons and visaac and news
        else {"error": "Not found"}
    )
    return jsonify(response)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    es_controller = EsController()
    app.run(debug=True, host="0.0.0.0")
