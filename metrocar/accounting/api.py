# -*- coding: utf-8 -*-
import invoices_management


def check_incoming_payments():
	invoices_management.check_incoming_payments()

def create_invoice(inv):
	invoices_management.create_invoice(inv)	

def print_invoice(inv):
	return invoices_management.print_invoice(inv)	

def delete_invoice_receiver(sender, **kwargs):
	invoices_management.delete_invoice_receiver(sender, **kwargs)

def save_invoice_receiver(sender, **kwargs):
	invoices_management.save_invoice_receiver(sender, **kwargs)	