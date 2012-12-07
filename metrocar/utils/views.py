from datetime import datetime

from django.http import HttpResponse
from django.utils import simplejson as json


class DateTimeJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        return (obj.isoformat() if isinstance(obj, datetime)
            else super(DateTimeJSONEncoder, self).default(obj))


def JsonResponse(content, pretty=True, **response_kwargs):
    kwargs = {'content_type': 'application/json'}
    kwargs.update(response_kwargs)
    indent = 2 if pretty else None
    serialized_content = json.dumps(content,
        cls=DateTimeJSONEncoder,
        indent=indent,
        ensure_ascii=False,
    )
    return HttpResponse(serialized_content, **kwargs)
