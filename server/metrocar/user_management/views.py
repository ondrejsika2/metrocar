from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from metrocar.user_management.models import MetrocarUser
from metrocar.user_management.permissions import IsAdminUserOrOwner
from metrocar.user_management.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrOwner,
    )
    queryset = MetrocarUser.objects.all()
    serializer_class = UserSerializer
