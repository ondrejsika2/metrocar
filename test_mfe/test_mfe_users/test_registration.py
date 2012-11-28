# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from selenium import webdriver
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from selenium.webdriver.common.keys import Keys
from metrocar.user_management.models import MetrocarUser

class TestRegistration(LiveServerTestCase):


	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
	
	def test_registration(self):
		self.browser.get(self.live_server_url + '/registrace/')
		headings = self.browser.find_elements_by_tag_name('h1')			
		self.assertEquals(headings[1].text, 'Registrace')
		username_field = self.browser.find_element_by_id('id_username')
		username_field.send_keys('testUser')
		password_field = self.browser.find_element_by_id('id_password')
		password_field.send_keys('password')
		password_confirm_field = self.browser.find_element_by_id('id_password2')
		password_confirm_field.send_keys('password')
		first_name_field = self.browser.find_element_by_id('id_first_name')
		first_name_field.send_keys('Pokusny')
		last_name_filed = self.browser.find_element_by_id('id_last_name')
		last_name_filed.send_keys('Uzivatel')
		email_field = self.browser.find_element_by_id('id_email')
		email_field.send_keys('pokusny@fel.cvut.cz')
		primary_phone_field = self.browser.find_element_by_id('id_primary_phone')
		primary_phone_field.send_keys('123 123456789')
		date_of_birth_field = self.browser.find_element_by_id('id_date_of_birth')
		date_of_birth_field.send_keys('1990-02-09')
		drivers_licence_number_field = self.browser.find_element_by_id('id_drivers_licence_number')
		drivers_licence_number_field.send_keys('123123123')
		identity_card_number_field = self.browser.find_element_by_id('id_identity_card_number')
		identity_card_number_field.send_keys('123123123')
		identity_card_number_field.send_keys(Keys.RETURN)
		succes_value = u"Registrace byla úspěšná. Děkujeme za váš zájem. Jakmile naši administrátoři ověří váš požadavek, bude vám zaslán email."
		
		
		succes = self.browser.find_element_by_css_selector("li[class='success']")
		

		self.assertEquals(succes.text, succes_value)


