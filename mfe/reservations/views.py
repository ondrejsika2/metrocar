'''
Created on 11.3.2010

@author: xaralis
'''

from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.context import RequestContext
from django.utils.translation import gettext_lazy as _

from metrocar.cars.models import Car
from metrocar.reservations.models import Reservation, ReservationError

from mfe.utils.forms import render_to_wizard, ViewFormWizard

class ReservationWizard(ViewFormWizard):
    from metrocar.reservations.forms import ReservationForm
    from mfe.reservations.forms import ReservationFormOne, ReservationFormThree
    _forms = [ ReservationFormOne, ReservationForm, ReservationFormThree ]
    
    def get_template(self, step):
        return 'reservations/reservation/%s.html' % step
            
    
    def process_step(self, request, form, step):
        from datetime import datetime
        " Overload to add extra content "
        
        if request.POST.has_key('0-car_id'):
            self.extra_context['car'] = Car.objects.get(
                pk=request.POST['0-car_id']
            )
        if step == 1:
            if hasattr(form, 'cleaned_data'):
                self.extra_context['price_estimation'] = Reservation.get_price_estimation(
                    self.extra_context['car'], 
                    form.cleaned_data['reserved_from'], 
                    form.cleaned_data['reserved_until']
                )
                self.extra_context['reserved_from'] = form.cleaned_data['reserved_from']
                self.extra_context['reserved_until'] = form.cleaned_data['reserved_until']
    
    def done(self, request, form_list):
        clean_data = form_list[1].cleaned_data
        car = Car.objects.get(pk=clean_data['car_id'])
        reservation = Reservation.objects.create_reservation(
            request.user, car, clean_data['reserved_from'], 
            clean_data['reserved_until'])
        return HttpResponseRedirect(reverse('mfe_reservations_reservation_success'))
    
@login_required
def reservation(request, car_id=None):
    context = { 'user_id': request.user.pk }
    if car_id: context['car_id'] = int(car_id)
    initial = {
        0: context,
        1: context,
        2: context
    }
    return render_to_wizard(ReservationWizard, context=context, 
        request=request, initial=initial)
    
@login_required
def pending_list(request, page=None):
    pending_reservations_dict = {
        'queryset': Reservation.objects.pending().filter(user=request.user),
        'paginate_by': 20,
        'page': page,
        'template_name': 'reservations/pending_reservation_list.html'
    }
    return object_list(request, **pending_reservations_dict)

@login_required
def finished_list(request, page=None):
    finished_reservations_dict = {
        'queryset': Reservation.objects.finished().filter(user=request.user),
        'paginate_by': 20,
        'page': page,
        'template_name': 'reservations/finished_reservation_list.html'
    }
    return object_list(request, **finished_reservations_dict)

@login_required
def cancel_reservation(request, reservation_id, confirmed=False):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    if confirmed:
        try:
            reservation.cancel()
        except ReservationError:
            messages.error(request, _('It is not possible to cancel reservation that has already begun.'))
            
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.warning(request, _('Do you want to cancel reservation %s for car %s? <a href="%s">Yes</a> | <a href="%s">No</a>') % (reservation, reservation.car, reverse('mfe_reservations_cancel_reservation', args=[reservation.pk]), request.META['HTTP_REFERER']))

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

