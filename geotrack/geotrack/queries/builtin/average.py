from pipetools import foreach, X


def average(seq):
    return sum(seq) / float(len(seq))


def execute(pre_results, field, **kwargs):
    return pre_results > foreach(X[field]) | tuple | average
