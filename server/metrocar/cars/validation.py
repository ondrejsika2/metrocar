from functools import partial

from metrocar.utils.validation import field_validator, validate, valid_int
from metrocar.cars.models import Car


def valid_car_id(val, field):
    return validate(
        partial(valid_int, field=field),
        partial(field_validator,
            test=lambda val: Car.objects.filter(id=val).exists(),
            message='{field}: Car with id "{value}" does not exist',
            field=field)
    )(val)
