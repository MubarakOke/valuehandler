from rest_framework import permissions

class AdminPermissionOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.user_type == "Admin"
        except AttributeError:
            return False