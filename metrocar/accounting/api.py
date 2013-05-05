# -*- coding: utf-8 -*-
import invoices_management


def check_incoming_payments():
	"""
	This function when called will execute automatic pairing of incoming 
	payments in the accounting system and then mark paid invoices as PAID.
	"""
	invoices_management.check_incoming_payments()

def create_invoice(inv):
	"""
	This function creates invoice in the accounting system from the informations
	that are inside inv which is metrocar.invoices.models.Invoice instance
	:param inv: metrocar.invoices.models.Invoice instance
	"""
	invoices_management.create_invoice(inv)	

def print_invoice(inv):
	"""
	Function returns path to the file that contains pdf of invoice inv. 
	This pdf is printed by accounting system.
	Returns: path to the pdf invoice
	:param inv: metrocar.invoices.models.Invoice instance 
	"""
	return invoices_management.print_invoice(inv)	

def delete_invoice_receiver(sender, **kwargs):
	"""
	This function act as a receiver of the signal whenever is instance of 
	Invoice deleted from the system. It takes care of deletion of Invoice in 
	the accounting system.
	"""
	invoices_management.delete_invoice_receiver(sender, **kwargs)

def save_invoice_receiver(sender, **kwargs):
	"""
	This function act as a receiver of the signal whenever is instance of 
	Invoice save to the db. It takes care of updating of the invoice.
	It is not supposed to hnadle situations like creation of invoice.
	"""
	invoices_management.save_invoice_receiver(sender, **kwargs)	