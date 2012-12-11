from pipetools import pipe, group_by, X, foreach, KEY, VALUE


r_int = pipe | round | int


def prune_to(max):
    def f(seq):
        if max > len(seq):
            return seq
        take_every_xth = len(seq) / float(max)
        indexes = xrange(r_int(max) - 1) > foreach((X * take_every_xth) | r_int)
        return [seq[i] for i in indexes] + [seq[-1]]
    return f


def execute(backend, query, max_items=50, **kwargs):
    return (query(**kwargs)
        > group_by(X['unit_id'])
        | X.iteritems()
        | foreach([KEY, VALUE | prune_to(max_items)])
        | dict)
