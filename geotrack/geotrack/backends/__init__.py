from logging import getLogger

from django.conf import settings
from django.utils import importlib


logger = getLogger('geotrack')

backends = {}


def get_backend(path=settings.GEOTRACK['BACKEND']):
    """
    Returns a backend by importing it from `path`, defaults to currently set
    backend -- defined by ``GEOTRACK['BACKEND']`` setting.
    """
    if path not in backends:
        try:
            backends[path] = importlib.import_module(path)
        except ImportError, ex:
            logger.error('Cannot import backend: "%s": %s' % (path, ex))
            raise
    return backends[path]
