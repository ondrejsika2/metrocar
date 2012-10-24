from pipetools import foreach, X


def average(seq):
    return sum(seq) / float(len(seq))


def execute(backend, query, field, **kwargs):
    return query(**kwargs) > foreach(X[field]) | tuple | average
