
# encoding: utf-8

from django_webtest import WebTest

from metrocar.user_management.models import MetrocarUser


class TestRegistration(WebTest):

    def test_valid_login(self):
        username = 'testUser'
        password = 'password'
        password2 = 'password'
        first_name = 'Pokusny'
        last_name = 'Uzivatel'
        email = 'pokusny@fel.cvut.cz'
        primary_phone = '123 123456789'
        date_of_birth = '1990-02-09'
        drivers_licence_number = '123123123'
        identity_card_number = '123123123'
        language = 'CS'

        page = self.app.get('/registrace/')
        form = page.forms['registration_form']
        form['username'] = username
        form['password'] = password
        form['password2'] = password2
        form['first_name'] = first_name
        form['last_name'] = last_name
        form['email'] = email
        form['primary_phone'] = primary_phone
        form['date_of_birth'] = date_of_birth
        identity_card_number
        form['drivers_licence_number'] = drivers_licence_number
        form['identity_card_number'] = identity_card_number
        form['language'] = language
        form['license_terms'] = 'true'
        
        response = form.submit()

        # Ma tohle bejt 200?
        self.assertEqual(response.status_code, 200)

    def test_invalid_registration(self):
        page = self.app.get('/registrace/')
        form = page.forms['registration_form']
        
        username = 'testUser'
        password = 'password'
        password2 = 'password'
        first_name = 'Pokusny'
        last_name = 'Uzivatel'
        email = 'x'
        primary_phone = '123 123456789'
        date_of_birth = '1990-02-09'
        drivers_licence_number = '123123123'
        identity_card_number = '123123123'
        language = 'CS'
        
        response = form.submit()
        self.assertEqual(response.status_code, 200)

