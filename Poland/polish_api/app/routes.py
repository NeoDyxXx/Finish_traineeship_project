from app import app
from .es_crud import ES_CRUD


@app.route("/api/consulates")
def get_consulates():
    consulates = ES_CRUD.get_all('consulate')

    results = {'consulates': [
        {
            'country': consulate['country'],
            'address': consulate['address'],
            'email': consulate['email'],
            'working_hours': consulate['working_hours'],
            'phone_number_1': consulate['phone_number_1'],
            'phone_number_2': consulate['phone_number_2']
        } for consulate in consulates]
    }
    return results


@app.route("/api/consulate/<int:id>")
def get_consulate_by_id(id):
    consulate = ES_CRUD.get_by_id('consulate', id)

    result = {
        'country': consulate['country'],
        'address': consulate['address'],
        'email': consulate['email'],
        'working_hours': consulate['working_hours'],
        'phone_number_1': consulate['phone_number_1'],
        'phone_number_2': consulate['phone_number_2']
    }
    return result


@app.route("/api/consulates/<city>")
def get_consulates_by_city(city):
    consulates = ES_CRUD.get_by_city('consulate', city)

    results = {f'consulates from {city}': [
        {
            'country': consulate['country'],
            'address': consulate['address'],
            'email': consulate['email'],
            'working_hours': consulate['working_hours'],
            'phone_number_1': consulate['phone_number_1'],
            'phone_number_2': consulate['phone_number_2']
        } for consulate in consulates]
    }
    return results


@app.route("/api/vac")
def get_visa_centers():
    visa_centers = ES_CRUD.get_all('visaac')

    results = {'visa_centers': [
        {
            'country': visa_center['country'],
            'address': visa_center['address'],
            'email': visa_center['email'],
            'apply_working_hours_1': visa_center['apply_working_hours_1'],
            'issue_working_hours_1': visa_center['issue_working_hours_2'],
            'phone_number': visa_center['phone_number']
        } for visa_center in visa_centers]
    }
    return results


@app.route("/api/vac/<city>")
def get_visa_centers_by_city(city):
    visa_centers = ES_CRUD.get_by_city('visaac', city)

    results = {f'visa_centers from {city}': [
        {
            'country': visa_center['country'],
            'address': visa_center['address'],
            'email': visa_center['email'],
            'apply_working_hours_1': visa_center['apply_working_hours_1'],
            'issue_working_hours_1': visa_center['issue_working_hours_2'],
            'phone_number': visa_center['phone_number']
        } for visa_center in visa_centers]
    }
    return results


@app.route("/api/news")
def get_news():
    all_news = ES_CRUD.get_all('news')

    results = {'news': [
        {
            'date': news['date'],
            'title': news['title'],
            'body': news['body'],
            'link': news['link']
        } for news in all_news]
    }
    return results


@app.route("/api/vac_and_consulates")
def get_visa_centers_and_consulates():
    results = {
        'visa centers info': get_visa_centers(),
        'consulates info': get_consulates()
    }
    return results


@app.route("/api/vac_and_consulates/<city>")
def get_visa_centers_and_consulates_by_city(city):
    results = {
        'visa centers': get_visa_centers_by_city(city),
        'consulates': get_consulates_by_city(city)
    }
    return results


@app.route("/api/all_data")
def get_all_data():
    results = {
        'consulates info': get_consulates(),
        'news': get_news(),
        'visa centers info': get_visa_centers()
    }
    return results
