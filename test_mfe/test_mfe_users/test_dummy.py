from djangosanetesting.cases import DatabaseTestCase
from django.test import LiveServerTestCase
from selenium import webdriver

class TestDummy(LiveServerTestCase):


	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()	
	
	def test_dumm(self):
		pass