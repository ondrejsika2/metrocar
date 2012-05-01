#coding=utf-8
'''
Created on 11.3.2010

@author: xaralis
'''
from django.core.exceptions import ValidationError

from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils import simplejson
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.context import RequestContext
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import sys
import traceback
from metrocar.cars.models import Car, Journey
from metrocar.reservations.models import Reservation, ReservationError
from mfe.utils.forms import render_to_wizard, ViewFormWizard

class ReservationWizard(ViewFormWizard):
    from mfe.reservations.forms import ReservationFormOne, ReservationFormThree
    _forms = [ ReservationFormOne, ReservationFormThree ]

    def get_template(self, step):
        return 'reservations/reservation/%s.html' % step
            
    
    def process_step(self, request, form, step):
        " Overload to add extra content "
        if request.POST.has_key('0-car_id'):
            self.extra_context['car'] = Car.objects.get(
                pk=request.POST['0-car_id']
            )

        if step == 0:
            from metrocar.config.settings_base import DEFAULT_RESERVATION_DISTANCE
            if hasattr(form, 'cleaned_data'):
                car = self.extra_context['car']
                total_price_estimation = Reservation.get_price_estimation(
                    car,
                    form.cleaned_data['reserved_from'],
                    form.cleaned_data['reserved_until'],
                    DEFAULT_RESERVATION_DISTANCE
                )
                base_price = Reservation.get_base_price(
                    car,
                    form.cleaned_data['reserved_from'],
                    form.cleaned_data['reserved_until']
                )

                pricelist = car.model.get_pricelist()

                self.extra_context['total_price_estimation'] = ('%0.2f' % total_price_estimation)
                self.extra_context['base_price'] = ('%0.2f' % base_price)
                self.extra_context['reserved_from'] = form.cleaned_data['reserved_from']
                self.extra_context['reserved_until'] = form.cleaned_data['reserved_until']
                self.extra_context['default_reservation_distance'] = DEFAULT_RESERVATION_DISTANCE
                self.extra_context['pickup_fee'] = ('%0.2f' % pricelist.pickup_fee)
                self.extra_context['reservation_fee'] = ('%0.2f' % pricelist.reservation_fee)
                self.extra_context['price_by_distance'] = ('%0.2f' % Reservation.get_price_by_distance(car, DEFAULT_RESERVATION_DISTANCE))

    def done(self, request, form_list):
        clean_data = form_list[0].cleaned_data
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
    }
    try:
        return render_to_wizard(ReservationWizard, context=context, request=request, initial=initial)
    except ValidationError:
        messages.error(request, _('This car seems to be already registered. Please try to choose another one.'))
        return HttpResponseRedirect(reverse('mfe_reservations_reservation'))
    except (Exception, ReservationError):
        messages.error(request, _('Unexpected error has been occured. Please try it again.'))
        return HttpResponseRedirect(reverse('mfe_reservations_reservation'))

@login_required
def recount_price_estimation(request):
    if not request.is_ajax():
        return HttpResponseNotFound()

    distance = request.GET.get('distance')
    car = Car.objects.get(pk=request.GET.get('car_id'))
    price_by_distance = Reservation.get_price_by_distance(car, distance)

    reserved_from_date = request.GET.get('reserved_from_date')
    reserved_from_time = request.GET.get('reserved_from_time')
    reserved_until_date = request.GET.get('reserved_until_date')
    reserved_until_time = request.GET.get('reserved_until_time')
    reserved_from = datetime.strptime(('%s %s' % (reserved_from_date, reserved_from_time)), '%d.%m.%Y %H:%M')
    reserved_until = datetime.strptime(('%s %s' % (reserved_until_date, reserved_until_time)), '%d.%m.%Y %H:%M')
    total_price_estimation = Reservation.get_price_estimation(car, reserved_from, reserved_until, distance)

    want_of_money = (request.user.account.balance < total_price_estimation)
    data = simplejson.dumps({
        'price_by_distance' : ('%0.2f' % price_by_distance),
        'total_price_estimation' : ('%0.2f' % total_price_estimation),
        'want_of_money': want_of_money,
        'warning_msg': str(_('You have want of money on your account!') if want_of_money else '')
    })
    return HttpResponse(data, 'application/javascript')

@login_required
def pending_list(request, page=None):
    pending_reservations_dict = {
        'queryset': Reservation.objects.pending().filter(user=request.user).order_by('reserved_from'),
        'paginate_by': 20,
        'page': page,
        'template_name': 'reservations/pending_reservation_list.html'
    }
    return object_list(request, **pending_reservations_dict)

@login_required
def finished_list(request, page=None):
    finished_reservations_dict = {
        'queryset': Reservation.objects.finished().filter(user=request.user).order_by('-ended'),
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
        except Exception, e:
           messages.error(request, e.message)
            
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.warning(request, _('Do you want to cancel reservation %(reservation)s for car %(car)s? <a href="%(yes_url)s">Yes</a> | <a href="%(no_url)s">No</a>') % {'reservation' : reservation, 'car' : reservation.car, 'yes_url' : reverse('mfe_reservations_cancel_reservation', args=[reservation.pk]), 'no_url' : request.META['HTTP_REFERER']})
        print request.META['HTTP_REFERER']
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if not reservation.user == request.user:
        messages.error(request, _('Access to reservation is denied.'))
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        journeys = Journey.objects.filter(user=request.user,reservation=reservation)
        return render_to_response('reservations/edit_reservation.html', {
            'reservation': reservation,
            'journeys': journeys
            }, context_instance=RequestContext(request))


@login_required
def outstanding_loans(request, page=None):
    reservations = Reservation.objects.non_finished().filter(user=request.user)
    non_finished_reservations_dict = {
        'queryset': reservations,
        'paginate_by': 20,
        'page': page,
        'template_name': 'reservations/outstanding_loans.html'
    }
    return object_list(request, **non_finished_reservations_dict)

@login_required
def add_journey(request, reservation_id):
    from mfe.reservations.forms import AddJourneyForm

    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # only 1 journey can be inserted
    if reservation.has_journey():
        messages.error(request, _('It is not allowed to add another journey.'))
        return HttpResponseRedirect(reverse('mfe_reservations_edit_reservation', kwargs={'reservation_id':reservation_id}))

    if request.method == 'POST':
        f_data = request.POST.copy()
        f_data['start_datetime_0'] = datetime.strptime(f_data['start_datetime_0'], '%d.%m.%Y').strftime('%Y-%m-%d')
        f_data['end_datetime_0'] = datetime.strptime(f_data['end_datetime_0'], '%d.%m.%Y').strftime('%Y-%m-%d')
        form = AddJourneyForm(data=f_data)
        if form.is_valid():
            journey = None
            try:
                data = {
                    'comment': form.cleaned_data['comment'],
                    'start_datetime': form.cleaned_data['start_datetime'],
                    'end_datetime': form.cleaned_data['end_datetime'],
                    'length': (form.cleaned_data['speedometer_end'] or 0) - (form.cleaned_data['speedometer_start'] or 0),
                    'speedometer_start': form.cleaned_data['speedometer_start'],
                    'speedometer_end': form.cleaned_data['speedometer_end'],
                    'reservation': reservation,
                    'car': reservation.car,
                    'user': request.user,
                }
                journey = Journey.objects.create(**data)
                if not journey.is_valid:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    journey.update_total_price()
                    # check user's account amount
                    if journey.total_price > request.user.account.balance:
                        raise ReservationError(_(u'You do not have enough money amount on your account. Journey bill is %.2f Kč.') % journey.total_price)

                    journey.save()
                    if reservation.started == None:
                        reservation.started = form.cleaned_data['start_datetime']
                        reservation.save();
                    return HttpResponseRedirect(reverse('mfe_reservations_edit_reservation', kwargs={'reservation_id':reservation_id}))
            except (AssertionError, ReservationError, Exception), e:
                if journey is not None:
                   journey.delete()
                if type(e) in [AssertionError, ReservationError]:
                    messages.error(request, e.message)
                else:
                    messages.error(request, _('Unexpected error has been occured.'))

            form.data['start_datetime_0'] = request.POST['start_datetime_0']
            form.data['end_datetime_0'] = request.POST['end_datetime_0']
        else:
            form.data['start_datetime_0'] = request.POST['start_datetime_0']
            form.data['end_datetime_0'] = request.POST['end_datetime_0']
    else:
        reserved_from = reservation.reserved_from
        reserved_until = reservation.reserved_until
        f_data = {
            'start_datetime' : [reserved_from.strftime('%d.%m.%Y'), reserved_from.strftime('%H:%M')],
            'end_datetime' : [reserved_until.strftime('%d.%m.%Y'), reserved_until.strftime('%H:%M')]
        }
        form = AddJourneyForm(initial=f_data)

    return render_to_response(
        "reservations/add_journey.html", {'form': form, 'view': 'add', 'reservation': reservation},
        context_instance=RequestContext(request)
    )

@login_required
def delete_journey(request, journey_id):
    journey = get_object_or_404(Journey, pk=journey_id, user=request.user)

    try:
        journey.delete()
    except Exception:
        messages.error(request, _('Error'))

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def finish_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    try:
        if not reservation.finish(by_daemon=True, normalize_journeys=False):
            messages.error(request, _('Reservation could not be finished. Some error has been occured.'))
    except Exception, e:
        messages.error(request, e.message)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponseRedirect(reverse('mfe_reservations_finish'))

@login_required
def confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    try:
        if reservation.finished:
            raise Exception, _('Reservation has been already finished.')

        journeys = Journey.objects.filter(user=request.user,reservation=reservation)
        if journeys:
            pricelist = reservation.car.model.get_pricelist()
            return render_to_response('reservations/confirmation.html', {
                'reservation': reservation,
                'journeys': journeys,
                'pickup_fee': pricelist.pickup_fee,
                'reservation_fee': pricelist.reservation_fee,
                'total_price': reservation.count_total_price()
            }, context_instance=RequestContext(request))

        return HttpResponseRedirect(reverse('mfe_reservations_outstanding_loans'))

    except Exception, e:
        messages.error(request, e.message)
        if 'HTTP_REFERER' not in request.META:
            return HttpResponseRedirect(reverse('mfe_reservations_outstanding_loans'))
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])



