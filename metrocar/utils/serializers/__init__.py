__author__="Xaralis"
__date__ ="$28.10.2009 17:20:38$"

from django.core import serializers

def to_dict(queryset, **kwargs):
    # check if queryset is iterable
    try:
        iter(queryset)
    except TypeError:
        queryset = (queryset,)
    return serializers.serialize('python_deep', queryset, **kwargs)