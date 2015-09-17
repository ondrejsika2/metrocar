from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from metrocar.reservations.models import Reservation, ReservationBill
from metrocar.reservations.serializers import ReservationSerializer
from metrocar.user_management.permissions import IsUserFullyActive
from metrocar.utils.api.paginations import CustomPaginationSerializer
from metrocar.settings.base import REST_FRAMEWORK

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsUserFullyActive,
    )
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    paginate_by = REST_FRAMEWORK['CUSTOM_RECORDS_PER_PAGE']
    pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        """
        This view should return a list of all the reservations
        for the currently authenticated user.
        """
        user = self.request.user
        return Reservation.objects.filter(user=user)

