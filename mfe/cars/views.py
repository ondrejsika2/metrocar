# encoding: utf-8
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.translation import gettext_lazy as _
from django.views.generic import list_detail
from django.views.generic.base import TemplateView

from metrocar.cars.models import CarType, Car, Parking
from metrocar.cars.views import CarPositions


def car_list(request, **kwargs):
    cars = Car.objects.filter(active=True)
    return list_detail.object_list(request, cars, **kwargs)

@login_required
def load_car_list(request, start_date=None, start_time=None, end_date=None, end_time=None):
    if request.is_ajax():
        datetime_start = datetime.strptime(start_date + ' ' + start_time, '%d.%m.%Y %H:%M')
        datetime_end = datetime.strptime(end_date + ' ' + end_time, '%d.%m.%Y %H:%M')
        cars = Car.list_of_available_cars(datetime_start, datetime_end, home_subsidiary=request.user.home_subsidiary)
        carsCount = len(cars)
        result = []
        keys = []
        if len(cars) > 0:
            for c in cars:
                keys.append(c.id)
                result.append('<option value="' + unicode(c.id) + '">'+ c.__unicode__() + '</option>')
        else:
            result.append('<option value="0">%s</option>' % _('No car is available in chosen time.'))

        data = simplejson.dumps({'count' : carsCount, 'data' : ''.join(result), 'keys' : keys})

        return HttpResponse(data, 'application/javascript')
    else:
        return HttpResponseNotFound()

def car_detail(request, id=None):
    if id is None:
        return HttpResponseNotFound()
    car = Car.objects.filter(active=True).get(pk=id)
    pricelist = car.model.get_pricelist()
    context = { 'object': car }

    if pricelist:
        context.update({
            'timeline': pricelist.get_pricing_summary()['timeline'],
            'color': 'green',
            'distance': '0'
        })
    template_name = 'cars/car_detail.html'
    if request.is_ajax():
        template_name = 'cars/car_detail_ajax.html'
    return render_to_response(template_name, context, context_instance=RequestContext(request))

def parking_list(request, **kwargs):
    return list_detail.object_list(request, Parking.objects.all(), **kwargs)

def fares(request):
    c = RequestContext(request)
    return render_to_response('cars/fares.html', { 'car_types': CarType.objects.all() }, context_instance=c)

FEED_TYPES = {
    'car': (Car, 'last_position'),
    'parking': (Parking, 'polygon')
}

def geo_feed(request, type=None):
    if type is None:
        return HttpResponse('No feed type supplied')
    if not FEED_TYPES.has_key(type):
        return HttpResponse('Invalid feed type. Possible feed types: %s' %
            ", ".join(list(FEED_TYPES)))
    if not request.GET.has_key('bbox'):
        return HttpResponse('No bounding box supplied')
    try:
        bbox = request.GET['bbox'].split(',')
    except:
        return HttpResponse('Invalid bbox')
    poly = Polygon.from_bbox(bbox)
    kwargs = { '%s__contained' % FEED_TYPES[type][1]: poly }
    return render_to_response('cars/geo_feed.html', {
        'objects': FEED_TYPES[type][0].objects.filter(**kwargs),
        'type': type
    })

def geo_details(request, type=None, id=None):
    if type is None:
        return HttpResponse('No feed type supplied')
    if not FEED_TYPES.has_key(type):
        return HttpResponse('Invalid feed type. Possible feed types: %s' %
            ", ".join(list(FEED_TYPES)))
    if id is None:
        return HttpResponse('No object id supplied')
    return render_to_response('cars/geo_detail_%s.html' % type, {
        'object': FEED_TYPES[type][0].objects.get(pk=id)
    });


class CarMap(TemplateView):
    template_name = 'cars/car_map.html'


class CarMapData(CarPositions):

    def filter(self, car):
        return True

    def get_car_data(self, cars):
        return render_to_string('cars/car_popup.html', {'cars': cars})
