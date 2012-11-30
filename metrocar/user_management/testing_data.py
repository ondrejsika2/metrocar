from django.conf import settings
from django.contrib.auth.models import User

from metrocar.user_management.models import MetrocarUser, Deposit, Account


def create_admin(username='admin', password='admin'):
    admin, created = User.objects.get_or_create(
        username=username,
        is_superuser=True,
        is_staff=True,
    )
    if created:
        admin.set_password(password)
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
        email=email or '%s@mailinator.com' % username,
        drivers_licence_number='0000000',
        gender='M',
        identity_card_number='0000000',
        primary_phone='000 000000000',
        language=settings.LANG_CHOICES[0][0],
    )
    user = MetrocarUser.objects.get_or_create(
        defaults=dict(defaults, **kwargs), **id)[0]
    user.set_password(password)
    user.save()
    return user


def create_deposit(username, amount, comment='Testing deposit', **kwargs):
    account = Account.objects.get(user__username=username)
    return Deposit.objects.get_or_create(
        account=account,
        money_amount=amount,
        comment=comment,
        defaults=kwargs)[0]


def create():
    return {
        'users': [
            create_admin(),
            create_user('test', 'test', 'John', 'Dope'),
        ],
        'deposits': [
            create_deposit('test', 9000),
        ]
    }
