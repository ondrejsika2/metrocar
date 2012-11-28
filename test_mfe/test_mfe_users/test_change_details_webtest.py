# encoding: utf-8


from django_webtest import WebTest
from pyquery import PyQuery


from metrocar.user_management.models import MetrocarUser


class TestDetails(WebTest):

    def test_valid_details(self):
    
        username = 'test'
        password = 'password'
        
        user = MetrocarUser.objects.create(username=username)
 
        user.set_password(password)
        user.password2 = 'password'
        user.first_name = 'Pokusny'
        user.last_name = 'Uzivatel'
        user.email = 'pokusny@fel.cvut.cz'
        user.primary_phone = '123 123456789'
        user.date_of_birth = '1990-02-09'
        user.drivers_licence_number = '123123123'
        user.identity_card_number = '123123123'
        user.language = 'CS'
        user.save()

        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = 'test'
        form['password'] = user.password
        response = form.submit()
        
        # Jak vypada celej response? Jak se k nemu dostat?
        
        self.assertEqual(response.status_code, 200)
        
        # http://webtest.pythonpaste.org/en/latest/#testapp
        # Vnoreny stringy
        
        jQuery = PyQuery(response)
        jQuery('strong').remove()
        
        username = jQuery('[id="li_username"]').text()
        name = jQuery('[id="li_name"]').text()
        date_of_birth = jQuery('[id="li_date_of_birth"]').text()
        language = jQuery('[id="li_language"]').text()
        email = jQuery('[id="li_email"]').text()
        primary_phone = jQuery('[id="li_primary_phone"]').text()
        drivers_licence_number = jQuery('[id="li_drivers_licence_number"]').text()
        

        self.assertEqual(jQuery('#li_username').text(), username)
        self.assertEqual(jQuery('[id="li_name"]').text(), name)
        self.assertEqual(jQuery('[id="li_date_of_birth"]').text(), date_of_birth)
        self.assertEqual(jQuery('[id="li_language"]').text(), language)
        self.assertEqual(jQuery('[id="li_email"]').text(), email)
        self.assertEqual(jQuery('[id="li_primary_phone"]').text(), primary_phone)
        self.assertEqual(jQuery('[id="li_drivers_licence_number"]').text(), drivers_licence_number)


    def test_detail_change(self):
    
        # Nastaveni a ulozeni noveho uzivatele
        
        username = 'test'
        password = 'password'
        
        user = MetrocarUser.objects.create(username=username)
 
        user.set_password(password)
        user.first_name = 'Pokusny'
        user.last_name = 'Uzivatel'
        user.email = 'pokusny@fel.cvut.cz'
        user.primary_phone = '123 123456789'
        user.date_of_birth = '1990-02-09'
        user.drivers_licence_number = '123123123'
        user.identity_card_number = '123123123'
        user.language = 'CS'
        user.save()
        
        # Otevreni pozadovane URL a zadani udaju do prihlasovaciho formu

        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = 'test'
        form['password'] = password
        response = form.submit().follow()

        
        # Uzivatel je prihlasen

        # Kliknuti na tlacitko
        
        page = response.click(href='/uzivatele/muj-ucet/upravit/')
        # page = response.click(u'Změnit moje detaily')
        
        # Nove udaje
        # from IPython import embed; embed()
        email = 'novy@novy.cz'
        primary_phone = '999 888777999'

        # Odeslani novych udaju
        
        form2 = page.forms['account_edit_form']
        form2['email'] = email
        form2['primary_phone'] = primary_phone
        response = form2.submit().follow()

        # Rozparsovani nove stranky
        
        jQuery = response.pyquery
        
        # Kontrola nastaveni novych promennych
            
        self.assertEqual(jQuery('#li_email a').text(), email)
        assert primary_phone in jQuery('#li_primary_phone').text()

