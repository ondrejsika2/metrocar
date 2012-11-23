'''
Created on 23.4.2010

@author: xaralis
'''
from nose.tools import raises

from djangosanetesting.cases import DatabaseTestCase

from test_metrocar.test_metrocar_utils.models import DummyModel

class TestCloneableModelMixin(DatabaseTestCase):
    def setUp(self):
        super(TestCloneableModelMixin, self).setUp()
        self.m = DummyModel(testfield=1)

    @raises(ValueError)
    def test_0_fail_for_unsaved(self):
        c = self.m.clone()

    def test_1_sucess_for_saved(self):
        self.m.save()
        c = self.m.clone()
        self.assert_not_equals(self.m.pk, c.pk)
        self.assert_equals(self.m.testfield, c.testfield)

