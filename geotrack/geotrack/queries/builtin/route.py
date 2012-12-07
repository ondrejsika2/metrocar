from pipetools import group_by, X


def execute(backend, query, **kwargs):
    return query(**kwargs) > group_by(X['unit_id'])
