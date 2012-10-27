from pipetools import X

from djangosanetesting.cases import UnitTestCase

from metrocar.car_unit_api.validation import validate, check, validate_each
from metrocar.car_unit_api.validation import valid_int, optional
from metrocar.car_unit_api.validation import is_valid_location, required, OK


class TestValidation(UnitTestCase):

    def test_validate_valid(self):
        d = 42
        valid, error = validate(
            check(X > 20),
            check(X == 42),
        )(d)
        self.assertTrue(valid)
        self.assertFalse(error)

    def test_validate_invalid(self):
        d = 42
        valid, error = validate(
            check(X > 20),
            check(X < 30, "value should be < 24"),
            check(lambda: 1 / 0, "this won't happen..."),
        )(d)
        self.assertEqual(valid, False)
        self.assertEqual(error, "value should be < 24")

    def test_validate_each(self):
        d = [3, 5, 7, 9, 10, 13]
        d2 = [3, 5, 7, 9, 11, 13]

        f = validate_each(
            check(X > 0),
            check(X % 2, 'odd test failed'),
        )
        self.assertEqual(f(d), (False, 'odd test failed'))
        self.assertEqual(f(d2), (True, None))

    def test_validate_each_non_iterable(self):
        d = 123
        f = validate_each(check(X > 0))
        self.assertEqual(f(d), (False, '"123" is not iterable'))


class TestValidLocation(UnitTestCase):

    def test_valid(self):
        self.assertTrue(is_valid_location([10, -20.123]))

    def test_invalid(self):
        self.assertFalse(is_valid_location(['asdf', 123]))


class TestRequired(UnitTestCase):

    def test_valid(self):
        data = {'some_field': 3}
        self.assertEqual(validate(
            required('some_field', valid_int),
        )(data), OK)

    def test_missing(self):
        data = {}
        self.assertEqual(validate(
            required('some_field', valid_int),
        )(data), (False, 'missing "some_field" field'))

    def test_invalid(self):
        data = {'some_field': []}
        self.assertEqual(validate(
            required('some_field', valid_int),
        )(data), (False, '"some_field" should be an integer, not "[]"'))


class TestOptional(UnitTestCase):

    def test_valid(self):
        data = {'some_field': 3}
        self.assertEqual(validate(
            optional('some_field', valid_int),
        )(data), OK)

    def test_missing(self):
        data = {}
        self.assertEqual(validate(
            optional('some_field', valid_int),
        )(data), OK)

    def test_invalid(self):
        data = {'some_field': []}
        self.assertEqual(validate(
            optional('some_field', valid_int),
        )(data), (False, '"some_field" should be an integer, not "[]"'))
