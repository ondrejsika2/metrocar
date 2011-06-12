'''
Created on 23.4.2010

@author: xaralis
'''

from nose import SkipTest
from nose.tools import raises


from djangosanetesting.cases import DatabaseTestCase

from models import DummyModel

class TestSystemModel(DatabaseTestCase):
    def setUp(self):
        super(TestSystemModel, self).setUp()
        self.m = DummyModel(testfield=1)
        self.m.save()
        
    @raises(AssertionError)
    def test_0_not_deletable(self):
        self.m.deleteable = False
        self.m.save()
        self.m.delete()
        
    def test_1_deletable(self):
        raise SkipTest('Nose compatibility issue')
        self.assert_true(self.m.delete())