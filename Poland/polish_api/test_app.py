from schema import Schema, And
import unittest
import app

BASE_URL = 'http://127.0.0.1:5000/api'
ENDPOINTS = {
    'consulates': '/consulates',
    'vc': '/vc',
    'news': '/news',
    'vc_and_consulates': '/vc_and_consulates',
    'all_data': '/all_data'
}
SCHEMAS = {
    'consulates': Schema([{'address': And(str, len),
                           'phone': And(str, len),
                           'working hours': And(str, len),
                           'working hours for delivery of docs': And(str, len),
                           'working hours for get a visa': And(str, len)}]),
    'news': Schema([{'date': And(str, len),
                     'link': And(str, len),
                     'news': And(str, len)}]),
    'OpeningHoursVC': Schema([{'day': And(str, len),
                               'description': And(str, len),
                               'hours': And(str, len)}])
}
SCHEMAS['vc'] = Schema([{'address': And(str, len),
                         'city': And(str, len),
                         'opening_hours': SCHEMAS['OpeningHoursVC']}])
SCHEMAS['vc_and_consulates'] = Schema({'consulates info': SCHEMAS['consulates'],
                                       'visa centers info': SCHEMAS['vc']})
SCHEMAS['all_data'] = Schema({'consulates info': SCHEMAS['consulates'],
                              'news': SCHEMAS['news'],
                              'visa centers info': SCHEMAS['vc']})


class TestFlaskApp(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app.app.test_client()
        self.app.testing = True

    def test_success(self):
        for e in ENDPOINTS.values():
            response = self.app.get(BASE_URL + e)
            self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        bad_url = BASE_URL + 'not_found'
        response = self.app.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_not_empty(self):
        for e in ENDPOINTS.values():
            response = self.app.get(BASE_URL + e)
            self.assertNotEqual(response.content_length, 0)

    def test_json_content_type(self):
        for e in ENDPOINTS.values():
            response = self.app.get(BASE_URL + e)
            self.assertEqual(response.content_type, 'application/json')

    def test_endpoints_schemas(self):
        for e in ENDPOINTS.keys():
            url = BASE_URL + ENDPOINTS[e]
            schema = SCHEMAS[e]
            data = self.app.get(url).json
            self.assertTrue(schema.is_valid(data))


if __name__ == '__main__':
    unittest.main()
