'''
Created on 10.3.2010

@author: xaralis
'''
import json as simplejson

from django import shortcuts
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context, Template
from django.db.models import Q

from metrocar.cars.models import Car
from metrocar.utils.nominatim import NominatimQuerier

def index(request):
    return shortcuts.render_to_response(
        "index.html", {},
        context_instance=RequestContext(request)
    )
    
def search(request):
    """
    Search function implemented by Google custom search
    """
    search_query = request.POST.get('search_query', '')
    
    return render_to_response(
        'search.html',
        {'search_query': search_query},
        context_instance=RequestContext(request))
        
    
#----------------------------------------------------------
    """
    First tries to search a car or car model
    If nothing found uses nominatim service to search for a location. 
    Returns results as json object with common structure (nominatim style)
    """
    #if request.method != 'POST' or not request.POST.has_key('q'):
        #return HttpResponseNotFound()
    
    #query = request.POST.get('q')
    
    #cars = Car.objects.filter(
        #Q(model__name__startswith=query) | 
        #Q(model__manufacturer__name__startswith=query)
    #)
    
    #results = []
    #if len(cars) != 0:
        #for c in cars:
            #results.append({
                #'display_name': c.__unicode__(),
                #'lon': c.last_position.y,
                #'lat': c.last_position.x,
                #'boundingbox': [ # make small bounding box
                    #c.last_position.y - 0.01,
                    #c.last_position.y + 0.01,
                    #c.last_position.x - 0.01,
                    #c.last_position.x + 0.01
                #]
            #})
    #else:
        #nq = NominatimQuerier()
        #results = nq.search_location(query)
    #return HttpResponse(simplejson.dumps(results), mimetype='application/json')
