from django.conf.urls import url, include
from cars.views import CarModelViewSet, CarColorViewSet, FuelBillViewSet, JourneyListView, ParkingViewSet
from metrocar.cars.views import CarViewSet
from metrocar.reservations.views import ReservationViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
from metrocar.user_management.views import UserViewSet, obtain_auth_token, AccountActivityListView
from user_management.views import AccountViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
# router.register(r'reservationbills', ReservationBillViewSet)
router.register(r'cars', CarViewSet)
router.register(r'carmodels', CarModelViewSet)
router.register(r'carcolors', CarColorViewSet)
router.register(r'fuelbill', FuelBillViewSet, base_name="fuelbill")
router.register(r'users', UserViewSet, base_name="user")
router.register(r'userbalances', AccountViewSet, base_name="userbalance")
router.register(r'parkings', ParkingViewSet, base_name="parking")


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth-token/', obtain_auth_token),
    url(r'accountactivities/',AccountActivityListView.as_view()),
    url(r'journey/', JourneyListView.as_view(),name="journey-list"),
]