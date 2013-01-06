from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

import geotrack.api

from metrocar.car_unit_api.models import CarUnit
from metrocar.cars.models import Car
from metrocar.cars.views import CarPositions as CarPositionsBase
from metrocar.utils.apis import APICall, process_request, parse_json


class UsageHistory(TemplateView):
    """
    A view containing a JavaScript interface for usage history.
    """
    template_name = 'audit/usage_history.html'

    def get(self, request):
        return self.render_to_response(dict(units=CarUnit.objects.all()))


class UsageQuery(APICall):
    """
    An API endpoint for UsageHistory view's JS application.

    Returns results of :func:`~metrocar.utils.geo.queries.usage_history` query.
    """

    # the maximum number of entries we will process
    threshold = 1000

    @process_request(parse_json)
    # using POST because it's easier to do with jQuery...
    def post(self, request, params):
        request_id = params.pop('request_id')

        if geotrack.api.query('count', **params) > self.threshold:
            return dict(request_id=request_id, status='too-much')

        results = geotrack.api.query('usage_history', max_items=200, **params)

        return dict(request_id=request_id, status='ok', results=results)


class CarPositionsMap(TemplateView):
    """
    A view containing a JavaScript interface for displaying car positions.
    """
    template_name = 'audit/car_positions.html'

    def get(self, request):
        return self.render_to_response(dict(
            cars=Car.objects.exclude(_last_position=None)))


class CarPositions(CarPositionsBase):
    """
    An API endpoint for car positions JS application.
    """

    def get_car_data(self, cars):
        return render_to_string('audit/car_popup.html', {'cars': cars})
