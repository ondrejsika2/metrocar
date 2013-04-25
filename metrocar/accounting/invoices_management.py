# -*- coding: utf-8 -*-
from time import strftime
import os
from flexipy.exceptions import FlexipyException
import flexipy
#get logger 
from metrocar.utils.log import get_logger


def create_invoice(invoice):
	"""
	This function except metrocar Invoice object.
	It creates invoice in accouting system(Flexibee).
	:param invoice: metrocar.invoices.models.Invoice object
	"""
	#get config
	conf = flexipy.config
	invoice_items = []
	invoice_params = {}
	for item in invoice.get_items():
		#account activity of item
		activity = item.account_activity
		#abs because if invoice is paid than all money where taken from account
		if invoice.status == 'PAID':
			it_price = str(abs(activity.money_amount))
		else:
			it_price = str(activity.money_amount)
		it = {'kod':'item'+str(item.id),'nazev': str(activity.as_concrete_class()), 'typSzbDphK':'typSzbDph.dphZakl','szbDph':'21','zdrojProSkl':False, 'ucetni':True,'cenaMj':it_price, 'typPolozkyK':conf.get_typ_polozky_vydane()[0]}
		invoice_items.append(it)
	# i need infromation about address of user for invoice	
	inv_address = invoice.user.get_invoice_address()
	street = inv_address.street +' '+ str(inv_address.land_registry_number)
	address_params = {'nazFirmy':invoice.user.full_name(),'ulice':street,'mesto':inv_address.city,'psc':inv_address.zip_code,'postovniShodna':True}
	invoice_params = {'typUcOp':'code:'+conf.get_typ_ucetni_operace()[0],'specSym':invoice.specific_symbol,'datSplat':str(invoice.due_date)}
	invoice_params.update(address_params)
	# now check if invoice is paid aka money where already taken from user's account
	if invoice.status == 'PAID':
		invoice_params['stavUhrK']='stavUhr.uhrazenoRucne'
		#todo datum splatnosti 
	try:
		result = flexipy.create_vydana_faktura(kod='inv'+str(invoice.id), var_sym=invoice.variable_symbol, datum_vyst=str(invoice.draw_date), dalsi_param = invoice_params, polozky_faktury=invoice_items)
		if result[0] == True:
			get_logger().info("Invoice with flexibee id "+str(result[1])+" was successfully created.")
		else:
			get_logger().error("Invoice was not created in Flexibee. Errors are "+str(result[2]))	
	except FlexipyException as e:
		get_logger().error("Error during creation of invoice in Flexibee, error was "+str(e))   
		

def delete_invoice(invoice):
	"""
	This function delete invoice from Flexibee.
	It is used when manager deletes invoice from metrocar administration.	
	:param invoice: metrocar.invoices.models.Invoice object
	"""
	try:
		flexInvoice = flexipy.get_vydana_faktura_by_code(code='inv'+str(invoice.id))
		flexID = flexInvoice['id']
		flexipy.delete_vydana_faktura(flexID)
		get_logger().info("Invoice with flexibee id "+str(invoice.id)+" was successfully deleted.")
	except FlexipyException as e:
		get_logger().error("Error during deletion of invoice in Flexibee, error was "+str(e)) 

def get_all_users_invoices(user):
	"""
	This function get list of all invoices in Flexibee which belong to MetrocarUser.
	:param user: metrocar.user_management.models.MetorcarUser
	:returns: List of all users invoices.
	"""
	list_invoices = []
	#MetrocarUser is specified by specific_number which is created from his id-card number
	#query="specSym='0'"
	try:
		list_invoices = flexipy.get_all_vydane_faktury(query="specSym='"+str(user.specific_symbol)+"'")
	except FlexipyException as e:
		get_logger().error("Error during readinf of users invoices in Flexibee, error was "+str(e))	
	return list_invoices	


def delete_invoice_receiver(sender, **kwargs):
	"""
	This function is receiver of signal from metrocar.invoices app. If invoice is deletd for example 
	in admin interface, it will send signal to delete it from Flexibee
	"""
	#get instance of invoice which will be deleted
	inv = kwargs['instance']
	delete_invoice(inv)	

def update_invoice(invoice):
	"""
	This method is called when invoice is updated through admin interface of metrocar system.
	This should not happen as manager should rather use web interface of Flexibee. But still just 
	for precaution. Also there are only two types of fields that can be modified in admin interface.
	"""
	#first i will get this invoice from flexibee
	try:
		flex_inv = flexipy.get_vydana_faktura_by_code(code='inv'+str(invoice.id))
		flex_inv['datSplat'] = str(invoice.draw_date)
		flex_inv['datSplat'] = str(invoice.due_date)
		inv_id = flex_inv['id']
		flexipy.update_vydana_faktura(inv_id, flex_inv)
	except FlexipyException as e:
		get_logger().error("Error during update of invoice in Flexibee, error was "+str(e))	
		

def save_invoice_receiver(sender, **kwargs):
	"""
	This function is receiving signal from metrocar.invoices.models.Invoice 
	whenever is invoice saved. It will save invoice into Flexibee.
	"""
	inv = kwargs['instance']
	if not kwargs['created']:
		#if kwargs contains created = True then the already existing instance
		#is being created
		update_invoice(inv)

def pair_payments():
	"""
	This function is flexibee specific, because flexibee can pait payemnts automaticly, 
	just by comparing incoming payments vs with invoice vs.
	"""		
	try:
		flexipy.proved_sparovani()
		get_logger().info("Automatic pairing of payments in Flexibee successfully executed.")
	except FlexipyException as e:
		get_logger().error("Error during automatic pairing of payments in Flexibee, error was "+str(e))	

def check_incoming_payments():
	"""
	This function will automaticly execute pairing of payments. Then 
	it will take all invoices from metrocar that are in ACTIVE state and compare them 
	to there doppelganger in Flexibee. 
	"""	
	pair_payments()
	from metrocar.invoices.models import Invoice
	from datetime import datetime
	#get all unpaid invoices from db
	unpaid_inv = Invoice.objects.all().filter(status='ACTIVE')
	for inv in unpaid_inv:
		try:
			#get doppelganger from Flexibee
			flex_inv = flexipy.get_vydana_faktura_by_code(code='inv'+str(inv.id))
			if flex_inv['stavUhrK'] == 'stavUhr.uhrazeno':
				#TODO osetreni castecne uhrady
				#set also metrocar invoice to PAID
				inv.status = 'PAID'
				inv.payment_datetime = datetime.now()
				inv.save()
		except FlexipyException as e:
			get_logger().error("Error during automatic pairing of payments in Flexibee, error was "+str(e))	


def print_invoice(invoice):
	"""
	This function print invoice in flexibee into pdf and save it to MEDIA_ROOT/files/invoices
	It returns path to the file.
	"""
	try:
		flex_inv = flexipy.get_vydana_faktura_by_code(code='inv'+str(invoice.id))
		pdf = flexipy.get_faktura_vydana_pdf(flex_inv['id'])
		filename = '%s_%s' % (invoice.user.username, invoice.variable_symbol)
		save_to = os.path.join('invoices', strftime('%Y-%m'))
		from django.conf import settings
		save_path = os.path.join(settings.MEDIA_ROOT, save_to)
		if not os.path.exists(save_path):
			os.makedirs(save_path)
		file = open('%s/%s.pdf' % (save_path, filename), 'wb')	
		file.write(pdf)
		file.close()
		get_logger().info("Pdf of invoice id="+str(invoice.id)+" successfully created.")
		return '%s/%s.pdf' % (save_to, filename)
	except FlexipyException as e:
		get_logger().error("Error during pdf printig invoice from Flexibee, error was "+str(e))	