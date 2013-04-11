from datetime import datetime, date
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.db.transaction import commit_on_success
from django.utils.translation import ugettext_lazy as _
import managers
from metrocar.subsidiaries.models import Subsidiary
from metrocar.utils.fields import *
import re

class Company(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False,
                            verbose_name=_('Name'))
    email = models.EmailField(null=True, verbose_name=_('E-mail'))
    ic = IcField(blank=False, null=True, verbose_name=_('IC'))
    dic = DicField(blank=False, null=True, verbose_name=_('DIC'))
    city = models.CharField(max_length=80, blank=False, null=False,
                            verbose_name=_('City'))
    street = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Street'))
    house_number = models.CharField(max_length=6, blank=False, null=True, verbose_name=_('House number'))
    land_registry_number = models.CharField(max_length=6, blank=False, null=True, verbose_name=_('Land registry number'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __unicode__(self):
        return self.name

class MetrocarUser(User):
    GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')),)

    user = models.OneToOneField(User, parent_link=True)
    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name=_('Date of birth'))
    drivers_licence_number = models.CharField(max_length=10, blank=False,
                                              null=False, verbose_name=_('Drivers licence number'))
    gender = models.CharField(max_length=1, blank=False, null=False,
                              choices=GENDER_CHOICES, verbose_name=_('Gender'))
    identity_card_number = IdentityCardNumberField(blank=False, null=False,
                                                   verbose_name=_('Identity card number'))
    primary_phone = PhoneField(blank=True, null=True,
                               verbose_name=_('Primary phone number'))
    secondary_phone = PhoneField(blank=True, null=True,
                                 verbose_name=_('Secondary phone number'))
    variable_symbol = models.IntegerField(max_length=12, blank=False,
        null=True, editable=False, verbose_name=_('Variable symbol'))
    invoice_date = models.DateField(blank=False, null=False,
        verbose_name=_('Invoice date'))
    company = models.ForeignKey(Company, null=True, blank=True,
                                verbose_name=_('Company'))
    home_subsidiary = models.ForeignKey(Subsidiary,
                                        verbose_name=_('Home subsidiary'))

    language = models.CharField(max_length=2, choices=settings.LANG_CHOICES)

    objects = managers.MetrocarUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return self.full_name()

    @models.permalink
    def get_absolute_url(self):
        return ('mfe_users_detail', (), {'id': self.pk})

    def get_language(self):
        return dict(list(settings.LANG_CHOICES))[self.language]

    def full_name(self):
        """
        Returns full name for the user.
        """
        return ('%s %s') % (self.first_name, self.last_name)

    def update_from_dict(self, dict):
        """
        Updates user with vals from dict dictionary
        """
        for name, value in dict.items():
            if hasattr(self, name):
                setattr(self, name, value)

        self.save()

    def get_invoice_address(self):
        """
        Return concrete invoice address for the user.
        """
        from metrocar.invoices.models import CompanyInvoiceAddress, \
            UserInvoiceAddress
        if self.company is not None:
            try:                
                return CompanyInvoiceAddress.objects.get(company=self.company)
            except CompanyInvoiceAddress.DoesNotExist:
                return None        
        else:
            try:
                return UserInvoiceAddress.objects.get(user=self)
            except UserInvoiceAddress.DoesNotExist:
                return None    

    def get_uninvoiced_account_activities(self):
        """
        Returns queryset of all account activities for user, which has not been
        invoiced yet.
        """
        return AccountActivity.objects.filter(invoice_item__isnull=True,
                                              account__user=self)

    def get_invoiceable_activities(self):
        """
        Returns list of account acivities which are currently ready to be
        invoiced.
        """
        ac_list = []
        for a in self.get_uninvoiced_account_activities():
            a = a.as_concrete_class()
            if a.ready_to_be_invoiced(): ac_list.append(a)
        return ac_list

    def get_unique_password_reset_hash_string(self):
        """
        Returns unique hash string composed of password and username for password reset confirmation
        """
        import datetime
        import hashlib

        now = datetime.datetime.now()
        hash = hashlib.sha1(str(now.year) + str(now.month) + str(now.day) + self.username + self.password).hexdigest()

        return hash

    def parse_vs_from_id_card_number(self):
        """
        Parses variable_symbol from identity_card_number. Extracts only digits and casts the number to int
        """
        vs = re.sub("\D", "", self.identity_card_number)
        try:
            vs = int(vs)
        except ValueError:      #should not happen, id_card_num consists only of digits and characters
            vs = 1
        return vs

    def request_password_reset(self):
        """
        Send user email with info about password reseting
        """
        params = {'password_reset_url': self.home_subsidiary.get_absolute_url() + "/" + slugify(_('users')) + "/" + slugify(_('password reset')) + "/" + self.username + "/" + self.get_unique_password_reset_hash_string()}

        from metrocar.utils.emails import EmailSender
        EmailSender.send_mail([self.email], 'REQ_RES', self.language, self.user, params)

    def save(self, **kwargs):
        """
        Overload to set home subsidiary if missing
        """
        self.invoice_date = date.today()
        self.variable_symbol = self.parse_vs_from_id_card_number()
        if not self.pk:
            try:
                self.home_subsidiary
            except Subsidiary.DoesNotExist:
                self.home_subsidiary = Subsidiary.objects.get_current()
        super(MetrocarUser, self).save(**kwargs)


    def delete(self):
        """
        Overload of delete for soft delete.
        """
        self.is_active = False
        self.save()

class UserRegistrationRequest(models.Model):
    user = models.OneToOneField(MetrocarUser, unique=True, blank=False, null=False, verbose_name=_('User'), related_name='user_registration_request')
    approved = models.BooleanField(blank=False, null=False, default=False, verbose_name=_('Approved'))
    resolved = models.BooleanField(blank=False, null=False, default=False, verbose_name=_('Resolved'))
    objects = managers.UserRegistrationRequestManager()

    class Meta:
        verbose_name = _('User registration request')
        verbose_name_plural = _('User registration requests')

    def __unicode__(self):
        return '%s' % self.user.__unicode__()

    @commit_on_success
    def approve(self):
        """
        Approves user registration, sets the user account active.
        """
        from metrocar.utils.emails import EmailSender
        EmailSender.send_mail([self.user.email], 'REG_APP', self.user.language, self.user)

        self.user.is_active = True
        self.resolved = True
        self.approved = True
        self.user.save()
        self.save()

    @commit_on_success
    def reject(self):
        """
        Rejects registration request.
        """
        from metrocar.utils.emails import EmailSender
        EmailSender.send_mail([self.user.email], 'REG_DNY', self.user.language, self)

        self.resolved = True
        self.approved = False
        self.user.is_active = False
        self.user.save()
        self.save()




class UserCard(models.Model):
    active = models.BooleanField(blank=False, null=False, default=False,
                                 verbose_name=_('Active'))
    code = models.IntegerField(max_length=8, blank=False, null=False,
                               verbose_name=_('User card'))
    last_modified = models.DateTimeField(default=datetime.now(), editable=False,
                                         verbose_name=_('Last modified'))
    registration_number = models.IntegerField(max_length=10, blank=False,
                                              null=False, verbose_name=_('Registration number'))
    is_service_card = models.BooleanField(blank=False, null=False,
                                          default=False, verbose_name=_('Service card'))
    user = models.OneToOneField(MetrocarUser, editable=False,
                                related_name='user_card', verbose_name=_('User'))

    class Meta:
        verbose_name = _('User card')
        verbose_name_plural = _('User cards')

    def __unicode__(self):
        return self.user.__unicode__()

    def save(self, * args, ** kwargs):
        """
        Overload of save for generation of code and registration number.
        """
        if not self.pk:
            self.code = self.create_code()
            self.registration_number = self.create_registration_number()
        super(UserCard, self).save(*args, ** kwargs)

    @classmethod
    def create_registration_number(cls):
        try:
            return UserCard.objects.all().order_by('-pk')[0].pk
        except IndexError:
            return 0

    @classmethod
    def create_code(cls):
        try:
            return UserCard.objects.all().order_by('-pk')[0].pk
        except IndexError:
            return 0


    @classmethod
    def create_for_user(cls, sender, ** kwargs):
        """
        Creates card for the user.
        """
        if kwargs['created']:
            card = UserCard()
            card.user = kwargs['instance']
            card.save()

post_save.connect(UserCard.create_for_user, sender=MetrocarUser)

class Account(models.Model):
    balance = models.DecimalField(decimal_places=3, max_digits=15,
                                  blank=False, null=False, default=0, verbose_name=_('Balance'))
    user = models.OneToOneField(MetrocarUser, editable=False,
                                related_name='account', verbose_name=_('User'))

    class Meta:
        verbose_name = _('User account')
        verbose_name_plural = _('User accounts')

    def __unicode__(self):
        return self.user.__unicode__()

    @classmethod
    def create_for_user(cls, sender, ** kwargs):
        """
        Handles creating of accounts for new users transparently.
        """
        if kwargs['created']:
            account = Account()
            account.user = kwargs['instance']
            account.save()

post_save.connect(Account.create_for_user, sender=MetrocarUser)

class AccountActivity(models.Model):
    account = models.ForeignKey(Account, verbose_name=_('Account'),
                                related_name='activities')
    datetime = models.DateTimeField(blank=False, null=False,
                                    default=datetime.now(), verbose_name=_('Datetime'))
    comment = models.TextField(blank=True, null=False, default='',
                               verbose_name=_('Comment'))
    money_amount = models.DecimalField(decimal_places=2, max_digits=8,
                                       blank=False, null=False, verbose_name=_('Money amount'))
    account_balance = models.DecimalField(decimal_places=2, max_digits=8,
                                          default=Decimal('0'), blank=False, null=False,
                                          editable=False, verbose_name=_('Account balance'))
    content_type = models.ForeignKey(ContentType, editable=False, null=True,
                                     verbose_name=_('Content type'))
    credited = models.BooleanField(editable=False, null=False, default=False,
                                   verbose_name=_('Credited'))

    """
    Not completely clean solution, as one can instantiate the class without
    being concrete, but it's the only acceptable solution available.
    """

    def __unicode__(self):
        return "%+8.2f" % self.money_amount

    @commit_on_success
    def save(self, **kwargs):
        """
        Overload save to correctly set the ContentType
        """
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        # new activity
        if not self.credited and self.ready_to_be_invoiced():
            # perform change of account balance and freeze it's current state
            # to account_balance field
            self.account.balance += self.money_amount
            self.account_balance = self.account.balance
            self.credited = True
            self.account.save()

        super(AccountActivity, self).save(**kwargs)

    def as_concrete_class(self):
        """
        Makes the abstract base class concrete
        """
        content_type = self.content_type
        model = content_type.model_class()
        if model == AccountActivity:
            return self
        return model.objects.get(id=self.id)

    def is_positive(self):
        """
        Returns true if money_amount is positive.
        """
        return self.money_amount > 0

    def ready_to_be_invoiced(self):
        """
        Base method for recognizing if activity is ready to be invoiced.
        """
        return True

class Deposit(AccountActivity):
    class Meta:
        verbose_name = _('Deposit')
        verbose_name_plural = _('Deposits')

    def __unicode__(self):
        return "%s %s" % (unicode(_('Deposit')), self.money_amount)
