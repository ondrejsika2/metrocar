from datetime import timedelta, datetime
from random import random, randint

from pipetools import pipe, foreach_do, as_kwargs

from geotrack.api import store


default_bounds = ((9.18457, 46.49839), (21.44531, 53.19945))


def within(bounds, point):
    x, y = point
    (bx1, by1), (bx2, by2) = bounds
    return (bx1 < x < bx2) and (by1 < y < by2)


def random_point(bounds=default_bounds):
    (x1, y1), (x2, y2) = bounds
    return (
        x1 + random() * (x2 - x1),
        y1 + random() * (y2 - y1),
    )


def random_move(point,
    x_range=(-0.004, 0.004),
    y_range=(-0.004, 0.004),
    bounds=default_bounds):
    assert within(bounds, point)
    x, y = point
    new_point = random_point((
        (x + x_range[0], y + y_range[0]),
        (x + x_range[1], y + y_range[1]),
    ))
    return new_point if within(bounds, new_point) else random_move(
        point, x_range, y_range, bounds)


def generate(
    start_point=None,
    start_time=None,
    time_step=timedelta(seconds=30),
    time_step_variation_seconds=2,
    unit_id=None,
    length=None,
    bounds=default_bounds,
    get_extra_data=lambda (x, y), index: {}):

    point = start_point or random_point()
    timestamp = start_time or datetime.now()
    unit_id = unit_id or randint(1, 1000)
    length = length or randint(100, 1000)

    x_range = 0.004
    y_range = 0.004
    dx = random() * x_range * 2 - x_range
    dy = random() * y_range * 2 - y_range
    dx_range = 0.004
    dy_range = 0.004

    for index in xrange(length):
        yield dict({
            'location': point,
            'unit_id': unit_id,
            'timestamp': timestamp,
        }, **get_extra_data(point, index))

        point = point[0] + dx, point[1] + dy
        if not within(bounds, point):
            point = random_move((point[0] - dx, point[1] - dy), bounds=bounds)
            dx = random() * x_range * 2 - x_range
            dy = random() * y_range * 2 - y_range
        dx += random() * dx_range * 2 - dx_range
        dy += random() * dy_range * 2 - dy_range
        d = time_step_variation_seconds
        timestamp += (time_step + timedelta(seconds=randint(-d, d)))


create_and_store_dummy_route = pipe | generate | foreach_do(as_kwargs(store))
