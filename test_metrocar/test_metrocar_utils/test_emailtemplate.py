'''
Created on 23.4.2010

@author: xaralis
'''
import django.test

from metrocar.utils.models import EmailTemplate

class TestEmailTemplate(django.test.TestCase):
    def setUp(self):
        super(TestEmailTemplate, self).setUp()
        self.template = EmailTemplate(code='test', name='testtemplate',
            subject='{{ subject }}', content='{{ subject|lower }}')
        
    def test_0_subject_render(self):
        self.assertEquals(self.template.render_subject(subject='subject'),
            'subject')
        
    def test_1_content_render(self):
        self.assertEquals(self.template.render_content(subject='SUBJECT'),
            'subject')