'''
Created on 14.3.2010

@author: xaralis
'''

from metrocar.subsidiaries.models import Subsidiary

def subsidiary(request):
    " Adds current subsidiary and subsidiary list to the context "
    # TODO caching
    return {
        'subsidiary': Subsidiary.objects.get_current(),
        'subsidiary_list': Subsidiary.objects.all()
    }