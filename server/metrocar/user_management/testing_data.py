from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from metrocar.user_management.models import MetrocarUser, Deposit, Account, UserRegistrationRequest
from metrocar.invoices.models import UserInvoiceAddress


def create_admin(username='admin', password='admin'):
    admin, created = User.objects.get_or_create(
        username=username,
        is_superuser=True,
        is_staff=True,
    )
    if created:
        admin.set_password(password)
        create_api_token_for_admin(admin)
        admin.save()
    return admin


def create_user(username, password, first_name, last_name, email=None, **kwargs):
    id = dict(username=username)

    if (User.objects.filter(**id).exists()
        and not MetrocarUser.objects.filter(**id).exists()):
        User.objects.get(**id).delete()

    defaults = dict(
        first_name=first_name,
        last_name=last_name,
        email=email or '%s.%s@google.com' % (first_name, last_name),
        drivers_licence_number='1873851470',
        gender='M',
        identity_card_number='200453854',
        primary_phone='723341678',
        language=settings.LANG_CHOICES[0][0],
        date_of_birth=datetime.strptime('16Sep1990', '%d%b%Y'),
        drivers_licence_image = "drivinglicence.jpg",
        identity_card_image = "identitycard.jpg",
    )
    user, created = MetrocarUser.objects.get_or_create(
        defaults=dict(defaults, **kwargs), **id)

    if created:
        user.set_password(password)
        user.save()
        create_invoice_address(user)
        create_api_token_for_user(user)
        user_registration_request = UserRegistrationRequest.objects.get_or_create(
            user=user
        )[0]
        user_registration_request.approved = True
        user_registration_request.save()

    return user


def create_invoice_address(user):
    UserInvoiceAddress.objects.create(street='Testing alley', land_registry_number=4815, zip_code=78916,
                                      city='Portland', user=user)

def create_api_token_for_user(user):
    Token.objects.get_or_create(user=user, key="25364cf4cc9fcf7d879ecaab7be78a3cec7b9b73")

def create_api_token_for_admin(user):
    Token.objects.get_or_create(user=user, key="15364cf4cc9fcf7d879ecaab7be78a3cec7b9b73")

def get_account(username):
    return Account.objects.get(user__username=username)

def create_deposit(username, amount, comment='Testing deposit', **kwargs):
    deposit, created = Deposit.objects.get_or_create(
        account=get_account(username),
        money_amount=amount,
        comment=comment,
        defaults=kwargs)
    if created:
        deposit.datetime = datetime.now() + timedelta(days=-100)
        deposit.save()


def create():
    return {
        'users': [
            create_admin(),
            create_user('user', 'password', 'John', 'Dope', 'jan.novak12345612@gmail.com'),
        ],
        'deposits': [
            create_deposit('user', 9000),
        ]
    }