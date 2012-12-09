"""
The public API
"""
from datetime import datetime
from pipetools import pipe, X
from geotrack.backends import get_backend
from geotrack.queries import get_query
from geotrack.utils import extract_timestamp


def store(unit_id, timestamp, location, **kwargs):
    if isinstance(timestamp, basestring):
        timestamp = extract_timestamp(timestamp)
    backend = get_backend()
    backend.store(
        unit_id=unit_id,
        timestamp=timestamp,
        location=location,
        added=datetime.now(),
        **kwargs)


def query(query_name, **kwargs):
    backend = get_backend()
    query = get_query(query_name, backend=backend)
    return query(**kwargs)


flush = pipe | get_backend | X.flush()
