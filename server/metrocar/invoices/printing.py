from time import strftime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.conf import settings
import os


from django.http import HttpResponse


class PrintableInvoice:
    """
    Invoice representation which is printable and can be returned as
    django HttpResponse object.
    """
    FORMAT_PDF = 'pdf'
    FORMAT_HTML = 'html'
    
    def __init__(self, invoice):
        self.set_invoice(invoice)
    
    def set_invoice(self, invoice):
        self._invoice = invoice
    
    def get_content(self):
        raise NotImplementedError
    
    def get_response(self):
        raise NotImplementedError
    
    @classmethod
    def get_mime(cls):
        raise NotImplementedError
    
    def get_filename_string(self):
        return '%s_%s' % (self._invoice.user.username,
            self._invoice.variable_symbol)
    
    @classmethod
    def create_printable_invoice(cls, invoice, format):
        """
        Returns correct PrintableInvoice instance for given invoice and format.
        """
        if format == cls.FORMAT_PDF:
            return PrintableInvoicePdf(invoice)
        elif format == cls.FORMAT_HTML:
            return PrintableInvoiceHtml(invoice)
        else:
            raise ValueError('Unknown PrintableInvoice format')

class PrintableInvoicePdf(PrintableInvoice):
    def generate_pdf(self):
		"""
		Renders an invoice into html template and transfers it to a pdf
		document
		Returns url of the generated pdf
		"""
		tmplt = get_template('invoice_template.html')
		context = Context({'pagesize': 'A4', 'invoice': self._invoice, 'numb': self._invoice.pk })
		html = tmplt.render(context)
		save_to = os.path.join('invoices', strftime('%Y-%m'))
		save_path = os.path.join(settings.MEDIA_ROOT, save_to)
		if not os.path.exists(save_path):
			os.makedirs(save_path)
		
		buffer = open('%s/%s.pdf' % (save_path, self.get_filename_string()), 'wb')
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), buffer)
		buffer.close()
		
		return '%s/%s.pdf' % (save_to, self.get_filename_string())
    
    def get_response(self):
        response = HttpResponse(mimetype=self.get_mime())
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' \
            % self.get_filename_string()
        response.write(self.get_content())
        return response
    
    @classmethod    
    def get_mime(cls):
        return 'application/pdf'

class PrintableInvoiceHtml(PrintableInvoice):
    pass
