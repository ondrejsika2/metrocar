# from datetime import datetime, timedelta
# from decimal import Decimal
# from functools import partial
# from pipetools import foreach, X, where, KEY
#
# import django.test
#
# import geotrack
#
# from metrocar.car_unit_api.models import Events
# from metrocar.car_unit_api.testing_data import unit
# from metrocar.cars import testing_data as cars_testing_data
# from metrocar.cars.models import Car, Journey
#
# from metrocar.utils.geo import create_journey, create_journeys, get_journey_data, journey_splitter, split_by_events, split_by_idle_time, distance
# from test_metrocar.helpers import skipIfNotGeoEnabled
#
#
# class TestSplitters(django.test.TestCase):
#
#     def test_split_by_events_empty(self):
#         self.assertEquals(split_by_events({'events': []}, {}), False)
#
#     def test_split_by_events_false(self):
#         journey = {'events': [Events.UNLOCKED, 'Y', Events.ENGINE_ON]}
#         self.assertEquals(split_by_events(journey, {}), False)
#
#     def test_split_by_events_true(self):
#         journey = {'events': [
#             Events.UNLOCKED,
#             'X',
#             Events.ENGINE_ON,
#             Events.ENGINE_OFF,
#             'Y',
#             Events.LOCKED,
#             'Z',
#         ]}
#         self.assertEquals(split_by_events(journey, {}), True)
#
#     def test_split_by_idle_time_false(self):
#         t = partial(datetime, 2012, 12, 12)
#         journey = {'entries': [
#             {'timestamp': t(10, 30)},
#             {'timestamp': t(10, 31)},
#             {'timestamp': t(10, 32)},
#         ]}
#         self.assertEquals(
#             split_by_idle_time(journey, {'timestamp': t(10, 35)}), False)
#
#     def test_split_by_idle_time_true(self):
#         t = partial(datetime, 2012, 12, 12)
#         journey = {'entries': [
#             {'timestamp': t(10, 30)},
#             {'timestamp': t(10, 31)},
#             {'timestamp': t(10, 32)},
#         ]}
#         self.assertEquals(
#             split_by_idle_time(journey, {'timestamp': t(10, 42, 1)}), True)
#
#     def test_split_by_idle_time_custom_delay(self):
#         t = partial(datetime, 2012, 12, 12)
#         journey = {'entries': [
#             {'timestamp': t(10, 30)},
#             {'timestamp': t(10, 31)},
#             {'timestamp': t(10, 32)},
#         ]}
#         self.assertEquals(
#             split_by_idle_time(journey, {'timestamp': t(10, 35)},
#                 idle_after=timedelta(minutes=2)), True)
#
#
# class TestDistance(django.test.TestCase):
#
#     def test_odometer(self):
#         entries = [
#             {'odometer': 12345.67},
#             {'odometer': 12346.89},
#             {'odometer': 12347.67},
#         ]
#         self.assertEquals(distance(entries), 2)
#
#     def test_invalid_odometer(self):
#         entries = [
#             {'odometer': 12345.67},
#             {'odometer': 12346.89},
#             {'odometer': 12342.67},
#         ]
#         with self.assertRaises(ValueError):
#             distance(entries)
#
#
# class TestJourneySplitter(django.test.TestCase):
#
#     always = lambda *a: True
#     never = lambda *a: False
#
#     def test_initial(self):
#         entry = {'event': 'SOME_EVENT'}
#         self.assertEquals(
#             journey_splitter([], entry, split_by=self.never),
#             [{'entries': [entry], 'events': ['SOME_EVENT']}],
#         )
#
#     def test_dont_split(self):
#         journeys = [
#             1,
#             2,
#             {'entries': ['some_entry'], 'events': ['SOME_EVENT']},
#         ]
#         entry = {'some': 'data'}
#         self.assertEquals(
#             journey_splitter(journeys, entry, split_by=self.never),
#             [
#                 1,
#                 2,
#                 {'entries': ['some_entry', entry], 'events': ['SOME_EVENT']},
#             ]
#         )
#
#     def test_do_split(self):
#         journeys = [
#             {'entries': ['some_entry'], 'events': ['SOME_EVENT']},
#         ]
#         entry = {'some': 'data'}
#         self.assertEquals(
#             journey_splitter(journeys, entry, split_by=self.always),
#             [
#                 {'entries': ['some_entry'], 'events': ['SOME_EVENT']},
#                 {'entries': [entry], 'events': []},
#             ]
#         )
#
#     def test_split_by_called_with_correct_args(self):
#         journey = {'entries': ['some_entry'], 'events': ['SOME_EVENT']}
#         journeys = [1, 2, journey]
#         entry = {'some': 'data'}
#
#         def split_by(j, e):
#             self.assertEquals(j, journey)
#             self.assertEquals(e, entry)
#             return True
#
#         self.assertEquals(
#             journey_splitter(journeys, entry, split_by=split_by),
#             [
#                 1,
#                 2,
#                 {'entries': ['some_entry'], 'events': ['SOME_EVENT']},
#                 {'entries': [entry], 'events': []},
#             ]
#         )
#
#
# class TestCreateJourney(django.test.TestCase):
#
#     def test_create_journey(self):
#         car = cars_testing_data.create()['cars'][0]
#
#         start_dt = datetime(2012, 12, 12, 12, 12)
#         end_dt = datetime(2012, 12, 12, 12, 13)
#         start_odo = 400.5
#         end_odo = 402
#         entries = [
#             {
#                 'timestamp': start_dt,
#                 'odometer': start_odo,
#                 'user_id': 1,
#             },
#             {
#                 'haha': 'we dont care about this',
#             },
#             {
#                 'timestamp': end_dt,
#                 'odometer': end_odo,
#                 'user_id': 1,
#             },
#         ]
#
#         journey = create_journey(entries, car=car)
#         self.assertEquals(journey.start_datetime, start_dt)
#         self.assertEquals(journey.end_datetime, end_dt)
#         self.assertEquals(journey.speedometer_start, start_odo)
#         self.assertEquals(journey.speedometer_end, end_odo)
#         self.assertEquals(journey.car_id, car.id)
#         self.assertEquals(journey.user_id, 1)
#         self.assertEquals(float(journey.length), 1.5)
#         assert journey.pk, "Journey not saved!"
#
#
# def create_dummy_entries():
#
#     entry_data = [
#         # 1
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(10, 20),
#             timestamp=datetime(2012, 12, 12, 12, 12, 12),
#             odometer=1300,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(10, 21),
#             timestamp=datetime(2012, 12, 12, 12, 12, 13),
#             odometer=1305,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(10, 22),
#             timestamp=datetime(2012, 12, 12, 12, 12, 14),
#             odometer=1310,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(10, 23),
#             timestamp=datetime(2012, 12, 12, 12, 12, 15),
#             odometer=1330,
#         ),
#
#         # different unit
#         dict(
#             unit_id=9999,
#             user_id=6656,
#             location=(10, 20),
#             timestamp=datetime(2012, 12, 12, 12, 12, 15),
#             odometer=1400,
#         ),
#         dict(
#             unit_id=9999,
#             user_id=6656,
#             location=(11, 23),
#             timestamp=datetime(2012, 12, 12, 13, 45, 12),
#             odometer=1405,
#         ),
#         #/
#
#         # 2
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(12, 23),
#             timestamp=datetime(2012, 12, 12, 13, 45, 13),
#             odometer=1305,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(12.5, 23),
#             timestamp=datetime(2012, 12, 12, 13, 45, 14),
#             odometer=1306,
#         ),
#
#         # 3
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(13, 23),
#             timestamp=datetime(2012, 12, 12, 17, 45, 12),
#             odometer=1307,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(14, 23),
#             timestamp=datetime(2012, 12, 12, 17, 45, 13),
#             odometer=1337,
#         ),
#
#         # different date
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(13, 23),
#             timestamp=datetime(2012, 12, 13, 17, 45, 12),
#             odometer=1500,
#         ),
#         dict(
#             unit_id=123,
#             user_id=1,
#             location=(14, 23),
#             timestamp=datetime(2012, 12, 13, 17, 45, 13),
#             odometer=1600,
#         ),
#     ]
#
#     for item in entry_data:
#         geotrack.api.store(**item)
#
#
# class TestGetJourneyData(django.test.TestCase):
#
#     @skipIfNotGeoEnabled
#     def test_basic(self):
#         create_dummy_entries()
#
#         result = get_journey_data(
#             start=datetime(2012, 12, 12),
#             end=datetime(2012, 12, 13),
#             unit_id=123)
#
#         def only_take_keys(*keys):
#             return X.iteritems() | where(KEY._in_(keys)) | dict
#
#         # we'll trim the result to only a certain set of keys in the entries,
#         # so this test doesn't break whenever a new field is added to the model
#         result = result > foreach({
#             'entries': X['entries'] | foreach(only_take_keys(
#                 'event',
#                 'location',
#                 'odometer',
#                 'timestamp',
#                 'unit_id',
#                 'user_id'
#             )) | list,
#             'events': X['events'],
#         }) | list
#
#         from pprint import pprint
#         pprint(result)
#
#         self.assertEquals(result, [
#             {u'entries': [{'event': None,
#             'location': (10.0, 20.0),
#             'odometer': Decimal('1300.00'),
#             'timestamp': datetime(2012, 12, 12, 12, 12, 12),
#             'unit_id': 123,
#             'user_id': 1},
#             {'event': None,
#             'location': (10.0, 21.0),
#             'odometer': Decimal('1305.00'),
#             'timestamp': datetime(2012, 12, 12, 12, 12, 13),
#             'unit_id': 123,
#             'user_id': 1},
#             {'event': None,
#             'location': (10.0, 22.0),
#             'odometer': Decimal('1310.00'),
#             'timestamp': datetime(2012, 12, 12, 12, 12, 14),
#             'unit_id': 123,
#             'user_id': 1},
#             {'event': None,
#             'location': (10.0, 23.0),
#             'odometer': Decimal('1330.00'),
#             'timestamp': datetime(2012, 12, 12, 12, 12, 15),
#             'unit_id': 123,
#             'user_id': 1}],
#             u'events': []},
#
#             {u'entries': [{'event': None,
#             'location': (12.0, 23.0),
#             'odometer': Decimal('1305.00'),
#             'timestamp': datetime(2012, 12, 12, 13, 45, 13),
#             'unit_id': 123,
#             'user_id': 1},
#             {'event': None,
#             'location': (12.5, 23.0),
#             'odometer': Decimal('1306.00'),
#             'timestamp': datetime(2012, 12, 12, 13, 45, 14),
#             'unit_id': 123,
#             'user_id': 1}],
#             u'events': []},
#
#             {u'entries': [{'event': None,
#             'location': (13.0, 23.0),
#             'odometer': Decimal('1307.00'),
#             'timestamp': datetime(2012, 12, 12, 17, 45, 12),
#             'unit_id': 123,
#             'user_id': 1},
#             {'event': None,
#             'location': (14.0, 23.0),
#             'odometer': Decimal('1337.00'),
#             'timestamp': datetime(2012, 12, 12, 17, 45, 13),
#             'unit_id': 123,
#             'user_id': 1}],
#             u'events': []}
#         ])
#
#         geotrack.api.flush()
#
#
# class TestCreateJourneys(django.test.TestCase):
#
#     @skipIfNotGeoEnabled
#     def test_basic(self):
#         Car.objects.all().delete()
#         Journey.objects.all().delete()
#         create_dummy_entries()
#         car = cars_testing_data.create()['cars'][0]
#         u = unit(123, car)
#
#         result = create_journeys(
#             start=datetime(2012, 12, 12),
#             end=datetime(2012, 12, 13),
#             car=car,
#         )
#
#         self.assertEquals(len(result), 3)
#
#         geotrack.api.flush()
#         u.delete()
