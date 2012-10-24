

def execute(backend, query, **kwargs):
    return backend.query_last_position(**kwargs)
