__author__="Xaralis"
__date__ ="$28.10.2009 17:29:19$"

from xmlrpclib import ServerProxy

def get_server():
    return ServerProxy('http://127.0.0.1:8000/xmlrpc/', allow_none = 1)