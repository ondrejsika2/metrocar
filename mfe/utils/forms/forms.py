'''
Created on 14.3.2010

@author: xaralis
'''

from django.contrib.formtools.wizard import FormWizard

class ViewFormWizard(FormWizard):
    def __init__(self, context, initial=None):
        # Override the extra context
        self.extra_context = context

        # Call the original init
        super(ViewFormWizard, self).__init__(self._forms, initial=initial)

    def __call__(self, request):
        return super(ViewFormWizard, self).__call__(request)
    
def render_to_wizard(form, request, context, initial=None):
    c = form(context=context, initial=initial)
    return c(request)
