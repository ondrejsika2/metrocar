import datetime
from django.conf import settings
from django.contrib.auth.models import User

from metrocar.user_management.models import MetrocarUser, Deposit, Account, UserRegistrationRequest
from metrocar.invoices.models import UserInvoiceAddress


def create_user_admin_1(save=True):
    admin = MetrocarUser.objects.get_or_create(
        first_name="Michal" + str(MetrocarUser.objects.count()),
        last_name="Pecka",
        username='admin' + str(MetrocarUser.objects.count()),
        password='admin',
        date_of_birth=datetime.datetime.strptime('16Sep1990', '%d%b%Y'),
        is_superuser=True,
        is_staff=True,
        email='mpecka@mailinator.com',
        drivers_licence_number='0000000',
        gender='M',
        identity_card_number='123123123',
        primary_phone='000 000000000',
        language=settings.LANG_CHOICES[0][0],
    )[0]
    return admin


def create_user_1(save=True):
    user = MetrocarUser.objects.get_or_create(
        first_name="Josef",
        last_name="Novak",
        username="jnovak",
        password="password",
        date_of_birth=datetime.datetime.strptime('16Sep1990', '%d%b%Y'),
        email='jnovak@mailinator.com',
        drivers_licence_number='0000000',
        gender='M',
        identity_card_number='123123123',
        primary_phone='000 000000000',
        language=settings.LANG_CHOICES[0][0],
    )[0]
    if save:
        account = create_account(user)
        user.account = account
        user.save()
        create_invoice_address(user)
        create_deposit(account, 100000)
        user_registration_request = UserRegistrationRequest.objects.get_or_create(
            user=user
        )[0]
        user_registration_request.approved = True
        user_registration_request.save()

    return user


def create_invoice_address(user, save=True):
    return UserInvoiceAddress.objects.get_or_create(
        street='Testing alley',
        land_registry_number=4815,
        zip_code=78916,
        city='Portland',
        user=user
    )[0]


def create_account(user):
    return Account.objects.get_or_create(
        user=user,
    )[0]


def create_deposit(account, amount, comment='Testing deposit', **kwargs):
    return Deposit.objects.get_or_create(
        account=account,
        money_amount=amount,
        comment=comment,
        defaults=kwargs)[0]
