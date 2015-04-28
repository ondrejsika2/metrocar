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
	Show technician index. 
	Contains list of ticket in "To resolve" status,
	list of tickets being solved by sthis technician,
	a form to report issue for customer.
	"""
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	if request.method == 'POST': # If the form has been submitted...
		form = TechnicianTicketForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.who_created_r = User.objects.get(pk=request.user.id)
			form.save()
			return HttpResponseRedirect(reverse('helpdesk_technician_index'))
	else:
		if not request.user.is_active:
			# Inactive user can't report any new defects.
			form = None
		else:
			# Active user, allowed to report defects.
			form =  TechnicianTicketForm()
			
	to_resolve_tickets = Ticket.objects.filter(status=Ticket.TO_RESOLVE_STATUS)
	resolving_tickets = Ticket.objects.filter(status=Ticket.RESOLVING_STATUS)
			
	return render(request, 'helpdesk/technician/index.html', 
		{'form': form, 'to_resolve_tickets' : to_resolve_tickets, 'resolving_tickets' : resolving_tickets})
				
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
	
	return render(request, 'helpdesk/customer/show_ticket.html', {'ticket' : ticket, 'public_comments':comments}) 
	
def take_ticket(request, ticket_id):
	try:
		ticket = Ticket.objects.get(pk=ticket_id)
		# check if the ticket was reported by this user
		#if not ticket.assigned_to.id == request.user.id:
		#	raise Http404
	except:
		raise Http404
		
	ticket.assigned_to = User.objects.get(pk=request.user.id)
	ticket.status = Ticket.RESOLVING_STATUS
	ticket.save()
	
	return HttpResponseRedirect(reverse('helpdesk_technician_index'))
		
	
