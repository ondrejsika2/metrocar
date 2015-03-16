#TODO-Vojta remove this file

# '''
# Created on 27.3.2010
#
# @author: xaralis
# '''
#
# from piston.handler import BaseHandler, AnonymousBaseHandler
# from piston.utils import rc, validate
#
# from metrocar.cars.models import Car
# from metrocar.reservations.models import Reservation
# # from metrocar.reservations.forms import ReservationForm
#
# class AnonymousReservationHandler(AnonymousBaseHandler):
#     """
#     Bridge to allow creation of reservations by client applications.
#
#     Supports GET and POST. Use GET to list reservations, or POST to create
#     a new one.
#
#     Anonymous users are allowed only to perform GET.
#     """
#     allowed_methods = ('GET',)
#     model = Reservation
#     fields = (
#         ('car', ('resource_uri',)),
#         ('user', ('username', 'resource_uri')),
#         'reserved_from',
#         'reserved_until'
#     )
#
#     def read(self, request, id=None):
#         """
#         Reads all reservations and returns information about them or specific
#         reservation if 'id' is supplied.
#
#         Returned information:
#             - car (resource_uri)
#             - user (username, resource_uri)
#             - reserved_from
#             - reserved_until
#         """
#         if id is not None:
#             try:
#                 res = self.model.objects.pending().get(pk=id)
#                 return res
#             except self.model.DoesNotExist:
#                 return rc.NOT_FOUND
#         return self.model.objects.pending()
#
#     @classmethod
#     def resource_uri(cls, *args, **kwargs):
#         return ('api_reservation_handler', ['id'])
#
# class ReservationHandler(BaseHandler):
#     """
#     Bridge to allow creation of reservations by client applications.
#
#     Supports GET and POST. Use GET to list reservations, or POST to create
#     a new one.
#     """
#
#     anonymous = AnonymousReservationHandler
#     allowed_methods = ('GET', 'POST')
#
#     def create(self, request):
#         """
#         Creates new reservation in the system. All validation is same as for
#         frontend. That means following required params:
#             - user_id - this is detected from request and is same as authenticated user performing request
#             - car_id
#             - reserved_from
#             - reserved_until
#
#         All checking of conflicts etc. is handled and if invalid, returned
#         automatically.
#         """
#         data = request.POST.copy()
#         data['user_id'] = request.user.pk
#         # form = ReservationForm(data)
#         # if form.is_valid():
#         #     cd = form.cleaned_data
#         #     car = Car.objects.get(cd['car_id'])
#         #     Reservation.objects.create_reservation(request.user, car,
#         #         cd['reserved_from'], cd['reserved_until'])
#         #     return rc.CREATED
#         # else:
#         return rc.BAD_REQUEST
#