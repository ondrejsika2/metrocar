from functools import wraps
from pipetools import flatten, foreach, first_of, unless, maybe, X
from django.conf import settings
from django.utils.importlib import import_module


conf = {
    'QUERY_PACKAGES': []
}

conf.update(settings.GEOTRACK)

packages = (
    conf['QUERY_PACKAGES'],
    'geotrack.queries.builtin',
) > flatten | tuple


_query_cache = {}


def import_query(potential_module_names):
    query_module = first_of(potential_module_names >
        foreach(unless(ImportError, import_module)))
    try:
        return query_module and query_module.execute
    except AttributeError:
        raise NotImplementedError('The "%s" module does not provide the '
            'execute method.' % query_module)


def load_native_query(name, backend):
    name = '%s_%s' % (name, backend.__name__.split('.')[-1])
    return _load_query(name, wrap_native_query, backend)


def load_universal_query(name, backend):
    return _load_query(name, wrap_universal_query, backend)


def _load_query(name, wrap, backend):
    return (packages > maybe
        | foreach('{0}.' + name)
        | import_query
        | (wrap, backend))


def load_query(name, backend):

    query = (load_native_query(name, backend)
          or load_universal_query(name, backend))

    if not query:
        raise ImportError(
            'Failed to import Geotrack query "%s", maybe you forgot '
            'to specify the GEOTRACK["QUERY_PACKAGES"] setting?' % name)

    return query


def get_query(name, backend):
    key = name, backend.__name__
    if key not in _query_cache:
        _query_cache[key] = load_query(name, backend)
    return _query_cache[key]


universal_query_args = 'start', 'end', 'in_polygon', 'units'


def wrap_universal_query(backend, query):

    @wraps(query)
    def wrapper(**kwargs):
        q_args = universal_query_args > foreach((X, kwargs.get)) | dict
        native_results = backend.query(**q_args)
        pre_results = backend.transform(native_results)
        return query(pre_results, **kwargs)
    return wrapper


def wrap_native_query(backend, query):

    @wraps(query)
    def wrapper(**kwargs):
        return query(backend, **kwargs)
    return wrapper
