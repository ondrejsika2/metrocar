from pipetools import group_by, X


def execute(pre_results, **kwargs):
    return pre_results > group_by(X['unit_id'])
