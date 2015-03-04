# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.utils.django.test import SkipTest

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from metrocar.user_management.models import MetrocarUser


class TestLogin(LiveServerTestCase):
    fixtures = ['user.json', 'user'] # Nefunguje
    fixtures = ['user2.json', 'user2'] # Auch nicht

    def setUp(self):
        try:
            self.browser = webdriver.Firefox()
        except WebDriverException:
            raise SkipTest('unable to start Selenium')
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login(self):

        username = 'test'
        password = 'password'

        user = MetrocarUser.objects.create(username=username)

        user.set_password(password)
        user.password2 = password
        user.first_name = 'Pokusny'
        user.last_name = 'Uzivatel'
        user.email = 'pokusny@fel.cvut.cz'
        user.primary_phone = '123 123456789'
        user.date_of_birth = '1990-02-09'
        user.drivers_licence_number = '123123123'
        user.identity_card_number = '123123123'
        user.language = 'CS'
        user.save()

        self.browser.get(self.live_server_url + '/prihlaseni/')
        headings = self.browser.find_elements_by_tag_name('h1')

        # Podle ./mfe/locale/cs/LC_MESSAGES/django.po
        self.assertEquals(headings[1].text, u"Přihlášení je vyžadováno")

        self.browser.find_element_by_id('j-open-login-box').click()

        username_field = self.browser.find_element_by_id('id_login-username')
        username_field.clear()
        username_field.send_keys('test')
        password_field = self.browser.find_element_by_id('id_login-password')
        password_field.clear()
        password_field.send_keys('password')
        password_field.send_keys(Keys.RETURN)

        # Podle ./mfe/locale/cs/LC_MESSAGES/django.po
        succes_value = u"Byli jste úspěšně přihlášeni."

        # Nas pripad
        succes = self.browser.find_element_by_css_selector("li[class='success']")

        # Otestovani hodnot v detailech - je nutne zadat IDcka u seznamu nebo to prepsat,
        # nebo umi Selenium vyhledavat jenom String fulltextove
        # Neco jako
        # self.assertEquals(self.browser.find_element_by_neco, user.username)
        # popr dalsi

        self.assertEquals(succes.text, succes_value)
