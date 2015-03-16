from abc import ABCMeta, abstractmethod

def get_accounting_instance():
	raise NotImplementedError('This is abstract module, that just defines API of accounting. Create seperate implementation.')

class AccountingManager:
	"""
	This is abstract base class which defines and enscalpulate api offered by accounting module.
	For a concrete accounting system just inherit this class and create something like FlexibeeManager 
	that is supposed to work with Flexibee accounting system, or PohodaManager which is working with
	Pohoda accounting system. 
	"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def create_invoice(self, invoice):
		"""
		This method should create invoice in the accounting system.
		As a argument it expects metrocar.invoices.models.Invoice object.
		:param invoice: metrocar.invoices.models.Invoice object
		"""
		pass

	@abstractmethod	
	def delete_invoice_receiver(self, sender, **kwargs):
		"""
		This abstract method is used as a receiver of signal from metrocar.invoices, 
		whenever the invoice instance is deleted it must delete invoice in the accounting sysyem.
		"""
		pass

	@abstractmethod
	def save_invoice_receiver(self, sender, **kwargs):
		"""
		This abstract method is used as a receiver of signal from metrocar.invoices, 
		whenever the invoice instance is updated it must update invoice in the accounting sysyem.
		"""
		pass

	@abstractmethod
	def print_invoice(self, invoice):
		"""
		This abstract method is supposed to create pdf file of invoice. 
		It returns path to the location of the new created invoice. The implementation
		depends on the accounting system that is currently in use.
		Returns: string which is path to th pdf file
		:param invoice: metrocar.invoices.models.Invoice object		
		"""
		pass

	@abstractmethod
	def check_incoming_payments(self):
		"""
		This abstract method should pair incoming payments with invoices and then 
		set all paid invoices to PAID status in the metrocar system.
		"""
		pass