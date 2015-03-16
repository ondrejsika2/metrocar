'''
Created on 27.3.2010

@author: xaralis
'''

from piston.authentication import HttpBasicAuthentication

def get_authentication_handler():
    """
    Utility function to decouple settings of authentication from application
    modules. Follows factory pattern.
    """
    return HttpBasicAuthentication(realm='Metrocar API')