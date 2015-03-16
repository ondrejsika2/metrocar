'''
Created on 12.3.2010

@author: xaralis
'''

from django.contrib.auth.backends import ModelBackend

from models import MetrocarUser

class MetrocarBackend(ModelBackend):
    """
    Inherited authentication backend for frontend use. Basically replaced
    User by MetrocarUser where applicable
    """

    def authenticate(self, username=None, password=None):
        try:
            user = MetrocarUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except MetrocarUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MetrocarUser.objects.get(pk=user_id)
        except MetrocarUser.DoesNotExist:
            return None