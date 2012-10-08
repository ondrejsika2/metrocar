from django.contrib.auth.models import User


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


def create():
    return {
        'users': [create_admin()],
    }
