from django.db.models.aggregates import Avg


def execute(backend, field, **kwargs):
    return backend.query(**kwargs).aggregate(x=Avg(field))['x']
