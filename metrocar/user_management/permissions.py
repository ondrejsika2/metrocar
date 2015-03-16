from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


# class IsOwner(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         """
#         Read permissions are allowed to any request,
#         so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#         return True
#
#         Instance must have an attribute named `owner`.
#         return request.user and obj.user.id == request.user.id
#         """

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
