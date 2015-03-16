import django.test

from metrocar.subsidiaries.models import Subsidiary
from metrocar.subsidiaries.context_processors import subsidiary


class TestContextProcessors(django.test.TestCase):

    def test_subsidiary_processor(self):
        context = subsidiary("dummy request")

        self.assertEquals(Subsidiary.objects.get_current().pk, context['subsidiary'].pk)
        self.assertEquals(len(Subsidiary.objects.all()), len(context['subsidiary_list']))
