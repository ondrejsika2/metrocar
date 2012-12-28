from itertools import groupby
from pipetools import pipe, foreach, X

from geotrack.queries.builtin.sparse_route import prune_to

from metrocar.utils.geo import split_entry_data_to_journeys


def prune_journeys_to(max_items, journeys):
    """
    For each journey we need first and last entry and overall at most
    `max_items` worth of entries.
    """
    entry_count = X['entries'] | len
    total_entries = journeys > foreach(entry_count) | sum

    for j in journeys:
        journey_max_items = max(2,
            max_items * (entry_count(j) / float(total_entries)))
        yield dict(j, entries=prune_to(journey_max_items)(j['entries']))


def group_by_location(entries):
    """
    Some entries could be on the same location, especially ones containing
    interesting events, like ENGINE_OFF, LOCKED, etc. Grouping will make
    displaying them on a map much easier.

    This function assumes that `entries` are sorted by timestamp.
    """
    return groupby(entries, ~X['location']) > foreach({
        'location': X[0],
        'entries': X[1] | tuple
    }) | tuple


def process_raw_results(data, max_items):
    return (data > pipe
        | split_entry_data_to_journeys
        | (prune_journeys_to, max_items)
        | foreach({
            'entries': X['entries'] | group_by_location,
            'events': X['events'],
          })
    )


def execute(backend, query, units=None, max_items=50, **kwargs):
    if not units or len(units) != 1:
        raise NotImplementedError(
            'usage_history is only implemented for a single unit')
    return (query(units=units, **kwargs) > pipe
        | (process_raw_results, X, max_items)
        | tuple)
