from itertools import chain
from operator import attrgetter
from rest_framework import status
from rest_framework import viewsets,generics
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from metrocar.cars.models import FuelBill
from metrocar.reservations.models import ReservationBill

from metrocar.user_management.models import MetrocarUser, Deposit, Account, AccountActivity, UserRegistrationRequest
from metrocar.user_management.permissions import IsAdminUserOrOwner
from metrocar.user_management.serializers import MetrocarUserSerializer, AccountSerializer, AccountActivitySerializer, \
    ReservationBillSerializer, DepositSerializer, FuelBillSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrOwner,
    )
    queryset = MetrocarUser.objects.all()
    serializer_class = MetrocarUserSerializer


class UserAuthToken(views.ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            print
            return Response({
                'token': token.key,
                'user': token.user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = UserAuthToken.as_view()


class RegistrationViewSet(viewsets.ModelViewSet):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = MetrocarUserSerializer
    model = MetrocarUser

    def create(self, request):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)

            print self.object

            user_registration_request = UserRegistrationRequest(
                user=self.object
            )
            user_registration_request.save()

            Token.objects.get_or_create(user=self.object)

            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrOwner,
    )
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)


class AccountActivityListView(generics.ListAPIView):

    serializer_class = AccountActivitySerializer

    def list(self, request, *args, **kwargs):

        # Create an iterator for the querysets and turn it into a list.
        results_list = list(
            chain(
                ReservationBill.objects.all(),
                Deposit.objects.all(),
                FuelBill.objects.all(),
            )
        )

        # Build the list with items based on the FeedItemSerializer fields
        results = list()

        sorted_list = sorted(results_list, key=attrgetter('datetime') , reverse=True)

        for entry in sorted_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, ReservationBill):
                serializer = ReservationBillSerializer(entry)
            if isinstance(entry, Deposit):
                serializer = DepositSerializer(entry)
            if isinstance(entry, FuelBill):
                serializer = FuelBillSerializer(entry)

            results.append(serializer.data)

        return Response(results)
