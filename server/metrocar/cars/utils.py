# encoding: utf-8
from datetime import datetime, date, time
from decimal import Decimal
from django.contrib.gis.geos import Polygon
from pipetools import maybe, foreach, X

from django.conf import settings

from olwidget.widgets import InfoMap, MapDisplay

from metrocar.cars.models import Car, CarModelManufacturer, Fuel, CarType, CarColor, CarModel, FuelBill, Parking
from metrocar.subsidiaries.models import Subsidiary
from metrocar.tarification.models import Pricelist, PricelistDay, PricelistDayTime


def get_car_infomap(width='100%', height='400px'):
    """
    Returns olwidget.widgets.InfoMap instance with available cars on it.
    """
    return InfoMap([
                       [c.last_position, c.__unicode__()] for c in Car.objects.all()],
                   options={
                       'default_zoom': 8,
                       'map_div_style': {'width': width, 'height': height},
                       'popupOutside': True,
                       'overlayStyle': {
                           'externalGraphic': settings.STATIC_URL + "img/marker.png",
                           'backgroundGraphic': settings.STATIC_URL + "img/marker_shadow.png",
                           'graphicXOffset': -10,
                           'graphicYOffset': -12,
                           'graphicWidth': 21,
                           'graphicHeight': 25,
                           'backgroundXOffset': 2,
                           'graphicOpacity': 1
                       }
                   }
    )


def get_map_for_geometry(geometry, width, height):
    """
    Returns basic MapDisplay instance for any GEOS geometry.
    """
    return MapDisplay(
        fields=[geometry],
        options={
            'default_zoom': 11,
            'map_div_style': {'width': width, 'height': height}
        }
    )


# TODO: smarter grouping.... probably best idea would be to send zoom level
# from the browser

def get_grouping_precision(bounds):
    x_min = min(x for (x, y) in bounds)
    x_max = max(x for (x, y) in bounds)
    dx = x_max - x_min
    return (
        20 if dx < .06 else
        2 if dx < .25 else
        1 if dx < 1.5 else
        0)


def grouping_precision(location, bounds=None, default=2):
    """
    Limit `location` precision to a level suitable for grouping locations
    for a view of given bounds (polygon). If no bounds given `default`
    precision will be used.
    """
    precision = get_grouping_precision(bounds) if bounds else default
    return tuple((round((n * 5), precision) / 5) for n in location)


# model factories:

def manufacturer(slug, name=None):
    return CarModelManufacturer.objects.get_or_create(
        slug=slug, defaults={'name': slug.capitalize()})[0]


def fuel(title):
    return Fuel.objects.get_or_create(title=title)[0]


def car_type(type):
    return CarType.objects.get_or_create(type=type)[0]


def color(color):
    return CarColor.objects.get_or_create(color=color)[0]


def car_model(make, name, **kwargs):
    defaults = dict(
        type=car_type('Hatchback'),
        engine='(unknown)',
        seats_count=5,
        storage_capacity=200,
        main_fuel=fuel('Natural'),
    )
    defaults.update(kwargs)
    return CarModel.objects.get_or_create(
        name=name,
        manufacturer=make,
        defaults=defaults,
    )[0]


def pricelist(car_model):
    pricelist_obj = Pricelist.objects.get_or_create(
        available=True,
        name='Test pricelist',
        pickup_fee=100,
        price_per_hour=10,
        price_per_km=50,
        reservation_fee=200,
        valid_from=date(day=1, month=1, year=2000),
        model=car_model
    )[0]

    pricelist_day = PricelistDay.objects.get_or_create(
            weekday_from=0,
            pricelist=pricelist_obj
        )[0]
    pricelist_day_time = PricelistDayTime.objects.get_or_create(
        car_unused_ratio=Decimal('0.5'), car_used_ratio=Decimal('1.6'),
        late_return_ratio=Decimal('5'), time_from=time(hour=0),
        pricelist_day=pricelist_day
    )[0]

    return pricelist_obj

def car(model, registration_number, parking, **kwargs):
    defaults = dict(
        active=True,
        manufacture_date=datetime(2000, 1, 1),
        color=color(u'Šedá'),
        home_subsidiary=Subsidiary.objects.get_current(),
        parking=parking
    )
    defaults.update(**kwargs)
    return Car.objects.get_or_create(
        model=model,
        registration_number=registration_number,
        defaults=defaults,
    )[0]


def fuel_bill_1(account, car, fuel):
    return FuelBill.objects.get_or_create(
        account=account,
        datetime=datetime(2015, 5, 10),
        money_amount=1000,
        car=car,
        fuel=fuel,
        liter_count=10,
        place="Praha",
        approved=True,
        image="fuelbill.jpg",
    )[0]


def fuel_bill_2(account, car, fuel):
    return FuelBill.objects.get_or_create(
        account=account,
        datetime=datetime(2015, 4, 24),
        money_amount=1500,
        car=car,
        fuel=fuel,
        liter_count=10,
        place="Praha",
        image="fuelbill.jpg",
    )[0]


def fuel_bill_3(account, car, fuel):
    return FuelBill.objects.get_or_create(
        account=account,
        datetime=datetime(2015, 3, 12),
        money_amount=2000,
        car=car,
        fuel=fuel,
        liter_count=10,
        place="Praha",
        approved=True,
        image="fuelbill.jpg",
    )[0]


def parking_1():
    return Parking.objects.get_or_create(
        name="Praha - Na Knížecí",
        places_count=20,
        land_registry_number="3",
        street="Za Ženskými domovy",
        city="Praha",
        polygon=Polygon((
            (14.4041007737154345, 50.0681585661877833),
            (14.4053506831159410, 50.0683479467924215),
            (14.4053721407868256, 50.0680414941669412),
            (14.4041544178972245, 50.0678555556647069),
            (14.4041007737154345, 50.0681585661877833)
        ))
    )[0]


def parking_2():
    return Parking.objects.get_or_create(
        name="Praha - Dejvice",
        places_count=20,
        land_registry_number="1903/7",
        street="Šolínova",
        city="Praha",
        polygon=Polygon((
            (14.3935704211271549, 50.1023107272912966),
            (14.3945145586924124, 50.1017739535571422),
            (14.3947076777486220, 50.1019391153467382),
            (14.3946433047268716, 50.1024139523198357),
            (14.3941819647797189, 50.1025997568106760),
            (14.3935704211271549, 50.1023107272912966)
        ))
    )[0]


def parking_3():
    return Parking.objects.get_or_create(
        name="Praha - Karlovo Náměstí",
        places_count=20,
        land_registry_number="293/13",
        street="Karlovo náměstí",
        city="Praha",
        polygon=Polygon((
            (14.4166105965539693, 50.0766805985855754),
            (14.4168037156029918, 50.0763156732595718),
            (14.4169324616356764, 50.0763501002961178),
            (14.4166964272421243, 50.0770042092863648),
            (14.4164603928494692, 50.0769697827200631),
            (14.4164818505212846, 50.0766943692980107),
            (14.4164925793576391, 50.0766805985855754),
            (14.4166105965539693, 50.0766805985855754)
        ))
    )[0]


def parking_4():
    return Parking.objects.get_or_create(
        name="Praha - Sokolovská",
        places_count=20,
        land_registry_number="1",
        street="Sokolovská",
        city="Praha",
        polygon=Polygon((
            (14.4982302168733881, 50.1098978192946873),
            (14.4987022856515306, 50.1091478295513539),
            (14.4989919642313616, 50.1091478295513539),
            (14.4991314390968142, 50.1097120431132055),
            (14.4989383200495716, 50.1100904753138892),
            (14.4988954047077421, 50.1100973558718863),
            (14.4982302168733881, 50.1098978192946873)
        ))
    )[0]

