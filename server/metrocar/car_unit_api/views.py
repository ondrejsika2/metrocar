# coding:UTF8
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime
from django.core import serializers
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from pipetools import pipe, X, foreach
import geotrack
import json
from metrocar.car_unit_api.models import CarUnit, JourneyDataFile
from metrocar.car_unit_api.utils import authenticate, update_car_status
from metrocar.car_unit_api.validation import valid_timestamp, valid_user_id
from metrocar.reservations.models import Reservation, ReservationBill
from metrocar.utils.apis import APICall, parse_json, process_request, validate_request
from metrocar.utils.geo.validation import valid_location
from metrocar.utils.validation import required, optional, validate_each, valid_int, valid_string, valid_float
from metrocar.cars.models import Journey
from metrocar.utils.validation import validate
from django.conf import settings
from metrocar.user_management.models import UserCard, MetrocarUser, Account, AccountActivity

# --------------------------------------------------------------------------------
# ----- Uložení záznamu ----------------------------------------------------------

class StoreLog(APICall):
    """
    An API method to store one or more log-entries from a car unit.
    """

    rules = (
        required('unit_id', valid_int),
        required('entries'),
        X['entries'] | validate_each(
            required('timestamp', valid_timestamp),
            required('location', valid_location),
            optional('event', valid_string),
            optional('user_id', valid_user_id),
            optional('odometer', valid_float),
            optional('velocity', valid_float),
            optional('consumption', valid_float),
            optional('fuel_remaining', valid_float),
            optional('altitude', valid_float),
            optional('engine_temp', valid_float),
            optional('engine_rpm', valid_float),
            optional('throttle', valid_float),
            optional('gps_accuracy', valid_float),
        ),
    )

    @process_request(pipe
        | parse_json
        | authenticate
        | (validate_request, rules))
    def post(self, request, data):
        store(data['unit_id'], data['entries'])
        return {'status': 'ok'}


def store(unit_id, entries):
    """
    The actual storing action. Assumes valid data.
    """
    for entry in entries:
        geotrack.api.store(unit_id=unit_id, **entry)

    update_car_status(unit_id, entries)

# --------------------------------------------------------------------------------
# ----- Získání rezervací --------------------------------------------------------

class PingView(APICall):
    """
    An API method that returns upcoming reservations for the unit making the
    request.
    """

    @process_request(pipe | parse_json | authenticate)
    def post(self, request, data):
        return {
            'status': 'ok',
            'timestamp': datetime.now(),
        }

# --------------------------------------------------------------------------------
# ----- Získání rezervací --------------------------------------------------------

class Reservations(APICall):
    """
    An API method that returns upcoming reservations for the unit making the
    request.
    """

    @process_request(pipe | parse_json | authenticate)
    def post(self, request, data):
        return {
            'status': 'ok',
            'timestamp': datetime.now(),
            'reservations': get_upcoming_reservations(data['unit_id']),
        }


def get_upcoming_reservations(unit_id):
    return serializers.serialize('json',(CarUnit.objects.get(unit_id=unit_id).car_id > pipe
         | Reservation.objects.get_upcoming))


def reservation_data_for_car_unit(reservation):
    user = reservation['user']
    return {
        'user': reservation_user_data(user),
        'start': reservation['reserved_from'],
        'end': reservation['reserved_until'],
        'reservationId': reservation['id'],
    }


def reservation_user_data(user):
    return {
        'id': user['id'],
        'username': user['username'],
        'password': user['password'],
    }

# --------------------------------------------------------------------------------
# ----- Upload souboru s jízdními daty / Download --------------------------------

class DataUploadView(APICall):

    @method_decorator(csrf_exempt)
    def post(self, request):

        print 'Request data:', request.REQUEST
        print 'Request meta:', request.META
        print 'Request meta.xxx:', request.META["SERVER_SOFTWARE"]
        # print json.loads(request.REQUEST["json"])
        print 'Request meta.uid:', request.META["HTTP_X_UID"]
        print 'Request meta.key:', request.META["HTTP_X_KEY"]

        # custom authentication
        if not self.authenticate(request):
            return {
                'status': 'failed',
                'reason': 'auth not successful'
            }

        # datafile entity id
        # datafileID = json.loads(request.REQUEST["json"])["datafile"];
        datafileID = request.META["HTTP_X_DATAFILE_ID"]
        print 'Upload datafile ID:', datafileID

        # save a file to filesystem
        dataFile = request.FILES['uploadedfile']
        destination = open(settings.UNIT_DATA_FILES_DIR + "/" + dataFile.name, 'wb+')
        for chunk in dataFile.chunks():
             destination.write(chunk)
             destination.close()
        print 'File saved'

        # save a datafile entity
        datafile = JourneyDataFile.objects.get(id = datafileID)
        datafile.filename = dataFile.name
        datafile.filesize = dataFile._size
        datafile.uploaded = True
        datafile.save()

        return {
            'status': 'ok',
            'timestamp': datetime.now(),
        }

    @staticmethod
    def authenticate(request):
        """
        Checks for a valid combination of ``unit_id`` and ``secret_key`` values in
        `data`.
        """
        unit_id = request.META["HTTP_X_UID"]
        secret_key = request.META["HTTP_X_KEY"]

        try:
            unit = CarUnit.objects.get(unit_id=unit_id, secret_key=secret_key)
        except CarUnit.DoesNotExist:
            unit = None

        return unit

class DataDownloadView(APICall):

    def get(self, request, **kwargs):

        # load the file db entry to locate file on filesystem
        fileid = kwargs['fileid']
        datafile = JourneyDataFile.objects.get(id = fileid)
        print "File id: ", datafile.id
        print "Filename: ", datafile.filename
        # return "File name iz: " + datafile.filename;
        filename = settings.UNIT_DATA_FILES_DIR + "/" + datafile.filename

        # retrieve the file from FS
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=%s' + datafile.filename
        response['Content-Length'] = datafile.filesize
        return response

# --------------------------------------------------------------------------------
# ----- Přidání jízdy ------------------------------------------------------------

class JourneyAPI(APICall):
    """
    An API method that returns upcoming reservations for the unit making the
    request.
    """

    @process_request(pipe | parse_json | authenticate)
    def post(self, request, data):

        # reservation
        reservation_id = data["reservation"]
        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            reservation = None
        if not reservation:
            return {
                'status': 'failed',
                'reason': 'reservation not recognised'
            }

        # user
        user_id = data["user_id"];

        # journey
        print "start date:", data["start_datetime"]
        print "end date:", data["end_datetime"]
        journey = Journey(comment="",
                          start_datetime = datetime.strptime(data["start_datetime"], "%Y-%m-%d %H:%M:%S.%f"),
                          end_datetime = datetime.strptime(data["end_datetime"], "%Y-%m-%d %H:%M:%S.%f"),
                          length = data["length"],
                          duration = data["duration"],
                          type = "T",
                          car_id = reservation.car_id,
                          user_id = user_id,
                          reservation = reservation,
                          total_price = reservation.count_total_price(journey)
                          )
        journey.save()

        # prepare datafile for future upload
        datafile = JourneyDataFile(journey = journey);
        datafile.save()

        # close the reservation, calc price
        reservation.cancelled = False
        reservation.finished = True
        reservation.price = journey.total_price
        reservation.save(force_save_user = True)
        print "Reservation price:", reservation.price

        # get user account
        account = Account.objects.get(user_id=user_id)

        # bill the reservation + journey -> create account activity
        reservation_bill = ReservationBill.objects.create_for_reservation(reservation)

        journey

        return {
            'status': 'ok',
            'timestamp': datetime.now(),
            'local_journey_id': data.get("local_journey_id"),
            'datafile_server_id': datafile.id,
            'cost_billed': float(reservation.price)
        }

# --------------------------------------------------------------------------------
# ----- Přihlášení uživatele k rezervaci -----------------------------------------

class ReservationCheckIn(APICall):
    """
    An API method handling user's card contact with on-board device.
    It check's whether user have an active reservation for current time and
    given car.
    """

    @process_request(pipe | parse_json | authenticate)
    def post(self, request, data):

        # get car unit making request, already authenticated
        unit_id=data['unit_id']
        try:
            unit = CarUnit.objects.get(unit_id=unit_id)
        except CarUnit.DoesNotExist:
            unit = None
        if not unit:
            return {
                'status': 'failed',
                'reason': 'car unit not recognized'
            }
        if not unit.car_id:
            return {
                'status': 'failed',
                'reason': 'car unit not associated to a car'
            }

        # nested user authentication using a card
        userCard = self.authenticate(data)
        if not userCard:
            return {
                'status': 'failed',
                'reason': 'card auth not successful'
            }

        # get user linked with the card
        user = userCard.user
        if not userCard:
            return {
                'status': 'failed',
                'reason': 'card have no user'
            }

        # get user's actual reservations
        now = datetime.now()
        reservations = Reservation.objects.filter(reserved_from__lt = now, reserved_until__gt = now, car_id = unit.car_id, user_id = user.id)
        if len(reservations) == 0:
            reservation = None
        else:
            reservation = reservations[0]
        # try:
        #     reservation = Reservation.objects.get(reserved_from__lt = now, reserved_until__gt = now, car_id = unit.car_id, user_id = user.id)
        # except Reservation.MultipleObjectsReturned:
        #     reservations = Reservation.objects.filter(reserved_from__lt = now, reserved_until__gt = now, car_id = unit.car_id, user_id = user.id)
        #     reservation = reservations[0]
        # except Reservation.DoesNotExist:
        #     reservation = None
        if not reservation:
            return {
                'status': 'failed',
                'reason': 'no reservation found'
            }

        return {
            'status': 'ok',
            'timestamp': datetime.now(),
            'user': user.id,
            'user_firstname': user.user.first_name,
            'user_lastname': user.user.last_name,
            'from': reservation.reserved_from,
            'to': reservation.reserved_until,
            'reservation': reservation.id
        }

    @staticmethod
    def authenticate(data):
        """
        Checks for a valid user card using stored code and key
        """
        cardID = data["card_id"]
        code = data["card_code"]
        card_key = data["card_key"]

        try:
            unit = UserCard.objects.get(id=cardID, code=code, card_key=card_key)
        except UserCard.DoesNotExist:
            unit = None

        return unit

# --------------------------------------------------------------------------------
# ----- Defaultní PIDy  ----------------------------------------------------------

class DefautPIDs(APICall):
    """
    An API method returning default car unit OBD2 PIDs
    """

    @process_request(pipe | parse_json | authenticate)
    def post(self, request, data):

        return {
            "pids":[
                [1, "Rychlost", "obd_speed", "010D1", "A", 0, 255, 1, 1],
                [2, "Otáčky", "obd_rpm", "010C2", "((A*256)+B)/4", 0, 6000, 1, 1],
                [3, "Pozice plynu", "obd_throttle", "01111", "(A*100)/255", 0, 100, 0, 0],
                [4, "Teplota motoru", "obd_engine_temp", "01051", "A-40", -40, 215, 0, 0],
                [5, "Airflow", "obd_airflow", "01102",  "((A*256)+B)/100", 0, 655, 0, 0]
            ]
        }