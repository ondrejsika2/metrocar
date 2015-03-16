from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from metrocar.reservations.models import Reservation, ReservationBill
from metrocar.reservations.serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the reservations
        for the currently authenticated user.
        """
        user = self.request.user
        return Reservation.objects.filter(user=user)

# class ReservationBillViewSet(viewsets.ModelViewSet):
#     permission_classes = (
#         IsOwnerOfReservation,
#     )
#     serializer_class = ReservationBillSerializer
#     queryset = ReservationBill.objects.all()
#
#     def get_queryset(self):
#         """
#         This view should return a list of all the reservation bills
#         for the currently authenticated user.
#         """
#         user = self.request.user
#         reservations = Reservation.objects.filter(user=user)
#         reservation_bills = []
#         for reservation in reservations:
#             reservation_bills.append(ReservationBill.objects.filter(reservation=reservation))
#         return reservation_bills
#         # reservation = Reservation.objects.get(pk=self.request.reservation)
#         # return ReservationBill.objects.filter(user=reservation.user)
