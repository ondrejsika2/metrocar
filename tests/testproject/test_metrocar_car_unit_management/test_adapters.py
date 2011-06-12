'''
Created on 21.4.2010

@author: xaralis
'''

from datetime import datetime

from djangosanetesting.cases import UnitTestCase
from django.conf import settings

from metrocar.car_unit_management.adapters import RequestAdapterXml, \
    RequestAdapterJSON, RequestAdapterGpx
    
    
REQUEST_RESULT = {
    'auth': {'authorization_key': '123', 'imei': '123'},
    'usages': [{
        'user_id': '1',
        'since': datetime.strptime('10-01-01 10:00', settings.COMM_TIME_FORMAT),
        'till': datetime.strptime('10-01-01 11:00', settings.COMM_TIME_FORMAT),
        'base_position': {'latitude': 18.0, 'longitude': 19.0},
        'incremental_positions': [
            {'latitude': 1.2, 'longitude': 1.4},
            {'latitude': 1.4, 'longitude': 1.8}
        ],
        'length': '100',
    }],
    'requirements': ['RESERVATIONS', 'SETTINGS']
}

RESPONSE = {
    'requirements': {        
        'settings': {'setting_1': "1"},
        'reservations': [
            {
                'user_id': 1,
                'rfid_codes': ['123123',],
                'phone_numbers': ['777 883 133',],
                'allowed_times': [(
                    datetime.strptime('10-01-01 10:00', settings.COMM_TIME_FORMAT),
                    datetime.strptime('10-01-01 11:00', settings.COMM_TIME_FORMAT)
                )]
            }
        ]
    }
}

REQUEST_RESULT_GPX = {
    'auth': {'authorization_key': '123', 'imei': '123'},
    'usages': [{
        'user_id': '1',
        'since': datetime.strptime('10-01-01 10:00', settings.COMM_TIME_FORMAT),
        'till': datetime.strptime('10-01-01 11:00', settings.COMM_TIME_FORMAT),
        'base_position': {'latitude': 19.2, 'longitude': 20.4},
        'incremental_positions': [
            {'latitude': 0.0, 'longitude': 0},
            {'latitude': 0.2, 'longitude': 0.4}
        ],
        'length': '100',
    }],
    'requirements': ['RESERVATIONS', 'SETTINGS']
} 

class TestRequestAdapterXml(UnitTestCase):
    
    def test_adapter_xml(self):
        request = """
<r>
    <a>123</a>
    <m>123</m>
    <v>
        <i>1</i>
        <s>10-01-01 10:00</s>
        <p>
            <b>18.0</b>
            <c>19.0</c>
        </p>
        <q>
            <d>1.2</d>
            <e>1.4</e>
        </q>
        <q>
            <d>1.4</d>
            <e>1.8</e>
        </q>
        <l>100</l>
        <t>10-01-01 11:00</t>
    </v>
    <z>
        <x>RESERVATIONS</x>
        <x>SETTINGS</x>
    </z>
</r>
        """
        
        response = """Content-Type: application/xml

<?xml version="1.0" encoding="windows-1252"?><r><u><v><i>1</i><p>777 883 133</p><q>123123</q><b><s>10-01-01 10:00</s><t>10-01-01 11:00</t></b></v></u><g><j><k>setting_1</k><h>1</h></j></g></r>"""
        adapter = RequestAdapterXml()
        self.assert_equals(adapter.preprocess_request(request), REQUEST_RESULT)
        self.assert_equals(str(adapter.postprocess_response(RESPONSE)), response)
        
    def test_adapter_json(self):
        request = """
{
    "auth":{"imei":"123", "authorization_key":"123"},
    "usages":[
        {
            "since":"10-01-01 10:00",
            "till":"10-01-01 11:00",
            "user_id":"1",
            "base_position":{"latitude":"18.0","longitude":"19.0"},
            "length":"100",
            "incremental_positions":[
                {"latitude":"1.2","longitude":"1.4"},{"latitude":"1.4","longitude":"1.8"}
            ]
        }
    ],
    "requirements": ["RESERVATIONS", "SETTINGS"]
}
"""

        response = """Content-Type: application/json

{"requirements": {"reservations": [{"rfid_codes": ["123123"], "user_id": 1, "phone_numbers": ["777 883 133"], "allowed_times": [["2010-01-01 10:00:00", "2010-01-01 11:00:00"]]}], "settings": {"setting_1": "1"}}}"""

        adapter = RequestAdapterJSON()
        self.assert_equals(adapter.preprocess_request(request), REQUEST_RESULT)
        self.assert_equals(str(adapter.postprocess_response(RESPONSE)), response)
        
    def test_adapter_gpx(self):
        request = """
<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
    <trk>
        <name>Sample</name>
        <trkseg>
            <trkpt lat="19.2" lon="20.4">
                <ele>2469.264</ele>
                <time>2010-01-01T10:00:00Z</time>
            </trkpt>
            <trkpt lat="19.4" lon="20.8">
                <ele>2473.626</ele>
                <time>2010-01-01T11:00:00Z</time>
            </trkpt>
            <extensions>
                <uid>1</uid>
                <since>2010-01-01T10:00:00Z</since>
                <till>2010-01-01T11:00:00Z</till>
                <length>100</length>
            </extensions>
        </trkseg>
    </trk>
    <extensions>
        <auth>
            <imei>123</imei>
            <key>123</key>
        </auth>
        <requirements>
            <requirement>RESERVATIONS</requirement>
            <requirement>SETTINGS</requirement>
        </requirements>
    </extensions>
</gpx>
"""

        response = """Content-Type: application/xml

<?xml version="1.0" encoding="windows-1252"?><r><u><v><i>1</i><p>777 883 133</p><q>123123</q><b><s>10-01-01 10:00</s><t>10-01-01 11:00</t></b></v></u><g><j><k>setting_1</k><h>1</h></j></g></r>"""

        adapter = RequestAdapterGpx()
        req = adapter.preprocess_request(request)
        self.assert_equals(REQUEST_RESULT_GPX['auth'], req['auth'])
        self.assert_equals(REQUEST_RESULT_GPX['requirements'], req['requirements'])
        self.assert_equals(REQUEST_RESULT_GPX['usages'][0]['user_id'], req['usages'][0]['user_id'])
        self.assert_equals(REQUEST_RESULT_GPX['usages'][0]['since'], req['usages'][0]['since'])
        self.assert_equals(REQUEST_RESULT_GPX['usages'][0]['till'], req['usages'][0]['till'])
        self.assert_almost_equals(
            REQUEST_RESULT_GPX['usages'][0]['base_position']['latitude'],
            req['usages'][0]['base_position']['latitude']
        )
        self.assert_almost_equals(
            REQUEST_RESULT_GPX['usages'][0]['base_position']['longitude'],
            req['usages'][0]['base_position']['longitude']
        )
        self.assert_almost_equals(
            REQUEST_RESULT_GPX['usages'][0]['incremental_positions'][0]['latitude'],
            req['usages'][0]['incremental_positions'][0]['latitude']
        )
        self.assert_almost_equals(
            REQUEST_RESULT_GPX['usages'][0]['incremental_positions'][0]['longitude'],
            req['usages'][0]['incremental_positions'][0]['longitude']
        )
        
        self.assert_equals(str(adapter.postprocess_response(RESPONSE)), response)
        