# coding=utf-8

from datetime import datetime, date, time, timedelta
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from metrocar.cars.models import CarModel, Journey
from metrocar.user_management.models import AccountActivity
from metrocar.utils.models import CloneableModelMixin
from metrocar.reservations.models import Reservation

import managers

class PricelistAssertionError(AssertionError):
	pass

class Pricelist(models.Model, CloneableModelMixin):
	available = models.BooleanField(blank=False, null=False, default=False,
		verbose_name=_('Available'))
	deleted = models.BooleanField(blank=False, null=False, default=False,
		verbose_name=_('Deleted'))
	description = models.TextField(blank=False, null=True, default='',
		verbose_name=_('Description'))
	name = models.CharField(max_length=50, blank=False, null=False,
		verbose_name=_('Name'), help_text=u'Název ceníku.')
	pickup_fee = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Pickup fee'),
		help_text=u'Částka, kterou zákazník zaplatí při vyzvednutí automobilu.')
	price_per_hour = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Price per hour'),
		help_text=u'Částka, kterou zákazník zaplatí za jednu hodinu, co bude mít automobil vypůjčený.')
	price_per_km = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Price per km'),
		help_text=u'Částka, kterou zákazník zaplatí za jeden ujetý kilometr.')
	reservation_fee = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Reservation fee'),
		help_text=u'Částka, kterou zákazník zaplatí za uskutečněnou rezervaci.')
	valid_from = models.DateField(blank=False, null=False,
		verbose_name=_('Valid from'))
	
	model = models.ForeignKey(CarModel, blank=False, null=False,
		verbose_name=_('Car model'), help_text=u'Model automobilu, nejedná se však o konkrétní vozidlo.')

	objects = managers.PricelistManager()

	class Meta:
		verbose_name = _('Pricelist')
		verbose_name_plural = _('Pricelists')

	def __unicode__(self):
		return self.name
	
	def clone(self, **kwargs):
		"""
		Overload CloneableModelMixin's clone() to add related records
		"""
		duplicate = super(Pricelist, self).clone(**kwargs)
		for day in self.pricelistday_set.all():
			day.clone(pricelist=duplicate)
		return duplicate
	
	def delete(self):
		"""
		Overload delete to act as soft delete.
		"""
		self.available = False
		self.deleted = True
		self.save()
	
	def get_basic_price_dict(self):
		"""
		Returns dictionary with basic fare information. It has following keys:
		  - pickup_fee - price of pickup
		  - price_per_km - price for one km
		  - price_per_hour_from - lowest price per hour
		  - price_per_hour_till - highest price for hour
		"""
		price_from = PricelistDayTime.objects.order_by('car_used_ratio') \
		    .filter(pricelist_day__pricelist=self)[0]
		price_till = PricelistDayTime.objects.order_by('-car_used_ratio') \
		    .filter(pricelist_day__pricelist=self)[0]
		
		return {
		    'pickup_fee': self.pickup_fee,
		    'price_per_km': self.price_per_km,
		    'price_per_hour_from': price_from.car_used_ratio
		        * self.price_per_hour,
		    'price_per_hour_till': price_till.car_used_ratio
		        * self.price_per_hour
		}
	
	def count_journey_price(self, journey):
		"""
		Counts price for a journey
		"""
		assert isinstance(journey, Journey)
		if not journey.is_finished(): return None
		
		# resolve key for pricing coefs
		key = 'used'
		if journey.type == Journey.TYPE_WAITING:
			key = 'unused'
		elif journey.type == Journey.TYPE_LATE_RETURN:
			key = 'late_return'
		
		total_price, km_price, time_price = (0, 0, 0)
		
		# first count price for time elapsed
		journey_parts = []
		# split journey into separate days
		for j in self._split_journey_into_days(journey):
			# find pricing for that day
			date = j[0].date()
			pricing = self.get_pricing_for_date(date)
			part_end_dt = j[1]
			curr_dt = j[0]
			while 1:
				# make interval based on pricing timeline
				curr_dt, end_dt, price_per_hour = self._make_pricing_interval(
					curr_dt, part_end_dt, pricing, key)
				duration = (end_dt - curr_dt)
				seconds = 0
				if duration.days > 0:
					seconds = (duration.days * 86400)
				else:
					seconds = duration.seconds
				# append final journey part
				part_price = Decimal(seconds) / Decimal(3600) \
				    * price_per_hour
				journey_parts.append({
					'start': curr_dt, # datetime.combine(date, curr_dt), 
					'end': end_dt, #datetime.combine(date, end_dt),
					'duration': duration,
					'price_per_hour': price_per_hour,
					'price': part_price
				})
				# add to the sum
				total_price += part_price
				time_price += part_price
				# if final time is reached, break the loop
				if end_dt == part_end_dt: break
				# otherwise make new curr_dt from end_dt and continue
				curr_dt = end_dt
		# now count the price for kms driven
		km_price = self.price_per_km * journey.length	
		total_price += km_price    
		return {
    		'total_price': total_price,
    		'km_price': km_price,
    		'time_price': time_price,
    		'journey_parts': journey_parts
	    }
		
	@staticmethod
	def _make_pricing_interval(curr_dt, end_dt, pricing, key):
		"""
		Returns start, end and pricing coef for curr_dt and end_dt
		"""
		#=======================================================================
		# First handle records except the last one
		#=======================================================================
		for rec in pricing:
			# find record which is last preceeding before curr_dt --------------
			if rec['from'] <= curr_dt.time(): continue
			used_rec = pricing[pricing.index(rec) - 1]
			return (
				curr_dt, # datetime from
				datetime.combine( # datetime till
					curr_dt.date(),
					min(end_dt.time(), rec['from'])
				),
				used_rec['coefs'][key] # used coef
			)
		#=======================================================================
		# Now handle last record
		#=======================================================================
		last_rec = pricing[len(pricing) - 1]
		# if end date is different, set end_dt to end_dt date
		if curr_dt.date() != end_dt.date():
			return (
				curr_dt, # datetime from
				datetime.combine( # datetime till
					end_dt.date(),
					min(end_dt.time(), last_rec['till'])
				),
				last_rec['coefs'][key]
			)
		# otherwise keep curr_dt date
		return (
			curr_dt, # datetime from
			datetime.combine( # datetime till
				curr_dt.date(),
				min(end_dt.time(), last_rec['till'])
			),
			last_rec['coefs'][key]
		)
		raise PricelistAssertionError('No suitable coef found.')
			
	@staticmethod
	def _split_journey_into_days(journey):
		"""
		Splits the journey into separate parts by day
		Each part is time interval
		"""
		assert isinstance(journey, Journey)
		
		start_datetime = journey.start_datetime
		end_datetime = journey.end_datetime
		
		assert start_datetime < end_datetime
		
		if start_datetime.date() != end_datetime.date():
			journey_parts = []
			
			# first part
			journey_parts.append(
				( start_datetime, 
				  datetime.combine(start_datetime.date()  + timedelta(days=1), time(hour=0)) ))
			
			start_datetime += timedelta(days=1)
			start_date = start_datetime.date()
			end_date = end_datetime.date()
			
			while start_date != end_date:
				# whole day part
				journey_parts.append(
					( datetime.combine(start_date, time(hour=0)),
					  datetime.combine(start_date + timedelta(days=1), time(hour=0)) ))
				start_date += timedelta(days=1)
		
			# last part
			journey_parts.append(
			        ( datetime.combine(start_datetime.date(), time(hour=0)), 
					  end_datetime ))
			
			return journey_parts
		else:
			return [ ( start_datetime, end_datetime ) ]
		
	def get_pricing_summary(self):
		"""
		Returns pricing summary for whole pricelist.
		
		Summary contains both rate summary and timeline records (splitted to 
		weekday and date parts)
		"""
		weekdays_timeline = [ ( { 'id': weekday.weekday_from, 'str': PricelistDay.get_weekday_human(weekday.weekday_from) }, weekday.get_pricing_timeline() )
							 for weekday in self.pricelistday_set.weekdays() ]
		# if it doesn't begin with monday copy last record to the begining
		if len(weekdays_timeline) and weekdays_timeline[0][0]['id'] != 0:
			tmp = [ ( { 'id': 0, 'str': PricelistDay.get_weekday_human(0) }, weekdays_timeline[len(weekdays_timeline) - 1][1] ) ]
			if len(weekdays_timeline) > 1:
				tmp += weekdays_timeline
			weekdays_timeline = tmp

		dates_timeline = [ ( { 'date': day.date }, day.get_pricing_timeline() ) 
						  for day in self.pricelistday_set.dates() ]
		return {
			'rates': {
				'pickup_fee': self.pickup_fee,
				'reservation_fee': self.reservation_fee,
				'per_hour': self.price_per_hour,
				'per_km': self.price_per_km
			},
			'timeline': {
				'weekdays': weekdays_timeline,
				'dates': dates_timeline
			}
	    }
		
	def get_pricelistday_for_date(self, date_to_find):
		"""
		Returns PricelistDay instance which is used for pricing on date_to_find.
		
		If there is PricelistDay record for specific date, it always has a 
		precedence before weekday records.
		
		If none PricelistDay is found, PricelistAssertionError is raised.
		"""
		assert isinstance(date_to_find, date)
		day = None

		try:
			# first try to find a day record (it has precedence)
			day = PricelistDay.objects.get(date=date_to_find, pricelist=self)
		except PricelistDay.DoesNotExist:
			# otherwise grab a weekday
			# first try to find a preceeding
			weekday = date_to_find.weekday()
			try:
				day = PricelistDay.objects.filter(weekday_from__lte=weekday,
					pricelist=self).order_by('-weekday_from')[0]
			except IndexError:
				# if none is found, try to grab last succeeding, or raise error
				try:
					day = PricelistDay.objects.filter(weekday_from__gt=weekday, pricelist=self).order_by('-weekday_from')[0]
				except IndexError:
					raise PricelistAssertionError(_('No timeline record exists but being requested'))
		return day

	def get_pricing_for_date(self, date_to_find):
		"""
		Returns pricing summary for given date.
		Raises PricelistAssertionError if no record is found.
		"""
		return self.get_pricelistday_for_date(date_to_find).get_pricing_timeline()

class PricelistDay(models.Model, CloneableModelMixin):
	WEEKDAYS = (
	    (0, _('Monday')), (1, _('Tuesday')), (2, _('Wednesday')), (3, _('Thursday')), 
	    (4, _('Friday')), (5, _('Saturday')), (6, _('Sunday'))
	)
	
	date = models.DateField(blank=True, null=True, verbose_name=_('Date'),
							help_text=u'Datum, ke kterému se bude tento ceník vztahovat. Pro jiné datum již nebude platit.')
	weekday_from = models.SmallIntegerField(max_length=1, blank=True,
		null=True, choices=WEEKDAYS, verbose_name=_('Weekday from'),
		help_text=u'Den v týdnu, od kterého se bude automaticky odvíjet ceník pro všechny následující dny. ' \
		          u'Přidáním nového dne do téhož ceníku se časové schéma změní.')

	pricelist = models.ForeignKey(Pricelist, blank=False, null=False,
		verbose_name=_('Pricelist'), help_text=u'Ceník, který je svázaný s konkrétním modelem automobilu.')

	objects = managers.PricelistDayManager()

	class Meta:
		verbose_name = _('Pricelist day')
		verbose_name_plural = _('Pricelist days')
		unique_together = (('date', 'pricelist'), ('weekday_from', 'pricelist'))

	def __unicode__(self):
		if self.weekday_from is not None:
			return u"%s (%s)" % (self.pricelist.name, self.weekday_from)
		return u"%s (%s)" % (self.pricelist.name, datetime.strftime(self.date,
			'%A, %d.%m.%Y')) 
	
	def clone(self, **kwargs):
		"""
		Overload CloneableModelMixin's clone() to add related records
		"""
		duplicate = super(PricelistDay, self).clone(**kwargs)
		for time in self.pricelistdaytime_set.all():
			time.clone(pricelist_day=duplicate)
		return duplicate
	
	@staticmethod
	def get_weekday_human(day_nr):
		"""
		Returns weekday in human readable form
		"""
		return force_unicode(dict(PricelistDay.WEEKDAYS).get(day_nr, day_nr))
	
	def get_str_rep(self):
		if self.weekday_from is not None:
			return PricelistDay.get_weekday_human(self.weekday_from)
		else:
			return u'%s' % self.date

	def get_pricing_timeline(self):
		"""
		Returns pricing timeline for this day. Summary is a dictionary containing
		separate parts of timeline. Each part has its ratios.
		"""
		base_price = self.pricelist.price_per_hour
		pricing_list = []
		
		def _make_part_dict(timeline_part, time_till):
			d_t = datetime.combine(date.today(), time_till)
			d_f = datetime.combine(date.today(), timeline_part.time_from)
			part = {
			    'from': timeline_part.time_from,
			    'till': time_till,
			    'minutes': int(round((d_t - d_f).seconds / 60)),
			    'coefs': {
			        'unused': base_price * timeline_part.car_unused_ratio,
					'used':	base_price * timeline_part.car_used_ratio,
					'late_return': base_price * timeline_part.late_return_ratio
				}
		    }
			return part

		for timeline_part in self.pricelistdaytime_set.order_by('time_from'): 
			try:
				following_time_part = self.pricelistdaytime_set.filter(pk__gt=timeline_part.pk).order_by('time_from')[0]
				time_till = (datetime.combine(date.today(), following_time_part.time_from) - timedelta(seconds=1)).time()
			except:
				time_till = time(hour=23, minute=59, second=59) 
			pricing_list.append(_make_part_dict(timeline_part, time_till))
		
		# if there is only one part, stretch it to whole day
		if len(pricing_list) == 1:
			pricing_list[0]['from'] = time(hour=0, minute=0, second=0)
			pricing_list[0]['minutes'] = 24 * 60
		# if timeline doesn't begin on midnight, copy last part as first
		if len(pricing_list) and pricing_list[0]['from'] != time(hour=0, minute=0, second=0):
			import copy
			first_rec = copy.copy(pricing_list[-1])
			d_f = datetime.combine(date.today(), time(hour=0, minute=0, second=0))
			d_t = datetime.combine(date.today(), pricing_list[0]['from']) - timedelta(seconds=1)
			first_rec['minutes'] = int(round((d_t - d_f).seconds / 60))
			first_rec['from'] = d_f.time()
			first_rec['till'] = d_t.time()
			pricing_list = [ first_rec ] + pricing_list
		return pricing_list

class PricelistDayTime(models.Model, CloneableModelMixin):
	car_unused_ratio = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Car unused ratio'))
	car_used_ratio = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Car used ratio'))
	late_return_ratio = models.DecimalField(decimal_places=3, max_digits=8,
		blank=False, null=False, verbose_name=_('Late return ratio'))
	time_from = models.TimeField(blank=False, null=False,
		verbose_name=_('Time from'))
	
	pricelist_day = models.ForeignKey(PricelistDay, blank=False, null=False,
		verbose_name=_('Pricelist day'))

	class Meta:
		verbose_name = _('Pricelist daytime')
		verbose_name_plural = _('Pricelist daytimes')
		unique_together = (('time_from', 'pricelist_day'),)

	def __unicode__(self):
		return u"%s %s" % (self.pricelist_day, self.time_from)
		
class StornoFeeTimeline(models.Model):
	preceeding_time_from = models.IntegerField(blank=False, null=False,
		verbose_name=_('From preceeding time'))
	price = models.DecimalField(max_digits=8, decimal_places=2, blank=False,
		null=False, default=Decimal('0'), verbose_name=_('Price'))
	
	class Meta:
		verbose_name = _('Storno fee timeline record')
		verbose_name_plural = _('Storno fee timeline records')

	def __unicode__(self):
		return _('Storno fee timeline')
	
	#TODO SOFT DELETE
		
class StornoFee(AccountActivity):
	reservation = models.ForeignKey(Reservation, unique=True,
		verbose_name=_('Reservation'))
	
	fee_timeline = models.ForeignKey(StornoFeeTimeline,
		verbose_name=_('Fee timeline'))

	objects = managers.StornoFeeManager()

	class Meta:
		verbose_name = _('Storno fee')
		verbose_name_plural = _('Storno fees')

	def __unicode__(self):
		return _('Storno fee')

	@classmethod
	def get_charge_value(cls, reservation):
		"""
		Returns expected storno fee for given reservation in case if it was 
		cancelled now
		"""
		timeline_rec = cls.objects.get_record_for_reservation(reservation)
		return timeline_rec.fee_timeline.price
