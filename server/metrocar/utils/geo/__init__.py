"""
Various utilities for dealing with geographic data.
"""
from datetime import timedelta
from decimal import Decimal
from functools import partial
from pipetools import pipe, maybe, X, where, foreach, unless

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import geotrack

if settings.GEO_ENABLED:
    from django.contrib.gis.db.models import GeoManager
else:
    from django.db.models import Manager as GeoManager


def get_car_last_position(car):
    """
    Returns car's last known position.

    First attempts to get it from a CarUnit assigned to `car` and if that fails
    (no CarUnit or it doesn't know the position) it falls back to the car's
    last_position attribute, which might have been filled out manually.
    """
    from metrocar.car_unit_api.models import CarUnit
    from_car_unit = CarUnit.objects.get_for(car) > maybe | X.get_last_position()
    return from_car_unit or car.last_position


def journey_splitter(journeys, entry, split_by):
    """
    A reducer function for splitting a sequence of (timestamp-ordered) entries
    into "journeys" using `split_by` function.

    Entries should be dictionaries containing:
    - timestamp
    - location
    - event (optional)

    Journeys are dictionaries containing:
    - entries = sequence of entries
    - events = sequence of events from entries (without None values)

    The `split_by` function should take a journey and an entry and return
    whether the journey should be split at that point (True) or that the entry
    still belongs to it (False).
    """
    last_journey = journeys > unless(IndexError, X[-1])
    event = entry.get('event')

    if (not last_journey) or split_by(last_journey, entry):
        # create new journey
        journeys.append({
            'entries': [entry],
            'events': [event] if event else [],
        })
    else:
        # append entry to last journey
        last_journey['entries'].append(entry)
        if event:
            last_journey['events'].append(event)

    return journeys


def split_by_events(journey, entry):
    """
    Returns whether the last two events in `journey` were ENGINE_OFF and LOCKED

    -- where we only care about events: ENGINE_OFF, ENGINE_ON, UNLOCKED, LOCKED
    """
    from metrocar.car_unit_api.models import Events

    events_of_interest = (
        Events.ENGINE_OFF,
        Events.ENGINE_ON,
        Events.UNLOCKED,
        Events.LOCKED,
    )
    events = journey['events'] > where(X._in_(events_of_interest)) | tuple
    return (len(events) >= 2 and
        (events[-2], events[-1]) == (Events.ENGINE_OFF, Events.LOCKED))


def split_by_idle_time(journey, entry, idle_after=timedelta(minutes=10)):
    """
    Returns if the time between the last entry in `journey` and `entry` is
    greater than `idle_after`.
    """
    t1 = journey['entries'][-1]['timestamp']
    t2 = entry['timestamp']
    return (t1 + idle_after) < t2


def split_by_any(*functions):
    """
    Returns a `split_by` function for `journey_splitter` that returns True
    if any of `functions` do.
    """
    def splitter(*args, **kwargs):
        for f in functions:
            if f(*args, **kwargs):
                return True
    return splitter


def split_entry_data_to_journeys(entries, reducer=None, split_by=None):
    """
    Splits Geotrack data to journey-segments using `reducer`.
    """
    split_by = split_by or split_by_any(split_by_events, split_by_idle_time)
    reducer = reducer or partial(journey_splitter, split_by=split_by)
    return reduce(reducer, entries, [])


def get_journey_data(start, end, unit_id, **splitter_kwargs):
    """
    Extracts data from Geotrack for `start`, `end` and `unit_id` and splits
    them into journey-segments.
    """
    entries = geotrack.api.query('all', start=start, end=end, units=[unit_id])
    return split_entry_data_to_journeys(entries, **splitter_kwargs)


def distance(entries):
    """
    Returns distance traveled between given (time-sorted) `entries`.

    If the `entries` contain `odometer` keys, that will be used for the
    computation (difference between the first and last entry).

    (TODO: Otherwise the distance will be calculated from entries' locations.)
    """
    if len(entries) < 2:
        return 0
    odo_start = entries[0].get('odometer') > maybe | str | Decimal
    odo_end = entries[-1].get('odometer') > maybe | str | Decimal
    if odo_start and odo_end:
        if odo_end < odo_start:
            raise ValueError("Last entry's odometer is less then first one's, "
                "something is wrong (ordering?)")
        return odo_end - odo_start

    raise NotImplementedError('TODO: compute distances from locations with geopy')


def create_journey(entries, user=None, **kwargs):
    """
    Creates a Journey object from a sequence of `entries`.

    `entries` should be dictionaries with the usual keys
    (location, timestamp, etc.), they are expected to be ordered by the
    timestamps
    """
    from metrocar.cars.models import Journey
    return Journey.objects.create(
        start_datetime=entries[0]['timestamp'],
        end_datetime=entries[-1]['timestamp'],
        length=distance(entries),
        user_id=user.id if user else entries[0]['user_id'],
        odometer_start=entries[0].get('odometer'),
        odometer_end=entries[-1].get('odometer'),
        **kwargs)


def create_journeys(start, end, car, user=None, split_by=None, **kwargs):
    from metrocar.car_unit_api.models import CarUnit

    unit = CarUnit.objects.get_for(car)
    if not unit:
        raise ImproperlyConfigured("No CarUnit associated with %s" % car)

    return (get_journey_data(start, end, unit.unit_id, split_by=split_by) > pipe
        | foreach(X['entries'])
        | foreach(create_journey, car=car, user=user, **kwargs)
        | tuple)
