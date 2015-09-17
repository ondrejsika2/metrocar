# coding=utf-8
from itertools import chain
from operator import attrgetter
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework import viewsets,generics
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from metrocar.cars.models import FuelBill
from metrocar.invoices.models import UserInvoiceAddress
from metrocar.reservations.models import ReservationBill

from metrocar.user_management.models import MetrocarUser, Deposit, Account, AccountActivity, UserRegistrationRequest
from metrocar.user_management.permissions import IsAdminUserOrOwner
from metrocar.user_management.serializers import MetrocarUserSerializer, AccountSerializer, AccountActivitySerializer, \
    ReservationBillSerializer, DepositSerializer, FuelBillSerializer, RegistrationSerializer
from metrocar.utils.api.paginations import TimelineMetaSerializer, \
    TimelinePaginationSerializer
from metrocar.settings.base import REST_FRAMEWORK
from metrocar.utils.exceptions import CustomAPIException


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrOwner,
    )
    queryset = MetrocarUser.objects.all()
    serializer_class = MetrocarUserSerializer

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            # full_clean on model instance may be called in pre_save,
            # so we have to handle eventual errors.
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        user_invoice_addresses = UserInvoiceAddress.objects.filter(user=self.object.id)
        if (user_invoice_addresses.__len__()):
            user_invoice_address = user_invoice_addresses[0]
            if "street" in request.DATA:
                user_invoice_address.street = request.DATA["street"]
            if "land_registry_number" in request.DATA:
                user_invoice_address.land_registry_number = request.DATA["land_registry_number"]
            if "zip_code" in request.DATA:
                user_invoice_address.zip_code = request.DATA["zip_code"]
            if "city" in request.DATA:
                user_invoice_address.city = request.DATA["city"]
            user_invoice_address.save()


        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)


        user_request = UserRegistrationRequest.objects.get_or_create(user=self.object)[0]
        user_request.approved = False
        user_request.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUserOrOwner,
    )
    queryset = MetrocarUser.objects.all()
    serializer_class = MetrocarUserSerializer

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            # full_clean on model instance may be called in pre_save,
            # so we have to handle eventual errors.
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)

        self.object.password = make_password(self.object.password)
        self.object.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAuthToken(views.ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            return Response({
                'token': token.key,
                'user': token.user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = UserAuthToken.as_view()


class RegistrationViewSet(viewsets.ModelViewSet):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = RegistrationSerializer
    model = MetrocarUser

    def create(self, request):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)


            errors = {}
            errors_flag = False

            if "street" in request.DATA is False:
                errors["street"] = [
                    "Pole je povinné."
                ]
                errors_flag = True
            if "land_registry_number" in request.DATA is False:
                errors["land_registry_number"] = [
                    "Pole je povinné."
                ]
                errors_flag = True
            if "zip_code" in request.DATA is False:
                errors["zip_code"] = [
                    "Pole je povinné."
                ]
                errors_flag = True
            if "city" in request.DATA is False:
                errors["city"] = [
                    "Pole je povinné."
                ]
                errors_flag = True


            if errors_flag:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            self.object.password = make_password(self.object.password)
            self.object.save()

            user_registration_request = UserRegistrationRequest(
                user=self.object
            )
            user_registration_request.save()

            Token.objects.get_or_create(user=self.object)

            user_invoice_address = UserInvoiceAddress(
                street = request.DATA["street"],
                land_registry_number = request.DATA["land_registry_number"],
                zip_code = request.DATA["zip_code"],
                city = request.DATA["city"],
                user = self.object
            )
            user_invoice_address.save()


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

    model = AccountActivity
    serializer_class = AccountActivitySerializer
    paginate_by = 5
    pagination_serializer_class = TimelinePaginationSerializer

    def list(self, request, *args, **kwargs):

        account = Account.objects.get(user=self.request.user)

        # Create an iterator for the querysets and turn it into a list.
        results_list = list(
            chain(
                ReservationBill.objects.filter(account=account),
                Deposit.objects.filter(account=account),
                FuelBill.objects.filter(account=account, approved=True),
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


        paginator = Paginator(results, self.paginate_by)

        page = request.QUERY_PARAMS.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            users = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = TimelinePaginationSerializer(users,
                                             context=serializer_context)
        return Response(serializer.data)

