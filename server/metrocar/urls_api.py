from django.conf.urls import url, include
from metrocar.cars.views import CarViewSet
from metrocar.reservations.views import ReservationViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

# Create a router and register our viewsets with it.
from metrocar.user_management.views import UserViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
# router.register(r'reservationbills', ReservationBillViewSet)
router.register(r'cars', CarViewSet)
router.register(r'users', UserViewSet, base_name="user")

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth-token/', views.obtain_auth_token)
]