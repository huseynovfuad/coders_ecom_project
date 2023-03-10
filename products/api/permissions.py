from rest_framework import permissions

class AccessPermission(permissions.BasePermission):
    message = 'You are not admin.'

    def has_permission(self, request, view):
        return request.user.email == "eli@gmail.com"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.company.user == request.user
