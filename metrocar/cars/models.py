from datetime import datetime
from datetime import timedelta
from decimal import *

from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos.point import Point
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _
import managers
from metrocar.reservations.models import Reservation
from metrocar.subsidiaries.models import Subsidiary
from metrocar.user_management.models import AccountActivity
from metrocar.user_management.models import MetrocarUser
from metrocar.utils.fields import *


class CarModelManufacturer(models.Model):
    slug = models.SlugField(blank=False, null=False, verbose_name=_('Slug'))
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Car manufacturer')
        verbose_name_plural = _('Car manufacturers')

    def __unicode__(self):
        return self.name


class Fuel(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Title'))

    class Meta:
        verbose_name = _('Fuel')
        verbose_name_plural = _('Fuel')

    def __unicode__(self):
        return self.title


class CarType(models.Model):
    type = models.CharField(max_length=50, blank=False, null=False, unique=True, verbose_name=_('Car type'))

    class Meta:
        verbose_name = _('Car type')
        verbose_name_plural = _('Car types')

    def __unicode__(self):
        return self.type

class CarModel(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Name'))
    manufacturer = models.ForeignKey(CarModelManufacturer, blank=False, null=False, verbose_name=_('Manufacturer'))
    type = models.ForeignKey(CarType, verbose_name=_('Car type'), related_name='models')
    engine = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Engine'))
    seats_count = models.IntegerField(blank=False, null=False, verbose_name=_('Seats count'))
    storage_capacity = models.IntegerField(blank=False, null=False, verbose_name=_('Storage capacity'))
    main_fuel = models.ForeignKey(Fuel, blank=False, null=False, related_name='main_fuel', verbose_name=_('Main fuel'))
    alternative_fuel = models.ForeignKey(Fuel, blank=True, null=True, related_name='alternative_fuel', verbose_name=_('Alternative fuel'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    image = models.ImageField(upload_to='car_models/%Y/%m', blank=True, null=True, verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')

    def __unicode__(self):
        return u"%s %s %s" % (self.manufacturer, self.name, self.engine)
	
    def get_pricelist(self):
        """
		Returns available and valid pricelist for current car model if possible
		If no pricelist is found, returns False
		"""
        #TODO caching
        from metrocar.tarification.models import Pricelist
        try:
            p = Pricelist.objects.valid().filter(model=self).order_by('-valid_from')[0]
            return p
        except IndexError:
            return False

class CarColor(models.Model):
    color = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Color'))

    class Meta:
        verbose_name = _('Car color')
        verbose_name_plural = _('Car colors')
	
    def __unicode__(self):
        return self.color

class Car(models.Model):
    STATE_LOCKED = 'LOCKED'
    STATE_OPENED = 'OPENED'

    active = models.BooleanField(blank=False, null=False, verbose_name=_('Active'))
    imei = models.CharField(unique=True, max_length=18, null=False, blank=False, verbose_name=_('IMEI'))
    authorization_key = models.CharField(max_length=40, null=False,
                                         blank=False, verbose_name=_('Authorization key'),
                                         help_text=_('SHA1 encoded. Use the '
                                         '<a href=\"change-authorization-key/\">change authorization key '
                                         'form</a> to change.'))
    dedicated_parking_only = models.BooleanField(null=False, blank=False, default=False, verbose_name=_('Dedicated parking only'))
    last_echo = models.DateTimeField(blank=True, null=True, verbose_name=_('Last echo'))
    manufacture_date = models.DateTimeField(blank=False, null=False, verbose_name=_('Manufacture date'))
    mobile_number = PhoneField(blank=False, null=False, verbose_name=_('Mobile number'))
    registration_number = models.CharField(max_length=20, blank=False, null=False, verbose_name=_('Registration number'))
    last_position = models.PointField(_('Last position'))
    last_address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Last address'))
    image = models.ImageField(upload_to='cars/%Y/%m', blank=True, null=True, verbose_name=_('Image'))

    model = models.ForeignKey(CarModel, null=False, blank=False, verbose_name=_('Car model'), related_name='cars')
    color = models.ForeignKey(CarColor, null=False, blank=False, verbose_name=_('Car color'))
    owner = models.ForeignKey(MetrocarUser, null=True, blank=True, verbose_name=_('Owner'))
    home_subsidiary = models.ForeignKey(Subsidiary, null=False, blank=False, verbose_name=_('Subsidiary'))

    objects = managers.CarManager()

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __unicode__(self):
        return self.get_full_name()

    def __setattr__(self, name, value):
        " Overload to listen on change of last position to reset the text "
        if name == 'last_position' and self.__dict__.has_key('last_position'):
            if isinstance(self.__dict__['last_position'], Point):
                self.__dict__['last_address'] = None
        super(Car, self).__setattr__(name, value)

    def save(self, * args, ** kwargs):
        """
		If position text is none, query it and save it.
		"""
        if self.last_address is None:
            try:
                from metrocar.utils.nominatim import NominatimQuerier
                n = NominatimQuerier()
                self.last_address = n.resolve_address(self.last_position.y,
                                                      self.last_position.x)['display_name']
            except:
                # cannot fetch nominatim data - fail silently
                from metrocar.utils.log import get_logger, logging
                get_logger().log(logging.WARN, "Cannot fetch nominatim data "
                                 "for position %s" % self.last_position)
        super(Car, self).save(*args, ** kwargs)

    def get_full_name(self):
        return "%s (%s)" % (unicode(self.model), self.registration_number)

    @property
    def full_name(self):
        return self.get_full_name()

    @models.permalink
    def get_absolute_url(self):
        return ('mfe_cars_detail', (), {'id': self.pk})

    def set_auth_key(self, key):
        """
		Sets the encrypted authorization key
		"""
        self.authorization_key = managers.CarManager().make_auth_key(key)

    def state(self):
        """
		Returns car state (locked or opened).
		"""
        if self.get_current_journey() is None:
            return Car.STATE_OPENED
        else:
            return Car.STATE_LOCKED

    def is_locked(self):
        """
		Returns true if car is locked
		"""
        return self.state == Car.STATE_LOCKED

    def get_current_journey(self):
        """
		Returns current journey for the car or None if it doesn't exist.
		"""
        try:
            return self.journey_set.get(end_datetime__isnull=True)
        except Journey.DoesNotExist:
            return None

    def update_last_position(self):
        """
		Updates car's last position according to last saved CarPosition object.
		"""
        try:
            last_pos = CarPosition.objects.filter(journey__car=self).order_by('-pk')[0]
            self.last_position = last_pos.position
            self.last_address = None
            self.save()
            return True
        except IndexError:
            return False

    def update_comm_status(self):
        """
		Updates last echo information for the car to be 'now'
		"""
        self.last_echo = datetime.now()
        self.save()

    def get_upcoming_reservations(self, format='json'):
        """
		Returns JSON object with reservation events suitable for using in
		calendar view.
		Each record has an id, title (containing username of reservee),
		start and end. Also, there is readOnly property for calendar use.
		"""
        reservation_list = []
        for reservation in Reservation.objects.filter(car=self,
                                                      reserved_until__gte=datetime.now()).order_by('reserved_from'):
            reservation_list.append({
                                    'id': reservation.pk,
                                    'title': reservation.user.username,
                                    'start': reservation.reserved_from.isoformat(),
                                    'end': reservation.reserved_until.isoformat(),
                                    'readOnly': True
                                    })

        if format == 'json':
            import simplejson
            return simplejson.dumps(reservation_list)
        else:
            return reservation_list

    def get_upcoming_reservations_json(self):
        """
		Shortcut for get_upcoming_reservations to be used in templates, where
		json is needed.
		"""
        return self.get_upcoming_reservations(format='json')

    def is_user_allowed(self, user, datetime):
        """
		Returns True if user is allowed to access the car in given time
		"""
        if user.user_card.is_service_card:
            return True
        try:
            Reservation.objects.get(cancelled=False, car=self,
                                    reserved_from__lte=datetime, reserved_until__gte=datetime,
                                    user=user)
            return True
        except Reservation.DoesNotExist:
            pass
        return False

    def get_allowed_users(self, dt=datetime.now()):
        """
		Returns list of users who are allowed to access the car along with times,
		when they are allowed to.
		"""
        from metrocar.utils.models import SiteSettings
        check_interval = SiteSettings.objects.get_current().gps_check_interval
        dt_till = dt + timedelta(seconds=check_interval)
        # part 1: users who have reservation
        active_reservations = Reservation.objects.filter(cancelled=False,
                                                         car=self, reserved_until__gte=dt, reserved_until__lte=dt_till)
        reservation_users = {}
        for reservation in active_reservations:
            if not reservation_users.has_key(reservation.user):
                reservation_users[reservation.user] = (reservation.reserved_from,
                                                       reservation.reserved_until, )
            else:
                reservation_users[reservation.user].append(
                                                           (reservation.reserved_from, reservation.reserved_until, ))

        #part 2: users with service card
        service_card_users = {}
        service_card_users_timetuple = [(dt - timedelta(minutes=5),
                                         dt + timedelta(days=31), )]
        for user in MetrocarUser.objects.filter(user_card__is_service_card=True):
            service_card_users[user] = service_card_users_timetuple

        # finally merge it
        return dict(reservation_users, ** service_card_users)

    def get_statistics(self, since_time, to_time):

        FuelBillList = FuelBill.objects.filter(car=self).filter(datetime__gte=since_time).filter(datetime__lte=to_time)
        fuelCount = 0
        fuelPriceCount = 0
        for b in FuelBillList:
            fuelCount += b.liter_count
            fuelPriceCount += b.money_amount

        MaintenanceBillList = MaintenanceBill.objects.filter(car=self).filter(datetime__gte=since_time).filter(datetime__lte=to_time)
        maintenancePriceCount = 0
        for m in MaintenanceBillList:
            maintenancePriceCount += m.money_amount

        JourneyList = Journey.objects.filter(car=self).filter(end_datetime__gte=since_time).filter(end_datetime__lte=to_time)
        kmTotal = Decimal(0)
        timeTotal = timedelta(0)
        for j in JourneyList:
            kmTotal += j.length
            timeTotal += (j.end_datetime - j.start_datetime)

        try:
            pricePerKm = fuelPriceCount / kmTotal
        except DivisionByZero:
            pricePerKm = 0

        return [fuelCount, kmTotal, fuelPriceCount, maintenancePriceCount, (fuelPriceCount + maintenancePriceCount), pricePerKm, timeTotal * 24]

    @classmethod
    def list_of_available_cars(cls, datetime_start, datetime_end, home_subsidiary=None):
        """
        Vrati vsechny automobily, ktere jsou v zadanem obdobi dostupne a patri ke zvolene pobocce
        """
        cars = Car.objects.filter()
        if (home_subsidiary is not None):
            cars = cars.filter(home_subsidiary=home_subsidiary)

        result = []
        for c in cars:
            reservations = Reservation.find_conflicts(c, datetime_start, datetime_end)
            if len(reservations) == 0:
                result.append(c)

        return result

class FuelBill(AccountActivity):
    code = models.CharField(max_length=20, blank=False, null=False,
                            verbose_name=_('Code'))
    approved = models.BooleanField(blank=False, null=False, default=False,
                                   verbose_name=_('Approved'))
    car = models.ForeignKey(Car, blank=False, null=False, verbose_name=_('Car'))
    fuel = models.ForeignKey(Fuel, blank=False, null=False, verbose_name=_('Fuel'))
    liter_count = models.DecimalField(decimal_places=2, max_digits=6,
                                      blank=False, null=False, verbose_name=_('Liter count'))
    place = models.CharField(max_length=100, blank=False, null=False,
                             verbose_name=_('Place'))
    image = models.ImageField(upload_to='fuel_bills/%Y/%m', blank=True,
                              null=True, verbose_name=_('Bill image'))

    class Meta:
        verbose_name = _('Fuel bill')
        verbose_name_plural = _('Fuel bills')
		
    def save(self, * args, ** kwargs):
        self.code = '#%s-%s' % (str(self.account.user.pk).zfill(4),
                                datetime.strftime(self.datetime, '%Y%m%d%H%M'))
        super(FuelBill, self).save(*args, ** kwargs)
		
    def ready_to_be_invoiced(self):
        """
		Returns true if item is ready to be invoiced.
		"""
        if self.approved: return True
        else: return False

    def __unicode__(self):
        return '%s %s %s %sl' % (self.code, unicode(_('Refuel')),
                                 self.fuel, round(self.liter_count, 1))

class MaintenanceBill(AccountActivity):
    code = models.CharField(max_length=20, blank=False, null=False, verbose_name=_('Code'))
    purpose = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Purpose'))
    approved = models.BooleanField(blank=False, null=False, default=False, verbose_name=_('Approved'))
    car = models.ForeignKey(Car, blank=False, null=False, verbose_name=_('Car'))
    place = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Place'))
    image = models.ImageField(upload_to='maintenence_bills/%Y/%m', blank=True, null=True, verbose_name=_('Bill image'))
    
    class Meta:
        verbose_name = _('Maintenance bill')
        verbose_name_plural = _('Maintenance bills')

    def save(self, * args, ** kwargs):
        self.code = '#%s-%s' % (str(self.account.user.pk).zfill(4),
                                datetime.strftime(self.datetime, '%Y%m%d%H%M'))
        super(MaintenanceBill, self).save(*args, ** kwargs)

    def ready_to_be_invoiced(self):
        """
		Returns true if item is ready to be invoiced.
		"""
        if self.approved: return True
        else: return False

    def __unicode__(self):
        return '%s %s %s' % (self.code, unicode(_('Maintenance')), self.comment)

class Parking(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False,
                            verbose_name=_('Name'))
    places_count = models.IntegerField(blank=False, null=False,
                                       verbose_name=_('Places count'))
    land_registry_number = models.CharField(max_length=50, blank=False,
                                            null=False, verbose_name=_('Land registry number'))
    street = models.CharField(max_length=255, blank=False, null=False,
                              verbose_name=_('Street'))
    city = models.CharField(max_length=50, blank=False, null=False,
                            verbose_name=_('City'))
    polygon = models.PolygonField(verbose_name=_('Area'))

    cars = models.ManyToManyField(Car, through='ParkingDescription')
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Parking')
        verbose_name_plural = _('Parkings')

    def __unicode__(self):
        return self.city + ' ' + self.street


class ParkingDescription(models.Model):
    description = models.TextField(blank=False, null=False,
                                   verbose_name=_('Description'))

    parking = models.ForeignKey(Parking, blank=False, null=False,
                                verbose_name=_('Parking'))
    car = models.ForeignKey(Car, blank=False, null=False, verbose_name=_('Car'))

    class Meta:
        verbose_name = _('Parking description')
        verbose_name_plural = _('Parking descriptions')

    def __unicode__(self):
        return self.description
	
class CarPosition(models.Model):
    position = models.PointField(_('Car position'))
    journey = models.ForeignKey('Journey', blank=False, null=False,
                                verbose_name=_('Journey'))

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Car position')
        verbose_name_plural = _('Car positions')

    def __unicode__(self):
        return "#%s %s" % (self.get_sequence_nr(), self.position)

    def save(self, * args, ** kwargs):
        """
		Overload save to update journey last position.
		
		We also add posibility to evade car position update by setting the
		parameter no_pos_update to True
		"""
        if kwargs.has_key('no_pos_update'):
            pos_update = not kwargs['no_pos_update']
            del kwargs['no_pos_update']
        else:
            pos_update = True
        super(CarPosition, self).save(*args, ** kwargs)
        # if we are told not to update car position (used for bulk canges)
        if pos_update:
            # update car position, don't expect we are the last one
            self.journey.car.update_last_position()
	
    def get_sequence_nr(self):
        """
		Returns CarPosition order in journey.
		"""
        return len(CarPosition.objects.filter(journey=self.journey, pk__lt=self.pk))

class Journey(models.Model):
    TYPE_WAITING = 'W'
    TYPE_TRIP = 'T'
    TYPE_LATE_RETURN = 'LR'
    TYPE_CHOICES = (
                    (TYPE_WAITING, _('Waiting')),
                    (TYPE_TRIP, _('Trip')),
                    (TYPE_LATE_RETURN, _('Late return'))
                    )
	
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))
    start_datetime = models.DateTimeField(blank=False, null=False,
                                          verbose_name=_('Start datetime'))
    end_datetime = models.DateTimeField(blank=True, null=True, default=None,
                                        verbose_name=_('End datetime'))
    length = models.DecimalField(decimal_places=3, max_digits=8, blank=False,
                                 null=False, default=0, verbose_name=_('Length'), editable=False)
    path = models.MultiLineStringField(null=True, blank=True,
                                       spatial_index=False, verbose_name=_('Path'))
    total_price = models.DecimalField(decimal_places=2, max_digits=8,
                                      blank=True, null=True, default=0, verbose_name=_('Price'))
    type = models.CharField(max_length=2, null=False, blank=False,
                            choices=TYPE_CHOICES, default='T', editable=False,
                            verbose_name=_('Journey type'))

    reservation = models.ForeignKey(Reservation, blank=True, null=True,
                                    related_name='journeys')
    car = models.ForeignKey(Car, null=False, verbose_name=_('Car'))
    user = models.ForeignKey(MetrocarUser, null=False, verbose_name=_('User'))

    speedometer_start = models.IntegerField(null=False, verbose_name=_('Speedometer start state'),
                                            blank=False)

    speedometer_end = models.IntegerField(null=False, verbose_name=_('Speedometer end state'),
                                            blank=False)

    objects = managers.JourneyManager()

    class Meta:
        verbose_name = _('Journey')
        verbose_name_plural = _('Journeys')

    def __unicode__(self):
        if self.start_datetime and self.end_datetime:
            return '%s - %s' % (datetime.strftime(self.start_datetime,
                                '%H:%M:%S %A, %d.%m.%Y'), datetime.strftime(self.end_datetime,
                                '%H:%M:%S %A, %d.%m.%Y'))
        else:
            return unicode(self.pk)
		
    def save(self, * args, ** kwargs):
        """Overload to add custom validation"""
        if self.is_valid():
            super(Journey, self).save(*args, ** kwargs)
		
    def is_valid(self):
        j = self.car.get_current_journey()
        if j is not None and j.pk != self.pk:
            raise AssertionError(_('Cannot save journey for Car `%s` because it has one which is already active') % self.car)
            return False
		
        if self.end_datetime is not None:
            if self.end_datetime <= self.start_datetime:
                raise AssertionError(_('Journey end time must be after journey start time'))
                return False

        if self.start_datetime is not None:
            if self.start_datetime < self.reservation.reserved_from:
                raise AssertionError(_('Journey start time must be after reservation start time or equal.'))
                return False

        if self.speedometer_end is not None and self.speedometer_start is not None:
            if self.speedometer_end <= self.speedometer_start:
                raise AssertionError(_('State of speedometer in the end of the journey must be higher than in the beginning of the journey.'))
                return False
        return True
		
    def update_total_price(self):
        """
		Refreshes total price of journey forcing recount
		"""
        self.total_price = self._get_total_price()

    def _get_total_price(self):
        """
		Stands as proxy for counting prices
		"""
        pricing_info = self.get_pricing_info()
        if pricing_info is not None:
            return pricing_info['total_price']
        return 0
	
    def get_pricing_info(self):
        """
		Stands as proxy for counting prices
		"""
        if self.reservation:
            return self.reservation.get_pricelist().count_journey_price(self)
        return None
	
    @classmethod
    def refresh_path(cls, sender, ** kwargs):
        """
		Forces refresh of journey path from CarPosition objects.
		"""
        journey = kwargs['instance'].journey
        position_points = [position.position for position in journey.carposition_set.order_by('pk')]
        line_strings = []
		
        if len(position_points) == 1:
            # create generic linestring with two same points
            line_strings = [LineString(position_points[0], position_points[0])]
        else:
            # create linestring connecting points
            for point_one, point_two in zip(position_points[:-1], position_points[1:]):
                line_strings.append(LineString(point_one, point_two))
		
        journey.path = MultiLineString(*line_strings)
        journey.save()
	
    def is_finished(self):
        """
		Returns true if journey is already finished.
		"""
        return self.end_datetime != None
	
    def is_service(self):
        """
		Returns true if journey is service type
		"""
        return self.reservation == None
	
    def finish(self, time):
        """
		Finishes journey and sets end_datetime to time param
		"""
        self.end_datetime = time
        self.save()
        return True
	
post_save.connect(Journey.refresh_path, sender=CarPosition)
pre_delete.connect(Journey.refresh_path, sender=CarPosition)
post_save.connect(Reservation.refresh_journey_data, sender=Journey)
post_delete.connect(Reservation.refresh_journey_data, sender=Journey)
