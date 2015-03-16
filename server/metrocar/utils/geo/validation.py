from collections import Iterable
from functools import partial

from metrocar.utils.validation import field_validator, convertible_to


def is_valid_location(val):
    return (len(val) == 2
        and convertible_to(float)(val[0])
        and convertible_to(float)(val[1]))


valid_location = partial(field_validator,
    test=is_valid_location,
    message='"{value}" is not a valid location')


def is_valid_polygon(val):
    return (isinstance(val, Iterable)
        and len(val) >= 3
        and all(is_valid_location(x) for x in val))


valid_polygon = partial(field_validator,
    test=is_valid_polygon,
    message='"{value}" is not a valid polygon')
