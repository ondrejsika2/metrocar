

def execute(backend, **kwargs):
    return backend.query(**kwargs).count()
