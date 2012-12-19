# encoding: utf-8

"""
from django_webtest import WebTest
from pyquery import PyQuery

from metrocar.user_management import testaing_data
from metrocar.user_management.models import MetrocarUser



# Test prihlaseni, zmeny hesla, odhlaseni a nasledne prihlaseni s novym heslem


class TestPasswordChange(WebTest):

    def test_change_password(self):
    
        # Nastaveni a ulozeni noveho uzivatele
        username = 'test'
        password = 'password'
        user = testing_data.create_user(username, password, 'Pokusny', 'Uzivatel', 'pokusny@fel.cvut.cz')
        

        # Otevreni pozadovane URL a zadani udaju do prihlasovaciho formu

        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = username
        form['password'] = password
        response = form.submit().follow()

        # from IPython import embed; embed()
        # Uzivatel je prihlasen

        # Kliknuti na tlacitko
        
        page = response.click(linkid='change_password')


        # Nove udaje
        
        new_password = 'newpassword'

        # Odeslani novych udaju
        
        form = page.forms['change_password_form']
        form['old_password'] = password
        form['new_password1'] = new_password
        form['new_password2'] = new_password
        response = form.submit().follow()

        # Rozparsovani nove stranky
        
        jQuery = response.pyquery
        
        # Kontrola nastaveni novych promennych
        # from IPython import embed; embed()
        self.assertEqual(jQuery('h2').text(), u'Heslo bylo změněno')
        
        # Odhlaseni
        page = response.click(href='/odhlaseni/')
        
        
        # Prihlaseni pod novymi udaji
        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = username
        form['password'] = new_password
        response = form.submit().follow()
        
        jQuery = response.pyquery
        
        self.assertEqual(jQuery('.success').text(), u'Byli jste úspěšně přihlášeni.')
        
        
"""
