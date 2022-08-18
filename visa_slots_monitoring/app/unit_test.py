import unittest
import requests


class TestPages(unittest.TestCase):
	def setUp(self):
		self.response_visa_center = requests.get(
			"http://127.0.0.1:5050/lva'"
		)
		self.response_embassy = requests.get(
			"http://127.0.0.1:5050/ltu'"
		)
		self.response_consulate = requests.get(
			"http://127.0.0.1:5050/pol'"
		)
		self.response_info = requests.get(
			"http://127.0.0.1:5050/esp'"
		)

		self.response_info = requests.get(
			"http://127.0.0.1:5050/tha'"
		)
		self.response_info = requests.get(
			"http://127.0.0.1:5050/aut'"
		)

	def test1(self):
		assert requests.get('http://127.0.0.1:5050/').status_code == 200

	def test2(self):
		assert requests.get('http://127.0.0.1:5050/lva').status_code == 200

	def test3(self):
		assert requests.get('http://127.0.0.1:5050/ltu').status_code == 200

	def test4(self):
		assert requests.get('http://127.0.0.1:5050/pol').status_code == 200

	def test5(self):
		assert requests.get('http://127.0.0.1:5050/esp').status_code == 200

	def test6(self):
		assert requests.get('http://127.0.0.1:5050/tha').status_code == 200

	def test7(self):
		assert requests.get('http://127.0.0.1:5050/aut').status_code == 200


if __name__ == '__main__':
	unittest.main()
