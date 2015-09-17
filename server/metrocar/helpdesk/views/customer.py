# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.http import Http404

from helpdesk.forms import CustomerTicketForm, CustomerTicketSupplementForm
from django.contrib.auth.decorators import login_required

from helpdesk.models import Ticket, FollowUp

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# Metrocar dependency 
from metrocar.reservations.models import Reservation
from metrocar.cars.models import Car    

def index(request):
	""" 
	Show customer index. 
	Contains list of tickets reported by this customer, 
	list of tickets reported by this customer that need supplement.
	"""
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
			
	customer_reports = Ticket.objects.filter(who_reported=request.user.id)
	customer_reports_supplement_needed = customer_reports.filter(status=Ticket.SUPPLEMENT_NEEDED_STATUS)
			
	return render(request, 'helpdesk/customer/index.html', 
		{'customer_reports' : customer_reports, 'customer_reports_supplement_needed' : customer_reports_supplement_needed})
				
def show_ticket(request, ticket_id):
	"""" Show one ticket, customer view. Allows to view only tickets reported by this customer. """
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	try:
		ticket = Ticket.objects.get(pk=ticket_id)
		# check if the ticket was reported by this user
		if not ticket.who_reported.id == request.user.id:
			raise Http404
	except:
		raise Http404
	# Customer can see only public comments/followups
	comments = FollowUp.objects.filter(ticket=ticket_id,public=True)
	
	return render(request, 'helpdesk/customer/show_ticket.html', {'ticket' : ticket, 'public_comments':comments}) 
		
def ticket_supplement(request, ticket_id):
	""" Supplement of ticket by customer. """
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	# Get the ticket that needs to be supplied.
	try:
		ticket = Ticket.objects.get(pk=ticket_id)
		if not ticket.who_reported.id == request.user.id:
			raise Http404
	except:
		return Http404
	
	if request.method == 'POST': # If the form has been submitted...
		form = CustomerTicketSupplementForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.ticket_id = ticket_id # which ticket is being supplied
			form.user_id = request.user.id # who is the one who supplies (Should be the same as who_reported)
			form.save()
			return HttpResponseRedirect(reverse('helpdesk_customer_index'))
	else:
		# Create form.
		form =  CustomerTicketSupplementForm()
	# Customer can see only public comments/followups
	comments = FollowUp.objects.filter(ticket=ticket_id,public=True)
		
	return render(request, 'helpdesk/customer/ticket_supplement.html', {'form':form, 'ticket' : ticket, 'public_comments': comments })
	
	
def report_defect(request):
	"""
	Page for customer with form for reporting car defects.
	"""
	# If the user if not logged in, redirect him to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	if request.method == 'POST': # If the form has been submitted...
		form = CustomerTicketForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.who_created_r = User.objects.get(pk=request.user.id)
			form.save()
			return HttpResponseRedirect(reverse('helpdesk_customer_index'))
	else:
		if not request.user.is_active:
			# Inactive user can't report any new defects.
			form = None
		else:
			# Active user, allowed to report defects.
			form =  CustomerTicketForm()
			# Customer should be able to report defects of cars which he had reserved
			form.fields['which_car'].choices = [(c.id, c.__unicode__()) for c in Car.objects.filter(reservations__user_id=request.user.id)] 		
			
	return render(request, 'helpdesk/customer/report_defect.html', {'form':form,}) 
