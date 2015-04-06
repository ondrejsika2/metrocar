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

