'''
Created on 28.3.2010

@author: xaralis
'''

from StringIO import StringIO
import simplejson
from lxml import etree, objectify
from xml.dom.minidom import Document
from datetime import datetime

from django.http import HttpResponse
from django.conf import settings
from django.utils.encoding import smart_str

class RequestAdapter():
    """
    Request adapter base class. Abstract.
    """
    def preprocess_request(self, request_str):
        """
        Takes request string, validates it and converts data into inner python
        representation.
        """
        raise NotImplementedError()
    
    def postprocess_response(self, response_data):
        """
        Converts inner response structure into suitable form for current 
        communication protocol.
        """
        raise NotImplementedError()

class RequestAdapterXml(RequestAdapter):
    """
    Adapter class to handle custom XML communication format with compressed 
    data flow.
    """
    def preprocess_request(self, request_str):
        """
        Takes request string, validates it and converts data into inner python
        representation.
        """
        # first validate against stored DTD
        f = open(settings.COMM_DTD_REQUEST)
        dtd = etree.DTD(f)
        root = objectify.fromstring(request_str)
        
        if not dtd.validate(root):
            raise ValueError('Incorrect request: could not parse the document, '
                'document is not valid')
        
        # now convert from xml to dictionary used for processing
        output = {'auth' : {}, 'usages' : [], 'requirements' : []}
        for element in root.iterchildren():
            if element.tag == 'a':
                output['auth']['authorization_key'] = element.text
            if element.tag == 'm':
                output['auth']['imei'] = element.text
            elif element.tag == 'v':
                output['usages'].append(self._parse_usages(element))
            elif element.tag == 'z':
                output['requirements'] = self._parse_requirements(element)
        return output
    
    def _parse_usages(self, usage):
        output = {'user_id': usage.i.text, 'incremental_positions' : []}
        
        try:
            output['since'] = datetime.strptime(usage.s.text, 
                    settings.COMM_TIME_FORMAT)
        except:
            pass
        try:
            output['till'] = datetime.strptime(usage.t.text,
                settings.COMM_TIME_FORMAT)
        except:
            pass
        output['base_position'] = {
            'latitude' : float(usage.p.b.text),
            'longitude' : float(usage.p.c.text)
        }
        for inc_pos in usage.q:
            output['incremental_positions'].append({
                'latitude' : float(inc_pos.d.text),
                'longitude' : float(inc_pos.e.text)
            })
        
        output['length'] = usage.l.text
        return output
    
    def _parse_requirements(self, requirements_root):
        output = []
        for element in requirements_root.iterchildren():
            output.append(str(element))
        return output
    
    def postprocess_response(self, response_data):
        """
        Converts inner response structure into suitable form for current 
        communication protocol.
        """
        root = Document()
        response_el = root.createElement('r')
        root.appendChild(response_el)
        
        def append_dict(dict, append_to, tag):
            for val in dict:
                el = root.createElement(tag)
                el_text = root.createTextNode(str(val))
                el.appendChild(el_text)
                append_to.appendChild(el)
            
        if response_data['requirements'].has_key('reservations'):
            # reservations
            reservations_el = root.createElement('u')
            response_el.appendChild(reservations_el)
            for allowed_user in response_data['requirements']['reservations']:
                # create user element under reservations el
                user_el = root.createElement('v')
                reservations_el.appendChild(user_el)
                # put user_id
                user_id_el = root.createElement('i')
                user_id_text_el = root.createTextNode(str(allowed_user['user_id']))
                user_id_el.appendChild(user_id_text_el)
                user_el.appendChild(user_id_el)
                # put phone numbers
                if allowed_user.has_key('phone_numbers'):
                    append_dict(allowed_user['phone_numbers'], user_el, 'p')
                # put rfid codes
                if allowed_user.has_key('rfid_codes'):
                    append_dict(allowed_user['rfid_codes'], user_el, 'q')
                # put allowed time intervals
                for since, till in allowed_user['allowed_times']:
                    # create interval element under user el
                    interval_el = root.createElement('b')
                    user_el.appendChild(interval_el)
                    
                    # put since
                    since_el = root.createElement('s')
                    since_text_el = root.createTextNode(since.strftime(
                        settings.COMM_TIME_FORMAT))
                    since_el.appendChild(since_text_el)
                    interval_el.appendChild(since_el)
                    # put till
                    till_el = root.createElement('t')
                    till_text_el = root.createTextNode(till.strftime(
                        settings.COMM_TIME_FORMAT))
                    till_el.appendChild(till_text_el)
                    interval_el.appendChild(till_el)
            
        # settings
        if response_data['requirements'].has_key('settings'):
            # begin settings
            settings_el = root.createElement('g')
            response_el.appendChild(settings_el)
            
            for key, val in response_data['requirements']['settings'].items():
                # create new setting under settings
                setting_el = root.createElement('j')
                settings_el.appendChild(setting_el)
                
                # key and val elements
                key_el = root.createElement('k')
                key_text_el = root.createTextNode(str(key))
                key_el.appendChild(key_text_el)
                val_el = root.createElement('h')
                val_text_el = root.createTextNode(str(val))
                val_el.appendChild(val_text_el)
                
                setting_el.appendChild(key_el)
                setting_el.appendChild(val_el)
        
        return HttpResponse(root.toxml(
            encoding=settings.COMM_OUTPUT_ENCODING), 
            content_type='application/xml')
        
class RequestAdapterGpx(RequestAdapterXml):
    """
    Adapter class to handle extended GPX communication format.
    """
    def_namesp = { 'd': 'http://www.topografix.com/GPX/1/1' }
    
    def preprocess_request(self, request_str):
        """
        Takes request string, validates it and converts data into inner python
        representation.
        """
        # first validate against stored XSD schema
        xmlschema_doc = etree.parse(settings.COMM_GPX_SCHEMA)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        doc = etree.parse(StringIO(smart_str(request_str)))

        if not xmlschema.validate(doc):
            raise ValueError('Incorrect request: could not parse the document, '
                'document is not valid')
        
        root = doc.getroot()
        
        # now convert from xml to dictionary used for processing
        output = {'auth' : {}, 'usages' : [], 'requirements' : []}
        
        output['auth']['imei'] = str(root.xpath(
            'd:extensions/d:auth/d:imei/text()', namespaces=self.def_namesp)[0])
        output['auth']['authorization_key'] = str(root.xpath(
            'd:extensions/d:auth/d:key/text()', namespaces=self.def_namesp)[0])
        output['usages'] = self._parse_usages(root)
        output['requirements'] = root.xpath(
            'd:extensions/d:requirements/*/text()', namespaces=self.def_namesp)
        return output
    
    def _parse_usages(self, root):
        from dateutil import parser
        output = []
        
        def _sub_base(i):
            """Small wrap fnc to alter point list items"""
            i['latitude'] -= base_lat
            i['longitude'] -= base_lon
            del i['time']
            return i
        
        for trkseg in root.xpath('d:trk/d:trkseg', namespaces=self.def_namesp):
            points = trkseg.xpath('d:trkpt', namespaces=self.def_namesp)
            point_list = [ { 
                'latitude': float(p.get('lat')), 
                'longitude': float(p.get('lon')), 
                'time': p.xpath('d:time/text()', namespaces=self.def_namesp)[0]
                } for p in points ]
            
            point_list = sorted(point_list, key=lambda k: k['time']) # sort by time
            base_lat = min(point_list, key=lambda k: k['latitude'])['latitude']
            base_lon = min(point_list, key=lambda k: k['longitude'])['longitude']
            point_list = map(_sub_base, point_list) # make incrementals
            
            rec = {
                'base_position': {'latitude': base_lat, 'longitude': base_lon},
                'incremental_positions': point_list,
                'user_id': trkseg.xpath('d:extensions/d:uid/text()',
                    namespaces=self.def_namesp)[0],
                'length': trkseg.xpath('d:extensions/d:length/text()',
                    namespaces=self.def_namesp)[0],
            }
            since = trkseg.xpath('d:extensions/d:since/text()', 
                namespaces=self.def_namesp)[0]
            till = trkseg.xpath('d:extensions/d:till/text()', 
                namespaces=self.def_namesp)[0]
            if since: rec['since'] = parser.parse(since, ignoretz=True)
            if till: rec['till'] = parser.parse(till, ignoretz=True)
            
            output.append(rec)
        return output
        
class RequestAdapterJSON(RequestAdapter):
    """
    Adapter class to handle our GeoJSON-enabled communication format.
    """
    def preprocess_request(self, request_str):
        """
        Takes request string, validates it and converts data into inner python
        representation.
        """
        resp = {
            'auth' : {},
            'usages': [],
            'requirements': []
        }
        resp.update(simplejson.loads(request_str, 
            encoding=settings.COMM_INPUT_ENCODING))
        """
        We need to update datetime strings to datetime instances, because the
        output should have all conversions already done
        
        Same thingy for floats
        """
        for usage in resp['usages']:
            try:
                usage['since'] = datetime.strptime(usage['since'], 
                    settings.COMM_TIME_FORMAT)
            except:
                pass
            try:
                usage['till'] = datetime.strptime(usage['till'],
                    settings.COMM_TIME_FORMAT)
            except:
                pass
            
            usage['base_position']['latitude'] = float(usage['base_position']['latitude'])
            usage['base_position']['longitude'] = float(usage['base_position']['longitude'])
            for p in usage['incremental_positions']:
                p['latitude'] = float(p['latitude'])
                p['longitude'] = float(p['longitude']) 
        return resp
    
    def postprocess_response(self, response_data):
        """
        Converts inner response structure into suitable form for current 
        communication protocol.
        """
        from django.core.serializers.json import DateTimeAwareJSONEncoder
        resp_str = simplejson.dumps(response_data, cls=DateTimeAwareJSONEncoder,
            encoding=settings.COMM_OUTPUT_ENCODING)        
        return HttpResponse(resp_str, content_type='application/json')
    
class InvalidFormatException(Exception):
    pass
    
def get_adapter(format):
    """
    Factory function to get correct format adapter.
    
    Formats supported:
        - xml : custom XML compressed format
        - gpx : customized GPX format
        - json : GeoJSON enabled format
        
    Raises InvalidFormatException if incorrect format str is supplied.
    """
    FORMATS = {
        'xml': RequestAdapterXml,
        'json': RequestAdapterJSON,
        'gpx' : RequestAdapterGpx
    }
    if format not in FORMATS.keys():
        raise InvalidFormatException(u'Invalid format requested: `%s`, '
            'choices are: %s' % (format, ", ".join(FORMATS.keys())))
    return FORMATS.get(format)()
    