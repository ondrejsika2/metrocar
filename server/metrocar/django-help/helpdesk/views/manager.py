# -*- coding: utf-8 -*-



from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from helpdesk.forms import TechnicianTicketForm
from django.contrib.auth.decorators import login_required

from helpdesk.models import Ticket, FollowUp

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

def index(request):
	""" 
	Show manager index. 
	Contains list of ticket in "To resolve" status,
	list of tickets being solved by sthis technician,
	a form to report issue for customer.
	"""
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
			
	new_tickets = Ticket.objects.filter(status=Ticket.NEW_STATUS)
	checking_tickets = Ticket.objects.filter(status=Ticket.CHECKING_STATUS)
			
	return render(request, 'helpdesk/manager/index.html', 
		{'new_tickets' : new_tickets, 'checking_tickets' : checking_tickets})
				
def show_ticket(request, ticket_id):
	"""" Show one ticket, technician view. Allows to view only tickets reported by this technician. """
	try:
		ticket = Ticket.objects.get(pk=ticket_id)
		# check if the ticket was reported by this user
		#if not ticket.assigned_to.id == request.user.id:
		#	raise Http404
	except:
		raise Http404
		
	comments = FollowUp.objects.filter(ticket=ticket_id)
	
	return render(request, 'helpdesk/manager/show_ticket.html', {'ticket' : ticket, 'public_comments':comments}) 
