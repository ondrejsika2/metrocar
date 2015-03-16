from django.conf.urls.defaults import url, patterns
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='tests/test-js.html')),
)
