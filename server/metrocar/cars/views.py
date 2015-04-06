from datetime import datetime
from django.shortcuts import _get_queryset
from django.utils.dateparse import parse_datetime
from pipetools import as_kwargs, foreach, where, X, maybe, group_by
from django.conf import settings

from metrocar.cars.models import FuelBill, Journey, Parking
from metrocar.car_unit_api.utils import get_current_car_position_data
from metrocar.cars.models import CarColor, CarModel
from metrocar.cars.utils import grouping_precision
from metrocar.cars.validation import valid_car_id
from metrocar.utils.apis import APICall, process_request, parse_json_optional, validate_request
from metrocar.utils.geo.validation import valid_polygon
from metrocar.utils.validation import optional
from metrocar.user_management.models import Account


def get_car_position_data(in_polygon=None, car_id=None):
    """
    Returns Cars and their positions, including a timestamp indicating when
    the position was last updated.

    Returns a sequence of mappings::

        {
            'car': Car,
            'location': (x, y),
            'timestamp': datetime,
        }
    """
    if car_id:
        return [car_position_data(Car.objects.get(id=car_id))]

    if settings.GEO_ENABLED:
        # In a GEO_ENABLED instance we'll use car_unit_api to retrieve the
        # positions. We could use Car.last_position lookup, but car_unit_api
        # might provide better optimization
        return get_current_car_position_data(in_polygon)

    else:
        # We still might have car positions, cannot filter by location,
        # but the geo-disabled version won't be run with a lot of cars
        # anyway so we can just return all of them
        return _get_position_data_from_cars()


def _get_position_data_from_cars():
    return Car.objects.all() > foreach(car_position_data)


def car_position_data(car):
    return {
        'car': car,
        'location': car.last_position > maybe | X.coords,
        'timestamp': car.last_echo,
    }


class CarPositions(APICall):
    """
    Returns a list of cars and their current positions.

    Accepts optional JSON content::

        {
            in_polygon: [(x, y), (x, y), ...],
            car_id: 123
        }
    """
    rules = (
        optional('in_polygon', valid_polygon),
        optional('car_id', valid_car_id),
    )

    @staticmethod
    def filter(car):
        """
        Override to filter out which cars should be displayed by this view.

        Returns True if `car` should be included in the result.
        """
        return True

    @staticmethod
    def get_car_data(cars):
        """
        Override to specify data to send to the front-end application for
        given `car`.
        """
        return [{
            'name': unicode(car),
        } for car in cars]

    @process_request(maybe | parse_json_optional | (validate_request, rules))
    def get(self, request, data):
        bounds = data > maybe | X.get('in_polygon')
        return ((data or {}) > as_kwargs(get_car_position_data)
            | where(X['car'] | self.filter)
            | group_by(X['location'] | (grouping_precision, X, bounds))
            | X.iteritems()
            | foreach({
                'location': X[1][0]['location'],
                'cars': X[1] | foreach(X['car']) | self.get_car_data,
              })
            | tuple)

    # POST with JSON content is easier to do in jQuery than GET
    post = get

from rest_framework import viewsets, generics
from metrocar.cars.models import Car
from metrocar.cars.serializers import CarSerializer, CarModelSerializer, CarColorSerializer, FuelBillSerializer, \
    JourneySerializer, ParkingSerializer
from metrocar.user_management.permissions import IsAdminOrReadOnly, IsAdminUserOrOwner, IsAccountOwner


class CarViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAdminOrReadOnly,
    )
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):

        reserved_from = self.request.QUERY_PARAMS.get('reserved_from', None)
        reserved_until = self.request.QUERY_PARAMS.get('reserved_until', None)

        print reserved_from
        print reserved_until

        if reserved_from is not None and reserved_until is not None:
            reserved_from = (datetime.strptime(reserved_from,'%Y-%m-%d, %X'))
            reserved_until = (datetime.strptime(reserved_until,'%Y-%m-%d, %X'))
            print reserved_from
            print reserved_until
            return Car.list_of_available_cars(datetime_start=reserved_from,datetime_end=reserved_until)

        return Car.objects.all()

class CarModelViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAdminOrReadOnly,
    )
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

class CarColorViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAdminOrReadOnly,
    )
    queryset = CarColor.objects.all()
    serializer_class = CarColorSerializer

class FuelBillViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAccountOwner,
    )
    queryset = FuelBill.objects.all()
    serializer_class = FuelBillSerializer

    def get_queryset(self):
        account = Account.objects.get(user=self.request.user)
        return FuelBill.objects.filter(account=account)

class JourneyListView(generics.ListAPIView):
    permission_classes = (
        IsAdminOrReadOnly,
        IsAdminUserOrOwner
    )
    serializer_class = JourneySerializer
    def get_queryset(self):
        return Journey.objects.filter(user=self.request.user)


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
