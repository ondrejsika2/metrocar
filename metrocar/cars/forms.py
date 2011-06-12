'''
Created on 2.4.2010

@author: xaralis
'''

from django.contrib.auth.forms import SetPasswordForm

class SetCarAuthKeyForm(SetPasswordForm):
    """
    A form that lets a user change car unit authorization key without
    entering the old one
    """
    def __init__(self, car, *args, **kwargs):
        self.car = car
        super(SetCarAuthKeyForm, self).__init__(car, *args, **kwargs)
    
    def save(self, commit=True):
        self.car.set_auth_key(self.cleaned_data['new_password1'])
        if commit:
            self.car.save()
        return self.user
