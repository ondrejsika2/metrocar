from pipetools import where, X, foreach, pipe, maybe

from django.forms import model_to_dict

from geotrack.backends.geodjango.models import get_storage_model, LastKnownPosition


__all__ = 'store', 'query', 'query_last_position', 'transform'


def store(**kwargs):
    data = dict(kwargs, location=encode_location(kwargs['location']))
    get_storage_model().objects.create(**data)


def query(start=None, end=None, in_polygon=None, units=None, model=None):
    model = model or get_storage_model()
    lookup = (
        ('timestamp__gte', start),
        ('timestamp__lte', end),
        ('location__within', in_polygon > maybe | encode_polygon),
        ('unit_id__in', units),
    ) > where(X[1]) | dict
    return model.objects.filter(**lookup)


def query_last_position(**kwargs):
    return query(model=LastKnownPosition, **kwargs) > foreach([X.unit_id, {
        'timestamp': X.timestamp,
        'location': X.location | decode_location,
    }]) | dict


encode_location = pipe | 'POINT({0} {1})'
encode_polygon = foreach('{0} {1}') | ', '.join | 'POLYGON(({0}))'
decode_location = ~X.coords


def transform_entry(instance):
    return dict(model_to_dict(instance, exclude=['id']),
        location=decode_location(instance.location))


transform = foreach(transform_entry) | tuple
