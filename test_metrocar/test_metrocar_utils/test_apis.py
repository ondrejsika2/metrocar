from pipetools import X

from django.utils import simplejson as json

from djangosanetesting.cases import UnitTestCase

from metrocar.utils import Bunch
from metrocar.utils.apis import parse_json, InvalidRequest, validate_request, process_request
from metrocar.utils.validation import check


class TestParseJson(UnitTestCase):

    def test_ok(self):
        request = Bunch(body='{"some": "value"}')
        self.assertEqual(parse_json(request), {'some': 'value'})

    def test_empty(self):
        request = Bunch(body='')
        with self.assertRaises(InvalidRequest) as ctx:
            parse_json(request)
        self.assertEqual(str(ctx.exception), 'Missing JSON data.')

    def test_invalid(self):
        request = Bunch(body='{12:34}')
        with self.assertRaises(InvalidRequest) as ctx:
            parse_json(request)
        self.assertEqual(str(ctx.exception),
            'Invalid JSON (Expecting property name: line 1 column 1 (char 1)).')


class TestValidateRequest(UnitTestCase):

    def setUp(self):
        self.rules = [
            check(X > 0)
        ]

    def test_valid(self):
        self.assertEqual(validate_request(self.rules, 3), 3)

    def test_invalid(self):
        with self.assertRaises(InvalidRequest):
            validate_request(self.rules, -1)


class TestProcessRequest(UnitTestCase):

    def test_valid(self):
        dummy_request = object()

        def process(request):
            self.assertEqual(request, dummy_request)
            return 'DATA'

        @process_request(process)
        def get(view, request, data):
            self.assertEqual(request, dummy_request)
            self.assertEqual(data, 'DATA')
            return 'RESULT'

        result = get(None, dummy_request)
        self.assertEqual(result, 'RESULT')

    def test_invalid(self):
        dummy_request = object()

        def process(request):
            raise InvalidRequest('ERROR MSG')

        @process_request(process)
        def get(view, request, data):
            return 'RESULT'

        result = get(None, dummy_request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json.loads(result.content),
            {'status': 'error', 'message': 'ERROR MSG'})
