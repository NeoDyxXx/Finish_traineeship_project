import unittest

from app import create_app
import requests


class TestPages(unittest.TestCase):
	def setUp(self):
		self.app = create_app()

	def test_app(self):
		assert self.app is not None


	def test1(self):
		r = requests.get('http://127.0.0.1:5000/')
		assert r.status_code == 200

	def test2(self):
		r = requests.get('http://127.0.0.1:5000/to-file')
		assert r.status_code == 200

	def test3(self):
		r = requests.get('http://127.0.0.1:5000/visa-center')
		assert r.status_code == 200

	def test4(self):
		assert requests.get('http://127.0.0.1:5000/news').status_code == 200

	def test5(self):
		assert requests.get('http://127.0.0.1:5000/news_in_file').status_code == 200




if __name__ == '__main__':
	unittest.main()