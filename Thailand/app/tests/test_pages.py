import requests
import unittest


class Flasktest(unittest.TestCase):
    def setUp(self):
        self.response_visa_center = requests.get(
            "http://127.0.0.1:5000/Thailand/visa-center/"
        )
        self.response_consulate = requests.get(
            "http://127.0.0.1:5000/Thailand/consulate/"
        )
        self.response_news = requests.get("http://127.0.0.1:5000/Thailand/news/")

    def test_index_news(self):
        self.assertEqual(self.response_news.status_code, 200)

    def test_index_consulate(self):
        self.assertEqual(self.response_consulate.status_code, 200)

    def test_visa_center(self):
        self.assertEqual(self.response_visa_center.status_code, 200)

    def test_content_consulate(self):
        self.assertEqual(
            self.response_consulate.headers["content-type"], "application/json"
        )

    def test_content_news(self):
        self.assertEqual(self.response_news.headers["content-type"], "application/json")

    def test_content_visa_center(self):
        self.assertEqual(
            self.response_visa_center.headers["content-type"], "application/json"
        )


if __name__ == "__main__":
    unittest.main()
