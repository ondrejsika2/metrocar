from random import randint
from datetime import datetime, time

from metrocar.tarification.models import Pricelist, PricelistDay, PricelistDayTime

from metrocar.cars import testing_data as cars_testing_data


def create_pricelist(
    car_model,
    pickup_fee,
    price_per_hour,
    price_per_km,
    reservation_fee,
    name=None,
    **kwargs):

    name = name or ('%s testing price list' % car_model.name)

    defaults = dict(
        description="%s's description" % name,
        valid_from=datetime.now(),
        available=True,
    )

    pl, created = Pricelist.objects.get_or_create(
        model=car_model,
        name=name,
        defaults=dict(defaults,
            pickup_fee=pickup_fee,
            price_per_hour=price_per_hour,
            price_per_km=price_per_km,
            reservation_fee=reservation_fee,
            **kwargs))

    if created:
        day = PricelistDay.objects.create(pricelist=pl, weekday_from=0)
        PricelistDayTime.objects.create(
            pricelist_day=day,
            car_unused_ratio=1,
            car_used_ratio=1,
            late_return_ratio=1,
            time_from=time(0, 0),
        )

    return pl


def create():

    models = cars_testing_data.create()['car_models']

    return {
        'pricelists': [create_pricelist(model,
            randint(0, 100),
            randint(2, 20),
            randint(2, 20),
            randint(0, 100),
        ) for model in models],
    }
