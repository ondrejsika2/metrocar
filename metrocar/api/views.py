'''
Created on 28.3.2010

@author: xaralis
'''

from django.shortcuts import render_to_response
from django.template import RequestContext

from piston.handler import typemapper
from piston.doc import generate_doc

def documentation(request):
    """
    Outputs API documentation dynamically from defined handlers.
    """
    docs = [ ]

    for handler, (model, anonymous) in typemapper.iteritems():
        docs.append(generate_doc(handler))
        
    return render_to_response('api/api_documentation.html', 
        { 'docs': docs }, RequestContext(request))