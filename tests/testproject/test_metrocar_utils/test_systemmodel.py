from nose.tools import raises
from djangosanetesting.cases import DatabaseTestCase

from testproject.test_metrocar_utils.models import DummyModel


class TestSystemModel(DatabaseTestCase):

    def setUp(self):
        self.m = DummyModel(testfield=1)
        self.m.save()

    @raises(AssertionError)
    def test_0_not_deletable(self):
        self.m.deleteable = False
        self.m.save()
        self.m.delete()

    @raises(DummyModel.DoesNotExist)
    def test_1_deletable(self):
        pk = self.m.pk
        assert pk is not None
        self.m.delete()
        DummyModel.objects.get(pk=pk)
