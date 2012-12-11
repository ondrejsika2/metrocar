from pipetools import pipe, count


def execute(backend, query, **kwargs):
    return query(**kwargs) > pipe | count
