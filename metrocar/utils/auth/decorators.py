__author__="Xaralis"
__date__ ="$9.11.2009 20:31:41$"

from django.conf import settings
from django.contrib.auth import authenticate
from django_xmlrpc.decorators import AuthenticationFailedException, PermissionDeniedException

def secure_func(perm=None):
    """
    Decorator that checks if permissions are required and eventually denies
    access to unauthorized user.
    """
    def _decorate(func):
        # Check in settings if authentication is ON
        if settings.XMLRPC_AUTHENTICATION_REQUIRED is None or \
           settings.XMLRPC_AUTHENTICATION_REQUIRED == False:
            return func

        # No way to eliminate copy & paste from django_xmlrpc as decorators
        # have to be 3-level deep ...
        def __authenticated_call(username, password, *args):
            user = authenticate(username=username, password=password)
            if not user:
                raise AuthenticationFailedException
            if perm and not user.has_perm(perm):
                raise PermissionDeniedException
            return func(user, *args)

        # Update the function's XML-RPC signature, if the method has one
        if hasattr(func, '_xmlrpc_signature'):
            sig = func._xmlrpc_signature

            # We just stick two string args on the front of sign['args'] to
            # represent username and password
            sig['args'] = (['string'] * 2) + sig['args']
            __authenticated_call._xmlrpc_signature = sig

        # Update the function's docstring
        if func.__doc__:
            __authenticated_call.__doc__ = func.__doc__ + \
                "\nNote: Authentication is required. First two params " \
                "are username and password."
            if perm:
                __authenticated_call.__doc__ += ' this function requires ' \
                                             +  '"%s" permission.' % perm
        return __authenticated_call

    return _decorate