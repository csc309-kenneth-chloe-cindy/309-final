from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
   
    def admin_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return False