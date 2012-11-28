
# encoding: utf-8

from django_webtest import WebTest

from metrocar.user_management.models import MetrocarUser


class TestLogin(WebTest):

    def test_valid_login(self):
        username = 'afdasdfadf'
        password = 'sadf68a46d'
        user = MetrocarUser.objects.create(username=username, language='CS')
        user.set_password(password)
        user.save()

        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = username
        form['password'] = password
        
        # Follow?
        response = form.submit()
        # if the login was successful, we should get a redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/uzivatele/muj-ucet/'))
        
        page = response.follow()
        
        
        # assert na testovani promennych kontextu
        self.assertEqual(page.context['user'].username, username)

    def test_invalid_login(self):
        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = 'invalid'
        form['password'] = 'invalid84984'
        response = form.submit()
        self.assertEqual(response.status_code, 200)
        
        # Assert na nadpis ze byl spatnej login

