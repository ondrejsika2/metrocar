from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from metrocar.user_management.models import Account, MetrocarUser, UserRegistrationRequest


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admins to edit it.
    For others there is at least the read-only permissions
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsAdminUserOrOwner(permissions.BasePermission):
    """
    Object-level permission to only allow admins to list it, edit it
    + current logged user can view and edit yourself
    """

    def has_object_permission(self, request, view, obj):
        return request.user \
               and (request.user.id == obj.id or request.user.is_staff)


    def has_permission(self, request, view):
        if request.method == 'PATCH' \
                or request.method == 'PUT'\
                or request.method == 'DELETE':
            return True
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            account = Account.objects.filter(user=request.user)
            if account.id == obj.account.id:
                return True
        return False

    def has_permission(self, request, view):
        if request.method == 'PATCH' \
                or request.method == 'PUT'\
                or request.method == 'DELETE':
            return False

        if request.method == 'POST':
            return True

        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

class IsUserFullyActive(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'PATCH' \
                or request.method == 'POST'\
                or request.method == 'PUT'\
                or request.method == 'DELETE':
            user_registration_request = UserRegistrationRequest.objects.filter(
                user=request.user
            )
            if (user_registration_request.__len__()):
                return user_registration_request[0].approved
            else:
                return False
        return True
