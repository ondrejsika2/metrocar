__author__="Xaralis"
__date__ ="$28.10.2009 14:51:40$"

import re

from django.db.models import CharField, IntegerField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class IdentityCardNumberField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9
        super(IdentityCardNumberField, self).__init__(*args, **kwargs)

class PhoneField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(PhoneField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        # FIXME
        return value

        if re.match('^[0-9]{2,3} [0-9]{9}$', value) is None:
            raise ValidationError(_('Enter a valid telephone number with '
                'format XXX XXXXXXXXX.'))

        return value

class IcField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super(IcField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        try:
            if not re.match('^[0-9]{8}', value):
                raise ValidationError(_('Enter valid IC number.'))

        except:
            raise ValidationError(_('Enter valid IC number.'))

        return value

class DicField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super(DicField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        try:
            if not re.match('CZ\d{8,10}', value):
                raise ValidationError(_('Enter valid DIC number.'))
        except:
            raise ValidationError(_('Enter valid DIC number.'))

        return value


# Make custom fields work with south
from south.modelsinspector import add_introspection_rules
fields = (
    'IdentityCardNumberField',
    'PhoneField',
    'IcField',
    'DicField',
)
for field in fields:
    add_introspection_rules([], ["^metrocar\.utils\.fields\.%s" % field])
