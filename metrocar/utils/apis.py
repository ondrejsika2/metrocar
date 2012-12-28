from functools import wraps

from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.base import View

from metrocar.utils.validation import validate
from metrocar.utils.views import JsonResponse


class APICall(View):
    """
    Base for an API view. Automatically converts responses that are not already
    an instance of an HttpResponse to JSON-responses.
    """
    def dispatch(self, request, *args, **kwargs):
        response = super(APICall, self).dispatch(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response)


class InvalidRequest(Exception):
    "An exception that is risen on an invalid API request from a client. "


def process_request(process):
    """
    Decorator to process an incoming request using the supplied `process`
    function.

    The `process` function is supposed to take the request object and any URL
    parameters if present and either:

    *   return a value -- presumably cleaned data for the decorated method

    *   or raise an ``InvalidRequest`` exception with a message explaining
        what was wrong with the request, which will be directly returned to
        the client.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(view, request, *args, **kwargs):
            try:
                clean_data = process(request, *args, **kwargs)
            except InvalidRequest, e:
                return JsonResponse({
                    'status': 'error',
                    'message': unicode(e),
                }, status=400)
            return view_func(view, request, clean_data)
        return wrapped
    return decorator


def parse_json(request):
    """
    Parse raw JSON data from a request.
    """
    raw_data = request.body
    if not raw_data:
        raise InvalidRequest('Missing JSON data.')
    try:
        return json.loads(request.body)
    except ValueError, ex:
        raise InvalidRequest('Invalid JSON (%s).' % ex)


def parse_json_optional(request):
    """
    Parse JSON data from a request if there are any.
    """
    return parse_json(request) if request.body else None


def validate_request(rules, data):
    valid, error = validate(rules)(data)
    if not valid:
        raise InvalidRequest(error)
    return data
