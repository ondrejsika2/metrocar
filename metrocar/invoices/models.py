'''
Created on 1.5.2010

@author: xaralis
'''
from datetime import date
from datetime import datetime
from datetime import timedelta

from decimal import Decimal

from django.utils import importlib
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
import managers
from django.conf import settings
from metrocar.invoices.printing import PrintableInvoice
from metrocar.invoices.printing import PrintableInvoicePdf
from metrocar.user_management.models import Account
from metrocar.user_management.models import AccountActivity
from metrocar.user_management.models import Company
from metrocar.user_management.models import MetrocarUser
from metrocar.utils.fields import *
from metrocar.utils.models import SystemModel
from metrocar.utils.log import get_logger


class InvoiceAddress(models.Model):
    street = models.CharField(max_length=100, blank=False, null=False,
                              verbose_name=_('Street'))
    land_registry_number = models.IntegerField(max_length=8, blank=False,
                                               null=False, verbose_name=_('Land registry number'))
    house_number = models.IntegerField(max_length=8, blank=True, null=True,
                                       verbose_name=_('House number'))
    zip_code = models.IntegerField(max_length=5, blank=False, null=False,
                                   verbose_name=_('Zip code'))
    city = models.CharField(max_length=80, blank=False, null=False,
                            verbose_name=_('City'))
    state = models.CharField(max_length=100, blank=False, null=False,
                             default=_('Czech Republic'), verbose_name=_('State'))
    deleted = models.BooleanField(blank=False, null=False, default=False,
                                  verbose_name=_('Deleted'))

    class Meta:
        abstract = True
        verbose_name = _('Invoice address')
        verbose_name_plural = _('Invoice addresses')

    def __unicode__(self):
        return '%s %s, %s %s, %s' % (self.street, self.land_registry_number, 
                                     self.zip_code, self.city, self.state)
    
class CompanyInvoiceAddress(InvoiceAddress):
    company = models.OneToOneField(Company, verbose_name=_('Company'),
                                   related_name='invoice_address')
    ic = IcField(blank=False, null=True, verbose_name=_('IC'))
    dic = DicField(blank=False, null=True, verbose_name=_('DIC'))
    
    class Meta:
        verbose_name = _('Company invoice address')
        verbose_name_plural = _('Company invoice addresses')

class UserInvoiceAddress(InvoiceAddress):
    user = models.OneToOneField(MetrocarUser, verbose_name=_('User'),
                                related_name='invoice_address')
    
    class Meta:
        verbose_name = _('User invoice address')
        verbose_name_plural = _('User invoice addresses')
    
class PaymentMethod(SystemModel):
    name = models.CharField(max_length=150, null=False, blank=False,
                            verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('Description'))
    code = models.CharField(max_length=10, null=False, blank=False,
                            verbose_name=_('Code'))
    
    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')
        
    def __unicode__(self):
        return self.name

class Invoice(models.Model):
    INVOICE_STATES = (('ACTIVE', _('Active')), ('OVERDUE', _('Overdue')), ('PAID', _('Paid')),)
    
    draw_date = models.DateField(blank=False, null=False,
                                 verbose_name=_('Draw date'))
    due_date = models.DateField(blank=False, null=False,
                                verbose_name=_('Due date'))
    variable_symbol = models.IntegerField(max_length=12, blank=False,
                                          null=False, editable=False, verbose_name=_('Variable symbol'))
    specific_symbol = models.IntegerField(max_length=12, blank=False,
                                          null=False, editable=False, verbose_name=_('Specific symbol'))
    payment_datetime = models.DateTimeField(blank=True, null=True,
                                            verbose_name=_('Date and time of payment'))
    status = models.CharField(max_length=7, blank=False, null=False,
                              choices=INVOICE_STATES, verbose_name=_('Invoice status'))
    user = models.ForeignKey(MetrocarUser, verbose_name=_('User'))
    pdf_invoice = models.FileField(upload_to='invoices/%Y-%m')			#the path is returned by pdf generator

    #TODO copy address information on save
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

    def __unicode__(self):
        return str(self.variable_symbol)
    
    def get_printable_invoice(self, format=PrintableInvoice.FORMAT_PDF):
        """
        Return PrintableInvoice object for current reservation.
        Factory pattern.
        """
        return PrintableInvoice.create_printable_invoice(self, format)
        
    def get_items(self):
        return InvoiceItem.objects.filter(invoice=self)
    
    def total_price(self):
        """
        Returns total price of invoice, which is a sum for all invoice items 
        gathered
        """
        if self.items is None:
            return 0
        total_price = 0
        for item in self.get_items():
            total_price += item.amount
        return total_price
        
    def total_price_with_tax(self):
        """
        Returns total price of invoice with tax computed from user's
        home subsidiary's tax rate
        """
        if self.items is None:
            return 0
        total_price = 0
        for item in self.get_items():
            total_price += item.amount_with_tax()
        return total_price.quantize(Decimal('0.01'))
    
    def send_by_email(self):
        """
        Sends email documenting invoice having the PDF attached
        """
        from metrocar.utils.models import EmailTemplate
        from django.core.mail import EmailMessage
        from metrocar.utils.serializers import to_dict
        from metrocar.utils.log import get_logger
        self.pdf_invoice.open(mode='rb')
        if self.status == 'PAID':
            et = EmailTemplate.objects.get(code='INV_' + self.user.language)
        else:
            et = EmailTemplate.objects.get(code='INV_A_' + self.user.language)    
        params = to_dict(self)
        params = params[0]
        subject = et.render_subject(** params)
        message = et.render_content(** params)
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [self.user.email])
        email.attach('Invoice.pdf', self.pdf_invoice.read(), PrintableInvoicePdf.get_mime())
        try:
            email.send(fail_silently=False)
            get_logger().info("Mail INV_" + self.user.language + " sent to " + str([self.user.email]))
        except Exception as ex:
            get_logger().error("Mail INV_" + self.user.language + " could not be sent. Exception was: " + str(ex))
        self.pdf_invoice.close()
    
    def save(self, * args, ** kwargs):
        """
        Overload django Model save method to add custom functionality.
        Generates VS and draw_date and due_date columns
        """
        if not self.pk:
            from django.conf import settings
            # generate vs, draw date and due date
            self.variable_symbol = Invoice.generate_variable_symbol()
            self.specific_symbol = self.user.specific_symbol
            self.draw_date = date.today()
            self.due_date = self.draw_date + timedelta(days=settings.INVOICE_DUE_DATE_INTERVAL)
            self.status = 'ACTIVE'
        super(Invoice, self).save(*args, ** kwargs)
    
    @classmethod
    def generate_variable_symbol(cls):
        """
        Generates variable symbol for new invoice. Variable symbol is used because specific_symbol alone would
        not unambiguously identify the invoice. Also VS should allways be unique.
        """
        now = datetime.now()
        ss = now.strftime("%m%d%H")
        order_count = len(cls.objects.filter(variable_symbol=ss))
        # expect maximum of 9998 orders per hour
        return u"%s%04d" % (ss, order_count + 1)
    
    @classmethod
    def create_invoice(cls, usr):
        """
        Creates, saves and returns new invoice for the given user.
        Also subtracts the invoice price from the user's account
        """
        activities = usr.get_invoiceable_activities()
        if len(activities) > 0:
            inv = Invoice(user=usr)
            inv.save()
            sum = inv.total_price_with_tax()
            if settings.ACCOUNTING_ENABLED == False:
                pdf = inv.get_printable_invoice()
                inv.pdf_invoice = pdf.generate_pdf()
            #if total price is less then zero then all these activites where taken from account
            #therefore invoice was already paid
            if sum < 0:
                inv.status = 'PAID'    
            if settings.ACCOUNTING_ENABLED:
                try:
                    accounting =  importlib.import_module(settings.ACCOUNTING['IMPLEMENTATION'])
                    account_instance = accounting.get_accounting_instance()
                    account_instance.create_invoice(inv)
                    inv.pdf_invoice = account_instance.print_invoice(inv)
                except ImportError, ex:
                    get_logger().error("Can't import accounting implementation from settings") 
            inv.save()    
            return inv
        else: 
            return None           

    @classmethod
    def get_count_of_unpaid_invoices(cls, usr):
        """
        Returns number of unpaid invoices.
        """
        #get all invoices of user ur
        number_of_invoices = len(Invoice.objects.filter(user=usr))
        # now get number of paid
        number_of_paid = len(Invoice.objects.filter(user=usr, status='PAID'))        
        return number_of_invoices - number_of_paid


    
    @classmethod
    def collect_payment(cls, vs, ss, sum):
            """
        Collects incoming payment. Checks variable symbol and sum against invoice data
        """
            inv = Invoice.objects.filter(variable_symbol=vs)
            inv = inv.get(specific_symbol=ss)
            if inv is None:
                return
            if inv.total_price_with_tax() == sum:
                inv.payment_datetime = datetime.now()
                inv.user.account.balance += sum
                inv.status = 'PAID'
                inv.save()
        
        
class InvoiceItem(models.Model):
    account_activity = models.OneToOneField(AccountActivity,
                                            related_name='invoice_item', verbose_name=_('Account activity'))
    
    invoice = models.ForeignKey(Invoice, related_name='items',
                                verbose_name=_('Invoice'))

    objects = managers.InvoiceItemManager()

    class Meta:
        verbose_name = _('Invoice item')
        verbose_name_plural = _('Invoice items')

    def __unicode__(self):
        return "Invoice item for %s" % self.account_activity
    
    @property
    def amount(self):
        """
        Returns amount of money 
        """
        return abs(self.account_activity.money_amount)

    def amount_with_tax(self):
        """
        Returns item's amount of money with tax added
        """
        tax = abs(self.amount) * Decimal(self.invoice.user.home_subsidiary.tax_rate / 100)
        return abs(self.amount) + tax
    

signals.post_save.connect(InvoiceItem.objects.create_for_invoice, Invoice)
if settings.ACCOUNTING_ENABLED:
    try:
        accounting =  importlib.import_module(settings.ACCOUNTING['IMPLEMENTATION'])
        account_instance = accounting.get_accounting_instance()
        signals.post_delete.connect(account_instance.delete_invoice_receiver, Invoice)
        signals.post_save.connect(account_instance.save_invoice_receiver, Invoice)
    except ImportError, ex:
        get_logger().error("Can't import accounting implementation from settings")   
