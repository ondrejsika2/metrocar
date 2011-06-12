'''
Created on 7.5.2010

@author: xaralis
'''
import hashlib
from datetime import datetime

from django.contrib.gis.db import models
from django.db.transaction import commit_on_success
from metrocar.reservations.models import Reservation
from django.contrib.auth.models import User
from metrocar.user_management.models import UserCard

class CarManager(models.GeoManager):
#    def get_query_set(self):
#        """
#        Return only cars from home subsidiary by default
#        """
#        from metrocar.utils.models import SiteSettings
#        current_subsidiary = SiteSettings.objects.get_current()
#        return super(CarManager, self).get_query_set().filter(home_subsidiary=current_subsidiary)
#
#    def get_all(self):
#        """
#        Returns all cars (not just local ones)
#        """
#        return super(CarManager, self).get_query_set()
    
    def authenticate(self, imei, authorization_key):
        """
        Tries to authenticate car unit by using given imei and authorization key
        """
        try:
            car = self.get_query_set().get(imei=imei)
            if car.authorization_key == self.make_auth_key(authorization_key):
                return car 
        except:
            pass
        return False
    
    @classmethod
    def make_auth_key(cls, password):
        return hashlib.sha1(password).hexdigest()
    
class JourneyManager(models.GeoManager):
    @commit_on_success
    def start_journey(self, car, user, time, type='T'):
        """
        Starts new Journey and eventually marks reservation as started if 
        there is a reservation for car, time and user active.
        """
        from metrocar.cars.models import Car
        assert isinstance(car, Car)
        assert isinstance(user, User)
        assert isinstance(time, datetime)
        
        j_params = {
            'start_datetime': time,
            'car': car,
            'user': user
        }
        user_card = user.user_card
        
        if not user_card.active:
            raise AssertionError("Inactive user card, possible account abuse.")
        
        if not user_card.is_service_card:
            # try to find suitable reservation
            try :
                reservation = Reservation.objects.get(car=car, user=user,
                    reserved_from__lte=time, reserved_until__gte=time)
                if reservation.started is None:
                    reservation.started = time
                    reservation.save() 
                    j_params['reservation'] = reservation
            except Reservation.DoesNotExist:
                raise AssertionError("Reservation expected, but not found. "
                    "Possible car abuse.")
        journey = self.model(**j_params)
        journey.save() # validation happens in save method automatically
        return journey

    def get_current_for_car_user_card(self, car, user_card, time):
        """
        Returns current journey for car a user card if possible.
        """
        from metrocar.cars.models import Car
        assert isinstance(car, Car)
        assert isinstance(user_card, UserCard)
        assert isinstance(time, datetime)

        if not user_card.is_service_card:
            journey = self.get(user=user_card.user, car=car,
                end_datetime__isnull=True)
        else:
            journey = self.get(user=user_card.user, car=car,
                end_datetime__isnull=True, reservation__isnull=True)
        return journey
    
    @commit_on_success
    def create_complete_journey(self, car, user_card, datetime_since,
                                datetime_till, type='T'):
        """
        Creates complete journey at once
        """
        journey = self.start_journey(car, user_card,
            datetime_since, type=type)
        journey.finish(datetime_till)
        return journey
    
    @commit_on_success
    def normalize_for_reservation(self, reservation):
        """
        Normalizes journeys for reservations.
        Adds waiting journeys, splits late-return journeys.
        """
        journeys = self.filter(reservation=reservation).order_by('start_datetime')
        assert len(journeys) >= 1
        # if last journey exceeds regular reservation end datetime, split it 
        # to two parts (last one will be late return type)
        last_journey = journeys[len(journeys) - 1]
        if last_journey.end_datetime > reservation.reserved_until:
            import itertools
            new_journey = self.model(
                start_datetime=reservation.reserved_until, 
                end_datetime=last_journey.end_datetime,
                reservation=reservation,
                car=last_journey.car,
                user=last_journey.user,
                type=self.model.TYPE_LATE_RETURN
            )
            new_journey.save()
            last_journey.end_datetime = reservation.reserved_until
            last_journey.save()
            # add new journey to the end of the iterator for future usage
            journeys = itertools.chain(journeys, [ new_journey ])
        # now iterate throught the journeys and fill up the missing parts 
        # with waiting journeys
        start_dt = reservation.reserved_from
        for j in journeys:
            if start_dt != j.start_datetime:
                # fill up missing part
                journey = self.model(
                    start_datetime=start_dt,
                    end_datetime=j.start_datetime,
                    reservation=reservation,
                    car=j.car,
                    user=j.user,
                    type=self.model.TYPE_WAITING
                )
                journey.save()
            start_dt = j.end_datetime
        # if start_dt preceeds regular reservation end, fill up missing part
        if start_dt < reservation.reserved_until:
            journey = self.model(
                    start_datetime=start_dt,
                    end_datetime=reservation.reserved_until,
                    reservation=reservation,
                    car=reservation.car,
                    user=reservation.user,
                    type=self.model.TYPE_WAITING
            )
            journey.save()
        # now get all journeys again (ordered) and force them to count their
        # price
        journeys = self.filter(reservation=reservation).order_by('start_datetime')
        for j in journeys:
            j.update_total_price()
            j.save()
    
