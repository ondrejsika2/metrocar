from django.conf import settings
from django.contrib.auth.models import User

from metrocar.user_management.models import MetrocarUser, Deposit, Account
from metrocar.invoices.models import UserInvoiceAddress


def create_user_admin_1(save=True):
    admin = MetrocarUser(
        first_name="Michal" + str(MetrocarUser.objects.count()),
        last_name="Pecka",
        username='admin' + str(MetrocarUser.objects.count()),
        password='admin',
        is_superuser=True,
        is_staff=True,
        email='mpecka@mailinator.com',
        drivers_licence_number='0000000',
        gender='M',
        identity_card_number='123123123',
        primary_phone='000 000000000',
        language=settings.LANG_CHOICES[0][0],
    )
    if save:
        admin.save()
    return admin


def create_user_1(save=True):
    user = MetrocarUser(
        first_name="Josef" + str(MetrocarUser.objects.count()),
        last_name="Novak",
        username="jnovak" + str(MetrocarUser.objects.count()),
        password="password",
        email='jnovak@mailinator.com',
        drivers_licence_number='0000000',
        gender='M',
        identity_card_number='123123123',
        primary_phone='000 000000000',
        language=settings.LANG_CHOICES[0][0],
    )
    if save:
        user.save()
        create_invoice_address(user)
    return user


def create_invoice_address(user, save=True):
    user_invoice_address = UserInvoiceAddress(street='Testing alley', land_registry_number=4815, zip_code=78916,
                                              city='Portland', user=user)
    if save:
        user_invoice_address.save()
    return user_invoice_address


def create_deposit(username, amount, comment='Testing deposit', **kwargs):
    account = Account.objects.get(user__username=username)
    return Deposit.objects.get_or_create(
        account=account,
        money_amount=amount,
        comment=comment,
        defaults=kwargs)[0]
