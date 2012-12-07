from djangosanetesting.cases import DatabaseTestCase

from metrocar.subsidiaries.models import Subsidiary
from metrocar.subsidiaries.context_processors import subsidiary


class TestContextProcessors(DatabaseTestCase):

    def test_subsidiary_processor(self):
        context = subsidiary("dummy request")

        self.assert_equals(Subsidiary.objects.get_current().pk, context['subsidiary'].pk)
        self.assert_equals(len(Subsidiary.objects.all()), len(context['subsidiary_list']))
