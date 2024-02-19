from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if obj.user == request.user:
    #         return True
    #     return False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False