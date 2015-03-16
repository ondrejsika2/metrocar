"""
Tools for data validation. Intended to also provide useful debugging information
for invalid data.
"""
from collections import Iterable
from functools import partial
from pipetools import pipe, X, unless, foreach, select_first, flatten


OK = True, None


def validate(*rules):
    """
    Creates a validation function that will check if it's input satisfies
    `rules`.

    `rules` should be an (arbitrarily nested) sequence of functions
    that take one argument and return a tuple of:
    ``(valid: bool, error: string or None)``
    where `valid` says if the argument satisfies the rule and `error` says
    why not if it doesn't.

    The rules are checked sequentially and when an error is encountered, it is
    returned immediately from the function, without checking the rest of the
    rules. The returned value is the one returned from the rule, i.e.
    ``(False, "error message")``

    If no error is encountered the function returns ``(True, None)``.

    (Note that the validation function itself is a rule.)
    """
    rules = rules > flatten | tuple
    return lambda val: rules > foreach(X(val)) | select_first(X != OK) or OK


def validate_each(*rules):
    """
    Like :func:`validate`, but checks each item in `iterable` separately
    against `rules`.

    Also the first encountered error is returned without checking the rest
    of the items.
    """
    return lambda val: (
        (val > foreach(validate(*rules)) | select_first(X != OK) or OK)
        if isinstance(val, Iterable) and not isinstance(val, basestring)
        else (False, '"{0}" is not iterable'.format(val)))


def check(cond, msg=None):
    """
    A helper for creating rules for :func:`validate`.
    """
    return lambda val: OK if (val > pipe | cond) else (False,
        (msg or '{0} test failed'.format(cond)).format(value=val))


def has_key(key, message='missing "{field}" field'):
    return check(lambda d: key in d, message.format(field=key))


def required(key, validate_value=lambda any, field: OK):
    """
    Validation shortcut for validating key/value in a dictionary (or something
    similar).

    `validate_value` has to take a `field` keyword argument (intended for
        displaying in an error message).
    """
    return validate(has_key(key), X[key] | partial(validate_value, field=key))


def optional(key, validate_value=lambda any, field: OK):
    """
    Like :func:`required`, but, well, optional.
    """
    return lambda val: validate_value(val[key], field=key) if key in val else OK


def field_validator(val, test, message, field):
    """
    Shortcut for defining the `validate_value` function for :func:`required`
    """
    return OK if test(val) else (False, message.format(field=field, value=val))


def convertible_to(typ):
    return unless((TypeError, ValueError), typ) | (X != None)


def valid_type(typ, name):
    return partial(field_validator,
        test=convertible_to(typ),
        message='"{field}" should be %s, not "{value}"' % name)


valid_int = valid_type(int, 'an integer')
valid_float = valid_type(float, 'a floating point number')
valid_string = valid_type(unicode, 'a string')
