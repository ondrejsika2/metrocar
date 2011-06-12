# Create your views here.

import urllib
import base64

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse

def request_generator(request):
    return render_to_response('app/request_generator.html',
        context_instance=RequestContext(request))
    
def http_proxy(request, url):
    """Simple HTTP proxy gate"""
    data = request.raw_post_data
    f = urllib.urlopen(base64.decodestring(url) + urllib.urlencode(request.GET), data)
    return HttpResponse(f.readlines())
    
