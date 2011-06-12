'''
Created on 10.3.2010

@author: xaralis
'''

from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import require_extended, validate, rc

from metrocar.user_management.models import *
from metrocar.user_management.forms import MetrocarUserCreationForm, \
    MetrocarUserChangeForm
from metrocar.reservations.models import Reservation

class CompanyHandler(BaseHandler):
    """Allows to perform listing of companies using the Metrocar."""
    
    allowed_methods = ('GET',)
    model = Company
    fields = ('name', 'email', 'ic', 'city', 'street', 'house_number', 
        'land_registry_number')
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_user_management_company_handler', ['id'])

class AnonymousUserHandler(AnonymousBaseHandler):
    """
    Handler for anonymous requests concerning users.
    
    Supports user registration.
    """
    
    model = MetrocarUser
    allowed_methods = ('GET', 'POST',)
    fields = ('id', 'username', 'resource_uri')
    exclude = ()
    
    @validate(MetrocarUserCreationForm)
    def create(self, request):
        """
        API way to expose registration of users. Expected parameters in POST request:
            - username
            - password
            - email
            - first_name
            - primary_phone
            - secondary_phone (optional)
            - date_of_birth (format YYYY-MM-DD)
            - drivers_licence_number
            - identity_card_number
        
        If some params are incorrect, method will fail.
        """
        form = MetrocarUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'primary_phone': form.cleaned_data['primary_phone'],
                'secondary_phone': form.cleaned_data['secondary_phone'],
                'date_of_birth': form.cleaned_data['date_of_birth'],
                'drivers_licence_number': form.cleaned_data['drivers_licence_number'],
                'identity_card_number': form.cleaned_data['identity_card_number']
            }
            user = MetrocarUser.objects.create_user(username, email, password,
                **data)
            return rc.CREATED
        return rc.FORBIDDEN
    
    @classmethod
    def resource_uri(cls, *args, **kwargs):
        return ('api_user_management_user_handler', ['username'])

class UserHandler(BaseHandler):
    """
    Handler for authenticated consumers.
    
    Besides anonymous functions, it allows also to list and preview some more 
    descriptive information about Metrocar users.
    """
    
    anonymous = AnonymousUserHandler
    allowed_methods = ('GET', 'PUT', 'POST')
    fields = (
        'id',
        'username',
        ('user', ('first_name', 'last_name'))
    )
    exclude = ()
    
    def read(self, request, username=None):
        """
        If username is supplied, will return information about only this user.
        Otherwise it will list all users available on current subsidiary.
        If authenticated is the same as requested user, more information 
        will be available to the client.
        """
        if username:
            try:
                user = MetrocarUser.objects.get(username=username)
            except:
                return rc.NOT_FOUND
            if request.user.is_authenticated():
                if user.pk == request.user.pk:
                    self.fields = (
                        'username',
                        ('user', ('first_name', 'last_name', 'email', 'is_active')),
                        ('account', ('balance', 'resource_uri')),
                        ('user_card', ('code', 'registration_number', 'is_service_card')),
                        'date_of_birth',
                        'gender',
                        'identity_card_number',
                        'company'
                    )
                    return user
            return user
        else:
            return MetrocarUser.objects.all()
    
    @validate(MetrocarUserChangeForm)
    def update(self, request, username):
        """
        Needs username param.
        Updates information about user. Only allowed when authenticated user
        is same as requesting user.
        """
        try:
            user = MetrocarUser.objects.get(username=username)
        except:
            return rc.NOT_FOUND
        form = MetrocarUserChangeForm(request.POST)
        if request.user.is_authenticated():
            if user.pk == request.user.pk and form.is_valid():
                user.email = form.cleaned_data.get('email')
                user.primary_phone = form.cleaned_data.get('primary_phone')
                user.secondary_phone = form.cleaned_data.get('secondary_phone')
                user.save()
                return rc.ALL_OK
        return rc.FORBIDDEN
    
class AccountHandler(BaseHandler):
    """Handler to provide information about users's account."""
    allowed_methods = ('GET',)
    model = Account
    fields = ('balance', ('activities', ('datetime', 'money_amount', ('content_type', ('name',)))))
    
    def read(self, request, username):
        """
        Returns summary of user's account balance and account acitvities.
        """
        try:
            user = MetrocarUser.objects.get(username=username)
        except:
            return rc.NOT_FOUND
        if request.user.is_authenticated():
            if user.pk == request.user.pk:
                return user.account
        return rc.FORBIDDEN
    
class ReservationHandler(BaseHandler):
    """Provides information about user's reservations."""
    allowed_methods = ('GET',)
    model = Reservation
    fields = (
        'reserved_from',
        'reserved_until',
        ('car', (('model', ('full_name',)), 'resource_uri',))
    )
    
    def read(self, request, username):
        """
        Returns information about user's currently pending reservations.
        """
        try:
            user = MetrocarUser.objects.get(username=username)
        except:
            return rc.NOT_FOUND
        if request.user.is_authenticated():
            if user.pk == request.user.pk:
                return user.reservations.pending()
        return rc.FORBIDDEN
    
        