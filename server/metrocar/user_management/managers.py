'''
Created on 7.5.2010

@author: xaralis
'''
from datetime import datetime

from django.db import models
from django.db.transaction import commit_on_success
from django.contrib.auth.models import UserManager

class MetrocarUserManager(UserManager):
    @commit_on_success
    def create_user(self, username, email, password, **kwargs):
        """
        Creates and saves a User with the given username, e-mail and password.
        """
        from metrocar.user_management.models import UserRegistrationRequest
        from metrocar.subsidiaries.models import Subsidiary
        
        now = datetime.now()
        defaults = {
            'id': None,
            'username': username,
            'email': email.strip().lower(),
            'password': 'placeholder',
            'is_staff': False,
            'is_active': False,
            'is_superuser': False,
            'last_login': now,
            'date_joined': now,
            'specific_symbol': 0,
            'invoice_date': now,
            'home_subsidiary': Subsidiary.objects.get_current(),
		        'language': 'CS',
        }
        defaults.update(**kwargs)
        
        metrocar_user = self.model(**defaults)
        if password:
            metrocar_user.set_password(password)
        else:
            metrocar_user.set_unusable_password()

#metrocar_user.variable_symbol = 1
#metrocar_user.invoice_date = 1999-10-10
        metrocar_user.save()
        
        # create registration request and return
        UserRegistrationRequest.objects.create_for_user(metrocar_user)
        return metrocar_user
    
    def local(self):
        """
        Returns queryset with users from current subsidiary
        """
        from metrocar.subsidiaries.models import Subsidiary
        # POSSIBLY BUG?
        return self.get_query_set().filter(home_subsidiary=Subsidiary.objects.get_current())
    
    def with_inactive(self):
        return super(MetrocarUserManager, self).get_query_set()
    
    def get_query_set(self):
        return super(MetrocarUserManager, self).get_query_set().exclude(
            user_registration_request__resolved=True,
            user_registration_request__approved=False).exclude(is_active=False)

	def get_all_my_paid_invoices(self):
		"""
		Returns all user's paid invoices
		"""
		from metrocar.invoices.models import Invoice
		
		usr = self.model()
		invs = []
		invs = Invoice.objects.filter(user = usr)
		invs = invs.filter(payment_datetime__lte=date.today())
		return invs

	def get_all_my_unpaid_invoices(self):
		"""
		Returns all user's unpaid invoices
		"""
		usr = self.model()
		invs = []
		invs = Invoice.objects.filter(user = usr)
		invs = invs.filter(payment_datetime__isnull=True)
		return invs
            
class UserRegistrationRequestManager(models.Manager):
    def get_query_set(self):
        return super(UserRegistrationRequestManager, self).get_query_set().filter(resolved=False)
    
    def with_resolved(self):
        return super(UserRegistrationRequestManager, self).get_query_set()
    
    def create_for_user(self, user):
        """
        Creates new registration request for user requiring registration.
        """
        #Send email to user - registration request accepted
        from metrocar.utils.emails import EmailSender
        EmailSender.send_mail([user.email], 'REG_REQ',user.language, user )

        r = self.model(user=user)
        r.save()
        return r
    
