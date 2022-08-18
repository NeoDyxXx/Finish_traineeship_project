import requests
import unittest


class test_app(unittest.TestCase):
    def setUp(self):
        self.response_visa_center = requests.get(
            "http://127.0.0.1:5000/latvia/visa_center"
        )
        self.response_embassy = requests.get(
            "http://127.0.0.1:5000/latvia/embassy"
        )
        self.response_consulate = requests.get(
            "http://127.0.0.1:5000/latvia/consulate"
        )
        self.response_info = requests.get(
            "http://127.0.0.1:5000/latvia/info"
        )

    def test_index_news(self):
        self.assertEqual(self.response_embassy.status_code, 200)

    def test_index_consulate(self):
        self.assertEqual(self.response_consulate.status_code, 200)

    def test_visa_center(self):
        self.assertEqual(self.response_visa_center.status_code, 200)

    def test_response_info(self):
        self.assertEqual(self.response_info.status_code, 200)


if __name__ == "__main__":
    unittest.main()