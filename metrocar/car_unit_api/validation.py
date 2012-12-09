"""
Car-unit-API-specific validation
"""
from functools import partial

from geotrack.utils import extract_timestamp

from metrocar.utils.validation import field_validator, convertible_to


valid_timestamp = partial(field_validator,
    # check if geotrack will be able to handle the value
    test=convertible_to(extract_timestamp),
    message='"{value}" is not a valid timestamp')


def is_valid_location(val):
    return (len(val) == 2
        and convertible_to(float)(val[0])
        and convertible_to(float)(val[1]))


valid_location = partial(field_validator,
    test=is_valid_location,
    message='"{value}" is not a valid location')
