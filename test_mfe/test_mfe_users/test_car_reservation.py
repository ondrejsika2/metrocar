# encoding: utf-8


from django_webtest import WebTest
from pyquery import PyQuery

import datetime
from test_metrocar.test_metrocar_user_management.fixtures import create_user_1
from metrocar.cars import testing_data as cartest
from metrocar.user_management.models import MetrocarUser
from metrocar.cars.models import Car,CarModel



# Test rezervace


class TestReservation(WebTest):

    def test_reservation(self):

        # Nastaveni a ulozeni noveho uzivatele
        username = 'test'
        password = 'password'
        user = create_user_1()

        # Naplenni databaze auty
        cars = cartest.create()

        # Otevreni pozadovane URL a zadani udaju do prihlasovaciho formu

        page = self.app.get('/prihlaseni/')
        form = page.forms['login_form']
        form['username'] = username
        form['password'] = password
        response = form.submit().follow()

        # from IPython import embed; embed()
        # Uzivatel je prihlasen


        # Kliknuti na tlacitko v menu

        page = response.click(linkid='tray_reservation')

        # Odeslani novych udaju

        now = datetime.datetime.now()
        year = now.year
        month =  now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second =  now.second

        date_from = str(month)+'.'+str(day)+'.'+str(year)
        date_to = str(month)+'.'+str(day)+'.'+str(year)
        # time_from = str(hour)+':'+str(minute)
        t = now.time().isoformat()
        # time_from = = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)



        form = page.forms['main_form']
        # from IPython import embed; embed()
        form['0-reserved_from_0'] = date_from
        form['0-reserved_from_1'] = '15:00'

        form['0-reserved_until_0'] = date_to
        form['0-reserved_until_1'] = '20:00'
        form['0-car_id'] = '4'
        response = form.submit()



