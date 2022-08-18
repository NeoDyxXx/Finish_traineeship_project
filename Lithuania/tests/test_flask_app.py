import requests
import unittest


class FlaskTest(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/lithuania/api'
    DOCS_URL = f'{URL}/docs'
    VISA_CENTRE_URL = f'{URL}/visa-centre'
    EMBASSY_URL = f'{URL}/embassy'

    def test_1_get_api_docs(self):
        response = requests.get(self.DOCS_URL)
        self.assertEqual(response.status_code, 200)

    def test_2_get_visa_centre_error(self):
        response = requests.get(self.VISA_CENTRE_URL)
        self.assertEqual(response.status_code, 404)

    def test_3_get_visa_centre_info(self):
        response = requests.get(f'{self.VISA_CENTRE_URL}/info')
        self.assertEqual(response.status_code, 200)

    def test_4_get_visa_centre_news(self):
        response = requests.get(f'{self.VISA_CENTRE_URL}/news')
        self.assertEqual(response.status_code, 200)

    def test_5_get_visa_centre_no_content(self):
        response = requests.get(f'{self.VISA_CENTRE_URL}/q')
        self.assertEqual(response.status_code, 204)

    def test_6_get_embassy_error(self):
        response = requests.get(self.EMBASSY_URL)
        self.assertEqual(response.status_code, 404)

    def test_7_get_embassy_info(self):
        response = requests.get(f'{self.EMBASSY_URL}/info')
        self.assertEqual(response.status_code, 200)

    def test_8_get_embassy_news(self):
        response = requests.get(f'{self.EMBASSY_URL}/news')
        self.assertEqual(response.status_code, 200)

    def test_9_get_embassy_no_content(self):
        response = requests.get(f'{self.EMBASSY_URL}/q')
        self.assertEqual(response.status_code, 204)

