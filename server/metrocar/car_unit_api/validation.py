"""
Car-unit-API-specific validation
"""
from functools import partial

from django.contrib.auth.models import User

from geotrack.utils import extract_timestamp

from metrocar.utils.validation import field_validator, convertible_to, valid_int, validate


valid_timestamp = partial(field_validator,
    # check if geotrack will be able to handle the value
    test=convertible_to(extract_timestamp),
    message='"{value}" is not a valid timestamp')


# TODO: some caching would be in order in case of higher loads, as these get
# called on every request

def user_exists(pk):
    return User.objects.filter(pk=pk).exists()


def user_is_active(pk):
    return User.objects.filter(pk=pk, is_active=True).exists()


def valid_user_id(val, field):
    """
    Validates that `val` is a valid user_id.

    We check in all users, not only MetrocarUsers, because maybe a service
    technician doesn't have to be a MetrocarUser (?). It's an easy fix
    if wasn't so, anyway.
    """
    return validate(
        partial(valid_int, field=field),

        partial(field_validator,
            test=user_exists,
            message='User with id "{value}" does not exist',
            field=field),

        partial(field_validator,
            test=user_is_active,
            message='User with id "{value}" is not active',
            field=field),
    )(val)
