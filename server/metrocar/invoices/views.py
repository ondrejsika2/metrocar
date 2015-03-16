
from django.http import HttpResponseForbidden

from metrocar.invoices.models import Invoice, PrintableInvoice

def print_invoice(request, invoice_id, format=PrintableInvoice.FORMAT_PDF):
    """
    Prints the selected invoice. Allow only if requiring user is the subject
    of invoice or system administrator.
    """
    invoice = Invoice.objects.get(pk=invoice_id)
    if request.user.is_authenticated() and \
        (request.user.pk == invoice.user.pk or request.user.is_superuser):
        pi = invoice.get_printable_invoice(format)
        return pi.get_response()
    else:
        return HttpResponseForbidden()
     
